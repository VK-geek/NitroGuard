# 🛡️ NitroGuard — AI Execution Gateway & Upstream Safety Interceptor

> **Built for the NitroStack AI Hackathon**  
> *An upstream physical safety gateway connecting local LLMs (Ollama / Llama 3) to real-time 3D MuJoCo physics simulations via NitroStack MCP servers and interactive Next.js widgets.*

---

## 🌟 Overview

Generative AI models are exceptional at high-level semantic reasoning, but lack physical spatial awareness — frequently generating straight-line paths that intersect machinery and hazard zones.

**NitroGuard** acts as an **Upstream Safety Gateway**:
1. **Semantic Task Planning**: A local **Llama 3** LLM (via Ollama) processes natural language prompts (e.g. *"Navigate AMR-01 to Press Cell A"*) and outputs planned destination coordinates.
2. **Nominal Path Generation**: `TrajectoryPlanner` generates the LLM's raw intent path (**Red Dashed Line**).
3. **Upstream Safety Interception**: `SafetyFilter` evaluates **Control Barrier Functions (CBFs)** per waypoint, deflecting dangerous collision vectors into a safe clearance path (**Green Solid Line**).
4. **Real-Time 3D MuJoCo Physics Engine**: The safe velocity commands are dispatched to a Python **MuJoCo 3D Physics Simulator**, driving an Autonomous Mobile Robot (AMR) body inside a rendered 15x15m factory workspace.
5. **Interactive Operations Console**: A sleek Next.js dark-mode widget displaying real-time 2D radar grid views, 3D isometric projections, risk telemetry, and an LLM Mission Chat window.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ 🦙 LOCAL LLM (Ollama / Llama 3)                                          │
│  - Receives prompt: "Move AMR-01 to Press Cell A in SAFEST mode"        │
│  - Evaluates spatial goal & outputs target coordinates (5.2, 5.5)       │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ ⚡ NITROSTACK MCP SERVER (TypeScript Framework)                          │
│  - Tools: execute_safe_movement (secured with ApiKeyGuard & RateLimit)   │
│  - Resources: sim://factory-layout, sim://robot-state, sim://hazard-map │
│  - TrajectoryPlanner: Generates 10 nominal straight-line waypoints       │
│  - SafetyFilter: Applies CBF vector deflections & evaluates risk levels │
└─────────────────────────────────────────────────────────────────────────┘
                                     │ (HTTP /apply_command)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 🐍 MUJOCO 3D PHYSICS SIMULATOR (Python / mujoco-sim)                     │
│  - Loads MJCF Model (models/amr_factory.xml)                             │
│  - Runs 200 Hz Physics Integration Loop (mj_step)                       │
│  - Opens Main-Thread Passive 3D Visualizer Window                        │
│  - Actuates AMR-01 sliding joint forces (fx, fy)                        │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 🖥️ NEXT.JS OPERATIONS CONSOLE WIDGET (http://localhost:3001)             │
│  - Displays Red Dashed (LLM Intent) vs Green Solid (CBF Safe) Paths     │
│  - Live LLM Mission Chat with real-time reasoning feedback              │
│  - Interactive SVG map (mouse click navigation & 2D/3D Iso toggle)      │
│  - Emergency Stop Lock trigger & reset                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js**: v18+
- **Python**: 3.10+
- **Python Dependencies**:
  ```bash
  pip install mujoco fastapi uvicorn numpy
  ```
- **Ollama** (optional for local LLM mode):
  ```bash
  ollama run llama3
  ```

---

### Step 1: Launch the MuJoCo 3D Physics Simulator
In your terminal, start the Python physics bridge:
```bash
cd mujoco-sim
python3 sim_bridge.py
```
> *A 3D graphical **MuJoCo Viewer** window will pop up rendering the factory workspace, cylindrical AMR robot, and hazard zones.*

---

### Step 2: Build & Launch the NitroStack MCP Server & Widget Dev Server
In a second terminal, start the NitroStack development server:
```bash
cd my-mcp-server
npm run dev
```

---

### Step 3: Open the Interactive Operations Console
Open your browser and navigate to:
👉 **[http://localhost:3001/trajectory-viewer](http://localhost:3001/trajectory-viewer)**

* **Chat with Llama**: Type *"Move to Press Cell A"* or *"Navigate to High Voltage Cabinet"* into the chat box.
* **Interactive Grid**: Click anywhere on the 2D map or 3D isometric view.
* **Observe Safety Interception**: See the red path cut through the hazard circle, while the green path deflects around it, driving the physical robot in your MuJoCo 3D window!

---

## 📂 Repository Structure

```text
NitroGuard_3D_Ubuntu_Bundle/
├── mujoco-sim/                   # Python MuJoCo 3D Physics Integration
│   ├── models/
│   │   └── amr_factory.xml       # MJCF XML world (AMR robot + obstacles)
│   ├── sim_bridge.py             # FastAPI physics server (main-thread viewer)
│   ├── robot_controller.py       # Actuator force mapper (fx, fy)
│   └── state_reader.py           # MuJoCo telemetry reader (camelCase JSON)
│
├── my-mcp-server/                # NitroStack MCP Server & Next.js Widgets
│   ├── src/
│   │   ├── modules/robotics/     # Modular TS Services
│   │   │   ├── trajectory-planner.service.ts
│   │   │   ├── safety-filter.service.ts
│   │   │   ├── execution-adapter.service.ts
│   │   │   ├── robotics.tools.ts
│   │   │   └── robotics.resources.ts
│   │   ├── guards/               # ApiKeyGuard security token validator
│   │   └── widgets/              # Next.js Operations Console App
│   │       └── app/trajectory-viewer/page.tsx
│
└── README.md
```

---

## 🛡️ License
Distributed under the MIT License. Built for the NitroStack Hackathon.
