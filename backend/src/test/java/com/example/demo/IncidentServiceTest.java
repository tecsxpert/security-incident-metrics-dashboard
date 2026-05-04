package com.example.demo.service;

import com.example.demo.entity.Incident;
import com.example.demo.repository.IncidentRepository;
import com.example.demo.service.impl.IncidentServiceImpl;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class IncidentServiceTest {

    @Mock
    private IncidentRepository repository;

    @Mock
    private EmailService emailService;   // ✅ FIX ADDED

    @InjectMocks
    private IncidentServiceImpl service;

    public IncidentServiceTest() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testCreateIncident() {
        Incident incident = new Incident();
        incident.setTitle("Test");
        incident.setDescription("Desc");
        incident.setSeverity("LOW");

        when(repository.save(any(Incident.class))).thenReturn(incident);
        doNothing().when(emailService).sendEmail(any(), any(), any()); // ✅ FIX

        Incident result = service.createIncident(incident);

        assertNotNull(result);
        verify(repository, times(1)).save(any(Incident.class));
        verify(emailService, times(1)).sendEmail(any(), any(), any());
    }

    @Test
    void testGetById() {
        Incident incident = new Incident();
        incident.setId(1L);

        when(repository.findById(1L)).thenReturn(Optional.of(incident));

        Incident result = service.getById(1L);

        assertEquals(1L, result.getId());
    }

    @Test
    void testDeleteIncident() {
        when(repository.existsById(1L)).thenReturn(true);
        doNothing().when(repository).deleteById(1L);

        service.delete(1L);

        verify(repository, times(1)).deleteById(1L);
    }
}
