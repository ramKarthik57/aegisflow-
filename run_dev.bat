@echo off
echo ===================================================
echo   AEGISFLOW: AI-Native Crisis Dispatch System
echo ===================================================
echo Starting FastAPI Backend Server on Port 8000...
start cmd /k "cd server && pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo Starting Next.js Frontend Server on Port 3000...
start cmd /k "cd client && npm run dev"

echo Both servers are starting up!
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:3000
echo ===================================================
