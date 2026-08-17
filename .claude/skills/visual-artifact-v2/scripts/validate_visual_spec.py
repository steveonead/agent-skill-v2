#!/usr/bin/env python3
"""Validate the additional profile for a visual-artifact-v2 HTML file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_artifact import ArtifactParser, Node, first, validate as validate_base


US_ID = re.compile(r"US-\d{2}")
AC_ID = re.compile(r"AC-\d{2}")
RESPONSE_HEAD = re.compile(r"^Response\s+(\d{3})$")
NO_PARAMS = re.compile(r"no\s+parameters|無參數|沒有參數", re.IGNORECASE)
REQUIRED_SECTIONS = ("overview", "open-items")


def validate_sections(root: Node, errors: list[str]) -> None:
    section_ids = {node.attrs.get("id", "") for node in root.descendants("section")}
    for required in REQUIRED_SECTIONS:
        if required not in section_ids:
            errors.append(f"spec requires a section with id {required!r}")


def validate_story_ids(root: Node, errors: list[str]) -> None:
    stories = [node for node in root.descendants("article") if "story" in node.classes()]
    if not stories:
        return
    seen: dict[str, int] = {}
    for story in stories:
        id_node = first(story.descendants(), class_name="story-id")
        if id_node is None or not US_ID.fullmatch(id_node.text()):
            errors.append(f"line {story.line}: each .story needs a US-NN .story-id")
            continue
        story_id = id_node.text()
        if story_id in seen:
            errors.append(f"line {id_node.line}: duplicate story id {story_id} (first at line {seen[story_id]})")
        else:
            seen[story_id] = id_node.line


def validate_criteria(root: Node, errors: list[str]) -> None:
    criteria = [node for node in root.descendants() if "ac" in node.classes()]
    seen: dict[str, int] = {}
    for criterion in criteria:
        id_node = first(criterion.descendants(), class_name="ac-id")
        if id_node is None or not AC_ID.fullmatch(id_node.text()):
            continue  # the base validator already reports a missing or malformed .ac-id
        ac_id = id_node.text()
        if ac_id in seen:
            errors.append(f"line {id_node.line}: duplicate criterion id {ac_id} (first at line {seen[ac_id]})")
        else:
            seen[ac_id] = id_node.line
        for beat in ("given", "when", "then"):
            beat_node = first(
                [node for node in criterion.descendants() if "beat" in node.classes()],
                class_name=beat,
            )
            if beat_node is None or not beat_node.text():
                errors.append(f"line {criterion.line}: {ac_id} needs a nonempty .beat.{beat}")


def heading_segments(body: Node) -> list[tuple[Node, list[Node]]]:
    """Pair each h4 in an .acc-body with the nodes that follow it, up to the next h4."""
    ordered = body.descendants()
    positions = [index for index, node in enumerate(ordered) if node.tag == "h4"]
    segments: list[tuple[Node, list[Node]]] = []
    for count, position in enumerate(positions):
        end = positions[count + 1] if count + 1 < len(positions) else len(ordered)
        segments.append((ordered[position], ordered[position + 1 : end]))
    return segments


def segment_has_payload(nodes: list[Node]) -> bool:
    return any(node.tag == "pre" and node.attrs.get("data-lang", "").strip() for node in nodes)


def validate_api(root: Node, errors: list[str]) -> None:
    ledgers = [node for node in root.descendants() if "ledger" in node.classes()]
    for ledger in ledgers:
        for entry in ledger.descendants("details"):
            summary = first(entry.descendants("summary"))
            if summary is None:
                errors.append(f"line {entry.line}: ledger entry needs a summary")
                continue
            verb = first(summary.descendants(), class_name="verb")
            path_node = first(summary.descendants(), class_name="path")
            if verb is None or path_node is None or not path_node.text():
                errors.append(f"line {entry.line}: ledger summary needs a .verb and a nonempty .path")
                continue
            label = path_node.text()
            body = first(entry.descendants(), class_name="acc-body")
            if body is None:
                errors.append(f"line {entry.line}: {label}: ledger entry needs an .acc-body")
                continue
            segments = heading_segments(body)
            headings = {segment[0].text(): segment[1] for segment in segments}
            if "fn" in verb.classes():
                signature = headings.get("Signature")
                if signature is None or not segment_has_payload(signature):
                    errors.append(f"line {body.line}: {label}: symbol entry needs a Signature code block")
            else:
                parameters = headings.get("Parameters")
                if parameters is not None:
                    if first(parameters, tag="table") is None:
                        errors.append(f"line {body.line}: {label}: Parameters heading needs a table")
                elif not NO_PARAMS.search(body.text()):
                    errors.append(
                        f"line {body.line}: {label}: endpoint needs a Parameters block or an explicit no-parameters marker"
                    )
            statuses: dict[str, int] = {}
            for heading, segment in segments:
                match = RESPONSE_HEAD.match(heading.text())
                if match is None:
                    continue
                status = match.group(1)
                if status in statuses:
                    errors.append(f"line {heading.line}: {label}: duplicate Response {status} heading")
                statuses[status] = heading.line
                if not segment_has_payload(segment):
                    errors.append(f"line {heading.line}: {label}: Response {status} needs a payload example block")


def validate_spec(path: Path) -> list[str]:
    errors = validate_base(path)
    parser = ArtifactParser()
    parser.feed(path.read_text(encoding="utf-8"))
    root = parser.root
    validate_sections(root, errors)
    validate_story_ids(root, errors)
    validate_criteria(root, errors)
    validate_api(root, errors)
    # Wireframe start screens and data-goto resolution are enforced by the base
    # flow checks that validate_base already ran.
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    if not args.artifact.is_file():
        print(f"error: file not found: {args.artifact}", file=sys.stderr)
        return 2
    errors = validate_spec(args.artifact)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"ok: {args.artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
