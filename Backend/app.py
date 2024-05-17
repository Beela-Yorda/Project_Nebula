from flask import Flask, send_file, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import os

# Load variables from environment
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_NAME = os.environ.get('DATABASE_NAME')

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
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM nebula_summary LIMIT 1;")
        cursor.close()
        return jsonify({'message': 'Database connection test successful'})
    except Exception as err:
        return jsonify({'error': str(err)}), 500

# Get All Students
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student FROM nebula_summary;")
        students = [{'student': student[0]} for student in cursor.fetchall()]
        cursor.close()
        return jsonify(students)
    except Exception as err:
        return jsonify({'error': str(err)}), 500

# Get Student Details
@app.route('/api/student/<student_name>', methods=['GET'])
def get_student_details(student_name):
    try:
        cursor = mysql.connection.cursor()
        query = """
        SELECT * FROM students 
        WHERE email IN (
            SELECT email FROM nebula_summary 
            WHERE student = %s
        );
        """
        cursor.execute(query, (student_name,))
        student = cursor.fetchone()
        cursor.close()
        if student:
            student_details = {
                'Cohort': student[0],
                'RANK': student[1],
                'Student': student[2],
                'email': student[3],
                # Add more fields as needed
            }
            return jsonify(student_details)
        else:
            return jsonify({'error': 'Student not found'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500

# Get Student Email
@app.route('/api/student-email/<student_name>', methods=['GET'])
def get_student_email(student_name):
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT email FROM nebula_summary WHERE student = %s;"
        cursor.execute(query, (student_name,))
        email = cursor.fetchone()
        cursor.close()
        if email:
            return jsonify({'email': email[0]})
        else:
            return jsonify({'error': 'Email not found for the student'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500

# Get Cohort Stats
@app.route('/api/cohort/stats/nebula', methods=['GET'])
def get_nebula_stats():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cohort_stats WHERE cohort_name = 'nebula';")
        nebula_stats = cursor.fetchone()
        cursor.close()
        if nebula_stats:
            stats = {
                'cohort_name': nebula_stats[0],
                'total_students': nebula_stats[1],
                'average_score': nebula_stats[2],
                # Add more stats fields as needed
            }
            return jsonify(stats)
        else:
            return jsonify({'error': 'Cohort "nebula" not found'}), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500

# Get All Records from Nebula Summary Table
@app.route('/api/nebula-summary', methods=['GET'])
def get_nebula_summary():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM nebula_summary;")
        nebula_summary = cursor.fetchall()
        cursor.close()
        summary_list = []
        for record in nebula_summary:
            record_dict = {
                'Cohort': record[0],  
                'RANK': record[1],
                'Student': record[2],
                'Email': record[3],
                'Personal': record[4],
                'Attendance': record[5],
                'A-Comp.': record[6],
                'Quiz Submitted': record[7],
                'Score': record[8],
                'Compliance': record[9],
                'Watcher': record[10],
            }

            summary_list.append(record_dict)
        return jsonify({'nebula_summary': summary_list})
    except Exception as err:
        return jsonify({'error': str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True)
