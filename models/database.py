from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLEnum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./guardianx.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    student = "student"
    admin = "admin"
    security = "security"
    technician = "technician"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    register_or_name = Column(String, unique=True, index=True) # register number for student, name for others
    dob = Column(String) # For simple authentication as requested
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.student)

class GatePass(Base):
    __tablename__ = "gate_passes"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    reason = Column(String)
    out_time = Column(DateTime)
    expected_return_time = Column(DateTime)
    status = Column(String, default="pending") # pending, approved, rejected, exited, returned
    qr_code_path = Column(String, nullable=True) # path to generated QR image
    actual_return_time = Column(DateTime, nullable=True)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
    location = Column(String)
    priority = Column(String, default="normal") # normal, high, critical
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="open") # open, resolved

class AlertLog(Base):
    __tablename__ = "alert_logs"
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String) # suspicious, crowd, energy
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
