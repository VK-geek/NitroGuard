# 🤖 NitroGuard: AI Execution Gateway for Physical Systems
> **Complete Architecture, System Context & Transfer Specification**  
> *Built on NitroStack (`@nitrostack/core`, `@nitrostack/widgets`)*

---

## 📌 Executive Summary

**NitroGuard** is an enterprise-grade Model Context Protocol (MCP) server that acts as a **deterministic safety gate and execution engine for physical AI systems** (Factory AMRs, Autonomous Guided Vehicles, Robotic Arms, Drones, and Digital Twins).

### The Problem It Solves
When generative AI models (LLMs) control physical hardware, they generate movement coordinates based on probabilistic token prediction. When context drifts or spatial reasoning fails, the LLM produces **hallucinated collision vectors** — commanding a robot directly into a machine hazard zone.

### The Solution: Upstream Intent Interception
Traditional robotics safety systems (e.g. ISO 10218, TS 15066) act reactively at the hardware/sensor level (cutting power or freezing). **NitroGuard sits upstream at the software layer**, intercepting the LLM's requested trajectory *before* dispatching motor commands, mathematically deflecting unsafe vectors using **Control Barrier Functions (CBF)**, and visualizing the correction live inside an interactive NitroStack Widget.

---

## 🏗️ High-Level System Architecture

```text
                                  USER
                                   │
                                   ▼
                    "Move robot to Press A safely"
                                   │
                                  LLM
                                   │
        ┌──────────────────────────┴──────────────────────────┐
        │  1. Inspects Knowledge Layer (MCP Resources)        │
        │     - sim://factory-layout                          │
        │     - sim://robot-state                             │
        │     - sim://hazard-map                              │
        │     - sim://safety-policy                           │
        │     - sim://mission-log                             │
        └──────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
        ┌─────────────────────────────────────────────────────┐
        │  2. Dispatches Tool Call                           │
        │     execute_safe_motion(targetX: 5.2, targetY: 5.5)│
        │     [@UseGuards(ApiKeyGuard) + @RateLimit]          │
        └──────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      NitroGuard Internal Pipeline                      │
 │                                                                        │
 │  PlannerService    ──► ValidationService ──► SafetyService (CBF Math)  │
 │  (Straight line)       (Hazard Check)       (Barrier Vector Deflect)   │
 │                                                      │                 │
 │  LoggerService    ◄── ExecutionService  ◄────────────┘                 │
 │  (Updates log)        (Moves Sim State)                                │
 └─────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   ▼
        ┌─────────────────────────────────────────────────────┐
        │  3. Real-Time Telemetry Event                       │
        │     ctx.emit('safety.violation.detected', payload)  │
        └──────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
        ┌─────────────────────────────────────────────────────┐
        │  4. NitroGuard Operations Console (@Widget)         │
        │     - 🔴 Dashed Red Line: LLM Nominal Vector        │
        │     - 🟢 Solid Green Line: NitroGuard Safe Vector   │
        │     - ⚠️ Badge: "CBF VECTOR CORRECTED"               │
        └─────────────────────────────────────────────────────┘
```

---

## 📦 MCP Surface Specification

### 1. MCP Resources (`sim://`)
Resources represent **structured knowledge**, allowing the LLM to inspect context *before* invoking tools:

| Resource URI | Description | MIME Type |
|---|---|---|
| `sim://factory-layout` | 15x15 industrial grid bounds and machine coordinates | `application/json` |
| `sim://robot-state` | Live position, battery (84%), velocity, and AUTO mode | `application/json` |
| `sim://hazard-map` | Active danger zones (Industrial Press, High Voltage Cabinet) | `application/json` |
| `sim://safety-policy` | Clearance margin (0.5m), emergency stop policy | `application/json` |
| `sim://mission-log` | Historical decision log (enables autonomous learning) | `application/json` |

### 2. MCP Tools
Public tools exposed to AI agents via NitroStack `@Tool`:

| Tool Name | Purpose | Decorators |
|---|---|---|
| `get_robot_state` | Read-only live telemetry poll | `@Tool` |
| `execute_safe_motion` | Core execution pipeline (Planner → Validator → CBF → Execute → Log) | `@Tool`, `@UseGuards(ApiKeyGuard)`, `@RateLimit`, `@Widget('trajectory-viewer')` |
| `emergency_stop` | Instant safety abort / state lock | `@Tool`, `@UseGuards(ApiKeyGuard)` |

### 3. Interactive UI Widget (`@Widget('trajectory-viewer')`)
Maps to `src/widgets/app/trajectory-viewer/page.tsx` powered by `@nitrostack/widgets` `useWidgetSDK()`.
- **Top Bar:** Status badge (`⚠️ CBF VECTOR CORRECTED` vs `✅ NOMINAL VECTOR SAFE`).
- **SVG Viewport:** 15x15 grid rendering active hazard circles, robot position, 🔴 LLM nominal vector, and 🟢 NitroGuard safe vector.
- **Decision Telemetry:** Risk level (HIGH/MED/NONE), deflection distance ($m$), and active hazard label.
- **Interactive Controls:** Drag/click simulation targets live.

---

## 🧮 Mathematical Engine: Control Barrier Functions (CBF)

For a circular 2D hazard zone $p_{\text{obs}} = (x_{\text{obs}}, y_{\text{obs}})$ with radius $r$ and safety buffer $m$:

$$\text{Safety Barrier Function: } h(p) = \|p - p_{\text{obs}}\|^2 - (r + m)^2 \ge 0$$

If nominal LLM target $p_{\text{nom}}$ violates $h(p_{\text{nom}}) < 0$:
$$\hat{u} = \frac{p_{\text{nom}} - p_{\text{obs}}}{\|p_{\text{nom}} - p_{\text{obs}}\|}$$
$$p_{\text{safe}} = p_{\text{obs}} + \hat{u} \cdot (r + m)$$

*Result:* $p_{\text{safe}}$ is mathematically guaranteed to sit at the closest safe tangent boundary outside the hazard zone.

---

## 💻 Project Directory Layout

```text
my-mcp-server/
├── HANDOFF_2D_WINDOWS.md          # 2D Setup Guide for Windows
├── HANDOFF_3D_UBUNTU_MUJOCO.md    # 3D Setup Guide for Ubuntu/MuJoCo
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts                   # Bootstrap entry point
    ├── app.module.ts              # Root module registering RoboticsModule
    ├── modules/
    │   └── robotics/
    │       ├── safety.service.ts  # Pure TS CBF Safety Engine
    │       ├── robotics.tools.ts  # execute_safe_motion & emergency_stop
    │       ├── robotics.resources.ts # 5 sim:// resources with @Cache
    │       ├── robotics.prompts.ts# Guided workflows
    │       └── robotics.module.ts # Module declaration
    └── widgets/
        └── app/
            └── trajectory-viewer/ # NitroGuard Operations Console
                └── page.tsx
```

---

## ⚡ Quick Start & Deployment Guide

### Windows 2D Setup
1. Unzip `NitroGuard_2D_Windows_Bundle.zip`
2. Run `npm install -g @nitrostack/cli`
3. Run `nitrostack-cli install`
4. Start dev server: `npm run dev`
5. Open **NitroStudio** (`nitrostack.ai/studio`), connect to `my-mcp-server`, and test in Ops Canvas!

### Ubuntu Linux 3D MuJoCo Extension
1. Unzip `NitroGuard_3D_Ubuntu_Bundle.zip`
2. Install Python deps: `pip install mujoco qpsolvers osqp numpy fastapi uvicorn`
3. Start 3D MuJoCo Bridge: `python3 sim_3d_bridge.py`
4. Run NitroStack Server: `npm run dev`

---

## 🎤 30-Second Hackathon Pitch

> *"Generative AI models are great at planning, but terrible at physics. When an LLM commands a robot arm or warehouse AMR into a high-voltage cabinet, standard safety systems only react after a physical collision is imminent.  
> We built **NitroGuard** — an AI Execution Gateway using NitroStack. It exposes factory context as MCP Resources, enforces security via `@UseGuards`, and intercepts LLM movement vectors using Control Barrier Functions before dispatch. We visualize the AI's requested path in red and NitroGuard's safe path in green, live inside a Next.js `@Widget`."*
