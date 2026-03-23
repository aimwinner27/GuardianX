from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random
from models.database import get_db, User, RoleEnum, AlertLog
from utils.auth_utils import require_role
from datetime import datetime

router = APIRouter(prefix="/api/energy", tags=["Energy Management"])

@router.get("/stats")
def get_energy_stats(current_user: User = Depends(require_role([RoleEnum.admin, RoleEnum.technician])), db: Session = Depends(get_db)):
    """Simulates real-time energy usage from IoT sensors in kWh."""
    usage_zones = {
        "Block A (Labs)": random.uniform(10.0, 50.0),
        "Block B (Classes)": random.uniform(5.0, 30.0),
        "Library": random.uniform(8.0, 20.0),
        "Hostel": random.uniform(20.0, 80.0)
    }
    
    total_usage = sum(usage_zones.values())
    status = "normal"
    
    anomalies = []
    # Simple logic for anomaly detection
    for zone, usage in usage_zones.items():
        if usage > 45.0 and zone != "Hostel":
            anomalies.append(zone)
            status = "abnormal"
        elif usage > 75.0 and zone == "Hostel":
            anomalies.append(zone)
            status = "abnormal"
            
    if anomalies:
        alert_msg = f"Abnormal energy spikes detected in: {', '.join(anomalies)}"
        alert = AlertLog(alert_type="energy", message=alert_msg)
        db.add(alert)
        db.commit()

    return {
        "zones": usage_zones,
        "total_usage_kwh": round(float(total_usage), 2),
        "status": status,
        "anomalies": anomalies,
        "timestamp": datetime.utcnow().isoformat()
    }
