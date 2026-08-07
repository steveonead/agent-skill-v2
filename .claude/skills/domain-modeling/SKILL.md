---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to resolve domain terminology or ubiquitous language, evaluate or record an architectural decision, or when another skill needs to add or change canonical terms, bounded contexts, or architectural decisions.
argument-hint: "要釐清的名詞、要劃的範圍，或要記錄的技術決定是什麼？"
user-invocable: false
---

# Domain Modeling

Read existing domain-context files directly when the task only consumes vocabulary.

## Modeling loop

Run these activities as a loop for the current discussion. Revisit an earlier activity whenever new evidence changes the context, language, boundary, or decision scope.

### Establish the scope

Inspect the repository before discussing or writing the model:

- When root `CONTEXT-MAP.md` exists, read it and identify the bounded context for the current topic. Treat links to legacy `CONTEXT.md` files as migration candidates.
- When no map exists, use root `DOMAIN-CONTEXT.md` as the single context. Read a legacy root `CONTEXT.md` as the domain context and migrate it when making the next change. Treat a repository with neither file as a single context until the first term is resolved.
- For an architectural decision, determine whether its scope is system-wide or limited to one bounded context.
- Ask which context applies only when repository evidence and the current discussion do not resolve it.

Create `DOMAIN-CONTEXT.md` when the first term is resolved. Create an ADR directory only after an ADR passes the gate and the user authorizes writing it.

Complete this activity when the relevant context and the scope for any decision under discussion are known.

### Sharpen the language

During the discussion:

- Surface any conflict between the user's wording and the existing ubiquitous language immediately.
- Replace vague or overloaded wording with one precise canonical term within the applicable bounded context.
- Stress-test domain relationships with concrete edge cases that expose unclear boundaries.
- Check claims about current behavior against the code and surface contradictions.
- Record unresolved disagreements explicitly and name each conflicting meaning.

Complete this activity when every domain term currently under discussion is either resolved to one canonical meaning within the applicable bounded context or marked as unresolved with the conflicting meanings named.

### Record resolved terms

Before editing a domain-context file, read [the shared domain-context rules](./references/DOMAIN-CONTEXT-FORMAT.md) in full. Preserve the language of an existing domain-context file. For a new domain-context file, read [the Traditional Chinese template](./references/DOMAIN-CONTEXT-FORMAT.zh-TW.md) when the user's primary language is Traditional Chinese, or [the English template](./references/DOMAIN-CONTEXT-FORMAT.en.md) when it is English. When the primary language is unclear or unsupported, ask the user to choose English or Traditional Chinese.

Update the applicable `DOMAIN-CONTEXT.md` as soon as a domain term resolves. When migrating a legacy `CONTEXT.md`, rename it and update every affected `CONTEXT-MAP.md` link in the same change. Update root `CONTEXT-MAP.md` when the resolution adds, renames, or moves a bounded context, or changes a relationship-defining domain event, published contract, synchronous API, or shared type.

Complete this activity when every resolved domain term from the current discussion appears once in the correct bounded context and every changed entry follows the shared rules and selected language template.

## ADR branch

Enter this branch when a concrete architectural decision has emerged or the user asks to record one. Exploration remains in the modeling loop until the decision is ready for the gate.

### Apply the ADR gate

Require evidence for every condition below:

1. **Decision**: A durable choice or rule exists. The subject is more than implementation steps, cleanup, migration mechanics, or a temporary experiment.
2. **Architectural reach**: The decision changes a system or bounded-context boundary, responsibility, published interface or data contract, cross-component dependency, key quality attribute, operability model, shared technology policy, or the architectural response to a security or compliance constraint.
3. **Enduring consequence**: The effect outlives the current task or release and either constrains multiple future changes, consumers, or teams, or requires a coordinated, risky, or materially costly reversal.
4. **Genuine choice**: At least two viable alternatives have materially different consequences. Each counted alternative must be viable.
5. **Ready now**: The problem, drivers, affected boundaries and stakeholders, preferred choice, major consequences, and reversal cost are known well enough to decide. Exploration belongs in an RFC, design note, or spike.
6. **Durable value**: Pass this condition only when the rationale lacks an authoritative home in an accepted ADR, standard, policy, or current document. Future maintainers need the rationale to avoid an unsafe reversal or repeated debate.

All six conditions must pass. Implementation effort, line count, file count, organizational visibility, and a wide mechanical refactor do not substitute for architectural reach or enduring consequence. A local UI restructure, backend cleanup, dependency update, rename, or file reorganization normally fails the gate. A cross-product design-system contract, service-boundary change, shared authorization model, or public schema change may pass when every condition is evidenced.

When a condition fails, route the material to another artifact. Name the failed condition and select the smallest fitting artifact: an issue or PR for implementation rationale, a design note for localized design, an RFC or spike for unresolved exploration, or a governing policy or architecture-constraints document for an externally imposed constraint that leaves no genuine choice.

Complete this activity when every condition has a pass or fail result supported by known facts and the next artifact is identified.

### Write the ADR after authorization

When all six conditions pass, offer to create an ADR. Treat an explicit user request to create the ADR as authorization after the gate passes. Otherwise, wait for authorization before writing.

After authorization:

1. Read [the shared ADR content rules](./references/ADR-FORMAT.md), then select the template from the user's primary language. Read [the Traditional Chinese template](./references/ADR-FORMAT.zh-TW.md) for Traditional Chinese. Read [the English template](./references/ADR-FORMAT.en.md) for English. When the primary language is unclear or unsupported, ask the user to choose English or Traditional Chinese.
2. Place a system-wide ADR in root `docs/adr/`. Place a bounded-context ADR in that context's `docs/adr/`.
3. Scan the selected directory for the highest sequential number and create `NNNN-short-slug.md` with the next number.
4. Write the context, decision, and rationale explicitly. Use optional material only when it adds durable information.

Complete this activity when the authorized ADR exists in the correct scope and language, has the next sequential number, and contains context, decision, and rationale.
