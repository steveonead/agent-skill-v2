# Backend coding standards

Applies to `apps/backend`. Read `general.md` first.

## Architecture and modules

- Organize each feature under `src/<domain>/` with its controller, module, `dto/`, and `use-cases/`.
- Reserve `Service` for infrastructure and cross-cutting providers. Model business operations as use-cases.
- List every use-case individually in the module's `providers`, with no aggregator provider re-exporting them.
- Export only providers another module injects, normally use-cases.
- Break circular module dependencies by moving the shared piece out or by emitting an event. If `forwardRef()` is genuinely unavoidable, leave a comment naming the cycle it resolves.
- Keep singleton providers. Use request scope only for per-request state. Propagate deep request context through middleware-backed `AsyncLocalStorage`.
- Use constructor injection, `useFactory` for asynchronously created values, and `onModuleInit` for provider initialization. Keep constructors side-effect free.

## API contracts and DTOs

- Backend DTOs subclass shared schemas. Do not redeclare shared contracts in `apps/backend`.

```ts
import { CreateOrderSchema } from '@superdsp/api-schemas';
import { createZodDto } from 'nestjs-zod';

export class CreateOrderDto extends createZodDto(CreateOrderSchema) {}
```

- Under strict validation, `@Body`, `@Param`, and `@Query` require Zod DTO classes. Plain types cause `ZodSchemaDeclarationException` and a 500. `@Req` remains plain, and validated handlers receive schema output after coercion, defaults, and transforms.
- Express 5 uses simple query parsing. Normalize query values before validation:

```text
?filter[status]=active -> { "filter[status]": "active" }
?ids=1&ids=2          -> { ids: ["1", "2"] }
?ids=1                -> { ids: "1" }
```
- Derive a variant with `Schema.omit`/`pick`/`extend`/`partial` on the shared schema instead of hand-writing a near-copy, so the variant tracks the original when it changes.
- Declare every non-204 response with `@ZodResponse({ type, status? })`. It supplies serializer and OpenAPI metadata, and sets `@HttpCode` when `status` is present.
- The global `ZodSerializerInterceptor` validates output. A schema mismatch returns a 500.
- Bare `@Res()` bypasses serialization and the `ok()` envelope. Use passthrough for headers or cookies and `StreamableFile` for streams.
- Keep server-only fields (internal ids, audit columns, anything the frontend must never see) in the module-local `dto/` directory. `@superdsp/api-schemas` is a shared package, and anything placed there is reachable from the browser bundle.
- A controller injecting five or more use-cases is the expected shape, not a smell to refactor around.

## Use-cases and business logic

Put each business operation in `<feature>/use-cases/<verb-noun>.use-case.ts` as a one-method class exposing `execute()`.

```ts
@Injectable()
export class GetOrderUseCase {
  constructor(private readonly prisma: PrismaService) {}

  async execute({ uid, advertiserId }: GetOrderParams): Promise<OrderDetail> {
    const order = await this.prisma.order.findFirst({
      where: { uid, advertiserId, deletedAt: null },
      select: {
        uid: true,
        name: true,
        orderItems: { where: { deletedAt: null }, select: { uid: true } },
      },
    });
    if (!order) throw new NotFoundException();
    return { uid: order.uid, name: order.name /* ... */ };
  }
}
```

- `execute()` takes one object matching the Zod input plus controller context such as `advertiserId` or `organizationId`.
- Throw the matching HTTP exception when a resource is missing or a rule is violated. Returning `null` pushes the decision onto every caller and produces a 200 with an empty body when one caller forgets.
- Return the response shape the contract declares, built explicitly from the queried row. A raw Prisma model leaks columns and changes shape whenever the schema does.
- Extract reusable or intricate rules as pure functions in the feature directory.
- Reuse use-cases directly from controllers, schedulers, and other use-cases. Keep controllers logic-free.

## Controllers and the response envelope

Controllers parse the request, call one use-case, and wrap the response.

```ts
@Post()
@ZodResponse({ type: CreateOrderResponseDto })
async create(@Body() dto: CreateOrderDto, @Req() req: AdvertiserScopedRequest) {
  const { advertiserId, organizationId } = req.advertiserContext;
  return ok(await this.createOrderUseCase.execute({ ...dto, advertiserId, organizationId }));
}
```

- Wrap every JSON response with shared `ok()`, `partialOk()`, or `error()` helpers so it carries the frontend-read internal `statusCode`.
- Use `partialOk()` for batch operations where some items succeeded and some failed, and the request as a whole is still a 200.

## Data access

- Use the singleton `PrismaService` as the only database entry point.
- Inject `PrismaService` directly. Add a feature-local repository only for a concrete data-source swap or an otherwise unavailable test double.
- Narrow queries with `select`, including nested relations, or global `omit`. `include` does not narrow parent columns.

```ts
const groups = await this.prisma.orderGroup.findMany({
  where: { advertiserId, ...(keyword ? { name: { contains: keyword } } : {}) },
  select: { id: true, name: true },
  orderBy: { name: 'asc' },
});
```

- Use `$transaction` when multiple writes must commit or roll back together.
- Inside `$transaction(async (tx) => ...)` every query goes through `tx`.

```ts
await this.prisma.$transaction(async (tx) => {
  // ❌ own connection, outside the transaction, escapes the rollback
  await this.prisma.orderItem.deleteMany({ where: { orderId } });
  // ✅
  await tx.orderItem.deleteMany({ where: { orderId } });
});
```

- The array form takes un-awaited query objects. A query awaited before the `$transaction` call has already run outside it.
- Keep only database work required for atomicity inside transaction callbacks. Move independent validation fetches outside, and avoid per-row loops that risk the transaction timeout.
- Side effects like Slack posts and emails happen after the commit. A rollback undoes the writes and cannot unsend a message.
- Express a concurrency conflict as a conditional write.

```ts
// ❌ lost-update race that no single-threaded test reproduces
const order = await this.prisma.order.findFirst({ where: { id, advertiserId } });
if (order.status !== 'draft') throw new ConflictException();
await this.prisma.order.update({ where: { id }, data: { status: 'submitted' } });

// ✅
const { count } = await this.prisma.order.updateMany({
  where: { id, advertiserId, status: 'draft' },
  data: { status: 'submitted' },
});
if (count === 0) throw new ConflictException();
```

- Acquire locks in one codebase-wide order and retry locking transactions on Prisma `P2034` deadlocks. Prisma does not retry automatically.
- Use tagged `$queryRaw` and `$executeRaw`, never the `Unsafe` variants.
- Map dynamic identifiers through an allow-list because SQL identifiers cannot be parameterized.
- Treat `$queryRaw<T>` as unchecked. Prefer model `count()` because raw MySQL `COUNT` is a `BigInt`.
- Filter soft-deleted rows and nested relations explicitly.
- Keep nullable `deletedAt` out of `@@unique`: MySQL permits multiple `NULL`s and has no partial indexes. For live-row uniqueness, use a non-null live sentinel or a generated column that is `NULL` only for deleted rows.
- Batch per-row queries by collecting ids and using `in`, or by selecting the nested relation in the parent query.
- Push filtering, sorting, and pagination into the query. When SQL cannot express a rule, in-memory computation is acceptable behind a `// NOTE: 刻意簡化:` comment.

## Errors and security

- Let exceptions reach the global filter, which owns the envelope, disclosure, and 5xx alerts. Local formatting catches bypass it.
- Route filters run before global filters. A route-level catch-all replaces the global filter.
- Keep authentication default-closed with the global Bearer-token guard. Mark explicit public routes `@Public()`.
- Anchor tenant isolation on Advertiser context and include `advertiserId` in every tenant-owned read and write. An entity outside Advertiser ownership requires a design change, not an ad-hoc scope.

## E2E testing

- E2E tests assert the HTTP status, envelope, and payload, not provider internals.
- Build requests from the shared endpoint objects, the same source the frontend uses, so a URL or method change fails the test instead of drifting silently.
- The e2e app factory adds only `main.ts` behavior outside `AppModule`, such as the global prefix and cookie parser. `APP_*` pipes, filters, and interceptors already arrive through `AppModule`.
- Load `.env.test` in `setupFiles` before Nest bootstraps.
- Run E2E serially against one shared database with isolation off. A global `beforeEach` resets and reseeds it. Depend on that baseline, leave each test's resulting state in place, and do not add per-test cleanup.
- Await or return every Supertest chain. Do not mix `.end(callback)` with `async`/`await`.
- Create one `request.agent()` per `describe` to isolate cookies and sessions.
