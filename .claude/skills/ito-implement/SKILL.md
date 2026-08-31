---
name: ito-implement
description: Implement a spec or ticket test-first, review it on standards and spec, then audit its comments.
argument-hint: "[spec 路徑、GitHub issue 編號或工作說明]"
disable-model-invocation: true
---

# Implement From a Spec

Use the invocation arguments and current conversation as the work request.

Step 1 ends in the one planned stop. After the user confirms there, run through to the review without further checkpoints.

Apply `tdd`, `implement-review`, and `no-comments` in this conversation at the step that reaches each skill. Use the environment's skill-loading capability when available. Otherwise read and follow each skill directly. Keep the spec, seam list, fixed point, and review reports in this context so later stages can reuse them.

## Step 1: Pin the spec and the seams

Resolve the work request into one spec that the review stage can read:

- **Supplied spec**: a path or an issue reference the user gave. Use its contents as-is.
- **Verbal request**: draft a short spec covering the required behavior, the constraints, and the completion conditions. Write it under `.scratch/`.

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

Repair every finding the review labelled a hard violation. Leave the judgement calls exactly as the reviewer wrote them. Run the affected tests and applicable self-run typecheck and lint commands, then commit the repairs separately as review fixes.

After those repairs, invoke `no-comments` with the fixed-point diff and the Standards report's ordered source list. Keep the comment reviewer read-only. Repair every comment hard violation, leave its judgement calls unchanged, and run the affected tests and applicable self-run typecheck and lint commands. Commit comment repairs separately with a commit such as `refactor(review): 移除無意義註解`.

When comment repairs were needed, send the repair diff and prior report back to the same reviewer for an incremental verification. Repeat repair and incremental verification until no comment hard violations remain. If reviewer follow-up is unavailable, give a fresh reviewer the prior report and repair diff instead of repeating the full fixed-point review.

Run the full suite once after all review repairs only when they changed executable code, tests, configuration, a suppression, or a workaround. When review only removed ordinary comments, the affected tests and applicable self-run typecheck and lint are sufficient. A hook-covered check remains satisfied by the repair commits.

Present the Standards and Spec reports as `implement-review` returned them. Then present the Comment report, the repairs, verification results, and every judgement call left for the user. Run `implement-review` once. The targeted comment verification does not rerun either axis.

Finish when all three reports are delivered, every hard violation is repaired and committed, the final Comment report has no hard violations, and the required checks are green apart from recorded pre-existing failures.
