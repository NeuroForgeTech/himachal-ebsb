from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Allow frontend JS to call API

# Store latest ESP32 data
esp_data = {
    "landslide": "Unknown",
    "solar_voltage": 0.0,
    "servo_angle": 0,
    "timestamp": None
}

# Store dashboard control commands
command_state = {
    "ropeway_mode": "AUTO",  # Can be AUTO or MANUAL
    "servo_angle": 0
}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/update', methods=['POST'])
def update_data():
    data = request.get_json()
    if data:
        esp_data.update(data)
        return jsonify({"status": "success", "message": "Data updated"})
    return jsonify({"status": "error", "message": "No JSON data"}), 400

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(esp_data)

@app.route('/api/command', methods=['GET'])
def get_command():
    return jsonify(command_state)

@app.route('/api/setcommand', methods=['POST'])
def set_command():
    data = request.get_json()
    if data:
        command_state.update(data)
        return jsonify({"status": "success", "command": command_state})
    return jsonify({"status": "error", "message": "No JSON data"}), 400

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
