"""
Unit Test Suite for Presage SmartSpectra VitalsGuard.
Verifies biometric ingestion, consent safety gates, and ergonomic evaluation algorithms.
"""
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from src.smartspectra_client import SmartSpectraClient, ConsentError, PhysiologicalSignals
from src.vitals_guard_engine import WellnessEvaluation

def test_consent_enforcement():
    client = SmartSpectraClient()
    assert not client.is_consent_active()
    
    # Must raise ConsentError if capture attempted before consent
    try:
        client.capture_vitals_sample()
        assert False, "Should have raised ConsentError!"
    except ConsentError:
        pass

    # Grant consent
    client.grant_user_consent(True)
    assert client.is_consent_active()

    # Capture succeeds
    vitals = client.capture_vitals_sample()
    assert isinstance(vitals, PhysiologicalSignals)
    assert 40.0 <= vitals.pulse_bpm <= 200.0
    assert 5.0 <= vitals.hrv_rmssd_ms <= 250.0
    assert 6.0 <= vitals.respiration_rate_brpm <= 45.0
    assert 0.0 <= vitals.perclos_fatigue_score <= 1.0

def test_stress_and_fatigue_evaluation():
    client = SmartSpectraClient()
    client.grant_user_consent(True)

    # 1. Normal state
    normal_signals = PhysiologicalSignals(
        pulse_bpm=72.0,
        hrv_rmssd_ms=48.0,
        respiration_rate_brpm=14.0,
        perclos_fatigue_score=0.08
    )
    eval_normal = WellnessEvaluation(normal_signals)
    assert eval_normal.alert_level == "GREEN"
    assert "OPTIMAL" in eval_normal.status

    # 2. High stress state (elevated pulse + low HRV)
    stressed_signals = PhysiologicalSignals(
        pulse_bpm=105.0,
        hrv_rmssd_ms=18.0,
        respiration_rate_brpm=26.0,
        perclos_fatigue_score=0.10
    )
    eval_stress = WellnessEvaluation(stressed_signals)
    assert eval_stress.alert_level in ("AMBER", "RED")
    assert any("diaphragmatic" in r.lower() or "breathing" in r.lower() for r in eval_stress.recommendations)

    # 3. Severe eye fatigue (high PERCLOS)
    fatigued_signals = PhysiologicalSignals(
        pulse_bpm=68.0,
        hrv_rmssd_ms=40.0,
        respiration_rate_brpm=12.0,
        perclos_fatigue_score=0.38
    )
    eval_fatigue = WellnessEvaluation(fatigued_signals)
    assert eval_fatigue.alert_level == "RED"
    assert any("20-20-20" in r or "20 feet" in r.lower() or "eye" in r.lower() for r in eval_fatigue.recommendations)

def test_consent_revocation():
    client = SmartSpectraClient()
    client.grant_user_consent(True)
    assert client.is_consent_active()

    client.revoke_consent()
    assert not client.is_consent_active()

    try:
        client.capture_vitals_sample()
        assert False, "Should fail after revocation"
    except ConsentError:
        pass

def main():
    print("Running Presage SmartSpectra VitalsGuard Test Suite...")
    test_consent_enforcement()
    print("[PASS] test_consent_enforcement")
    test_stress_and_fatigue_evaluation()
    print("[PASS] test_stress_and_fatigue_evaluation")
    test_consent_revocation()
    print("[PASS] test_consent_revocation")
    print("=" * 60)
    print("ALL 3/3 VITALSGUARD TESTS PASSED (100% SUCCESS)!")
    print("=" * 60)

if __name__ == "__main__":
    main()
