package com.example.demo.exception;

import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class GlobalExceptionHandlerTest {
    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test
    void testHandleRuntime() {
        RuntimeException ex = new RuntimeException("Test error");
        ResponseEntity<?> response = handler.handleRuntime(ex);
        assertEquals(500, response.getStatusCode().value());
        Map<?, ?> body = (Map<?, ?>) response.getBody();
        assertEquals("Test error", body.get("message"));
    }

    @Test
    void testHandleGeneric() {
        Exception ex = new Exception("Generic error");
        ResponseEntity<?> response = handler.handleGeneric(ex);
        assertEquals(500, response.getStatusCode().value());
    }

    @Test
    void testHandleValidation() {
        MethodArgumentNotValidException ex = mock(MethodArgumentNotValidException.class);
        BindingResult bindingResult = mock(BindingResult.class);
        FieldError fieldError = new FieldError("incident", "severity", "must not be null");
        when(ex.getBindingResult()).thenReturn(bindingResult);
        when(bindingResult.getFieldErrors()).thenReturn(List.of(fieldError));
        ResponseEntity<?> response = handler.handleValidation(ex);
        assertEquals(400, response.getStatusCode().value());
    }
}
