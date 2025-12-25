import random
import time
import math

class TacticalUnit:
    def __init__(self, unit_id, unit_type, start_lat, start_lon):
        self.unit_id = unit_id
        self.unit_type = unit_type # 'UAV', 'UGV', 'BS' (Base Station)
        self.lat = start_lat
        self.lon = start_lon
        self.heading = random.uniform(0, 360)
        self.speed = 0.0001 if unit_type == 'UAV' else 0.00005 
        self.status = "ACTIVE"

    def update_position(self):
        """Simulates movement based on heading and speed."""
        if self.status != "ACTIVE":
            return

        # Simple movement logic
        self.lat += self.speed * math.cos(math.radians(self.heading))
        self.lon += self.speed * math.sin(math.radians(self.heading))
        
        # Random heading change for dynamic movement
        if random.random() < 0.1:
            self.heading += random.uniform(-15, 15)

    def get_telemetry(self):
        return {
            "id": self.unit_id,
            "type": self.unit_type,
            "lat": self.lat,
            "lon": self.lon,
            "heading": self.heading,
            "status": self.status
        }
