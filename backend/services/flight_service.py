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


def search_flights_to_destination(destination):
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
        WHERE destination = ?
    """, (destination,))

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

    # User did not provide a destination
    if not destination_city:
        return None

    destination = get_airport_code(destination_city)

    # Destination is not available in our database
    if not destination:
        return []

    # =========================
    # DESTINATION ONLY
    # =========================

    if not origin_city:
        return search_flights_to_destination(destination)

    # =========================
    # ORIGIN + DESTINATION
    # =========================

    origin = get_airport_code(origin_city)

    # Origin is not available in our database
    if not origin:
        return []

    return search_flights(origin, destination)


if __name__ == "__main__":

    print("----- RIYADH TO DUBAI -----")

    flights = search_flights_from_question(
        "What flights are available from Riyadh to Dubai?"
    )

    if flights:
        for flight in flights:
            print(flight)
    else:
        print("No flights found.")


    print("\n----- ALL FLIGHTS TO DUBAI -----")

    flights = search_flights_from_question(
        "What flights go to Dubai?"
    )

    if flights:
        for flight in flights:
            print(flight)
    else:
        print("No flights found.")


    print("\n----- ALL FLIGHTS TO DUBAI - ARABIC -----")

    flights = search_flights_from_question(
        "وش الرحلات الي تودي على دبي؟"
    )

    if flights:
        for flight in flights:
            print(flight)
    else:
        print("No flights found.")