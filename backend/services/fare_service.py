import re


SUPPORTED_FARES = [
    "Light",
    "Value",
    "Plus"
]


def find_fare_in_question(question):
    question_lower = question.lower()

    for fare in SUPPORTED_FARES:
        if fare.lower() in question_lower:
            return fare

    return None


def find_mentioned_fare(question):
    """
    Detect the fare mentioned by the user.

    Returns:
    - Light
    - Value
    - Plus
    - Unsupported fare name
    - None if no fare was mentioned
    """

    question_lower = question.lower()

    # Check supported fares first
    for fare in SUPPORTED_FARES:
        if fare.lower() in question_lower:
            return fare

    # Look for fare names after common phrases
    patterns = [
        r"\bfor\s+(?:the\s+)?([a-zA-Z]+)\s+fare\b",
        r"\bto\s+([a-zA-Z]+)\b",
        r"\b(?:fare|class|package)\s+([a-zA-Z]+)\b"
    ]

    ignored_words = {
        "the",
        "my",
        "a",
        "an",
        "this",
        "that",
        "myself",
        "booking"
    }

    for pattern in patterns:
        matches = re.findall(pattern, question_lower)

        for match in matches:
            fare = match.strip(".,?!").capitalize()

            if fare.lower() not in ignored_words:
                return fare

    return None


if __name__ == "__main__":

    print(
        find_fare_in_question(
            "What is the cancellation fee for the Plus fare?"
        )
    )

    print(
        find_fare_in_question(
            "What baggage is included in the Light fare?"
        )
    )

    print(
        find_fare_in_question(
            "Can I cancel my Value fare?"
        )
    )

    print(
        find_fare_in_question(
            "What is the cancellation fee?"
        )
    )

    print(
        find_mentioned_fare(
            "What is the cancellation fee for the Premium fare?"
        )
    )

    print(
        find_mentioned_fare(
            "Can I add extra baggage to Premium?"
        )
    )

    print(
        find_mentioned_fare(
            "Can I add extra baggage to my booking?"
        )
    )