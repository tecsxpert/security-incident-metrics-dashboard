package com.example.demo.auth;

import com.example.demo.security.JwtUtil;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final JwtUtil jwtUtil;

    public AuthController(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

   @PostMapping("/login")
public String login(@RequestBody AuthRequest request) {

    String username = request.getUsername();
    String password = request.getPassword();

    // your existing validation logic
    if (username.equals("admin") && password.equals("admin")) {
        return jwtUtil.generateToken(username);
    }

    throw new RuntimeException("Invalid credentials");
}

    @PostMapping("/register")
    public String register() {
        return "User registered (mock)";
    }
}