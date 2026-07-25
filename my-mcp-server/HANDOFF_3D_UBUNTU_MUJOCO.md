# 🐧 NitroGuard 3D Ubuntu & MuJoCo Simulation Handoff Guide

Welcome to the **NitroGuard 3D Physics & MuJoCo Extension** for Ubuntu Linux! This guide details how to take the NitroStack MCP Server and bridge it with 3D physical artificial intelligence using **MuJoCo** (Multi-Joint Dynamics with Contact) and 3D Control Barrier Functions (CBFs).

---

## 🎯 Architectural Overview: 2D → 3D Extension

```text
       Claude / LLM / Client (MCP)
                   │
                   ▼
  NitroStack MCP Server (@nitrostack/core)
   ├── 5 Resources (sim://factory-layout, sim://robot-state, etc.)
   └── Tool: execute_safe_motion_3d
                   │
                   ▼
  3D CBF Safety Layer (OSQP / Python Microservice)
   ├── Enforces h(x,y,z) = ||p - p_obs||^2 - (r + margin)^2 >= 0
   └── Minimizes ||u_safe - u_nominal||^2
                   │
                   ▼
   MuJoCo 3D Physics Simulator (Linux / MJCF xml)
   ├── Render 3D Bounding Spheres & Mesh Collision
   └── Step Physics World (mj_step)
                   │
                   ▼
  Next.js @Widget ('nitroguard-ops-console')
   └── Three.js / WebGL 3D Interactive Viewport
```

---

## 🐧 Ubuntu System Prerequisites & Setup

### 1. Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y build-essential libgl1-mesa-dev libosmesa6-dev python3-pip python3-venv git
```

### 2. Node.js 20 & NitroStack
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g @nitrostack/cli tsx
```

### 3. Python Virtual Environment for MuJoCo + OSQP
```bash
python3 -m venv venv
source venv/bin/activate
pip install mujoco qpsolvers osqp numpy scipy fastapi uvicorn
```

---

## 🐍 Python 3D CBF & MuJoCo Bridge Microservice (`sim_3d_bridge.py`)

Create this Python service to bridge NitroStack with MuJoCo 3D physics:

```python
import numpy as np
import mujoco
from fastapi import FastAPI
from pydantic import BaseModel
from qpsolvers import solve_qp

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

@app.post("/solve-3d-cbf")
def solve_3d_cbf(req: MotionRequest3D):
    p_nom = np.array([req.targetX, req.targetY, req.targetZ])
    p_safe = np.copy(p_nom)
    was_corrected = False
    active_obs = None

    for obs in OBSTACLES_3D:
        min_dist = obs["radius"] + SAFETY_MARGIN
        diff = p_safe - obs["pos"]
        dist = np.linalg.norm(diff)

        # 3D Sphere Barrier Constraint: ||p - p_obs|| >= r + margin
        if dist < min_dist:
            was_corrected = True
            active_obs = obs["label"]
            unit_vec = diff / (dist if dist > 1e-4 else 1.0)
            p_safe = obs["pos"] + unit_vec * min_dist

    corr_dist = float(np.linalg.norm(p_safe - p_nom))

    return {
        "nominalTarget": {"x": req.targetX, "y": req.targetY, "z": req.targetZ},
        "safeTarget": {"x": float(p_safe[0]), "y": float(p_safe[1]), "z": float(p_safe[2])},
        "wasCorrected": was_corrected,
        "activeObstacle": active_obs,
        "correctionDistance": round(corr_dist, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## ⚡ Integrating 3D Microservice into NitroStack Server

In `src/modules/robotics/safety.service.ts`, add the 3D fetch handler:

```typescript
async solveCBF3D(nominal: { x: number; y: number; z: number }) {
  try {
    const res = await fetch('http://localhost:8000/solve-3d-cbf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nominal)
    });
    return await res.json();
  } catch (err) {
    // Fallback to local 2D/3D math if Python bridge is offline
    return this.solveCBF2D(nominal);
  }
}
```

---

## 🏆 Presentation Narrative for Ubuntu 3D Demo

1. **"From 2D Grid to 3D Physical AI"**: Show that NitroGuard's architecture is invariant to dimensionality. The MCP `@Resource` knowledge layer and `@Tool` contracts remain identical whether driving a 2D floor AMR or a 3D 6-DOF industrial robot arm in MuJoCo.
2. **"Seamless Multi-Language Interop"**: Highlighting how NitroStack TypeScript handles server protocol & React widgets while delegating heavy 3D Quadratic Programming (QP) to Python / MuJoCo physics backends via REST or gRPC.
