import subprocess
import requests


class PowerManager:
    """
    KRISHNA Power Manager.

    Sleep:
        - Finds currently running Ollama models.
        - Stops only the models that are actually loaded.
        - Keeps KRISHNA itself running.

    Wake:
        - Wakes KRISHNA from sleep.
        - Does NOT load any AI model immediately.
        - Models are loaded automatically when an AI request
          is made.

    This design is intended to reduce RAM and CPU usage.
    """

    def __init__(self):

        self.ollama_url = "http://localhost:11434"

        self.ps_url = (
            f"{self.ollama_url}/api/ps"
        )

        self.tags_url = (
            f"{self.ollama_url}/api/tags"
        )

        self.sleeping = False

    # =========================================================
    # CHECK SLEEP STATE
    # =========================================================

    def is_sleeping(self):

        return self.sleeping

    # =========================================================
    # GET RUNNING OLLAMA MODELS
    # =========================================================

    def get_running_models(self):

        try:

            response = requests.get(
                self.ps_url,
                timeout=3
            )

            response.raise_for_status()

            data = response.json()

            models = data.get(
                "models",
                []
            )

            running_models = []

            for model in models:

                name = model.get(
                    "name"
                )

                if name:
                    running_models.append(
                        name
                    )

            return running_models

        except (
            requests.exceptions.RequestException,
            ValueError,
            TypeError
        ):

            return []

    # =========================================================
    # STOP ONE OLLAMA MODEL
    # =========================================================

    def stop_model(self, model_name):

        try:

            result = subprocess.run(
                [
                    "ollama",
                    "stop",
                    model_name
                ],
                capture_output=True,
                text=True,
                timeout=15
            )

            return result.returncode == 0

        except (
            subprocess.TimeoutExpired,
            FileNotFoundError,
            OSError
        ):

            return False

    # =========================================================
    # SLEEP
    # =========================================================

    def sleep(self):

        if self.sleeping:

            return (
                "KRISHNA: I am already sleeping."
            )

        running_models = (
            self.get_running_models()
        )

        stopped_models = []
        failed_models = []

        # -----------------------------------------------------
        # Stop only models that are currently loaded
        # -----------------------------------------------------

        for model in running_models:

            if self.stop_model(model):

                stopped_models.append(
                    model
                )

            else:

                failed_models.append(
                    model
                )

        # -----------------------------------------------------
        # Enter sleep state
        # -----------------------------------------------------

        self.sleeping = True

        # -----------------------------------------------------
        # Response
        # -----------------------------------------------------

        if stopped_models:

            models_text = ", ".join(
                stopped_models
            )

            if failed_models:

                failed_text = ", ".join(
                    failed_models
                )

                return (
                    "KRISHNA: Going to sleep now.\n"
                    f"Unloaded: {models_text}\n"
                    f"Could not unload: {failed_text}\n"
                    "KRISHNA itself is still running."
                )

            return (
                "KRISHNA: Going to sleep now.\n"
                f"Unloaded: {models_text}\n"
                "AI models are no longer running."
            )

        # -----------------------------------------------------
        # No models were loaded
        # -----------------------------------------------------

        if failed_models:

            failed_text = ", ".join(
                failed_models
            )

            return (
                "KRISHNA: Going to sleep now.\n"
                f"Could not unload: {failed_text}\n"
                "KRISHNA itself is still running."
            )

        return (
            "KRISHNA: Going to sleep now.\n"
            "No AI models were running, so there was "
            "nothing to unload.\n"
            "KRISHNA itself is still running."
        )

    # =========================================================
    # CHECK OLLAMA
    # =========================================================

    def ollama_available(self):

        try:

            response = requests.get(
                self.tags_url,
                timeout=3
            )

            return response.status_code == 200

        except requests.exceptions.RequestException:

            return False

    # =========================================================
    # WAKE
    # =========================================================

    def wake(self):

        if not self.sleeping:

            return (
                "KRISHNA: I am already awake."
            )

        self.sleeping = False

        # -----------------------------------------------------
        # Important:
        #
        # We DO NOT load a model here.
        #
        # Ollama will load the required model when
        # the next AI request is made.
        # -----------------------------------------------------

        if self.ollama_available():

            return (
                "KRISHNA: I am awake now.\n"
                "AI models will be loaded only when needed."
            )

        return (
            "KRISHNA: I am awake now.\n"
            "Ollama is not currently available. "
            "AI models will work once Ollama is running."
        )