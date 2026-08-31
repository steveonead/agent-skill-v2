---
name: no-comments
description: Audit comments in a caller-supplied diff or file set. Use after implementation or review repairs to find redundant comments, suppressions, workarounds, and unenforced constraints without editing code.
user-invocable: false
---

# Audit comments

Return a read-only report. The caller owns every repair.

## Scope

Use the diff command or files the caller supplies. Otherwise compare the current work, including the working tree, with the repository's default branch. Inspect added or modified comments and scoped lint or type-system suppressions. Read nearby code when needed to test a comment's claim, but keep findings inside the caller's scope.

Accept an ordered standards-source list from the caller. When none is supplied, discover the repository's applicable coding standards before auditing comments. A project rule overrides this skill only when it explicitly requires a comment or directly implies one.

For an incremental verification, inspect the prior report, its finding locations, and the repair diff. Reuse the initial reviewer when follow-up is available. Otherwise give a fresh reviewer that same bounded context. Keep the verification bounded to that context.

## Independent review

Assign the initial audit to a fresh reviewer when delegation is available, and require the reviewer to leave the working tree unchanged. Give it the scope and standards sources without defending existing comments. When delegation is unavailable, perform the same audit in a separate read-only pass based only on the evidence in the code and standards.

## Strictness

Classify every audited comment or suppression under **Hard violations**, **Judgement calls**, or **Kept comments**. Keep one only with cited proof that a project standard requires it or that it records an external constraint, public contract, or safety fact the codebase cannot encode or change. Recommend removal as a hard violation when neither the keep rule nor the judgement-call boundary applies.

Treat these as hard violations:

- A comment that narrates the code, repeats names or types, is stale, marks dead code, or adds emphasis without information.
- A lint or type-system suppression whose correctness or safety problem has an in-scope root-cause fix.
- A workaround, surprise, or constraint comment whose cause can be removed or encoded within the caller's scope without changing architecture, a public API, or product behavior.

Treat a finding as a judgement call when the smallest honest fix changes architecture, a public API, product behavior, or work outside the supplied scope. Describe the smallest root-cause fix and the boundary it crosses. A vague `IMPORTANT`, `do not remove`, ownership note, or historical explanation is not proof by itself.

Recommend the smallest in-scope root-cause fix. A type, runtime check, test, or CI rule is stronger than a comment when it can enforce the claim. Preserve comments that the applicable standards require, including the reason or removal condition those standards demand.

## Report

Return these sections:

- **Scope**: the diff or files checked and the standards consulted.
- **Hard violations**: file and line, the comment or suppression, why it fails, and the smallest in-scope repair.
- **Judgement calls**: the evidence, proposed root-cause fix, and the boundary that prevents automatic repair.
- **Kept comments**: file and line plus the exact standard or unchangeable fact that justifies each keep.
- **Verification**: whether this was an initial or incremental pass, the findings resolved, and any remaining hard violations.

Report zero findings explicitly.
