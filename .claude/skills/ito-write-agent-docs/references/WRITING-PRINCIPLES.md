# Agent Writing Principles

Use these principles for any document an agent consumes, including skills, `AGENTS.md`, `CLAUDE.md`, and files reached through their pointers. The writing goal remains predictability: the agent follows the same process on each run, even when the output should vary.

## Context pointers

A context pointer names material outside the current context and states the condition for loading it. A skill description and an instruction that directs an agent to another file are both pointers.

Write each pointer to perform two jobs: identify the material and name each distinct branch that should load it. Front-load a leading word that the agent will recognize. Keep one trigger for each real branch. Remove identity that the target already supplies.

Sharpen a weak pointer before moving its target inline.

## The two loads

Every document spends one or both of these budgets:

- **Context load**: always-loaded text consumes tokens and attention on every run.
- **Cognitive load**: material without automatic discovery requires the human to remember that it exists and when to request it.

Put universal instructions where the agent always sees them. Put branch-specific material behind a precise pointer. Leave deliberately manual material unpointed only when human judgment should control access.

## Information hierarchy

Rank content by how soon the agent needs it:

1. **In-file steps**: ordered actions the agent performs.
2. **In-file reference**: definitions, rules, and facts consulted while performing those actions.
3. **Disclosed reference**: branch-specific material loaded through a context pointer.

Keep steps visible. **Progressive disclosure** moves branch-specific reference down the hierarchy and behind a precise pointer. **Co-location** keeps a concept's definition, rules, and caveats together under one heading once its hierarchy level is chosen.

Sprawl occurs when a document becomes too long even though its lines remain unique and current. Reduce sprawl by disclosing branch-specific reference or splitting a sequence only where the split earns its added load.

## Steps and completion criteria

End every step with a completion criterion. A strong criterion is both checkable and exhaustive.

Criterion clarity resists premature completion. The visible steps after the current one are its **post-completion steps**, and they pull attention forward. Sharpen a vague boundary before changing the workflow. When the boundary cannot be made precise and post-completion steps demonstrably cause a rush, hide them behind a real context boundary such as a handoff.

Criterion demand controls legwork. Require the agent to account for every relevant item when exhaustive work matters. Legwork belongs inside a step rather than as a separate procedural step.

## Leading words and positive steering

A leading word is a compact, established concept that recruits useful prior knowledge. Repeat the word, rather than its full definition, to anchor related behavior and reduce duplicated prose. Prefer an established term over a coined label that needs its own explanation. Hunt for restatements that a stronger leading word can retire.

**Negation** frames an instruction around unwanted behavior, making that behavior more available. State the required behavior positively. For a hard safety or authorization boundary, state the required behavior first, then add the prohibition when the boundary remains ambiguous.

## Punctuation

Punctuate with commas, colons, periods, and parentheses. Replace an em dash with a colon, a comma, or a sentence break. Replace a semicolon with a period.

## Pruning

**Duplication** gives one meaning multiple authoritative homes. Restore a **single source of truth** by keeping one authoritative place.

Treat the environment as a source of truth. A **cache** is a documented copy of a fact the environment already exposes. Read scripts, configuration, directory structure, and command help instead of caching facts that are cheap to discover and likely to drift. Document conventions, reasons, and gotchas that the environment cannot reveal.

Test every line for relevance. Sediment is the accumulation of stale or irrelevant instructions. Remove stale layers and branches that belong behind pointers.

Run the no-op test on every sentence: would the agent behave differently without it? The answer is model-relative. Settle disagreements by running the document rather than debating the prose. Delete a sentence that does not change behavior. Strengthen a weak leading word when the idea matters but its current wording does not beat the model's default.

## Failure-mode index

When diagnosing misbehavior, test all six modes: **premature completion**, **duplication**, **sediment**, **sprawl**, **no-op**, and **negation**. Use the definitions and remedies above.
