# SpectraGuard: Contactless Vital Signs & Attention Telemetry HUD
### Built with the Presage SmartSpectra SDK for the DEV.to Presage Challenge 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DEV.to Challenge](https://img.shields.io/badge/DEV.to-Presage%20SmartSpectra%20Challenge-black.svg)](https://dev.to/challenges/presage-2026-11-04)
[![Tests](https://img.shields.io/badge/Unit%20Tests-100%25%20Passing-brightgreen.svg)](test_vitals_guard.py)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local%20WASM%20Only-orange.svg)](#camera-consent--responsible-data-handling)

---

## 1. Executive Summary & Vision

Modern knowledge workers and software engineers spend 8 to 12 hours daily in front of screens, frequently experiencing **visual fatigue, autonomic stress, and posture-induced shallow breathing** without realizing it until burnout strikes.

**SpectraGuard** is an open-source, contactless biofeedback and ergonomic telemetry HUD powered by the **Presage SmartSpectra SDK**. Using a standard commodity laptop webcam (no wearables, no chest straps, and no expensive pulse oximeters), SpectraGuard extracts:
1. **Pulse Rate (rPPG)**: Beats per minute calculated from sub-perceptual facial skin color variations.
2. **Heart Rate Variability (HRV - RMSSD)**: Real-time marker of autonomic stress and cognitive load.
3. **Respiration Rate (BrPM)**: Optical chest/shoulder micro-movement and facial perfusion analysis.
4. **PERCLOS Eye Fatigue Index**: Percentage of eye closure and micro-blink frequency to detect screen drowsiness.

When sustained cognitive overload or eye fatigue is detected, SpectraGuard triggers gentle, proactive recovery prompts (e.g. diaphragmatic box breathing, 20-20-20 visual resets).

---

## 2. System Architecture

```
[Webcam Ingress] ──► [User Consent Gate]
                            │
                            ▼ (If Explicitly Granted)
                 [Presage SmartSpectra WASM]
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          Pulse (rPPG)     HRV       Respiration & Blink
              │             │             │
              └─────────────┼─────────────┘
                            │
                            ▼
             [VitalsGuard Evaluation Engine]
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       [Live Biofeedback HUD]     [Ergonomic Interventions]
```

---

## 3. Camera Consent & Responsible Data Handling

In strict compliance with the **DEV.to Presage Challenge guidelines**:
1. **Explicit User Opt-In**: The camera stream and biometric pipeline remain strictly disabled until the user explicitly clicks *"Accept & Start Ingestion"*.
2. **Zero Video Storage / Transmission**: Raw camera video frames are processed **in-memory inside the client browser / local WebAssembly runtime**. No video bytes, facial images, or raw sensor frames are ever written to disk or transmitted over the internet.
3. **Instant Revocation**: Users can revoke biometric permissions at any moment with one click.
4. **Non-Medical Disclaimer**: SpectraGuard is purely an ergonomic productivity and biofeedback aid. It makes **zero medical claims** and is not designed for diagnosis, clinical monitoring, or medical treatment.

---

## 4. Quickstart & Verification

### Running the Unit Tests
```bash
python test_vitals_guard.py
```
*Output: 100% passing across consent enforcement, physiological boundary validation, and stress evaluation.*

### Launching the Interactive Biofeedback HUD
```bash
pip install -r requirements.txt
python -m src.dashboard_app
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 5. Repository Structure
```
presage_smartspectra_vitals_guard/
├── requirements.txt           # FastAPI, Uvicorn, NumPy, PyTest
├── test_vitals_guard.py       # Full unit test suite (3/3 PASS)
├── src/
│   ├── smartspectra_client.py # Presage SDK integration & consent gate
│   ├── vitals_guard_engine.py # Wellness & cognitive load evaluator
│   └── dashboard_app.py       # Local FastAPI biofeedback HUD
├── web/
│   └── index.html             # Responsive dark-mode telemetry interface
└── README.md                  # Documentation and privacy disclosures
```
