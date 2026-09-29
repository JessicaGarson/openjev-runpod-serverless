"""Small synchronous client for the OpenJev load-balancer API."""
import os
import time

import requests


class OpenJev:
    def __init__(self, session=None):
        key = os.environ.get("RUNPOD_API_KEY")
        endpoint = os.environ.get("ENDPOINT_ID")
        if not key or not endpoint:
            raise ValueError("Set RUNPOD_API_KEY and ENDPOINT_ID first.")
        if not all(c.isalnum() or c == "-" for c in endpoint):
            raise ValueError("ENDPOINT_ID must be an endpoint ID, not a URL.")
        self.base_url = f"https://{endpoint}.api.runpod.ai"
        self.session = session or requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {key}"})

    def wait_until_ready(self, max_wait=1200):
        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            try:
                response = self.session.get(
                    f"{self.base_url}/v1/version",
                    timeout=min(130, max(0.1, deadline - time.monotonic())),
                )
                if response.status_code == 200:
                    print("Worker ready.")
                    return
                if response.status_code in (401, 403):
                    raise RuntimeError("Check RUNPOD_API_KEY and endpoint permissions.")
                if "not allowed for QB API" in response.text:
                    raise RuntimeError("Create a Load balancer endpoint, not Queue.")
                if 400 <= response.status_code < 500 and response.status_code != 429:
                    response.raise_for_status()
                print(f"Waiting for worker (HTTP {response.status_code}).")
            except (requests.ConnectionError, requests.Timeout):
                print("Waiting for worker (connection not ready).")
            time.sleep(min(10, max(0, deadline - time.monotonic())))
        raise TimeoutError("No worker ready within the deadline. Check Runpod worker logs.")

    def ask(self, state, questions, attempts=3):
        payload = {"model": "openjev", "state": state, "questions": questions}
        for attempt in range(attempts):
            try:
                response = self.session.post(
                    f"{self.base_url}/v1/systemone", json=payload, timeout=60
                )
                if response.status_code == 429 or response.status_code >= 500:
                    if attempt + 1 < attempts:
                        time.sleep(10)
                        continue
                response.raise_for_status()
                return response.json()
            except (requests.ConnectionError, requests.Timeout):
                if attempt + 1 == attempts:
                    raise
                time.sleep(10)
        raise RuntimeError("No answer returned.")
