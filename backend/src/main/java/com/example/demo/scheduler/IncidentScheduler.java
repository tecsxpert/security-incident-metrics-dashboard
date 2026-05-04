package com.example.demo.scheduler;

import com.example.demo.repository.IncidentRepository;
import com.example.demo.service.EmailService;
import org.springframework.stereotype.Component;

@Component
public class IncidentScheduler {

    private final IncidentRepository repository;
    private final EmailService emailService;

    public IncidentScheduler(IncidentRepository repository, EmailService emailService) {
        this.repository = repository;
        this.emailService = emailService;
    }

    // ❌ TEMPORARILY DISABLED FOR TESTING (IMPORTANT)
    // @Scheduled(fixedRate = 60000)
    public void sendIncidentReport() {

        long count = repository.count();

        String message = "Daily Incident Report\nTotal Incidents: " + count;

        emailService.sendEmail(
                "cinthiyajenniefer@gmail.com",
                "Incident Report",
                message
        );

        System.out.println("Email scheduler disabled for testing");
    }
}
