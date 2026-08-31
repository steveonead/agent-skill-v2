---
name: ito-explain-code
description: Explain how something works in this codebase by exploring code and producing a clear architectural explanation.
argument-hint: "[要理解的子系統、流程或問題]"
disable-model-invocation: true
---

# Explain How It Works

Use the invocation arguments and current conversation as the question. Explain at the level of a senior engineer onboarding onto a subsystem: stop where the reader can predict the behavior from the explanation alone.

## Step 1: Fix the scope

Read every `CLAUDE.md` and `AGENTS.md` that governs the directories named in the question.

State which subsystem, flow, or runtime path the answer will cover. When the question admits several readings, state the chosen reading and continue.

Finish when every governing instruction file has been read and the question and its covered scope are stated.

## Step 2: Choose the path and announce it

Classify the question by the smallest tier that covers it:

- **Simple**: one module, one utility, or one narrow question such as how a single function behaves.
- **Complex**: a subsystem spanning files or services, a cross-cutting feature, or a whole-architecture overview.

Announce the chosen tier before exploring. For the complex tier, announce how many explorers will run and the slice each one covers.

Prefer the simple tier while the classification is uncertain.

Finish when the tier is announced, and for the complex tier every explorer slice is named.

## Step 3: Explore

For the simple tier, explore directly with Glob, Grep, and Read. Return to Step 2 when this exploration stalls.

For the complex tier, dispatch 2 to 4 read-only exploration sub-agents in a single message. Give each one a distinct slice of the subsystem, such as the data model, the runtime pipeline, or the surrounding infrastructure.

Every exploration follows the same method:

- Follow the thread from the entry point through callers, callees, data flow, and type definitions.
- Treat file names as a hypothesis to confirm against the code.
- Record what a newcomer would get wrong.

Require each sub-agent to return exactly four items: the components it found, the flow it traced, the absolute paths it read, and anything surprising or counter-intuitive.

Finish when every step of the path from trigger to effect is backed by code that was read or by a named boundary outside this codebase.

## Step 4: Synthesize and present

Write the explanation directly from the findings, reconciling overlaps and resolving contradictions against the code. Match the conversation language.

Use these sections, and keep only those the question needs:

- **Overview**: one or two paragraphs on what the thing is, what it does, and why it exists.
- **Key Concepts**: the types, services, and abstractions required to follow the rest.
- **How It Works**: the flow in prose. What triggers it, what happens in order, where the data goes, and which decision points exist. Cite files and functions so the reader can look, and quote a snippet only when the point depends on it.
- **Where Things Live**: the files and directories someone needs to start working in this area.
- **Gotchas**: non-obvious behavior, sharp edges, and history that explains why something looks strange.

Include a diagram when it carries a data flow, call chain, or state transition more clearly than the surrounding prose. Draw it as ASCII in the conversation.

When the behavior lives outside this codebase, such as inside a third-party package or an external service, state that and name the boundary the trace reached.

Finish when the presented explanation covers every part of the scope stated in Step 1.

## Step 5: Offer to save

Offer to save the explanation and wait for the answer.

On acceptance, resolve the project root with `git rev-parse --show-toplevel`, and use the current working directory as the project root for a standalone working directory. Create `docs/ito-temp/explain/` under that root when it is absent. Scan that destination for Markdown files with a three-digit leading number, increment the highest number, and start at `001` for an empty destination. Name the file `NNN-<slug>.md`, with `<slug>` an English kebab-case phrase from the question.

Rewrite each ASCII diagram as a mermaid block in the saved file, which carries the mermaid form alone.

Finish when the written path is reported, or when the user declined to save.
