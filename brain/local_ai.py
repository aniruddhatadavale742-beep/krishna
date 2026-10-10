import requests


class LocalAI:
    """
    KRISHNA's local/offline AI using Ollama.

    Normal local model:
        qwen2.5:1.5b

    The model is unloaded automatically after every response
    to reduce RAM usage.
    """

    def __init__(self):

        # -----------------------------
        # OLLAMA CONFIGURATION
        # -----------------------------

        self.model = "qwen2.5:1.5b"

        self.base_url = "http://localhost:11434"

        self.tags_url = f"{self.base_url}/api/tags"

        self.generate_url = f"{self.base_url}/api/generate"

        # Maximum time to wait for Ollama itself
        self.connection_timeout = 5

        # Maximum time to wait for model response
        self.response_timeout = 120


    # =========================================================
    # CHECK OLLAMA
    # =========================================================

    def is_available(self):
        """
        Check whether Ollama is running.
        """

        try:

            response = requests.get(
                self.tags_url,
                timeout=self.connection_timeout
            )

            return response.status_code == 200

        except requests.exceptions.RequestException:

            return False


    # =========================================================
    # CHECK MODEL
    # =========================================================

    def model_available(self):
        """
        Check whether the configured local model
        is actually installed in Ollama.
        """

        try:

            response = requests.get(
                self.tags_url,
                timeout=self.connection_timeout
            )

            response.raise_for_status()

            data = response.json()

            models = data.get("models", [])

            for model in models:

                if model.get("name") == self.model:
                    return True

            return False

        except requests.exceptions.RequestException:

            return False

        except (ValueError, TypeError):

            return False


    # =====================================================
    # LIGHTWEIGHT STATUS CHECK
    # =====================================================

    def get_status(self):
        """
        Check Ollama and the configured model with one /api/tags
        request. This does not load the model into memory.
        """
        try:
            response = requests.get(
                self.tags_url,
                timeout=min(self.connection_timeout, 2)
            )
            response.raise_for_status()
            data = response.json()
            models = data.get("models", [])

            installed_names = {
                item.get("name")
                for item in models
                if isinstance(item, dict) and item.get("name")
            }

            return {
                "ollama_available": True,
                "model": self.model,
                "model_available": self.model in installed_names,
                "detail": "responding",
            }

        except requests.exceptions.Timeout:
            detail = "request timed out"
        except requests.exceptions.RequestException:
            detail = "could not connect"
        except (ValueError, TypeError, AttributeError):
            detail = "invalid response"

        return {
            "ollama_available": False,
            "model": self.model,
            "model_available": False,
            "detail": detail,
        }

    # =====================================================
    # GENERATE RESPONSE
    # =========================================================

    def generate_response(self, prompt):
        """
        Generate a response using the local Qwen model.

        The model is automatically unloaded after the response.
        """

        # -----------------------------
        # CHECK OLLAMA
        # -----------------------------

        if not self.is_available():

            return (
                "KRISHNA: Offline AI is unavailable. "
                "Please make sure Ollama is running."
            )


        # -----------------------------
        # CHECK MODEL
        # -----------------------------

        if not self.model_available():

            return (
                f"KRISHNA: My local model "
                f"'{self.model}' is not installed in Ollama."
            )


        # -----------------------------
        # PREPARE REQUEST
        # -----------------------------

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            # Automatically unload model
            # after generating the response.
            "keep_alive": 0,

            "options": {

                # Keep responses reasonably fast
                "temperature": 0.7,

                # Prevent unnecessarily huge answers
                "num_predict": 512
            }
        }


        # -----------------------------
        # SEND REQUEST
        # -----------------------------

        try:

            response = requests.post(

                self.generate_url,

                json=payload,

                timeout=self.response_timeout
            )

            response.raise_for_status()

            data = response.json()


            # -----------------------------
            # GET RESPONSE
            # -----------------------------

            answer = data.get("response", "").strip()


            if not answer:

                return (
                    "KRISHNA: The local AI returned "
                    "an empty response."
                )


            return answer


        # -----------------------------
        # TIMEOUT
        # -----------------------------

        except requests.exceptions.Timeout:

            return (
                "KRISHNA: The local AI took too long "
                "to respond. The request was stopped "
                "to protect system resources."
            )


        # -----------------------------
        # CONNECTION ERROR
        # -----------------------------

        except requests.exceptions.ConnectionError:

            return (
                "KRISHNA: I cannot connect to Ollama. "
                "Please make sure Ollama is running."
            )


        # -----------------------------
        # OTHER REQUEST ERROR
        # -----------------------------

        except requests.exceptions.RequestException as error:

            return (
                f"KRISHNA: Offline AI Error: {error}"
            )


        # -----------------------------
        # INVALID JSON
        # -----------------------------

        except ValueError:

            return (
                "KRISHNA: Ollama returned an invalid response."
            )