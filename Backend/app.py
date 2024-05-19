from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load variables from environment with default values
DATABASE_URL = os.environ.get('DATABASE_URL', 'localhost')
DATABASE_USER = os.environ.get('DATABASE_USER', 'root')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'nebula-db')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL configurations
app.config['MYSQL_HOST'] = DATABASE_URL
app.config['MYSQL_USER'] = DATABASE_USER
app.config['MYSQL_PASSWORD'] = DATABASE_PASSWORD
app.config['MYSQL_DB'] = DATABASE_NAME

# Initialize MySQL
mysql = MySQL(app)

# Route to serve the index.html file from the root directory
@app.route("/", methods=['GET'])
def index():
    frontend_path = os.path.join(os.getcwd(), 'index.html')
    return send_file(frontend_path)

# Health Check
@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'})

# Test Database Connection
@app.route('/api/test-db-connection', methods=['POST'])
def test_db_connection():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT student FROM nebula_summary WHERE student = %s;", ("Jamie Smith",))
        return jsonify({'message': 'Database connection test successful'})
    except Exception as err:
        app.logger.error(f"Database connection failed: {err}")
        return jsonify({'error': f'Database connection failed: {err}'}), 500

# Get All Students
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT Student FROM nebula_summary;")
            students = [{'student': student[0]} for student in cursor.fetchall()]
        return jsonify(students)
    except Exception as err:
        app.logger.error(f"Failed to fetch students: {err}")
        return jsonify({'error': f'Failed to fetch students: {err}'}), 500

@app.route('/api/student/email', methods=['POST'])
def get_student_email():
    data = request.get_json()
    student_name = data.get('student_name')
    if not student_name:
        return jsonify({'error': 'Student name is required'}), 400

    try:
        conn = test_db_connection()
        cursor = conn.cursor()
        query = "SELECT Email FROM nebula_summary WHERE student = '%s'"
        cursor.execute(query, (student_name,))
        email = cursor.fetchone()
        cursor.close()
        conn.close()

        if email:
            return jsonify({'email': email[0]})
        else:
            return jsonify({'error': 'Email not found for the student'}), 404

    except mysql.connector.Error as err:
        app.logger.error(f"Failed to fetch email for {student_name}: {err}")
        return jsonify({'error': f'Failed to fetch email for {student_name}: {err}'}), 500

# Get Cohort Stats
@app.route('/api/cohort/stats/[cohort_name]', methods=['GET'])
def get_cohort_stats(cohort_name):
    try:
        with mysql.connection.cursor() as cursor:
            query = """
            SELECT Attendance, Score, RANK 
            FROM nebula_summary 
            WHERE cohort_name = %s;
            """
            cursor.execute(query, (cohort_name,))
            cohort_stats = cursor.fetchone()
        if cohort_stats:
            stats = {
                'Attendance': cohort_stats[0],
                'Score': cohort_stats[1],
                'RANK': cohort_stats[2],
            }
            return jsonify(stats)
        else:
            return jsonify({'error': f'Cohort "{cohort_name}" not found'}), 404
    except Exception as err:
        app.logger.error(f"Failed to fetch stats for cohort {cohort_name}: {err}")
        return jsonify({'error': f'Failed to fetch stats for cohort {cohort_name}: {err}'}), 500

if __name__ == "__main__":
    app.run(debug=True)
