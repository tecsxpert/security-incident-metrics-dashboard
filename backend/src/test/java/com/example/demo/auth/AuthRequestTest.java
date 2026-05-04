package com.example.demo.auth;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AuthRequestTest {

    @Test
    void testAuthRequest() {
        AuthRequest request = new AuthRequest();
        request.setUsername("admin");
        request.setPassword("admin123");

        assertEquals("admin", request.getUsername());
        assertEquals("admin123", request.getPassword());
    }
}
