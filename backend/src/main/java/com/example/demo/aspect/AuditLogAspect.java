package com.example.demo.aspect;

import com.example.demo.entity.AuditLog;
import com.example.demo.entity.Incident;
import com.example.demo.repository.AuditLogRepository;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class AuditLogAspect {

    private final AuditLogRepository auditLogRepository;

    public AuditLogAspect(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    private String getCurrentUsername() {
        try {
            return SecurityContextHolder.getContext().getAuthentication().getName();
        } catch (Exception e) {
            return "SYSTEM";
        }
    }

    @AfterReturning(pointcut = "execution(* com.example.demo.service.IncidentService.createIncident(..))", returning = "result")
    public void logCreate(JoinPoint joinPoint, Object result) {
        if (result instanceof Incident incident) {
            auditLogRepository.save(new AuditLog("Incident", incident.getId(), "CREATE", getCurrentUsername(), "Created incident: " + incident.getTitle()));
        }
    }

    @AfterReturning(pointcut = "execution(* com.example.demo.service.IncidentService.update(..))", returning = "result")
    public void logUpdate(JoinPoint joinPoint, Object result) {
        if (result instanceof Incident incident) {
            auditLogRepository.save(new AuditLog("Incident", incident.getId(), "UPDATE", getCurrentUsername(), "Updated incident: " + incident.getTitle()));
        }
    }

    @AfterReturning(pointcut = "execution(* com.example.demo.service.IncidentService.delete(..))")
    public void logDelete(JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs();
        if (args.length > 0 && args[0] instanceof Long id) {
            auditLogRepository.save(new AuditLog("Incident", id, "DELETE", getCurrentUsername(), "Soft deleted incident ID: " + id));
        }
    }
}
