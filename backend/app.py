from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Global state (simulate control state)
esp32_status = {
    'connected': False,
    'tilt': 0,
    'voltage': 0.0,
    'servo_angle': 90,
    'ropeway_mode': 'manual'
}

@app.route('/')
def serve_dashboard():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/update', methods=['POST'])
def update_data():
    data = request.json
    esp32_status['connected'] = True
    esp32_status['tilt'] = data.get('tilt', 0)
    esp32_status['voltage'] = data.get('voltage', 0.0)
    esp32_status['servo_angle'] = data.get('servo_angle', 90)
    print(f"✅ Received ESP32 data: {data}")
    return jsonify({'status': 'ok', 'message': 'Data updated successfully'})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(esp32_status)

if __name__ == '__main__':
    app.run(debug=True)
