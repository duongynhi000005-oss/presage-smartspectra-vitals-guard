"""
VitalsGuard Assessment Engine: Evaluates physiological signals and recommends ergonomic pauses.
NOT A MEDICAL DEVICE: For wellness, productivity, and ergonomic biofeedback only.
"""
from typing import Dict, Any, List
from .smartspectra_client import PhysiologicalSignals

class WellnessEvaluation:
    def __init__(self, signals: PhysiologicalSignals):
        self.signals = signals
        self.status = "OPTIMAL_FLOW"
        self.alert_level = "GREEN"
        self.recommendations: List[str] = []
        self._evaluate()

    def _evaluate(self):
        # 1. Stress & Autonomic Tone Evaluation via HRV and Pulse
        if self.signals.hrv_rmssd_ms < 25.0 and self.signals.pulse_bpm > 95.0:
            self.status = "COGNITIVE_SATURATION_STRESS"
            self.alert_level = "AMBER"
            self.recommendations.append("Autonomic stress elevated (low HRV). Take 3 deep diaphragmatic box breaths.")

        # 2. Visual & Cognitive Fatigue Evaluation via PERCLOS
        if self.signals.perclos_fatigue_score > 0.22:
            self.status = "DROWSINESS_OR_EYE_STRAIN"
            self.alert_level = "RED" if self.signals.perclos_fatigue_score > 0.35 else "AMBER"
            self.recommendations.append("Blink frequency slowed (eye fatigue detected). Look at an object 20 feet away for 20 seconds.")

        # 3. Respiration Hyperventilation
        if self.signals.respiration_rate_brpm > 24.0:
            self.recommendations.append("Breathing rate accelerated. Pace your breathing to 6 breaths per minute.")

        # Default wellness state
        if not self.recommendations:
            self.status = "OPTIMAL_FLOW_STATE"
            self.alert_level = "GREEN"
            self.recommendations.append("Physiological state balanced. In the zone!")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.signals.timestamp_ms,
            "metrics": {
                "pulse_bpm": self.signals.pulse_bpm,
                "hrv_rmssd_ms": self.signals.hrv_rmssd_ms,
                "respiration_brpm": self.signals.respiration_rate_brpm,
                "fatigue_index": self.signals.perclos_fatigue_score,
                "signal_quality": self.signals.signal_quality_snr
            },
            "evaluation": {
                "status": self.status,
                "alert_level": self.alert_level,
                "recommendations": self.recommendations
            },
            "disclaimer": "Non-Medical Device: For ergonomic, workplace wellness, and attention biofeedback only. Not intended for diagnosis, treatment, or cure of any medical condition."
        }
