# lint.sh

改自 super-dsp-2.0 的 `lint-and-format.sh`。差在兩件事：

1. eslint 拿掉 `--fix`，只報錯，不改檔案。
2. prettier 整段拿掉。

理由：hook 改寫檔案，harness 就會把整份新檔重新塞回對話，一次可能上千行。只報不改，就不會觸發重貼。

格式化改由 git pre-commit 負責。目標專案要裝 husky 加 lint-staged，commit 時對暫存的檔案跑 `prettier --write`。專案沒裝的話，`ito-implement-v3` skill 會在 commit 前自己跑一次 formatter。

## settings.json 要加的片段

放進目標專案的 `.claude/settings.json`：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/scripts/hooks/lint.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```
