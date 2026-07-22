import unittest
import asyncio
import os
import sys

# Adjust import path to include app directory and main app path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app.main import (
    health_check, 
    get_responders, 
    login, 
    analyze_video_frame, 
    analyze_incident_text,
    LoginRequest,
    VideoFrameAnalysisRequest
)
from app.database import SessionLocal

class TestAegisFlowBackend(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        self.db = SessionLocal()

    async def asyncTearDown(self):
        self.db.close()

    async def test_health_check(self):
        """Test the system health check logic directly."""
        res = await health_check()
        self.assertEqual(res["status"], "healthy")
        self.assertIn("timestamp", res)

    async def test_get_responders(self):
        """Test getting the initial list of responders directly from the DB handler."""
        res = await get_responders(self.db)
        self.assertGreater(len(res), 0)
        self.assertEqual(res[0]["id"], "AMB-01")

    async def test_auth_login_fail(self):
        """Test login fails with incorrect credentials."""
        from fastapi import HTTPException
        req = LoginRequest(username="dispatcher", password="wrongpassword")
        with self.assertRaises(HTTPException) as context:
            await login(req, self.db)
        self.assertEqual(context.exception.status_code, 401)

    async def test_auth_login_success(self):
        """Test login succeeds with default credentials."""
        req = LoginRequest(username="dispatcher", password="aegis123")
        res = await login(req, self.db)
        self.assertIn("access_token", res)
        self.assertEqual(res["role"], "dispatcher")

    async def test_incident_ai_triage_mock(self):
        """Test semantic fallback matching for triage classification."""
        fire_res = analyze_incident_text("Help! There is heavy smoke and fire in our building.")
        self.assertEqual(fire_res["category"], "Structure Fire")
        self.assertEqual(fire_res["priority"], "Critical")
        
        accident_res = analyze_incident_text("A major car crash occurred, a truck is leaking gasoline.")
        self.assertEqual(accident_res["category"], "Motor Vehicle Collision")
        self.assertEqual(accident_res["priority"], "Critical")

    async def test_video_analysis(self):
        """Test YOLO multimodal mock analysis returns object tags with confidences."""
        req = VideoFrameAnalysisRequest(frame_b64="mock_data_string")
        res = await analyze_video_frame(req)
        self.assertEqual(res["status"], "success")
        self.assertIn("Smoke (91%)", res["detected_objects"])

if __name__ == "__main__":
    unittest.main()
