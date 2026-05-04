package com.example.demo.entity;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class UserEntityTest {

    @Test
    void testUserGettersSetters() {
        User user = new User();
        user.setId(1L);
        user.setUsername("admin");
        user.setPassword("admin123");
        user.setRole("ADMIN");

        assertEquals(1L, user.getId());
        assertEquals("admin", user.getUsername());
        assertEquals("admin123", user.getPassword());
        assertEquals("ROLE_ADMIN", user.getRole());
    }

    @Test
    void testUserConstructor() {
        User user = new User("admin", "admin123", "ADMIN");
        assertEquals("admin", user.getUsername());
        assertEquals("ADMIN", user.getRole());
    }
}
