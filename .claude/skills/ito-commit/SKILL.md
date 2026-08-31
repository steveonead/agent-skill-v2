---
name: ito-commit
description: "Review and commit the current worktree as a confirmed set of atomic commits."
disable-model-invocation: true
---

# Commit the current worktree

Accept only an invocation with no arguments. Reject flags, paths, and other arguments before inspecting or changing the repository.

Review the complete worktree, propose atomic commits, and create only the plan the user confirms. Leave excluded worktree content unchanged and never push.

## Inspect the worktree

Confirm that the current directory belongs to a Git worktree. Inspect the complete staged and unstaged diffs, status including untracked paths, and the five most recent commit subjects. Stop and report any unresolved conflict before planning commits.

Treat staged and unstaged changes as one change set for analysis. Do not alter the index or worktree during inspection.

List all untracked paths and ask the user which to include. Accept all paths, no paths, or an explicit subset. Keep every unselected path outside the plan and unchanged.

Inspect included paths and added diff content for secret-looking material such as environment files, private keys, credentials, passwords, and tokens. Never reproduce a suspected secret value. When a path or added value looks sensitive, identify the affected path, explain the reason without exposing the value, and obtain a dedicated yes-or-no confirmation before continuing.

## Plan atomic commits

Account for every included change exactly once. Group changes by intent so each commit represents one coherent change. Keep an implementation with its directly related tests, documentation, and configuration. Keep a dependency manifest with its related lock file.

Write Conventional Commits messages that follow repository instructions when they define additional rules. Use English only when all five inspected commit subjects are English. Use Traditional Chinese when fewer than five subjects exist or any of the five is not English. Keep established code identifiers and technical terms in their original language.

Present the complete plan with each commit message and its paths. Also identify excluded untracked paths and state that the confirmed execution will replace the current staging arrangement. Allow as many commits as atomic grouping requires.

Obtain explicit confirmation of the complete plan. When the user requests a change, revise and present the complete plan again. Treat confirmation as applying only to the exact worktree and index state represented by that preview.

## Create the confirmed commits

Immediately before changing the index, verify that the worktree and index still match the confirmed preview. If either changed, return to inspection and obtain confirmation for a new complete plan.

After verification, clear the existing staging arrangement without changing worktree content. For each planned commit, stage only that group's exact changes and verify the staged diff against the plan before committing. Let repository commit hooks run. Do not run separate tests, lint, type checking, or other validation.

After each commit, verify its hash, message, content, and the remaining planned worktree state. If a hook fails or any file changes unexpectedly, stop immediately. Preserve the current worktree and index, and do not roll back or repair the failure automatically.

Finish only when every confirmed group has been committed and no included change remains uncommitted. Report each created commit's hash and message, any excluded paths still in the worktree, and whether hooks completed successfully.

On any failure, distinguish commits already created from groups not yet attempted, then report the failing command or hook, its relevant output, and the exact current worktree and index state.
