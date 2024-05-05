from flask import Flask, send_file

app = Flask(__name__)

# Route to serve the index.html file from the root directory
@app.route('/')
def index():
    return send_file('index.html')

    # Health Check
@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    app.run(debug=True)
