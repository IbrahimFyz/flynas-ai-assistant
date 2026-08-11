from database.database import get_connection


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

    for city in cities:
        if city.lower() in question_lower:
            found_cities.append(city)

    return found_cities


def extract_route_from_question(question):
    """
    Extract origin and destination from questions
    such as:
    'What flights are available from Riyadh to Dubai?'
    """

    question_lower = question.lower()

    if "from" not in question_lower or "to" not in question_lower:
        return None, None

    after_from = question_lower.split("from", 1)[1]

    if "to" not in after_from:
        return None, None

    origin_text, destination_text = after_from.split("to", 1)

    origin = origin_text.strip(" ?.,")
    destination = destination_text.strip(" ?.,!")

    return origin, destination


if __name__ == "__main__":
    print(get_airport_code("Riyadh"))
    print(get_airport_code("Dubai"))

    print(
        find_cities_in_question(
            "What flights are available from Riyadh to Dubai?"
        )
    )

    print(
        extract_route_from_question(
            "What flights are available from Riyadh to Dubai?"
        )
    )