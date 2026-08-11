from database.database import get_connection
from services.airport_service import get_airport_code


def search_flights(origin, destination):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            flight_number,
            origin,
            destination,
            departure_time,
            arrival_time,
            status
        FROM flights
        WHERE origin = ?
        AND destination = ?
    """, (origin, destination))

    flights = cursor.fetchall()

    connection.close()

    return flights


def search_flights_by_city(origin_city, destination_city):
    origin = get_airport_code(origin_city)
    destination = get_airport_code(destination_city)

    if not origin or not destination:
        return []

    return search_flights(origin, destination)


def search_flights_from_question(question):
    from services.airport_service import extract_route_from_question

    origin_city, destination_city = extract_route_from_question(question)

    # User did not provide both origin and destination
    if not origin_city or not destination_city:
        return None

    origin = get_airport_code(origin_city)
    destination = get_airport_code(destination_city)

    # One or both cities are not available in our database
    if not origin or not destination:
        return []

    return search_flights(origin, destination)


if __name__ == "__main__":
    flights = search_flights_from_question(
        "What flights are available from Riyadh to Dubai?"
    )

    if flights:
        for flight in flights:
            print(flight)
    else:
        print("No flights found.")