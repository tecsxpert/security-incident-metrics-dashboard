package com.example.demo.security;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class JwtUtilTest {
    private final JwtUtil jwtUtil = new JwtUtil();

    @Test
    void testGenerateAndValidateToken() {
        String token = jwtUtil.generateToken("admin", "ADMIN");
        assertTrue(jwtUtil.validateToken(token));
    }

    @Test
    void testExtractUsername() {
        String token = jwtUtil.generateToken("admin", "ADMIN");
        assertEquals("admin", jwtUtil.extractUsername(token));
    }

    @Test
    void testExtractRole() {
        String token = jwtUtil.generateToken("admin", "ADMIN");
        assertEquals("ADMIN", jwtUtil.extractRole(token));
    }

    @Test
    void testInvalidToken() {
        assertFalse(jwtUtil.validateToken("invalid.token.here"));
    }
}
