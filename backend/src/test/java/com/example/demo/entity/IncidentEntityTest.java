package com.example.demo.entity;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class IncidentEntityTest {
    @Test
    void testIncidentGettersSetters() {
        Incident incident = new Incident();
        incident.setId(1L);
        incident.setTitle("Test");
        incident.setDescription("Desc");
        incident.setSeverity("HIGH");
        incident.setStatus("OPEN");

        assertEquals(1L, incident.getId());
        assertEquals("Test", incident.getTitle());
        assertEquals("Desc", incident.getDescription());
        assertEquals("HIGH", incident.getSeverity());
        assertEquals("OPEN", incident.getStatus());
    }
}
