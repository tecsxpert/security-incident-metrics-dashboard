# AI Service — Tool-58 Security Incident Metrics Dashboard

Flask-based AI microservice using Groq LLaMA-3.3-70b. Provides three AI-powered endpoints for security incident analysis.

---

## Setup

### 1. Clone and navigate
```bash
cd ai-service
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Copy `.env.example` to `.env` in the project root and fill in your values:
```bash
cp .env.example .env
```

Required variables:
```
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_MAX_RETRIES=3
GROQ_BACKOFF_BASE=2
GROQ_MAX_TOKENS=1024
GROQ_TEMPERATURE=0.5
AI_SERVICE_BASE_URL=http://localhost:5000
AI_CACHE_TTL_SECONDS=900
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 5. Run the service
```bash
python app.py
```

Service starts on **port 5000**.

---

## Docker
```bash
docker-compose up --build
```

---

## API Reference

### GET /health
Health check with model info, uptime and average response time.

**Response:**
```json
{
  "status":            "ok",
  "service":           "ai-service",
  "port":              5000,
  "model":             "llama-3.3-70b-versatile",
  "avg_response_time": 1.234,
  "uptime":            { "days": 0, "hours": 1, "minutes": 30, "seconds": 5, "total_seconds": 5405 },
  "cache_enabled":     true
}
```

---

### POST /describe
Analyze a security incident and return structured description.

**Request:**
```json
{
  "title":           "Phishing Attack on Finance Team",
  "incident_type":   "Phishing",
  "severity":        "High",
  "affected_system": "Email Server",
  "description":     "15 employees received phishing emails targeting credentials"
}
```

**Response:**
```json
{
  "success":      true,
  "is_fallback":  false,
  "generated_at": "2024-04-21T10:30:00Z",
  "data": {
    "summary":                "A phishing campaign targeted finance team members.",
    "attack_vector":          "Spear phishing emails impersonating the CFO",
    "impact":                 "Credential theft affecting 3 employees",
    "indicators":             ["suspicious-domain.com", "unusual login times"],
    "severity_justification": "High due to credential exposure"
  },
  "usage": { "model": "llama-3.3-70b-versatile", "total_tokens_used": 320 }
}
```

**Severity values:** `Low` | `Medium` | `High` | `Critical`

---

### POST /recommend
Generate exactly 3 actionable remediation recommendations.

**Request:** Same fields as `/describe`

**Response:**
```json
{
  "success":         true,
  "is_fallback":     false,
  "generated_at":    "2024-04-21T10:30:00Z",
  "recommendations": [
    { "action_type": "containment", "description": "Block sender domain immediately",   "priority": "Immediate" },
    { "action_type": "eradication", "description": "Reset all affected account creds",  "priority": "High"      },
    { "action_type": "prevention",  "description": "Enable MFA for all finance staff",  "priority": "Medium"    }
  ],
  "usage": { "model": "llama-3.3-70b-versatile", "total_tokens_used": 280 }
}
```

---

### POST /generate-report
Generate a full professional incident report.

**Request:** Same fields as `/describe`

**Response:**
```json
{
  "success":      true,
  "is_fallback":  false,
  "generated_at": "2024-04-21T10:30:00Z",
  "report": {
    "report_title":      "Phishing Incident Report — Finance Team",
    "executive_summary": "A targeted phishing campaign affected the finance team...",
    "incident_timeline": [
      { "time": "T+0h", "event": "Incident detected" },
      { "time": "T+1h", "event": "Investigation started" }
    ],
    "technical_analysis": {
      "attack_vector":            "Spear phishing via email",
      "affected_components":      ["Email Server", "Finance Workstations"],
      "data_at_risk":             "Employee credentials and financial data",
      "indicators_of_compromise": ["suspicious-domain.com"]
    },
    "impact_assessment": {
      "business_impact": "Finance operations disrupted for 4 hours",
      "data_impact":     "Credentials potentially compromised",
      "user_impact":     "15 employees affected"
    },
    "remediation": {
      "immediate_actions":         ["Block malicious domain", "Reset compromised passwords"],
      "long_term_recommendations": ["Deploy MFA", "Run security awareness training"]
    },
    "lessons_learned": ["Email filtering rules need updating"],
    "risk_rating":     "High",
    "report_generated_at": "2024-04-21T10:30:00Z"
  },
  "usage": { "model": "llama-3.3-70b-versatile", "total_tokens_used": 750 }
}
```

---

## Error Responses

| Status | Meaning |
|---|---|
| 400 | Bad request — missing/invalid fields or prompt injection detected |
| 404 | Endpoint not found |
| 405 | Wrong HTTP method |
| 429 | Rate limit exceeded — max 30 requests/min per IP |
| 500 | Internal server error |
| 502 | AI returned invalid response — retry |
| 503 | AI service unavailable — fallback returned |

---

## Fallback Behaviour
When Groq API is unavailable, all endpoints return a structured fallback response with `"is_fallback": true` instead of an error. The system never crashes — it degrades gracefully.

---

## Rate Limiting
- 30 requests per minute per IP address
- Enforced by `flask-limiter`
- Returns HTTP 429 with `X-RateLimit` headers

---

## Caching
- Redis cache with SHA256 keys
- 15-minute TTL (configurable via `AI_CACHE_TTL_SECONDS`)
- Identical requests return cached responses instantly
- Cache gracefully disabled if Redis is unavailable

---

## Security
- HTML stripped from all inputs using `bleach`
- 14 prompt injection patterns detected and blocked
- Security headers on all responses (X-Frame-Options, X-Content-Type-Options, etc.)
- API keys loaded from `.env` only — never hardcoded
- See `SECURITY.md` for full threat documentation

---

## Running Tests
```bash
python -m unittest tests.test_week1_week2 -v
```

Expected: **55 tests passing**

---

## Folder Structure
```
ai-service/
├── middleware/
│   ├── sanitiser.py       — HTML stripping + injection detection
│   └── helpers.py         — shared validation used by all routes
├── prompts/
│   ├── describe.txt       — prompt template for /describe
│   ├── recommend.txt      — prompt template for /recommend
│   └── generate_report.txt — prompt template for /generate-report
├── routes/
│   ├── health.py          — GET /health
│   ├── describe.py        — POST /describe
│   ├── recommend.py       — POST /recommend
│   └── generate_report.py — POST /generate-report
├── services/
│   ├── groq_client.py     — Groq API wrapper with retry/backoff
│   ├── cache_service.py   — Redis cache with SHA256 keys
│   └── fallback_service.py — fallback templates when Groq is down
├── tests/
│   └── test_week1_week2.py — 55 tests
├── app.py                 — Flask entry point
├── Dockerfile
└── README.md
```

---

*AI Developer — Tool-58 Capstone Sprint | Apr 14 – May 9, 2026*