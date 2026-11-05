"""
FastAPI Dashboard Server for Presage SmartSpectra VitalsGuard.
Exposes REST and streaming biometric endpoints with strict consent gates.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .smartspectra_client import SmartSpectraClient, ConsentError
from .vitals_guard_engine import WellnessEvaluation
import os

app = FastAPI(
    title="Presage SmartSpectra VitalsGuard",
    description="Contactless rPPG Biometric & Ergonomic Biofeedback HUD",
    version="1.0.0"
)

client = SmartSpectraClient()

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>VitalsGuard API Active</h1><p>Visit /api/vitals</p>"

@app.post("/api/consent")
async def set_consent(granted: bool = Query(..., description="User explicit opt-in")):
    try:
        client.grant_user_consent(granted)
        return {"status": "SUCCESS", "consent_active": True}
    except ConsentError as e:
        return JSONResponse(status_code=403, content={"status": "REVOKED", "error": str(e)})

@app.get("/api/vitals")
async def get_live_vitals(stress_level: float = Query(0.2, ge=0.0, le=1.0)):
    try:
        sample = client.capture_vitals_sample(sim_stress_level=stress_level)
        eval_result = WellnessEvaluation(sample)
        return eval_result.to_dict()
    except ConsentError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {
        "status": "UP",
        "service": "Presage SmartSpectra VitalsGuard",
        "consent_active": client.is_consent_active(),
        "privacy_tier": "ephemeral_local_only"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
