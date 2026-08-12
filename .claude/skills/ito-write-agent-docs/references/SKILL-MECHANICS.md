# Skill Mechanics

## Packaging

Name the skill folder and frontmatter `name` with the same lowercase hyphenated value.

Add `agents/openai.yaml` for Codex UI metadata. Add `scripts/`, `references/`, or `assets/` when the workflow uses them. Keep agent instructions in `SKILL.md`, detailed knowledge in `references/`, deterministic repeated operations in `scripts/`, and output materials in `assets/`.

## Invocation

- A **model-invoked** skill is discoverable by the agent and by other skills. Its description is an always-loaded context pointer, so it earns concise trigger coverage for every distinct branch. Omit `disable-model-invocation` and allow implicit invocation in `agents/openai.yaml`.
- A **user-invoked** skill is reached explicitly by the human. It spends cognitive load instead of permanent context load. Set `disable-model-invocation: true`, keep the description to a human-facing one-line summary, and set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

Choose model invocation when the agent or another skill must discover the workflow without a human naming it. A user can still invoke a model-invoked skill explicitly.

Split a model-invoked skill when a distinct leading word should trigger the new branch independently or another skill must reach it. Each split adds an always-loaded description, so independent reach must justify that load.

When many user-invoked skills become difficult to remember, create one user-invoked router that names them and explains when the human should choose each one.

## Frontmatter

Use this shape for a model-invoked skill:

```yaml
---
name: skill-name
description: Leading-word description that names each trigger branch.
---
```

Use this shape for a user-invoked skill:

```yaml
---
name: skill-name
description: One-line human-facing summary.
disable-model-invocation: true
---
```

Keep discovery triggers in the description. Reserve the body for post-invocation instructions.

## Codex metadata

Write `agents/openai.yaml` with quoted string values:

```yaml
interface:
  display_name: "same-as-the-skill-name"
  short_description: "A brief picker summary"
  default_prompt: "Use $skill-name to perform a representative task."
```

Add this block for a user-invoked skill:

```yaml
policy:
  allow_implicit_invocation: false
```

Add icons, brand color, and dependencies when the user supplies them or the workflow requires them. Keep the display name, summary, prompt, and invocation policy aligned with `SKILL.md`.
