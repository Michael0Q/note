#!/usr/bin/env python3
"""exam/問題/ 配下のノートの category が出題範囲表の小項目に一致するか検証する。

統計検定2級 出題範囲表（2018/12/14版）の小項目21個をホワイトリストとして持ち、
それ以外の名称が使われていたら異常として報告する。

背景: 2021年6月_問17 を作った際に範囲表にない「検定」という名称を使い、
続けて作った問18〜20がそれを踏襲して揺れが発生した（2026-09-12に修正）。
既存ノートの表記を参考にすると誤りが伝播するため、必ずこのスクリプトで検証する。

使い方:
    python3 exam/スクリプト/validate_category.py
    python3 exam/スクリプト/validate_category.py --list   # 小項目一覧を表示

終了コード: 0=すべて正常 / 1=違反あり
"""
import sys
import os
import re
import glob

# 統計検定2級 出題範囲表（2018/12/14版）の小項目。
# https://www.toukei-kentei.jp/hubfs/files/grade_range/grade2_hani_20181214.pdf
# 大項目ごとに、範囲表の掲載順で並べている。
SUBCATEGORIES = {
    "データソース": ["身近な統計"],
    "データの分布": ["データの分布の記述"],
    "1変数データ": ["中心傾向の指標", "散らばりなどの指標", "中心と散らばりの活用"],
    "2変数以上のデータ": ["散布図と相関", "カテゴリカルデータ"],
    "データの活用": ["単回帰と予測", "時系列データの処理"],
    "推測のためのデータ収集法": ["観察研究と実験研究", "標本調査と無作為抽出", "実験"],
    "確率モデルの導入": ["確率", "確率変数", "確率分布"],
    "推測": ["標本分布", "推定", "仮説検定"],
    "線形モデル": ["回帰分析", "実験計画の概念の理解"],
    "活用": ["統計ソフトウェアの活用"],
}

ALLOWED = [s for subs in SUBCATEGORIES.values() for s in subs]

# 過去に混入した誤りと、正しい名称の対応。見つけたら具体的に指摘する。
KNOWN_MISTAKES = {
    "検定": "仮説検定",
    "統計的検定": "仮説検定",
    "区間推定": "推定",
    "点推定": "推定",
    "相関": "散布図と相関",
    "分散分析": "実験計画の概念の理解",
}

EXAM_PREFIX = "統計検定2級/"
NOTE_DIR = "exam/問題"


def read_category(path):
    """frontmatter から category の値を取り出す。無ければ None。"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    front = text[3:end] if end != -1 else text
    m = re.search(r"^category:\s*(.*)$", front, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'")


def main():
    if "--list" in sys.argv:
        for major, subs in SUBCATEGORIES.items():
            print(f"[{major}]")
            for s in subs:
                print(f"  - {s}")
        return 0

    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    paths = sorted(glob.glob(os.path.join(root, NOTE_DIR, "*.md")))
    if not paths:
        print(f"問題ノートが見つかりません: {os.path.join(root, NOTE_DIR)}")
        return 1

    violations = []
    counts = {}
    for p in paths:
        name = os.path.basename(p)
        cat = read_category(p)
        if cat is None or cat == "":
            violations.append((name, cat, "category が空、または frontmatter に存在しない"))
            continue
        if not cat.startswith(EXAM_PREFIX):
            violations.append((name, cat, f"'{EXAM_PREFIX}<小項目>' の形式になっていない"))
            continue
        sub = cat[len(EXAM_PREFIX):]
        counts[sub] = counts.get(sub, 0) + 1
        if sub not in ALLOWED:
            hint = KNOWN_MISTAKES.get(sub)
            msg = f"出題範囲表にない小項目。正しくは '{hint}'" if hint else "出題範囲表にない小項目"
            violations.append((name, cat, msg))

    print(f"検査対象: {len(paths)} 件")
    if violations:
        print(f"\n違反 {len(violations)} 件:")
        for name, cat, msg in violations:
            print(f"  - {name}")
            print(f"      category: {cat}")
            print(f"      {msg}")
        print("\n出題範囲表の小項目一覧は --list で確認できます。")
        return 1

    print("違反なし。すべて出題範囲表の小項目に一致しています。\n")
    print("分野別の件数:")
    for sub in ALLOWED:
        if sub in counts:
            print(f"  {counts[sub]:3d}  {sub}")
    unused = [s for s in ALLOWED if s not in counts]
    if unused:
        print(f"\n未使用の小項目: {' / '.join(unused)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
