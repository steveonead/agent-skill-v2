#!/usr/bin/env python3
"""Validate structural contracts for a visual-artifact HTML file."""

from __future__ import annotations

import argparse
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


SUPPORTED_MERMAID = {
    "stateDiagram-v2",
    "sequenceDiagram",
    "classDiagram",
    "erDiagram",
    "xychart-beta",
}
FLOW_HEADER = re.compile(r"^(?:flowchart|graph)\s+(?:TD|TB|LR|BT|RL)$")


@dataclass
class Node:
    tag: str
    attrs: dict[str, str]
    line: int
    parent: "Node | None" = None
    children: list["Node"] = field(default_factory=list)
    text_parts: list[str] = field(default_factory=list)

    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())

    def text(self) -> str:
        parts = list(self.text_parts)
        for child in self.children:
            parts.append(child.text())
        return "".join(parts).strip()

    def descendants(self, tag: str | None = None) -> list["Node"]:
        found: list[Node] = []
        for child in self.children:
            if tag is None or child.tag == tag:
                found.append(child)
            found.extend(child.descendants(tag))
        return found


class ArtifactParser(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("document", {}, 1)
        self.stack = [self.root]
        self.comments: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {key: value or "" for key, value in attrs}, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].text_parts.append(data)

    def handle_comment(self, data: str) -> None:
        self.comments.append((self.getpos()[0], data))


def first(nodes: list[Node], tag: str | None = None, class_name: str | None = None) -> Node | None:
    for node in nodes:
        if tag is not None and node.tag != tag:
            continue
        if class_name is not None and class_name not in node.classes():
            continue
        return node
    return None


def validate_mermaid(root: Node, errors: list[str]) -> None:
    for diagram in [node for node in root.descendants() if "diagram" in node.classes()]:
        mermaid = first(diagram.descendants("pre"), class_name="mermaid")
        if mermaid is None:
            errors.append(f"line {diagram.line}: .diagram must contain pre.mermaid")
            continue
        source = mermaid.text()
        lines = [line.strip() for line in source.splitlines() if line.strip()]
        if not lines:
            errors.append(f"line {mermaid.line}: Mermaid source is empty")
            continue
        header = lines[0]
        keyword = header.split()[0]
        if not FLOW_HEADER.match(header) and keyword not in SUPPORTED_MERMAID:
            errors.append(f"line {mermaid.line}: unsupported Mermaid header {header!r}")
        if ";" in header:
            errors.append(f"line {mermaid.line}: Mermaid header must stand alone")
        parent = diagram.parent
        if parent is None:
            continue
        index = parent.children.index(diagram)
        caption = parent.children[index + 1] if index + 1 < len(parent.children) else None
        if caption is None or caption.tag != "p" or "diagram-cap" not in caption.classes() or not caption.text():
            errors.append(f"line {diagram.line}: .diagram must be followed by a nonempty p.diagram-cap")


def validate_flows(root: Node, errors: list[str]) -> None:
    flows = [node for node in root.descendants() if "data-flow" in node.attrs]
    for flow in flows:
        screens = [node for node in flow.descendants() if "data-screen" in node.attrs]
        ids = [node.attrs["data-screen"] for node in screens]
        if not screens:
            errors.append(f"line {flow.line}: data-flow has no screens")
            continue
        if len(ids) != len(set(ids)):
            errors.append(f"line {flow.line}: data-screen values must be unique within a flow")
        for screen in screens:
            if not screen.attrs.get("data-screen-title", "").strip():
                errors.append(f"line {screen.line}: data-screen-title is required")
            panels = [node for node in screen.descendants() if "data-state-panel" in node.attrs]
            panel_ids = [node.attrs["data-state-panel"] for node in panels]
            if len(panel_ids) != len(set(panel_ids)):
                errors.append(f"line {screen.line}: data-state-panel values must be unique within a screen")
            for panel in panels:
                if not panel.attrs.get("data-state-label", "").strip():
                    errors.append(f"line {panel.line}: data-state-label is required")
        start = flow.attrs.get("data-start", "")
        if start not in ids:
            errors.append(f"line {flow.line}: data-start must name a screen in the flow")
            continue
        graph = {screen_id: set() for screen_id in ids}
        for screen in screens:
            for trigger in [node for node in screen.descendants() if "data-goto" in node.attrs]:
                target = trigger.attrs["data-goto"]
                if target not in graph:
                    errors.append(f"line {trigger.line}: data-goto {target!r} has no screen in its flow")
                else:
                    graph[screen.attrs["data-screen"]].add(target)
        reached = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for target in graph[current] - reached:
                reached.add(target)
                queue.append(target)
        missing = sorted(set(ids) - reached)
        if missing:
            errors.append(f"line {flow.line}: screens unreachable from data-start: {', '.join(missing)}")


AC_ID = re.compile(r"AC-\d{2}")


def validate_stories(root: Node, errors: list[str]) -> None:
    stories = [node for node in root.descendants("article") if "story" in node.classes()]
    for story in stories:
        count_node = first(story.descendants(), class_name="story-count")
        grid = first(story.descendants(), class_name="ac-grid")
        criteria = [node for node in story.descendants() if "ac" in node.classes()]
        ids = set()
        if grid is None:
            errors.append(f"line {story.line}: story requires an .ac-grid criteria list")
        elif first(grid.descendants(), class_name="ac-head") is None:
            errors.append(f"line {grid.line}: .ac-grid requires one .ac-head row")
        for criterion in criteria:
            id_node = first(criterion.descendants(), class_name="ac-id")
            if id_node is None or not AC_ID.fullmatch(id_node.text()):
                errors.append(f"line {criterion.line}: each .ac needs an AC-NN .ac-id")
                continue
            ids.add(id_node.text())
            if criterion.attrs.get("data-ac") != id_node.text():
                errors.append(f"line {criterion.line}: .ac data-ac must equal its .ac-id")
        if count_node is None:
            errors.append(f"line {story.line}: story-count is required")
        else:
            match = re.search(r"\d+", count_node.text())
            if match is None or int(match.group()) != len(criteria):
                errors.append(f"line {count_node.line}: story-count must equal the number of .ac rows")
        # The picture carries the criteria that share its shape. The grid is the
        # complete list, so the picture references a subset of it.
        mermaid = first([node for node in story.descendants("pre") if "mermaid" in node.classes()])
        if mermaid is not None:
            for referenced in sorted(set(AC_ID.findall(mermaid.text())) - ids):
                errors.append(f"line {mermaid.line}: {referenced} has no .ac row in its story")
        for cell in [node for node in story.descendants() if "data-ac" in node.attrs and "ac" not in node.classes()]:
            if cell.attrs["data-ac"] not in ids:
                errors.append(f"line {cell.line}: data-ac {cell.attrs['data-ac']!r} has no .ac row in its story")


URL_ATTRS = ("href", "src", "xlink:href")
FORBIDDEN_ELEMENTS = {"iframe", "object", "embed", "form"}


def validate_active_content(root: Node, errors: list[str]) -> None:
    for node in root.descendants():
        for name in node.attrs:
            if name.startswith("on"):
                errors.append(f"line {node.line}: event-handler attribute {name!r} is not allowed")
        for attr in URL_ATTRS:
            value = node.attrs.get(attr)
            if value is None:
                continue
            compact = re.sub(r"\s+", "", value).lower()
            if compact.startswith("javascript:"):
                errors.append(f"line {node.line}: javascript: URL in {attr} is not allowed")
            if compact.startswith("data:text/html"):
                errors.append(f"line {node.line}: data:text/html URL in {attr} is not allowed")
        if node.tag in FORBIDDEN_ELEMENTS:
            errors.append(f"line {node.line}: {node.tag} element is not allowed")
        if node.tag == "script" and (node.parent is None or node.parent.tag != "body"):
            errors.append(f"line {node.line}: script is allowed only as a template-shipped direct child of body")


def validate_code_renderer(root: Node, source: str, errors: list[str]) -> None:
    code_blocks = [
        pre
        for pre in root.descendants("pre")
        if "mermaid" not in pre.classes() and pre.attrs.get("data-lang", "").strip()
    ]
    if not code_blocks:
        return
    required_markers = {
        "Shiki import": "from 'https://esm.sh/shiki@3'",
        "Shiki renderer": "codeToHtml(",
        "code-block selector": "pre[data-lang]",
    }
    for name, marker in required_markers.items():
        if marker not in source:
            errors.append(f"code blocks require the template {name}")
    if any(pre.attrs["data-lang"] in {"json", "ts", "tsx"} for pre in code_blocks):
        required_formatters = {
            "Prettier import": "https://esm.sh/prettier@3/standalone",
            "JSON formatter": "JSON.stringify(JSON.parse(code), null, 2)",
        }
        for name, marker in required_formatters.items():
            if marker not in source:
                errors.append(f"JSON or TypeScript code blocks require the template {name}")


def validate(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    parser = ArtifactParser()
    parser.feed(source)
    root = parser.root
    errors: list[str] = []

    for line, comment in parser.comments:
        if "ARTIFACT:" in comment or "SPEC:" in comment:
            errors.append(f"line {line}: unresolved placeholder")

    html = first(root.descendants("html"))
    if html is None or not html.attrs.get("lang", "").strip():
        errors.append("html lang is required")
    title = first(root.descendants("title"))
    heading = first(root.descendants("h1"))
    lede = first(root.descendants(), class_name="lede")
    if title is None or not title.text():
        errors.append("nonempty title is required")
    if heading is None or not heading.text():
        errors.append("nonempty h1 is required")
    if lede is None or not lede.text():
        errors.append("nonempty .lede summary is required")

    sections = root.descendants("section")
    section_ids = [node.attrs.get("id", "") for node in sections]
    if not sections:
        errors.append("at least one section is required")
    if any(not value for value in section_ids):
        errors.append("every section needs an id")
    if len(section_ids) != len(set(section_ids)):
        errors.append("section ids must be unique")
    for section in sections:
        if not section.attrs.get("data-title", "").strip():
            errors.append(f"line {section.line}: section data-title is required")
        if first(section.descendants("h2")) is None:
            errors.append(f"line {section.line}: section h2 is required")
        if section.descendants("script") or section.descendants("style"):
            errors.append(f"line {section.line}: authored sections cannot contain script or style")

    for pre in root.descendants("pre"):
        if "mermaid" in pre.classes():
            continue
        if "data-lang" not in pre.attrs or not pre.attrs["data-lang"].strip():
            errors.append(f"line {pre.line}: code pre requires data-lang")
        if first(pre.descendants("code")) is None:
            errors.append(f"line {pre.line}: code pre requires a code child")

    validate_mermaid(root, errors)
    validate_flows(root, errors)
    validate_stories(root, errors)
    validate_active_content(root, errors)
    validate_code_renderer(root, source, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    if not args.artifact.is_file():
        print(f"error: file not found: {args.artifact}", file=sys.stderr)
        return 2
    errors = validate(args.artifact)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"ok: {args.artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
