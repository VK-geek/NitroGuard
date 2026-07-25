# NitroStack Framework: Complete Master Context & Architecture Reference
*A portable, end-to-end technical guide covering NitroStack architecture, core primitives, widget development, CLI tools, NitroStudio workflows, hackathon guidelines, and sponsor-track victory strategy.*

---

## Table of Contents
1. [Overview & Core Architecture](#1-overview--core-architecture)
2. [Environment Setup & CLI Reference](#2-environment-setup--cli-reference)
3. [Framework Primitives & Decorator API](#3-framework-primitives--decorator-api)
4. [UI Widgets & `@nitrostack/widgets` SDK](#4-ui-widgets---nitrostackwidgets-sdk)
5. [NitroStudio Desktop IDE & NitroCloud](#5-nitrostudio-desktop-ide--nitrocloud)
6. [Troubleshooting & Common Fixes](#6-troubleshooting--common-fixes)
7. [Hackathon Best Practices (Do's & Don'ts)](#7-hackathon-best-practices-dos--donts)
8. [Sponsor Track Strategy & Problem Selection Blueprint](#8-sponsor-track-strategy--problem-selection-blueprint)

---

## 1. Overview & Core Architecture

NitroStack is an enterprise-grade TypeScript framework for building Model Context Protocol (MCP) servers. Inspired by NestJS, it provides a decorator-driven, modular architecture with built-in dependency injection, Zod schema validation, and Next.js visual widget integration.

### Core Architectural Layers
```
┌──────────────────────────────────────────────────────────────────────────┐
│                         NitroStack Core Server                           │
├───────────────────────────────┬──────────────────────────────────────────┤
│ Decorator Engine              │ Reflect-Metadata Reflection Pipeline     │
│ Dependency Injection Container│ Singleton / Scoped / Transient Providers │
│ Execution Pipeline            │ RateLimit ➔ Cache ➔ Guard ➔ Validate     │
│ Dual Transport Layer          │ STDIO (Local Dev) & HTTP SSE (Cloud/Prod)│
└───────────────┬───────────────┴────────────────────┬─────────────────────┘
                │                                    │
                ▼                                    ▼
┌──────────────────────────────┐    ┌──────────────────────────────────────┐
│  NitroStudio Desktop IDE     │    │  Next.js UI Widgets                  │
│  • App Canvas Inspection     │    │  • @nitrostack/widgets SDK           │
│  • Telemetry Logs & Traffic  │    │  • Theme-aware (Light/Dark)          │
│  • AI Chat & Vibe Coding     │    │  • Dual Platform (OpenAI & MCP Apps) │
└──────────────────────────────┘    └──────────────────────────────────────┘
```

---

## 2. Environment Setup & CLI Reference

### Environment Prerequisites
* **Node.js**: `v20.x` recommended (`v18+` minimum).
* **Package Managers**: `npm` or `pnpm`.
* **Global CLI Installation**:
  ```bash
  npm install -g @nitrostack/cli
  ```
  *(Or execute directly using `npx @nitrostack/cli@latest`)*

### Quick Start Commands
```bash
# Initialize a new project with a template
nitrostack-cli init my-mcp-server --template typescript-starter

# Move into project directory
cd my-mcp-server

# Run local development server (MCP Server + Widget Dev Server on port 3001)
npm run dev

# Production Build (Outputs static widgets to src/widgets/out and TS to dist/)
npm run build

# Start Production Server
npm run start
```

### Official Templates
1. `typescript-starter`: Starter calculator module with 1 tool, 1 resource, 1 prompt, and 2 widgets.
2. `typescript-pizzaz`: Pizza shop finder featuring Mapbox maps, state persistence, layout modes, and filtering.
3. `typescript-oauth`: Full OAuth 2.1 authentication integration with Auth0 and flight booking system.

---

## 3. Framework Primitives & Decorator API

NitroStack unifies backend endpoints, security, caching, rate limiting, and UI rendering into method-level decorator stacks.

### 1. Root Application & Modules
```typescript
// src/app.module.ts
import { McpApp, Module, ConfigModule } from '@nitrostack/core';
import { CalculatorModule } from './modules/calculator/calculator.module.js';

@McpApp({
  module: AppModule,
  server: { name: 'calculator-server', version: '1.0.0' },
  logging: { level: 'info' }
})
@Module({
  name: 'app',
  imports: [ConfigModule.forRoot(), CalculatorModule]
})
export class AppModule {}
```

### 2. Tools (`@Tool`)
Tools define executable actions for AI models, parsed and validated with Zod schemas.

```typescript
import { Tool, Widget, UseGuards, Cache, RateLimit, ExecutionContext, z } from '@nitrostack/core';

export class CalculatorTools {
  @Tool({
    name: 'calculate',
    description: 'Perform basic arithmetic calculations',
    inputSchema: z.object({
      operation: z.enum(['add', 'subtract', 'multiply', 'divide']),
      a: z.number(),
      b: z.number()
    }),
    invocation: {
      invoking: 'Computing result...',
      invoked: 'Calculation completed'
    },
    examples: {
      request: { operation: 'add', a: 5, b: 3 },
      response: { operation: 'add', a: 5, b: 3, result: 8, expression: '5 + 3 = 8' }
    }
  })
  @Cache({ ttl: 300, key: (input) => `calc:${input.operation}:${input.a}:${input.b}` })
  @Widget('calculator-result')
  async calculate(input: any, ctx: ExecutionContext) {
    ctx.logger.info('Executing calculation', { input });
    const result = input.a + input.b; // Logic here
    return { ...input, result, expression: `${input.a} + ${input.b} = ${result}` };
  }
}
```

### 3. Resources (`@Resource`)
Resources expose static or dynamic ground-truth data URIs.

```typescript
import { Resource, ExecutionContext } from '@nitrostack/core';

export class CalculatorResources {
  @Resource({
    uri: 'calculator://operations',
    name: 'Calculator Operations',
    description: 'Lists all available operations supported by the server',
    mimeType: 'application/json'
  })
  @Widget('calculator-operations')
  async getOperations(uri: string, ctx: ExecutionContext) {
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(['add', 'subtract', 'multiply', 'divide'])
      }]
    };
  }
}
```

### 4. Prompts (`@Prompt`)
Prompts provide reusable conversation templates and agentic workflows.

```typescript
import { Prompt, ExecutionContext } from '@nitrostack/core';

export class CalculatorPrompts {
  @Prompt({
    name: 'calculator_help',
    description: 'Provides guidance on using the calculator tools and resources',
    arguments: [{ name: 'topic', description: 'Specific area to get help on', required: false }]
  })
  async getHelp(args: { topic?: string }, ctx: ExecutionContext) {
    return {
      messages: [{
        role: 'user',
        content: `Explain how to use the calculator for topic: ${args.topic || 'general'}`
      }]
    };
  }
}
```

### 5. Guards (`@UseGuards`) & Services (`@Injectable`)
```typescript
@Injectable()
export class AuthService {
  validateToken(token: string): boolean { return token === 'valid-secret'; }
}

@Tool({ name: 'admin_action' })
@UseGuards(AdminGuard)
async adminAction(input: any) { /* Restricted Logic */ }
```

---

## 4. UI Widgets & `@nitrostack/widgets` SDK

Widgets are Next.js components (`src/widgets/app/<widget-name>/page.tsx`) rendered inside client applications.

### Key Widget Hooks
```tsx
'use client';

import { 
  useWidgetSDK, 
  useTheme, 
  useWidgetState, 
  useDisplayMode, 
  useMaxHeight 
} from '@nitrostack/widgets';

export default function MyWidget() {
  const { isReady, getToolOutput, callTool, openExternal } = useWidgetSDK();
  const theme = useTheme(); // 'light' | 'dark'
  const displayMode = useDisplayMode(); // 'inline' | 'pip' | 'fullscreen'
  const maxHeight = useMaxHeight();
  
  // Persistent state across widget reloads
  const [state, setState] = useWidgetState<{ activeTab: string }>(() => ({
    activeTab: 'summary'
  }));

  // Retrieve output returned by the tool
  let data = getToolOutput<any>();

  // Browser Preview Fallback Pattern
  if (!data) {
    data = { expression: '5 + 3 = 8', result: 8 }; // Mock fallback for direct browser viewing
  }

  if (!isReady) return <div>Loading Widget...</div>;

  return (
    <div style={{
      background: theme === 'dark' ? '#1e293b' : '#ffffff',
      color: theme === 'dark' ? '#f8fafc' : '#0f172a',
      padding: '20px',
      borderRadius: '12px',
      maxHeight
    }}>
      <h3>Result: {data.result}</h3>
      <button onClick={() => setState({ activeTab: 'details' })}>
        View Mode: {state?.activeTab}
      </button>
    </div>
  );
}
```

### Platform Compatibility
The Widget SDK automatically bridges both window contexts:
* **OpenAI Apps SDK**: `window.openai` / `openai:ready`
* **MCP Apps Spec**: `window.__MCP_APP_CONTEXT__` / `mcp:ready`

---

## 5. NitroStudio Desktop IDE & NitroCloud

NitroStudio is the official IDE for building, inspecting, testing, and debugging MCP servers.

### Connecting a Project in NitroStudio
1. Open NitroStudio.
2. Click **Add Server** $\rightarrow$ select **Nitro Project**.
3. Select your project folder on disk.
4. Choose **Studio App Canvas** (for inspection/testing) or **Vibe Code (Compose)**.
5. Studio spawns the local process via `npx tsx src/index.ts` automatically over **STDIO**.

### Studio Navigation & Features
* **App Canvas (`/`)**: Visual topology diagram connecting Prompts, Resources, Tools, and Widgets.
* **Tools (`/tools`)**: Auto-generated UI form based on Zod input schema, Execute button, and live Mobile/Tablet/Desktop **Widget Preview**.
* **Prompts (`/prompts`)**: Execute conversation templates and inspect role-labeled messages.
* **Resources (`/resources`)**: Inspect URI schemas and syntax-highlighted data payloads.
* **AI Chat (`/chat`)**: Chat directly with AI models that trigger your tools with **Allow/Deny** approval modals.
* **Logs (`/logs`)**: Real-time traffic inspector showing request/response JSON payloads.
* **Compose / Vibe Coding**: AI coding agent workspace with live file edit streaming, Diff Queue (`Keep`/`Revert`), and Checkpoints.

### Deployment & ChatGPT Integration
1. **NitroCloud**: Create app at `nitrocloud.ai` and click **Deploy** from Studio or link a GitHub repo for auto-deploy on push.
2. **ChatGPT Integration**:
   * Enable **Developer Mode** in ChatGPT (*Settings → Plugins/Apps*).
   * Click **+** (New Plugin) and paste your server's SSE URL: `{serviceUrl}/sse`.

---

## 6. Troubleshooting & Common Fixes

### 1. `ReferenceError: require is not defined in ES module scope` in Next.js Widgets
* **Cause**: Next.js compiles internal server bundles (like `_document.js`) as CommonJS. Having `"type": "module"` in `src/widgets/package.json` forces Node to treat `.js` files as ES Modules.
* **Fix**:
  1. Remove `"type": "module"` from `src/widgets/package.json`.
  2. In `src/widgets/next.config.js`, change `export default nextConfig;` to `module.exports = nextConfig;`.

### 2. Widget Server 404 Error on `http://localhost:3001/`
* **Cause**: Next.js App Router has widget routes like `/calculator-result` but lacks a root `/` page.
* **Fix**: Create a `src/widgets/app/page.tsx` landing page listing registered widgets and linking to them.

### 3. Widget Stuck on "Loading..." when Opened Directly in Browser
* **Cause**: `getToolOutput()` returns `undefined` outside an active MCP client session.
* **Fix**: Provide fallback mock data inside the widget page component when `!data`.

### 4. `npm run dev` Exits with `Shutting down...` in Standard Terminal
* **Cause**: STDIO transport requires an open, interactive stdin connection.
* **Fix**: Open and connect the project inside **NitroStudio Desktop App**, which maintains the active STDIO session automatically.

---

## 7. Hackathon Best Practices (Do's & Don'ts)

### ✅ DO's
* **Framework Usage**: Build strictly using the official NitroStack TypeScript SDK (`@nitrostack/core`, `@nitrostack/widgets`).
* **Repository hygiene**: Commit regularly, provide a detailed `README.md`, and maintain a clean `.gitignore`.
* **Testing**: Test tools, prompts, resources, and widgets continuously in **NitroStudio**.
* **Deployment**: Deploy early to **NitroCloud** to ensure your project works end-to-end before final submission.

### ❌ DON'Ts
* **Never Commit Secrets**: Do not push API keys, `.env` files, or `node_modules` to GitHub.
* **Avoid Un-typed Tools**: Do not leave Zod input schemas empty or loosely typed (`z.any()`).
* **Don't Ignore MCP Surface**: Do not build *only* bare tools—leverage `@Resource` and `@Prompt` primitives.
* **Don't Wait Until the End**: Deploy to cloud early; do not defer testing until the final submission hour.

---

## 8. Sponsor Track Strategy & Problem Selection Blueprint

To win the **NitroStack Sponsor Track**, your project must highlight NitroStack's core differentiators: **Decorator Stacking**, **Full MCP Surface**, **Rich Interactive Widgets**, and **NitroStudio Live Demonstration**.

### The 6-Stage Problem Selection Filter Stack
1. **Target Friction User**: Name the exact professional feeling weekly pain (e.g. On-Call SRE, Warehouse Logistics Dispatcher).
2. **Plain LLM Failure Point**: The problem *must* require live telemetry, hardware/database write actions, or deterministic algorithms an LLM would hallucinate.
3. **Safety & Guards Contrast**: Public read resources (`@Resource`) vs. protected write tools (`@UseGuards`).
4. **Timebox Feasibility**: Use controllable local mock data/drivers; avoid flaky external third-party APIs.
5. **The Visual "One Moment"**: Design a 10-second interactive widget moment (e.g., live re-routing map with 1-click override).
6. **Sponsor Differentiator**: Use `@Tool` + `@UseGuards` + `@Cache` + `@RateLimit` + `@Widget` together on a single method.

### Complete Code Blueprint Pattern

```typescript
// src/modules/fleet/fleet.tools.ts
import { Tool, Widget, UseGuards, Cache, RateLimit, ExecutionContext, z } from '@nitrostack/core';
import { SafetyOverrideGuard } from '../../guards/safety-override.guard.js';

export class FleetTools {
  constructor(private readonly pathfindingService: PathfindingService) {}

  // 1. Cached & Unrestricted Path Computation
  @Tool({
    name: 'plan_path',
    description: 'Computes optimal route avoiding obstacles',
    inputSchema: z.object({
      startZone: z.string(),
      targetZone: z.string(),
      robotId: z.string()
    }),
    examples: {
      request: { startZone: 'A1', targetZone: 'B4', robotId: 'bot-01' },
      response: { distanceMeters: 42, pathNodes: ['A1', 'A2', 'B2', 'B4'], status: 'OPTIMAL' }
    }
  })
  @Cache({ ttl: 300, key: (input) => `path:${input.startZone}:${input.targetZone}` })
  @Widget('fleet-map')
  async planPath(input: any, ctx: ExecutionContext) {
    ctx.logger.info('Calculating deterministic path', { robotId: input.robotId });
    return await this.pathfindingService.calculate(input.startZone, input.targetZone);
  }

  // 2. Guarded Write Action
  @Tool({
    name: 'dispatch_robot',
    description: 'Dispatches autonomous robot on specified route. Requires supervisor authorization.',
    inputSchema: z.object({
      robotId: z.string(),
      routeId: z.string(),
      priority: z.enum(['LOW', 'MEDIUM', 'CRITICAL'])
    })
  })
  @UseGuards(SafetyOverrideGuard)
  @RateLimit({ requests: 5, window: '1m' })
  @Widget('fleet-map')
  async dispatchRobot(input: any, ctx: ExecutionContext) {
    ctx.logger.warn('Dispatching hardware payload', { robotId: input.robotId });
    return { status: 'DISPATCHED', timestamp: new Date().toISOString(), robotId: input.robotId };
  }
}
```

```typescript
// src/modules/fleet/fleet.resources.ts
import { Resource, ExecutionContext } from '@nitrostack/core';

export class FleetResources {
  @Resource({
    uri: 'warehouse://map-layout',
    name: 'Warehouse Floor Grid Layout',
    description: 'Ground-truth grid matrix of warehouse zones and hazard boundaries',
    mimeType: 'application/json'
  })
  async getWarehouseLayout(uri: string, ctx: ExecutionContext) {
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify({
          gridDimensions: { width: 100, height: 100 },
          activeZones: ['A1', 'A2', 'B1', 'B2', 'B3', 'B4'],
          restrictedZones: ['C1', 'C2']
        })
      }]
    };
  }
}
```

```typescript
// src/modules/fleet/fleet.prompts.ts
import { Prompt, ExecutionContext } from '@nitrostack/core';

export class FleetPrompts {
  @Prompt({
    name: 'replan_fleet_hazard',
    description: 'Agentic workflow to inspect telemetry, replan paths around obstacles, and present dispatch widgets',
    arguments: [{ name: 'hazardZone', description: 'Zone where obstruction occurred', required: true }]
  })
  async replanFleet(args: { hazardZone: string }, ctx: ExecutionContext) {
    return {
      messages: [{
        role: 'user',
        content: `Hazard reported in zone ${args.hazardZone}. 
1. Fetch live map layout from warehouse://map-layout.
2. Replan path for active bots using plan_path.
3. Present the interactive fleet-map widget with updated routes.`
      }]
    };
  }
}
```

### Winning Demo Script Walkthrough
1. **Launch NitroStudio**: Open your project inside NitroStudio Desktop App.
2. **Show App Canvas**: Highlight the complete topology (Prompts $\rightarrow$ Resources $\rightarrow$ Tools $\rightarrow$ Widgets).
3. **Show Code Decorator Stack**: Point to `@Tool + @UseGuards + @Cache + @RateLimit + @Widget` in one method signature ("One stack does everything").
4. **Trigger `@Prompt` Workflow**: Run your agentic prompt in NitroStudio AI Chat. Show it reading `@Resource` ground-truth data and calling `@Tool`.
5. **Demonstrate Interactive Widget**: Interact with the React widget live inside NitroStudio. Click interactive action buttons using `useWidgetState()`.
6. **Show Live Telemetry Logs**: Open NitroStudio's `/logs` panel to demonstrate structured logging and real-time MCP traffic.
