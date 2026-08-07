---
name: ito-debug
description: Diagnose a reported bug through falsifiable hypotheses before repairing it or filing a GitHub issue.
disable-model-invocation: true
---

# Diagnose Bugs

Use the invocation arguments and current conversation as the bug report. Diagnose before modifying code.

## Step 1: Frame the symptom

- Read the repository instructions that govern the affected code.
- State the reported symptom, expected behavior, actual behavior, and available evidence.
- Remind the user to review evidence for credentials, tokens, cookies, authorization headers, personal data, and private paths. Keep user-supplied evidence unchanged after the reminder.
- Present one temporary hypothesis, its falsifiable prediction, and the smallest probe that distinguishes it from alternatives. Name a file, function, line, state transition, or runtime condition when the evidence permits.
- When the current facts cannot support a discriminating probe, provide the smallest read-only probe that the user can run and state what result to return.

Finish when the user can see one unconfirmed hypothesis, its prediction, and a concrete next observation.

## Step 2: Validate the hypothesis

Run the stated probe immediately. Prefer a fast, deterministic, agent-runnable feedback loop that reaches the exact symptom. Measure the underlying system or tool before its higher-level consumer for system or tooling symptoms. Use runtime evidence for lifecycle, async, timing, UI, native, rendering, and generated-artifact symptoms.

For user-only environments, provide one copyable read-only probe, wait for its result, and preserve the hypothesis count. A missing observation is pending evidence rather than a refutation.

Finish when the probe result supports or refutes the prediction with actual evidence.

## Step 3: Confirm, discard, or hand off

- **Supported**: Confirm the root cause only when the evidence explains every observed symptom. State it in one sentence with its exact location or condition.
- **Refuted**: Discard the hypothesis completely, show the result briefly, and create the next hypothesis from the new evidence. Count one refutation.
- **Third refutation**: Stop diagnosis and present the blocked handoff below. Offer `create GitHub issue`, `provide requested evidence`, or `explicitly authorize continued diagnosis`. Limit this branch to the blocked handoff and its three actions.

Use this handoff format after three refutations:

```
Symptom: [one sentence]
Hypotheses tested: [each hypothesis, probe, and why it was ruled out]
Evidence collected: [key logs, repro, environment facts]
Ruled out: [eliminated causes]
Unknowns: [missing facts]
Suggested next steps: [specific evidence or investigation]
Status: blocked
```

Finish when either one root cause is confirmed or the blocked handoff and its three allowed actions are shown.

## Step 4: Report the confirmed diagnosis

Perform a read-only sibling sweep for the confirmed bug pattern. Inspect every match and classify it as `same bug`, `safe`, or `uncertain`. Keep any later repair scoped to the confirmed bug.

Report only the minimum evidence needed to support the conclusion.

Use this concise format:

```
Outcome: [confirmed]
Root cause: [cause and location]
Evidence: [key supporting result]
Verification: [repro, probe, or test result]
Repair: [smallest safe change]
Sibling sweep: [matches checked and classification]
Scope warning: [none, or expected files and shared interfaces]
```

Then offer `repair directly`, `create GitHub issue`, or `report only`. Write code or create an issue after the user selects that action.

Finish when the report and the three actions are shown.

## Step 5: Repair directly

Estimate the repair scope before editing. When it exceeds five hand-written source, test, or configuration files, or changes a shared interface or crosses modules, show the affected scope and strongly recommend a GitHub issue. Wait for a second explicit confirmation before continuing with direct repair.

For an approved repair, follow this sequence:

1. Turn the minimized reproduction into a regression test at the correct seam, one that exercises the real bug pattern at its call site. Run it and observe the unfixed failure.
2. When no correct seam exists, document why, retain the original feedback loop as the guard, and continue with the smallest repair that addresses the confirmed cause.
3. Apply the smallest repair that satisfies the confirmed prediction.
4. Run the regression test to green when it exists. Re-run the original feedback loop against the original scenario.
5. Remove temporary instrumentation and throwaway diagnostic artifacts. Confirm the intended diff and report the outcome, verification result, regression guard, and sibling-sweep disposition.

Limit mutation to the approved repair. Require a separate explicit request for commits and pushes.

Finish when the original symptom is verified fixed, the regression guard is green or its absence is documented, and temporary diagnostics are removed.

## Step 6: Create a GitHub issue

Resolve the current repository from its GitHub remote. Inspect its issue templates or forms and use the applicable template. Build the issue from the confirmed report or blocked handoff, including the symptom, reproduction, expected and actual behavior, evidence, root-cause status, sibling sweep, proposed repair, and verification plan.

Before creating the issue, repeat the evidence-review reminder from Step 1. Use `gh` to create the issue only after the user selected this action. When the remote, authentication, template, or GitHub command blocks creation, state the blocker and provide the completed issue title and body.

Finish when the issue URL is reported, or when the user has a completed issue draft and the specific creation blocker.

## Step 7: Report only

Deliver the confirmed report or blocked handoff as the sole outcome.

Finish when the report is delivered.
