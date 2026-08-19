from database.database import get_connection
import re


# =========================
# ARABIC CITY NAMES
# =========================

ARABIC_CITY_NAMES = {
    "الرياض": "Riyadh",
    "جدة": "Jeddah",
    "الدمام": "Dammam",
    "المدينة": "Madinah",
    "المدينة المنورة": "Madinah",
    "دبي": "Dubai",
    "القاهرة": "Cairo",
    "اسطنبول": "Istanbul",
    "إسطنبول": "Istanbul",
}


def get_airport_code(city):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT airport_code
        FROM airports
        WHERE LOWER(city) = LOWER(?)
    """, (city,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def find_cities_in_question(question):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT city
        FROM airports
    """)

    cities = [row[0] for row in cursor.fetchall()]

    connection.close()

    found_cities = []

    question_lower = question.lower()

    # Check English city names
    for city in cities:
        if city.lower() in question_lower:
            found_cities.append(city)

    # Check Arabic city names
    for arabic_city, english_city in ARABIC_CITY_NAMES.items():
        if arabic_city in question:
            if english_city not in found_cities:
                found_cities.append(english_city)

    return found_cities


def normalize_city(city):
    """
    Convert Arabic city names to their English
    database names.
    """

    city = city.strip(" ؟?.,!")

    if city in ARABIC_CITY_NAMES:
        return ARABIC_CITY_NAMES[city]

    return city


def extract_route_from_question(question):
    """
    Extract origin and destination from English
    and Arabic questions.

    Examples:

    What flights are available from Riyadh to Dubai?
    -> Riyadh, Dubai

    وش الرحلات المتاحة من الرياض إلى دبي؟
    -> Riyadh, Dubai

    What flights go to Dubai?
    -> None, Dubai

    وش الرحلات الي تودي على دبي؟
    -> None, Dubai
    """

    question_clean = question.strip()

    # =========================
    # ENGLISH: FROM X TO Y
    # =========================

    english_match = re.search(
        r"\bfrom\s+(.+?)\s+to\s+(.+?)(?:[?.!]|$)",
        question_clean,
        re.IGNORECASE
    )

    if english_match:

        origin = english_match.group(1).strip(" ?.,!")
        destination = english_match.group(2).strip(" ?.,!")

        origin = normalize_city(origin)
        destination = normalize_city(destination)

        return origin, destination


    # =========================
    # ARABIC: من X إلى Y
    # =========================

    arabic_match = re.search(
        r"من\s+(.+?)\s+(?:إلى|الى)\s+(.+?)(?:[؟?.!]|$)",
        question_clean
    )

    if arabic_match:

        origin = arabic_match.group(1).strip(" ؟?.,!")
        destination = arabic_match.group(2).strip(" ؟?.,!")

        origin = normalize_city(origin)
        destination = normalize_city(destination)

        return origin, destination


    # =========================
    # ENGLISH: DESTINATION ONLY
    # =========================

    english_destination_match = re.search(
        r"\b(?:to|towards|go\s+to|going\s+to|fly\s+to|flights?\s+to)\s+(.+?)(?:[?.!]|$)",
        question_clean,
        re.IGNORECASE
    )

    if english_destination_match:

        destination = english_destination_match.group(1).strip(" ?.,!")

        destination = normalize_city(destination)

        if destination:
            return None, destination


    # =========================
    # ARABIC: DESTINATION ONLY
    # =========================

    arabic_destination_match = re.search(
        r"(?:إلى|الى|على)\s+(.+?)(?:[؟?.!]|$)",
        question_clean
    )

    if arabic_destination_match:

        destination = arabic_destination_match.group(1).strip(" ؟?.,!")

        destination = normalize_city(destination)

        if destination:
            return None, destination


    return None, None


if __name__ == "__main__":

    print("----- AIRPORT CODE TEST -----")

    print(get_airport_code("Riyadh"))
    print(get_airport_code("Dubai"))


    print("\n----- CITY DETECTION TEST -----")

    print(
        find_cities_in_question(
            "What flights are available from Riyadh to Dubai?"
        )
    )

    print(
        find_cities_in_question(
            "وش الرحلات المتاحة من الرياض إلى دبي؟"
        )
    )


    print("\n----- ROUTE EXTRACTION TEST -----")

    print(
        extract_route_from_question(
            "What flights are available from Riyadh to Dubai?"
        )
    )

    print(
        extract_route_from_question(
            "وش الرحلات المتاحة من الرياض إلى دبي؟"
        )
    )

    print(
        extract_route_from_question(
            "هل فيه رحلات من جدة إلى دبي؟"
        )
    )

    print(
        extract_route_from_question(
            "What flights go to Dubai?"
        )
    )

    print(
        extract_route_from_question(
            "وش الرحلات الي تودي على دبي؟"
        )
    )