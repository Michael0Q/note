#!/bin/bash

# 1. GCS から条件に合うすべての PDF ファイルのリストを取得します

gcloud storage ls "gs://kaikoku-production/users/\*/pr-resume/\*\*.pdf" | \

# 2. awk を使い、「pr-resume」ディレクトリごとに「最初の 1 ファイル」だけを抽出します

awk -F'/' '
{ # パスを "/" で分割し、"pr-resume" が見つかるまで結合してディレクトリキーを作成します
dir_key = ""
for (i = 1; i <= NF; i++) {
dir_key = dir_key $i "/"
        # フィールドが "pr-resume" だったら、キーの作成を終了します
        if ($i == "pr-resume") {
break
}
}

    # このキーが初めて現れた場合のみ、ファイルパス全体を出力します
    # これにより、各 `pr-resume` ディレクトリから最初の1ファイルだけが選ばれます
    if (!seen[dir_key]++) {
        print $0
    }

}
' | \

# 3. ダウンロードする件数を 60 件に制限します

head -n 500 | \

# 4. xargs を使い、抽出されたファイルリストを gcloud storage cp に渡してダウンロードします

xargs -I {} gcloud storage cp "{}" ./datasets/

echo "🎉 All tasks completed."
