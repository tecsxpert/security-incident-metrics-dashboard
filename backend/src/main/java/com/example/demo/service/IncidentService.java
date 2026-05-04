package com.example.demo.service;

import com.example.demo.entity.Incident;
import java.util.List;

public interface IncidentService {

    List<Incident> getAllIncidents();

    Incident createIncident(Incident incident);

    Incident getById(Long id);

    Incident update(Long id, Incident incident);

    void delete(Long id);
}
