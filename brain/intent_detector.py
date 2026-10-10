class IntentDetector:
    """
    Detects the user's general intent.

    This is Version 1 of KRISHNA's understanding system.

    Later, this module can be upgraded to use a real
    AI language model for semantic understanding.
    """

    def detect_intent(self, user_input):

        text = user_input.lower().strip()

        # -----------------------------
        # IDENTITY
        # -----------------------------

        identity_patterns = [
            "who is your master",
            "who is your owner",
            "who owns you",
            "who created you",
            "what is your name",
            "tell me your name"
        ]

        if any(pattern in text for pattern in identity_patterns):
            return "identity"

        # -----------------------------
        # SYSTEM COMMANDS
        # -----------------------------

        command_patterns = [
            "open ",
            "close ",
            "shutdown",
            "restart",
            "start "
        ]

        if any(pattern in text for pattern in command_patterns):
            return "command"

        # -----------------------------
        # SCREEN / VISION
        # -----------------------------

        vision_patterns = [
            "look at my screen",
            "analyze my screen",
            "share my screen",
            "what is on my screen",
            "see my screen"
        ]

        if any(pattern in text for pattern in vision_patterns):
            return "vision"

        # -----------------------------
        # SECURITY
        # -----------------------------

        security_patterns = [
            "change password",
            "change my password",
            "security settings",
            "verify my identity"
        ]

        if any(pattern in text for pattern in security_patterns):
            return "security"

        # -----------------------------
        # MATHEMATICS
        # -----------------------------

        math_patterns = [
            "calculate",
            "solve",
            "integrate",
            "differentiate",
            "derivative",
            "equation",
            "matrix",
            "factor",
            "simplify",
            "limit"
        ]

        if any(pattern in text for pattern in math_patterns):
            return "math"

        # Detect simple mathematical expressions
        math_symbols = ["+", "-", "*", "/", "=", "^"]

        if any(symbol in text for symbol in math_symbols):
            return "math"

        # -----------------------------
        # CONVERSATION
        # -----------------------------

        conversation_patterns = [
            "hello",
            "hi",
            "how are you",
            "i am tired",
            "i'm tired",
            "i feel tired",
            "i am bored",
            "i'm bored",
            "let's talk",
            "talk to me",
            "thank you",
            "thanks"
        ]

        if any(pattern in text for pattern in conversation_patterns):
            return "conversation"

        # -----------------------------
        # DEFAULT
        # -----------------------------

        return "general"