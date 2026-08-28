---
name: visual-explainer
description: Create a disposable HTML visual explainer when the user or another workflow asks to visualize technical or structured information such as a diff, PR, spec, plan, architecture, or process.
---

# Visual explainer

Turn supplied context into one HTML page that a newcomer understands through pictures or diagrams. You own the visuals. The requester owns the research and the claims: keep what they assert, and keep facts, inferences, and unknowns visibly distinct when the source distinguishes them.

## Think in pictures first

Decide what the reader must see before writing HTML: the one idea to retain, and each relationship that carries the explanation. Draw every relationship whose shape carries meaning. A pipeline becomes connected steps, a matrix becomes a grid of yes/no cells, numeric thresholds become zones on a number line, containment becomes a scope tree, and a comparison becomes two aligned frames. When the subject changes a user-visible interface, a simplified UI mockup with real component names is the primary view, animated slowly when the behavior is dynamic.

Aim for 90% picture or diagrams, 10% text. Prose carries only what a picture cannot: why it matters. Keep a paragraph to two sentences.

Two anti-patterns matter most:

- Typeset text. Cards, tables, badges, and numbered lists of sentences are still prose. Redraw or merge away a section whose primary content is boxes of text.
- Retranscription. Once a picture shows the paths, delete the prose that walks through them again. Keep at most a caption that tells the reader what to notice.

## Keep it small

Match page length to the supplied reading budget, and honor a supplied main-path or appendix boundary. Skip glossaries, metadata records, and exhaustive inventories. Put worthwhile off-path detail in collapsed disclosures. Prefer a few large obvious shapes over many small nodes: the silhouette should reveal the structure before any label is read.

## Make the hierarchy readable

Give a primary diagram enough canvas to carry its section. Enlarge Mermaid output that leaves substantial unused space, with a scale cap that keeps a simple or narrow graph subordinate to the page. Diagram labels must render at least as large as `--fs-micro`. When that requires crowding, simplify the graph or use another pattern.

Use the page sans-serif stack for prose, headings, labels, controls, and diagram text. Reserve Maple Mono for source code, commands, paths, file trees, and syntax highlighting. Choose weights the selected font files provide: 400 for regular text and 600 or 700 for emphasis. Keep adjacent heading levels visibly distinct without making section headings compete with the page title.

## Produce

Start from [assets/template.html](assets/template.html): keep its tokens, base CSS, and loader script, replace all starter content, and set the requested language, or the source language otherwise. Every shape above has a copyable snippet in [assets/patterns.html](assets/patterns.html): copy it, swap the labels, and follow the comments. Select only the patterns the explanation needs. Add CSS only for a shape no snippet can express, using the existing `--fs-*` tokens for every font size. Escape all source text before inserting it into HTML.

Write to the supplied destination, or to a writable temporary directory otherwise, and return the exact path. Overwrite any file already at the destination without reading it: an earlier artifact is stale, and its stylesheet can reintroduce components the template no longer defines. The page must stay understandable without JavaScript: a failed renderer leaves readable source in place.

## Verify

Run [scripts/validate_artifact.py](scripts/validate_artifact.py) on the finished page, or read the script's checks and apply them by hand when Python is unavailable. Then scan the page once: a section whose primary content is prose is a defect. Fix what fails in one pass, and report any defect that remains.
