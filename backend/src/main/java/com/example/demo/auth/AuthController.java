package com.example.demo.auth;

import com.example.demo.security.JwtUtil;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final JwtUtil jwtUtil;

    public AuthController(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody AuthRequest request) {

        // 🔥 SIMPLE DEMO LOGIN (replace with DB later if needed)
        String username = request.getUsername();
        String role = request.getUsername().equals("admin") ? "ADMIN" : "USER";

        String token = jwtUtil.generateToken(username, role);

        return ResponseEntity.ok(new AuthResponse(token, role));
    }

    // DTOs
    static class AuthRequest {
        private String username;
        private String password;

        public String getUsername() { return username; }
        public void setUsername(String username) { this.username = username; }

        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
    }

    static class AuthResponse {
        private String token;
        private String role;

        public AuthResponse(String token, String role) {
            this.token = token;
            this.role = role;
        }

        public String getToken() { return token; }
        public String getRole() { return role; }
    }
}
