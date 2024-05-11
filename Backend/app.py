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
app.static_folder = 'public/assets'


@app.route('/static/<path:filename>')
def serve_static_file(filename):
  return serve_static_file(filename)

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
        db_connection = mysql.connect()
        cursor = db_connection.cursor()
        cursor.execute("SELECT nebula FROM cohort")  # Corrected query
        cursor.close()
        db_connection.close()
        return jsonify({'message': 'Database connection test successful'})
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    
# Get All Students
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        db_connection = mysql.connect()  # Establish database connection
        cursor = db_connection.cursor()
        query = "SELECT student FROM nebula_summary;"
        cursor.execute(query)
        students = [{'student': student[0]} for student in cursor.fetchall()]
        db_connection.close()  # Close database connection
        return jsonify(students)
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@app.route('/api/student/<email>', methods=['POST'])
def get_student_details(email):
    try:
        db_connection = mysql.connect()
        cursor = db_connection.cursor()
        query = "SELECT * FROM students WHERE email IN (SELECT email FROM nebula_summary WHERE nebula_summary.email = %s);"
        cursor.execute(query, (email,))
        student = cursor.fetchone()
        cursor.close()
        db_connection.close()
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

# Get Cohort Stats
@app.route('/api/cohort/stats/nebula', methods=['GET'])
def get_nebula_stats():
    try:
        db_connection = mysql.connect()
        cursor = db_connection.cursor()

        # Execute SQL query to retrieve cohort statistics for the "nebula" cohort
        query = "SELECT * FROM cohort_stats WHERE cohort_name = 'nebula';"
        cursor.execute(query)
        nebula_stats = cursor.fetchone()

        cursor.close()
        db_connection.close()

        # Check if "nebula" cohort stats are found
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
        db_connection = mysql.connect()
        cursor = db_connection.cursor()

        # Execute SQL query to select all records from nebula_summary table
        query = "SELECT * FROM nebula_summary;"
        cursor.execute(query)
        nebula_summary = cursor.fetchall()

        cursor.close()
        db_connection.close()

        # Convert the result into a list of dictionaries
        summary_list = []
        for record in nebula_summary:
            record_dict = {
                'Cohort': record[0],  # Replace 'column1', 'column2', etc. with actual column names
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
                # Add more columns as needed
            }
            summary_list.append(record_dict)

        # Return the list of records as JSON response
        return jsonify({'nebula_summary': summary_list})
    except Exception as err:
        return jsonify({'error': str(err)}), 500




if __name__ == "__main__":
    app.run(debug=True)
