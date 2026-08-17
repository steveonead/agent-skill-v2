# Agent Writing Principles

Use these principles for any document an agent consumes, including skills, `AGENTS.md`, `CLAUDE.md`, and files reached through their pointers. The writing goal is predictable behavior: the document reliably serves the same intent even when the agent's method and output should vary with context.

## Instruction depth

Give the agent the judgment it needs before prescribing a procedure:

- **When** identifies the conditions, branches, and scope in which an instruction applies.
- **What** defines the intended outcome, constraints, evidence, and completion conditions.
- **Why** explains a non-obvious boundary, tradeoff, or reason the agent needs in order to generalize correctly.
- **How** specifies a method or sequence.

Emphasize When, What, and Why. Reserve Why for reasoning that changes judgment rather than explaining familiar concepts. Prescribe How when correctness, safety, authorization, interoperability, or determinism depends on a particular method or sequence. Otherwise, leave implementation choices to the agent.

## Context pointers

A context pointer names material outside the current context and states the condition for loading it. A skill description and an instruction that directs an agent to another file are both pointers.

A complete pointer identifies the material and names each distinct branch that should load it. Use a recognizable leading word and one trigger for each real branch.

## The two loads

Every document spends one or both of these budgets:

- **Context load**: always-loaded text consumes tokens and attention on every run.
- **Cognitive load**: material without automatic discovery requires the human to remember that it exists and when to request it.

Universal instructions belong where the agent always sees them. Branch-specific material belongs behind a precise pointer. Deliberately manual material remains unpointed when human judgment should control access.

## Information hierarchy

Place content according to when the agent needs it:

1. **In-file instructions**: outcomes, constraints, and ordered actions whose sequence matters.
2. **In-file reference**: definitions, rules, and facts consulted while acting.
3. **Disclosed reference**: branch-specific material loaded through a context pointer.

Keep decision-critical instructions visible. **Progressive disclosure** moves branch-specific reference down the hierarchy and behind a precise pointer. **Co-location** keeps a concept's definition, rules, and caveats together under one heading once its hierarchy level is chosen.

Sprawl occurs when a document becomes too long even though its lines remain unique and current. Reduce sprawl by disclosing branch-specific reference or splitting a sequence only where the split earns its added load.

## Completion criteria

Set checkable completion criteria for the overall result and for boundaries where premature completion creates meaningful risk. Require an exhaustive account when missing one relevant item would make the result unreliable.

Use ordered steps when order changes the result. Keep flexible work outcome-oriented, and let the agent choose the supporting legwork.

## Leading words and positive steering

A leading word is a compact, established concept that recruits useful prior knowledge. Use it consistently to anchor related behavior and remove repeated explanations. Prefer an established term over a coined label that needs its own explanation.

**Negation** frames an instruction around unwanted behavior, making that behavior more available. State the required behavior positively. For a hard safety or authorization boundary, state the required behavior first, then add the prohibition when the boundary remains ambiguous.

## Punctuation

Punctuate with commas, colons, periods, and parentheses. Replace an em dash with a colon, a comma, or a sentence break. Replace a semicolon with a period.

## Pruning and coherence

**Duplication** gives one meaning multiple authoritative homes. Restore a **single source of truth** by keeping one authoritative place.

Treat the environment as a source of truth. A **cache** is a documented copy of a fact the environment already exposes. Keep cheap, drift-prone facts discoverable from scripts, configuration, directory structure, or command help out of the document. Document conventions, reasons, and gotchas that the environment cannot reveal.

**Sediment** is stale or irrelevant instruction left behind as the document evolves. Test each sentence for relevance: would the agent behave differently without it? The answer is model-relative. Delete sediment and no-op prose. Strengthen a weak leading word when the idea matters but its current wording does not beat the model's default.

Prune the document as a whole rather than treating cuts as independent wins. Review the resulting document against the user's intent. It must remain logically clear, preserve every required behavior, and contain no contradictory instructions.

## Failure-mode index

When diagnosing misbehavior, test all eight modes: **premature completion**, **duplication**, **sediment**, **sprawl**, **no-op**, **negation**, **intent drift**, and **contradiction**.

**Intent drift** occurs when a revision no longer produces the behavior the user requested. Compare the complete candidate with the request and settled decisions.

**Contradiction** occurs when instructions require incompatible behavior. Resolve the conflict in favor of the user's intent and the applicable authoritative source.
