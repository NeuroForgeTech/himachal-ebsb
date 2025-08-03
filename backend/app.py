from flask import Flask, jsonify, send_from_directory
import serial
import json
import os

app = Flask(__name__, static_folder="../frontend", static_url_path='')

# Set the serial port and baud rate (adjust COM port as needed)
try:
    ser = serial.Serial('COM4', 9600, timeout=1)
except Exception as e:
    print("Serial error:", e)
    ser = None

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/get_status')
def get_status():
    default_data = {
        "tilt_angle": 0,
        "landslide": False,
        "solar_voltage": 0.0,
        "sun_position": "Unknown",
        "servo_value": 90,
        "ropeway_status": "Unknown",
        "esp32": "disconnected",
        "mega": "disconnected"
    }

    if ser and ser.is_open:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data = json.loads(line)
                data["esp32"] = "connected"
                data["mega"] = "connected"
                return jsonify(data)
        except Exception as e:
            print("Data read error:", e)
    
    return jsonify(default_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
