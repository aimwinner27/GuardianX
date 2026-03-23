from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil

from models.database import get_db, User, RoleEnum, Report, AlertLog
from models.schema import ReportResponse
from utils.auth_utils import get_current_user, require_role
from services.ai_analysis import analyze_report_urgency

router = APIRouter(prefix="/api/reports", tags=["Suspicious Activity"])

@router.post("/", response_model=ReportResponse)
async def create_report(
    description: str = Form(...),
    location: str = Form(...),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Analyze urgency
    priority = analyze_report_urgency(description)
    
    image_path = None
    if image:
        os.makedirs(os.path.join("static", "images", "reports"), exist_ok=True)
        image_path = f"static/images/reports/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
    new_report = Report(
        student_id=current_user.id, # We know who reported, though UI might say 'anonymous' to others
        description=description,
        location=location,
        priority=priority,
        image_path=image_path
    )
    
    db.add(new_report)
    
    if priority in ["high", "critical"]:
        alert = AlertLog(alert_type="suspicious", message=f"{priority.upper()} alert at {location}: {description[:50]}...")
        db.add(alert)
        
    db.commit()
    db.refresh(new_report)
    return new_report

@router.get("/", response_model=list[ReportResponse])
def get_reports(current_user: User = Depends(require_role([RoleEnum.admin, RoleEnum.security])), db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.created_at.desc()).all()

@router.put("/{report_id}/resolve", response_model=ReportResponse)
def resolve_report(report_id: int, current_user: User = Depends(require_role([RoleEnum.admin, RoleEnum.security])), db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    report.status = "resolved"
    db.commit()
    db.refresh(report)
    return report
