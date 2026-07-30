# Test-Driven Development

TDD is the red → green loop. This reference is what makes that loop produce tests worth keeping: what a good test is, what isn't worth testing, where tests go, the anti-patterns, and the rules of the loop.

Keep the loop to unit and integration tests, and leave end-to-end browser tests outside it.

## Discover the stack first

The TDD cycle is universal, the commands are not. Before writing the first test, discover how *this* repository tests, and use its commands for every red, green, and verification step:

- **Language and build system**: `package.json`, `pom.xml`/`build.gradle`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, a `Makefile`
- **Checked-in wrappers**: prefer `./gradlew`, `./mvnw`, `make test`, or a repo script over globally installed tools
- **Test framework and configuration**: and how it runs a single focused test vs the full suite
- **Existing conventions**: where tests live, how files are named, what patterns neighboring tests follow

Run the repository's focused-test command during the loop and its full-suite command at close-out.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely, tests shouldn't. A good test reads like a specification, "user can checkout with valid cart" tells you exactly what capability exists, and survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## What isn't worth testing

Test what would be genuinely bad if it broke, not what raises coverage. One test on the behavior that matters beats ten on the trivia around it, and that gap is widest in the UI, where most of what a component does was decided by whoever built the component library.

Leave code you did not write to whoever wrote it, even when a tool has vendored it into your repo. Test the layer you put on top: your variants, your composition, the behavior the feature promises. What earns a test is a change of yours that alters what the underlying component guarantees.

Out of scope: lifecycle hooks, internal component state, styling, the attributes a library sets on its own markup, and large snapshots.

Heavy environment stubbing to make a test run at all means you are testing at the wrong level. Move it to a level that exercises the real thing, or delete it.

## Seams, where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

## The Prove-It Pattern, for bug fixes

A bug fix starts with a test that reproduces the bug, not with the fix. A test written after the fix proves nothing: you never saw it fail, so you never saw it disagree with the code.

The reproduction test must fail for the bug's own reason. Read the failure message and check it is the reported symptom, rather than a typo, a missing import, or a wrong path.

```typescript
// Bug: "Completing a task doesn't update the completedAt timestamp"

// Step 1: Write the reproduction test (it should FAIL)
it('sets completedAt when task is completed', async () => {
  const task = await taskService.createTask({ title: 'Test' });
  const completed = await taskService.completeTask(task.id);

  expect(completed.status).toBe('completed');
  expect(completed.completedAt).toBeInstanceOf(Date);
});

// Step 2: Fix the bug
export async function completeTask(id: string): Promise<Task> {
  return db.tasks.update(id, {
    status: 'completed',
    completedAt: new Date(),
  });
}

// Step 3: Test passes → bug fixed, regression guarded
```

The reproduction test stays in the suite. It is the guard that stops the same bug coming back.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth, a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead, one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage, not the red → green implementation cycle.
