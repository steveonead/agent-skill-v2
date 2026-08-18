# Contract-First Slicing

How to turn user-visible behavior into agent-sized work while frontend and backend remain separate. The unit of planning is a behavior slice. The unit of execution may be a contract-gated FE or BE ticket.

## Scope hierarchy

Use the shallowest hierarchy that keeps each level meaningful:

1. A **requirement** states the complete product outcome.
2. A **feature** is an independently recognizable, demonstrable, or releasable user capability.
3. A **behavior slice** is one narrow user interaction or outcome within a feature.
4. An **execution ticket** is work that one fresh implementation context can complete and verify.

A single-feature requirement can omit feature and behavior-slice planning nodes. A multi-feature requirement places feature issues under the requirement. Add behavior-slice issues only when a feature contains several independent demonstrations. Planning nodes organize outcomes and progress. Execution tickets own implementation work.

For a scope too large to decompose reliably in one context, publish the feature hierarchy first. Preserve ticket quality by expanding each feature in a fresh ticketing session.

## Contract gate

Establish the shared interface before FE and BE implementation diverge. Prefer the repository's existing contract mechanism. Typical fits include schema-first contracts for cross-language boundaries, consumer-driven contracts for independently released consumers and providers, and shared types for a same-language monorepo.

Use a narrow contract ticket when the integration boundary is understood and the repository can validate the artifact. The contract covers one behavior slice, including request, response, errors, and user-visible states needed by that slice. The gate completes when the contract artifact is merged.

Use a walking skeleton when the repository lacks a reliable contract mechanism or important integration assumptions remain unknown. A walking skeleton is a tiny, permanent, real end-to-end path through the principal components. It uses production-shaped integration and establishes the interface that later work deepens. A mock or schema alone is not a walking skeleton.

## Parallel execution

Once the gate completes, FE and BE tickets may enter the frontier together:

- **FE** implements the slice against a contract-derived mock and demonstrates the owned user states.
- **BE** implements the provider behavior, passes contract validation, and verifies its business behavior.
- **Integration** exists only when it owns new integration code, end-to-end tests, deployment work, or another result not owned by FE or BE.

A contract test establishes shared understanding of the interface. It does not replace functional or business-behavior tests. Each execution ticket grades only work it owns.

## Dependencies

Use a blocking edge only when the blocked ticket cannot start safely without the blocker's artifact or decision. Contract or walking-skeleton gates block their FE and BE tickets. FE and BE do not block each other when the contract makes parallel work safe.

Place shared prefactoring at the lowest hierarchy node that owns every affected slice. Prefactoring earns a ticket only when it lowers risk for multiple slices, stays green independently, and has observable acceptance criteria.

Features remain parallel by default. Add cross-feature edges only for genuine product, contract, data, or platform prerequisites.

## Contract evolution

For a backward-compatible contract change, expand the shared contract, migrate consumers and providers in independently green batches, then remove the old form after every migration completes.

For a breaking change, establish a new contract gate and block every affected execution ticket on it. Update the graph before implementation continues. FE and BE tickets do not redefine the shared contract independently.

## Wide refactors

A mechanical change with a codebase-wide blast radius uses an expand-migrate-contract sequence. In this sequence, **Contract** names the cleanup phase that removes the old form, distinct from the shared-interface contract gate:

1. **Expand** adds the new form beside the old while the repository remains green.
2. **Migrate** moves callers in batches defined by independently green repository, package, or team-ownership boundaries. FE and BE batches may proceed in parallel.
3. **Contract** removes the old form after every migration batch completes.

When a migration batch cannot remain green independently, make the temporary integration constraint explicit and assign final integration work to a ticket that owns the resulting verification.

## Quality checks

Every execution ticket answers these questions:

- Which user-visible slice does this work support?
- What artifact or behavior does this ticket own?
- What can be demonstrated or observed when it finishes?
- Could its acceptance criteria fail before this ticket starts?
- Can one fresh implementation context complete it?
- Are all blockers necessary for safe progress?
