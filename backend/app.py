from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# In-memory message store (optional)
messages = {"esp32": "", "web": ""}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    source = data.get("source")
    content = data.get("message")

    if source in messages:
        messages[source] = content
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "invalid source"}), 400

@app.route("/receive/<target>", methods=["GET"])
def receive_message(target):
    if target in messages:
        return jsonify({"message": messages[target]}), 200
    else:
        return jsonify({"error": "invalid target"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # <-- critical for Render
    app.run(host="0.0.0.0", port=port, debug=True)
