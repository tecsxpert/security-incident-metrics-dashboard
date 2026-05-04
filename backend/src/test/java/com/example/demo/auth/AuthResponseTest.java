package com.example.demo.auth;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AuthResponseTest {

    @Test
    void testAuthResponse() {
        AuthResponse response = new AuthResponse("token123", "ADMIN");
        assertEquals("token123", response.getToken());
        assertEquals("ADMIN", response.getRole());

        response.setToken("newtoken");
        response.setRole("USER");
        assertEquals("newtoken", response.getToken());
        assertEquals("USER", response.getRole());
    }
}
