// 問題ノートの ○/△/× ボタンから Meta Bind (js action) 経由で実行されるスクリプト。
// 実行には JS Engine プラグインが必要。
//
// 遷移ルール:
//   ○: level +2（上限8）。level>=7 からの○なら retired: true（卒業）
//   △: level +1（上限8）
//   ×: level 据え置き。ダッシュボード側で「期限 = last + 1日」に上書きされ翌日必ず出る
//   ×状態からの ○/△: level -1 の位置に戻して再開（△の +1 と相殺して据え置きに
//   ならないよう、直前status="×" のときだけ特別扱いする）
//
// 日付は window.moment()（ローカルタイムゾーン）で YYYY-MM-DD 文字列を生成し、
// frontmatter には常に日付のみを保存する（時刻・UTC起因のズレを避けるため）。

const LADDER = [1, 2, 3, 5, 8, 13, 21, 34, 55];
const LADDER_MAX = LADDER.length - 1; // 8

const grade = context?.args?.grade;
if (!["○", "△", "×"].includes(grade)) {
	new obsidian.Notice("review.js: grade引数が不正です（Meta Bindのargsを確認）: " + grade);
	return;
}

// Meta Bind (js action) は JS Engine 経由で「ボタンが置かれているノート」を
// context.file として渡してくる。ホバープレビュー内ではアクティブファイルが
// プレビュー中のノートと一致しないため、context.file を優先する。
const file = context?.file ?? app.workspace.getActiveFile();
if (!file) {
	new obsidian.Notice("review.js: 対象ファイルを特定できません");
	return;
}

const fm = app.metadataCache.getFileCache(file)?.frontmatter ?? {};
const tags = [].concat(fm.tags ?? []);
if (!tags.includes("problem")) {
	new obsidian.Notice("review.js: #problem のノートではないため何もしません");
	return;
}

const today = window.moment().format("YYYY-MM-DD");
const prevStatus = String(fm.status ?? "");
let level = Number(fm.level);
if (!Number.isFinite(level)) level = 0;
level = Math.min(Math.max(level, 0), LADDER_MAX);
let retired = fm.retired === true;

if (grade === "×") {
	// levelは据え置き。期限計算はダッシュボード側で「翌日」に上書きされる
} else if (prevStatus === "×") {
	// ×からの復帰は ○/△ どちらでも「1段戻して再開」
	level = Math.max(0, level - 1);
} else if (grade === "○") {
	if (level >= 7) retired = true; // 34日以上の間隔を○で通過 → 卒業
	level = Math.min(LADDER_MAX, level + 2);
} else if (grade === "△") {
	level = Math.min(LADDER_MAX, level + 1);
}

await app.fileManager.processFrontMatter(file, (f) => {
	f.level = level;
	f.last = today;
	f.status = grade;
	f.retired = retired;
});

// 「## 復習ログ」はテンプレート上で最終セクションなので、ファイル末尾への追記で
// 時系列順のログになる
const logLine = `- ${today}: ${grade}`;
await app.vault.process(file, (content) => {
	const trimmed = content.replace(/\s+$/, "");
	if (trimmed.includes("## 復習ログ")) {
		return trimmed + "\n" + logLine + "\n";
	}
	return trimmed + "\n\n## 復習ログ\n" + logLine + "\n";
});

if (retired) {
	new obsidian.Notice(`🎓 卒業！ ${file.basename}`);
} else if (grade === "×") {
	new obsidian.Notice(`× 記録: level ${level} のまま、明日もう一度出ます`);
} else {
	const next = window.moment().add(LADDER[level], "days").format("YYYY-MM-DD");
	new obsidian.Notice(`${grade} 記録: level ${level} / 次回 ${next}`);
}
