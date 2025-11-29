import re
from rules import rules

fallback_response = "I'm not sure about that. Please contact the university administration."


def get_response(user_input: str) -> str:
    """Matches user input with rules and returns the best response."""

    user_input = user_input.lower()

    for pattern, response in rules.items():
        if re.search(pattern, user_input):
            return response

    return fallback_response
