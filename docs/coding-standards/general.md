# General coding standards

Applies to `apps/frontend`, `apps/backend`, and `packages/*`. Frontend and backend work also follows its scope-specific standard.

Oxlint enforces the mechanical rules. This document covers the judgment lint cannot check.

## TypeScript

### Types as constraints, not decoration

- Model mutually exclusive states as discriminated unions. Optional fields admit impossible states.
- Close every union switch with a `never` assignment so adding a variant becomes a compile error instead of a silent fallthrough.

```ts
type Result =
  | { status: 'success'; data: Order }
  | { status: 'failure'; reason: string }

function render(result: Result) {
  switch (result.status) {
    case 'success': return result.data.name
    case 'failure': return result.reason
    default: {
      const unreachable: never = result
      return unreachable
    }
  }
}
```

- Use literal unions for fixed strings and branded types for non-interchangeable IDs.
- Make invalid states unconstructable.

```ts
// ❌ every consumer must handle an empty batch
type Batch = { orders: Order[] }

// ✅ the type guarantees at least one order
type Batch = { orders: readonly [Order, ...Order[]] }
```

- Strengthen types until partiality no longer leaks into callers. A non-null assertion, `arr[0] as T`, or an impossible-case throw signals a weak type. Push that case into the signature, then stop when more precision adds ceremony without safety.
- Use `readonly` at call boundaries to show that a function does not mutate its argument. It is shallow. Model nested readonly fields explicitly, and use `as const` for literal values.

### Inference and assertions

- Infer local variables and internal returns. Annotate exported API contracts. Redundant annotations drift.
- Use `satisfies` to check a value without widening its literals.

```ts
const routes = {
  order: '/orders/:id',
  report: '/reports/:id',
} satisfies Record<string, `/${string}`>

// typeof routes.order is '/orders/:id', not string
```

- Treat external, untyped, and caught values as `unknown`, then narrow before use. Avoid `any` because it disables downstream checking. Check `instanceof Error` before reading a caught value's `.message`.
- Narrow instead of asserting. Prefer a discriminant, then `in`, `typeof`, or `instanceof`, a named guard or assertion function, and Zod at system boundaries. Reserve `as` for test fixtures, confirmed DOM lookups, and third-party type gaps.

```ts
// ❌ compiles even when result is a failure
const name = (result as Extract<Result, { status: 'success' }>).data.name

// ✅ the discriminant proves it at runtime
const name = result.status === 'success' ? result.data.name : undefined
```

- Extract repeated narrowing into a named guard, and ensure its body proves the predicate.
- Derive types from their owning declarations with `Pick`, `Omit`, `ReturnType`, `Awaited`, `typeof`, or `z.infer`. Parallel hand-written shapes drift.

### Repo conventions

- Declare object shapes with `type`. This repo does not use `interface`, including where mainstream guidance would.
- Express fixed sets as literal unions or `as const` objects. This repo does not use `enum`.

### Function signatures

- Take an object when two parameters share a primitive type, because no signature catches a swap.

```ts
// ❌ transfer(toId, fromId) compiles and moves the money backwards
function transfer(fromId: number, toId: number) {}

// ✅ transfer({ toId, fromId }) is the same call
function transfer({ fromId, toId }: { fromId: number; toId: number }) {}
```

- Name values that repeatedly travel together as one object type. Keep short, type-distinct parameters positional.

### Control flow

- Express a pure input-to-output mapping as a `Record` or `Map` lookup rather than an `if`/`switch` chain.

```ts
// ❌ a new status slips through to the fallback
function labelOf(status: OrderStatus) {
  if (status === 'draft') return 'Draft'
  if (status === 'active') return 'Active'
  return 'Unknown'
}

// ✅ a new status is a compile error
const ORDER_STATUS_LABEL: Record<OrderStatus, string> = { draft: 'Draft', active: 'Active' }
```

- The same branching on the same type appearing a second time is the moment to move it into one shared lookup.
- Run independent async work through `Promise.all`, or `Promise.allSettled` when partial failure is acceptable. Sequential `await` on independent calls silently multiplies latency.
- Every catch must log and rethrow, or log with a comment explaining why continuation is safe. Include enough identifiers to reconstruct the case.
- Deep-copy with `structuredClone`. Use `es-toolkit`'s `cloneDeep` only to preserve class prototypes. It keeps functions by reference.

### Modules

- Use named exports only. Avoid defaults and barrel `export *` so rename and source tracing remain accurate without directory-wide imports.
- Export parsed domain shapes, not transport, storage, or framework types, so boundary changes remain local.

### Complexity budget

- Keep decisions in pure functions and leave the framework layer mechanical. Logic that needs a request, a component, or a container to run can only be exercised by constructing one.
- Prefer simple data shapes to deep conditional or recursive types. Most hard type problems are data-modeling problems.
- Delete abstractions unused by the current requirement. Speculative layers impose cost before proving value.
- One change spread across many files signals split ownership. Unrelated changes in one file signal mixed responsibilities. Move code rather than add a layer.

## Zod

### Schemas are the API contract

- `@superdsp/api-schemas` is the single source of truth for every request and response shape crossing the frontend and backend boundary. Both sides import from it. Neither side declares its own copy of a shape the other also knows about.
- Each endpoint is expressed as an endpoint object carrying its URL, method, and schemas together, so a route change cannot land on one side only.
- Derive types with `z.infer`.
- Validation is Zod everywhere. class-validator has no place in this codebase.

### List endpoint naming contract

Every paginated list endpoint uses these names, without variation:

- Request: `page`, `limit`, `keyword`.
- Response: `items`, `totalCount`, `totalPage`.

Shared client-side pagination, table, and query code depends on these names. A single endpoint that renames one field forces a special case through every layer above it.

### Parse at the boundary

- Parse untrusted input exactly once, where it enters the system: HTTP request bodies and query strings, HTTP responses from external services, `localStorage`, URL params, and file or message payloads. Past that point, trust the inferred type.
- Re-validating a value downstream distrusts the type system and spreads the blast radius of every schema change. A downstream function that feels like it needs to re-validate means the parse sits in the wrong place.
- Use `safeParse` where failure is an expected outcome to handle: user input, third-party responses, stored values. Use `parse` where failure means a broken contract or a programmer error, including responses from our own backend, and let it surface.

### Write Zod 4, not Zod 3

Use Zod 4 APIs. Deprecated Zod 3 forms may still compile. Two differences affect behavior:

- `.default()` requires an output-typed fallback. Use `.prefault()` when the fallback must pass through coercion or transforms.

```ts
z.coerce.number().default(1)
z.coerce.number().prefault('1')
```
- A `z.coerce` field no longer absorbs a missing key. Decide what absence means and mark the field `.optional()` or `.default()`, otherwise a request that omits an optional filter fails with `invalid_type`.

### Schema construction

- Use `z.discriminatedUnion` whenever the variants share a discriminator key. `z.union` tries every branch and merges the failures into an unreadable error.
- Use `z.strictObject` for request schemas (bodies and query strings) so unexpected client fields surface as errors. Use plain `z.object` for response schemas, so an additive backend field does not break a deployed frontend that parses the response.
- Use `.refine` for a single condition and `.superRefine` when one validation pass must emit several issues or attach custom paths. Chained `.refine` calls all run and all report, because checks are continuable by default, but each `.refine` emits at most one issue.
- Write recursive schemas with the v4 getter syntax, and bound the depth wherever nesting is attacker-controlled. Unbounded recursion is a stack-overflow vector with getters and `z.lazy` alike.

### Input and output types

Transforms and coercions make schema input and output types differ. `z.infer` is the output type.

```ts
const QuerySchema = z.object({ page: z.coerce.number() })

type QueryIn = z.input<typeof QuerySchema>   // { page: unknown }
type QueryOut = z.output<typeof QuerySchema> // { page: number }, same as z.infer
```

Use `z.input` for `.parse()` input and `z.output` for its result.

## Testing

### Test behavior and intent

- Test descriptions state why behavior matters, not the function name.
- Assert on observable outcomes: return values, thrown errors, persisted state, rendered output. Assert on an internal call only where the call itself is the contract (an outbound HTTP request, an emitted event).
- A test that keeps passing after the business rule changes is not protecting anything. A test that fails on a pure refactor with no behavior change is a liability.
- Await every `.resolves` and `.rejects` assertion. Use `expect.assertions(n)` when assertions are inside a callback or `catch`, so skipped paths fail.
- When removed behavior needs regression protection, assert the external behavior that would break, rather than asserting that code or an internal call is gone.

### Mock discipline

- Mock slow, flaky, or side-effecting boundaries. Use real implementations elsewhere.
- Keep the unit under test real. When passing requires mocking most of the thing being tested, the test is testing the mock.
- Use `vi.spyOn` for existing methods and `vi.fn()` for standalone stubs. Enable `restoreMocks` or restore spies explicitly.
- Restore fake timers in `afterEach`, and use the `*Async` timer APIs for async code. Change environment variables and globals through `vi.stubEnv` and `vi.stubGlobal`.

### Mock hoisting

`vi.mock()` calls are hoisted above all imports, so a factory that closes over a module-scope variable reads it before it is assigned. Use `vi.hoisted()` for anything the factory needs.

```ts
const { fetchSpy } = vi.hoisted(() => ({ fetchSpy: vi.fn() }))

vi.mock('./api-client', () => ({ fetchOrder: fetchSpy }))
```

### Test configuration

- Use `node` for pure logic and API tests, and a DOM environment only for DOM code.
- Use targeted inline snapshots. Avoid whole-tree snapshots.
