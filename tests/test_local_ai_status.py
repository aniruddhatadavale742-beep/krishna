import unittest
from unittest.mock import Mock, patch

import requests

from brain.local_ai import LocalAI


class LocalAIStatusTests(unittest.TestCase):
    def setUp(self):
        self.local_ai = LocalAI()

    @patch("brain.local_ai.requests.get")
    def test_status_reports_available_model(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "models": [{"name": self.local_ai.model}]
        }
        mock_get.return_value = response

        status = self.local_ai.get_status()

        self.assertTrue(status["ollama_available"])
        self.assertTrue(status["model_available"])
        self.assertEqual(status["model"], self.local_ai.model)
        mock_get.assert_called_once_with(
            self.local_ai.tags_url,
            timeout=min(self.local_ai.connection_timeout, 2),
        )

    @patch("brain.local_ai.requests.get")
    def test_status_reports_missing_model(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"models": []}
        mock_get.return_value = response

        status = self.local_ai.get_status()

        self.assertTrue(status["ollama_available"])
        self.assertFalse(status["model_available"])

    @patch("brain.local_ai.requests.get")
    def test_status_handles_connection_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()

        status = self.local_ai.get_status()

        self.assertFalse(status["ollama_available"])
        self.assertFalse(status["model_available"])
        self.assertEqual(status["detail"], "could not connect")

    @patch("brain.local_ai.requests.get")
    def test_status_handles_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()

        status = self.local_ai.get_status()

        self.assertFalse(status["ollama_available"])
        self.assertEqual(status["detail"], "request timed out")


if __name__ == "__main__":
    unittest.main()
