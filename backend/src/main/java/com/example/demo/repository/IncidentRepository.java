package com.example.demo.repository;

import com.example.demo.entity.Incident;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface IncidentRepository extends JpaRepository<Incident, Long> {

    List<Incident> findByStatus(String status);

    List<Incident> findBySeverity(String severity);
}