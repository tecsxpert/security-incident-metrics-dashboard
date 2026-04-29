package com.example.demo.controller;

import com.example.demo.entity.Incident;
import com.example.demo.service.IncidentService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import org.springframework.data.domain.Page;

@RestController
@RequestMapping("/api/incidents")
public class IncidentController {

    private final IncidentService incidentService;

    public IncidentController(IncidentService incidentService) {
        this.incidentService = incidentService;
    }

    // ✅ GET ALL (PAGINATION)
    @GetMapping("/all")
    public ResponseEntity<Page<Incident>> getAll(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "5") int size) {

        return ResponseEntity.ok(
                incidentService.getAllIncidents(page, size)
        );
    }

    // ✅ GET BY ID (404 handled in service)
    @GetMapping("/{id}")
    public ResponseEntity<Incident> getById(@PathVariable Long id) {
        return ResponseEntity.ok(incidentService.getById(id));
    }

    // ✅ CREATE
    @PostMapping("/create")
    public ResponseEntity<Incident> create(@Valid @RequestBody Incident incident) {
        Incident created = incidentService.createIncident(incident);
        return new ResponseEntity<>(created, HttpStatus.CREATED);
    }

    // ✅ UPDATE
    @PutMapping("/{id}")
    public ResponseEntity<Incident> update(
            @PathVariable Long id,
            @Valid @RequestBody Incident incident) {

        return ResponseEntity.ok(
                incidentService.update(id, incident)
        );
    }

    // ✅ DELETE
    @DeleteMapping("/{id}")
    public ResponseEntity<String> delete(@PathVariable Long id) {
        incidentService.delete(id);
        return ResponseEntity.ok("Deleted successfully");
    }
}