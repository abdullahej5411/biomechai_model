"""
BioMechAI Backend Verification Client
Tests:
1. REST GET /health
2. REST POST /classify (matching Flutter ExerciseRecognitionService)
3. WebSocket /ws/stream (real-time 30 Hz streaming)
"""

import sys
import os
import json
import time
import urllib.request
import asyncio
import websockets

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws/stream"

def test_health():
    print("\n[TEST 1] Testing GET /health...")
    url = f"{BASE_URL}/health"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("  Status code:", resp.status)
        print("  Response:", json.dumps(data, indent=2))
        assert data["status"] == "healthy"
        assert "PoseC3D" in data["model"]
    print("  PASS: /health is operational!")

def test_classify():
    print("\n[TEST 2] Testing POST /classify (Flutter contract)...")
    landmark_file = "data/landmarks/squat/squat_08_clip00.json"
    with open(landmark_file, "r") as f:
        clip_data = json.load(f)
    landmarks_seq = clip_data["landmarks"] # (90, 33, 3)

    url = f"{BASE_URL}/classify"
    payload = json.dumps({"landmarks": landmarks_seq, "fps": 30}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    t0 = time.time()
    with urllib.request.urlopen(req) as resp:
        duration = time.time() - t0
        data = json.loads(resp.read().decode("utf-8"))
        print(f"  Status code: {resp.status} (Took {duration:.2f}s)")
        print("  Response:", json.dumps(data, indent=2))
        assert "exercise" in data
        assert "confidence" in data
        print(f"  PASS: /classify returned: {data['exercise']} ({data['confidence']*100:.1f}%)")

async def test_websocket_stream():
    print("\n[TEST 3] Testing WebSocket /ws/stream (Real-Time 30 Hz Streaming)...")
    landmark_file = "data/landmarks/squat/squat_08_clip00.json"
    with open(landmark_file, "r") as f:
        clip_data = json.load(f)
    landmarks_seq = clip_data["landmarks"]

    async with websockets.connect(WS_URL) as ws:
        print("  Connected to WebSocket stream successfully!")
        
        frames_sent = 0
        latencies = []

        for idx, lms in enumerate(landmarks_seq[:60]):
            frame_msg = {
                "frame_idx": idx,
                "landmarks": lms,
                "width": 640,
                "height": 480
            }
            t_send = time.time()
            await ws.send(json.dumps(frame_msg))
            resp_text = await ws.recv()
            t_recv = time.time()
            latencies.append((t_recv - t_send) * 1000)

            resp_data = json.loads(resp_text)
            frames_sent += 1
            if idx % 15 == 0:
                print(f"  Frame {idx:02d} | Reps: {resp_data['reps']} | Flexion: {resp_data['knee_flexion']}° | FPPA: {resp_data['fppa']}° | Alert: {resp_data['form_alert']['message']} | PoseC3D: {resp_data['posec3d']['display_name']}")

        avg_lat = sum(latencies) / len(latencies)
        print(f"\n  Streamed {frames_sent} frames successfully!")
        print(f"  Average Round-Trip Latency: {avg_lat:.2f} ms per frame")
        assert avg_lat < 100.0, "Latency must be sub-100ms"
        print("  PASS: WebSocket streaming verified!")

def main():
    test_health()
    test_classify()
    asyncio.run(test_websocket_stream())
    print("\n" + "="*60)
    print("  ALL BACKEND INTEGRATION TESTS PASSED (DAY 1 COMPLETE)!")
    print("="*60)

if __name__ == "__main__":
    main()
