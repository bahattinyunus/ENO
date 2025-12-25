import time
from src.eno_core.system import SystemMonitor
from src.eno_net.secure_channel import SecureChannel
from src.eno_sim.threat_detector import ThreatDetector
from colorama import Fore, Style

def main():
    print(f"\n{Fore.MAGENTA}=== ENO DEFENSE OS v1.0.4 ==={Style.RESET_ALL}\n")
    
    # 1. Initialize System
    sys_mon = SystemMonitor(system_name="ENO-TACTICAL")
    sys_mon.boot_sequence()
    
    # 2. Establish Secure Comms
    channel = SecureChannel(channel_id="UPLINK-ALPHA")
    
    # 3. Simulate Operations
    messages = [
        "Coordinate update: 34.55, 42.11",
        "Status report: Green",
        "DROP TABLE traffic_logs; -- SQL Injection Attack Attempt" 
    ]
    
    detector = ThreatDetector(sensitivity_level=4)
    
    for msg in messages:
        time.sleep(1)
        print(f"\nProcessing Message: '{msg}'")
        
        # Encrypt & Transmit
        encrypted = channel.transmit(msg)
        
        # Decrypt (Simulate receiver)
        decrypted = channel.receive(encrypted)
        
        # Analyze for Threats
        detector.scan_network_traffic(msg) # Scan plaintext for demo

    print(f"\n{Fore.MAGENTA}=== SESSION TERMINATED ==={Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
