ユーザーからのコマンドに応じて、指定したプロンプトをを元に処理を実行してください。

<if>make knowlage {ContextArg1}
<prompt>
表題またはコンテキストファイルの一番目のについて、権威のある一次ソースを元にファクトベースでナレッジを作成してください。
作成するファイルは ./knowlage とし、作成するファイルのジャンルに応じて、別途ディレクトリを作成するか、既存のディレクトリに配置してください。
</prompt>

<else if>fact check {ContextArg1}
対象のドキュメントについての事実確認を行なってください。ハルシネーションがないか確認してください。

<else if>test {ContextArg1}
コンテキストファイルの一番目のファイルの末尾にテストセクションを設け、そのナレッジの理解度を測るテスト問題を作成してください。

<else if>feedback test {ContextArg1}
ファイル末尾のテストセクションに記載されている回答の正誤を判定し、フィードバックを記載してください。
