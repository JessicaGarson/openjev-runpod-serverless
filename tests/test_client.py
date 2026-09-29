import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from client import OpenJev


def response(status, payload=None, text=""):
    result = Mock(status_code=status, text=text)
    result.json.return_value = payload
    if status >= 400:
        result.raise_for_status.side_effect = requests.HTTPError(str(status))
    return result


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"RUNPOD_API_KEY": "test-only", "ENDPOINT_ID": "test-endpoint"})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.session = Mock(headers={})
        self.client = OpenJev(self.session)

    @patch("client.time.sleep")
    def test_cold_start_then_ready(self, sleep):
        self.session.get.side_effect = [response(503), response(200)]
        self.client.wait_until_ready()
        self.assertEqual(self.session.get.call_count, 2)

    def test_auth_failure_does_not_retry(self):
        self.session.get.return_value = response(401)
        with self.assertRaises(RuntimeError):
            self.client.wait_until_ready()
        self.assertEqual(self.session.get.call_count, 1)

    def test_queue_endpoint_fails_immediately(self):
        self.session.get.return_value = response(400, text="not allowed for QB API")
        with self.assertRaisesRegex(RuntimeError, "Load balancer"):
            self.client.wait_until_ready()

    def test_bad_request_does_not_retry(self):
        self.session.post.return_value = response(400)
        with self.assertRaises(requests.HTTPError):
            self.client.ask("review", {})
        self.assertEqual(self.session.post.call_count, 1)

    @patch("client.time.sleep")
    def test_transient_error_retries_same_request(self, sleep):
        payload = {"answers": {"likes_sound": {"noul": 0.98}}}
        self.session.post.side_effect = [response(503), response(200, payload)]
        self.assertEqual(self.client.ask("review", {}), payload)
        self.assertEqual(self.session.post.call_count, 2)
        sent = self.session.post.call_args.kwargs["json"]
        self.assertEqual(sent["model"], "openjev")
        self.assertEqual(self.session.headers["Authorization"], "Bearer test-only")

    @patch("client.time.sleep")
    def test_timeout_has_bounded_attempts(self, sleep):
        self.session.post.side_effect = requests.Timeout()
        with self.assertRaises(requests.Timeout):
            self.client.ask("review", {})
        self.assertEqual(self.session.post.call_count, 3)

    def test_zero_readiness_deadline(self):
        with self.assertRaises(TimeoutError):
            self.client.wait_until_ready(max_wait=0)
        self.session.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
