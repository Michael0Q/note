[[JWT（JSON Web Token）]]を特定の暗号化アルゴリズムと秘密鍵で署名した文字列の総称。JOSEという認証規格で使われる。

フォーマットは下記のように「.」で連結した３つの文字列からなる。
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJleHAiOjE3ODc3MzA0MTksInN1YiI6InQubWl5YXphdG9AYmxhbS5jby5qcCIsInJvbGUiOjJ9.
Sj30M-plDZbaBiGKIKrhwSmcI-y7b0m_IQX-nBZlMDQ
```

1段目「eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.」をBASE64デコードすると、下記になり、ハッシュ化アルゴリズム「alg」と、トークンのタイプ「typ」からなるJSONであることがわかる。つまりJWT

これを、ヘッダーという。
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

2段目「eyJleHAiOjE3ODc3MzA0MTksInN1YiI6InQubWl5YXphdG9AYmxhbS5jby5qcCIsInJvbGUiOjJ9」をBASE64デコードすると、下記になり、exp、subはJWT規格で予約されたクレームで、expは期限のタイムスタンプ、subはユーザーIDなどの主体を表す。
roleは任意に追加したフィールドで、好きなフィールドを含めることができるのが特徴である。復元可能なので、パスワードなどは含めてはならない。

これを、ペイロードという。
```json
{
  "exp": 1787730419,
  "sub": "t.miyazato@blam.co.jp",
  "role": 2
}
```

3段目「Sj30M-plDZbaBiGKIKrhwSmcI-y7b0m_IQX-nBZlMDQ」は前述のヘッダーとペイロードをBASE64エンコードして「.」で結合した文字列を、ヘッダのアルゴリズム（alg）と秘密鍵で署名したもの。