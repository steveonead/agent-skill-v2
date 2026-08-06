---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to resolve domain terminology or ubiquitous language, evaluate or record an architectural decision, or when another skill needs to add or change canonical terms, bounded contexts, or architectural decisions.
---

# Domain Modeling

Read existing context files without invoking this skill when only consuming vocabulary.

## Step 1: Locate the context

Inspect the repository before discussing or writing the model:

1. When root `CONTEXT-MAP.md` exists, read it and identify the bounded context for the current topic.
2. Otherwise, use root `CONTEXT.md` as the single context. Treat a repository with neither file as a single context until the first term is resolved.
3. For an architectural decision, determine whether its scope is system-wide or limited to one bounded context.
4. Ask which context applies only when repository evidence and the current discussion do not resolve it.

Create `CONTEXT.md` when the first term is resolved. Create an ADR directory only after an ADR passes the gate and the user authorizes writing it.

Finish when the relevant context and the scope for any decision under discussion are known.

## Step 2: Sharpen the language

During the discussion:

- Surface any conflict between the user's wording and the existing glossary immediately.
- Replace vague or overloaded wording with one precise canonical term within the applicable bounded context.
- Stress-test domain relationships with concrete edge cases that expose unclear boundaries.
- Check claims about current behavior against the code and surface contradictions.
- Record unresolved disagreements explicitly and name each conflicting meaning.

Finish when every domain term currently under discussion is either resolved to one canonical meaning within the applicable bounded context or marked as unresolved with the conflicting meanings named.

## Step 3: Record resolved terms

Before editing a context file, read [the shared context rules](./references/CONTEXT-FORMAT.md) in full. Preserve the language of an existing context file. For a new context file, read [the Traditional Chinese template](./references/CONTEXT-FORMAT.zh-TW.md) when the user's primary language is Traditional Chinese, or [the English template](./references/CONTEXT-FORMAT.en.md) when it is English. When the primary language is unclear or unsupported, ask the user to choose English or Traditional Chinese.

Update the applicable `CONTEXT.md` as soon as a domain term resolves. Update root `CONTEXT-MAP.md` when the resolution adds, renames, or moves a bounded context, or changes a relationship-defining domain event, published contract, synchronous API, or shared type.

Finish when every resolved domain term from the current discussion appears once in the correct bounded context and every changed entry follows the shared rules and selected language template.

## Step 4: Apply the ADR gate

Evaluate an ADR only when a concrete decision has emerged or the user asks to record one. Require evidence for every condition below:

1. **Decision**: A durable choice or rule exists. The subject is more than implementation steps, cleanup, migration mechanics, or a temporary experiment.
2. **Architectural reach**: The decision changes a system or bounded-context boundary, responsibility, published interface or data contract, cross-component dependency, key quality attribute, operability model, shared technology policy, or the architectural response to a security or compliance constraint.
3. **Enduring consequence**: The effect outlives the current task or release and either constrains multiple future changes, consumers, or teams, or requires a coordinated, risky, or materially costly reversal.
4. **Genuine choice**: At least two viable alternatives have materially different consequences. Each counted alternative must be viable.
5. **Ready now**: The problem, drivers, affected boundaries and stakeholders, preferred choice, major consequences, and reversal cost are known well enough to decide. Exploration belongs in an RFC, design note, or spike.
6. **Durable value**: Pass this condition only when the rationale lacks an authoritative home in an accepted ADR, standard, policy, or current document. Future maintainers need the rationale to avoid an unsafe reversal or repeated debate.

All six conditions must pass. Implementation effort, line count, file count, organizational visibility, and a wide mechanical refactor do not substitute for architectural reach or enduring consequence. A local UI restructure, backend cleanup, dependency update, rename, or file reorganization normally fails the gate. A cross-product design-system contract, service-boundary change, shared authorization model, or public schema change may pass when every condition is evidenced.

When a condition fails, route the material to another artifact. Name the failed condition and select the smallest fitting artifact: an issue or PR for implementation rationale, a design note for localized design, an RFC or spike for unresolved exploration, or a governing policy or architecture-constraints document for an externally imposed constraint that leaves no genuine choice.

Finish when every condition has a pass or fail result supported by known facts and the next artifact is identified.

## Step 5: Offer and write an ADR

When all six conditions pass, offer to create an ADR. Treat an explicit user request to create the ADR as authorization after the gate passes. Otherwise, wait for authorization before writing.

After authorization:

1. Read [the shared ADR content rules](./references/ADR-FORMAT.md), then select the template from the user's primary language. Read [the Traditional Chinese template](./references/ADR-FORMAT.zh-TW.md) for Traditional Chinese. Read [the English template](./references/ADR-FORMAT.en.md) for English. When the primary language is unclear or unsupported, ask the user to choose English or Traditional Chinese.
2. Place a system-wide ADR in root `docs/adr/`. Place a bounded-context ADR in that context's `docs/adr/`.
3. Scan the selected directory for the highest sequential number and create `NNNN-short-slug.md` with the next number.
4. Write the context, decision, and rationale explicitly. Use optional material only when it adds durable information.

Finish when the authorized ADR exists in the correct scope and language, has the next sequential number, and contains context, decision, and rationale.
