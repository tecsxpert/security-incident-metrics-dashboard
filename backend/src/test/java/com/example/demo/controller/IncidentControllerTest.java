package com.example.demo.controller;

import com.example.demo.entity.Incident;
import com.example.demo.service.IncidentService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.ResponseEntity;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class IncidentControllerTest {

    @Mock
    private IncidentService incidentService;

    @InjectMocks
    private IncidentController incidentController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetAll() {
        Incident i = new Incident();
        i.setId(1L);
        i.setTitle("Test");
        i.setSeverity("HIGH");
        i.setStatus("OPEN");
        when(incidentService.getAllIncidents()).thenReturn(List.of(i));

        ResponseEntity<List<Incident>> response = incidentController.getAll();
        assertEquals(200, response.getStatusCode().value());
        assertEquals(1, response.getBody().size());
    }

    @Test
    void testGetById() {
        Incident i = new Incident();
        i.setId(1L);
        i.setTitle("Test");
        when(incidentService.getById(1L)).thenReturn(i);

        ResponseEntity<Incident> response = incidentController.getById(1L);
        assertEquals(200, response.getStatusCode().value());
        assertEquals("Test", response.getBody().getTitle());
    }

    @Test
    void testCreate() {
        Incident i = new Incident();
        i.setTitle("New");
        i.setSeverity("HIGH");
        i.setStatus("OPEN");
        when(incidentService.createIncident(any())).thenReturn(i);

        ResponseEntity<Incident> response = incidentController.create(i);
        assertEquals(200, response.getStatusCode().value());
    }

    @Test
    void testUpdate() {
        Incident i = new Incident();
        i.setTitle("Updated");
        when(incidentService.update(eq(1L), any())).thenReturn(i);

        ResponseEntity<Incident> response = incidentController.update(1L, i);
        assertEquals(200, response.getStatusCode().value());
    }

    @Test
    void testDelete() {
        doNothing().when(incidentService).delete(1L);
        ResponseEntity<String> response = incidentController.delete(1L);
        assertEquals(200, response.getStatusCode().value());
        assertEquals("Deleted successfully", response.getBody());
    }
}
