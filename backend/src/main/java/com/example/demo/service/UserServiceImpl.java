package com.example.demo.service.impl;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class UserServiceImpl {

    // SIMPLE IN-MEMORY USERS (for capstone project)
    private static final Map<String, String> USERS = new HashMap<>();

    static {
        USERS.put("admin", "admin123");
        USERS.put("user", "user123");
    }

    // Validate user credentials
    public boolean validateUser(String username, String password) {
        return USERS.containsKey(username)
                && USERS.get(username).equals(password);
    }

    // Get role based on username
    public String getRole(String username) {
        if ("admin".equals(username)) {
            return "ROLE_ADMIN";
        } else if ("user".equals(username)) {
            return "ROLE_USER";
        }
        return null;
    }
}
