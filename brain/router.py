from brain.intent_detector import IntentDetector


class RequestRouter:
    """
    Routes user requests to the appropriate
    KRISHNA system module.
    """

    def __init__(self):

        self.intent_detector = IntentDetector()

    def route_request(self, user_input):

        intent = self.intent_detector.detect_intent(user_input)

        return intent