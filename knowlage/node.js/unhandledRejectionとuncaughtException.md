# unhandledRejection vs. uncaughtException in Node.js

Node.jsでは、`unhandledRejection`と`uncaughtException`はプロセスレベルでエラーを通知するイベントですが、それぞれ異なるコード領域（非同期と同期）から発生します。

## `uncaughtException`

`uncaughtException`イベントは、JavaScriptの例外が`try...catch`ブロックでキャッチされずにイベントループまで到達したときに発生します。これは通常、**同期的なコード**で発生します。

**例:**
```javascript
// 'uncaughtException'イベントがトリガーされます
throw new Error('これは同期的なエラーです');
```

デフォルトでは、Node.jsはスタックトレースを`stderr`に出力し、終了コード1でプロセスを終了します。このイベントをリッスンして、シャットダウン前に同期的なクリーンアップ処理を行うことはできますが、アプリケーションが未定義の状態になるため、**通常の運用を再開することは推奨されません。**

## `unhandledRejection`

`unhandledRejection`イベントは、`Promise`が拒否(reject)され、イベントループの1ターン内に`.catch()`ブロックなどのエラーハンドラがアタッチされなかった場合に発生します。これは**非同期的なPromiseベースのコード**に特有です。

**例:**
```javascript
Promise.reject(new Error('これはPromiseの拒否です'));

// またはasync関数内で:
async function someAsyncFunc() {
  throw new Error('async関数内のエラー');
}
someAsyncFunc(); // .catch()で処理されない場合
```

これらのケースでは、拒否されたPromiseを処理する`.catch()`ハンドラがない場合、`unhandledRejection`イベントが発生します。

## 主な違い

| 特徴 | `uncaughtException` | `unhandledRejection` |
| :--- | :--- | :--- |
| **発生源** | 同期コード。エラーがスローされたが`try...catch`でキャッチされなかった場合。 | 非同期の`Promise`ベースのコード。Promiseが拒否されたが`.catch()`などで処理されなかった場合。 |
| **デフォルトの動作** | スタックトレースを出力し、プロセスを終了コード1で終了させる。 | Node.js v15以降では、未処理の拒否は`uncaughtException`のように扱われ、デフォルトでプロセスがクラッシュする。古いバージョンでは警告が出力されるだけだった。 |
| **イベントリスナー** | `process.on('uncaughtException', (err) => { ... });` | `process.on('unhandledRejection', (reason, promise) => { ... });` |

## 対処法

`process`オブジェクトにリスナーをアタッチすることで、これらのイベントをグローバルに処理できます。

```javascript
process.on('uncaughtException', (err) => {
  console.error('キャッチされなかった例外:', err);
  // 同期的なクリーンアップ処理を行い、終了することが推奨される
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('未処理のPromise拒否:', promise, '理由:', reason);
  // アプリケーション固有のロギングやエラー処理など
  // 例: 再スローしてuncaughtExceptionに変換する
  // throw reason;
});
```

**重要な注意点:** `uncaughtException`が発生した後にアプリケーションの実行を継続しようとすることは、アプリケーションの状態が信頼できなくなるため**非常に危険**です。推奨されるプラクティスは、エラーを記録し、正常にシャットダウンすることです。
