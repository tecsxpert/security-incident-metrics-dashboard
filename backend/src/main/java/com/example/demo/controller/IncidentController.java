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

    // ✅ SEARCH
    @GetMapping("/search")
    @PreAuthorize("hasAnyRole('ADMIN','USER')")
    public ResponseEntity<List<Incident>> search(@RequestParam("q") String query) {
        return ResponseEntity.ok(incidentService.search(query));
    }

    // ✅ EXPORT CSV
    @GetMapping("/export")
    @PreAuthorize("hasAnyRole('ADMIN','USER')")
    public ResponseEntity<String> exportCsv() {
        List<Incident> incidents = incidentService.getAllIncidents();
        StringBuilder csv = new StringBuilder("ID,Title,Severity,Status\n");
        for (Incident i : incidents) {
            csv.append(i.getId()).append(",")
               .append(i.getTitle() != null ? i.getTitle().replace(",", " ") : "").append(",")
               .append(i.getSeverity()).append(",")
               .append(i.getStatus()).append("\n");
        }
        return ResponseEntity.ok()
                .header("Content-Disposition", "attachment; filename=\"incidents.csv\"")
                .body(csv.toString());
    }

    // ✅ UPLOAD CSV
    @PostMapping("/upload")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<String> uploadCsv(@RequestParam("file") org.springframework.web.multipart.MultipartFile file) {
        if (file.isEmpty() || file.getOriginalFilename() == null || !file.getOriginalFilename().endsWith(".csv")) {
            return ResponseEntity.badRequest().body("Invalid file type. Please upload a CSV.");
        }
        if (file.getSize() > 5 * 1024 * 1024) {
            return ResponseEntity.badRequest().body("File size exceeds 5MB.");
        }
        return ResponseEntity.ok("File uploaded successfully.");
    }
}
