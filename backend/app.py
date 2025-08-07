# File: app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import datetime

app = Flask(__name__, static_folder='../frontend')
CORS(app)

esp32_state = {
    "tilt": 0,
    "voltage": 0.0,
    "servo_angle": 90,
    "connected": False,
    "last_update": None
}

command_state = {
    "ropeway_mode": "AUTO"
}

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/update', methods=['POST'])
def update_from_esp32():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400

        esp32_state["tilt"] = data.get("tilt", esp32_state["tilt"])
        esp32_state["voltage"] = data.get("voltage", esp32_state["voltage"])
        esp32_state["servo_angle"] = data.get("servo_angle", esp32_state["servo_angle"])
        esp32_state["connected"] = True
        esp32_state["last_update"] = datetime.datetime.utcnow()

        return jsonify({"message": "Data updated", "status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/command', methods=['GET'])
def get_latest_command():
    return jsonify({
        "ropeway_mode": command_state["ropeway_mode"]
    })

@app.route('/api/setcommand', methods=['POST'])
def set_command_from_ui():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400

    command = data.get("ropeway_mode")
    if command in ["AUTO", "MANUAL"]:
        command_state["ropeway_mode"] = command
        return jsonify({"message": "Command updated", "status": "success"}), 200
    else:
        return jsonify({"message": "Invalid command", "status": "error"}), 400

@app.route('/get_status', methods=['GET'])
def get_status():
    status = {
        "tilt_angle": esp32_state.get("tilt", 0),
        "solar_voltage": esp32_state.get("voltage", 0.0),
        "sun_position": f"{esp32_state.get('servo_angle', 90)}°",
        "servo_value": esp32_state.get("servo_angle", 90),
        "ropeway_status": command_state.get("ropeway_mode", "AUTO"),
        "esp32": "connected" if esp32_state.get("connected") else "disconnected",
        "mega": "disconnected"  # Update in future when Mega2560 is integrated
    }
    return jsonify(status), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
