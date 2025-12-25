import unittest
from src.eno_core.system import SystemMonitor
from src.eno_net.secure_channel import SecureChannel

class TestEnoCore(unittest.TestCase):
    def test_system_status(self):
        sys = SystemMonitor()
        status = sys.get_status()
        self.assertEqual(status["status"], "OPERATIONAL")
        self.assertIsNotNone(status["id"])

    def test_encryption_integrity(self):
        channel = SecureChannel()
        message = "Test Message 123"
        encrypted = channel.transmit(message)
        decrypted = channel.receive(encrypted)
        self.assertEqual(message, decrypted)
        self.assertNotEqual(message, encrypted)

if __name__ == '__main__':
    unittest.main()
