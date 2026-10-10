import base64
import io
import os
import requests

from PIL import Image

from brain.ai_mode_manager import AIModeManager


class VisionAI:
    """
    KRISHNA's local visual AI system.

    Optimized for low-power laptops.

    Supports:
    - Local image files
    - Image URLs
    - Screenshots
    - Image analysis
    - OCR and text reading
    """

    def __init__(self):

        self.mode_manager = AIModeManager()

        self.model = self.mode_manager.get_vision_model()

        self.api_url = "http://localhost:11434/api/generate"


    def ollama_available(self):
        """
        Check whether Ollama is running.
        """

        try:

            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=5
            )

            return response.status_code == 200

        except requests.RequestException:

            return False


    def is_url(self, path):
        """
        Check whether input is an internet URL.
        """

        return (
            path.startswith("http://")
            or path.startswith("https://")
        )


    def encode_image(self, image_path, max_size=512):
        """
        Load, resize, compress and convert image to Base64.

        Default 512px is optimized for KRISHNA's laptop.
        """

        image_path = image_path.strip().strip('"').strip("'")

        try:

            # =====================================
            # LOAD IMAGE FROM URL
            # =====================================

            if self.is_url(image_path):

                response = requests.get(
                    image_path,
                    timeout=30
                )

                response.raise_for_status()

                image_data = response.content

                image = Image.open(
                    io.BytesIO(image_data)
                )


            # =====================================
            # LOAD LOCAL IMAGE
            # =====================================

            else:

                if not os.path.exists(image_path):

                    return None

                image = Image.open(image_path)


            # Convert image to RGB

            if image.mode != "RGB":

                image = image.convert("RGB")


            # =====================================
            # RESIZE IMAGE
            # =====================================

            width, height = image.size

            if width > max_size or height > max_size:

                image.thumbnail(
                    (max_size, max_size)
                )


            # =====================================
            # COMPRESS IMAGE
            # =====================================

            buffer = io.BytesIO()

            image.save(
                buffer,
                format="JPEG",
                quality=75,
                optimize=True
            )

            image_data = buffer.getvalue()


            # Convert to Base64

            encoded_image = base64.b64encode(
                image_data
            ).decode("utf-8")

            return encoded_image


        except Exception as error:

            print(
                f"Image loading error: {error}"
            )

            return None


    def analyze_image(
        self,
        image_path,
        user_prompt,
        detailed=False
    ):
        """
        Analyze an image using Qwen3-VL.

        detailed=False → Faster, lower CPU usage
        detailed=True  → Better detail, higher CPU usage
        """

        # Check Ollama

        if not self.ollama_available():

            return (
                "Vision AI Error: Ollama is not running."
            )


        # =====================================
        # SELECT IMAGE QUALITY
        # =====================================

        if detailed:

            max_size = 1024

        else:

            # Optimized for your laptop
            max_size = 512


        # Load and process image

        encoded_image = self.encode_image(
            image_path,
            max_size
        )

        if not encoded_image:

            return (
                "Vision AI Error: Unable to read "
                "or download the image."
            )


        # =====================================
        # PREPARE AI REQUEST
        # =====================================

        payload = {

            "model": self.model,

            "prompt": (
                "You are KRISHNA's visual intelligence system. "
                "Analyze the provided image carefully. "
                "Give a clear and concise answer. "
                "Do not provide unnecessary long descriptions. "
                f"User request: {user_prompt}"
            ),

            "images": [
                encoded_image
            ],

            "stream": False,

            # Unload model immediately after response
            "keep_alive": 0
        }


        try:

            if detailed:

                print(
                    "Vision model is processing in detailed mode. "
                    "This may take several minutes..."
                )

            else:

                print(
                    "Vision model is processing in optimized mode..."
                )


            response = requests.post(
                self.api_url,
                json=payload,

                # Maximum safety timeout
                timeout=600
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "I could not generate a visual analysis."
            )


        except requests.Timeout:

            return (
                "Vision AI Error: The visual model took more "
                "than 10 minutes to respond."
            )


        except requests.RequestException as error:

            return (
                f"Vision AI Error: {error}"
            )