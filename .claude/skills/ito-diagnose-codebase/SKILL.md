---
name: ito-diagnose-codebase
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then batch-grill through whichever one you pick.
argument-hint: "[模組、子系統或架構痛點]"
disable-model-invocation: true
---

# Diagnose Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

- Invoke `codebase-design` for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion. Refer to modules, interfaces, and seams instead of components, services, APIs, or boundaries.
- Invoke `domain-modeling` to locate the applicable domain-context files and ADRs. Their domain language gives names to good seams. Treat their decisions as settled unless new evidence warrants revisiting them.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the applicable domain-context files and any ADRs in the area you're touching first.

Then spawn a sub-agent to walk the codebase. Explore organically instead of following rigid heuristics, and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a single HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user with an available browser or file-opening capability and tell them the absolute path. When no opener is available, report the path without opening it.

Write every user-visible report string in Traditional Chinese (zh-TW). Keep code identifiers and the canonical `codebase-design` terms in English. The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals: use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: concise Traditional Chinese description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram**: side-by-side, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `強烈建議`, `值得探索`, `推測性建議`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use the project's domain vocabulary and the `codebase-design` vocabulary for the architecture.** If the domain model defines "Order," talk about "Order 接單 module" rather than "FooBarHandler" or "Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"與 ADR-0007 衝突，但值得重新檢視，因為……"_). List only conflicts that pass this threshold.

Before writing the report, read [assets/html-report.md](assets/html-report.md) in full and follow its scaffold, diagram patterns, and styling guidance.

Stop before interface design. After the file is written, ask the user: "你想深入探索哪一個候選項目？"

### 3. Batch-grilling loop

Once the user picks a candidate, invoke `batch-grilling` to walk the decision tree with them in rounds: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

During the rounds, track proposed domain-context and ADR changes without writing them. After `batch-grilling` reaches shared understanding and the user confirms it, invoke `domain-modeling` to apply the confirmed changes:

- **Naming a deepened module after a concept not in the applicable domain context?** Add the confirmed term to that context. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Add the confirmed definition to the applicable domain context.
- **User rejects the candidate with a load-bearing reason?** During the rounds, offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Record it after confirmation only when the user accepts and a future explorer would need the reason to avoid suggesting the same change again. Ephemeral reasons ("not worth it right now") and self-evident reasons do not qualify.
- **Want to explore alternative interfaces for the deepened module?** Invoke `codebase-design` and use its design-it-twice parallel sub-agent pattern.
