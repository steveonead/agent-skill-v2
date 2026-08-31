---
name: ito-prototype
description: Build throwaway code to answer one unresolved logic, state-model, or UI design question.
argument-hint: "[要驗證的設計問題]"
disable-model-invocation: true
---

# Prototype

Use the invocation arguments and current conversation as the work request.

A prototype is throwaway code built to answer one design question. Use this workflow when discussion cannot settle how a state model should behave or what a UI should look like. If the requested behavior is already settled, stop and direct the work to a specification or `ito-implement`.

## Frame the question

Write the question in one sentence before changing files. Choose one branch:

- **Logic or state model**: load [logic.md](references/logic.md). Use this branch for business rules, state transitions, data shapes, or APIs that need hands-on exploration.
- **UI direction**: load [ui.md](references/ui.md). Use this branch when the unresolved question concerns layout, information hierarchy, or primary interaction.

Ask the user when the branch or question is ambiguous. When the user is unavailable, infer the branch from the surrounding code and place the assumption at the top of the prototype. A backend module points to logic. A page or component points to UI.

Keep the question small enough to answer in one working session. If it is not, stop and propose smaller questions. A full application, sales demo, or already specified feature is outside this workflow.

## Isolate the work

Before creating Git state, ask for approval to create an isolated worktree, a `prototype/<slug>` branch from the repository's default branch, and the eventual prototype commit. If the user declines, stop. Do not place the prototype in the initiating worktree.

Create the prototype in the approved worktree. Keep its files close to the module or page under study and mark their names or routes as prototypes. If the question depends on uncommitted changes absent from the default branch, surface that conflict and ask how to proceed. Copy those changes only with explicit direction.

For a directory without Git, create a separate prototype directory after obtaining equivalent approval.

## Keep it disposable

Apply these constraints to both branches:

- Make the prototype trivial to start.
- Keep state in memory. When persistence is the question, use a scratch database or local file whose name marks it as disposable.
- Ask before installing a dependency, and install one only when the question cannot be answered without it.
- Add only the error handling needed to keep the prototype runnable. Skip tests, reusable abstractions, speculative cases, and production hardening.
- Iterate on the prototype when feedback exposes a sharper scenario or alternative. Keep every change tied to the original question.

## Capture the answer

Finish when the intended reviewer can operate the prototype and the answer can be stated in one sentence.

Write `docs/ito-temp/design/<slug>.md` in the initiating workspace with:

- the question
- the verdict
- the reasons supported by the prototype
- the `prototype/<slug>` branch, or the separate prototype directory when Git is unavailable, as the evidence pointer
- the consequences for later specification or implementation

When Git is available, commit the runnable prototype to its approved branch and keep that branch out of the mainline. Leave production code unchanged. Route the validated decision to a specification or `ito-implement` rather than promoting prototype code.

When Git is available, ask before removing the worktree. Remove it only after the prototype commit exists and the worktree is clean. Preserve the branch as the primary source. Without Git, preserve the separate prototype directory as the primary source.
