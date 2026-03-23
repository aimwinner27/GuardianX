from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db, User, RoleEnum, AlertLog
from utils.auth_utils import require_role
from services.camera_mock import analyze_crowd

router = APIRouter(prefix="/api/crowd", tags=["Crowd Management"])

@router.get("/status")
def get_crowd_status(current_user: User = Depends(require_role([RoleEnum.admin, RoleEnum.security, RoleEnum.technician])), db: Session = Depends(get_db)):
    """Simulate getting real-time feed metrics from camera."""
    data = analyze_crowd()
    
    if data["status"] in ["high", "critical"]:
        # Log anomaly, but to avoid spam, maybe add throttling in real app.
        alert = AlertLog(alert_type="crowd", message=f"{data['status'].upper()} crowd density detected: {data['count']} people.")
        db.add(alert)
        db.commit()
        
    return data
