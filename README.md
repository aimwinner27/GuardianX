# GuardianX - AI Powered Campus Safety System

A complete hackathon-ready campus safety platform that leverages modern web aesthetics and AI logic (mocked for demo purposes) to handle Gate Passes, Suspicious Activity Reporting, Crowd Management, and Energy Monitoring.

## 🚀 Features & Modules

### 1. Digital Gate Pass System
- **Student Flow**: Fill out out-time, expected return, and reason.
- **Admin Flow**: Approve or reject requests. Approved requests generate a QR code.
- **Security Flow**: Scan QR code to log Exits and Returns.
- **Bonus**: Automated Mock SMS to parents upon exit and return.

### 2. Suspicious Activity Reporting
- **Student Flow**: Anonymously report issues with descriptions and locations.
- **AI Analysis**: Lightweight Natural Language Processing mechanism scans the text for urgency keywords (e.g. "fight", "weapon" -> Critical).
- **Admin Flow**: Views prioritized alerts and resolves them.

### 3. Crowd Management System
- **IoT/Camera Integration Mock**: Simulates a live camera feed counting density at main gates.
- **Threshold Alerts**: If density breaches a limit (e.g., > 100 people), an automatic `CRITICAL` state is engaged.

### 4. Energy Management System
- **Smart Monitoring**: Simulates real-time energy usage across campus zones (Hostel, Labs, Library).
- **Anomaly Detection**: Warns technicians if abnormal spikes occur.

### Bonus Feature: Auto Alert System
- Any module generating a "High" or "Critical" priority event triggers a cross-system Alert Log entry stored in the database.

---

## 🛠 Tech Stack

- **Backend**: Python 3, FastAPI
- **Database**: SQLite (via SQLAlchemy ORM)
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (Single Page Architecture logic inside `app.js` and `api.js`)
- **Styling**: Custom CSS with Glassmorphism, CSS Grid/Flexbox, dynamic animations, and Ionicons.
- **Libraries/APIs**: 
  - `python-jose` (JWT)
  - `passlib` (Hashing)
  - `qrcode` & `Pillow` (QR Generation)

---

## 📂 Project Structure

```text
GuardianX/
│── main.py                   # FastAPI application entry point & router mounting
│── requirements.txt          # Python dependencies
│── guardianx.db              # SQLite Database (Auto-generated)
├── models/
│   ├── database.py           # SQLAlchemy setup and Database Models
│   └── schema.py             # Pydantic schemas for data validation
├── routes/
│   ├── auth.py               # Authentication and Registration API
│   ├── gate_pass.py          # Gate Pass API logic
│   ├── reports.py            # Suspicious Activity API
│   ├── crowd.py              # Crowd density feed API
│   └── energy.py             # Energy monitoring API
├── services/
│   ├── ai_analysis.py        # Text analysis AI mock for reports
│   └── camera_mock.py        # Simulated camera feed data generator
├── utils/
│   ├── auth_utils.py         # JWT creation, decoding, and role dependencies
│   └── notifiers.py          # QR Code generator and mock SMS functions
├── static/
│   ├── css/
│   │   └── styles.css        # Core UI Glassmorphism styles
│   ├── js/
│   │   ├── api.js            # Fetch wrapper for all API calls
│   │   └── app.js            # UI interaction & DOM manipulation
│   └── images/               # Auto-generated QR Codes and uploads
└── templates/
    ├── index.html            # Entry routing script
    ├── login.html            # Auth UI
    └── dashboard.html        # Interactive SPA modules (Cards, Tables, Feeds)
```

---

## ⚙️ Architecture

GuardianX operates as a monolithic web service tailored for rapid hackathon deployment:
1. **Client-Side Rendering**: Vanilla JS dynamically updates `<div class="module-section">` blocks in `dashboard.html` by querying the REST APIs, making navigation instant (like CodeTantra).
2. **RESTful APIs**: FastAPI endpoints heavily utilize Dependency Injection (`Depends`) to extract and verify the JWT token from the `Authorization` header and enforce role constraints (`require_role()`).
3. **Database Layer**: SQLAlchemy interfaces seamlessly with an in-memory or file-based SQLite database. 

---

## 🏁 How to Run

1. **Install Python 3.9+** on your machine.
2. **Navigate** to the project folder (`GuardianX`).
3. **(Optional)** Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Start the Server**:
   ```bash
   uvicorn main:app --reload
   ```
6. **Open Browser** and navigate to:
   [http://localhost:8000](http://localhost:8000)

---

## 👥 Pre-Configured Mock Users

Use these accounts (Username / Date of Birth) to test out role-based navigation:

| Role | Username | Date of Birth |
| :--- | :--- | :--- |
| **Student** | `STU123` | `2000-01-01` |
| **Faculty/Admin** | `Admin John` | `1980-05-15` |
| **Security Guard** | `Guard Mike` | `1975-10-20` |
| **Technician** | `Tech Sarah` | `1990-03-30` |

*Note: For the hackathon demo, the Date of Birth acts functionally as the password field for ease of testing.*
