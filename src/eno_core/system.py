import time
import uuid
import logging
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class SystemMonitor:
    def __init__(self, system_name="ENO-CORE"):
        self.system_id = uuid.uuid4()
        self.system_name = system_name
        self.active_modules = []
        self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(self.system_name)

    def boot_sequence(self):
        """Simulates a high-tech system boot sequence."""
        print(f"{Fore.CYAN}Initializing {self.system_name} Protocol...{Style.RESET_ALL}")
        time.sleep(0.5)
        self.log_event("KERNEL", "Loading core modules...")
        
        steps = [
            ("MEMORY_ALLOC", "Allocating safe memory block...", 0.3),
            ("SECURE_BOOT", "Verifying cryptographic signatures...", 0.4),
            ("NET_INTERFACE", "Establishing loopback connection...", 0.2),
            ("DEFENSE_GRID", "Activating firewall protocols...", 0.5)
        ]
        
        for module, message, delay in steps:
            time.sleep(delay)
            self.log_event(module, message)
            print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} {message}")
            self.active_modules.append(module)

        print(f"{Fore.CYAN}SYSTEM READY. ID: {self.system_id}{Style.RESET_ALL}")
        print("-" * 50)

    def log_event(self, source, message, level="INFO"):
        """Logs an event securely."""
        log_entry = f"[{source}] {message}"
        if level == "INFO":
            self.logger.info(log_entry)
        elif level == "WARNING":
            self.logger.warning(f"{Fore.YELLOW}{log_entry}{Style.RESET_ALL}")
        elif level == "ERROR":
            self.logger.error(f"{Fore.RED}{log_entry}{Style.RESET_ALL}")

    def get_status(self):
        return {
            "id": str(self.system_id),
            "status": "OPERATIONAL",
            "uptime": time.time(),
            "active_modules": self.active_modules
        }
