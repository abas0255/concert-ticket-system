import sqlite3

connection = sqlite3.connect('tickets.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS bookings')

cursor.execute('''
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    date_of_birth TEXT,
    ic_number TEXT,
    payment_reference TEXT,
    seat_type TEXT,
    number_of_pax INTEGER,
    ticket_id TEXT,
    queue_number INTEGER,
    ip_address TEXT,
    booking_timestamp TEXT
)
''')

connection.commit()
connection.close()

print("Database created successfully")