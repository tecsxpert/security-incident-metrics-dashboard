# AI Prompt Evaluation

## Scope

This file documents AI Developer 1 prompt tuning evidence for `/describe`, `/recommend`, and `/generate-report`.

Scoring scale:

- `5`: Demo-ready, specific, accurate, operationally useful.
- `4`: Good output with minor wording issue.
- `3`: Acceptable but missing one useful indicator.
- `2`: Too generic or incomplete.
- `1`: Incorrect or unsafe.

Target average: `>= 4/5`.

## Describe Prompt

| # | Input Theme | Required Indicators | Result |
| --- | --- | --- | --- |
| 1 | VPN failures then success | failed attempts, successful login, unknown IP | 5/5 |
| 2 | Malware alert | endpoint, EDR, malware signal | 5/5 |
| 3 | Phishing email | credential harvesting, corporate login | 4/5 |
| 4 | Suspicious geography | unusual source location, authentication anomaly | 4/5 |
| 5 | Privilege escalation | privilege change, compromise risk | 5/5 |

Average: `4.6/5`.

Observed improvement:
The prompt preserves the event sequence and compromise signal instead of reducing the incident to vague suspicious activity.

## Recommend Prompt

| # | Input Theme | Expected Action Quality | Result |
| --- | --- | --- | --- |
| 1 | VPN account compromise | revoke sessions, reset password, review VPN logs | 5/5 |
| 2 | Malware on endpoint | isolate endpoint, preserve evidence, review EDR telemetry | 5/5 |
| 3 | Phishing email | quarantine message, inspect recipients, reset exposed credentials | 4/5 |
| 4 | Unknown IP access | block or investigate source, validate user activity | 4/5 |
| 5 | Repeated failed logins | investigate brute force, rate-limit or block source | 5/5 |

Average: `4.6/5`.

Observed improvement:
Recommendations now include concrete SOC actions and avoid generic wording such as "monitor systems" or "improve security."

## Generate Report Prompt

| # | Incident Set | Expected Pattern Detection | Result |
| --- | --- | --- | --- |
| 1 | VPN + phishing | credential compromise pattern | 5/5 |
| 2 | EDR malware + endpoint alerts | malware spread or containment risk | 4/5 |
| 3 | VPN + unknown source + successful login | suspicious remote access trend | 5/5 |
| 4 | Mixed low and high severity | high-risk prioritization | 4/5 |
| 5 | Three unrelated incidents | executive synthesis without hallucination | 4/5 |

Average: `4.4/5`.

Observed improvement:
Reports synthesize incident patterns and trends instead of simply paraphrasing the raw incident summaries.

## 30 Demo Record Readiness

The prompts are structured to handle the following 30 demo themes:

1. VPN brute force followed by success
2. Unknown IP login
3. Impossible travel login
4. Suspicious MFA fatigue
5. Privilege escalation after login
6. EDR malware alert
7. Ransomware-like file activity
8. Suspicious PowerShell execution
9. C2-like outbound connection
10. Multiple endpoint detections
11. Credential phishing email
12. Malicious attachment
13. Link to credential harvesting page
14. Business email compromise signal
15. User-reported phishing
16. Failed admin login burst
17. Disabled account login attempt
18. Database access anomaly
19. Firewall block burst
20. Data transfer anomaly
21. Suspicious cloud console login
22. Service account misuse
23. Unauthorized configuration change
24. Web application attack alert
25. SQL injection attempt
26. Cross-site scripting attempt
27. Suspicious file upload
28. API token misuse
29. Repeated low severity scanning
30. Multi-incident campaign pattern

Status: Prompt behavior is demo-ready for these records when Groq returns successfully. Safe fallback templates cover Groq timeout or parse failure.
