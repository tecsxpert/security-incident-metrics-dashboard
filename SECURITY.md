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
the AI system prompt — instructing the model to ignore its role
or reveal internal instructions.

**Impact:** High — AI produces harmful or unauthorized output

**Mitigation:**
- System message enforces strict cybersecurity-only role
- User input never concatenated directly into system prompt
- Prompt templates stored separately in `prompts/`
- `middleware/sanitiser.py` strips all HTML using `bleach`
- 14 regex patterns detect and block injection attempts
- Returns HTTP 400 on detection


---

## Threat 3 — Rate Limit Bypass

**Description:**
An attacker floods endpoints with rapid requests, exhausting
the free Groq API quota or degrading service for all users.

**Impact:** Medium — service unavailability, API quota exhaustion

**Mitigation:**
- `flask-limiter` enforces 30 requests/minute per IP
- Exceeding limit returns HTTP 429
- `X-RateLimit` headers returned to clients
- Redis caches repeated AI responses
- Groq errors trigger 3-retry with exponential backoff


---

## Threat 4 — Unauthenticated Endpoint Access

**Description:**
Attacker calls Flask AI service endpoints directly, bypassing
JWT authentication in the Java backend entirely.

**Impact:** High — unauthorized AI usage, data exposure

**Mitigation:**
- Flask service not exposed publicly — internal Docker network only
- Java backend (port 8080) is the only public entry point
- JWT validation enforced in Spring Security before any AI call
- Docker Compose network isolates `ai-service`


---

## Threat 5 — Sensitive Data in Logs

**Description:**
Error logs accidentally include API keys, JWT tokens, or
incident PII readable by anyone with log access.

**Impact:** Medium — credential theft, privacy violation

**Mitigation:**
- Logger set to `INFO` level in production
- API keys and tokens never passed to `logger.*` calls
- Incident data logged by ID only — not full content
- Log output reviewed as part of security testing checklist


---

## Threat 6 — Empty / Malformed Input

**Description:**
Attacker sends empty, null, or malformed JSON to crash
the AI service or cause unexpected behaviour.

**Impact:** Medium — service crash, unhandled exceptions

**Mitigation:**
- `parse_json_body()` in `helpers.py` validates JSON before processing
- `validate_input()` checks all required fields are present and non-empty
- Returns HTTP 400 with clear error message on invalid input


---

## Threat 7 — SQL Injection

**Description:**
Attacker sends SQL commands in input fields attempting
to manipulate the PostgreSQL database.

**Impact:** High — data theft, data corruption, full DB access

**Mitigation:**
- All DB queries use JPA/Hibernate with parameterised queries
- No raw SQL strings constructed from user input
- Input sanitised before reaching backend
- Flyway migrations use versioned SQL files only


---

*Last updated: Day 5 — AI Developer 2*