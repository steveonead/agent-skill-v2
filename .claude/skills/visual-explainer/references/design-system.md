# Design system

## Character

Build a technical editorial page, not a dashboard, slide deck, or marketing site. The page should feel calm, direct, and inspectable. Visual structure carries the explanation. Prose connects it at the length the content needs.

Use these principles in order:

1. Show the whole before the parts.
2. Give each section one primary idea.
3. Make relationships spatial when space explains them better than prose.
4. Use labels that state meaning, not interface mechanics.
5. Remove any decoration that does not encode information.

## Tokens

The template defines the canonical color tokens. Use those roles consistently. The primary accent may change to suit the subject. Keep the neutral and semantic roles stable.

The page background is paper. Explanatory surfaces are near-white. Use sunk gray for subordinate regions. Ink carries titles and important structure. Accent identifies the main path. Positive, danger, and warning colors keep their semantic meaning.

Do not add gradients, decorative blobs, translucent effects, or a second dominant hue. Favor fine rules and flat surfaces over shadows. Corners stay square or use a radius no larger than 4px.

## Type

Use the system sans stack from the template for body prose and Mermaid labels. Use Maple Mono NF CN for code, identifiers, file paths, metrics, compact metadata labels, and HTML diagram nodes.

Use the template's type tokens for every fixed size. The minimum is `--fs-micro` at 16px. Body copy starts at `--fs-body` at 18px, the lead uses `--fs-lead` at 23px, section titles use `--fs-section-title` at 38px, and the page title uses `--fs-title` at 46px. Keep letter spacing at zero and keep type sizes independent of viewport width. Add a semantic token when a custom component needs a size that the existing roles cannot express. Do not use inline `font-size` declarations.

Use bold weight to create hierarchy before adding color. Keep prose line length near 36em for Chinese and mixed-language text. Inside compact components, use smaller headings that fit the component rather than page-level display type.

Apply `text-wrap: pretty` to natural-language headings, prose, list and table text, captions, and explanatory labels. Keep preformatted code, diagram source, rendered diagram labels, and atomic status tags outside this rule. Prefer natural wrapping and separate paragraphs over manual line breaks. Use a manual line break only when the break itself communicates structure.

## Page rhythm

Use one vertical editorial column with a maximum content width near 1200px. Design for a minimum viewport width of 1280px and use 1440 x 900 as the baseline. A typical artifact begins with:

```text
eyebrow
large literal title
focused thesis
overall mental model
--------------------------------
progressive detail sections
--------------------------------
evidence and source notes
```

Let the first viewport establish the topic, thesis, and at least the beginning of the mental model. Use generous whitespace between sections and tighter spacing inside a single idea. Sections are unframed page bands. Reserve bordered surfaces for individual repeated items, code, diagrams, and genuine callouts.

Treat the baseline desktop viewport as the artifact's layout target. Responsive variants and accessibility auditing are outside the completion criteria.

Use one left edge across the page. Align section kickers, headings, cards, tables, code, and diagrams to it. Stack each section kicker above its heading and supporting copy instead of indenting the heading.

Never put a card inside another card. Do not turn every paragraph into a panel.

## Pictures and density

Prefer a small number of large, obvious shapes over many tiny nodes. A reader should understand the broad relationship before reading labels.

Apply the renderer, node, text-density, and width constraints while selecting components and before drafting their contents. Split excess detail into prose, a table, or a later section instead of shrinking labels or crowding a visual.

Treat these as warning signs, not hard limits:

- A diagram with more than nine visible nodes probably needs grouping or progressive disclosure.
- A card with more than two short paragraphs probably contains more than one idea.
- A section with multiple competing accent colors has lost its hierarchy.
- A diagram that needs a legend for basic reading may be too abstract.

After the central relationships have literal views, preserve remaining text-heavy detail with full-width vertical rows instead of shortened, shrunken, or crowded text.

Use the compact diagram variant when a small linear or low-node diagram does not need reserved vertical space. Apply `.is-compact` to remove the diagram minimum height and reduce its padding. Keep the default diagram spacing for larger graphs and diagrams whose visual weight carries the section.

Use inline SVG for simple custom pictures when HTML and CSS cannot express the shape cleanly. Keep strokes, fills, labels, and semantic colors aligned with the tokens.

## Interaction and motion

Use interaction only to reduce simultaneous complexity. Appropriate patterns are disclosure, a before-and-after toggle, flow focus, and necessary tabs.

Animate only when motion encodes direction, state change, or time. Do not add entrance animation, scroll effects, parallax, or decorative motion.
