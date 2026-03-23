import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models.database import engine, Base, SessionLocal, User, RoleEnum
from routes import auth, gate_pass, reports, crowd, energy

# Create all tables in DB
Base.metadata.create_all(bind=engine)

# Ensure static directories exist
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app = FastAPI(title="GuardianX - Campus Safety System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth.router)
app.include_router(gate_pass.router)
app.include_router(reports.router)
app.include_router(crowd.router)
app.include_router(energy.router)

# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize Mock Data
def init_mock_data():
    db = SessionLocal()
    try:
        # Check if users exist
        if not db.query(User).first():
            print("Initializing mock users...")
            mock_users = [
                User(register_or_name="STU123", dob="2000-01-01", role=RoleEnum.student),
                User(register_or_name="Admin John", dob="1980-05-15", role=RoleEnum.admin),
                User(register_or_name="Guard Mike", dob="1975-10-20", role=RoleEnum.security),
                User(register_or_name="Tech Sarah", dob="1990-03-30", role=RoleEnum.technician),
                User(register_or_name="732925AMR036", dob="2007-12-27", role=RoleEnum.student),
            ]
            db.add_all(mock_users)
            db.commit()
            print("Mock users created successfully!")
    finally:
        db.close()

# Run initialization
init_mock_data()

# Frontend Routes
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
