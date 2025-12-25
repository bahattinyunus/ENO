import base64
import hashlib
from colorama import Fore, Style

class SecureChannel:
    def __init__(self, channel_id="SEC-001"):
        self.channel_id = channel_id
        self.is_encrypted = True
        self.session_key = self._generate_session_key()

    def _generate_session_key(self):
        """Generates a pseudo-random session key for visual purposes."""
        return hashlib.sha256(self.channel_id.encode()).hexdigest()[:16]

    def transmit(self, data):
        """Simulates sending encrypted data."""
        if not self.is_encrypted:
            print(f"{Fore.RED}[WARNING] Channel unencrypted!{Style.RESET_ALL} Sending plaintext.")
            return data
        
        encrypted_data = self._encrypt(data)
        print(f"{Fore.BLUE}[TX] {self.channel_id} >> {encrypted_data}{Style.RESET_ALL}")
        return encrypted_data

    def receive(self, encrypted_data):
        """Simulates receiving and decrypting data."""
        decrypted_data = self._decrypt(encrypted_data)
        print(f"{Fore.GREEN}[RX] {self.channel_id} << {decrypted_data}{Style.RESET_ALL}")
        return decrypted_data

    def _encrypt(self, plaintext):
        """Simple mockup encryption (Base64 + inversion) for visualization."""
        # Using Base64 to make it look 'encoded' but readable if needed for debugging
        encoded = base64.b64encode(plaintext.encode()).decode()
        return f"ENC({encoded})"

    def _decrypt(self, ciphertext):
        if not ciphertext.startswith("ENC("):
            return "ERROR: INVALID PROTOCOL"
        
        encoded = ciphertext[4:-1]
        try:
            return base64.b64decode(encoded).decode()
        except:
            return "ERROR: DECRYPTION FAILED"
