import random
from datetime import datetime

class CameraServerMock:
    def __init__(self):
        self.crowd_count = 10
        self.trend = 1
        
    def get_current_crowd_count(self) -> int:
        """Simulate real-time crowd fluctuation"""
        change = random.randint(-5, 8) * self.trend
        self.crowd_count += change
        
        if self.crowd_count < 0:
            self.crowd_count = 0
            self.trend = 1
        elif self.crowd_count > 150:
            self.trend = -1
            
        return self.crowd_count

camera_mock = CameraServerMock()

def analyze_crowd():
    count = camera_mock.get_current_crowd_count()
    status = "normal"
    if count > 100:
        status = "critical"
    elif count > 70:
        status = "high"
        
    return {
        "count": count,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }
