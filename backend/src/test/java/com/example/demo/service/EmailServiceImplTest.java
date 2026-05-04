package com.example.demo.service;

import com.example.demo.service.impl.IncidentServiceImpl;
import com.example.demo.entity.Incident;
import com.example.demo.repository.IncidentRepository;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import java.util.Arrays;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class EmailServiceImplTest {

    @Mock
    private IncidentRepository repository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private IncidentServiceImpl service;

    public EmailServiceImplTest() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetAllReturnsMultiple() {
        Incident i1 = new Incident();
        i1.setTitle("First");
        i1.setSeverity("HIGH");

        Incident i2 = new Incident();
        i2.setTitle("Second");
        i2.setSeverity("LOW");

        when(repository.findAll()).thenReturn(Arrays.asList(i1, i2));
        List<Incident> result = service.getAllIncidents();
        assertEquals(2, result.size());
    }

    @Test
    void testUpdateOnlyTitle() {
        Incident existing = new Incident();
        existing.setId(1L);
        existing.setTitle("Old");
        existing.setSeverity("LOW");
        existing.setStatus("OPEN");

        Incident update = new Incident();
        update.setTitle("New Title");

        when(repository.findById(1L)).thenReturn(java.util.Optional.of(existing));
        when(repository.save(any())).thenReturn(existing);

        Incident result = service.update(1L, update);
        assertEquals("New Title", result.getTitle());
        assertEquals("LOW", result.getSeverity());
    }
}
