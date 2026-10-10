import json
import os


class AIModeManager:
    """
    Manages KRISHNA's AI operating mode
    and AI model configuration.
    """

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.config_path = os.path.join(
            base_dir,
            "config",
            "ai_config.json"
        )

        self.config = self.load_config()


    def load_config(self):

        with open(self.config_path, "r") as file:

            return json.load(file)


    def save_config(self):

        with open(self.config_path, "w") as file:

            json.dump(
                self.config,
                file,
                indent=4
            )


    def get_mode(self):

        return self.config.get(
            "mode",
            "online"
        )


    def set_mode(self, mode):

        mode = mode.lower()

        if mode not in ["online", "offline"]:

            return False

        self.config["mode"] = mode

        self.save_config()

        return True


    def get_cloud_ai(self):

        return self.config.get(
            "cloud_ai",
            "gemini"
        )


    def get_local_ai(self):

        return self.config.get(
            "local_ai",
            "ollama"
        )


    def get_local_model(self):

        return self.config.get(
            "local_model",
            "qwen2.5:1.5b"
        )


    def get_vision_model(self):

        return self.config.get(
            "vision_model",
            "qwen3-vl:2b"
        )