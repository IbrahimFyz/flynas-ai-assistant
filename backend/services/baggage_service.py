from database.database import get_connection


def get_baggage_policy(fare_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            fares.fare_name,
            fares.price,
            baggage_policies.cabin_baggage_kg,
            baggage_policies.checked_baggage_kg,
            baggage_policies.extra_baggage_allowed
        FROM fares
        JOIN baggage_policies
            ON fares.id = baggage_policies.fare_id
        WHERE fares.fare_name = ?
    """, (fare_name,))

    policy = cursor.fetchone()

    connection.close()

    return policy

if __name__ == "__main__":
    policy = get_baggage_policy("Value")

    print(policy)