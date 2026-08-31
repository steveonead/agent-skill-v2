# Frontend coding standards

Applies to `apps/frontend`. Read `general.md` first.

## Architecture

### Organize by feature, not by file type

- Put a feature's components, queries, mutations, hooks, stores, and helpers under `src/features/<domain>/`, with tests in a co-located `__test__/`.
- Keep feature changes within one directory. A `components/` plus `hooks/` split hides which parts belong together.
- Promote code to `src/lib/` or `src/components/shared/` only once a second feature actually consumes it. A single caller is not shared code.

### Treat `src/components/ui/` as a vendored dependency

- Generate shadcn components with this repo's Base UI style. Treat `src/components/ui/` as replaceable generated code, and put custom behavior in shared or feature wrappers.

### Route through the API contract objects

- Build every request from the `@superdsp/api-schemas` endpoint object, including its URL, method, and request and response schemas.

```ts
mutationFn: (body: CreateOrderRequest) =>
  sendRequest(
    { method: createOrderEndpoint.method, url: createOrderEndpoint.url, data: body },
    { schema: createOrderEndpoint.responseSchema },
  ),
```

### Split components at a seam, not at a line count

- Simplify in place first. Extract when a piece has its own reason to change and a narrow interface: a business rule, a reusable primitive, a boundary someone else will call.
- A 300-line component with one job stays. A 60-line component doing two jobs splits.

### Keep data access out of presentational components

- `useQuery` and `useMutation` belong in a route component or feature hook. Leaf components take props and callbacks so they remain reusable.

```tsx
// ❌ refetches once per instance in a list, needs a QueryClient to test
function OrderNameCell({ orderId, advertiserId }: { orderId: number; advertiserId: number }) {
  const { data } = useQuery(orderDetailQueryOptions({ advertiserId, orderId }));
  return <td>{data?.name}</td>;
}

// ✅
function OrderNameCell({ order }: { order: Order }) {
  return <td>{order.name}</td>;
}
```

## State management

### Choose state location by its source of truth

| Source of truth | Where it belongs | Signal |
| --- | --- | --- |
| The server | TanStack Query cache | The value can change without this browser doing anything |
| The URL | Route `validateSearch` plus `Route.useSearch()` | A user pasting the link should see the same view: filters, pagination, sorting, active tab |
| One component | `useState` | Nothing outside the component reads it |
| Distant components | Zustand store | Shared across a subtree too wide for props, and purely client-owned |
| A form in progress | Form library state | Values are drafts until submit |

- Each source has its own lifecycle. Copying server or URL state creates a second source of truth that drifts.

### Derive, do not sync

- Store the smallest client fact and derive rendered values from it and server data. Do not synchronize the derived value with an effect.

```tsx
const { data: orders } = useQuery(orderListQueryOptions(advertiserId));
const [selectedId, setSelectedId] = useState<number | null>(null);

// Derived: a selection that vanished server-side falls back on its own.
const selected = orders?.items.find((o) => o.id === selectedId) ?? orders?.items[0];
```

### URL state is declared once on the route

- Define search params with `validateSearch` and a Zod schema on the route, then read them through `Route.useSearch()` and write them through `navigate({ search })`.

```tsx
// ❌ a second source of truth, lost on reload and on back navigation
const [page, setPage] = useState(1);

// ✅
const { page } = Route.useSearch();
navigate({ search: (prev) => ({ ...prev, page: prev.page + 1 }) });
```

- Why: the route schema gives defaults, validation, and types in one place.

## React

### Write the React 19 element APIs

- Use React 19 element APIs. Accept `ref` as a prop and render context as `<Context>`.

### Render is pure, and the compiler depends on it

- Treat props, state, hook inputs, hook outputs, and values passed to JSX as immutable. Mutation can invalidate compiler caching.

### Skip manual memoization

React Compiler runs in infer mode over the whole app, so `useMemo`, `useCallback`, and `React.memo` are noise in new code. Two exceptions remain real:

- A value used as a `useEffect` dependency, where referential stability changes how often the effect runs.
- A component holding a mutable library instance the compiler cannot model, such as TanStack Table's `useReactTable`: those components opt out with `'use no memo'`, removable when the compiler learns to model such instances.

### Treat `'use no memo'` as a tracked debt

- When a component must opt out, pair the directive with a comment stating what breaks and the condition for removing it. An untracked escape hatch becomes permanent.

### Effects synchronize with external systems only

- Subscriptions, timers, imperative DOM handles, and analytics belong in effects. Compute derived values during render, and fetch through Query.
- Reset a subtree's state by passing the identity prop as `key`, and adjust part of the state during render. A reset effect renders the stale state for one frame first.

### Compose with children, not with boolean props

- Replace accumulating boolean variants with composable children and context read through `use()`. Each boolean multiplies render paths.

### Prefer Query's optimistic pattern over `useOptimistic`

- Anything backed by a query cache updates through `onMutate` and `onError`, so the rollback and the cache stay in one place. Reserve `useOptimistic` for actions with no query behind them.

### Virtualize long lists

- Virtualize any list that can grow unbounded. The compiler removes re-render cost, not DOM node cost.

## TanStack Query

### Write Query v5, not v4

- `useQuery` has no `onSuccess`, `onError`, or `onSettled`. Mutations keep all three. Derive values during render. Run external side effects in `useEffect` keyed by destructured query data.
- Pending state reads through `isPending` (status is `pending`). `isFetching` means a request is in flight, and `isLoading` is `isPending && isFetching`, the first load only.
- Keep prior list data with `placeholderData: keepPreviousData`. Placeholder status is `success`, so indicate it with `isPlaceholderData`, not `isPending`.

### `queryOptions()` is the unit of reuse

One definition feeds `useQuery`, `useSuspenseQuery`, `prefetchQuery`, and route loaders, so key and fetcher can never disagree between a loader and the component it primes.

### One key factory per feature, broad to narrow

- Declare keys with `createQueryKeys()` from the shared query-key factory module, in the feature's `queries/keys.ts`. A key array never appears inline at a call site.
- Order key segments from broad to narrow so a partial key invalidates everything below it.

```ts
export const orderKeys = createQueryKeys('order', {
  list: (advertiserId: number, filters?: OrderListFilters) =>
    [advertiserId, filters ?? {}] as const,
  detail: (params: { advertiserId: number | undefined; orderId: number }) => [params] as const,
});
// orderKeys.all() invalidates every order query, list included.
```

- Treat the query key as the queryFn's dependencies. Include every fetched variable and change the key instead of calling `refetch()` from an effect.

### Set `staleTime` deliberately

- Raise the project default for data that rarely changes, lower it for data a user expects to be live. Keep `gcTime` at or above `staleTime`, otherwise an entry dropped after unmount forces a refetch on remount for data that should still be fresh.

### Invalidate through `mutation.meta.invalidates`

- Declare invalidated keys in `mutation.meta.invalidates`. The global `MutationCache.onSuccess` invalidates them.
- `meta.invalidates` is this project's convention built on typed `mutationMeta`, not an official TanStack API, so expect no upstream documentation for it.
- Use `meta.errorToast` for a message and `meta.skipGlobalError` for local handling. Deduplicate system failures under the shared app-wide toast id.
- A queryFn signals failure only by throwing or rejecting. A raw `fetch` without an `!response.ok` check leaves the query with no retry, no error UI, and no `meta.errorToast`.

```ts
// ❌ swallows the rejection into a permanent success state with empty data
queryFn: () => fetchOrders(advertiserId).catch(() => null),
```

```ts
useMutation({
  mutationFn: updateOrder,
  meta: {
    invalidates: [orderKeys.all()],
    errorToast: 'Update failed. Please try again.',
  },
});
```

### Optimistic updates follow a fixed order

- Optimistic updates cancel in-flight queries, snapshot, write, restore in `onError`, then invalidate through `meta.invalidates`.

### `select` must be a stable reference

- Define `select` at module scope so its stable reference lets Query reuse the previous selection.

## TanStack Router

### Guards live in `beforeLoad`

- Put shared authentication and access guards in a pathless route's `beforeLoad`. Read router context and `throw redirect()` before loaders and queries run.
- A route guard is user experience, not an authorization boundary. The server enforces access on every request.

### Loaders prime the cache, components subscribe

- Start `prefetchQuery` without awaiting for a non-blocking loader. Return `ensureQueryData` to block the transition. Components subscribe with the same options through Query hooks. Do not use `useLoaderData` for query-backed server data.

```ts
export const Route = createFileRoute('/orders/$orderId')({
  loader: ({ context, params }) =>
    context.queryClient.ensureQueryData(
      orderDetailQueryOptions({ advertiserId: context.advertiserId, orderId: params.orderId }),
    ),
  component: OrderDetailPage,
});
```

- Set `defaultPreloadStaleTime: 0` so Query's `staleTime` remains the sole freshness authority.

### Choose suspense per data importance

- Use `useSuspenseQuery` with a blocking loader and `errorComponent` for page-critical data. Use `useQuery` with `isPending` for secondary panels.

### Route error and pending UI come from router defaults

- Configure shared error, not-found, and pending UI on router defaults. Override only routes that differ.

## Zustand

### Stores hold client state only

- API-backed state belongs in Query. Stores hold client choices.

### One store per domain

- Name one-concern stores `use[Domain]Store`. Keep view-defining filters in the URL.

### Put actions in a stable `actions` object

- Group actions in one stable `actions` object and expose a selector hook so action-only consumers do not re-render.
- When a store uses `persist`, exclude `actions` via `partialize`. JSON serialization writes the group back as an empty object, and the default shallow merge then overwrites the real actions on rehydration.

```ts
export function useOrderTableColumnVisibility() {
  return useOrderTableStore((state) => state.columnVisibility);
}

export function useOrderTableActions() {
  return useOrderTableStore((state) => state.actions);
}
```

### Select primitives individually

- Select one primitive per hook. Wrap unavoidable object selectors in `useShallow` to keep references stable.

## Tailwind

### Configure in CSS

- Define design tokens in the CSS entry's `@theme` and use Tailwind v4 idioms.
- Use complete literal class names so Tailwind can discover them.

```tsx
// ❌ never appears in the scanned source, so v4 generates nothing
<Badge className={`bg-${color}-600`} />
// ✅
const badgeTone: Record<OrderStatus, string> = { draft: 'bg-slate-600', live: 'bg-emerald-600' };
<Badge className={badgeTone[status]} />
```

### Arbitrary values are temporary

- Reach for a built-in token first. When the same arbitrary value appears roughly three times, promote it to a `@theme` token and replace the usages.

### `@apply` is for base styles and third-party overrides

- Reuse component styles through a React component that accepts `className` and merges with `cn()`.

### Style from existing state attributes

- Style Base UI's part-specific data attributes with variants instead of mirroring state in JS. Check each part's API reference for its attributes.

```tsx
<AccordionTrigger className="data-panel-open:bg-muted data-disabled:opacity-50" />
```

## Testing with React Testing Library

### Query the way a user finds things

- Query by role, label, then visible text. Use `getByTestId` last, and assert only user-observable behavior.
- Create a user with `userEvent.setup()` and await every interaction. Reserve `fireEvent` for non-user events. Treat `act` warnings as async-completion signals first. Use manual `act()` only for APIs Testing Library does not wrap.

### `waitFor` callbacks assert, nothing else

- A `waitFor` callback contains one assertion and no side effects. Use `findBy*` for appearance.

### One custom `render` for providers

- Provide one test-utils `render` with QueryClient, router, and theme providers. Re-export `screen` and `userEvent`, and create a fresh QueryClient per test.
