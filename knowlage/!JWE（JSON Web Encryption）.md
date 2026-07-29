[[JWT（JSON Web Token）]]を暗号化し、安全に運ぶための規格。[[JWS（JSON Web Signature）]]が改竄を検知する仕組みだったのに対し、こちらはそもそも内容を読ませないためのもの。

### 構成

```
①...BASE64URL(UTF8(JWE Protected Header)) || '.' ||   
②...BASE64URL(JWE Encrypted Key) || '.' ||
③...BASE64URL(JWE Initialization Vector) || '.' ||
④...BASE64URL(JWE Ciphertext) || '.' ||
⑤...BASE64URL(JWE Authentication Tag)
```

①JWEヘッダー
JWSと同様、暗号化に仕様するアルゴリズムを記載する。JWTと違うのは、2段構えの暗号化になっている点。
```json
{
  "alg": "RSA-OAEP", <- コンテンツ全体を暗号化するアルゴリズム
  "enc": "A256GCM"　<- JWTを暗号化するアルゴリズム
}
```

