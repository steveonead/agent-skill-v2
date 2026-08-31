---
name: ito-handoff
description: "Compact the current conversation into continuation context for a fresh agent session. Use when the user asks to hand off work, create continuation notes, preserve session context, or prepare a fresh agent session."
argument-hint: "[下一個工作階段的目標] [--os]"
disable-model-invocation: true
---

# ITO Handoff

## Step 1: Frame the handoff

Treat `--os` as the storage flag. Treat all remaining invocation arguments as the next session's goal. With an omitted goal, preserve the context needed for a fresh agent to continue the session.

Read the current conversation, workspace state, and artifacts relevant to that goal. Distinguish confirmed facts from open questions and failed attempts.

Finish when the next session goal or full-session scope, relevant sources, and unresolved state are identified.

## Step 2: Select the destination

By default, resolve the project root with `git rev-parse --show-toplevel`. For a standalone working directory, use the current working directory as the project root. Create `docs/ito-temp/handoff/` under that root.

In the default destination, name the file `[NNNN]-[topic-slug].md`. Scan matching four-digit Markdown files, increment the highest number, and start at `0001` for an empty destination. Derive a lowercase hyphenated topic slug from the next session goal, or use `session`.

With `--os`, use the operating system's temporary-file facility to create a unique Markdown file in its temporary directory.

Finish when one unique output path has been selected in the selected destination.

## Step 3: Capture continuity

Write a free-form handoff document organized for the next session goal. Include information that changes how the next agent should act. Redact credentials, tokens, passwords, personal data, and other sensitive values.

Cover the next action, confirmed decisions, constraints, relevant files, verification results, unresolved questions, and failed approaches when they affect continuation.

Reference existing specifications, plans, ADRs, issues, commits, and diffs by path or URL when they contain facts the next agent needs.

Add a `Suggested Skills` section when a specific skill and its task condition would help the next agent.

Finish when the document gives a fresh agent the goal, current state, executable next actions, and links to relevant existing artifacts.

## Step 4: Report the handoff

Save the document, then report its absolute path and the next session goal in one concise response.

Finish when the saved path and goal are reported.
