# AI Demo Script — Tool-58
## Day 14 — 60-second tech explanation for non-technical panel

---

## Demo Inputs (use exactly these)

### Input 1 — Phishing (for /describe)
```json
{
  "title":           "Phishing Attack on Finance Team",
  "incident_type":   "Phishing",
  "severity":        "High",
  "affected_system": "Email Server",
  "description":     "15 finance employees received emails impersonating the CFO requesting urgent wire transfers. 3 employees clicked malicious links exposing credentials."
}
```
**Expected:** summary, attack_vector, impact, indicators, severity_justification

---

### Input 2 — Ransomware (for /recommend)
```json
{
  "title":           "Ransomware on File Server",
  "incident_type":   "Ransomware",
  "severity":        "Critical",
  "affected_system": "Windows File Server FS-01",
  "description":     "Ransomware encrypted 2TB of shared drives. Attackers demand $50,000 Bitcoin. Backups are 3 days old."
}
```
**Expected:** 3 recommendations — containment, eradication, prevention

---

### Input 3 — Unauthorized Access (for /generate-report)
```json
{
  "title":           "Unauthorized Admin Access to Production Database",
  "incident_type":   "Unauthorized Access",
  "severity":        "Critical",
  "affected_system": "PostgreSQL Production Database",
  "description":     "An ex-employee account accessed the production database at 2AM. 50,000 customer records including PII were exported."
}
```
**Expected:** Full professional incident report with timeline, analysis, remediation

---

## 60-Second Tech Explanation (say this to panel)

> "Our AI service is a Flask microservice running on port 5000, powered by
> Groq's LLaMA-3.3-70b model — one of the fastest large language models
> available today, running completely free.
>
> When a security incident is created in our dashboard, the Java backend
> calls three AI endpoints automatically.
>
> First — /describe analyzes the incident and returns a structured
> breakdown: what happened, how it happened, and what was affected.
>
> Second — /recommend generates exactly three prioritized remediation
> actions your security team should take immediately.
>
> Third — /generate-report produces a complete professional incident
> report ready to send to management — in under 3 seconds.
>
> Every input is sanitized against 14 prompt injection patterns before
> reaching the AI. Responses are cached in Redis so repeated queries
> return instantly. And if Groq is unavailable, our fallback system
> ensures the dashboard never crashes — it just returns a structured
> placeholder instead.
>
> In total, the AI service has 55 automated tests — all passing."

---

## Backup Plan (if Groq is slow on demo day)

1. Show cached response — mention Redis cache is working
2. Show fallback — `is_fallback: true` in response
3. Show test results — `python -m unittest tests.test_week1_week2`
4. Show `/health` endpoint — uptime, model, cache status

---

## Response Time Targets

| Endpoint | Target | Acceptable |
|---|---|---|
| /describe | < 2s | < 5s |
| /recommend | < 2s | < 5s |
| /generate-report | < 3s | < 8s |
| /health | < 0.1s | < 0.5s |