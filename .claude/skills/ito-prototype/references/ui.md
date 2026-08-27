# UI prototype

Use this branch when the question concerns a page's layout, information hierarchy, or primary interaction. Produce several structurally different variants on one route so the user can compare them in the real application context.

## Choose the host

Prefer an existing page. Keep its authentication, parameters, data fetching, surrounding navigation, and realistic content density. Replace only the rendered region under evaluation.

Create a new prototype route only when no existing page can host the proposed UI. Follow the project's routing conventions and include `prototype` in the route or filename.

## Define the variants

Create three variants by default and limit the comparison to five. State the plan in a top-of-file comment, including the number of variants, the target page or region, and the `?variant=` parameter.

Make variants disagree about structure, information hierarchy, and primary affordance. Changes limited to color, copy, or small card arrangements do not count. Redesign a variant when it remains structurally similar to another.

Use the project's existing components and styling system. Give every variant a clear exported name. Share surrounding application components, but let each variant own the layout being compared.

Use real read-only data where the host page already provides it. Stub mutations and unavailable services in memory. The prototype evaluates the UI direction, not backend behavior.

## Wire the comparison

Select the active variant from the `variant` URL search parameter. Make every variant available on the same route and render only the selected variant. Preserve the parameter across reloads and make each variant directly shareable.

Add one shared switcher fixed at the bottom center of the viewport. It contains:

- a previous control that wraps to the last variant
- the current variant key and descriptive name
- a next control that wraps to the first variant

Update the URL through the project's router. Support the left and right arrow keys, except while an input, textarea, or editable element has focus. Make the switcher visually distinct from the UI under evaluation.

## Evaluate it

Give the user the route, each `?variant=` URL, and the question being answered. Let the user choose one direction or identify parts to combine. Revise variants when the comparison does not expose a meaningful design choice.

The UI prototype is complete when the variants expose distinct tradeoffs and the user can state a preferred direction with reasons. Return to [SKILL.md](../SKILL.md) to record the verdict and preserve the prototype.
