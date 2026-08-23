---
name: ito-explain-pr
description: Explain a pull request or diff as a visual HTML artifact for an engineer new to the codebase.
argument-hint: "PR 編號或 URL、branch、commit range，留空自動抓目前 branch 的 PR 或本地 diff。"
disable-model-invocation: true
---

# Explain a change visually

Explain a code change to an engineer who knows nothing about this codebase. Big pictures, few words: visuals carry the explanation, prose does only what a visual cannot, and the reader should answer "what changed and why" from the visuals alone without opening a diff. Line-level detail stays on GitHub. The actual code is the source of truth, and the PR description is reference material.

## Step 1: Resolve the change

Parse the invocation argument as one of: a PR number or GitHub PR URL, a commit range, or a branch name. With no argument, use the open PR of the current branch, otherwise the current branch against its merge-base with the default branch, otherwise the uncommitted working tree diff.

Fetch the diff and metadata with `gh` for a PR and `git` otherwise. Record the base and head SHAs, the changed file list, the repository web URL, and the PR title and description when they exist.

Finish when the diff, both endpoint SHAs, and the source kind (PR, range, branch, or working tree) are stated.

## Step 2: Explore through sub-agents

Group the changed files into behavior clusters by intent. Dispatch 1 to 3 read-only exploration sub-agents in parallel, each owning distinct clusters, and keep the main conversation for synthesis and rendering. When delegation is unavailable, run the same exploration in the main conversation.

Each exploration must:

- Read the diff plus the base and head versions of its files.
- Trace callers and callees of changed symbols until it can state the externally visible behavior change.
- Classify each change as logic (behavior changed) or mechanical (rename, constant, config, import move, formatting).
- Return per cluster: the intent, the before behavior, the after behavior, evidence as `path:line` at the head SHA, surprises, and any point where the code contradicts the PR description.

Finish when every changed file belongs to a cluster whose behavior change or mechanical nature is stated with evidence.

## Step 3: Compose the sections

Build the artifact from this skeleton, dropping a section only when the change gives it nothing to say:

1. **TL;DR**: one paragraph of intent and net effect, leading with the conclusion. Stat cards (files, additions, deletions, touched areas) are context, never the lead. Put the highest-impact risk in a callout.
2. **Mental model**: the domain entities the change reasons about and the states it branches on, as a matrix crossing those states against what the new code does with each. A newcomer who reads this section should be able to predict the outcomes Behavior changes explains.
3. **System orientation**: a 30-second introduction to the touched subsystem for a newcomer, then a diagram or file tree that marks where the change lands.
4. **Behavior changes**: at most 5 groups organized by intent, never a per-file walk. Give every logic change in the core groups a before and after contrast whose delta is visually loud, and keep unchanged context muted. A change that threads several files gets one overview contrast instead of per-file drawings. A new file gets an after view plus one line on its role. A deleted file gets a before view plus what takes over. Collect mechanical changes and overflow beyond the 5 groups into a single list of one-line before and after rows.
5. **Impact and risks**: a matrix crossing each affected caller against the change that reaches it and the action it must take, then compatibility and migration notes, all grounded in code that was read. When the code contradicts the PR description, add a callout stating what the description claims and what the code does. Close with a verification snippet the reader can run: a request and its expected response for a new endpoint, otherwise the command or test path that exercises the change.
6. **Details exit**: a closing pointer to the PR Files changed tab for line-level review.

Draw each mechanism once: a given function or use case gets one visual for how it works, and a before and after contrast is allowed on top of it because it proves a different claim. A second drawing of the same mechanism from another angle is a cut.

Prose describes the change, not the investigation that found it. Code snippets appear only when a snippet is the clearest proof of a claim, and never open a section. Link behavior evidence to the blob URL at the head SHA with a line anchor. Without a PR, keep evidence as plain `path:line` text.

Finish when every skeleton section is composed or explicitly dropped, and every claim carries evidence.

## Step 4: Render and deliver

Invoke the artifact-visualizer skill with the composed sections in order, each carrying content, source, and a component hint. Pass `docs/ito-temp/diff/NNN-<slug>.html` as the output path, following the caller-path numbering and slug convention in its output contract. Author prose in Traditional Chinese and keep identifiers, code, and established technical terms in English.
Deliver the local HTML file, and publish a shareable claude.ai Artifact only when the user asks.

Finish when the artifact path is reported along with any behavior the exploration could not verify.
