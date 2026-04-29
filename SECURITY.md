# SECURITY.md — Security Incident Metrics Dashboard

## Overview
This document identifies the top security threats relevant to this
application and the mitigations applied or planned.

---

## Threat 1 — API Key Exposure

**Description:**
The Groq API key, if hardcoded or committed to version control,
can be stolen and used to exhaust API quotas or access AI services
under the project's account.

**Impact:** High — financial cost, service disruption

**Mitigation:**
- API key stored exclusively in `.env` (never committed)
- `.env` listed in `.gitignore`
- `.env.example` used as a safe template for teammates
- Application reads key via `os.environ.get()` at runtime only

---

## Threat 2 — Prompt Injection

**Description:**
A malicious user crafts an incident description that manipulates
the AI system prompt — for example, instructing the model to
ignore its role or reveal internal instructions.

**Impact:** High — AI produces harmful, misleading, or unauthorized output

**Mitigation:**
- System message enforces strict cybersecurity-only role
- User input is never concatenated directly into the system prompt
- Prompt templates stored separately in `prompts/` and reviewed
- AI responses are validated before being returned to the frontend

---

## Threat 3 — Rate Limit Bypass

**Description:**
An attacker floods the `/generate-report`, `/describe`, or
`/recommend` endpoints with rapid requests, exhausting the free
Groq API quota or degrading service for all users.

**Impact:** Medium — service unavailability, API quota exhaustion

**Mitigation:**
- `flask-limiter` enforces 30 requests/minute per IP address
- Exceeding the limit returns HTTP 429 Too Many Requests
- Redis used to cache repeated AI responses (reduces API calls)
- Groq API errors trigger 3-retry with exponential backoff

---

## Threat 4 — Unauthenticated Endpoint Access

**Description:**
The Flask AI service endpoints are called directly by an attacker
who bypasses the Java backend, skipping JWT authentication and
role-based access control entirely.

**Impact:** High — unauthorized AI usage, data exposure

**Mitigation:**
- Flask service is not exposed publicly — internal Docker network only
- Only the Java backend (port 8080) is the public-facing entry point
- JWT validation enforced in Spring Security before any AI call
- Docker Compose network isolates `ai-service` from direct access

---

## Threat 5 — Sensitive Data in Logs

**Description:**
Error logs or debug output accidentally include API keys, JWT
tokens, user credentials, or incident PII — which can be read by
anyone with log access.

**Impact:** Medium — credential theft, privacy violation, compliance breach

**Mitigation:**
- Logger configured to `INFO` level in production (no DEBUG)
- API keys and tokens are never passed to `logger.*` calls
- Incident data logged by ID only — not full content
- Log output reviewed as part of security testing checklist

---

*Last updated: Day 2 — AI Developer 2*