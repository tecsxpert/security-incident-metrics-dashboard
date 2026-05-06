package com.example.demo.controller;

import com.example.demo.entity.Incident;
import com.example.demo.service.IncidentService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.Arrays;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

public class IncidentControllerTest {

    private MockMvc mockMvc;

    @Mock
    private IncidentService incidentService;

    @InjectMocks
    private IncidentController incidentController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        mockMvc = MockMvcBuilders.standaloneSetup(incidentController).build();
    }

    @Test
    void getAllIncidents_ShouldReturnList() throws Exception {
        Incident incident = new Incident();
        incident.setTitle("Test");
        when(incidentService.getAllIncidents()).thenReturn(Arrays.asList(incident));

        mockMvc.perform(get("/api/incidents"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].title").value("Test"));
    }

    @Test
    void getIncidentById_ShouldReturnIncident() throws Exception {
        Incident incident = new Incident();
        incident.setTitle("Test ID");
        when(incidentService.getById(1L)).thenReturn(incident);

        mockMvc.perform(get("/api/incidents/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Test ID"));
    }

    @Test
    void createIncident_ShouldReturnCreatedIncident() throws Exception {
        Incident incident = new Incident();
        incident.setTitle("New");
        when(incidentService.createIncident(any(Incident.class))).thenReturn(incident);

        mockMvc.perform(post("/api/incidents")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"title\":\"New\",\"severity\":\"HIGH\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("New"));
    }

    @Test
    void updateIncident_ShouldReturnUpdatedIncident() throws Exception {
        Incident incident = new Incident();
        incident.setTitle("Updated");
        when(incidentService.update(anyLong(), any(Incident.class))).thenReturn(incident);

        mockMvc.perform(put("/api/incidents/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"title\":\"Updated\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Updated"));
    }

    @Test
    void deleteIncident_ShouldReturnSuccess() throws Exception {
        doNothing().when(incidentService).delete(1L);

        mockMvc.perform(delete("/api/incidents/1"))
                .andExpect(status().isOk())
                .andExpect(content().string("Deleted successfully"));
    }

    @Test
    void searchIncidents_ShouldReturnList() throws Exception {
        Incident incident = new Incident();
        incident.setTitle("Match");
        when(incidentService.search("Match")).thenReturn(Arrays.asList(incident));

        mockMvc.perform(get("/api/incidents/search?q=Match"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].title").value("Match"));
    }
}
