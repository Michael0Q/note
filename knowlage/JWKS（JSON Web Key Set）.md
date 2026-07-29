[[JWS（JSON Web Signature）]]の署名に仕様した公開鍵の一覧。

レスポンス例
```json{
  "keys": [
    {
      "kid": "9e1a4f3b8c2d...",
      "kty": "RSA",
      "alg": "RS256",
      "use": "sig",
      "n": "wq3d8f...(超長いBase64URL文字列)...9Kw",
      "e": "AQAB"
    },
    {
      "kid": "3b7f2a91d0e5...",
      "kty": "RSA",
      "alg": "RS256",
      "use": "sig",
      "n": "zx7bA2...(別の鍵の値)...pQ2",
      "e": "AQAB"
    }
  ]
}
```

* kid
	JWTのヘッダーに書かれているkidと付き合わせて、そのJWTの公開鍵を見つける。
* kty
	鍵の種類
* alg
	暗号化アルゴリズムの種類
