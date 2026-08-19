import re

from database.database import get_connection


SUPPORTED_FARES = [
    "Light",
    "Value",
    "Plus"
]


# =========================
# FARE DETECTION
# =========================

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
    # English
    r"\bfor\s+(?:the\s+)?([a-zA-Z]+)\s+fare\b",
    r"\bto\s+([a-zA-Z]+)\b",
    r"\b(?:fare|class|package)\s+([a-zA-Z]+)\b",
    r"\bin\s+([a-zA-Z]+)\b",
    r"\bof\s+(?:the\s+)?([a-zA-Z]+)\b",
    r"\bmy\s+([a-zA-Z]+)\s+fare\b",

    # Arabic
    r"(?:سعر|فئة|باقة)\s+([a-zA-Z]+)\b",
    r"(?:في|من)\s+فئة\s+([a-zA-Z]+)\b",
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


# =========================
# DATABASE
# =========================

def get_fare(fare_name):
    """
    Get complete information about one fare.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            fares.fare_name,
            fares.price,
            fares.cabin_class,
            fares.refundable,
            fares.changeable,
            baggage_policies.cabin_baggage_kg,
            baggage_policies.checked_baggage_kg,
            baggage_policies.extra_baggage_allowed,
            booking_policies.change_allowed,
            booking_policies.cancellation_allowed,
            booking_policies.change_fee,
            booking_policies.cancellation_fee
        FROM fares
        JOIN baggage_policies
            ON fares.id = baggage_policies.fare_id
        JOIN booking_policies
            ON fares.id = booking_policies.fare_id
        WHERE fares.fare_name = ?
    """, (fare_name,))

    fare = cursor.fetchone()

    connection.close()

    return fare


def get_all_fares():
    """
    Get complete information about all fares.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            fares.fare_name,
            fares.price,
            fares.cabin_class,
            fares.refundable,
            fares.changeable,
            baggage_policies.cabin_baggage_kg,
            baggage_policies.checked_baggage_kg,
            baggage_policies.extra_baggage_allowed,
            booking_policies.change_allowed,
            booking_policies.cancellation_allowed,
            booking_policies.change_fee,
            booking_policies.cancellation_fee
        FROM fares
        JOIN baggage_policies
            ON fares.id = baggage_policies.fare_id
        JOIN booking_policies
            ON fares.id = booking_policies.fare_id
        ORDER BY fares.id
    """)

    fares = cursor.fetchall()

    connection.close()

    return fares


# =========================
# TEST
# =========================

if __name__ == "__main__":

    print(
    find_mentioned_fare(
        "What baggage is included in Premium?"
    )
    )

    print(
        find_mentioned_fare(
            "كم سعر Premium؟"
        )
    )

    print(
        find_mentioned_fare(
            "Can I cancel my Premium fare?"
        )
    )

    print("----- FARE DETECTION -----")

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


    print("\n----- DATABASE FARES -----")

    fares = get_all_fares()

    for fare in fares:
        print(fare)


    print("\n----- LIGHT -----")
    print(get_fare("Light"))

    print("\n----- VALUE -----")
    print(get_fare("Value"))

    print("\n----- PLUS -----")
    print(get_fare("Plus"))