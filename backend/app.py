from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store latest data and command
latest_data = {}
latest_command = ""

@app.route('/api/update', methods=['POST'])
def update_data():
    global latest_data
    try:
        latest_data = request.get_json()
        print(f"✅ Data received from ESP32: {latest_data}")
        return jsonify({"status": "success", "message": "Data updated"})
    except Exception as e:
        print("❌ Error in /api/update:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command', methods=['GET', 'POST'])
def command():
    global latest_command
    if request.method == 'POST':
        latest_command = request.get_json().get("command", "")
        print(f"🛰️ New command from dashboard: {latest_command}")
        return jsonify({"status": "success", "message": "Command updated"})

    elif request.method == 'GET':
        print("📡 ESP32 requested command:", latest_command)
        return jsonify({"command": latest_command})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "connected"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
