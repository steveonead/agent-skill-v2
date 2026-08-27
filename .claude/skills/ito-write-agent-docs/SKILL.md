---
name: ito-write-agent-docs
description: "Create or edit the documents a coding agent consumes: SKILL.md, AGENTS.md, CLAUDE.md, and the reference files they point to. Use when writing a new skill, revising an existing skill's purpose, behavior, description, or invocation, or when an agent document produces unreliable behavior. For human-facing README or product docs, write them directly instead."
argument-hint: "想寫或改哪份文件？加 --grill 先釐清設計。"
---

Write `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `agents/openai.yaml`, and agent-facing reference files in English, regardless of the conversation language.

Treat harness-agnostic behavior as the default. Unless the user explicitly targets one harness, write shared instructions entirely in terms of required capabilities and outcomes. Reserve product names, proprietary tool names, harness-specific invocation syntax, UI metadata, discovery metadata, and setup for native configuration. Define an outcome-preserving fallback for unavailable capabilities.

## Establish the intent and target

When the request includes the literal `--grill` flag, immediately invoke `batch-grilling` with the remaining request and current discussion as its subject. Its result must cover the relevant codebase and filesystem facts and every unresolved design decision. Wait for the user to confirm the shared understanding, then resume this workflow and treat the confirmed decisions as requirements.

Read [`references/writing-principles.md`](references/writing-principles.md) in full before drafting. Resolve whether the request creates or edits a document, the target kind, and the absolute target path. Follow an explicit path first. Otherwise, derive the path from governing repository instructions and existing agent configuration, and ask only when multiple plausible targets remain or no target can be found.

Read every governing repository instruction. For `SKILL.md`, also read [`references/skill-mechanics.md`](references/skill-mechanics.md) in full before deciding invocation or packaging. For an edit, read the complete target and every agent-facing file it directly points to.

Derive decisions from the request and environment before asking questions. Without `--grill`, ask only about unresolved decisions whose answers materially change the result. Settle the intended purpose, applicable branches and scope, required outcomes and constraints, and, for a skill, its invocation. Treat a requested change as settled input. When the user reports misbehavior instead, diagnose it against every failure mode in `writing-principles.md`.

## Draft the complete result

Produce a complete, coherent version of every affected file. Preserve unrelated behavior and repository conventions, limiting edits to the requested changes and their necessary consequences.

For a new skill, choose a lowercase hyphenated name unless the user supplied one. Draft `SKILL.md` and the applicable native companion metadata according to `skill-mechanics.md`, and include only the directly required references, scripts, or assets. For an existing skill, keep every affected native companion metadata file aligned when its name, purpose, or invocation changes.

## Review with fresh eyes

When agent delegation is available, MUST assign one holistic review to a fresh agent. Give that reviewer the complete candidate files, the user's intent and settled decisions, and the absolute path to `writing-principles.md`. Require the reviewer to read the principles in full, then:

- Run the no-op test on every sentence and return a keep-or-cut disposition for each sentence, with a reason for every cut.
- Report duplication, sediment, sprawl, stale caches, weak context pointers, unnecessary procedural detail, avoidable negation, intent drift, contradictions, em dashes, and semicolons.
- Return a coherent pruned candidate that still fulfills the user's intent and resolves every contradiction.

Apply every cut verdict that preserves the intended behavior, and record a reason for each cut verdict not adopted. When delegation is unavailable, perform and record the same sentence-level review directly. After any later content fix, repeat the holistic review on the complete candidate. Finish when every sentence and reported issue has a disposition, every accepted cut is applied, and every rejected cut has a reason.

## Write and verify

A request to create, implement, edit, modify, or apply changes authorizes writing. A request only to draft, review, or propose changes authorizes presentation until the user explicitly approves writing.

For presentation-only work, present the complete proposal and wait for approval. For an authorized change, write every affected file. Validate a skill with the environment's skill validator when one is available. Confirm that every context pointer resolves, metadata matches the skill's name, purpose, and invocation, repository instructions apply at the intended scope, and shared instructions remain harness-agnostic unless the user requested a single-harness result. Fix every error or mismatch before reporting.

Report the files written, the important behavior changes, the pruning result, and the verification result. Include each rejected cut and its reason. Expand the report only for unresolved or unavailable checks.
