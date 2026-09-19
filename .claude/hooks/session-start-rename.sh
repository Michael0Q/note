#!/bin/bash
# SessionStart hook: セッション冒頭でユーザーが指定する試験回・問番号から
# 即座にセッションタイトルを付けさせるためのルールを文脈に注入する。
# 詳細な書式は .claude/skills/rename-session/SKILL.md 側が持つ。
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
cat >/dev/null 2>&1 || true

read -r -d '' CTX <<'EOF' || true
このvaultのセッションでは、ユーザーの最初のメッセージに解きたい問題の試験回と問番号が含まれていることが多い（例:「202106 Q14」「2021-06のQ14 解いて」「2019年11月の問3」）。
その場合は解説に取りかかる前に、まず rename-session スキルを実行してセッションタイトルを YYYYMMQn 形式（例: 202106Q14）にすること。ユーザーの指示を待たない。
試験回・問番号が読み取れないメッセージ（雑談・タスク管理・vault編集など）のときは何もしない。
EOF

jq -n --arg ctx "$CTX" \
	'{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$ctx}}'
