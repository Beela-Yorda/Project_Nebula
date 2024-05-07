from flask import Flask, send_file, jsonify
import os
from flask_cors import CORS
import mysql.connector
#from config import DATABASE


app = Flask(__name__)
cors = CORS(app, origin='*')

# Route to serve the index.html file from the root directory
@app.route("/", methods=['GET'])
def index():
    frontend_path = os.path.join(os.getcwd(), 'frontend', 'index.html')
    return send_file(frontend_path)

# Health Check
@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'})

# Function to establish MySQL database connection
#def connect_to_database():
    #return mysql.connector.connect(**DATABASE)


if __name__ == "__main__":
    app.run(debug=True)

