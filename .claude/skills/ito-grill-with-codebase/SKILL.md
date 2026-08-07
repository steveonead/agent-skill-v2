---
name: ito-grill-with-codebase
description: Run a relentless interview to sharpen a plan or design. Pass `--batch` for a round of questions at a time.
argument-hint: "給我一個模糊的計畫或想法，我幫你釐清"
disable-model-invocation: true
---

Invoke `domain-modeling`.

Invoke `batch-grilling` when the invocation carries a `--batch` argument. Invoke `grilling` otherwise.

Grill the subject named in the remaining arguments. Without a named subject, grill whatever is under discussion.
