from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time
import random
import threading
from src.eno_core.system import SystemMonitor
from src.eno_net.secure_channel import SecureChannel
from src.eno_sim.threat_detector import ThreatDetector
from src.eno_sim.tactical_unit import TacticalUnit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eno-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Core Systems
sys_mon = SystemMonitor(system_name="ENO-COMMAND-NODE")
channel = SecureChannel(channel_id="SAT-LINK-7")
detector = ThreatDetector(sensitivity_level=3)

# Initialize Tactical Units (Centered roughly around Turkey or a generic ops area)
units = [
    TacticalUnit("TB2-01", "UAV", 39.9334, 32.8597), # Ankara
    TacticalUnit("TB2-02", "UAV", 41.0082, 28.9784), # Istanbul
    TacticalUnit("UGV-ALPHA", "UGV", 37.0000, 35.3213)  # Adana
]

# Shared State
latest_traffic = []

def simulation_tick():
    """Background task to push real-time updates."""
    sys_mon.boot_sequence()
    
    sample_messages = [
        "Telemetry: OK", "Heartbeat: Active", "Syncing...", 
        "DROP DATABASE credentials", # Threat
        "Target Acquired", "Lost Signal", "EXEC: /bin/sh", # Threat
        "Routine Patrol"
    ]

    while True:
        socketio.sleep(1) # Non-blocking sleep for SocketIO
        
        # 1. Update Units & Emit Positions
        unit_data = []
        for unit in units:
            unit.update_position()
            unit_data.append(unit.get_telemetry())
        
        socketio.emit('map_update', unit_data)

        # 2. Network Traffic Sim
        if random.random() < 0.4: # 40% chance of message per tick
            msg = random.choice(sample_messages)
            timestamp = time.strftime("%H:%M:%S")
            is_threat = detector.scan_network_traffic(msg)
            
            log_entry = {
                "time": timestamp,
                "message": msg,
                "encrypted": channel.transmit(msg),
                "status": "THREAT" if is_threat else "SECURE"
            }
            
            socketio.emit('traffic_event', log_entry)
            
            if is_threat:
                sys_mon.log_event("IDS", f"Threat detected: {msg}", "WARNING")
                socketio.emit('alert_event', {"time": timestamp, "alert": f"Malicious Signature: {msg}"})

        # 3. System Stats (Push every 2 seconds roughly)
        if int(time.time()) % 2 == 0:
             stats = {
                "system": sys_mon.get_status(),
                "hardware": {
                    "cpu": random.randint(10, 55),
                    "memory": random.randint(30, 65),
                    "temp": random.randint(40, 55)
                }
            }
             socketio.emit('status_update', stats)

@socketio.on('connect')
def handle_connect():
    print('Client Connected')
    emit('system_message', {'data': 'Connected to ENO Command Node'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start background thread
    socketio.start_background_task(simulation_tick)
    socketio.run(app, debug=True, port=5000)
