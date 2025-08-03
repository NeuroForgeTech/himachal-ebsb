from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='../frontend')

# In-memory store (for demo; not persistent)
latest_data = {}
latest_command = {"ropeway_mode": "manual", "servo_angle": 90}

# Serve frontend/index.html
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# ESP32 sends data to this route
@app.route('/upload', methods=['POST'])
def upload_data():
    global latest_data
    latest_data = request.get_json()
    print("[ESP32] Uploaded data:", latest_data)
    return jsonify({"status": "success"})

# Dashboard polls latest ESP32 data
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(latest_data)

# ESP32 asks for latest control command
@app.route('/command', methods=['GET'])
def get_command():
    return jsonify(latest_command)

# Dashboard sets new control command for ESP32
@app.route('/set-command', methods=['POST'])
def set_command():
    global latest_command
    latest_command = request.get_json()
    print("[Dashboard] Updated command:", latest_command)
    return jsonify({"status": "updated"})

# Required for Render health checks (optional but recommended)
@app.route('/healthz')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
