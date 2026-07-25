import numpy as np
import os
import time
import threading
from fastapi import FastAPI
from pydantic import BaseModel

# Try importing mujoco
try:
    import mujoco
    import mujoco.viewer
    MUJOCO_AVAILABLE = True
except ImportError:
    MUJOCO_AVAILABLE = False
    print("⚠️ Warning: 'mujoco' module not found. Running in local mathematical calculation mode.")

app = FastAPI(title="NitroGuard 3D MuJoCo Bridge")

class MotionRequest3D(BaseModel):
    targetX: float
    targetY: float
    targetZ: float

# Define 3D Hazard Obstacles (Center XYZ, Radius)
OBSTACLES_3D = [
    {"id": "press_3d", "pos": np.array([5.0, 5.0, 2.0]), "radius": 2.0, "label": "3D Industrial Robotic Press"},
    {"id": "cabinet_3d", "pos": np.array([10.0, 3.0, 1.5]), "radius": 1.5, "label": "High Voltage Terminal"},
    {"id": "conveyor_3d", "pos": np.array([7.0, 11.0, 2.5]), "radius": 2.2, "label": "Automated Gantry"}
]

SAFETY_MARGIN = 0.5

# Initialize MuJoCo Simulation World
model = None
data = None
viewer = None

if MUJOCO_AVAILABLE:
    try:
        # Search for XML in root or subfolder locations
        xml_paths = [
            "factory.xml",
            "my-mcp-server/factory.xml",
            "/home/vishal/NitroGuard_3D_Ubuntu_Bundle/my-mcp-server/factory.xml",
            "/home/vishal/NitroGuard_3D_Ubuntu_Bundle/factory.xml"
        ]
        xml_path = None
        for path in xml_paths:
            if os.path.exists(path):
                xml_path = path
                break

        if xml_path:
            print(f"📦 Loading MuJoCo Model: {xml_path}")
            model = mujoco.MjModel.from_xml_path(xml_path)
            data = mujoco.MjData(model)

            # Launch Passive 3D Visualizer Window
            try:
                viewer = mujoco.viewer.launch_passive(model, data)
                print("🚀 MuJoCo 3D Passive Visualizer Window launched successfully!")
            except Exception as e:
                print(f"⚠️ Could not start MuJoCo visualizer window: {e}")

            # Background Physics step and render sync loop (200 Hz)
            def physics_loop():
                while True:
                    mujoco.mj_step(model, data)
                    if viewer is not None and viewer.is_running():
                        viewer.sync()
                    time.sleep(0.005)

            threading.Thread(target=physics_loop, daemon=True).start()
        else:
            print("⚠️ Could not locate factory.xml in search paths. MuJoCo physics engine disabled.")
    except Exception as e:
        print(f"❌ Failed to load MuJoCo environment: {e}")

@app.post("/solve-3d-cbf")
def solve_3d_cbf(req: MotionRequest3D):
    p_nom = np.array([req.targetX, req.targetY, req.targetZ])
    p_safe = np.copy(p_nom)
    was_corrected = False
    active_obs = None

    # Enforce Control Barrier Functions (CBFs) to deflect coordinates
    for obs in OBSTACLES_3D:
        min_dist = obs["radius"] + SAFETY_MARGIN
        diff = p_safe - obs["pos"]
        dist = np.linalg.norm(diff)

        # 3D Sphere Barrier Constraint: ||p - p_obs|| >= r + margin
        if dist < min_dist:
            was_corrected = True
            unit_vec = diff / (dist if dist > 1e-4 else 1.0)
            p_safe = obs["pos"] + unit_vec * min_dist
            active_obs = {
                "id": obs["id"],
                "label": obs["label"],
                "x": float(obs["pos"][0]),
                "y": float(obs["pos"][1]),
                "z": float(obs["pos"][2]),
                "radius": float(obs["radius"])
            }

    corr_dist = float(np.linalg.norm(p_safe - p_nom))

    # Move the robot joints inside the MuJoCo simulator
    if MUJOCO_AVAILABLE and model is not None and data is not None:
        try:
            # Assign values directly to slide joints in qpos vector
            # robot_x: index 0, robot_y: index 1, robot_z: index 2
            data.qpos[0] = p_safe[0]
            data.qpos[1] = p_safe[1]
            data.qpos[2] = p_safe[2]
            
            # Reset velocities to stop immediately at destination
            data.qvel[0] = 0
            data.qvel[1] = 0
            data.qvel[2] = 0
        except Exception as e:
            print(f"⚠️ Error updating MuJoCo telemetry: {e}")

    # Build 3D obstacles list for visualizer widgets
    obstacles_list = [
        {
            "id": obs["id"],
            "label": obs["label"],
            "x": float(obs["pos"][0]),
            "y": float(obs["pos"][1]),
            "z": float(obs["pos"][2]),
            "radius": float(obs["radius"])
        }
        for obs in OBSTACLES_3D
    ]

    return {
        "nominalTarget": {"x": req.targetX, "y": req.targetY, "z": req.targetZ},
        "safeTarget": {"x": float(p_safe[0]), "y": float(p_safe[1]), "z": float(p_safe[2])},
        "wasCorrected": was_corrected,
        "activeObstacle": active_obs,
        "correctionDistance": round(corr_dist, 2),
        "obstacles": obstacles_list
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
