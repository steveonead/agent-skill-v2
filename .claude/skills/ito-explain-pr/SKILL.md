---
name: ito-explain-pr
description: Explain a pull request or diff as a visual HTML artifact for an engineer new to the codebase.
argument-hint: "PR 編號或 URL、branch、commit range，留空自動抓目前 branch 的 PR 或本地 diff。"
disable-model-invocation: true
---

# Explain a change visually

Explain a code change to an engineer who knows nothing about this codebase. Visuals carry the claims that change how the reader judges the change, and prose carries everything else in as few words as it takes. The reader should answer "what changed and why" from the visuals alone without opening a diff. Line-level detail stays on GitHub. The actual code is the source of truth, and the PR description is reference material.

## Step 1: Resolve the change

Parse the invocation argument as one of: a PR number or GitHub PR URL, a commit range, or a branch name. With no argument, use the open PR of the current branch, otherwise the current branch against its merge-base with the default branch, otherwise the uncommitted working tree diff.

Record the base and head SHAs, the changed file list, the repository web URL, and the PR title and description when they exist.

Finish when the diff, both endpoint SHAs, and the source kind are stated.

## Step 2: Explore through sub-agents

Before dispatching, read the project's configuration for the facts an explorer would otherwise infer from code alone: the datastore and its configured modes, the runtime and framework, and the test runner. Put them in every brief, so every explorer reasons from the same ground truth and their findings compose.

Group the changed files into behavior clusters by intent. Dispatch 1 to 3 read-only exploration sub-agents in parallel, each brief naming the files its cluster owns, and keep the main conversation for synthesis and rendering. Dispatch, then end the turn and wait for the completion notification, so every file stays with its explorer until the findings arrive. When delegation is unavailable, run the same exploration in the main conversation.

Each exploration must:

- Read the diff plus the base and head versions of its files.
- Trace callers and callees of changed symbols until it can state the externally visible behavior change.
- Classify each change as logic (behavior changed) or mechanical (rename, constant, config, import move, formatting).
- Return per cluster: the intent, the before behavior, the after behavior, evidence as `path:line` at the head SHA, surprises, and any point where the code contradicts the PR description.

Finish when every changed file belongs to a cluster whose behavior change or mechanical nature is stated with evidence.

## Step 3: Compose the sections

Findings earn visuals. Give the reader the smallest set that changes how they judge this change.

Two tests govern every candidate visual:

- **It changes a judgment.** Take it away: when the reader would still decide the same thing about correctness, risk, or their own next action, its content belongs in a sentence or belongs nowhere. Whatever the reader reproduces in seconds from the PR page, such as diff statistics, the changed-file list, a signature the caller can read off the schema, or a mechanical rename, fails this test.
- **Its claim is still unproven.** Each claim gets one visual, and the same mechanism drawn again from another angle is a cut.

The changed-line total sets one ceiling for the whole document: at most 10 visuals up to 500 lines, at most 16 up to 2000, and above that group by subsystem and hold the ceiling. Sections and behavior groups compete for that ceiling rather than each drawing from it, so a change with five behavior groups spends most of its budget there and states the rest in prose.

Compose from these sections, keeping the ones the findings fill:

1. **Bottom line**: one paragraph of intent and net effect, leading with the conclusion. Put the highest-impact risk in a callout. A number earns a card of its own only when that number is itself the finding.
2. **Mental model**: the domain entities the change reasons about and the states it branches on, crossed against what the new code does with each, which a matrix usually carries best. A newcomer who reads this section should be able to predict the outcomes Behavior changes explains.
3. **System orientation**: a 30-second introduction to the touched subsystem for a newcomer, and a visual of where the change lands when the layout is itself a finding, such as a change threading subsystems that rarely meet.
4. **Behavior changes**: at most 5 groups organized by intent, never a per-file walk. Give every logic change that passes both tests a before and after contrast whose delta is visually loud, and keep unchanged context muted. A change that threads several files gets one overview contrast instead of per-file drawings. A new file gets an after view plus one line on its role, and a deleted file gets a before view plus what takes over. Mechanical changes and everything beyond the 5 groups reduce to one line of prose each.
5. **Impact and risks**: each affected caller crossed against the change that reaches it and the action it must take, then compatibility and migration notes, all grounded in code that was read. When the code contradicts the PR description, add a callout stating what the description claims and what the code does. Close with the command or request that exercises the change, in prose unless it runs past a handful of lines.

Prose describes the change, not the investigation that found it. Code snippets appear only when a snippet is the clearest proof of a claim, and never open a section. Link behavior evidence to the blob URL at the head SHA with a line anchor. Without a PR, keep evidence as plain `path:line` text. End the last section with a pointer to the PR Files changed tab for line-level review.

Finish when the visual count is at or under the ceiling for the changed-line total, every visual passes both tests, and every claim carries evidence. Report the count alongside its ceiling.

## Step 4: Render and deliver

Invoke the artifact-visualizer skill with the composed sections in order, each carrying content, source, and a component hint, and state that the list is the document in full. Pass `docs/ito-temp/diff/NNN-<slug>.html` as the output path, incrementing the largest numeric prefix already in that directory and starting at `001`. Keep identifiers, code, and established technical terms in English inside the prose.

Deliver the local HTML file, and publish a shareable claude.ai Artifact only when the user asks.

Finish when the artifact path is reported along with any behavior the exploration could not verify.
