#!/usr/bin/env python3

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


MIN_FONT_SIZE_PX = 16.0
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
FONT_DECLARATION = re.compile(r"(?:^|;)\s*font(?:-size)?\s*:", re.IGNORECASE)
HIDDEN_DECLARATION = re.compile(
    r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)\b",
    re.IGNORECASE,
)
FS_TOKEN = re.compile(r"(--fs-[\w-]+)\s*:\s*([^;}{]+)", re.IGNORECASE)
FONT_SIZE = re.compile(r"font-size\s*:\s*([^;}{]+)", re.IGNORECASE)
TOKEN_REFERENCE = re.compile(r"^var\(\s*(--fs-[\w-]+)\s*\)$", re.IGNORECASE)
CSS_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)
TEMPLATE_PLACEHOLDERS = (
    "Topic / context",
    "One clear idea",
    "State the conclusion",
    "Show the relationship",
    "Replace this starter component",
)


class ArtifactParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.stack = []
        self.style_blocks = []
        self.scripts = []
        self.title_parts = []
        self.inline_fonts = []
        self.starter_lines = []
        self.wrappers = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        frame = {
            "tag": tag,
            "classes": classes,
            "wrapper": None,
            "script": tag == "script",
        }

        if tag == "html":
            self.lang = attributes.get("lang", "").strip()
        if "data-visual-explainer-starter" in attributes:
            self.starter_lines.append(self.getpos()[0])

        style = attributes.get("style", "")
        if FONT_DECLARATION.search(style):
            self.inline_fonts.append(self.getpos()[0])

        kind = None
        if "js-mermaid" in classes:
            kind = "mermaid"
        elif "js-shiki" in classes:
            kind = "shiki"

        if kind:
            wrapper = {
                "kind": kind,
                "line": self.getpos()[0],
                "has_source": False,
                "has_output": False,
                "source_hidden": False,
                "source_text": [],
            }
            frame["wrapper"] = wrapper
            self.wrappers.append(wrapper)

        active = self._active_wrapper(frame)
        if active:
            source_class = "diagram-source" if active["kind"] == "mermaid" else "code-source"
            output_class = "diagram-output" if active["kind"] == "mermaid" else "code-output"
            if source_class in classes:
                active["has_source"] = True
                active["source_hidden"] = (
                    "hidden" in attributes or bool(HIDDEN_DECLARATION.search(style))
                )
            if output_class in classes:
                active["has_output"] = True

        if tag not in VOID_ELEMENTS:
            self.stack.append(frame)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        tags = {frame["tag"] for frame in self.stack}
        if "style" in tags:
            self.style_blocks.append(data)
        if "title" in tags:
            self.title_parts.append(data)
        if any(frame["script"] for frame in self.stack):
            self.scripts.append(data)

        wrapper = self._active_wrapper()
        if not wrapper:
            return
        source_class = "diagram-source" if wrapper["kind"] == "mermaid" else "code-source"
        if any(source_class in frame["classes"] for frame in self.stack):
            wrapper["source_text"].append(data)

    def _active_wrapper(self, pending=None):
        frames = self.stack + ([pending] if pending else [])
        for frame in reversed(frames):
            if frame and frame["wrapper"]:
                return frame["wrapper"]
        return None


def _top_level_dynamic_imports(script):
    positions = []
    depth = 0
    index = 0
    state = "code"
    quote = None

    while index < len(script):
        char = script[index]
        next_char = script[index + 1] if index + 1 < len(script) else ""

        if state == "line_comment":
            if char == "\n":
                state = "code"
            index += 1
            continue
        if state == "block_comment":
            if char == "*" and next_char == "/":
                state = "code"
                index += 2
            else:
                index += 1
            continue
        if state == "string":
            if char == "\\":
                index += 2
            elif char == quote:
                state = "code"
                index += 1
            else:
                index += 1
            continue

        if char == "/" and next_char == "/":
            state = "line_comment"
            index += 2
            continue
        if char == "/" and next_char == "*":
            state = "block_comment"
            index += 2
            continue
        if char in {'"', "'", "`"}:
            state = "string"
            quote = char
            index += 1
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth = max(0, depth - 1)
        elif script.startswith("import", index):
            before = script[index - 1] if index else ""
            after = script[index + 6] if index + 6 < len(script) else ""
            if not (before.isalnum() or before in "_$") and not (
                after.isalnum() or after in "_$"
            ):
                cursor = index + 6
                while cursor < len(script) and script[cursor].isspace():
                    cursor += 1
                if cursor < len(script) and script[cursor] == "(" and depth == 0:
                    positions.append(index)
        index += 1

    return positions


def audit(path):
    source = path.read_text(encoding="utf-8")
    parser = ArtifactParser()
    parser.feed(source)
    errors = []

    if not parser.lang or parser.lang.lower() == "und":
        errors.append("set <html lang> to the artifact's concrete language")
    if not "".join(parser.title_parts).strip():
        errors.append("add a non-empty <title>")
    for line in parser.starter_lines:
        errors.append(f"line {line}: replace template placeholders and remove the starter marker")
    for placeholder in TEMPLATE_PLACEHOLDERS:
        if placeholder.casefold() in source.casefold():
            errors.append(f"replace template placeholder {placeholder!r}")
    for line in parser.inline_fonts:
        errors.append(f"line {line}: move inline font declarations into a shared token or class")

    css = "\n".join(parser.style_blocks)
    tokens = {}
    for match in FS_TOKEN.finditer(css):
        name, value = match.group(1), match.group(2).strip()
        tokens[name.lower()] = value
        pixel_value = re.fullmatch(r"([0-9]*\.?[0-9]+)px", value, re.IGNORECASE)
        if not pixel_value:
            errors.append(f"font token {name} must use a fixed px value of at least 16px")
        elif float(pixel_value.group(1)) < MIN_FONT_SIZE_PX:
            errors.append(f"font token {name} is below {MIN_FONT_SIZE_PX:g}px")

    for match in FONT_SIZE.finditer(css):
        value = match.group(1).strip()
        reference = TOKEN_REFERENCE.fullmatch(value)
        if not reference:
            errors.append(f"font-size '{value}' must use a --fs-* token")
        elif reference.group(1).lower() not in tokens:
            errors.append(f"font-size references undefined token {reference.group(1)}")

    for match in CSS_RULE.finditer(css):
        selector, declarations = match.group(1), match.group(2)
        if not HIDDEN_DECLARATION.search(declarations):
            continue
        for branch in selector.split(","):
            targets_source = ".diagram-source" in branch or ".code-source" in branch
            if targets_source and ".is-rendered" not in branch:
                errors.append("source fallbacks may be hidden only under an .is-rendered selector")
            rightmost = re.split(r"\s+|[>+~]", branch.strip())[-1]
            if ".js-mermaid" in rightmost or ".js-shiki" in rightmost:
                errors.append("do not hide optional-renderer wrappers")

    for wrapper in parser.wrappers:
        label = f"line {wrapper['line']}: {wrapper['kind']} wrapper"
        if not wrapper["has_source"]:
            errors.append(f"{label} is missing its source fallback element")
        elif not "".join(wrapper["source_text"]).strip():
            errors.append(f"{label} has an empty source fallback")
        elif wrapper["source_hidden"]:
            errors.append(f"{label} hides its source fallback before rendering succeeds")
        if not wrapper["has_output"]:
            errors.append(f"{label} is missing its output element")

    scripts = "\n".join(parser.scripts)
    if _top_level_dynamic_imports(scripts):
        errors.append("load optional libraries inside a renderer after finding a render target")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate a visual-explainer HTML artifact.")
    parser.add_argument("artifacts", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False

    for path in args.artifacts:
        try:
            errors = audit(path)
        except (OSError, UnicodeError) as error:
            errors = [str(error)]

        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
