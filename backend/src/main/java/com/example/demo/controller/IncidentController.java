package com.example.demo.controller;

import com.example.demo.entity.Incident;
import com.example.demo.service.IncidentService;

import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/incidents")
public class IncidentController {

    private final IncidentService incidentService;

    public IncidentController(IncidentService incidentService) {
        this.incidentService = incidentService;
    }

    // ✅ CREATE (ADMIN ONLY)
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Incident> create(@RequestBody Incident incident) {
        return ResponseEntity.ok(incidentService.createIncident(incident));
    }

    // ✅ GET ALL (ADMIN + USER)
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN','USER')")
    public ResponseEntity<List<Incident>> getAll() {
        return ResponseEntity.ok(incidentService.getAllIncidents());
    }

    // ✅ GET BY ID
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','USER')")
    public ResponseEntity<Incident> getById(@PathVariable Long id) {
        return ResponseEntity.ok(incidentService.getById(id));
    }
    


    // ✅ UPDATE (FIXED)
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Incident> update(
            @PathVariable Long id,
            @RequestBody Incident incident) {

        return ResponseEntity.ok(incidentService.update(id, incident));
    }

    // ✅ DELETE
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<String> delete(@PathVariable Long id) {
        incidentService.delete(id);
        return ResponseEntity.ok("Deleted successfully");
    }
}
