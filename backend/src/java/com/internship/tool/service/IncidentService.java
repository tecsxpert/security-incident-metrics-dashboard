package com.internship.tool.service;

import com.internship.tool.entity.Incident;
import com.internship.tool.repository.IncidentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class IncidentService {

    private static final Logger logger = LoggerFactory.getLogger(IncidentService.class);

    private final IncidentRepository incidentRepository;
    private final AiServiceClient    aiServiceClient;

    public IncidentService(IncidentRepository incidentRepository,
                           AiServiceClient aiServiceClient) {
        this.incidentRepository = incidentRepository;
        this.aiServiceClient    = aiServiceClient;
    }

    // Create incident then call AI async
    public Incident createIncident(Incident incident) {
        Incident saved = incidentRepository.save(incident);
        enrichWithAiAsync(saved);
        return saved;
    }

    // Call AI asynchronously — does not block response
    @Async
    public void enrichWithAiAsync(Incident incident) {
        logger.info("Async AI enrichment started — incident id: {}", incident.getId());

        try {
            Map<String, Object> aiResult = aiServiceClient.describe(
                incident.getTitle(),
                incident.getIncidentType(),
                incident.getSeverity(),
                incident.getAffectedSystem(),
                incident.getDescription()
            );

            if (aiResult == null) {
                logger.warn("AI returned null for incident id: {} — skipping enrichment", incident.getId());
                return;
            }

            // Attach AI result to incident
            Object data = aiResult.get("data");
            if (data != null) {
                incident.setAiDescription(data.toString());
                incidentRepository.save(incident);
                logger.info("AI enrichment complete — incident id: {}", incident.getId());
            }

        } catch (Exception e) {
            // Never crash — AI failure must not affect core incident creation
            logger.error("AI enrichment failed — incident id: {} error: {}",
                incident.getId(), e.getMessage());
        }
    }
}