import os
import subprocess
import sys
import tempfile
import threading
import time
import winsound

import speech_recognition as sr


class PiperTTS:
    """
    KRISHNA Text-to-Speech using Piper.

    Voice:
        en_US-joe-medium

    Features:
        - Same voice for online and offline AI
        - Low resource usage
        - Temporary WAV files
        - Voice interruption using "stop"
        - TTS does NOT depend on internet
        - Speech recognition for STOP is optional
    """

    def __init__(self):

        # =====================================================
        # PIPER SETTINGS
        # =====================================================

        self.voice_name = "en_US-joe-medium"

        self.voice_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Voice speed
        self.length_scale = "1.10"

        # Pause between sentences
        self.sentence_silence = "0.20"

        # =====================================================
        # SPEECH STATE
        # =====================================================

        self.speaking = False
        self.stop_requested = False

        # Prevent multiple TTS playback sessions
        self.speak_lock = threading.Lock()

        # =====================================================
        # STOP LISTENER
        # =====================================================

        self.stop_listener = None

        self.stop_recognizer = sr.Recognizer()

        self.stop_recognizer.pause_threshold = 0.5
        self.stop_recognizer.non_speaking_duration = 0.3

        self.microphone = None

    # =========================================================
    # START STOP LISTENER
    # =========================================================

    def _start_stop_listener(self):

        self.stop_requested = False

        try:

            self.microphone = sr.Microphone()

            # -------------------------------------------------
            # Calibrate microphone
            # -------------------------------------------------

            with self.microphone as source:

                self.stop_recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.2
                )

            # -------------------------------------------------
            # Start background listener
            # -------------------------------------------------

            self.stop_listener = (
                self.stop_recognizer.listen_in_background(
                    self.microphone,
                    self._check_for_stop,
                    phrase_time_limit=2
                )
            )

        except Exception as error:

            # IMPORTANT:
            # Failure of the STOP listener must NEVER
            # prevent Piper from speaking.

            print(
                f"KRISHNA: Stop listener unavailable: {error}"
            )

            self.stop_listener = None

    # =========================================================
    # CHECK FOR STOP COMMAND
    # =========================================================

    def _check_for_stop(
        self,
        recognizer,
        audio
    ):

        # If Joe has already stopped speaking,
        # don't process anything.
        if not self.speaking:

            return

        try:

            text = recognizer.recognize_google(
                audio
            )

            text = text.lower().strip()

            stop_commands = [
                "stop",
                "stop speaking",
                "stop talking",
                "be quiet",
                "quiet",
                "shut up"
            ]

            if text in stop_commands:

                print(
                    "\nKRISHNA: Speech interrupted."
                )

                self.stop_requested = True

                # -------------------------------------------------
                # Stop Windows audio immediately
                # -------------------------------------------------

                try:

                    winsound.PlaySound(
                        None,
                        winsound.SND_PURGE
                    )

                except Exception:

                    pass

        except sr.UnknownValueError:

            # Normal speech/noise that wasn't understood.
            pass

        except sr.RequestError:

            # -------------------------------------------------
            # IMPORTANT:
            # Google recognition unavailable.
            #
            # This happens when offline.
            #
            # DO NOT stop Piper.
            # Joe must continue speaking.
            # -------------------------------------------------

            pass

        except Exception:

            pass

    # =========================================================
    # STOP BACKGROUND LISTENER
    # =========================================================

    def _stop_stop_listener(self):

        if self.stop_listener is not None:

            try:

                self.stop_listener(
                    wait_for_stop=False
                )

            except Exception:

                pass

            self.stop_listener = None

    # =========================================================
    # STOP AUDIO
    # =========================================================

    def stop(self):

        self.stop_requested = True

        try:

            winsound.PlaySound(
                None,
                winsound.SND_PURGE
            )

        except Exception:

            pass

    # =========================================================
    # SPEAK
    # =========================================================

    def speak(self, text):

        text = str(text).strip()

        if not text:

            return False

        # -----------------------------------------------------
        # Prevent two responses speaking simultaneously
        # -----------------------------------------------------

        with self.speak_lock:

            return self._speak_internal(
                text
            )

    # =========================================================
    # INTERNAL SPEAK FUNCTION
    # =========================================================

    def _speak_internal(self, text):

        wav_file = None

        playback_thread = None

        try:

            # =================================================
            # CREATE TEMPORARY WAV FILE
            # =================================================

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp:

                wav_file = temp.name

            # =================================================
            # PIPER COMMAND
            # =================================================

            command = [
                sys.executable,
                "-m",
                "piper",
                "-m",
                self.voice_name,
                "--data-dir",
                self.voice_dir,
                "--length-scale",
                self.length_scale,
                "--sentence-silence",
                self.sentence_silence,
                "-f",
                wav_file,
                "--",
                text
            ]

            # =================================================
            # GENERATE SPEECH
            # =================================================

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120
            )

            # =================================================
            # CHECK PIPER
            # =================================================

            if result.returncode != 0:

                print(
                    "\nKRISHNA TTS Error:"
                )

                print(
                    result.stderr
                )

                return False

            # =================================================
            # VERIFY WAV FILE
            # =================================================

            if not os.path.exists(wav_file):

                print(
                    "KRISHNA TTS Error: "
                    "Piper did not create the audio file."
                )

                return False

            # =================================================
            # START SPEAKING
            # =================================================

            self.stop_requested = False
            self.speaking = True

            # =================================================
            # START STOP LISTENER
            # =================================================

            self._start_stop_listener()

            # =================================================
            # PLAY AUDIO
            # =================================================

            def play_audio():

                try:

                    winsound.PlaySound(
                        wav_file,
                        winsound.SND_FILENAME
                    )

                except Exception as error:

                    print(
                        f"KRISHNA Audio Error: {error}"
                    )

            playback_thread = threading.Thread(
                target=play_audio,
                daemon=True
            )

            playback_thread.start()

            # =================================================
            # MONITOR PLAYBACK
            # =================================================

            while playback_thread.is_alive():

                if self.stop_requested:

                    try:

                        winsound.PlaySound(
                            None,
                            winsound.SND_PURGE
                        )

                    except Exception:

                        pass

                    break

                time.sleep(0.05)

            # =================================================
            # WAIT A LITTLE FOR PLAYBACK THREAD
            # =================================================

            if playback_thread.is_alive():

                playback_thread.join(
                    timeout=1
                )

            # =================================================
            # RESULT
            # =================================================

            if self.stop_requested:

                return False

            return True

        # =====================================================
        # PIPER TIMEOUT
        # =====================================================

        except subprocess.TimeoutExpired:

            print(
                "KRISHNA TTS: "
                "Speech generation timed out."
            )

            return False

        # =====================================================
        # GENERAL ERROR
        # =====================================================

        except Exception as error:

            print(
                f"KRISHNA TTS Error: {error}"
            )

            return False

        # =====================================================
        # CLEANUP
        # =====================================================

        finally:

            self.speaking = False

            # Stop microphone listener
            self._stop_stop_listener()

            # Stop any remaining audio if requested
            if self.stop_requested:

                try:

                    winsound.PlaySound(
                        None,
                        winsound.SND_PURGE
                    )

                except Exception:

                    pass

            # Delete temporary WAV file
            if wav_file and os.path.exists(
                wav_file
            ):

                try:

                    os.remove(wav_file)

                except OSError:

                    pass