# Skill Mechanics

## Packaging

Name the skill folder and frontmatter `name` with the same lowercase hyphenated value.

Add `scripts/`, `references/`, or `assets/` when the workflow uses them. Keep agent instructions in `SKILL.md`, detailed knowledge in `references/`, deterministic repeated operations in `scripts/`, and output materials in `assets/`.

Treat `SKILL.md`, references, scripts, and assets as shared artifacts governed by the harness-agnostic default in `SKILL.md`. Keep their workflows independent of native metadata and configuration.

## Invocation

Determine whether the skill is **user-invoked** or **model-invoked** from the user's explicit choice or governing requirements, independent of the skill name or naming prefix. Confirm that choice before creating the skill or changing its invocation.

- A **user-invoked** skill is reached explicitly by the human. Set `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
- A **model-invoked** skill is discoverable by the agent and other skills. Set `user-invocable: false` in `SKILL.md` and keep `policy.allow_implicit_invocation: true` in `agents/openai.yaml`.

Codex has no documented metadata field that blocks explicit `$skill` invocation while allowing implicit invocation. For a model-invoked skill, `allow_implicit_invocation: true` records the intended policy but cannot enforce the human-invocation restriction in Codex.

Before writing native metadata, check the current official specification for each target. Use only documented fields and preserve unrelated supported metadata.

Split a model-invoked skill when a distinct leading word should trigger the new branch independently or another skill must reach it. Each split adds an always-loaded description, so independent reach must justify that load.

When many user-invoked skills become difficult to remember, create one user-invoked router that names them and explains when the human should choose each one.

## Frontmatter

Write `SKILL.md` frontmatter with fields supported by the current official specification. Keep `name` and `description` in English. Include optional fields only when the skill's behavior requires them.

Include `argument-hint` only when the skill accepts invocation arguments. Write it in Traditional Chinese (zh-TW) as autocomplete placeholders rather than an instruction sentence:

```yaml
argument-hint: "[議題編號] [輸出格式]"
```

Use this shape for a model-invoked skill:

```yaml
---
name: skill-name
description: Leading-word description that names each trigger branch.
user-invocable: false
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

For a model-invoked skill, keep discovery triggers in the description. For a user-invoked skill, keep the description as a concise human-facing summary. Reserve the body for post-invocation instructions.

## `agents/openai.yaml` metadata

Write `agents/openai.yaml` from the current official OpenAI specification. Use only documented fields and write every string value in English. Set `interface.display_name` to the exact `name` from `SKILL.md`. Quote string values:

```yaml
interface:
  display_name: "skill-name"
  short_description: "A brief picker summary"
  default_prompt: "Use $skill-name to perform a representative task."
```

Add this block for a user-invoked skill:

```yaml
policy:
  allow_implicit_invocation: false
```

Add this block for a model-invoked skill:

```yaml
policy:
  allow_implicit_invocation: true
```

Add icons, brand color, and dependencies when the user supplies them or the workflow requires them. Keep the display name, summary, prompt, and invocation policy aligned with `SKILL.md`.
