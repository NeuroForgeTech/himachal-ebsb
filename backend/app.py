from flask import Flask, send_from_directory, jsonify
import serial
import threading
import time
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# === SERIAL PORT SETUP ===
ser = None
serial_data = {
    'landslide_status': None,
    'tilt_angle': None,
    'voltage': None,
    'servo_angle': None,
    'ropeway_mode': None,
    'ropeway_position': None
}

def read_serial_data():
    global ser, serial_data
    try:
        ser = serial.Serial('COM4', 9600, timeout=1)
        time.sleep(2)  # wait for serial to initialize
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith("DATA:"):
                    payload = line[5:].split(',')
                    if len(payload) == 6:
                        serial_data['landslide_status'] = payload[0]
                        serial_data['tilt_angle'] = payload[1]
                        serial_data['voltage'] = payload[2]
                        serial_data['servo_angle'] = payload[3]
                        serial_data['ropeway_mode'] = payload[4]
                        serial_data['ropeway_position'] = payload[5]
    except Exception as e:
        print(f"Serial error: {e}")

# Start serial thread
threading.Thread(target=read_serial_data, daemon=True).start()

# === ROUTES ===
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/api/data')
def get_data():
    return jsonify(serial_data)

# === ENTRY POINT ===
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
