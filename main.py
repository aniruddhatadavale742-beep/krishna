from core.assistant import KrishnaAssistant
from utils.code_handler import CodeHandler

import speech_recognition as sr


# ============================================================
# VOICE INPUT SYSTEM
# ============================================================

class VoiceInput:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        # Makes conversation feel more natural
        self.recognizer.pause_threshold = 0.8

        # Small amount of silence allowed around speech
        self.recognizer.non_speaking_duration = 0.5

        # Maximum time to wait for someone to start speaking
        self.listen_timeout = 5

        # Maximum length of one spoken request
        self.phrase_time_limit = 15

    def listen(self):

        try:

            with sr.Microphone() as source:

                print("\nKRISHNA: Listening...")

                # Adjust for background noise
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=self.listen_timeout,
                    phrase_time_limit=self.phrase_time_limit
                )

            print("KRISHNA: Processing voice...")

            text = self.recognizer.recognize_google(
                audio
            )

            text = text.strip()

            if text:
                print(f"You: {text}")
                return text

            return None

        except sr.WaitTimeoutError:

            print(
                "KRISHNA: I didn't hear anything."
            )

            return None

        except sr.UnknownValueError:

            print(
                "KRISHNA: I couldn't understand that."
            )

            return None

        except sr.RequestError as error:

            print(
                "KRISHNA: Voice recognition service "
                "is unavailable."
            )

            print(
                f"Voice recognition error: {error}"
            )

            return None

        except Exception as error:

            print(
                "KRISHNA: Microphone error:"
            )

            print(error)

            return None


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # --------------------------------------------------------
    # INITIALIZE KRISHNA
    # --------------------------------------------------------

    assistant = KrishnaAssistant()

    # ========================================================
    # CHROME PROFILE TEST
    # ========================================================

    try:

        print("\nChecking Chrome profiles...")

        chrome_profiles = (
            assistant.windows_control.list_chrome_profiles()
        )

        print(chrome_profiles)

    except Exception as error:

        print(
            "KRISHNA: Could not read Chrome profiles."
        )

        print(
            f"Chrome profile error: {error}"
        )

    # --------------------------------------------------------
    # CODE GENERATION / FILE HANDLING SYSTEM
    # --------------------------------------------------------

    code_handler = CodeHandler()

    # --------------------------------------------------------
    # VOICE INPUT SYSTEM
    # --------------------------------------------------------

    voice_input = VoiceInput()

    # --------------------------------------------------------
    # DEFAULT INPUT MODE
    # --------------------------------------------------------

    # KRISHNA starts in voice mode automatically.
    input_mode = "voice"

    # --------------------------------------------------------
    # KRISHNA HEADER
    # --------------------------------------------------------

    print("=" * 55)
    print(f"              {assistant.name} AI ASSISTANT")
    print("=" * 55)

    print(f"\nVersion: {assistant.version}")
    print(f"Owner: {assistant.owner}")
    print(f"Status: {assistant.status}")

    print("\nSystem initialized successfully.")

    print("\nKRISHNA is in VOICE MODE.")
    print("Say 'shift text mode' to use keyboard input.")
    print("Say 'shift voice mode' to return to voice.")
    print("Say 'exit' to shut down KRISHNA.")

    print("")

    # --------------------------------------------------------
    # MAIN CONVERSATION LOOP
    # --------------------------------------------------------

    while True:

        try:

            # =================================================
            # VOICE MODE
            # =================================================

            if input_mode == "voice":

                user_input = voice_input.listen()

                # ---------------------------------------------
                # If speech was not recognized
                # ---------------------------------------------

                if not user_input:

                    # Stay in voice mode.
                    # Do NOT ask T/V again.
                    continue

            # =================================================
            # TEXT MODE
            # =================================================

            else:

                user_input = input(
                    "\nYou: "
                ).strip()

                # Ignore empty input
                if not user_input:

                    continue

            # ------------------------------------------------
            # CLEAN INPUT
            # ------------------------------------------------

            text = user_input.lower().strip()

            # =================================================
            # SWITCH TO TEXT MODE
            # =================================================

            if text in [
                "shift text mode",
                "switch text mode",
                "go to text mode",
                "text mode",
                "use text mode",
                "switch to text"
            ]:

                input_mode = "text"

                print(
                    "\nKRISHNA: Switching to text mode."
                )

                print(
                    "KRISHNA: Type your messages now."
                )

                continue

            # =================================================
            # SWITCH TO VOICE MODE
            # =================================================

            if text in [
                "shift voice mode",
                "switch voice mode",
                "go to voice mode",
                "voice mode",
                "use voice mode",
                "switch to voice"
            ]:

                input_mode = "voice"

                print(
                    "\nKRISHNA: Switching to voice mode."
                )

                continue

            # =================================================
            # EXIT COMMAND
            # =================================================

            if text in [
                "exit",
                "quit",
                "shutdown",
                "goodbye",
                "shut down krishna",
                "close krishna"
            ]:

                print(
                    "\nKRISHNA: Goodbye! "
                    "Shutting down..."
                )

                break

            # =================================================
            # PROCESS USER REQUEST
            # =================================================

            print(
                "KRISHNA: Thinking..."
            )

            response = assistant.process_request(
                user_input
            )

            # =================================================
            # HANDLE GENERATED CODE
            # =================================================

            response = code_handler.process_response(
                response
            )

            # =================================================
            # DISPLAY RESPONSE
            # =================================================

            print(
                f"\nKRISHNA: {response}\n"
            )

            # =================================================
            # CONTINUE CONVERSATION
            # =================================================

            if input_mode == "voice":

                print(
                    "KRISHNA: Ready."
                )

            # In text mode, the next loop automatically
            # waits for keyboard input.

        # ----------------------------------------------------
        # CTRL + C
        # ----------------------------------------------------

        except KeyboardInterrupt:

            print(
                "\n\nKRISHNA: Shutdown requested."
            )

            break

        # ----------------------------------------------------
        # UNEXPECTED ERROR
        # ----------------------------------------------------

        except Exception as error:

            print(
                "\nKRISHNA ERROR:"
            )

            print(
                f"{error}\n"
            )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()