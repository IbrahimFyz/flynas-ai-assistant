import sqlite3

DATABASE_NAME = "flynas.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS airports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_code TEXT NOT NULL UNIQUE,
            airport_name TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT NOT NULL UNIQUE,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (origin) REFERENCES airports(airport_code),
        FOREIGN KEY (destination) REFERENCES airports(airport_code)
    )
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fare_name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        cabin_class TEXT NOT NULL,
        refundable INTEGER NOT NULL,
        changeable INTEGER NOT NULL
    )
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS baggage_policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fare_id INTEGER NOT NULL,
        cabin_baggage_kg INTEGER NOT NULL,
        checked_baggage_kg INTEGER NOT NULL,
        extra_baggage_allowed INTEGER NOT NULL,
        FOREIGN KEY (fare_id) REFERENCES fares(id)
    )
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS booking_policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fare_id INTEGER NOT NULL,
        change_allowed INTEGER NOT NULL,
        cancellation_allowed INTEGER NOT NULL,
        change_fee REAL NOT NULL,
        cancellation_fee REAL NOT NULL,
        FOREIGN KEY (fare_id) REFERENCES fares(id)
    )
""")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")