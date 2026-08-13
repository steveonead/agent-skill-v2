---
name: ito-write-agent-docs
description: Create or edit the documents a coding agent consumes: SKILL.md, AGENTS.md, CLAUDE.md, and the reference files they point to. Use when writing a new skill, revising an existing skill's steps, description, or invocation, or when an agent document produces unreliable behavior. For human-facing README or product docs, write them directly instead.
argument-hint: "想寫或改哪份文件？SKILL.md、AGENTS.md，還是 CLAUDE.md？"
---

Write `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `agents/openai.yaml`, and agent-facing reference files in English, regardless of the conversation language.

## Step 1: Load the principles

Read [`references/WRITING-PRINCIPLES.md`](references/WRITING-PRINCIPLES.md) in full before drafting.

Finish when `references/WRITING-PRINCIPLES.md` has been read in full.

## Step 2: Fix the track and target

Choose the track from the request: create a new document or edit an existing document. Choose the target kind: `SKILL.md`, `AGENTS.md`, or `CLAUDE.md`.

Resolve an explicit target path first. Otherwise, search the working directory and its parents for the requested filename. For a new skill, identify the skills directory from governing repository instructions or existing agent configuration directories. Ask for a path when the search leaves multiple plausible targets or none.

When the target kind is `SKILL.md`, read [`references/SKILL-MECHANICS.md`](references/SKILL-MECHANICS.md) in full before deciding its invocation or packaging.

Finish when the track, target kind, and absolute target path are recorded, and every governing repository instruction and target-specific reference has been identified and read in full.

## Creating a document

### Step 3: Settle the design

Derive decisions from the request and filesystem before asking questions. Put each unresolved decision to the user one at a time, with a recommended answer that can be accepted in one word:

1. **Purpose**: what work should the document make the agent perform?
2. **Branches and scope**: which distinct situations should it handle, and where should its instructions apply?
3. **Content shape**: which material is ordered steps, in-file reference, or disclosed reference?
4. **Completion criteria**: what checkable and exhaustive condition ends each step?
5. **Invocation**: for a skill only, should the model discover it or should the user invoke it explicitly?

For a skill, propose a lowercase hyphenated name derived from its purpose and leading word unless the user supplied one. Finish when every applicable decision has one recorded answer.

### Step 4: Draft

For a new skill, inspect the environment's exposed tools and skill-creation utilities. When exactly one scaffolder supports the target format, initialize the scaffold in an operating-system temporary workspace, then replace its generated placeholders while drafting. Keep the resolved target unchanged until Step 6.

Draft the complete target and every directly required reference file.

For a skill, draft `SKILL.md` and `agents/openai.yaml` according to `references/SKILL-MECHANICS.md`.

For `AGENTS.md` or `CLAUDE.md`, preserve repository conventions and the file's scope.

Finish when the draft covers every recorded design decision and branch, follows governing repository instructions and target-specific mechanics, includes every required companion file, and gives every step a completion criterion.

## Editing a document

### Step 3: Diagnose

Read the target and every agent-facing file it directly points to. Treat a request that names the desired edit as a specified change.

When the request describes misbehavior instead, test every failure mode defined in `references/WRITING-PRINCIPLES.md` against the evidence. Record every matching mode and adopt its stated remedy.

Finish when each requested change or observed symptom maps to a concrete revision.

### Step 4: Revise

Draft the complete revised text of every affected file. Preserve unrelated instructions and repository conventions. For a skill, update `agents/openai.yaml` when its name, purpose, or invocation changes. Compare the draft semantically with the original to identify every behavior change.

Finish when the semantic comparison shows that every behavior change maps to the request or diagnosis and all unrelated behavior remains intact.

## Closing steps

### Step 5: Prune with fresh eyes

Write the complete candidate file tree to an operating-system temporary directory. When the current environment exposes an agent-delegation tool, delegate the pruning pass to a fresh agent given only the pruning inputs. Give it the temporary directory, the absolute path of `references/WRITING-PRINCIPLES.md`, and this brief:

- Read `WRITING-PRINCIPLES.md` in full before reviewing the draft.
- Run the no-op test on every sentence in isolation. Return a keep-or-cut verdict for each sentence and a one-line reason for every cut.
- Report duplication, irrelevant lines, stale caches of repository facts, weak context pointers, and negation that can be stated positively.
- Report every em dash and every semicolon, each with the replacement punctuation named in `WRITING-PRINCIPLES.md`.

When delegation runs, apply its verdicts and record every sentence kept against a cut verdict with the reason. When delegation is unavailable, record that fresh-eyes pruning did not run. Remove the temporary path after either branch.

Finish when every sentence and reported issue has a recorded disposition, every accepted cut is applied, every rejected cut has a reason, and the temporary path is removed. When delegation is unavailable, finish when that state is recorded and the temporary path is removed.

### Step 6: Write the files

Classify a request to create, implement, or apply changes as write authorization on either track. Classify a request to draft, review, or propose changes as presentation-only authorization.

For a write-authorized request, write the complete draft and every required companion file to their resolved paths.

For a presentation-only request, present the complete proposed changes and stop the run pending explicit write authorization. On authorization, resume at Step 6.

Finish when every authorized file exists at its resolved path and contains the final draft, or when every proposed change has been presented and the run is paused pending authorization. Proceed to Step 7 only after the files have been written.

### Step 7: Verify

For a skill, inspect governing instructions and the current environment for a skill validator. Run it when found, or record that validation tooling is unavailable. Confirm that every context pointer resolves and that `agents/openai.yaml` matches the skill's name, purpose, and invocation. Fix every validator error, broken pointer, and metadata mismatch.

For `AGENTS.md` or `CLAUDE.md`, confirm that every context pointer resolves, the instructions apply at the intended directory scope, and the revision is consistent with governing repository instructions.

Treat every content fix as a revision and repeat Steps 5 through 7 before reporting. Finish when all available checks pass on the pruned final content and every unavailable check is recorded for the report.

### Step 8: Report

Report the track, target kind, absolute path of every file written, validation results or tooling unavailability, fresh-eyes pruning status, the number of sentences cut, and each sentence kept against the pruner's verdict with a one-line reason.

Finish when the report includes every applicable field, including an explicit reason when fresh-eyes pruning did not run.
