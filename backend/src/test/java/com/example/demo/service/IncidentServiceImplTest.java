package com.example.demo.service;

import com.example.demo.entity.Incident;
import com.example.demo.repository.IncidentRepository;
import com.example.demo.service.impl.IncidentServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import java.util.List;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class IncidentServiceImplTest {

    @Mock
    private IncidentRepository repository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private IncidentServiceImpl service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetAllIncidents() {
        Incident i = new Incident();
        i.setTitle("Test");
        when(repository.findAll()).thenReturn(List.of(i));
        List<Incident> result = service.getAllIncidents();
        assertEquals(1, result.size());
    }

    @Test
    void testGetById_NotFound() {
        when(repository.findById(99L)).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> service.getById(99L));
    }

    @Test
    void testUpdateIncident() {
        Incident existing = new Incident();
        existing.setId(1L);
        existing.setTitle("Old");
        existing.setSeverity("LOW");
        existing.setStatus("OPEN");
        existing.setDescription("Old desc");

        Incident updated = new Incident();
        updated.setTitle("New");
        updated.setSeverity("HIGH");
        updated.setStatus("RESOLVED");
        updated.setDescription("New desc");

        when(repository.findById(1L)).thenReturn(Optional.of(existing));
        when(repository.save(any())).thenReturn(existing);

        Incident result = service.update(1L, updated);
        assertEquals("New", result.getTitle());
    }

    @Test
    void testDeleteNotFound() {
        when(repository.existsById(99L)).thenReturn(false);
        assertThrows(RuntimeException.class, () -> service.delete(99L));
    }
}
