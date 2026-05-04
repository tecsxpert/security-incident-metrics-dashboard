package com.example.demo.security;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class JwtAuthFilterTest {

    private final JwtUtil jwtUtil = new JwtUtil();

    @Test
    void testValidToken() {
        String token = jwtUtil.generateToken("user", "USER");
        assertTrue(jwtUtil.validateToken(token));
        assertEquals("user", jwtUtil.extractUsername(token));
        assertEquals("USER", jwtUtil.extractRole(token));
    }

    @Test
    void testExpiredOrInvalidToken() {
        assertFalse(jwtUtil.validateToken("bad.token.here"));
    }
}
