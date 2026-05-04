package com.example.demo.config;

import com.example.demo.entity.Incident;
import com.example.demo.repository.IncidentRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Component
public class DataSeeder implements CommandLineRunner {

    private final IncidentRepository incidentRepository;

    public DataSeeder(IncidentRepository incidentRepository) {
        this.incidentRepository = incidentRepository;
    }

    @Override
    public void run(String... args) throws Exception {

        if (incidentRepository.count() >= 30) {
            System.out.println("Data already seeded. Skipping...");
            return;
        }

        List<Incident> incidents = new ArrayList<>();

        String[][] data = {
            {"Server Down", "Production server not responding", "HIGH", "OPEN"},
            {"DB Connection Failed", "Database connection timeout", "CRITICAL", "OPEN"},
            {"Memory Leak", "Application memory usage high", "HIGH", "IN_PROGRESS"},
            {"API Gateway Error", "API gateway returning 502", "HIGH", "OPEN"},
            {"SSL Certificate Expired", "SSL cert expired on prod", "CRITICAL", "RESOLVED"},
            {"Slow Query", "DB query taking too long", "MEDIUM", "OPEN"},
            {"Disk Space Low", "Server disk usage at 95%", "HIGH", "IN_PROGRESS"},
            {"Login Service Down", "Users unable to login", "CRITICAL", "OPEN"},
            {"Email Service Failing", "Emails not being sent", "MEDIUM", "OPEN"},
            {"Cache Miss Rate High", "Redis cache miss rate above 80%", "MEDIUM", "OPEN"},
            {"Load Balancer Issue", "Load balancer not distributing traffic", "HIGH", "RESOLVED"},
            {"Backup Failed", "Nightly backup job failed", "HIGH", "OPEN"},
            {"Security Breach", "Unauthorized access detected", "CRITICAL", "IN_PROGRESS"},
            {"Network Latency", "High network latency detected", "MEDIUM", "OPEN"},
            {"Service Crash", "Payment service crashed", "CRITICAL", "OPEN"},
            {"Config Error", "Wrong config deployed to prod", "HIGH", "RESOLVED"},
            {"Timeout Error", "Request timeout on checkout", "MEDIUM", "OPEN"},
            {"CPU Spike", "CPU usage at 100%", "HIGH", "IN_PROGRESS"},
            {"Log Service Down", "Logging service not working", "LOW", "OPEN"},
            {"DNS Resolution Failed", "DNS lookup failing", "HIGH", "OPEN"},
            {"Auth Token Expired", "JWT tokens expiring too fast", "MEDIUM", "RESOLVED"},
            {"File Upload Failed", "File upload service down", "MEDIUM", "OPEN"},
            {"Notification Delay", "Push notifications delayed", "LOW", "OPEN"},
            {"Search Service Down", "Elasticsearch not responding", "HIGH", "OPEN"},
            {"Report Generation Failed", "PDF reports not generating", "MEDIUM", "IN_PROGRESS"},
            {"Third Party API Down", "Payment gateway API down", "CRITICAL", "OPEN"},
            {"Data Sync Failed", "Data sync between services failed", "HIGH", "OPEN"},
            {"Queue Overflow", "Message queue at capacity", "HIGH", "IN_PROGRESS"},
            {"Rate Limit Exceeded", "API rate limit exceeded", "MEDIUM", "OPEN"},
            {"Deployment Failed", "Latest deployment failed on prod", "CRITICAL", "OPEN"}
        };

        for (String[] d : data) {
            Incident incident = new Incident();
            incident.setTitle(d[0]);
            incident.setDescription(d[1]);
            incident.setSeverity(d[2]);
            incident.setStatus(d[3]);
            incident.setCreatedAt(LocalDateTime.now());
            incident.setUpdatedAt(LocalDateTime.now());
            incidents.add(incident);
        }

        incidentRepository.saveAll(incidents);
        System.out.println("✅ 30 incidents seeded successfully!");
    }
}
