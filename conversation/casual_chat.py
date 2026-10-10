from conversation.personality import KrishnaPersonality


class CasualChat:

    """
    Handles normal and informal conversations.
    """

    def __init__(self, owner_name):

        self.owner_name = owner_name
        self.personality = KrishnaPersonality()

    def respond(self, user_input):

        text = user_input.lower().strip()

        # Greetings
        if "hello" in text or text == "hi" or "hey" in text:

            return self.personality.greeting(
                self.owner_name
            )

        # Tired
        if "tired" in text or "exhausted" in text:

            return self.personality.tired_response(
                self.owner_name
            )

        # Bored
        if "bored" in text:

            return self.personality.bored_response()

        # Thank you
        if "thank" in text:

            return self.personality.thanks_response()

        # How are you
        if "how are you" in text:

            return self.personality.how_are_you_response()

        # Default conversation
        return (
            "I'm listening. Tell me more."
        )