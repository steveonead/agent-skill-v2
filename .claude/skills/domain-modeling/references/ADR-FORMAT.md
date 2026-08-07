# ADR Content Rules

Require the minimum paragraph to state the context, decision, and rationale. Replace generic claims such as `best practice` or `最佳實踐` with the concrete driver or tradeoff that justified the decision.

Add material only when it preserves useful information that the minimum paragraph cannot carry:

- Add status frontmatter when the lifecycle matters: `proposed`, `accepted`, `deprecated`, or `superseded by ADR-NNNN`.
- Add the language template's considered-options heading when future maintainers need the rejected alternatives and their material differences.
- Add the language template's consequences heading when non-obvious downstream effects need explicit ownership or follow-up.

Finish when the ADR states context, decision, and rationale, and every optional section adds information needed by future maintainers.
