import json
import time
import socket
import asyncio
import websockets
import numpy as np

def get_local_wifi_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

WIFI_IP = get_local_wifi_ip()
WS_URL = f"ws://{WIFI_IP}:8000/ws/stream"
LANDMARK_FILE = "data/landmarks/squat/squat_08_clip00.json"

async def run_wifi_trace():
    print(f"Detected Physical Wi-Fi LAN IP: {WIFI_IP}")
    print(f"Connecting to Physical Wi-Fi WebSocket: {WS_URL}...")
    print(f"Loading landmark sequence from {LANDMARK_FILE}...")
    with open(LANDMARK_FILE, "r") as f:
        clip_data = json.load(f)
    landmarks_seq = clip_data["landmarks"]

    async with websockets.connect(WS_URL) as ws:
        print(f"Connected via Wi-Fi Interface! Streaming {len(landmarks_seq)} real athlete squat frames...\n")
        
        latencies = []

        header = f"{'Frame':>5} | {'Latency':>10} | {'Reps':>4} | {'Stage':>11} | {'Flexion':>8} | {'FPPA':>7} | {'Alert Message':<28} | {'PoseC3D'}"
        print(header)
        print("-" * len(header))

        for idx, lms in enumerate(landmarks_seq):
            frame_msg = {
                "frame_idx": idx,
                "landmarks": lms,
                "width": 640,
                "height": 480
            }
            t_send = time.perf_counter()
            await ws.send(json.dumps(frame_msg))
            resp_text = await ws.recv()
            t_recv = time.perf_counter()

            lat_ms = (t_recv - t_send) * 1000.0
            latencies.append(lat_ms)

            resp = json.loads(resp_text)
            stage = resp.get("stage", "N/A")
            reps = resp.get("reps", 0)
            flex = resp.get("knee_flexion", 0.0)
            fppa = resp.get("fppa", 0.0)
            alert = resp.get("form_alert", {}).get("message", "N/A")
            pose = resp.get("posec3d", {}).get("display_name", "N/A")
            rep_event = resp.get("rep_event")

            log_str = f"{idx:5d} | {lat_ms:8.2f} ms | {reps:4d} | {stage:>11} | {flex:7.1f}° | {fppa:6.1f}° | {alert:<28} | {pose}"
            if rep_event:
                log_str += f"  <-- [REP {rep_event['rep_number']} COMPLETED! Min Depth: {rep_event['min_flexion']}°]"
            print(log_str)

        lat_arr = np.array(latencies)
        print("\n" + "=" * 70)
        print(f"        PHYSICAL WI-FI LAN INTERFACE ({WIFI_IP}) BENCHMARK")
        print("=" * 70)
        print(f"Total Frames Streamed  : {len(lat_arr)}")
        print(f"Mean Round-Trip Latency: {lat_arr.mean():.2f} ms")
        print(f"Median Latency (p50)   : {np.median(lat_arr):.2f} ms")
        print(f"p90 Latency            : {np.percentile(lat_arr, 90):.2f} ms")
        print(f"p95 Latency            : {np.percentile(lat_arr, 95):.2f} ms")
        print(f"p99 Latency            : {np.percentile(lat_arr, 99):.2f} ms")
        print(f"Min Latency            : {lat_arr.min():.2f} ms")
        print(f"Max Latency (Spike)    : {lat_arr.max():.2f} ms")
        print(f"Frames > 33.3ms (Drop) : {np.sum(lat_arr > 33.33)} / {len(lat_arr)} ({np.sum(lat_arr > 33.33)/len(lat_arr)*100:.1f}%)")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_wifi_trace())
