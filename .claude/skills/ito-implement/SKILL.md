---
name: ito-implement
description: Implement a spec or ticket test-first, then review the result on standards and spec.
argument-hint: "要實作什麼？給我 spec 檔案路徑、GitHub issue 編號，或直接講清楚要做的事。"
disable-model-invocation: true
---

# Implement From a Spec

Use the invocation arguments and current conversation as the work request.

Step 1 ends in the one planned stop. After the user confirms there, run through to the review without further checkpoints.

Load `tdd` and `implement-review` with the Skill tool in this conversation, each at the step that reaches it. The spec, the seam list, and the fixed point stay in one context that way, so neither skill has to rediscover them.

## Step 1: Pin the spec and the seams

Resolve the work request into one spec that the review stage can read:

- **Supplied spec**: a path or an issue reference the user gave. Use its contents as-is.
- **Verbal request**: draft a short spec covering the required behavior, the constraints, and the completion conditions. Write it under `.scratch/`.

Keep the path or issue reference: the review stage reads the same one.

Then load `tdd` and use its seam guidance to draft the seam list covering the behaviors this spec requires. Put the spec and the seam list to the user together, so the work needs one agreement pass instead of one per slice.

Finish when the user has confirmed one spec and the seam list in a single pass.

## Step 2: Set the baseline

Create a working branch when `HEAD` sits on the repository's default branch. Otherwise stay on the current branch.

Record `git rev-parse HEAD` as the **fixed point**: the commit the whole change is reviewed against, and the baseline for judging test failures.

Discover the repository's typecheck, test, and lint commands from its configuration and instructions. Check which of them a hook already runs automatically: those stay hook-covered, and you run the rest yourself.

Finish when `HEAD` is off the default branch, the fixed point SHA is recorded, and each of typecheck, test, and lint is a known command or confirmed absent, marked hook-covered or self-run.

## Step 3: Implement in vertical slices

Follow `tdd` for every slice against the confirmed seams. It owns the red → green loop and what makes a test worth keeping.

Per slice, run typecheck and the affected test file, then commit on green. Use Conventional Commits with a scope and a Traditional Chinese description, such as `feat(auth): 加入登入表單驗證`.

Finish when every behavior the spec requires is green and committed.

## Step 4: Verify the whole change

Run the full test suite, plus any self-run typecheck and lint.

Check each failing test against the fixed point before repairing it. A test that already failed there is pre-existing: record it and continue. Repair every failure this change introduced.

Finish when the suite is green apart from recorded pre-existing failures.

## Step 5: Review and resolve

Invoke `implement-review` with the fixed point SHA from Step 2 and the spec from Step 1, so it uses the confirmed spec rather than rediscovering one.

Repair every finding the review labelled a hard violation. Leave the judgement calls exactly as the reviewer wrote them. Commit the repairs separately, marked as review fixes, and re-run the full suite.

Present both axis reports as `implement-review` returned them, then list the repairs you made and the judgement calls you left for the user. Run the review once, and report the remaining findings as they stand.

Finish when both axes have reported, the reports are delivered, the repairs are committed, and the suite is green.
