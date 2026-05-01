package com.example.demo.service.impl;

import com.example.demo.entity.Incident;
import com.example.demo.repository.IncidentRepository;
import com.example.demo.service.EmailService;
import com.example.demo.service.IncidentService;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class IncidentServiceImpl implements IncidentService {

    private final IncidentRepository repository;
    private final EmailService emailService;

    // ✅ Constructor Injection
    public IncidentServiceImpl(IncidentRepository repository,
                               EmailService emailService) {
        this.repository = repository;
        this.emailService = emailService;
    }

    // =========================
    // GET ALL (CACHE ENABLED)
    // =========================
    @Override
    @Cacheable("incidents")
    public List<Incident> getAllIncidents() {
        return repository.findAll();
    }

    // =========================
    // CREATE + EMAIL ALERT
    // =========================
    @Override
    @CacheEvict(value = "incidents", allEntries = true)
    public Incident createIncident(Incident incident) {

        Incident saved = repository.save(incident);

        // 📧 EMAIL NOTIFICATION
        emailService.sendEmail(
                "cinthiyajenniefer@gmail.com",
                "🚨 New Incident Created",
                "Incident ID: " + saved.getId() +
                        "\nTitle: " + saved.getTitle() +
                        "\nSeverity: " + saved.getSeverity()
        );

        return saved;
    }

    // =========================
    // GET BY ID
    // =========================
    @Override
    public Incident getById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found"));
    }

    // =========================
    // UPDATE (CACHE CLEAR)
    // =========================
    @Override
    @CacheEvict(value = "incidents", allEntries = true)
    public Incident update(Long id, Incident incident) {

        Incident existing = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found"));

        if (incident.getTitle() != null)
            existing.setTitle(incident.getTitle());

        if (incident.getDescription() != null)
            existing.setDescription(incident.getDescription());

        if (incident.getSeverity() != null)
            existing.setSeverity(incident.getSeverity());

        if (incident.getStatus() != null)
            existing.setStatus(incident.getStatus());

        return repository.save(existing);
    }

    // =========================
    // DELETE (CACHE CLEAR)
    // =========================
    @Override
    @CacheEvict(value = "incidents", allEntries = true)
    public void delete(Long id) {

        if (!repository.existsById(id)) {
            throw new RuntimeException("Incident not found");
        }

        repository.deleteById(id);
    }
}
