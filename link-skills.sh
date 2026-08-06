#!/usr/bin/env bash
# 把 .claude/skills 的內容搬到 .agents/skills，再把 .claude/skills 換成指向它的 symlink。
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

SRC=".claude/skills"
DST=".agents/skills"

if [ -L "$SRC" ]; then
  echo "$SRC 已經是 symlink 了，什麼都不用做。"
  exit 0
fi

if [ ! -d "$SRC" ]; then
  echo "找不到 $SRC，中止。"
  exit 1
fi

mkdir -p "$DST"

# 清掉系統自動產生的垃圾檔
find "$DST" -name ".DS_Store" -delete

shopt -s dotglob nullglob
for item in "$SRC"/*; do
  name="$(basename "$item")"

  # .DS_Store 直接丟掉
  if [ "$name" = ".DS_Store" ]; then
    rm -f "$item"
    continue
  fi

  # 空資料夾直接丟掉（例如意外產生的雜物）
  if [ -d "$item" ] && [ -z "$(find "$item" -mindepth 1 -print -quit)" ]; then
    echo "跳過並刪除空資料夾：$item"
    rm -rf "$item"
    continue
  fi

  if [ -e "$DST/$name" ]; then
    echo "錯誤：$DST/$name 已經存在，不確定該怎麼合併，中止。請自行處理後再跑一次。"
    exit 1
  fi

  if git ls-files --error-unmatch "$item" >/dev/null 2>&1; then
    git mv "$item" "$DST/$name"
  else
    mv "$item" "$DST/$name"
  fi
  echo "搬移完成：$item -> $DST/$name"
done
shopt -u dotglob nullglob

remaining="$(find "$SRC" -mindepth 1 -print -quit)"
if [ -n "$remaining" ]; then
  echo "$SRC 裡還有東西沒搬走，先停下來，你自己看一下："
  find "$SRC" -mindepth 1
  exit 1
fi

rmdir "$SRC"
ln -s "../$DST" "$SRC"

echo "完成。$SRC 現在是指向 $DST 的 symlink。"
ls -la "$SRC"
