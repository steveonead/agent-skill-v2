#!/usr/bin/env bash
# 兩邊皆可用，依來源取出要處理的檔案清單：
#   Claude Code Edit/Write → tool_input.file_path（單一絕對路徑）
#   Codex apply_patch       → tool_input.command（raw patch，解析 "*** Add/Update File:" 取路徑，可多檔）
#
# 只報不改：eslint 不帶 --fix，也不跑 prettier。
# hook 一旦改寫檔案，harness 會把整份新檔塞回對話，這比報錯本身貴得多。
# 格式化交給 git pre-commit（lint-staged），不進對話。
INPUT=$(cat)

ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"

# 先取 Claude 的 file_path；若無則解析 Codex apply_patch 的 patch 內容
FILES=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')
if [ -z "$FILES" ]; then
  PATCH=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')
  FILES=$(printf '%s\n' "$PATCH" \
    | grep -oE '^\*\*\* (Add|Update) File: .+' \
    | sed -E 's/^\*\*\* (Add|Update) File: //')
fi

[ -z "$FILES" ] && exit 0

LINT_EXIT=0

while IFS= read -r FILE; do
  [ -z "$FILE" ] && continue

  # 只處理 JS/TS 檔案
  [[ "$FILE" =~ \.(js|mjs|cjs|ts|mts|cts|jsx|tsx)$ ]] || continue

  # apply_patch 路徑為 repo 相對；補成絕對路徑（Claude 的 file_path 已是絕對）
  case "$FILE" in
    /*) ABS="$FILE" ;;
    *)  ABS="${ROOT:+$ROOT/}$FILE" ;;
  esac
  [ -f "$ABS" ] || continue

  # 找最近的 package 根目錄（含 eslint.config.mjs 的目錄）
  # ESLint flat config 以 CWD 定位設定檔——必須 cd 到正確的 package 根目錄
  PKG_DIR=$(dirname "$ABS")
  while [ "$PKG_DIR" != "/" ]; do
    [ -f "$PKG_DIR/eslint.config.mjs" ] && break
    PKG_DIR=$(dirname "$PKG_DIR")
  done
  [ "$PKG_DIR" = "/" ] && continue

  # eslint 只檢查：error 寫 stderr，exit 2 讓 harness 把 lint 錯誤餵回 Claude
  if ! ESLINT_OUT=$(cd "$PKG_DIR" && pnpm exec eslint "$ABS" 2>&1); then
    printf '%s\n' "$ESLINT_OUT" >&2
    LINT_EXIT=1
  fi

done < <(printf '%s\n' "$FILES")

[ "$LINT_EXIT" -ne 0 ] && exit 2
exit 0
