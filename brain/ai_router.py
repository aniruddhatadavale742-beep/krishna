from brain.ai_mode_manager import AIModeManager
from brain.gemini_ai import GeminiAI
from brain.local_ai import LocalAI
from utils.math_response_formatter import MathResponseFormatter


class AIRouter:
    """
    KRISHNA AI Router

    Online mode:
        Uses Gemini.

    If Gemini fails:
        Automatically falls back to local Ollama AI.

    Offline mode:
        Uses local Ollama AI.

    Mathematical AI responses:
        LaTeX-style formatting is converted into
        readable terminal mathematics.
    """

    def __init__(self):

        # -----------------------------------------------------
        # AI COMPONENTS
        # -----------------------------------------------------

        self.mode_manager = AIModeManager()

        self.gemini = GeminiAI()

        self.local_ai = LocalAI()

        # -----------------------------------------------------
        # MATHEMATICAL RESPONSE FORMATTER
        # -----------------------------------------------------

        self.math_formatter = MathResponseFormatter()

    # =========================================================
    # MAIN RESPONSE FUNCTION
    # =========================================================

    def get_response(self, user_input):

        if not user_input:
            return "KRISHNA: Please give me something to work with."

        current_mode = self.mode_manager.get_mode()

        # =====================================================
        # OFFLINE MODE
        # =====================================================

        if current_mode == "offline":

            print("KRISHNA: Using local AI...")

            response = self.local_ai.generate_response(
                user_input
            )

            return self.format_response(
                user_input,
                response
            )

        # =====================================================
        # ONLINE MODE
        # =====================================================

        if current_mode == "online":

            print("KRISHNA: Using cloud AI...")

            try:

                response = self.gemini.ask(
                    user_input
                )

                return self.format_response(
                    user_input,
                    response
                )

            except Exception as error:

                print(
                    f"KRISHNA: Cloud AI unavailable: {error}"
                )

                print(
                    "KRISHNA: Automatically switching "
                    "to local AI..."
                )

                # -------------------------------------------------
                # Save offline mode
                # -------------------------------------------------

                self.mode_manager.set_mode(
                    "offline"
                )

                response = self.local_ai.generate_response(
                    user_input
                )

                return self.format_response(
                    user_input,
                    response
                )

        # =====================================================
        # INVALID MODE
        # =====================================================

        return (
            "KRISHNA: Invalid AI mode configuration."
        )

    # =========================================================
    # RESPONSE FORMATTER
    # =========================================================

    def format_response(
        self,
        user_input,
        response
    ):
        """
        Format mathematical AI responses without
        modifying normal conversations or code responses.

        This prevents the math formatter from accidentally
        changing programming code.
        """

        if not response:

            return (
                "KRISHNA: The AI returned an empty response."
            )

        text = user_input.lower()

        # -----------------------------------------------------
        # Detect mathematical questions
        # -----------------------------------------------------

        math_keywords = [

            # General mathematics
            "math",
            "mathematics",
            "formula",
            "equation",
            "theorem",
            "calculate",
            "calculation",

            # Algebra
            "algebra",
            "quadratic",
            "polynomial",
            "factor",
            "factorize",
            "factorise",

            # Calculus
            "derivative",
            "differentiate",
            "differentiation",
            "integral",
            "integrate",
            "integration",
            "limit",
            "calculus",

            # Geometry
            "area",
            "volume",
            "perimeter",
            "radius",
            "diameter",
            "circumference",
            "triangle",
            "circle",
            "sphere",
            "cylinder",
            "cone",
            "pyramid",

            # Trigonometry
            "trigonometry",
            "trigonometric",
            "sine",
            "sin",
            "cosine",
            "cos",
            "tangent",
            "tan",

            # Statistics
            "statistics",
            "mean",
            "median",
            "mode",
            "variance",
            "probability",

            # Physics-style mathematical formulas
            "velocity formula",
            "acceleration formula",
            "force formula",
            "energy formula",
            "momentum formula",
        ]

        # -----------------------------------------------------
        # Check if this is probably mathematical
        # -----------------------------------------------------

        is_math = any(
            keyword in text
            for keyword in math_keywords
        )

        # -----------------------------------------------------
        # Also detect LaTeX in AI response
        # -----------------------------------------------------

        contains_latex = (
            "\\frac" in response
            or "\\times" in response
            or "\\sqrt" in response
            or "\\text{" in response
            or "\\[" in response
            or "\\]" in response
            or "$$" in response
            or "\\(" in response
            or "\\)" in response
        )

        # -----------------------------------------------------
        # Format only when appropriate
        # -----------------------------------------------------

        if is_math or contains_latex:

            return self.math_formatter.format(
                response
            )

        return response

    # =========================================================
    # CURRENT MODE
    # =========================================================

    def get_current_mode(self):

        return self.mode_manager.get_mode()

    # =========================================================
    # MANUAL MODE SWITCH
    # =========================================================

    def switch_mode(self, mode):

        mode = mode.lower().strip()

        # =====================================================
        # OFFLINE
        # =====================================================

        if mode == "offline":

            success = self.mode_manager.set_mode(
                "offline"
            )

            if success:

                return (
                    "KRISHNA: Got it, Aniruddha. "
                    "Switching to offline mode now."
                )

            return (
                "KRISHNA: Unable to switch "
                "to offline mode."
            )

        # =====================================================
        # ONLINE
        # =====================================================

        elif mode == "online":

            success = self.mode_manager.set_mode(
                "online"
            )

            if success:

                return (
                    "KRISHNA: Switching to online mode."
                )

            return (
                "KRISHNA: Unable to switch "
                "to online mode."
            )

        # =====================================================
        # INVALID MODE
        # =====================================================

        return (
            "KRISHNA: Invalid mode. "
            "Please choose online or offline."
        )