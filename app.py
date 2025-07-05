import os
import json
from flask import Flask, request, jsonify, abort
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Discord App is running!", 200

@app.route("/interactions", methods=["POST"])
def interactions():
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    raw_body = request.data.decode("utf-8")

    # Verify signature
    try:
        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{raw_body}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        abort(401, "Invalid request signature")

    data = request.json

    # Ping = basic check
    if data["type"] == 1:
        return jsonify({"type": 1})  # Pong

    # Handle slash command
    if data["type"] == 2 and data["data"]["name"] == "hello":
        return jsonify({
            "type": 4,
            "data": {
                "content": f"Hello, {data['member']['user']['username']}!"
            }
        })

    return "Unhandled interaction", 400

if __name__ == "__main__":
    app.run(debug=True)
