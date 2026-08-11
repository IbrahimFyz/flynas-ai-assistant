from database.database import get_connection


def get_booking_policy(fare_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            fares.fare_name,
            fares.price,
            booking_policies.cancellation_allowed,
            booking_policies.change_allowed,
            booking_policies.cancellation_fee,
            booking_policies.change_fee
        FROM fares
        JOIN booking_policies
            ON fares.id = booking_policies.fare_id
        WHERE fares.fare_name = ?
    """, (fare_name,))

    policy = cursor.fetchone()

    connection.close()

    return policy


if __name__ == "__main__":
    print("Value:")
    print(get_booking_policy("Value"))

    print("Plus:")
    print(get_booking_policy("Plus"))

    print("Light:")
    print(get_booking_policy("Light"))