# Best Practice Map

## 不適用

- `apps/frontend/src/components/ui` 內為 shadcn/ui 的基礎 UI，在 Code Review 時直接跳過，不作任何修改

## frontend (apps/frontend — Vite + React + TanStack Router + TanStack Query)

- **js-ts-best-practices** (`.agents/skills/js-ts-best-practices/SKILL.md`): TypeScript 型別定義、utility function、module 結構
- **react-best-practices** (`.agents/skills/react-best-practices/SKILL.md`): React component、hook、context 的實作與審查
- **shadcn**: shadcn/ui component 新增、修改、組合（`apps/frontend/src/components/ui` 內的基礎元件除外）
- **tailwind-best-practices** (`.agents/skills/tailwind-best-practices/SKILL.md`): className 撰寫、responsive 設計、設計 token 使用
- **tanstack-best-practices** (`.agents/skills/tanstack-best-practices/SKILL.md`): TanStack Router 路由設計、loader、search params；TanStack Query 的 query/mutation
- **zod-best-practices** (`.agents/skills/zod-best-practices/SKILL.md`): API response 型別驗證、表單 schema 定義、runtime type guard
- **zustand-best-practices** (`.agents/skills/zustand-best-practices/SKILL.md`): Zustand store 設計、效能優化、middleware 組合、TypeScript 型別
- **vitest-best-practices** (`.agents/skills/vitest-best-practices/SKILL.md`): utility function 與 custom hook 的 unit test
- **rtl-best-practices** (`.agents/skills/rtl-best-practices/SKILL.md`): component 整合測試、使用者互動流程驗證

## backend (apps/backend — NestJS + Prisma)

- **js-ts-best-practices** (`.agents/skills/js-ts-best-practices/SKILL.md`): TypeScript 型別設計、decorator 使用、DI pattern
- **nestjs-best-practices** (`.agents/skills/nestjs-best-practices/SKILL.md`): module / controller / service / guard / interceptor 架構設計與審查
- **zod-best-practices** (`.agents/skills/zod-best-practices/SKILL.md`): DTO 驗證、config schema、環境變數型別安全
- **vitest-best-practices** (`.agents/skills/vitest-best-practices/SKILL.md`): service unit test、helper function 測試、mock 外部依賴
- **supertest-best-practices** (`.agents/skills/supertest-best-practices/SKILL.md`): NestJS e2e 測試撰寫、Supertest 請求建構、server 生命週期管理

## packages (packages/\*)

- **js-ts-best-practices** (`.agents/skills/js-ts-best-practices/SKILL.md`): 共享型別設計、monorepo 模組邊界、package exports 設定
- **zod-best-practices** (`.agents/skills/zod-best-practices/SKILL.md`): 共享 Zod schema 定義（api-schemas）、跨前後端 API contract 設計
- **vitest-best-practices** (`.agents/skills/vitest-best-practices/SKILL.md`): schema unit test、helper function 測試
