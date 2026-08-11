from database import get_connection


def seed_airports():
    connection = get_connection()
    cursor = connection.cursor()

    airports = [
        ("RUH", "King Khalid International Airport", "Riyadh", "Saudi Arabia"),
        ("JED", "King Abdulaziz International Airport", "Jeddah", "Saudi Arabia"),
        ("DMM", "King Fahd International Airport", "Dammam", "Saudi Arabia"),
        ("MED", "Prince Mohammad bin Abdulaziz International Airport", "Madinah", "Saudi Arabia"),
        ("DXB", "Dubai International Airport", "Dubai", "UAE"),
        ("CAI", "Cairo International Airport", "Cairo", "Egypt"),
        ("IST", "Istanbul Airport", "Istanbul", "Turkey"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO airports
        (airport_code, airport_name, city, country)
        VALUES (?, ?, ?, ?)
        """,
        airports
    )

    connection.commit()
    connection.close()

    print("Airports seeded successfully.")

def seed_flights():
    connection = get_connection()
    cursor = connection.cursor()

    flights = [
        ("FN-M001", "RUH", "DXB", "2026-08-15 08:00", "2026-08-16 10:00", "Scheduled"),
        ("FN-M002", "RUH", "JED", "2026-08-15 10:30", "2026-08-15 12:30", "Scheduled"),
        ("FN-M003", "JED", "CAI", "2026-08-15 14:00", "2026-08-15 16:30", "Scheduled"),
        ("FN-M004", "DMM", "DXB", "2026-08-16 09:00", "2026-08-16 10:30", "Scheduled"),
        ("FN-M005", "RUH", "IST", "2026-08-16 20:00", "2026-08-17 01:30", "Scheduled"),
        ("FN-M006", "MED", "RUH", "2026-08-17 11:00", "2026-08-17 12:30", "Scheduled"),
        ("FN-M007", "RUH", "DMM", "2026-08-17 15:00", "2026-08-17 16:45", "Scheduled"),
        ("FN-M008", "JED", "DXB", "2026-08-18 18:00", "2026-08-18 20:30", "Scheduled"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO flights
        (
            flight_number,
            origin,
            destination,
            departure_time,
            arrival_time,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        flights
    )

    connection.commit()
    connection.close()

    print("Flights seeded successfully.")

def seed_fares():
    connection = get_connection()
    cursor = connection.cursor()

    fares = [
        ("Light", 299.00, "Economy", 0, 1),
        ("Value", 399.00, "Economy", 0, 1),
        ("Plus", 549.00, "Economy", 1, 1),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO fares
        (
            fare_name,
            price,
            cabin_class,
            refundable,
            changeable
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        fares
    )

    connection.commit()
    connection.close()

    print("Fares seeded successfully.")

def seed_baggage_policies():
    connection = get_connection()
    cursor = connection.cursor()

    baggage_policies = [
        (1, 7, 0, 1),
        (2, 7, 20, 1),
        (3, 7, 30, 1),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO baggage_policies
        (
            fare_id,
            cabin_baggage_kg,
            checked_baggage_kg,
            extra_baggage_allowed
        )
        VALUES (?, ?, ?, ?)
        """,
        baggage_policies
    )

    connection.commit()
    connection.close()

    print("Baggage policies seeded successfully.")

def seed_booking_policies():
    connection = get_connection()
    cursor = connection.cursor()

    booking_policies = [
        (1, 1, 0, 100.00, 0.00),
        (2, 1, 1, 75.00, 150.00),
        (3, 1, 1, 0.00, 100.00),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO booking_policies
        (
            fare_id,
            change_allowed,
            cancellation_allowed,
            change_fee,
            cancellation_fee
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        booking_policies
    )

    connection.commit()
    connection.close()

    print("Booking policies seeded successfully.")


if __name__ == "__main__":
    seed_airports()
    seed_flights()
    seed_fares()
    seed_baggage_policies()
    seed_booking_policies()
    