package com.example.demo.controller;

import com.example.demo.service.EmailService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/mail")
public class MailController {

    private final EmailService emailService;

    public MailController(EmailService emailService) {
        this.emailService = emailService;
    }

    @GetMapping("/test")
    public String sendTestMail() {
        emailService.sendEmail(
                "cinthiyajenniefer@gmail.com", // ✅ your email here
                "Test Mail",
                "Hello from Spring Boot "
        );
        return "Email sent!";
    }
}
