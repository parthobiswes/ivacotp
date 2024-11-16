from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Path to your SQLite database file
db_path = 'otp_database.db'


# Database helper function
def get_otp_data(mobile_number):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM otp WHERE mobile = ?", (mobile_number,))
        return cursor.fetchone(), None
    except sqlite3.Error as e:
        return None, str(e)
    finally:
        connection.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data():
    mobile_number = request.args.get('mobile', None)
    if not mobile_number or not mobile_number.isdigit():
        return 'handleResponse({"error": "Invalid mobile number"});', 400

    row, error = get_otp_data(mobile_number)
    if error:
        return f'handleResponse({{"error": "Database error: {error}"}});', 500

    if row:
        response = {
            "otp": row[2],
            "sender": "NAGAD",
            "otp1": row[4],
            "sender1": "16216",
            "otp2": row[6],
            "sender2": "+8801708404440",
            "otp3": row[6],
            "sender3": "IVAC_BD"
        }
    else:
        response = {"error": "No data found for the given mobile number"}
    
    return f'handleResponse({response});', 200


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True, host='0.0.0.0')
