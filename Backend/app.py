from flask import Flask, send_file, jsonify
from flask_cors import CORS
import mysql.connector
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

app = Flask(__name__)
cors = CORS(app, origin='*')

# MySQL Configuration
DATABASE = {
    'host': os.getenv('DATABASE_HOST'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'database': os.getenv('DATABASE_NAME')
}

# Initialize MySQL
mysql = MySQL(app)

# Function to establish MySQL database connection
def connect_to_database():
    return mysql.connector.connect(**DATABASE)

# Function to close database connection
def close_database_connection(connection, cursor):
    if connection.is_connected():
        cursor.close()
        connection.close()

# Route to serve the index.html file from the root directory
@app.route("/", methods=['GET'])
def index():
    frontend_path = os.path.join(os.getcwd(),'index.html')
    return send_file(frontend_path)

# Health Check
@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'})

# Test Database Connection
@app.route('/api/test-db-connection', methods=['POST'])
def test_db_connection():
    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute("SELECT nebula FROM cohort")  # Corrected query
        close_database_connection(db_connection, cursor)
        return jsonify({'message': 'Database connection test successful'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


if __name__ == "__main__":
    app.run(debug=True)
