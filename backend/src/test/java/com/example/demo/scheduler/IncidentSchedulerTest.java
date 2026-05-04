package com.example.demo.scheduler;

import com.example.demo.repository.IncidentRepository;
import com.example.demo.service.EmailService;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.mockito.Mockito.*;

class IncidentSchedulerTest {

    @Mock
    private IncidentRepository repository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private IncidentScheduler scheduler;

    public IncidentSchedulerTest() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testSendIncidentReport() {
        when(repository.count()).thenReturn(5L);
        doNothing().when(emailService).sendEmail(any(), any(), any());
        scheduler.sendIncidentReport();
        verify(repository, times(1)).count();
    }
}
