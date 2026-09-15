"""
BioMechAI FastAPI Local Backend Bridge
Serves dual-timescale AI fitness analysis:
1. REST endpoint: POST /classify (matching Flutter ExerciseRecognitionService)
2. WebSocket: /ws/stream (real-time 30 Hz repetition tracking, joint angles, and clinical valgus alerts)
3. REST endpoint: GET /health
"""

import os
import time
import json
import socket
import asyncio
import numpy as np
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.config import (
    CLASSES,
    CLASS_DISPLAY_NAMES,
    COCO_MP_MAP,
    BOTTOM_DEPTH_THRESHOLD,
    TOP_RETURN_THRESHOLD,
    VALGUS_LOAD_THRESHOLD,
    VALGUS_FPPA_THRESHOLD,
    KNEE_FLEXION_SANITY_FLOOR,
)
from backend.kinematics import (
    calculate_knee_flexion,
    calculate_fppa_munro,
    validate_landmark_tracking,
    select_optimal_tracking_leg,
    RepetitionStateMachine,
    evaluate_knee_valgus,
    VoiceCoachingEngine,
)
from backend.engine import PoseC3DEngine

app = FastAPI(
    title="BioMechAI Backend API",
    description="Dual-Timescale AI Fitness Analysis & Clinical Injury Prevention",
    version="1.0.0"
)

# Enable CORS for local Wi-Fi, web dashboards, and mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Global PoseC3D AI Engine
engine = PoseC3DEngine(device="cpu")

# ------------------------------------------------------------------------------
# Pydantic Request Models
# ------------------------------------------------------------------------------
class ClassifyRequest(BaseModel):
    landmarks: List[List[List[float]]] = Field(..., description="(T, 33, 3) normalized MediaPipe landmarks")
    fps: Optional[int] = Field(default=30, description="Camera capture frame rate")

class HealthResponse(BaseModel):
    status: str
    model: str
    classes: List[str]
    thresholds: Dict[str, float]

def get_lan_ip() -> str:
    """Auto-detects the host machine's primary physical LAN IPv4 address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

# ------------------------------------------------------------------------------
# REST Endpoints
# ------------------------------------------------------------------------------
@app.get("/", tags=["General"])
def root():
    lan_ip = get_lan_ip()
    return {
        "app": "BioMechAI API",
        "status": "online",
        "version": "1.0.0",
        "host_ip": lan_ip,
        "endpoints": ["/health", "/classify", "/ws/stream", "/latency_test", "/api/pairing", "/pair"]
    }

@app.get("/download/app-debug.apk", tags=["Download"])
def download_apk():
    """Serves the latest compiled Flutter debug APK with HTTP Range & streaming support."""
    apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), r"..\..\biomechai_flutter_latest\build\app\outputs\flutter-apk\app-debug.apk"))
    if os.path.exists(apk_path):
        return FileResponse(apk_path, media_type="application/vnd.android.package-archive", filename="app-debug.apk")
    raise HTTPException(status_code=404, detail=f"APK not found at {apk_path}")

@app.get("/api/pairing", tags=["Pairing"])
def dynamic_pairing_config():
    """
    Dynamic server discovery endpoint solving router DHCP IP volatility.
    Mobile clients query or scan this to automatically bind to the active host IP.
    """
    lan_ip = get_lan_ip()
    return {
        "status": "ready",
        "server_ip": lan_ip,
        "port": 8000,
        "ws_stream_url": f"ws://{lan_ip}:8000/ws/stream",
        "classify_url": f"http://{lan_ip}:8000/classify",
        "health_url": f"http://{lan_ip}:8000/health",
        "pairing_timestamp": time.time()
    }

@app.get("/api/sample_squat_landmarks", tags=["Diagnostics"])
def get_sample_squat_landmarks():
    """
    Returns 90 frames of verified real-athlete squat keypoints (squat_08_clip00.json)
    for real-motion telemetry streaming benchmarks on physical mobile devices.
    """
    sample_path = "data/landmarks/squat/squat_08_clip00.json"
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail="Sample landmark file not found.")
    with open(sample_path, "r") as f:
        data = json.load(f)
    return {
        "exercise": data.get("exercise", "squat"),
        "total_frames": len(data.get("landmarks", [])),
        "landmarks": data.get("landmarks", [])
    }

@app.get("/pair", response_class=HTMLResponse, tags=["Pairing"])
def mobile_pairing_qr_page():
    lan_ip = get_lan_ip()
    ws_url = f"ws://{lan_ip}:8000/ws/stream"
    api_url = f"http://{lan_ip}:8000"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BioMechAI - Dynamic Server Pairing</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; text-align: center; }}
    .card {{ background: #1e293b; border-radius: 16px; padding: 28px; max-width: 440px; margin: 0 auto; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
    h1 {{ color: #38bdf8; font-size: 22px; margin-bottom: 8px; }}
    p {{ color: #94a3b8; font-size: 14px; margin-bottom: 20px; line-height: 1.5; }}
    #qrcode {{ background: white; padding: 16px; border-radius: 12px; display: inline-block; margin: 16px auto; }}
    .ip-badge {{ background: #0284c7; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-family: monospace; font-size: 16px; display: inline-block; margin-bottom: 12px; }}
    .url-text {{ color: #a5f3fc; font-family: monospace; font-size: 13px; word-break: break-all; margin-top: 8px; }}
    .btn {{ display: block; background: #38bdf8; color: #0f172a; text-decoration: none; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 20px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>📲 BioMechAI Dynamic Pairing</h1>
    <p>Scan this QR code from your mobile device or Flutter app to dynamically bind to the active host server without hardcoding IP addresses.</p>
    <div class="ip-badge">{lan_ip}:8000</div>
    <div id="qrcode"></div>
    <div class="url-text">{api_url}</div>
    <a class="btn" href="/latency_test">Open Real-Motion Wi-Fi Benchmark &rarr;</a>
  </div>
  <script>
    new QRCode(document.getElementById("qrcode"), {{
      text: "{api_url}",
      width: 220,
      height: 220,
      colorDark: "#0f172a",
      colorLight: "#ffffff",
      correctLevel: QRCode.CorrectLevel.H
    }});
  </script>
</body>
</html>
"""

@app.get("/health", response_model=HealthResponse, tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "model": "PoseC3D-v5-SlowOnly-R50",
        "classes": CLASSES,
        "thresholds": {
            "bottom_depth_threshold": BOTTOM_DEPTH_THRESHOLD,
            "top_return_threshold": TOP_RETURN_THRESHOLD,
            "valgus_load_threshold": VALGUS_LOAD_THRESHOLD,
            "valgus_fppa_threshold": VALGUS_FPPA_THRESHOLD,
        }
    }

@app.get("/api/sample_squat_landmarks", tags=["Diagnostics"])
def get_sample_squat_landmarks():
    """
    Returns 90 consecutive frames of real athlete MediaPipe 33-landmarks
    extracted from squat_08_clip00.json for real-motion latency & kinematic replay.
    """
    sample_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "landmarks", "squat", "squat_08_clip00.json")
    if not os.path.exists(sample_file):
        raise HTTPException(status_code=404, detail="Sample squat landmarks file not found.")
    with open(sample_file, "r") as f:
        data = json.load(f)
    return {
        "status": "success",
        "clip": "squat_08_clip00",
        "frame_count": len(data.get("landmarks", [])),
        "landmarks": data.get("landmarks", [])
    }

@app.get("/latency_test", response_class=HTMLResponse, tags=["Diagnostics"])
def mobile_latency_test_page():
    lan_ip = get_lan_ip()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BioMechAI - Real-Motion Wi-Fi Benchmark</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 16px; margin: 0; }}
    .card {{ background: #1e293b; border-radius: 12px; padding: 18px; margin-bottom: 14px; border: 1px solid #334155; }}
    h1 {{ font-size: 19px; margin-top: 0; color: #38bdf8; display: flex; align-items: center; justify-content: space-between; }}
    p {{ font-size: 13px; color: #94a3b8; line-height: 1.5; margin: 6px 0 14px; }}
    .btn-group {{ display: flex; flex-direction: column; gap: 10px; }}
    button {{ color: white; border: none; padding: 12px 18px; border-radius: 8px; font-size: 15px; font-weight: bold; width: 100%; cursor: pointer; transition: background 0.2s; }}
    .btn-primary {{ background: #0284c7; }}
    .btn-primary:hover {{ background: #0369a1; }}
    .btn-secondary {{ background: #334155; color: #cbd5e1; }}
    .btn-secondary:hover {{ background: #475569; }}
    button:disabled {{ background: #475569 !important; color: #94a3b8 !important; cursor: not-allowed; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 14px; }}
    .stat-box {{ background: #0f172a; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #334155; }}
    .stat-val {{ font-size: 22px; font-weight: bold; color: #38bdf8; }}
    .stat-lbl {{ font-size: 11px; color: #94a3b8; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .pass {{ color: #4ade80 !important; }}
    .warn {{ color: #fbbf24 !important; }}
    .fail {{ color: #f87171 !important; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; }}
    th, td {{ padding: 6px 4px; text-align: left; border-bottom: 1px solid #334155; }}
    th {{ color: #94a3b8; font-weight: 600; }}
    .table-wrap {{ max-height: 280px; overflow-y: auto; margin-top: 12px; border-radius: 8px; border: 1px solid #334155; }}
    .badge {{ background: #0369a1; color: #e0f2fe; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: normal; }}
    .pairing-bar {{ display: flex; justify-content: space-between; align-items: center; background: #0f172a; padding: 10px 14px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 12px; font-size: 12px; }}
    .ip-code {{ font-family: monospace; color: #38bdf8; font-weight: bold; }}
    a.pair-link {{ color: #a5f3fc; text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="pairing-bar">
    <span>Host IP: <span class="ip-code">{lan_ip}:8000</span></span>
    <a class="pair-link" href="/pair">QR Pairing &rarr;</a>
  </div>

  <div class="card">
    <h1>📱 Full-Pipeline Mobile Wi-Fi Test <span class="badge">Dual-Timescale</span></h1>
    <p>Validates real-time 30 Hz kinematics (flexion, Munro FPPA, 4-stage rep FSM) and PoseC3D action recognition across your physical Wi-Fi network.</p>
    <div class="btn-group">
      <button id="realMotionBtn" class="btn-primary" onclick="startTest(true)">🏋️ Stream Real Athlete Squat (90 Frames)</button>
      <button id="syntheticBtn" class="btn-secondary" onclick="startTest(false)">⚡ Synthetic 60-Frame Latency Benchmark</button>
    </div>
  </div>

  <div id="resultsCard" class="card" style="display:none;">
    <h1>📊 Live Telemetry & Latency</h1>
    <div class="grid">
      <div class="stat-box"><div class="stat-val" id="meanVal">--</div><div class="stat-lbl">Mean Latency</div></div>
      <div class="stat-box"><div class="stat-val" id="repsVal">0</div><div class="stat-lbl">Completed Reps</div></div>
      <div class="stat-box"><div class="stat-val" id="minFlexVal">--</div><div class="stat-lbl">Min Flexion (Depth)</div></div>
      <div class="stat-box"><div class="stat-val" id="poseVal">--</div><div class="stat-lbl">PoseC3D Class</div></div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>#</th><th>Latency</th><th>Flexion</th><th>FPPA</th><th>Stage</th><th>Reps</th><th>PoseC3D</th></tr></thead>
        <tbody id="logBody"></tbody>
      </table>
    </div>
  </div>

  <script>
    let isRunning = false;

    async function startTest(isRealMotion) {{
      if (isRunning) return;
      isRunning = true;

      const realBtn = document.getElementById('realMotionBtn');
      const synBtn = document.getElementById('syntheticBtn');
      realBtn.disabled = true;
      synBtn.disabled = true;
      
      const activeBtn = isRealMotion ? realBtn : synBtn;
      activeBtn.innerText = "Loading Telemetry...";
      document.getElementById('resultsCard').style.display = 'block';
      const logBody = document.getElementById('logBody');
      logBody.innerHTML = "";

      let framesToStream = [];

      if (isRealMotion) {{
        try {{
          const res = await fetch('/api/sample_squat_landmarks');
          const clipData = await res.json();
          framesToStream = clipData.landmarks;
        }} catch (err) {{
          alert("Failed to load sample squat frames from server.");
          realBtn.disabled = false;
          synBtn.disabled = false;
          isRunning = false;
          return;
        }}
      }} else {{
        for (let i = 0; i < 60; i++) {{
          const lms = Array(33).fill([0.5, 0.5, 0.0]);
          lms[23] = [0.45, 0.40, 0.0];
          lms[25] = [0.45, 0.65, 0.0];
          lms[27] = [0.45, 0.90, 0.0];
          framesToStream.push(lms);
        }}
      }}

      const wsProtocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${{wsProtocol}}//${{location.host}}/ws/stream`;
      const ws = new WebSocket(wsUrl);

      ws.onopen = async () => {{
        activeBtn.innerText = isRealMotion ? `Streaming ${{framesToStream.length}} Real Squat Frames...` : "Streaming 60 Frames...";
        const latencies = [];
        let minFlexion = 180.0;
        
        for (let i = 0; i < framesToStream.length; i++) {{
          const msg = JSON.stringify({{
            frame_idx: i,
            landmarks: framesToStream[i],
            width: 640,
            height: 480
          }});

          const t0 = performance.now();
          ws.send(msg);

          const respText = await new Promise(resolve => {{
            ws.onmessage = e => resolve(e.data);
          }});
          const t1 = performance.now();
          const lat = t1 - t0;
          latencies.push(lat);

          const resp = JSON.parse(respText);
          const flex = resp.knee_flexion;
          if (flex < minFlexion) minFlexion = flex;

          const tr = document.createElement('tr');
          const latClass = lat < 20 ? 'pass' : (lat < 33.3 ? 'warn' : 'fail');
          const stageClass = resp.stage === 'BOTTOM' ? 'warn' : (resp.stage === 'TOP' ? 'pass' : '');
          
          tr.innerHTML = `<td>${{i}}</td><td class="${{latClass}}">${{lat.toFixed(1)}} ms</td><td>${{flex}}°</td><td>${{resp.fppa}}°</td><td class="${{stageClass}}"><b>${{resp.stage}}</b></td><td style="color:#38bdf8;font-weight:bold;">${{resp.reps}}</td><td>${{resp.posec3d.display_name}}</td>`;
          logBody.appendChild(tr);

          // Rolling summary updates
          const mean = latencies.reduce((a, b) => a + b, 0) / latencies.length;
          const meanEl = document.getElementById('meanVal');
          meanEl.innerText = `${{mean.toFixed(1)}} ms`;
          meanEl.className = `stat-val ${{mean < 25 ? 'pass' : 'warn'}}`;

          document.getElementById('repsVal').innerText = resp.reps;
          document.getElementById('minFlexVal').innerText = `${{minFlexion.toFixed(1)}}°`;
          document.getElementById('poseVal').innerText = resp.posec3d.display_name;

          await new Promise(r => setTimeout(r, 20)); // ~30 FPS realistic camera cadence
        }}

        ws.close();
        realBtn.disabled = false;
        synBtn.disabled = false;
        realBtn.innerText = "🏋️ Stream Real Athlete Squat (90 Frames)";
        synBtn.innerText = "⚡ Synthetic 60-Frame Latency Benchmark";
        isRunning = false;
      }};

      ws.onerror = (e) => {{
        alert("WebSocket connection failed. Ensure phone is on the same Wi-Fi!");
        realBtn.disabled = false;
        synBtn.disabled = false;
        isRunning = false;
      }};
    }}
  </script>
</body>
</html>
"""

@app.post("/classify", tags=["Action Recognition"])
def classify_exercise(payload: ClassifyRequest):
    """
    Direct drop-in endpoint matching Flutter's ExerciseRecognitionService.
    Accepts 33-landmark sequence collected on-device, feeds into PoseC3D v5,
    and returns exercise class with confidence.
    """
    if not payload.landmarks or len(payload.landmarks) < 16:
        raise HTTPException(status_code=400, detail="Landmarks sequence must contain at least 16 frames.")

    result = engine.predict_from_landmarks_sequence(payload.landmarks)
    return result

# ------------------------------------------------------------------------------
# High-Performance WebSocket Streaming Endpoint
# ------------------------------------------------------------------------------
@app.websocket("/ws/stream")
async def websocket_stream_endpoint(websocket: WebSocket):
    """
    Dual-Timescale Streaming Connection:
    - Receives per-frame MediaPipe 33-landmarks at 30 Hz from mobile phone.
    - Fast Path: Instantly computes knee flexion, FPPA valgus, and rep counts.
    - Slow Path: Buffers into rolling 48-frame queue and updates PoseC3D prediction.
    - Returns sub-50ms JSON telemetry packet back to client.
    """
    await websocket.accept()
    print("[WebSocket] Client connected successfully.")

    state_machine = RepetitionStateMachine()
    voice_engine = VoiceCoachingEngine()
    frame_counter = 0

    try:
        while True:
            data_text = await websocket.receive_text()
            data = json.loads(data_text)

            # Extract frame data
            landmarks = data.get("landmarks") # list of 33 [x, y, z] points
            w = data.get("width", 640)
            h = data.get("height", 480)
            frame_idx = data.get("frame_idx", frame_counter)

            if not landmarks or len(landmarks) < 33:
                continue

            # 1. Fast Path: Bilateral Leg Selection for 45°/90° Oblique & Sagittal Viewpoints
            leg_name, (hip_lm, knee_lm, ankle_lm), is_left_leg = select_optimal_tracking_leg(landmarks)

            # Validate optimal leg framing & tracking quality
            is_valid_tracking, tracking_err = validate_landmark_tracking(
                hip_lm, knee_lm, ankle_lm
            )

            # Joint Angle Trigonometry (3D coordinates where available to prevent 2D projection collapse)
            hip_3d = np.array([
                hip_lm[0] * w, 
                hip_lm[1] * h, 
                hip_lm[2] * w if len(hip_lm) > 2 else 0.0
            ], dtype=np.float32)
            knee_3d = np.array([
                knee_lm[0] * w, 
                knee_lm[1] * h, 
                knee_lm[2] * w if len(knee_lm) > 2 else 0.0
            ], dtype=np.float32)
            ankle_3d = np.array([
                ankle_lm[0] * w, 
                ankle_lm[1] * h, 
                ankle_lm[2] * w if len(ankle_lm) > 2 else 0.0
            ], dtype=np.float32)

            knee_flexion = calculate_knee_flexion(hip_3d, knee_3d, ankle_3d)
            fppa_valgus = calculate_fppa_munro(
                (hip_3d[0], hip_3d[1]), 
                (knee_3d[0], knee_3d[1]), 
                (ankle_3d[0], ankle_3d[1]), 
                is_left=is_left_leg
            )

            # Strict anatomical sanity check: reject 2D occlusion glitch (< 35.0 deg)
            is_angle_sane = (knee_flexion >= KNEE_FLEXION_SANITY_FLOOR)

            # 2. Fast Path: Hardened Repetition State Machine
            rep_event = state_machine.update(knee_flexion, frame_idx, is_tracking_valid=is_valid_tracking)

            # 3. Fast Path: Dynamic Knee Valgus / Framing Injury Alert
            if not is_valid_tracking:
                form_alert = {
                    "has_warning": True,
                    "code": "WARN_CAMERA_FRAMING",
                    "message": f"WARN: Step Back! ({tracking_err})",
                    "voice_cue": "Step back and keep feet in frame!"
                }
            else:
                form_alert = evaluate_knee_valgus(knee_flexion, fppa_valgus)

            # 4. Slow Path: Push COCO-17 Keypoints into PoseC3D Buffer
            current_coco = np.zeros((17, 2), dtype=np.float32)
            for c_i, mp_i in enumerate(COCO_MP_MAP):
                current_coco[c_i, 0] = landmarks[mp_i][0] * w
                current_coco[c_i, 1] = landmarks[mp_i][1] * h

            engine.push_coco_keypoints(current_coco)

            # Trigger background PoseC3D inference asynchronously only when worker is idle
            # Throttled to interval of 60 frames (~2s), or 120 frames (~4s) once high confidence is achieved
            current_conf = engine.last_prediction.get("confidence", 0.0)
            inference_interval = 120 if current_conf >= 0.85 else 60
            if engine.is_buffer_full() and (frame_counter % inference_interval == 0) and not engine.is_inferring:
                asyncio.create_task(engine.trigger_async_inference(img_shape=(h, w)))

            pose_pred = engine.last_prediction

            # 5. Emit Real-Time Telemetry Back to Mobile Client
            # Knee flexion is only reported if tracking is valid and angle is anatomically sane (>= 35.0 deg)
            safe_knee_flexion = round(knee_flexion, 1) if (is_valid_tracking and is_angle_sane) else None
            safe_fppa = round(fppa_valgus, 1) if is_valid_tracking else None

            # Evaluate voice coaching trigger (Edge-triggered, cooldown envelopes & load-gated recovery)
            is_under_load = (knee_flexion < VALGUS_LOAD_THRESHOLD) and is_valid_tracking and is_angle_sane
            voice_cue_packet = voice_engine.evaluate(
                rep_event, form_alert, time.time(), is_squatting_under_load=is_under_load
            )
            voice_cue_text = voice_cue_packet.get("text") if voice_cue_packet else None
            if voice_cue_packet is not None:
                print(f"[VoiceCoachingEngine @ {time.strftime('%H:%M:%S')}] Emitted Cue: '{voice_cue_text}' (Priority: {voice_cue_packet.get('priority')}, Frame: {frame_idx})")

            response_payload = {
                "frame_idx": frame_idx,
                "tracked_leg": leg_name,
                "reps": state_machine.rep_count,
                "stage": state_machine.stage,
                "rep_event": rep_event,
                "knee_flexion": safe_knee_flexion,
                "fppa": safe_fppa,
                "is_tracking_valid": is_valid_tracking,
                "tracking_error": tracking_err if not is_valid_tracking else None,
                "form_alert": form_alert,
                "voice_cue": voice_cue_text,
                "voice_cue_detail": voice_cue_packet,
                "posec3d": {
                    "exercise": pose_pred.get("exercise", "buffering"),
                    "display_name": pose_pred.get("display_name", "Buffering..."),
                    "confidence": pose_pred.get("confidence", 0.0),
                    "buffer_pct": pose_pred.get("buffer_pct", 0.0)
                }
            }

            await websocket.send_text(json.dumps(response_payload))
            frame_counter += 1

    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected.")
    except Exception as e:
        print(f"[WebSocket Error]: {e}")
        try:
            await websocket.close()
        except:
            pass
