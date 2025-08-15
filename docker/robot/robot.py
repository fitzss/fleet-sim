#!/usr/bin/env python3
import os, time, json, random
import requests

ROBOT_ID = os.getenv("ROBOT_ID", "unknown")
MONITOR_URL = os.getenv("MONITOR_URL", "http://fleet-monitor:8000")

def get_status():
    return {
        "robot_id": ROBOT_ID,
        "battery": random.randint(30, 100),
        "position": {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        "status": "operational"
    }

def main():
    print(f"Robot {ROBOT_ID} starting...")
    while True:
        try:
            status = get_status()
            r = requests.post(f"{MONITOR_URL}/ingest", json=status, timeout=2)
            print(f"[robot {ROBOT_ID}] sent status -> {r.status_code}")
        except Exception as e:
            print(f"[robot {ROBOT_ID}] failed: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
