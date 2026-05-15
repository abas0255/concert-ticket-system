from flask import Flask, request, render_template
import sqlite3
import uuid
import random
from datetime import datetime

app = Flask(__name__)

# Queue Page
@app.route('/')
def queue_page():
    return render_template('queue.html')

# Queue Management
@app.route('/enter-queue', methods=['POST'])
def enter_queue():

    queue_number = random.randint(1000, 9999)
    wait_time = random.randint(1, 5)

    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>Queue Waiting Room</title>

        <script>

            let seconds = 10;

            function updateTimer() {{

                document.getElementById("countdown").innerHTML = seconds;

                seconds--;

                if (seconds < 0) {{
                    window.location.href = "/booking-form";
                }}
            }}

            setInterval(updateTimer, 1000);

        </script>

    </head>

    <body>

        <h1>Queue Assigned</h1>

        <p>Your Queue Number: {queue_number}</p>

        <p>Estimated Wait Time: {wait_time} minutes</p>

        <p>You will automatically enter the booking system in:</p>

        <h2 id="countdown">10</h2>

    </body>

    </html>
    """

# Booking Form
@app.route('/booking-form')
def booking_form():
    return render_template('index.html')

# Booking API
@app.route('/book-ticket', methods=['POST'])
def book_ticket():

    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    date_of_birth = request.form.get('date_of_birth')
    ic_number = request.form.get('ic_number')
    payment_reference = request.form.get('payment_reference')
    seat_type = request.form.get('seat_type')
    number_of_pax = request.form.get('number_of_pax')

    # Metadata Retention
    ip_address = request.remote_addr
    booking_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Queue Metadata
    queue_number = random.randint(1000, 9999)

    # Age Verification
    dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
    today = datetime.today()

    age = today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )

    if age < 18:
        return """
        <h1>Booking Failed</h1>
        <p>User must be 18 years old and above.</p>
        <a href="/">Back to Queue Page</a>
        """

    # Ticket Generator
    ticket_id = str(uuid.uuid4())[:8]

    connection = sqlite3.connect('tickets.db')
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO bookings (
        full_name,
        email,
        phone,
        date_of_birth,
        ic_number,
        payment_reference,
        seat_type,
        number_of_pax,
        ticket_id,
        queue_number,
        ip_address,
        booking_timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        full_name,
        email,
        phone,
        date_of_birth,
        ic_number,
        payment_reference,
        seat_type,
        number_of_pax,
        ticket_id,
        queue_number,
        ip_address,
        booking_timestamp
    ))

    connection.commit()
    connection.close()

    return f"""
    <h1>Ticket Booked Successfully</h1>

    <p>Ticket ID: {ticket_id}</p>

    <p>Seat Type: {seat_type}</p>

    <p>Number of Pax: {number_of_pax}</p>

    <p>Queue Number: {queue_number}</p>

    <a href="/">Back to Queue Page</a>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5001)