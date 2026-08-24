---
name: ito-explain-pr
description: Explain a pull request or diff as a visual brief that gets an impatient reviewer into context before they read code.
argument-hint: "PR number or URL, branch, or commit range. Leave empty to detect the current branch's PR or local diff."
disable-model-invocation: true
---

# Explain a change visually

Write for an impatient software engineer who does not know this project and has 5 to 10 minutes. The brief gets that reader into context and hands them back to the code, where line-level review happens and the code remains the source of truth.

The brief succeeds when a reader who stops after the first two screens can say what the change does and where to start reviewing, and a reader who finishes can recover every externally visible behavior and contract change from the visuals alone. Claim a reason for the change only where the repository, PR, issue, ticket, or commit history provides evidence.

## Resolve the change

Parse the argument as a PR number or GitHub PR URL, commit range, or branch name. With no argument, use the current branch's open PR when one exists. Otherwise compare the branch with its merge-base against the default branch when committed changes exist, then fall back to the uncommitted working tree diff.

Record the comparison endpoint identities and their SHAs, changed files, repository web URL, and PR title and description when available.

## Explore the behavior

Group changed files into behavior clusters by intent, which organize exploration rather than the brief's sections. Explore independent clusters in parallel through read-only sub-agents when available, otherwise explore them in the main conversation.

For each cluster:

- Read the diff, both endpoint versions of its files, and the repository context needed to interpret them.
- Trace changed symbols through callers and callees far enough to name the externally visible behavior.
- Separate logic and contract changes from mechanical work.
- Record the before behavior, after behavior, affected consumers, verification evidence, and source evidence as `path:line`.
- Verify leads from the PR description against code, and record contradictions and evidence gaps.

Finish when every changed file has been examined and every externally visible change has evidence.

## Plan the brief

Order the brief by what the reader needs in order to follow the next part, rather than by what matters most to a reviewer:

1. A plain-language summary of two or three sentences: what changed, for whom, and why when evidence exists. Use the domain words the reader already has, such as "campaigns can now be deleted, and only while no line item under them is running or has spent".
2. Where to start reviewing: the one or two files that carry the behavior, plus the link to the PR Files changed view when a PR exists, otherwise the source diff.
3. A mental model visual whenever the change depends on domain terms, entities, or state flags the reader must hold in mind, covering only the entities and states this change touches. It comes before the first visual that uses those terms.
4. One section per externally visible behavior or contract change, each carrying one visual whose before and after are both visible.
5. Reviewer-depth material last, under one heading: concurrency, lock ordering, tenancy, stubs, and verification gaps, one line each with a pointer, and only where it changes correctness, merge judgment, or the next review action.

Write every section title as a conclusion the reader can repeat, such as "Deleting a campaign is refused while any line item is running or has spend".

Report mechanical work such as fixtures, imports, and registrations as one count or one line, unless those files are themselves the subject.

Budget: at most six visuals, and at most one code or diff excerpt cut to the smallest span that proves its claim. Exceeding either budget requires naming what was already cut and why the remainder still needs more.

The plan is complete when the summary contains no file names and no symbol names, the mental model precedes the first use of every domain term, every section title is a conclusion sentence, and both budgets hold.

## Render the brief

Invoke `artifact-visualizer` with the completed plan as its caller contract: `audience`, `language`, document `title`, `lead` paragraph, section grouping, output path, closing link, and the ordered visuals, each with its `claim`, `source`, `relationship`, `content`, and `boundaries`. The visualizer owns component choice and rendering verification.

Set the output path to the directory `docs/ito-temp/diff/`. Set the language to the user's conversation language, and keep identifiers, code, and established technical terms in English inside localized prose.

When the visualizer reports a claim it cannot render faithfully, revise the plan and render again.

## Audit the reading experience

Run both stages with a fresh agent who did not explore the change. When delegation is unavailable, run them in the main conversation and report that fallback.

Stage 1, impatience. The auditor sees only the first two screens, roughly the first 1800 pixels at 1440 wide, with one minute of reading, then states what the change does and where they would start reviewing. A miss here means rewriting the top of the document before touching anything else.

Stage 2, completeness. With section prose and captions hidden and labels inside visuals visible, the auditor restates every externally visible behavior and contract change, its before and after, and its main impact on consumers, correctness, or the next review action. Revise on any miss, then rerun this stage.

## Deliver

Report the local HTML path, both audit results, any behavior that could not be verified, any claimed reason whose evidence remains incomplete, and any budget overrun with its justification.
