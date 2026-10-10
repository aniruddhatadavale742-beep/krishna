import json
import os
import re
import subprocess
import webbrowser
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


class WindowsControl:
    def __init__(self):
        self.chrome_paths = [
            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
            ),
        ]

        self.chrome_user_data = os.path.expandvars(
            r"%LocalAppData%\Google\Chrome\User Data"
        )

    # =========================================================
    # CHROME
    # =========================================================

    def find_chrome(self):
        """
        Find the installed Google Chrome executable.
        """
        for path in self.chrome_paths:
            if os.path.exists(path):
                return path

        # Extra fallback: ask Windows where chrome.exe is.
        try:
            result = subprocess.run(
                ["where", "chrome.exe"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    path = line.strip()
                    if os.path.exists(path):
                        return path

        except Exception:
            pass

        return None

    def get_chrome_profiles(self):
        """
        Read Chrome's Local State file and return:

        {
            "Profile 1": "Profile 1",
            "Madras Profile": "Profile 2",
            ...
        }

        Key   = friendly profile name
        Value = Chrome internal profile directory
        """

        local_state_path = os.path.join(
            self.chrome_user_data,
            "Local State"
        )

        if not os.path.exists(local_state_path):
            return {}

        try:
            with open(
                local_state_path,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            profile_info = (
                data
                .get("profile", {})
                .get("info_cache", {})
            )

            profiles = {}

            for directory_name, info in profile_info.items():
                if not isinstance(info, dict):
                    continue

                profile_name = info.get("name")

                if profile_name:
                    profiles[profile_name] = directory_name

            return profiles

        except (
            OSError,
            json.JSONDecodeError,
            UnicodeDecodeError,
            TypeError,
            AttributeError
        ):
            return {}

    def normalize_profile_name(self, name):
        """
        Normalize names so voice commands are easier to match.
        """
        name = str(name).lower().strip()

        name = re.sub(
            r"\s+",
            " ",
            name
        )

        return name

    def find_chrome_profile(self, requested_name):
        """
        Find a Chrome profile by its visible name.

        Example:
            Madras Profile
            madras profile
            MADRAS PROFILE

        all resolve to the same Chrome profile.
        """

        requested_name = self.normalize_profile_name(
            requested_name
        )

        if not requested_name:
            return None

        profiles = self.get_chrome_profiles()

        # Exact match first.
        for profile_name, directory_name in profiles.items():
            if self.normalize_profile_name(profile_name) == requested_name:
                return directory_name

        # Then allow partial matching.
        for profile_name, directory_name in profiles.items():
            normalized = self.normalize_profile_name(profile_name)

            if requested_name in normalized:
                return directory_name

        return None

    def list_chrome_profiles(self):
        """
        Return a human-readable list of Chrome profiles.
        """

        profiles = self.get_chrome_profiles()

        if not profiles:
            return (
                "KRISHNA: I could not find any Chrome profiles."
            )

        names = list(profiles.keys())

        return (
            "KRISHNA: Your Chrome profiles are: "
            + ", ".join(names)
            + "."
        )

    def _launch_chrome(self, url=None, profile_name=None):
        """
        Launch Chrome directly.

        IMPORTANT:
        We do NOT use webbrowser.open() here.
        This prevents Windows from sending the request to Edge.
        """

        chrome_path = self.find_chrome()

        if not chrome_path:
            return (
                "KRISHNA: Google Chrome was not found "
                "on this computer."
            )

        command = [chrome_path]

        # If a profile was requested, resolve its internal folder.
        if profile_name:
            profile_directory = self.find_chrome_profile(
                profile_name
            )

            if not profile_directory:
                profiles = self.get_chrome_profiles()

                if profiles:
                    available = ", ".join(profiles.keys())

                    return (
                        f"KRISHNA: I could not find the Chrome "
                        f"profile '{profile_name}'. "
                        f"Available profiles are: {available}."
                    )

                return (
                    "KRISHNA: I could not read your Chrome profiles."
                )

            command.append(
                f"--profile-directory={profile_directory}"
            )

        if url:
            command.append(url)

        try:
            subprocess.Popen(command)

            if profile_name:
                if url:
                    return (
                        f"KRISHNA: Opening {profile_name} "
                        "in Chrome, sir."
                    )

                return (
                    f"KRISHNA: Opening Chrome with "
                    f"{profile_name}, sir."
                )

            if url:
                return "KRISHNA: Opening Chrome, sir."

            return "KRISHNA: Opening Chrome, sir."

        except Exception as error:
            return (
                f"KRISHNA: I could not open Chrome. "
                f"{error}"
            )

    def open_chrome(self, profile_name=None):
        return self._launch_chrome(
            profile_name=profile_name
        )

    def open_chrome_and_search(
        self,
        query,
        profile_name=None
    ):
        query = query.strip()

        if not query:
            return (
                "KRISHNA: What should I search for?"
            )

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        return self._launch_chrome(
            url=url,
            profile_name=profile_name
        )

    # =========================================================
    # GOOGLE
    # =========================================================

    def open_google(self, profile_name=None):
        return self._launch_chrome(
            url="https://www.google.com",
            profile_name=profile_name
        )

    def google_search(
        self,
        query,
        profile_name=None
    ):
        query = query.strip()

        if not query:
            return (
                "KRISHNA: What should I search for?"
            )

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        return self._launch_chrome(
            url=url,
            profile_name=profile_name
        )

    # =========================================================
    # YOUTUBE
    # =========================================================

    def open_youtube(self, profile_name=None):
        return self._launch_chrome(
            url="https://www.youtube.com",
            profile_name=profile_name
        )

    def youtube_search(
        self,
        query,
        profile_name=None
    ):
        query = query.strip()

        if not query:
            return (
                "KRISHNA: What should I search for on YouTube?"
            )

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

        return self._launch_chrome(
            url=url,
            profile_name=profile_name
        )

    # =========================================================
    # WINDOWS APPLICATIONS
    # =========================================================

    def open_calculator(self):
        try:
            subprocess.Popen(["calc.exe"])

            return (
                "KRISHNA: Opening Calculator, sir."
            )

        except Exception as error:
            return (
                f"KRISHNA: I could not open Calculator. "
                f"{error}"
            )

    def open_notepad(self):
        try:
            subprocess.Popen(["notepad.exe"])

            return (
                "KRISHNA: Opening Notepad, sir."
            )

        except Exception as error:
            return (
                f"KRISHNA: I could not open Notepad. "
                f"{error}"
            )

    def open_file_explorer(self):
        try:
            subprocess.Popen(["explorer.exe"])

            return (
                "KRISHNA: Opening File Explorer, sir."
            )

        except Exception as error:
            return (
                f"KRISHNA: I could not open File Explorer. "
                f"{error}"
            )

    def open_application(self, application_name):
        application_name = application_name.strip()

        if not application_name:
            return (
                "KRISHNA: Please tell me which "
                "application to open."
            )

        key = application_name.lower().strip()

        known_apps = {
            "chrome": self.open_chrome,
            "google chrome": self.open_chrome,
            "calculator": self.open_calculator,
            "calc": self.open_calculator,
            "notepad": self.open_notepad,
            "file explorer": self.open_file_explorer,
            "explorer": self.open_file_explorer,
        }

        if key in known_apps:
            return known_apps[key]()

        try:
            safe_name = application_name.replace(
                "'",
                "''"
            )

            command = (
                "$app = Get-StartApps | "
                f"Where-Object {{$_.Name -like '*{safe_name}*'}} | "
                "Select-Object -First 1; "
                "if ($app) { "
                "Start-Process "
                "('shell:AppsFolder\\' + $app.AppID); "
                "Write-Output 'FOUND' "
                "} else { "
                "Write-Output 'NOT_FOUND' "
                "}"
            )

            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    command
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if "FOUND" in result.stdout:
                return (
                    f"KRISHNA: Opening "
                    f"{application_name}, sir."
                )

            return (
                f"KRISHNA: I could not find "
                f"{application_name} in Windows."
            )

        except Exception as error:
            return (
                f"KRISHNA: I could not open "
                f"{application_name}. {error}"
            )

    # =========================================================
    # WEB SEARCH + SUMMARY
    # =========================================================

    def search_web_and_summarize(self, query):
        query = query.strip()

        if not query:
            return (
                "KRISHNA: What should I search for?"
            )

        search_url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0 Safari/537.36"
            )
        }

        try:
            response = requests.get(
                search_url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            results = []

            for block in soup.select("div.MjjYud"):
                text = block.get_text(
                    " ",
                    strip=True
                )

                if not text:
                    continue

                text = re.sub(
                    r"\s+",
                    " ",
                    text
                )

                if len(text) > 400:
                    text = text[:400] + "..."

                results.append(text)

                if len(results) >= 3:
                    break

            if not results:
                return (
                    f"KRISHNA: I searched for {query}, "
                    "but I could not extract the "
                    "search results."
                )

            summary = (
                f"KRISHNA: I searched the web for "
                f"{query}. Here is what I found:\n"
            )

            for index, result in enumerate(
                results,
                start=1
            ):
                summary += (
                    f"\n{index}. {result}"
                )

            return summary

        except requests.exceptions.Timeout:
            return (
                "KRISHNA: The web search took "
                "too long to respond."
            )

        except requests.exceptions.ConnectionError:
            return (
                "KRISHNA: I cannot reach the "
                "internet right now."
            )

        except requests.exceptions.RequestException as error:
            return (
                f"KRISHNA: Web search error: {error}"
            )

        except Exception as error:
            return (
                f"KRISHNA: I could not process "
                f"the web results. {error}"
            )