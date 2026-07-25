"""
sim_bridge.py
FastAPI bridge between NitroStack TypeScript server and MuJoCo Physics Engine.

Threading architecture:
- Main Thread: MuJoCo viewer rendering loop & physics step (GLFW requires main thread)
- Background Thread: FastAPI / Uvicorn HTTP server
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

from robot_controller import apply_velocity_command
from state_reader import read_state

# ── Model & Data ────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "amr_factory.xml")

print(f"📦 Loading MuJoCo Model: {MODEL_PATH}")
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path(MODEL_PATH)
data = mujoco.MjData(model)

state_lock = threading.Lock()

# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(title="NitroGuard MuJoCo Bridge", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    linearVelocity: float
    angularVelocity: float = 0.0
    nstep: int = 10

OBSTACLES = [
    {"id": "pressA",   "label": "Industrial Robotic Press", "x": 5.0,  "y": 5.0,  "radius": 2.0},
    {"id": "cabinet",  "label": "High Voltage Cabinet",     "x": 10.0, "y": 3.0,  "radius": 1.5},
    {"id": "conveyor", "label": "Automated Gantry",         "x": 7.0,  "y": 11.0, "radius": 2.2},
]

@app.post("/apply_command")
def apply_command(cmd: CommandRequest):
    with state_lock:
        apply_velocity_command(data, cmd.linearVelocity, cmd.angularVelocity)
        mujoco.mj_step(model, data, cmd.nstep)
        return read_state(data, status="MOVING")

@app.get("/robot_state")
def robot_state():
    with state_lock:
        return read_state(data)

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
    print(f"🌐 Starting FastAPI HTTP server on http://0.0.0.0:{port}")

    # Run Uvicorn in a background thread
    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    # Launch Passive 3D Viewer on MAIN THREAD
    try:
        print("🚀 Launching MuJoCo 3D Visualizer Window on Main Thread...")
        with mujoco.viewer.launch_passive(model, data) as viewer:
            while viewer.is_running():
                step_start = time.time()
                with state_lock:
                    mujoco.mj_step(model, data)
                    viewer.sync()
                # Maintain ~60 FPS / physics pacing
                time_until_next_frame = model.opt.timestep - (time.time() - step_start)
                if time_until_next_frame > 0:
                    time.sleep(time_until_next_frame)
    except Exception as e:
        print(f"⚠️  Visualizer exited or failed to launch (headless?): {e}")
        # If visualizer fails or is closed, keep physics stepping on main thread
        while True:
            with state_lock:
                mujoco.mj_step(model, data)
            time.sleep(0.005)
