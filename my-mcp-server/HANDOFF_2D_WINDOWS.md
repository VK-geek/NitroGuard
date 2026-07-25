# 🚀 NitroGuard 2D Windows Handoff & Setup Guide

Welcome to the **NitroGuard** MCP Server project! This package contains the complete, enterprise-grade Model Context Protocol (MCP) server built using **NitroStack**, designed to act as an **AI Execution Gateway for Physical Systems** (2D Factory AMR / Mobile Robot Safety Interceptor).

---

## 📁 Repository & File Structure

```text
my-mcp-server/
├── src/
│   ├── index.ts                      # Server bootstrap entry point
│   ├── app.module.ts                 # Root module registering RoboticsModule
│   ├── modules/
│   │   ├── robotics/                 # Core NitroGuard Robotics Module
│   │   │   ├── safety.service.ts     # Deterministic 2D CBF Safety Filter
│   │   │   ├── robotics.tools.ts     # MCP Tools (execute_safe_motion, etc.)
│   │   │   ├── robotics.resources.ts # MCP Resources (sim://factory-layout, sim://robot-state, etc.)
│   │   │   ├── robotics.prompts.ts   # Guided workflows
│   │   │   └── robotics.module.ts    # Module configuration
│   │   └── calculator/               # Sample reference module
│   └── widgets/                      # Next.js UI Widget SDK Component
│       └── app/
│           ├── trajectory-viewer/    # NitroGuard Operations Console Widget
│           └── calculator-result/
├── package.json
└── tsconfig.json
```

---

## ⚡ Quick Start Instructions

### 1. Prerequisites
- **Node.js**: `20.18.1` (or Node 18+)
- **npm**: `9.0+`
- **NitroStack CLI**:
  ```bash
  npm install -g @nitrostack/cli
  ```

### 2. Install Dependencies
Run from the root `my-mcp-server` directory:
```bash
# Installs root dependencies AND src/widgets dependencies automatically
nitrostack-cli install
```
*(Or manually: `npm install` in root, then `cd src/widgets && npm install`)*

### 3. Run Development Server
```bash
npm run dev
```
- MCP Transport Server starts at `http://localhost:3000` (or STDIO mode for Claude Desktop)
- Next.js Widget Server starts at `http://localhost:3001`

### 4. Connect to NitroStudio
1. Download & open **NitroStudio** (`nitrostack.ai/studio`).
2. Connect NitroStudio to `C:\path\to\my-mcp-server`.
3. Open the **Ops Canvas** and test the `execute_safe_movement` tool!

---

## 🧪 Demo Test Prompts for Claude / NitroStudio

Paste these exact prompts to demonstrate the system live to judges:

1. **Test 1 (Safe Vector - No Deflection):**
   > *"Move the robot to coordinates (2.0, 2.0)."*
   - **Expected:** `wasCorrected: false`. Nominal vector == Safe vector.

2. **Test 2 (Unsafe Vector - Major Deflection):**
   > *"Move the robot directly to coordinates (5.2, 5.5)."*
   - **Expected:** `wasCorrected: true`. Trajectory deflected from Industrial Press `(5,5)` to safe boundary `(6.77, 7.17)`. Badge displays `⚠️ CBF VECTOR CORRECTED`.

3. **Test 3 (Resource Inspection):**
   > *"Inspect the hazard zones using sim://hazard-map and sim://factory-layout, then request a safe position."*

---

## 🎯 Key Architectural Talking Points for Judges

1. **"AI Execution Gateway"**: NitroGuard sits between non-deterministic LLMs and physical controllers. The LLM plans intent; NitroGuard enforces physical safety rules.
2. **NitroStack Primitives Used**:
   - `@Tool` with Zod validation (`execute_safe_movement`)
   - `@Resource` with `@Cache({ ttl: 60 })` (`sim://obstacle-map`)
   - `@Widget` (`trajectory-viewer` / NitroGuard Operations Console)
   - `@UseGuards(ApiKeyGuard)` for authorization
3. **Control Barrier Function (CBF)**: Enforces $h(x) \ge 0$ mathematically. If the LLM hallucinates a target inside a machine hazard zone, the vector is projected along the normal to the minimum safe boundary.
