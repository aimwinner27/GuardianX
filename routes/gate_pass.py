from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from models.database import get_db, User, RoleEnum, GatePass
from models.schema import GatePassCreate, GatePassResponse
from utils.auth_utils import get_current_user, require_role
from utils.notifiers import generate_qr_code, send_mock_sms

router = APIRouter(prefix="/api/passes", tags=["Gate Pass"])

@router.post("/", response_model=GatePassResponse)
def create_pass(pass_data: GatePassCreate, current_user: User = Depends(require_role([RoleEnum.student])), db: Session = Depends(get_db)):
    new_pass = GatePass(
        student_id=current_user.id,
        reason=pass_data.reason,
        out_time=pass_data.out_time,
        expected_return_time=pass_data.expected_return_time
    )
    db.add(new_pass)
    db.commit()
    db.refresh(new_pass)
    return new_pass

@router.get("/", response_model=list[GatePassResponse])
def get_passes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == RoleEnum.student:
        return db.query(GatePass).filter(GatePass.student_id == current_user.id).all()
    # Admns and Security can see all passes
    return db.query(GatePass).all()

@router.put("/{pass_id}/approve", response_model=GatePassResponse)
def approve_pass(pass_id: int, current_user: User = Depends(require_role([RoleEnum.admin])), db: Session = Depends(get_db)):
    db_pass = db.query(GatePass).filter(GatePass.id == pass_id).first()
    if not db_pass:
        raise HTTPException(status_code=404, detail="Gate pass not found")
    
    db_pass.status = "approved"
    
    # Generate QR Code
    qr_path = generate_qr_code(db_pass.id)
    db_pass.qr_code_path = qr_path
    
    student = db.query(User).filter(User.id == db_pass.student_id).first()
    send_mock_sms("Parent_Phone_Mock", f"Gate pass approved for {student.register_or_name}. Valid until {db_pass.expected_return_time}.")
    
    db.commit()
    db.refresh(db_pass)
    return db_pass

@router.put("/{pass_id}/reject", response_model=GatePassResponse)
def reject_pass(pass_id: int, current_user: User = Depends(require_role([RoleEnum.admin])), db: Session = Depends(get_db)):
    db_pass = db.query(GatePass).filter(GatePass.id == pass_id).first()
    if not db_pass:
        raise HTTPException(status_code=404, detail="Gate pass not found")
    
    db_pass.status = "rejected"
    db.commit()
    db.refresh(db_pass)
    return db_pass

@router.put("/{pass_id}/scan_exit", response_model=GatePassResponse)
def scan_exit(pass_id: int, current_user: User = Depends(require_role([RoleEnum.security])), db: Session = Depends(get_db)):
    db_pass = db.query(GatePass).filter(GatePass.id == pass_id).first()
    if not db_pass:
        raise HTTPException(status_code=404, detail="Gate pass not found")
    
    if db_pass.status != "approved":
        raise HTTPException(status_code=400, detail="Gate pass is not approved or already used.")
    
    db_pass.status = "exited"
    db.commit()
    db.refresh(db_pass)
    
    student = db.query(User).filter(User.id == db_pass.student_id).first()
    send_mock_sms("Parent_Phone_Mock", f"SECURITY ALERT: {student.register_or_name} has exited the campus at {datetime.now()}.")
    
    return db_pass

@router.put("/{pass_id}/scan_return", response_model=GatePassResponse)
def scan_return(pass_id: int, current_user: User = Depends(require_role([RoleEnum.security])), db: Session = Depends(get_db)):
    db_pass = db.query(GatePass).filter(GatePass.id == pass_id).first()
    if not db_pass:
        raise HTTPException(status_code=404, detail="Gate pass not found")
    
    if db_pass.status != "exited":
        raise HTTPException(status_code=400, detail="Student has not exited using this pass.")
    
    db_pass.status = "returned"
    db_pass.actual_return_time = datetime.utcnow()
    db.commit()
    db.refresh(db_pass)
    
    student = db.query(User).filter(User.id == db_pass.student_id).first()
    send_mock_sms("Parent_Phone_Mock", f"SECURITY ALERT: {student.register_or_name} has returned to the campus at {datetime.now()}.")
    
    return db_pass
