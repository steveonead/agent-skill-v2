# Reviewing the Diff

Review the change along two axes, one sub-agent each, kept separate so one cannot mask the other:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue, PRD, or ticket?

A change can pass one and fail the other. Code that follows every standard but implements the wrong thing is a Standards pass and a Spec fail. Code that does exactly what the ticket asked but breaks the project's conventions is the reverse.

Report each finding with its fix. The sender does the editing.

## Standards

The documented sources are the rule sets `BEST-PRACTICE-MAP.md` points at, plus anything else in the repo describing how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below, a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins. Where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*. Match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it. If no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type, named from `CONTEXT.md`.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it, inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

On top of the smells, flag two more things in the diff:

- **Dead commentary**: a comment carrying no *why* the code cannot show, or one that logs what changed ("added X", "changed per ticket 12", "was previously Y"). → delete it.
- **Tests that protect nothing**: a test covering behavior a library already guarantees, or asserting on lifecycle hooks, internal state, styling, the attributes a library sets on its own markup, or a large snapshot. → delete it.

## Spec

Against the spec or tickets you were given, report on the diff:

1. Requirements the spec asked for that are missing or partial.
2. Behaviour in the diff that wasn't asked for (scope creep).
3. Requirements that look implemented but where the implementation looks wrong.

Quote the spec line for each finding.
