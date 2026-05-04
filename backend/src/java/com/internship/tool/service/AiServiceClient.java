// backend/src/main/java/com/internship/tool/service/AiServiceClient.java

package com.internship.tool.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

@Service
public class AiServiceClient {

    private static final Logger logger =
        LoggerFactory.getLogger(AiServiceClient.class);

    private final RestTemplate restTemplate;

    @Value("${ai.service.base-url}")
    private String aiServiceBaseUrl;

    //Constructor — 10s timeout 
    public AiServiceClient(RestTemplateBuilder builder) {
        this.restTemplate = builder
            .connectTimeout(Duration.ofSeconds(10))
            .readTimeout(Duration.ofSeconds(10))
            .build();
    }

    //  Helper — build JSON headers 
    private HttpHeaders jsonHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        return headers;
    }

    // Helper — build request body 
    private Map<String, String> buildRequestBody(
        String title,
        String incidentType,
        String severity,
        String affectedSystem,
        String description
    ) {
        Map<String, String> body = new HashMap<>();
        body.put("title",           title);
        body.put("incident_type",   incidentType);
        body.put("severity",        severity);
        body.put("affected_system", affectedSystem);
        body.put("description",     description);
        return body;
    }

    //  Helper — execute POST call 
    private Map<String, Object> executePost(String url, Map<String, String> body) {
        try {
            HttpEntity<Map<String, String>> request =
                new HttpEntity<>(body, jsonHeaders());

            ResponseEntity<Map> response = restTemplate.exchange(
                url,
                HttpMethod.POST,
                request,
                Map.class
            );

            logger.info("AI call SUCCESS — url: {} status: {}", url, response.getStatusCode());
            return response.getBody();

        } catch (HttpClientErrorException e) {
            logger.error("AI client error — url: {} status: {} body: {}",
                url, e.getStatusCode(), e.getResponseBodyAsString());
            return null;

        } catch (HttpServerErrorException e) {
            logger.error("AI server error — url: {} status: {} body: {}",
                url, e.getStatusCode(), e.getResponseBodyAsString());
            return null;

        } catch (ResourceAccessException e) {
            logger.error("AI timeout/connection error — url: {} error: {}",
                url, e.getMessage());
            return null;

        } catch (Exception e) {
            logger.error("AI unexpected error — url: {} error: {}",
                url, e.getMessage());
            return null;
        }
    }

    //  POST /describe
    /**
     * Call Flask /describe endpoint.
     * Returns structured incident description from AI.
     * Returns null on any error.
     */
    public Map<String, Object> describe(
        String title,
        String incidentType,
        String severity,
        String affectedSystem,
        String description
    ) {
        logger.info("Calling AI /describe for incident: {}", title);
        String url = aiServiceBaseUrl + "/describe";
        Map<String, String> body = buildRequestBody(
            title, incidentType, severity, affectedSystem, description
        );
        return executePost(url, body);
    }

    // POST /recommend 
    /**
     * Call Flask /recommend endpoint.
     * Returns 3 recommendations as JSON array.
     * Returns null on any error.
     */
    public Map<String, Object> recommend(
        String title,
        String incidentType,
        String severity,
        String affectedSystem,
        String description
    ) {
        logger.info("Calling AI /recommend for incident: {}", title);
        String url = aiServiceBaseUrl + "/recommend";
        Map<String, String> body = buildRequestBody(
            title, incidentType, severity, affectedSystem, description
        );
        return executePost(url, body);
    }

    // POST /generate-report 
    /**
     * Call Flask /generate-report endpoint.
     * Returns full AI generated incident report.
     * Returns null on any error.
     */
    public Map<String, Object> generateReport(
        String title,
        String incidentType,
        String severity,
        String affectedSystem,
        String description
    ) {
        logger.info("Calling AI /generate-report for incident: {}", title);
        String url = aiServiceBaseUrl + "/generate-report";
        Map<String, String> body = buildRequestBody(
            title, incidentType, severity, affectedSystem, description
        );
        return executePost(url, body);
    }

    //  GET /health 
    /**
     * Check if Flask AI service is running.
     * Returns true if healthy, false on any error.
     */
    public boolean isHealthy() {
        String url = aiServiceBaseUrl + "/health";
        logger.info("Checking AI service health");

        try {
            ResponseEntity<Map> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                new HttpEntity<>(jsonHeaders()),
                Map.class
            );
            boolean healthy = response.getStatusCode() == HttpStatus.OK;
            logger.info("AI service health — healthy: {}", healthy);
            return healthy;

        } catch (Exception e) {
            logger.error("AI health check failed — {}", e.getMessage());
            return false;
        }
    }
}