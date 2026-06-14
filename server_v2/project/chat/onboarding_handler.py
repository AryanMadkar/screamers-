from onboarding.onboarding_service import handle_onboarding

class OnboardingHandler:
    @staticmethod
    def handle(conversation_id, user_id, message):
        return handle_onboarding(conversation_id, user_id, message)
