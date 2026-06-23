package com.jyx.config;

import com.alibaba.fastjson2.JSON;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.UUID;

@Component
public class JwtConfig {
    // 有效期
    private static final long JWT_EXPIRE = 60 * 180 * 1000L; // 1小时
    // 密钥（需为 Base64 编码字符串）
    private static final String JWT_KEY = "y3aX2K8/4TdF6zBmQv7hPwScN9jLgRtA+UoWxEiYlDn5fMpGqHtJkKuV"; // 示例密钥，需替换

    public String createToken(Object data) {
        return Jwts.builder()
                .id(UUID.randomUUID().toString())
                .subject(JSON.toJSONString(data))
                .issuer("system")
                .issuedAt(new Date(System.currentTimeMillis()))
                .expiration(new Date(System.currentTimeMillis() + JWT_EXPIRE))
                .signWith(getSigningKey(), Jwts.SIG.HS256) // 使用新版签名方法
                .compact();
    }

    private SecretKey getSigningKey() {
        byte[] keyBytes = Decoders.BASE64.decode(JWT_KEY); // 解码 Base64 密钥
        return Keys.hmacShaKeyFor(keyBytes); // 生成 HMAC-SHA 密钥
    }

    public Claims parseToken(String token) {
        return Jwts.parser()
                .verifyWith(getSigningKey()) // 验证密钥
                .build()
                .parseSignedClaims(token)   // 替换旧版 parseClaimsJws
                .getPayload();
    }

    public <T> T parseToken(String token, Class<T> clazz) {
        Claims claims = parseToken(token);
        return JSON.parseObject(claims.getSubject(), clazz);
    }
}
