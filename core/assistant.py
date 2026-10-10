from config.settings import (
    ASSISTANT_NAME,
    OWNER_NAME,
    VERSION,
    SYSTEM_STATUS
)

from brain.router import RequestRouter
from brain.ai_router import AIRouter
from brain.math_engine import MathEngine
from brain.formula_engine import FormulaEngine
from brain.power_manager import PowerManager

from conversation.casual_chat import CasualChat

# Support both the package layout and the root-level Piper file in this repository.
try:
    from voice.piper_tts import PiperTTS
except ModuleNotFoundError as error:
    if error.name not in {"voice", "voice.piper_tts"}:
        raise
    from piper_tts import PiperTTS

from utils.windows_control import WindowsControl


class KrishnaAssistant:
    """
    KRISHNA Main Assistant Controller.

    Handles:
        Identity
        Conversation
        Mathematics
        Known mathematical formulas
        AI mode switching
        Windows control
        Chrome profiles
        Commands
        Vision
        Security
        General AI questions
        Sleep
        Wake
        Text-to-Speech
    """

    def __init__(self):

        # =====================================================
        # BASIC INFORMATION
        # =====================================================

        self.name = ASSISTANT_NAME
        self.owner = OWNER_NAME
        self.version = VERSION
        self.status = SYSTEM_STATUS

        # =====================================================
        # SYSTEM COMPONENTS
        # =====================================================

        self.router = RequestRouter()
        self.ai_router = AIRouter()

        self.conversation = CasualChat(
            self.owner
        )

        # =====================================================
        # WINDOWS CONTROL
        # =====================================================

        self.windows_control = WindowsControl()

        # =====================================================
        # MATHEMATICS
        # =====================================================

        self.math_engine = MathEngine()

        # =====================================================
        # FORMULA ENGINE
        # =====================================================

        self.formula_engine = FormulaEngine()

        # =====================================================
        # POWER MANAGER
        # =====================================================

        self.power_manager = PowerManager()

        # =====================================================
        # TEXT-TO-SPEECH
        # =====================================================

        self.tts = PiperTTS()

    # =========================================================
    # RESPONSE HANDLER
    # =========================================================

    def _respond(self, response):
        """
        Sends KRISHNA's response to the TTS engine
        and returns the same response for normal text output.
        """

        if response is None:
            response = ""

        response = str(response).strip()

        if response:
            self.tts.speak(response)

        return response

    # =========================================================
    # AI MODE COMMAND DETECTION
    # =========================================================

    def detect_ai_mode_command(self, text):
        """
        Detect commands that switch KRISHNA between
        online and offline AI modes.
        """

        # Normalize punctuation and an optional leading wake word so
        # common speech-recognition variants still match reliably.
        text = self.remove_wake_word(text)
        text = text.lower().strip()
        text = text.rstrip(" .,!?:;")

        # -----------------------------------------------------
        # ONLINE COMMANDS
        # -----------------------------------------------------

        online_commands = [
            "switch online",
            "go online",
            "online mode",
            "switch to online",
            "switch to online mode",
            "set online",
            "set mode online",
            "use online ai",
            "use online ai mode",
            "use cloud ai",
            "connect online",
            "krishna online",
            "krishna go online",
            "krishna switch online"
        ]

        if text in online_commands:
            return "online"

        # -----------------------------------------------------
        # OFFLINE COMMANDS
        # -----------------------------------------------------

        offline_commands = [
            "switch offline",
            "go offline",
            "offline mode",
            "switch to offline",
            "switch to offline mode",
            "set offline",
            "set mode offline",
            "use offline ai",
            "use offline ai mode",
            "use local ai",
            "disconnect online",
            "krishna offline",
            "krishna go offline",
            "krishna switch offline"
        ]

        if text in offline_commands:
            return "offline"

        return None

    # =========================================================
    # REMOVE KRISHNA WAKE WORD
    # =========================================================

    def remove_wake_word(self, user_input):
        """
        Removes the spoken KRISHNA wake word from the beginning
        of a command.

        Examples:

            Krishna open Chrome
            Krishna, open Chrome

        become:

            open Chrome
        """

        text = user_input.strip()

        lower_text = text.lower()

        if lower_text.startswith("krishna, "):
            return text[9:].strip()

        if lower_text.startswith("krishna "):
            return text[8:].strip()

        return text

    # =========================================================
    # SYSTEM STATUS REPORT
    # =========================================================

    def build_status_report(self):
        """
        Return a lightweight diagnostic report without generating
        an AI response or loading a model.
        """
        lines = [
            "KRISHNA SYSTEM STATUS",
            f"Assistant: {self.name}",
            f"Version: {self.version}",
        ]

        try:
            mode = self.ai_router.get_current_mode()
            lines.append(f"AI mode: {str(mode).upper()}")
        except Exception:
            lines.append("AI mode: Unable to read configuration")

        try:
            sleeping = self.power_manager.is_sleeping()
            lines.append(
                f"Assistant state: {'SLEEPING' if sleeping else 'AWAKE'}"
            )
        except Exception:
            lines.append("Assistant state: Unable to determine")

        # A single /api/tags request checks Ollama and model availability
        # without loading a model into memory.
        try:
            status = self.ai_router.local_ai.get_status()
            if status["ollama_available"]:
                lines.append("Ollama: AVAILABLE")
                model_name = status.get("model", "configured local model")
                model_state = (
                    "INSTALLED"
                    if status["model_available"]
                    else "NOT INSTALLED"
                )
                lines.append(f"Local model ({model_name}): {model_state}")
            else:
                lines.append(
                    f"Ollama: UNAVAILABLE ({status.get('detail', 'no response')})"
                )
                lines.append("Local model: Not checked")
        except Exception:
            lines.append("Ollama/model status: Unable to check")

        try:
            profiles = self.windows_control.get_chrome_profiles()
            lines.append(f"Chrome profiles detected: {len(profiles)}")
        except Exception:
            lines.append("Chrome profiles: Unable to check")

        lines.append("Diagnostic check did not load an AI model.")
        return "\n".join(lines)

    # =========================================================
    # CHROME PROFILE COMMAND DETECTION
    # =========================================================

    def detect_chrome_profile_command(self, user_input):
        """
        Detect commands using Chrome profile names.

        Supports:

            open Madras Profile
            launch College Profile
            start Friends Profile
            use Profile 1

            open Chrome Madras Profile
            open Chrome profile of Madras Profile
            open Chrome profile of Madras

            Krishna open Chrome profile of Madras
        """

        text = self.remove_wake_word(
            user_input
        )

        text = text.strip().lower()

        profiles = self.windows_control.get_chrome_profiles()

        if not profiles:
            return None

        # =====================================================
        # CHECK EACH REAL CHROME PROFILE
        # =====================================================

        for profile_name in profiles.keys():

            profile_lower = (
                profile_name
                .strip()
                .lower()
            )

            # -------------------------------------------------
            # Direct profile commands
            # -------------------------------------------------

            direct_commands = [
                f"open {profile_lower}",
                f"launch {profile_lower}",
                f"start {profile_lower}",
                f"use {profile_lower}"
            ]

            if text in direct_commands:

                return self.windows_control.open_chrome(
                    profile_name
                )

            # -------------------------------------------------
            # Chrome + profile
            # -------------------------------------------------

            chrome_commands = [
                f"open chrome {profile_lower}",
                f"launch chrome {profile_lower}",
                f"start chrome {profile_lower}",
                f"open google chrome {profile_lower}",
                f"launch google chrome {profile_lower}",
                f"start google chrome {profile_lower}"
            ]

            if text in chrome_commands:

                return self.windows_control.open_chrome(
                    profile_name
                )

            # -------------------------------------------------
            # Chrome profile of...
            # -------------------------------------------------

            profile_of_commands = [
                f"open chrome profile of {profile_lower}",
                f"open chrome profile {profile_lower}",
                f"launch chrome profile of {profile_lower}",
                f"launch chrome profile {profile_lower}",
                f"start chrome profile of {profile_lower}",
                f"start chrome profile {profile_lower}",
                f"open google chrome profile of {profile_lower}",
                f"open google chrome profile {profile_lower}",
                f"launch google chrome profile of {profile_lower}",
                f"launch google chrome profile {profile_lower}"
            ]

            if text in profile_of_commands:

                return self.windows_control.open_chrome(
                    profile_name
                )

            # -------------------------------------------------
            # Allow "profile of Madras" when the actual profile
            # name is "Madras Profile".
            # -------------------------------------------------

            profile_without_word = profile_lower

            if profile_lower.endswith(" profile"):
                profile_without_word = (
                    profile_lower[:-8].strip()
                )

                short_profile_commands = [
                    f"open chrome profile of {profile_without_word}",
                    f"open chrome profile {profile_without_word}",
                    f"launch chrome profile of {profile_without_word}",
                    f"launch chrome profile {profile_without_word}",
                    f"start chrome profile of {profile_without_word}",
                    f"start chrome profile {profile_without_word}",
                    f"open google chrome profile of {profile_without_word}",
                    f"open google chrome profile {profile_without_word}"
                ]

                if text in short_profile_commands:

                    return self.windows_control.open_chrome(
                        profile_name
                    )

        return None

    # =========================================================
    # WINDOWS COMMAND DETECTION
    # =========================================================

    def detect_windows_command(self, user_input):
        """
        Detect Windows, Chrome, Google and YouTube commands.

        Windows commands are checked before the general AI
        router so that system actions do not get sent to Gemini
        or the local AI.
        """

        # =====================================================
        # REMOVE WAKE WORD
        # =====================================================

        text = self.remove_wake_word(
            user_input
        )

        text = text.strip()

        lower_text = text.lower()

        # =====================================================
        # CHROME PROFILE COMMANDS
        # =====================================================

        profile_response = (
            self.detect_chrome_profile_command(
                text
            )
        )

        if profile_response:
            return profile_response

        # =====================================================
        # OPEN CHROME
        # =====================================================

        if lower_text in [
            "open chrome",
            "launch chrome",
            "start chrome",
            "open google chrome",
            "launch google chrome",
            "start google chrome"
        ]:

            return self.windows_control.open_chrome()

        # =====================================================
        # OPEN GOOGLE
        # =====================================================

        if lower_text in [
            "open google",
            "launch google",
            "start google"
        ]:

            return self.windows_control.open_google()

        # =====================================================
        # OPEN YOUTUBE
        # =====================================================

        if lower_text in [
            "open youtube",
            "launch youtube",
            "start youtube"
        ]:

            return self.windows_control.open_youtube()

        # =====================================================
        # OPEN CALCULATOR
        # =====================================================

        if lower_text in [
            "open calculator",
            "launch calculator",
            "start calculator",
            "open calc",
            "launch calc",
            "start calc"
        ]:

            return self.windows_control.open_calculator()

        # =====================================================
        # OPEN NOTEPAD
        # =====================================================

        if lower_text in [
            "open notepad",
            "launch notepad",
            "start notepad"
        ]:

            return self.windows_control.open_notepad()

        # =====================================================
        # OPEN FILE EXPLORER
        # =====================================================

        if lower_text in [
            "open file explorer",
            "launch file explorer",
            "start file explorer",
            "open explorer",
            "launch explorer",
            "start explorer"
        ]:

            return self.windows_control.open_file_explorer()

        # =====================================================
        # OPEN YOUTUBE + SEARCH
        # =====================================================

        youtube_open_search_patterns = [
            "open youtube and search ",
            "open youtube and search for ",
            "launch youtube and search ",
            "launch youtube and search for ",
            "start youtube and search ",
            "start youtube and search for "
        ]

        for pattern in youtube_open_search_patterns:

            if lower_text.startswith(pattern):

                query = text[len(pattern):].strip()

                if query:
                    return (
                        self.windows_control
                        .youtube_search(
                            query
                        )
                    )

        # =====================================================
        # CHROME SEARCH
        # =====================================================

        chrome_search_patterns = [
            "open chrome and search ",
            "open chrome and type ",
            "search chrome for ",
            "search chrome ",
            "chrome search "
        ]

        for pattern in chrome_search_patterns:

            if lower_text.startswith(pattern):

                query = text[len(pattern):].strip()

                if query:
                    return (
                        self.windows_control
                        .open_chrome_and_search(
                            query
                        )
                    )

        # =====================================================
        # GOOGLE SEARCH
        # =====================================================

        google_search_patterns = [
            "search google for ",
            "search google ",
            "google search for ",
            "google search "
        ]

        for pattern in google_search_patterns:

            if lower_text.startswith(pattern):

                query = text[len(pattern):].strip()

                if query:
                    return (
                        self.windows_control
                        .google_search(
                            query
                        )
                    )

        # =====================================================
        # YOUTUBE SEARCH
        # =====================================================

        youtube_search_patterns = [
            "search youtube for ",
            "search youtube ",
            "youtube search for ",
            "youtube search "
        ]

        for pattern in youtube_search_patterns:

            if lower_text.startswith(pattern):

                query = text[len(pattern):].strip()

                if query:
                    return (
                        self.windows_control
                        .youtube_search(
                            query
                        )
                    )

        # =====================================================
        # GENERIC APPLICATION OPEN
        # =====================================================

        generic_open_patterns = [
            "open ",
            "launch ",
            "start "
        ]

        for pattern in generic_open_patterns:

            if lower_text.startswith(pattern):

                application_name = (
                    text[len(pattern):].strip()
                )

                if application_name:

                    # -----------------------------------------
                    # Do not treat Chrome profiles as generic
                    # applications.
                    # -----------------------------------------

                    profile_response = (
                        self.detect_chrome_profile_command(
                            text
                        )
                    )

                    if profile_response:
                        return profile_response

                    known_application_names = [
                        "chrome",
                        "google chrome",
                        "google",
                        "youtube",
                        "calculator",
                        "calc",
                        "notepad",
                        "file explorer",
                        "explorer"
                    ]

                    if (
                        application_name.lower()
                        not in known_application_names
                    ):

                        return (
                            self.windows_control
                            .open_application(
                                application_name
                            )
                        )

        return None

    # =========================================================
    # MAIN REQUEST PROCESSOR
    # =========================================================

    def process_request(self, user_input):

        user_input = user_input.strip()

        if not user_input:

            return self._respond(
                "Please enter a request."
            )

        text = user_input.lower().strip()

        # Status is informational, so it also works during application sleep.
        command_text = (
            self.remove_wake_word(user_input)
            .lower()
            .strip()
            .rstrip(" .,!?:;")
        )
        status_commands = {
            "status",
            "system status",
            "krishna status",
            "system check",
            "check system",
            "run diagnostics",
            "diagnostics",
            "health check",
        }
        if command_text in status_commands:
            return self._respond(self.build_status_report())

        # =====================================================
        # SLEEP COMMAND
        # =====================================================

        sleep_commands = [
            "sleep",
            "go to sleep",
            "go sleep",
            "sleep now",
            "krishna sleep",
            "krishna go to sleep"
        ]

        if text in sleep_commands:

            return self._respond(
                self.power_manager.sleep()
            )

        # =====================================================
        # WAKE COMMAND
        # =====================================================

        wake_commands = [
            "wake",
            "wake up",
            "wake up now",
            "wake krishna",
            "krishna wake",
            "krishna wake up",
            "krishna wake up now"
        ]

        if text in wake_commands:

            return self._respond(
                self.power_manager.wake()
            )

        # =====================================================
        # BLOCK NORMAL AI WHILE SLEEPING
        # =====================================================

        if self.power_manager.is_sleeping():

            return self._respond(
                "KRISHNA: I am sleeping right now.\n"
                "Say 'wake up' to wake me."
            )

        # =====================================================
        # AI MODE SWITCHING
        # =====================================================

        ai_mode = self.detect_ai_mode_command(
            text
        )

        if ai_mode == "online":

            result = self.ai_router.switch_mode(
                "online"
            )

            result = result.replace(
                "KRISHNA: KRISHNA:",
                "KRISHNA:"
            )

            return self._respond(
                result
            )

        if ai_mode == "offline":

            result = self.ai_router.switch_mode(
                "offline"
            )

            result = result.replace(
                "KRISHNA: KRISHNA:",
                "KRISHNA:"
            )

            return self._respond(
                result
            )

        # =====================================================
        # WINDOWS CONTROL
        # =====================================================
        #
        # IMPORTANT:
        #
        # Windows commands are checked BEFORE the normal
        # intent router.
        #
        # This prevents commands such as:
        #
        #   Krishna open Chrome profile of Madras
        #
        # from being sent to the AI.
        # =====================================================

        windows_response = (
            self.detect_windows_command(
                user_input
            )
        )

        if windows_response:

            return self._respond(
                windows_response
            )

        # =====================================================
        # FORMULA ENGINE
        # =====================================================

        formula_response = (
            self.formula_engine.solve(
                user_input
            )
        )

        if formula_response:

            return self._respond(
                formula_response
            )

        # =====================================================
        # NORMAL INTENT ROUTING
        # =====================================================

        intent = self.router.route_request(
            user_input
        )

        # =====================================================
        # IDENTITY
        # =====================================================

        if intent == "identity":

            return self._respond(
                self.handle_identity(
                    user_input
                )
            )

        # =====================================================
        # CONVERSATION
        # =====================================================

        elif intent == "conversation":

            return self._respond(
                self.ai_router.get_response(
                    user_input
                )
            )

        # =====================================================
        # MATHEMATICS
        # =====================================================

        elif intent == "math":

            return self._respond(
                self.math_engine.solve(
                    user_input
                )
            )

        # =====================================================
        # COMMAND
        # =====================================================

        elif intent == "command":

            return self._respond(
                "I understand you want me to perform "
                "a system action. "
                "My automation system will handle this."
            )

        # =====================================================
        # VISION
        # =====================================================

        elif intent == "vision":

            return self._respond(
                "I understand this is related to "
                "screen or visual analysis. "
                "My vision system will handle this."
            )

        # =====================================================
        # SECURITY
        # =====================================================

        elif intent == "security":

            return self._respond(
                "This is a security-sensitive request. "
                "Authentication will be required."
            )

        # =====================================================
        # GENERAL AI
        # =====================================================

        else:

            return self._respond(
                self.ai_router.get_response(
                    user_input
                )
            )

    # =========================================================
    # IDENTITY HANDLER
    # =========================================================

    def handle_identity(self, user_input):

        text = user_input.lower()

        # -----------------------------------------------------
        # MASTER / OWNER
        # -----------------------------------------------------

        if (
            "master" in text
            or "owner" in text
            or "owns you" in text
        ):

            return (
                f"My master and owner is "
                f"{self.owner}."
            )

        # -----------------------------------------------------
        # CREATOR
        # -----------------------------------------------------

        elif "created" in text:

            return (
                f"I am being developed by "
                f"{self.owner}."
            )

        # -----------------------------------------------------
        # NAME
        # -----------------------------------------------------

        elif "name" in text:

            return (
                f"My name is "
                f"{self.name}."
            )

        # -----------------------------------------------------
        # DEFAULT
        # -----------------------------------------------------

        return (
            f"I am {self.name}, "
            f"your AI assistant."
        )