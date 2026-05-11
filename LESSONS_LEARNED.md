# Lessons Learned — Tool-58 AI Service
## Post-Demo — AI Developer 2

---

## What Went Well

**1. Groq API — Free and Fast**
LLaMA-3.3-70b on Groq exceeded expectations. Response times were
consistently under 2 seconds. Free tier was sufficient for the entire
sprint with no quota issues.

**2. Prompt Templates as Files**
Storing prompts in `.txt` files instead of hardcoding them in Python
was the right decision. Easy to tune without touching code. Rewriting
prompts took minutes instead of hours.

**3. Fallback System**
Building fallback templates from Day 9 meant the service never crashed
during testing — even when Groq had occasional slow responses.

**4. Shared helpers.py**
Extracting validation and sanitisation into `middleware/helpers.py`
eliminated duplicated code across all 3 routes. Any future route
just imports the same 3 functions.

**5. 55 Automated Tests**
Having a full test suite meant every change could be verified
immediately. Caught the `/recommend` list bug instantly in logs.

---

## What Was Difficult

**1. Prompt Brace Escaping**
Python's `.format()` treats `{` and `}` in prompt files as variables.
Every JSON example in prompt files needed double braces `{{` and `}}`.
This caused multiple test failures before being fixed.

**2. /recommend 500 Error**
Groq returned a raw list instead of `{"recommendations": [...]}`.
The fix was a simple isinstance check but took time to diagnose.
Lesson: always log the raw AI response during development.

**3. .env Path Resolution**
`load_dotenv()` path needed to be absolute using `Path(__file__).resolve()`
to work correctly regardless of where the script was run from.

**4. Redis Not Running Locally**
Tests ran without Redis — cache was disabled gracefully but caused
`CacheService` to initialize slowly. In production Docker, Redis
is always available.

---

## What to Improve in Future Sprints

**1. Streaming Responses**
For `/generate-report`, streaming the AI response to the frontend
would feel faster even if total time is the same.

**2. Async Endpoints**
Using Flask async or switching to FastAPI would allow parallel
AI calls — useful if multiple incidents need analysis simultaneously.

**3. Prompt Versioning**
Track which prompt version produced which output. Useful for
debugging when AI quality drops after prompt changes.

**4. AI Response Validation**
Add JSON schema validation on AI responses. Currently we check
structure manually — a schema validator would be more robust.

**5. Monitoring**
Add Prometheus metrics to track real response times, cache hit
rates, and Groq error rates in production.

---

## Features for Future Sprints

- Streaming AI responses to frontend
- Batch incident analysis
- AI confidence scoring
- Historical AI accuracy tracking
- Multi-language incident reports
- Custom prompt templates per organization

---

## Final Note

The AI service is fully functional, tested, and documented.
All 55 tests pass. All 3 endpoints verified working with real
Groq API calls. Security reviewed and signed off.

*AI Developer 2 — Tool-58 Capstone Sprint*
*Apr 14 – May 9, 2026*