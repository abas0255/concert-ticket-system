import sqlite3

connection = sqlite3.connect('tickets.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    payment_reference TEXT,
    ticket_id TEXT
)
''')

connection.commit()
connection.close()

print("Database created successfully")