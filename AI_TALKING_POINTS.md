# AI Talking Points Card — Tool-58
## Demo Day — Print and keep with you

---

## What is Groq?

Groq is a cloud AI platform that runs large language models at extremely
fast speeds. We use their free tier — no credit card, no cost.

The model we use is **LLaMA-3.3-70b** — a 70 billion parameter model
made by Meta, hosted on Groq's infrastructure. It is one of the most
capable open-source models available today.

---

## What do our 3 AI endpoints do?

### POST /describe
Takes a security incident and returns a structured analysis:
- What happened (summary)
- How the attack worked (attack vector)
- What was affected (impact)
- Warning signs to look for (indicators)
- Why this severity level is correct

**Plain English:** "Tell me what this incident is about"

### POST /recommend
Takes the same incident and returns exactly 3 prioritized actions:
- Containment — stop the bleeding right now
- Eradication — remove the threat completely
- Prevention — make sure it never happens again

**Plain English:** "Tell me what to do about it"

### POST /generate-report
Produces a complete professional incident report including:
- Executive summary for management
- Full timeline of events
- Technical analysis
- Impact assessment
- Remediation plan
- Lessons learned

**Plain English:** "Write me a proper report I can send to my boss"

---

## How does the AI know what to say?

We use **prompt templates** — text files that tell the AI exactly what
role to play and what format to respond in.

Example from our describe prompt:
> "You are a senior cybersecurity analyst working in a SOC.
> Analyze the incident and return ONLY valid JSON."

The AI always responds in JSON format so our Java backend can parse
it and display it cleanly in the dashboard.

---

## What happens if Groq is down?

We built a **fallback system**. If Groq fails after 3 retries:
- The endpoint still returns HTTP 200
- The response contains `"is_fallback": true`
- A pre-written structured template is returned
- The dashboard never crashes

---

## How do we prevent misuse?

**Rate limiting:** Maximum 30 requests per minute per IP address.
Exceeding this returns HTTP 429.

**Prompt injection protection:** We check every input against
14 patterns that detect attempts to manipulate the AI — like
"ignore all previous instructions" or "jailbreak". These return
HTTP 400 immediately without ever reaching Groq.

**Input sanitisation:** All HTML is stripped from inputs using
the `bleach` library before processing.

---

## How fast is it?

- /describe — typically 1-2 seconds
- /recommend — typically 1-2 seconds
- /generate-report — typically 2-4 seconds
- Cached responses — under 50ms

Redis caches identical requests for 15 minutes. If the same
incident is analyzed twice, the second response is instant.

---

## Security talking points

| What panel asks | Your answer |
|---|---|
| "Is the API key safe?" | Stored in .env only, never committed, loaded at runtime |
| "What if someone sends bad input?" | 14 injection patterns blocked, HTML stripped, 400 returned |
| "What if Groq is down?" | Fallback templates — service never crashes |
| "How do you prevent abuse?" | 30 req/min rate limit per IP via flask-limiter |
| "Is PII sent to Groq?" | No — only incident title, type, severity, system, description |
| "How many tests?" | 55 automated tests — all passing |

---

## /health endpoint — show this live

```
GET http://localhost:5000/health
```

Response shows:
- Service status
- Model being used
- Average response time
- Uptime
- Whether Redis cache is active

---

## 60-second explanation (say this)

"Our AI service is a Python Flask microservice on port 5000.
It uses Groq's LLaMA-3.3-70b model — completely free, no credit card.

When you create an incident in the dashboard, Java calls three AI
endpoints automatically. Describe tells you what happened. Recommend
gives you three actions to take. Generate-report writes a full
professional report in seconds.

Every input is checked for prompt injection before reaching the AI.
Responses are cached in Redis so repeated queries are instant.
If Groq goes down, our fallback system keeps everything running.

55 tests. All passing."