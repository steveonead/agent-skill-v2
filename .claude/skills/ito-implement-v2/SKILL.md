---
name: ito-implement-v2
description: "Implement a piece of work based on a spec or set of tickets, whether that work is a new feature or a bug fix."
disable-model-invocation: true
---

# Implement

Implement the work described by the user in the spec or tickets.

## 1. Load the project's rules and language

Search the whole project for `BEST-PRACTICE-MAP.md`, `CONTEXT-MAP.md`, and `CONTEXT.md`.

`BEST-PRACTICE-MAP.md` points at the project's rule sets and says which set governs what. Read every map found, then every rule set it points at that bears on this piece of work, and state for each one what it constrains here.

Take your names, test names, and interface vocabulary from `CONTEXT.md`. When more than one is found, use the one in the nearest ancestor directory of the files this work expects to touch. A `CONTEXT-MAP.md` means multiple contexts, so read it to find which one this work sits in. See [context-format.md](references/context-format.md) for the shape of these files. Respect any ADRs in `docs/adr/` that cover the area you are touching.

Note the current commit.

Fix the commit language from `git log -10 --format=%s`: every subject in English means English, everything else, including an empty log, means zh-TW.

**Done when**: every rule that bears on this work is loaded, and the commit language is fixed.

## 2. Agree the seams

Read [tdd.md](references/tdd.md).

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside.

Write down the seams under test and confirm them with the user before writing any test. A seam that surfaces later is confirmed the same way, before its test.

## 3. Work the loop, one vertical slice at a time

**A feature** goes red → green. Write the failing test at an agreed seam, then only enough code to pass it.

**A bug** goes through the **Prove-It Pattern**. Do not start by trying to fix it. Start by writing a test that reproduces it, and watch it fail:

```
Bug report arrives
       │
       ▼
  Write a test that demonstrates the bug
       │
       ▼
  Test FAILS (confirming the bug exists)
       │
       ▼
  Implement the fix
       │
       ▼
  Test PASSES (proving the fix works)
```

Run typechecking regularly and single test files regularly.

Refactoring waits for step 4.

### Comments

A comment earns its place only when the *why* behind a line cannot be recovered from the code itself: a constraint imposed from outside the file, a workaround for someone else's bug, an alternative that was tried and failed.

A comment never restates what the line does. A comment is never a work log, so "added X", "changed per ticket 12", and "was previously Y" belong in the commit message instead.

### Committing

Commit each slice the moment it goes green, its test and its implementation in one commit.

Write the subject in Conventional Commits form, in the language fixed in step 1: 72 characters in English, 36 in Chinese. Pick the type from `feat`, `fix`, `chore`, `refactor`, `test`, `docs`, `style`, `ci`. When every file in the slice sits under one module directory, use that directory's name as the scope (`feat(auth): ...`), otherwise leave the scope out.

**Done when**: for a bug, a test failed before the fix with the bug's own symptom in the failure message, and passes after. For every slice, its test went from red to green, typechecking passes, nothing was built for a need the spec does not have, and the slice is committed.

## 4. Close out

Run the full test suite once, using the repository's own command.

Then review `git diff <the commit noted in step 1>...HEAD`. Send one message with two `Agent` calls: a **Standards** sub-agent and a **Spec** sub-agent. Paste the opening of [code-review.md](references/code-review.md) plus that agent's own section into each prompt in full, and hand each one the diff command, the rule sets and `CONTEXT.md` from step 1, and the spec or tickets. Report the two sets of findings under their own headings.

Refactor here, with the findings in hand and the whole diff visible. Commit the refactor on its own as `refactor`. Commit the fixes for the findings separately, typed by what each one is. Leave the step 3 commits as they stand.

Run the full test suite again.

**Done when**: the full suite is green, every review finding is either fixed or answered out loud with why it stands, and the work is committed.
