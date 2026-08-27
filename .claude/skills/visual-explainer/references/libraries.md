# Libraries

[The template](../assets/template.html) is the source of truth for library versions, browser URLs, and the font stylesheet. Preserve those pins unless the requester explicitly asks for an update. Keep the local font fallback stack so font delivery cannot make the artifact unreadable.

## Boundaries

Beautiful Mermaid is for relationships whose edges carry meaning, such as sequence, state, dependency, and branching flow diagrams. Prefer HTML and CSS for linear steps, comparisons, ledgers, metrics, and simple maps. Use the shared theme object in the template. The initializer removes Beautiful Mermaid's remote font import so diagrams use the artifact's local system font. The template imports the library only when a `.js-mermaid` target exists.

### Beautiful Mermaid 1.1.3 boundaries

These behaviors have been verified in the browser for the pinned version:

| Capability | Observed behavior |
| --- | --- |
| `flowchart`, `stateDiagram-v2`, and `erDiagram` | Render successfully |
| `classDef` with `class` assignments | Applies custom node styling |
| Line breaks inside node labels | Do not render reliably. `<br/>` collapses and a source newline can create another node |
| `erDiagram` field comments | Do not appear in the rendered diagram |
| Parallel Mermaid diagrams for Before / After | Size and lay out independently, so corresponding content does not align reliably |

Keep every Mermaid node label short and on one line. Put explanatory text outside the diagram.

Shiki is for short code or diff evidence. Keep an escaped plain-text fallback in the document. The template hides that fallback only after highlighting succeeds and imports Shiki only when a `.js-shiki` target exists. Preserve the template's Vitesse Light and Vitesse Dark dual-theme configuration with `defaultColor: false`. Apply the emitted `--shiki-light` and `--shiki-dark` variables through the template CSS. Keep the page palette light in both system modes. Only code blocks follow the system setting.

## Markup conventions

For Mermaid, place escaped source in the fallback element:

```html
<div class="diagram js-mermaid">
  <pre class="diagram-source">flowchart LR
    A[Input] --&gt; B[Result]</pre>
  <div class="diagram-output"></div>
</div>
```

For Shiki, use the same fallback-first structure:

```html
<div class="code-frame js-shiki" data-lang="typescript">
  <pre class="code-source">const result = explain(input);</pre>
  <div class="code-output"></div>
</div>
```

The template reads `textContent`, renders into the output element, and marks the wrapper as rendered only after success.
