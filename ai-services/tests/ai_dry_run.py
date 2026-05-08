# scripts/ai_dry_run.py — Day 14 dry run on demo machine

import requests
import time
import json

BASE_URL = "http://localhost:5000"

DEMO_INPUTS = [
    {
        "title":           "Phishing Attack on Finance Team",
        "incident_type":   "Phishing",
        "severity":        "High",
        "affected_system": "Email Server",
        "description":     "15 finance employees received emails impersonating CFO. 3 clicked malicious links."
    },
    {
        "title":           "Ransomware on File Server",
        "incident_type":   "Ransomware",
        "severity":        "Critical",
        "affected_system": "Windows File Server FS-01",
        "description":     "2TB of shared drives encrypted. Attackers demand $50,000 Bitcoin."
    },
    {
        "title":           "Unauthorized DB Access",
        "incident_type":   "Unauthorized Access",
        "severity":        "Critical",
        "affected_system": "PostgreSQL Production Database",
        "description":     "Ex-employee account accessed prod DB at 2AM. 50,000 customer records exported."
    },
]


def run_endpoint(name, url, body):
    start = time.time()
    try:
        r       = requests.post(url, json=body, timeout=30)
        elapsed = round(time.time() - start, 2)
        status  = "PASS" if r.status_code == 200 else "FAIL"
        print(f"  {status} — {name} | {elapsed}s | HTTP {r.status_code}")
        return elapsed
    except Exception as e:
        print(f"  FAIL — {name} | ERROR: {str(e)}")
        return None


if __name__ == "__main__":
    print("=" * 55)
    print("Tool-58 AI Service — Demo Dry Run")
    print("=" * 55)

    # Health check
    print("\n[Health]")
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    h = r.json()
    print(f"  Status  : {h.get('status')}")
    print(f"  Model   : {h.get('model')}")
    print(f"  Cache   : {h.get('cache_enabled')}")
    print(f"  Uptime  : {h.get('uptime', {}).get('total_seconds')}s")

    all_times = []

    for i, body in enumerate(DEMO_INPUTS, 1):
        print(f"\n[Input {i}] {body['title']}")
        t1 = run_endpoint("/describe",        f"{BASE_URL}/describe",        body)
        t2 = run_endpoint("/recommend",       f"{BASE_URL}/recommend",       body)
        t3 = run_endpoint("/generate-report", f"{BASE_URL}/generate-report", body)
        for t in [t1, t2, t3]:
            if t:
                all_times.append(t)

    if all_times:
        avg = round(sum(all_times) / len(all_times), 2)
        mx  = round(max(all_times), 2)
        print(f"\n{'=' * 55}")
        print(f"Avg response time : {avg}s")
        print(f"Max response time : {mx}s")
        print(f"Target            : under 2s average")
        print(f"Result            : {'PASS' if avg < 2 else 'SLOW — check Groq latency'}")
        print("=" * 55)