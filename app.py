from flask import Flask, request, jsonify, render_template
import sqlite3
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book-ticket', methods=['POST'])
def book_ticket():

    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    payment_reference = request.form.get('payment_reference')

    ticket_id = str(uuid.uuid4())[:8]

    connection = sqlite3.connect('tickets.db')
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO bookings (
        full_name,
        email,
        phone,
        payment_reference,
        ticket_id
    ) VALUES (?, ?, ?, ?, ?)
    ''', (
        full_name,
        email,
        phone,
        payment_reference,
        ticket_id
    ))

    connection.commit()
    connection.close()

    return f"""
    <h1>Ticket Booked Successfully</h1>
    <p>Ticket ID: {ticket_id}</p>
    <a href="/">Back to Booking Page</a>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5001)