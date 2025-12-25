from flask import Flask, render_template, jsonify
from flask_cors import CORS
import time
import random
import threading
from src.eno_core.system import SystemMonitor
from src.eno_net.secure_channel import SecureChannel
from src.eno_sim.threat_detector import ThreatDetector

app = Flask(__name__)
CORS(app)

# Initialize Core Systems
sys_mon = SystemMonitor(system_name="ENO-COMMAND-NODE")
channel = SecureChannel(channel_id="SAT-LINK-7")
detector = ThreatDetector(sensitivity_level=3)

# Shared State for Demo
latest_traffic = []
system_alerts = []

def simulation_loop():
    """Background thread to generate data continually."""
    sample_messages = [
        "Telemetry: 44.2N, 32.1E",
        "Heartbeat: OK",
        "Syncing Database...",
        "DROP DATABASE credentials", # Threat
        "Uplink Established",
        "Packet Loss Detected",
        "EXEC: /bin/sh -i", # Threat
        "Routine Check: Passed"
    ]
    
    while True:
        msg = random.choice(sample_messages)
        
        # 1. Process Traffic
        timestamp = time.strftime("%H:%M:%S")
        is_threat = detector.scan_network_traffic(msg)
        
        log_entry = {
            "time": timestamp,
            "message": msg,
            "encrypted": channel.transmit(msg),
            "status": "THREAT" if is_threat else "SECURE"
        }
        
        # Update State (Keep last 10 logs)
        latest_traffic.insert(0, log_entry)
        if len(latest_traffic) > 15:
            latest_traffic.pop()
            
        if is_threat:
            sys_mon.log_event("IDS", f"Threat detected: {msg}", "WARNING")
            system_alerts.append({"time": timestamp, "alert": f"Malicious Signature: {msg}"})
        
        time.sleep(2)

# Start Simulation in Background
sim_thread = threading.Thread(target=simulation_loop, daemon=True)
sim_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    # Mock Hardware Stats
    cpu_usage = random.randint(10, 45)
    mem_usage = random.randint(30, 60)
    
    return jsonify({
        "system": sys_mon.get_status(),
        "hardware": {
            "cpu": cpu_usage,
            "memory": mem_usage,
            "temp": random.randint(35, 50)
        }
    })

@app.route('/api/traffic')
def get_traffic():
    return jsonify(latest_traffic)

@app.route('/api/alerts')
def get_alerts():
    return jsonify(system_alerts[-5:]) # Return last 5 alerts

if __name__ == '__main__':
    sys_mon.boot_sequence()
    app.run(debug=True, port=5000)
