from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from models.database import get_db, User, RoleEnum
from models.schema import UserCreate, UserResponse, LoginRequest, Token
from utils.auth_utils import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.register_or_name == user.register_or_name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # In a real app we'd hash the DOB/password. Here we store plain for hackathon demo.
    new_user = User(
        register_or_name=user.register_or_name,
        dob=user.dob,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.register_or_name == login_req.register_or_name).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if user.dob != login_req.dob:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
