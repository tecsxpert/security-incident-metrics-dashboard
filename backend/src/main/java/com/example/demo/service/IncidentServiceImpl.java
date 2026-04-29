package com.example.demo.service;

import com.example.demo.entity.Incident;
import com.example.demo.exception.ResourceNotFoundException;
import com.example.demo.repository.IncidentRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class IncidentServiceImpl implements IncidentService {

    private final IncidentRepository repository;

    public IncidentServiceImpl(IncidentRepository repository) {
        this.repository = repository;
    }

    @Override
    public Incident createIncident(Incident incident) {
        return repository.save(incident);
    }

    // ✅ FIXED (Pagination version for Day 4)
    @Override
    public Page<Incident> getAllIncidents(int page, int size) {
        return repository.findAll(PageRequest.of(page, size));
    }

    @Override
    public Incident getById(Long id) {
        return repository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Incident not found: " + id));
    }

    @Override
    public Incident update(Long id, Incident incident) {
        Incident existing = getById(id);

        existing.setTitle(incident.getTitle());
        existing.setDescription(incident.getDescription());
        existing.setSeverity(incident.getSeverity());
        existing.setStatus(incident.getStatus());

        return repository.save(existing);
    }

    @Override
    public void delete(Long id) {
        repository.delete(getById(id));
    }

    @Override
    public List<Incident> getByStatus(String status) {
        return repository.findByStatus(status);
    }

    @Override
    public List<Incident> getBySeverity(String severity) {
        return repository.findBySeverity(severity);
    }
}