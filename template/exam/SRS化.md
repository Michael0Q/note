<%*
// 既存ノート（knowlage等）をその場でSRS対象にするテンプレート。
// ファイルは移動しない。frontmatterにSRSフィールドを追記し、
// カーソル位置に ○/△/× ボタンを挿入する。
// 使い方: SRS化したいノートを開き、ボタンを置きたい位置にカーソルを置いて
// 「Templater: Open insert template modal」→ SRS化 を選ぶ。

// 既存の #problem ノート全体から分野を収集して選択式で入力
const catSet = new Set();
for (const f of app.vault.getMarkdownFiles()) {
	const fm = app.metadataCache.getFileCache(f)?.frontmatter;
	if (!fm) continue;
	if (![].concat(fm.tags ?? []).includes("problem")) continue;
	if (fm.category) catSet.add(String(fm.category));
}
const cats = [...catSet].sort((a, b) => a.localeCompare(b, "ja"));
const NEW_CAT = "＋ 新規入力…";
let category = "";
if (cats.length > 0) {
	const picked = await tp.system.suggester(
		[...cats, NEW_CAT],
		[...cats, NEW_CAT],
		false,
		"分野を選択（入力で絞り込み）"
	);
	if (picked === NEW_CAT) {
		category = (await tp.system.prompt("分野（例: 統計/確率）")) ?? "";
	} else {
		category = picked ?? "";
	}
} else {
	category = (await tp.system.prompt("分野（例: 統計/確率）")) ?? "";
}

// 既存frontmatterを壊さないよう、無いフィールドだけ補う
const target = tp.config.target_file;
await app.fileManager.processFrontMatter(target, (f) => {
	const tags = [].concat(f.tags ?? []);
	if (!tags.includes("problem")) tags.push("problem");
	f.tags = tags;
	if (!Number.isFinite(Number(f.level))) f.level = 0;
	if (!f.last) f.last = tp.date.now("YYYY-MM-DD");
	if (f.status === undefined || f.status === null) f.status = "";
	if (f.retired !== true) f.retired = false;
	if (category) f.category = category;
});
-%>
```meta-bind-button
id: srs-o
class: srs-btn-o
hidden: true
label: "○ 正解＋説明できた"
style: primary
action:
  type: js
  file: exam/スクリプト/review.js
  args:
    grade: "○"
```

```meta-bind-button
id: srs-tri
class: srs-btn-tri
hidden: true
label: "△ 正解したが説明できない"
style: default
action:
  type: js
  file: exam/スクリプト/review.js
  args:
    grade: "△"
```

```meta-bind-button
id: srs-x
class: srs-btn-x
hidden: true
label: "× 不正解"
style: destructive
action:
  type: js
  file: exam/スクリプト/review.js
  args:
    grade: "×"
```

`BUTTON[srs-o]` `BUTTON[srs-tri]` `BUTTON[srs-x]`
