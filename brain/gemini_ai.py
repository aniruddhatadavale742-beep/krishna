import os
import requests
from dotenv import load_dotenv


class GeminiAI:
    """
    KRISHNA's online AI using Google Gemini.

    This version uses a short HTTP timeout so that
    KRISHNA can automatically fall back to local AI
    instead of getting stuck waiting for Gemini.
    """

    def __init__(self):

        load_dotenv()

        self.api_key = os.getenv("GEMINI_API_KEY")

        self.model = "gemini-3.7-flash"

        self.base_url = (
            "https://generativelanguage.googleapis.com"
            f"/v1beta/models/{self.model}:generateContent"
        )

    def ask(self, user_input):

        if not self.api_key:
            raise Exception("GEMINI_API_KEY is missing.")

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": user_input
                        }
                    ]
                }
            ]
        }

        try:

            response = requests.post(
                self.base_url,
                params={
                    "key": self.api_key
                },
                json=payload,

                # IMPORTANT:
                # Do not let Gemini keep KRISHNA stuck.
                timeout=15
            )

            # Quota / rate limit
            if response.status_code == 429:
                raise Exception(
                    "Gemini quota exceeded."
                )

            # Authentication problem
            if response.status_code == 401:
                raise Exception(
                    "Gemini API key is invalid."
                )

            # Other API errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    message = error_data.get(
                        "error",
                        {}
                    ).get(
                        "message",
                        "Gemini API error."
                    )
                except Exception:
                    message = response.text

                raise Exception(message)

            data = response.json()

            candidates = data.get(
                "candidates",
                []
            )

            if not candidates:
                raise Exception(
                    "Gemini returned no response."
                )

            parts = (
                candidates[0]
                .get("content", {})
                .get("parts", [])
            )

            if not parts:
                raise Exception(
                    "Gemini returned empty content."
                )

            answer = parts[0].get(
                "text",
                ""
            ).strip()

            if not answer:
                raise Exception(
                    "Gemini returned an empty response."
                )

            return answer

        except requests.exceptions.Timeout:
            raise Exception(
                "Gemini request timed out."
            )

        except requests.exceptions.ConnectionError:
            raise Exception(
                "Unable to connect to Gemini."
            )

        except requests.exceptions.RequestException as error:
            raise Exception(
                f"Gemini connection error: {error}"
            )