# AegisFlow: Next-Gen Emergency Dispatch & Incident Triage Engine

AegisFlow is a production-grade, AI-native crisis coordination platform designed for public safety emergency responders (911/112), municipal networks, and private campuses. It fuses **ambient audio classification**, **real-time Whisper voice transcription**, **multimodal YOLOv8 video analysis**, and **Gemini 1.5 Agentic RAG** to automatically triage incoming emergencies, map routes, and allocate assets.

---

## 1. System Architecture

```text
Caller / Bystander
   │
   │ [Audio stream via WebSocket & bystander video stream via WebRTC]
   ▼
Next.js Frontend (Port 3000)
   │
   │ [Secure API calls & WebSocket pipeline]
   ▼
FastAPI Backend (Port 8000)
   ├── SQLite + SQLAlchemy (Incident history & Audit logs)
   ├── YAMNet Acoustic sound classifier (screams, fire, crashes)
   ├── YOLOv8 Multimodal hazard classifier (smoke, flames, trauma)
   └── Gemini 1.5 Agentic Parser & RAG Engine
           │
           ▼
Dispatcher Dashboard (Live GIS, Routing paths, AI priorities)
```

---

## 2. Project Directory Structure

```text
aegisflow/
├── run_dev.bat             # Combined local development launcher (Windows)
├── docker-compose.yml      # Orchestration for containerized deployments
├── client/                 # Next.js Frontend App
│   ├── src/app/
│   │   ├── page.js         # Unified Dispatch Dashboard & Login UI
│   │   ├── globals.css     # CSS Styling imports
│   │   └── layout.js       # HTML meta layouts
│   ├── public/
│   │   └── accident.png    # Ingested bystander camera feed frame
│   └── Dockerfile          # Frontend container build config
└── server/                 # FastAPI Python Backend
    ├── app/
    │   ├── main.py         # REST Endpoints & WebSocket handler
    │   └── database.py     # SQLAlchemy models & SQLite config
    ├── tests/
    │   └── test_backend.py # Backend test suite
    ├── Dockerfile          # Backend container build config
    └── requirements.txt    # Python dependencies list
```

---

## 3. Quickstart & Installation

### Option A: Local Dev Execution (Recommended)
1. Ingest the environment configuration by creating a `.env` file under `/server` (see `/server/.env.example`).
2. Run the unified launcher script:
   ```cmd
   run_dev.bat
   ```
3. Open your browser:
   * **Dashboard & Login UI**: `http://localhost:3000`
   * **FastAPI Interactive Docs**: `http://localhost:8000/docs`

### Option B: Docker Container Deployment
1. Set the `GEMINI_API_KEY` environment variable in your terminal.
2. Spin up the container services:
   ```bash
   docker-compose up --build
   ```
3. The application will map to `http://localhost:3000`.

---

## 4. API Documentation

### Authentication Routing
* `POST /api/auth/login` - Authenticate dispatcher or admin credentials. Returns JWT bearer token.
  - Request body: `{ "username": "admin", "password": "aegis123" }`

### Incident Operations
* `GET /api/incidents` - Get all persistent incidents. Supports searching (`?search=text`) and filtering (`?priority=Critical&status=Active`).
* `POST /api/incidents` - Log new incoming incident. Triggers the Gemini parser.
* `PATCH /api/incidents/{id}` - Modify priority, status, or summary.
* `POST /api/incidents/{id}/export` - Generates a secure encrypted PDF log.

### Resource Fleet Management
* `GET /api/responders` - Fetch coordinates and status list of all emergency vehicles.
* `POST /api/responders/{id}/dispatch?incident_id={id}` - Assign responder unit to active incident.

### System Telemetry & Diagnostics
* `GET /health` - Basic health check endpoint.
* `GET /api/system/telemetry` - Fetches CPU, Memory, and AI processing speeds.

---

## 5. Mock Credentials for Demo
* **Admin Login**: Username: `admin` | Password: `aegis123`
* **Dispatcher Login**: Username: `dispatcher` | Password: `aegis123`

# AegisFlow Project Setup
# Active development logs initialized.
# Local testing verified: python -m unittest tests/test_backend.py