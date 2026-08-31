# Authoring Rules

## Render brief

Normalize caller context into this internal brief, deriving every field from the supplied material.

| Field | Requirement | Rule |
| --- | --- | --- |
| `title` | Required | Use a literal subject name. When the subject cannot be inferred, use `Untitled Artifact`. |
| `summary` | Required | State what the artifact explains in one sentence. When a supported summary cannot be inferred, state that context is missing. |
| `language` | Required | Default to `zh-TW`. Preserve code, identifiers, API names, and quotations. |
| `output` | Required | Use the caller path or the default path from [`SKILL.md` Step 3](../SKILL.md#step-3-resolve-the-output). |
| `product` | Optional | Show when supplied or evident from the material. |
| `artifact_type` | Optional | Examples include `Spec`, `Review`, `Architecture`, and `Explainer`. |
| `status` | Optional | Examples include `Draft`, `Proposed`, and `Final`. |
| `date` | Optional | Use the generation date unless the material names another relevant date. |
| `source` | Optional | A file, issue, symbol, commit, or URL that anchors the material. |
| `sections` | Required | An ordered inventory of content and the relationships each item carries. |

## Content boundary

Perform editorial transformation. Reorder sections, shorten repetition, name implicit relationships, and replace prose with a catalog component when the component improves comprehension. Keep every factual statement within the supplied material.

Use these claim states:

| State | Meaning |
| --- | --- |
| `verified` | The supplied material establishes the claim as current fact. |
| `proposed` | The claim describes an intended change or recommendation. |
| `assumption` | The claim is an inference needed to explain the material. |
| `unknown` | The material leaves the claim unresolved. |

Attach a source line to a claim when the material supplies one.

## Shell contract

Every authored section uses this shape:

```html
<section id="stable-english-id" data-title="目錄標題">
  <div class="sec-head">
    <h2>章節標題</h2>
    <span class="eyebrow">Section kind</span>
  </div>
  <!-- Catalog components or prose -->
</section>
```

Write section IDs in lowercase kebab-case. Include an optional metadata element only when the material supplies its value.

The template contains the only authored `<style>` and executable `<script>` blocks. Compose sections with markup, catalog classes, `data-*` attributes, and Mermaid source. Catalog prose is the authoring contract. The validator enforces its machine-checkable subset.

## Component choice

Choose by information relationship:

| Relationship | Component |
| --- | --- |
| Definition, scope, or one constraint | Note or prose |
| Current fact, recommendation, inference, or gap | Evidence note |
| Included and excluded work | Goals and out of scope |
| Two versions or two options | Comparison |
| Ordered stages without branching | Timeline |
| Options against shared criteria | Decision matrix |
| One outcome varying along two axes | Rule matrix |
| A few categorical states | Status summary |
| A few important quantities | Metric summary |
| Repeated fields or exact mappings | Data table |
| Nodes connected by edges | Mermaid diagram |
| Source text or executable shape | Code block |
| Optional detail | Disclosure |

Prefer prose for a single fact or a one-step action. A visual component must expose a relationship that is harder to scan in prose.

## Diagram readability

Keep Mermaid diagrams readable at their natural size. Favor a layout with few branches per rank.
