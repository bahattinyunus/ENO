import random
from colorama import Fore, Style

class ThreatDetector:
    def __init__(self, sensitivity_level=5):
        self.sensitivity = sensitivity_level
        self.known_threats = ["SIG-INT-001", "MALWARE-X", "UNAUTHORIZED_ACCESS", "DDOS_PATTERN"]

    def scan_network_traffic(self, traffic_sample):
        """Analyzes a traffic sample for potential threats."""
        print(f"Scanning traffic sample: {traffic_sample[:20]}...")
        
        threat_score = random.randint(0, 10)
        
        if "ENC" not in traffic_sample and "DROP" in traffic_sample:
             # Heuristic rule mockup
             threat_score += 2

        if threat_score > self.sensitivity:
            detected_threat = random.choice(self.known_threats)
            self._alert(detected_threat, threat_score)
            return True
        else:
            print(f"{Fore.GREEN}No threats detected. Integrity: {100 - (threat_score * 10)}%{Style.RESET_ALL}")
            return False

    def _alert(self, threat_name, severity):
        print(f"{Fore.RED}[ALERT] Threat Detected: {threat_name} (Severity: {severity}){Style.RESET_ALL}")
        print(f"{Fore.RED} >>> Initiating Countermeasures...{Style.RESET_ALL}")
