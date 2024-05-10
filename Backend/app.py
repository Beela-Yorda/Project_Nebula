from flask import Flask, send_file, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('DATABASE_HOST')
app.config['MYSQL_USER'] = os.getenv('DATABASE_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DATABASE_NAME')

# Initialize MySQL
mysql = MySQL(app)

# Configure static files directory
app.static_folder = 'static'

# Route to serve the index.html file from the root directory
@app.route("/", methods=['GET'])
def index():
    frontend_path = os.path.join(os.getcwd(), 'public', 'index.html')
    return send_file(frontend_path)

# Health Check
@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'})

# Test Database Connection
@app.route('/api/test-db-connection', methods=['POST'])
def test_db_connection():
    try:
        db_connection = mysql.connect()
        cursor = db_connection.cursor()
        cursor.execute("SELECT nebula FROM cohort")  # Corrected query
        cursor.close()
        db_connection.close()
        return jsonify({'message': 'Database connection test successful'})
    except Exception as err:
        return jsonify({'error': str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True)
