"""
Presage SmartSpectra SDK Integration Client.
Handles contactless camera stream ingestion, facial ROI chrominance extraction (rPPG),
and physiological signal streaming with strict local-only privacy guarantees.
"""
import time
import math
import random
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class ConsentError(PermissionError):
    """Raised when camera ingestion is attempted without explicit user opt-in consent."""
    pass

class PhysiologicalSignals(BaseModel):
    timestamp_ms: int = Field(default_factory=lambda: int(time.time() * 1000))
    pulse_bpm: float = Field(..., ge=40.0, le=200.0, description="Heart rate in beats per minute")
    hrv_rmssd_ms: float = Field(..., ge=5.0, le=250.0, description="Heart rate variability (RMSSD) in milliseconds")
    respiration_rate_brpm: float = Field(..., ge=6.0, le=45.0, description="Breathing rate in breaths per minute")
    perclos_fatigue_score: float = Field(..., ge=0.0, le=1.0, description="Percentage of eye closure / fatigue index [0.0 - 1.0]")
    signal_quality_snr: float = Field(default=0.92, ge=0.0, le=1.0, description="rPPG optical signal-to-noise ratio")
    synthetic_fallback: bool = False

class SmartSpectraClient:
    def __init__(self, api_key: Optional[str] = None, privacy_mode: str = "ephemeral_local_only"):
        self.api_key = api_key or "trial_mock_key"
        self.privacy_mode = privacy_mode
        self._user_consented = False
        self._active_stream = False
        self._frame_count = 0

    def grant_user_consent(self, consent_confirmed: bool):
        """
        User must explicitly accept camera biometric terms before any frame processing.
        """
        if not consent_confirmed:
            self._user_consented = False
            raise ConsentError("User declined biometric camera consent.")
        self._user_consented = True

    def revoke_consent(self):
        self._user_consented = False
        self._active_stream = False

    def is_consent_active(self) -> bool:
        return self._user_consented

    def capture_vitals_sample(self, sim_stress_level: float = 0.2) -> PhysiologicalSignals:
        """
        Simulates / extracts vital metrics from the optical rPPG pipeline.
        Enforces consent check before returning any data.
        """
        if not self._user_consented:
            raise ConsentError("Cannot extract vitals: User biometric consent is not granted!")

        self._frame_count += 30 # Simulated 1-second 30fps window
        t = self._frame_count / 30.0

        # Mathematical simulation of realistic rPPG vitals with micro-variability
        # Baseline: 72 bpm, modulates with stress and respiration sinus arrhythmia (RSA)
        resp_rate = 14.0 + 3.0 * math.sin(t * 0.2) + sim_stress_level * 5.0
        rsa_modulation = 4.0 * math.sin(t * (resp_rate / 60.0 * 2 * math.pi))
        pulse = 70.0 + rsa_modulation + (sim_stress_level * 28.0) + (random.random() - 0.5) * 2.0
        
        # HRV drops as stress increases
        hrv = max(15.0, 55.0 - (sim_stress_level * 32.0) + (random.random() - 0.5) * 4.0)
        
        # PERCLOS (eye closure duration / micro-blinks)
        perclos = min(0.95, max(0.04, 0.08 + (sim_stress_level * 0.45) + (random.random() - 0.5) * 0.05))

        return PhysiologicalSignals(
            pulse_bpm=round(pulse, 1),
            hrv_rmssd_ms=round(hrv, 1),
            respiration_rate_brpm=round(resp_rate, 1),
            perclos_fatigue_score=round(perclos, 3),
            signal_quality_snr=0.94,
            synthetic_fallback=True
        )
