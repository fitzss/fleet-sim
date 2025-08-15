#!/usr/bin/env python3
from flask import Flask, request, jsonify
from datetime import datetime
from threading import Lock

app = Flask(__name__)
STATE = {}
LOCK = Lock()

@app.route("/health")
def health():
    return "ok", 200

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json(force=True)
    with LOCK:
        rid = str(data.get("robot_id", "unknown"))
        data["last_seen"] = datetime.utcnow().isoformat() + "Z"
        STATE[rid] = data
    return {"ok": True}, 200

@app.route("/fleet")
def fleet():
    with LOCK:
        resp = {
            "total_robots": len(STATE),
            "robots": STATE,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
