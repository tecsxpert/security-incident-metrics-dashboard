package com.example.demo.service;

import com.example.demo.entity.Incident;

import java.util.List;

import org.springframework.data.domain.Page;

public interface IncidentService {

    Incident createIncident(Incident incident);

    Page<Incident> getAllIncidents(int page, int size);

    Incident getById(Long id);

    Incident update(Long id, Incident incident);

    void delete(Long id);

    List<Incident> getByStatus(String status);

    List<Incident> getBySeverity(String severity);
}