"""
sim_bridge.py
FastAPI bridge between NitroStack TypeScript server and MuJoCo Physics Engine.

Features:
- Main Thread: MuJoCo viewer rendering loop & physics step at ~60 FPS
- Background Thread: FastAPI / Uvicorn HTTP server
- Smooth joint actuation & real-time AMR animation across 3D factory layout
"""

import os
import sys
import time
import threading
import socket
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import mujoco
import mujoco.viewer

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "amr_factory.xml")

print(f"📦 Loading Realistic 3D Factory Model: {MODEL_PATH}")
model = mujoco.MjModel.from_xml_path(MODEL_PATH)
data = mujoco.MjData(model)

state_lock = threading.Lock()

# FastAPI App Setup
app = FastAPI(title="NitroGuard 3D Real Factory MuJoCo Bridge", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    linearVelocity: float = 1.2
    angularVelocity: float = 0.0
    targetX: float = None
    targetY: float = None
    nstep: int = 20

OBSTACLES = [
    {"id": "pressA",   "label": "Industrial Robotic Press", "x": 5.0,  "y": 5.0,  "radius": 2.0},
    {"id": "cabinet",  "label": "High Voltage Cabinet",     "x": 10.0, "y": 3.0,  "radius": 1.5},
    {"id": "conveyor", "label": "Automated Gantry",         "x": 7.0,  "y": 11.0, "radius": 2.2},
]

def read_state_dict():
    # Read robot position from joints: robot_x (idx 0), robot_y (idx 1), robot_z (idx 2)
    x = float(data.qpos[0])
    y = float(data.qpos[1])
    z = float(data.qpos[2])
    return {
        "robotId": "AMR-01",
        "x": round(x, 2),
        "y": round(y, 2),
        "z": round(z, 2),
        "heading": 0.0,
        "linearVelocity": 1.2,
        "angularVelocity": 0.0,
        "battery": 88,
        "mode": "AUTO",
        "status": "MOVING"
    }

@app.post("/apply_command")
def apply_command(cmd: CommandRequest):
    with state_lock:
        # If target coordinates are provided, smoothly nudge joint qpos towards target
        if cmd.targetX is not None and cmd.targetY is not None:
            curr_x = data.qpos[0]
            curr_y = data.qpos[1]
            dx = cmd.targetX - curr_x
            dy = cmd.targetY - curr_y
            dist = np.sqrt(dx * dx + dy * dy)
            if dist > 0.05:
                step_size = min(0.3, dist)
                data.qpos[0] += (dx / dist) * step_size
                data.qpos[1] += (dy / dist) * step_size
        else:
            # Random subtle motion to simulate active drive motor
            data.qpos[0] += np.random.uniform(-0.02, 0.02)
            data.qpos[1] += np.random.uniform(-0.02, 0.02)

        # Step physics world
        for _ in range(cmd.nstep):
            mujoco.mj_step(model, data)

        return read_state_dict()

@app.get("/robot_state")
def robot_state():
    with state_lock:
        return read_state_dict()

@app.get("/factory_layout")
def factory_layout():
    return {
        "bounds": {"width": 15, "height": 15},
        "obstacles": OBSTACLES,
        "safetyMargin": 0.5
    }

def find_available_port(default_port=8000):
    for p in range(default_port, default_port + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p
    return default_port

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", find_available_port(8000)))
    print(f"🌐 Starting Real Factory MuJoCo HTTP server on http://0.0.0.0:{port}")

    # Run Uvicorn in background thread
    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    # Launch Passive 3D Visualizer Window on Main Thread
    try:
        print("🚀 Launching MuJoCo 3D Visualizer Window on Main Thread...")
        with mujoco.viewer.launch_passive(model, data) as viewer:
            while viewer.is_running():
                step_start = time.time()
                with state_lock:
                    mujoco.mj_step(model, data)
                    viewer.sync()
                # Render loop ~60 FPS
                time.sleep(0.016)
    except Exception as e:
        print(f"⚠️ Visualizer exited or failed: {e}")
        while True:
            with state_lock:
                mujoco.mj_step(model, data)
            time.sleep(0.01)
