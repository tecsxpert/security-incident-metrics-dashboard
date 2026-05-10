from __future__ import annotations

import os
import threading
import time


class RuntimeMetrics:
    def __init__(self) -> None:
        self.started_at = time.time()
        self._lock = threading.Lock()
        self._total_response_time_ms = 0.0
        self._request_count = 0

    def record_response_time(self, duration_ms: float) -> None:
        with self._lock:
            self._request_count += 1
            self._total_response_time_ms += duration_ms

    def snapshot(self) -> dict[str, float | int | str]:
        with self._lock:
            avg_response_time_ms = (
                self._total_response_time_ms / self._request_count
                if self._request_count
                else 0.0
            )

        return {
            "uptime_seconds": round(time.time() - self.started_at, 3),
            "avg_response_time_ms": round(avg_response_time_ms, 3),
            "request_count": self._request_count,
            "model_name": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        }


runtime_metrics = RuntimeMetrics()
