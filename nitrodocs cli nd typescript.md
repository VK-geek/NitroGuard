/
intro
Introduction to NitroStack
Welcome to NitroStack. This guide details the architecture and capabilities of the framework designed for building production-grade Model Context Protocol (MCP) servers.

Overview
NitroStack is a high-performance TypeScript framework engineered for scalability and maintainability. It provides a robust architecture for developing MCP servers, offering advanced features such as dependency injection, modular organization, and type-safe tooling out of the box.

Designed for enterprise applications, NitroStack enforces architectural best practices, ensuring your codebase remains clean, testable, and adaptable as it scales from a single tool to a complex distributed system.

Core Architecture
Decorator-Based Design
NitroStack utilizes a descriptive, decorator-based architecture. This approach reduces boilerplate and improves readability by keeping configuration close to the implementation.

Key Advantages

Declarative Syntax: Define behavior and configuration using clear, semantic decorators.
Type, Schema & Validation: Native TypeScript integration with Zod schemas ensures end-to-end type safety and runtime validation.
Composability: Apply multiple behaviors—such as authentication, caching, and rate limiting—via composable decorators.
Developer Experience: leveraging TypeScript's metadata reflection for robust IntelliSense and refactoring support.
Example Implementation

Typescript

@Tool({
  name: 'search_products',
  description: 'Search product catalog with advanced filtering specification',
  inputSchema: z.object({
    query: z.string(),
    category: z.string().optional(),
    filters: z.object({
      minPrice: z.number().optional(),
      maxPrice: z.number().optional(),
    }).optional(),
    pagination: z.object({
      page: z.number().default(1),
      limit: z.number().default(20)
    }).default({})
  })
})
@UseGuards(JwtAuthGuard)
@UseMiddleware(AuditLoggingMiddleware)
@Cache({ ttl: 600, key: (input) => `search:${input.query}` })
@RateLimit({ requests: 100, window: '1h' })
@Widget('product-grid-view')
async searchProducts(input: any, ctx: ExecutionContext) {
  ctx.logger.info('Executing product search', { query: input.query });
  return await this.productService.executeSearch(input);
}
This single declaration encapsulates API definition, validation, security, observability, performance optimization, and UI presentation layer association.

Modular Organization
NitroStack enforces a modular architecture to promote separation of concerns and maintainability. Applications are comprised of self-contained modules that encapsulate related capabilities, providers, and context.

Module Definition

Typescript

@Module({
  name: "commerce-engine",
  description: "Core commerce and product management domain",
  controllers: [ProductTools, InventoryResources, PricingPrompts],
  providers: [ProductService, InventoryService, PricingEngine],
  imports: [DatabaseModule, AuthenticationModule],
  exports: [ProductService]
})
export class CommerceModule {}
Architectural Benefits

Encapsulation: Strict boundaries between domains (e.g., User Management, Payment Processing).
Reusability: Modules can be exported and shared across different services.
Dependency Management: Explicit definition of module dependencies and public interfaces.
Testability: Modules can be isolated for unit and integration testing.
Dependency Injection (DI)
At the core of NitroStack is a sophisticated Dependency Injection container. This system manages the lifecycle of application components, resolving dependencies automatically and promoting loose coupling.

DI Implementation

Typescript

@Injectable()
export class OrderService {
  constructor(
    private readonly repository: OrderRepository,
    private readonly paymentGateway: PaymentGateway,
    private readonly notificationService: NotificationService
  ) {}

  async processOrder(order: OrderDto): Promise<OrderResult> {
    const transaction = await this.paymentGateway.authorize(order.payment);
    const result = await this.repository.save({ ...order, transactionId: transaction.id });
    await this.notificationService.notifyConfirmation(result);
    return result;
  }
}
The DI system supports:

Singleton, Transient, and Scoped lifecycles
Factory Providers for dynamic instantiation
Value Providers for configuration injection
Circular Dependency Resolution
Security & Guards
Security is implemented via a declarative Guard system. Guards intercept execution contexts to validate requests, manage authentication, and enforce authorization policies before business logic is invoked.

Typescript

@Tool({ name: 'admin_dashboard' })
@UseGuards(OAuth2Guard, RoleGuard.for(['admin', 'super-admin']))
async accessDashboard(input: any, ctx: ExecutionContext) {
  // Logic executes only if all guards pass
  return this.dashboardService.getMetrics();
}
Included security primitives:

Authentication: JWT, OAuth 2.1, API Key strategies.
Authorization: Role-based (RBAC) and Attribute-based (ABAC) access control.
Scope Management: Fine-grained permission scopes for secure tool execution.
Intelligent UI Widgets
NitroStack bridges the gap between backend logic and frontend presentation with its Widget system. Tools can define associated UI components using React and Next.js, which are rendered by compatible clients (such as NitroStack Studio).

Typescript

@Tool({ name: 'portfolio_analysis' })
@Widget('financial-dashboard') 
async analyzePortfolio(input: PortfolioInput) {
  return await this.financeService.analyze(input);
}
Widgets leverage standard web technologies (React, Tailwind CSS) to provide rich, interactive interfaces for AI model outputs, enhancing the user experience beyond simple text responses.

Ecosystem Features
NitroStack provides a comprehensive suite of enterprise-ready capabilities:

Middleware Pipeline: Intercept and transform requests and responses globally or per-route.
Interceptors: Advanced execution flow control and response mapping.
Pipes: Reusable input validation and transformation logic.
Exception Filters: Centralized error handling and standardized response formatting.
Observability: Integrated structured logging and event systems.
NitroStack Studio: A dedicated environment for developing, testing, and debugging MCP servers and widgets.
Why NitroStack?
For Enterprise Development
Standardization: Enforces consistent patterns across large teams.
Reliability: Built on proven architectural patterns for long-term maintainability.
Security: Security-first design with robust authentication and authorization mechanisms.
For AI Integration
Context Protocol Native: Built specifically for the Model Context Protocol specification.
Rich Interaction: Delivers structured data and interactive UI components to AI agents.
Scalable Context: Efficiently manages tools and resources for complex agentic workflows.
Next Steps

Installation - Setup your development environment.
Quick Start - Initialize your first NitroStack project.
CLI Introduction - Learn about the CLI tools.
Server Architecture - Deep dive into server concepts.
Next
📦 Installation
/
installation
Installation
Package Overview
NitroStack consists of three separate packages:

Package	Purpose	When to Install
@nitrostack/cli	CLI tools for project management	Install globally once
nitrostack	Core SDK for MCP servers	Included in projects
@nitrostack/widgets	Widget development SDK	Included in widget projects
Install CLI (Required)
Install the NitroStack CLI globally:

Bash

npm install -g @nitrostack/cli
Verify Installation
Bash

nitrostack-cli --version
Alternative: Use npx
You can also use npx without global installation:

Bash

npx @nitrostack/cli init my-project
Project Dependencies
When you create a new project, dependencies are automatically added:

Root Project (package.json)
JSON

{
  "dependencies": {
    "@nitrostack/core": "^1",
    "zod": "^3.22.4",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "@nitrostack/cli": "^1",
    "@types/node": "^22.10.0",
    "typescript": "^5.3.3"
  }
}
Widgets Project (src/widgets/package.json)
JSON

{
  "dependencies": {
    "@nitrostack/widgets": "^1",
    "next": "^14",
    "react": "^18",
    "react-dom": "^18"
  }
}
System Requirements
Node.js: 18.x or 20.x (LTS recommended)
npm: 8.x or newer
OS: Windows, macOS, or Linux
Install in Existing Projects
Installing Root Dependencies
Bash

# Install all dependencies in root and widgets
nitrostack-cli install
This runs npm install in both the root directory and src/widgets.

Manual Installation
Bash

# Root dependencies
npm install @nitrostack/core zod dotenv
npm install -D @nitrostack/cli @types/node typescript

# Widget dependencies (if using widgets)
cd src/widgets
npm install @nitrostack/widgets next react react-dom
Upgrading Packages
Upgrade NitroStack packages to the latest version:

Bash

nitrostack-cli upgrade
This updates nitrostack in both root and widgets directories.

See Upgrade Command for more options.

NitroStudio Setup
NitroStudio is now a standalone application:

Download NitroStudio from nitrostack.ai/studio
Start your project: npm run dev
Connect Studio to your project directory
Studio connects to your MCP server and widget server automatically.

Next Steps
Quick Start Guide
Init Command
Dev Command
Previous
👋 Introduction
Next
⚡ Quick Start
Quick Start Guide
This guide walks you through creating your first NitroStack MCP server. By the end, you will have a working server with tools, resources, and a visual widget.

Prerequisites
Node.js 20.18.1 (recommended) - Use NVM (Node Version Manager) to install and manage Node.js versions
npm 9 or higher
tsx - Install globally: npm i tsx -g
Step 1: Install NitroStudio (Optional)
NitroStudio is a desktop application for testing and debugging MCP servers. Download it from nitrostack.ai/studio.

While optional, NitroStudio significantly improves the development experience by providing:

Real-time tool testing
AI chat integration
Widget preview
Request/response inspection
Step 2: Create Your Project
Use the NitroStack CLI to scaffold a new project:

Bash

npx @nitrostack/cli init my-server
This creates a complete project structure with:

Sample tools, resources, and prompts
Widget components (Next.js)
TypeScript configuration
Development scripts
Navigate to your project directory:

Bash

cd my-server
Step 3: Open Project in NitroStudio
Open your project folder in NitroStudio to connect automatically. NitroStudio will start the development server and provide a visual interface for testing your MCP server.

If you prefer running the server manually, you can still use:

Bash

npm run dev
Project Structure
my-server/
├── src/
│   ├── index.ts              # Application entry point
│   ├── app.module.ts         # Root module configuration
│   └── modules/
│       └── calculator/       # Sample feature module
│           ├── calculator.module.ts
│           ├── calculator.tools.ts
│           ├── calculator.resources.ts
│           └── calculator.prompts.ts
├── src/widgets/              # Next.js widget components
│   └── app/
│       └── calculator-result/
│           └── page.tsx
├── package.json
├── tsconfig.json
└── .env
Understanding the Code
Entry Point
The entry point bootstraps the application:

Typescript

// src/index.ts
import 'dotenv/config';
import { McpApplicationFactory } from '@nitrostack/core';
import { AppModule } from './app.module.js';

async function bootstrap() {
  const server = await McpApplicationFactory.create(AppModule);
  await server.start();
}

bootstrap();
Root Module
The root module configures the application and imports feature modules:

Typescript

// src/app.module.ts
import { McpApp, Module, ConfigModule } from '@nitrostack/core';
import { CalculatorModule } from './modules/calculator/calculator.module.js';

@McpApp({
  module: AppModule,
  server: {
    name: 'calculator-server',
    version: '1.0.0'
  }
})
@Module({
  imports: [
    ConfigModule.forRoot(),
    CalculatorModule
  ]
})
export class AppModule {}
Tool Definition
Tools are functions that AI models can invoke:

Typescript

// src/modules/calculator/calculator.tools.ts
import { ToolDecorator as Tool, Widget, z, ExecutionContext } from '@nitrostack/core';

export class CalculatorTools {
  @Tool({
    name: 'calculate',
    description: 'Perform arithmetic calculations on two numbers',
    inputSchema: z.object({
      operation: z.enum(['add', 'subtract', 'multiply', 'divide'])
        .describe('The arithmetic operation to perform'),
      a: z.number().describe('First operand'),
      b: z.number().describe('Second operand')
    })
  })
  @Widget('calculator-result')
  async calculate(
    input: { operation: string; a: number; b: number },
    ctx: ExecutionContext
  ) {
    const operations: Record<string, number> = {
      add: input.a + input.b,
      subtract: input.a - input.b,
      multiply: input.a * input.b,
      divide: input.a / input.b
    };

    const result = operations[input.operation];

    return {
      result,
      expression: `${input.a} ${input.operation} ${input.b} = ${result}`
    };
  }
}
Widget Component
Widgets provide visual representations of tool outputs:

TSX

// src/widgets/app/calculator-result/page.tsx
'use client';
import { useWidgetSDK } from '@nitrostack/widgets';

export default function CalculatorResult() {
  const { isReady, getToolOutput } = useWidgetSDK();

  if (!isReady) {
    return <div className="p-4">Loading...</div>;
  }

  const data = getToolOutput();

  return (
    <div className="p-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl text-white text-center">
      <h2 className="text-4xl font-bold">{data.result}</h2>
      <p className="text-lg opacity-90">{data.expression}</p>
    </div>
  );
}
Common Commands
Bash

# Development
npm run dev              # Start development server with hot reload

# Building
npm run build            # Build for production
npm start                # Run production server

# CLI Commands
nitrostack-cli dev       # Alternative: run dev server directly
nitrostack-cli build     # Build with CLI
nitrostack-cli generate types  # Generate TypeScript types for widgets
Adding Your First Tool
Create a new tool in an existing module or create a new module:

Typescript

// src/modules/calculator/calculator.tools.ts
@Tool({
  name: 'format_number',
  description: 'Format a number with specified decimal places and locale',
  inputSchema: z.object({
    value: z.number().describe('The number to format'),
    decimals: z.number().int().min(0).max(10).default(2)
      .describe('Number of decimal places'),
    locale: z.string().default('en-US')
      .describe('Locale for formatting')
  })
})
async formatNumber(
  input: { value: number; decimals: number; locale: string },
  ctx: ExecutionContext
) {
  const formatted = new Intl.NumberFormat(input.locale, {
    minimumFractionDigits: input.decimals,
    maximumFractionDigits: input.decimals
  }).format(input.value);

  return {
    original: input.value,
    formatted,
    locale: input.locale
  };
}
Troubleshooting
Port Already in Use
If the default port is in use, specify an alternative:

Bash

nitrostack-cli dev --port 3002
Widget Not Loading
Verify the widget server is running at http://localhost:3001
Ensure the widget route matches the @Widget('name') decorator
Check browser console for errors
TypeScript Compilation Errors
Bash

npm install
npm run build
Module Not Found
Ensure all imports use the .js extension for ESM compatibility:

Typescript

// Correct
import { UserService } from './user.service.js';

// Incorrect
import { UserService } from './user.service';
Next Steps
Server Concepts - Learn about modules, DI, and architecture
Tools Guide - Deep dive into tool creation
UI Widgets Guide - Build custom visual components
Authentication - Secure your server
Deployment - Prepare for production
Previous
📦 Installation
Next
🏗️ Server Concepts
Quick Start Guide
This guide walks you through creating your first NitroStack MCP server. By the end, you will have a working server with tools, resources, and a visual widget.

Prerequisites
Node.js 20.18.1 (recommended) - Use NVM (Node Version Manager) to install and manage Node.js versions
npm 9 or higher
tsx - Install globally: npm i tsx -g
Step 1: Install NitroStudio (Optional)
NitroStudio is a desktop application for testing and debugging MCP servers. Download it from nitrostack.ai/studio.

While optional, NitroStudio significantly improves the development experience by providing:

Real-time tool testing
AI chat integration
Widget preview
Request/response inspection
Step 2: Create Your Project
Use the NitroStack CLI to scaffold a new project:

Bash

npx @nitrostack/cli init my-server
This creates a complete project structure with:

Sample tools, resources, and prompts
Widget components (Next.js)
TypeScript configuration
Development scripts
Navigate to your project directory:

Bash

cd my-server
Step 3: Open Project in NitroStudio
Open your project folder in NitroStudio to connect automatically. NitroStudio will start the development server and provide a visual interface for testing your MCP server.

If you prefer running the server manually, you can still use:

Bash

npm run dev
Project Structure
my-server/
├── src/
│   ├── index.ts              # Application entry point
│   ├── app.module.ts         # Root module configuration
│   └── modules/
│       └── calculator/       # Sample feature module
│           ├── calculator.module.ts
│           ├── calculator.tools.ts
│           ├── calculator.resources.ts
│           └── calculator.prompts.ts
├── src/widgets/              # Next.js widget components
│   └── app/
│       └── calculator-result/
│           └── page.tsx
├── package.json
├── tsconfig.json
└── .env
Understanding the Code
Entry Point
The entry point bootstraps the application:

Typescript

// src/index.ts
import 'dotenv/config';
import { McpApplicationFactory } from '@nitrostack/core';
import { AppModule } from './app.module.js';

async function bootstrap() {
  const server = await McpApplicationFactory.create(AppModule);
  await server.start();
}

bootstrap();
Root Module
The root module configures the application and imports feature modules:

Typescript

// src/app.module.ts
import { McpApp, Module, ConfigModule } from '@nitrostack/core';
import { CalculatorModule } from './modules/calculator/calculator.module.js';

@McpApp({
  module: AppModule,
  server: {
    name: 'calculator-server',
    version: '1.0.0'
  }
})
@Module({
  imports: [
    ConfigModule.forRoot(),
    CalculatorModule
  ]
})
export class AppModule {}
Tool Definition
Tools are functions that AI models can invoke:

Typescript

// src/modules/calculator/calculator.tools.ts
import { ToolDecorator as Tool, Widget, z, ExecutionContext } from '@nitrostack/core';

export class CalculatorTools {
  @Tool({
    name: 'calculate',
    description: 'Perform arithmetic calculations on two numbers',
    inputSchema: z.object({
      operation: z.enum(['add', 'subtract', 'multiply', 'divide'])
        .describe('The arithmetic operation to perform'),
      a: z.number().describe('First operand'),
      b: z.number().describe('Second operand')
    })
  })
  @Widget('calculator-result')
  async calculate(
    input: { operation: string; a: number; b: number },
    ctx: ExecutionContext
  ) {
    const operations: Record<string, number> = {
      add: input.a + input.b,
      subtract: input.a - input.b,
      multiply: input.a * input.b,
      divide: input.a / input.b
    };

    const result = operations[input.operation];

    return {
      result,
      expression: `${input.a} ${input.operation} ${input.b} = ${result}`
    };
  }
}
Widget Component
Widgets provide visual representations of tool outputs:

TSX

// src/widgets/app/calculator-result/page.tsx
'use client';
import { useWidgetSDK } from '@nitrostack/widgets';

export default function CalculatorResult() {
  const { isReady, getToolOutput } = useWidgetSDK();

  if (!isReady) {
    return <div className="p-4">Loading...</div>;
  }

  const data = getToolOutput();

  return (
    <div className="p-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl text-white text-center">
      <h2 className="text-4xl font-bold">{data.result}</h2>
      <p className="text-lg opacity-90">{data.expression}</p>
    </div>
  );
}
Common Commands
Bash

# Development
npm run dev              # Start development server with hot reload

# Building
npm run build            # Build for production
npm start                # Run production server

# CLI Commands
nitrostack-cli dev       # Alternative: run dev server directly
nitrostack-cli build     # Build with CLI
nitrostack-cli generate types  # Generate TypeScript types for widgets
Adding Your First Tool
Create a new tool in an existing module or create a new module:

Typescript

// src/modules/calculator/calculator.tools.ts
@Tool({
  name: 'format_number',
  description: 'Format a number with specified decimal places and locale',
  inputSchema: z.object({
    value: z.number().describe('The number to format'),
    decimals: z.number().int().min(0).max(10).default(2)
      .describe('Number of decimal places'),
    locale: z.string().default('en-US')
      .describe('Locale for formatting')
  })
})
async formatNumber(
  input: { value: number; decimals: number; locale: string },
  ctx: ExecutionContext
) {
  const formatted = new Intl.NumberFormat(input.locale, {
    minimumFractionDigits: input.decimals,
    maximumFractionDigits: input.decimals
  }).format(input.value);

  return {
    original: input.value,
    formatted,
    locale: input.locale
  };
}
Troubleshooting
Port Already in Use
If the default port is in use, specify an alternative:

Bash

nitrostack-cli dev --port 3002
Widget Not Loading
Verify the widget server is running at http://localhost:3001
Ensure the widget route matches the @Widget('name') decorator
Check browser console for errors
TypeScript Compilation Errors
Bash

npm install
npm run build
Module Not Found
Ensure all imports use the .js extension for ESM compatibility:

Typescript

// Correct
import { UserService } from './user.service.js';

// Incorrect
import { UserService } from './user.service';
Next Steps
Server Concepts - Learn about modules, DI, and architecture
Tools Guide - Deep dive into tool creation
UI Widgets Guide - Build custom visual components
Authentication - Secure your server
Deployment - Prepare for production
Previous
📦 Installation
Next
🏗️ Server Concepts

installation
CLI Installation Guide
Overview
The NitroStack CLI (@nitrostack/cli) is a separate package that provides commands for creating, developing, and building MCP server projects.

Global Installation
Install the CLI globally for easy access:

Bash

npm install -g @nitrostack/cli
Verify Installation
Bash

nitrostack-cli --version
Expected output:

@nitrostack/cli/1.0.3
Alternative: Using npx
You can use npx without global installation:

Bash

# Create a new project
npx @nitrostack/cli init my-project

# Run commands in existing project
npx @nitrostack/cli dev
Requirements
Node.js: 18.x or 20.x (LTS recommended)
npm: 8.x or newer
OS: Windows, macOS, or Linux
Package Architecture
NitroStack uses a monorepo structure with separate packages:

Package	Purpose	Install Method
@nitrostack/cli	CLI tools	npm install -g
nitrostack	Core SDK	Auto-installed in projects
@nitrostack/widgets	Widget SDK	Auto-installed in widget projects
Available Commands
After installation, you have access to:

Command	Description
nitrostack-cli init	Create new project
nitrostack-cli dev	Start development mode
nitrostack-cli build	Build for production
nitrostack-cli start	Start production server
nitrostack-cli install	Install all dependencies
nitrostack-cli upgrade	Upgrade packages
nitrostack-cli generate	Generate code scaffolds
Quick Start
Bash

# 1. Install CLI
npm install -g @nitrostack/cli

# 2. Create project
nitrostack-cli init my-project

# 3. Enter project
cd my-project

# 4. Start development
npm run dev
Updating the CLI
To update to the latest version:

Bash

npm install -g @nitrostack/cli@latest
Check for updates:

Bash

npm outdated -g @nitrostack/cli
Troubleshooting
Permission Errors (Linux/macOS)
If you get EACCES errors:

Bash

# Option 1: Fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Option 2: Use nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
Command Not Found
If nitrostack-cli is not found:

Bash

# Check npm global bin directory
npm bin -g

# Add to PATH if needed
export PATH="$(npm bin -g):$PATH"
Version Mismatch
Ensure CLI version matches your project:

Bash

# Check CLI version
nitrostack-cli --version

# Check project dependencies
cat package.json | grep nitrostack
Uninstalling
To remove the CLI:

Bash

npm uninstall -g @nitrostack/cli
Next Steps
Init Command
Dev Command
Quick Start Guide
Next
👋 Introduction
/
cli
/
init
Init Command
Usage
Bash

nitrostack-cli init my-project
Options
Bash

nitrostack-cli init my-project --template typescript-auth
Available Templates
`typescript` - Basic TypeScript template
`typescript-auth` - Full-featured e-commerce template with auth
What It Creates
my-project/
├── src/
│   ├── modules/         # Feature modules
│   ├── app.module.ts    # Root module
│   └── index.ts         # Entry point
├── widgets/             # UI components
├── .env.example         # Environment template
└── package.json
Next Steps
`cd my-project`
`npm install`
`npm run dev`
Next
👋 Introduction
Dev Command
Overview
The dev command starts your NitroStack server in development mode with hot reload and the widget development server.

Note: NitroStudio is now a standalone application. The dev command no longer starts Studio automatically. See Studio Standalone Setup for details.

Usage
Bash

nitrostack-cli dev [options]
Options
Option	Description	Default
--no-open	Don't open browser (widget server)	false
What It Does
When you run nitrostack-cli dev, it:

Starts MCP Server

Runs your server via stdio transport
Watches for file changes in src/
Auto-reloads on changes
Starts Widget Server (if src/widgets exists)

Next.js dev server on port 3001
Hot reload for widgets
React Fast Refresh
Shows Ready Screen

Displays connection information
Shows how to connect NitroStudio
Architecture
┌─────────────────────────────────────────────────────────────────┐
│                    nitrostack-cli dev                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐     ┌────────────────────────┐      │
│  │     MCP Server         │     │    Widget Server       │      │
│  │     (stdio)            │     │    (port 3001)         │      │
│  │                        │     │                        │      │
│  │  • TypeScript watch    │     │  • Next.js dev         │      │
│  │  • Auto-reload         │     │  • Hot reload          │      │
│  │  • Tools & Resources   │     │  • React components    │      │
│  └────────────────────────┘     └────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Connect separately
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     NitroStudio (Standalone)                     │
│                                                                  │
│  • Select project folder                                         │
│  • Connects to MCP server                                        │
│  • Renders widgets from port 3001                                │
└─────────────────────────────────────────────────────────────────┘
Examples
Basic Usage
Bash

nitrostack-cli dev
Output:

┌──────────────────────────────────────────────────────────────────┐
│  NITROSTACK ━━ Development                                       │
│  Starting development servers                                    │
└──────────────────────────────────────────────────────────────────┘

✔ MCP Server ready (stdio)
✔ Widget Server ready (http://localhost:3001)

┌──────────────────────────────────────────────────────────────────┐
│  ✓ Development servers ready                                     │
│                                                                  │
│  MCP Server: stdio transport                                     │
│  Widgets: http://localhost:3001                                  │
│                                                                  │
│  To test your server:                                            │
│  1. Open NitroStudio                                             │
│  2. Select this project folder                                   │
│  3. Click Connect                                                │
└──────────────────────────────────────────────────────────────────┘
Using npm Script
Bash

npm run dev
Features
Hot Reload
Changes to your code automatically reload the server:

Watched Files:

src/**/*.ts - TypeScript source
src/**/*.js - JavaScript source
.env - Environment variables
Not Watched:

node_modules/
dist/
logs/
src/widgets/ (handled by Next.js)
Widget Hot Reload
Widgets support React Fast Refresh:

Save changes to see updates instantly
State preserved during reload
Fast iteration cycle
Environment Variables
Configure dev mode via .env:

Bash

# Widget port
WIDGET_PORT=3001

# Log level
LOG_LEVEL=info

# Transport type (for MCP)
MCP_TRANSPORT_TYPE=stdio
Development Workflow
Start Dev Mode

Bash

npm run dev
Open NitroStudio

Launch NitroStudio (standalone app)
Select your project folder
Click Connect
Make Changes

Edit tools in src/modules/*/tools.ts
Edit widgets in src/widgets/app/
Edit services in src/services/
Test in Studio

Use AI chat to test tools
Execute tools manually
Preview widgets
Iterate

Changes auto-reload
Test again
Repeat
Troubleshooting
Port Already in Use
Error: listen EADDRINUSE: address already in use :::3001

Solution:

Bash

# Find process using port
lsof -i :3001

# Kill process
kill -9 <PID>
TypeScript Errors
Error: Compilation errors on start

Solution:

Bash

# Check for type errors
npx tsc --noEmit

# Fix errors and restart
npm run dev
Widgets Not Loading
Error: 500 error when loading widgets

Solution:

Bash

# Check widget server
curl http://localhost:3001

# Ensure widget dependencies installed
cd src/widgets && npm install

# Restart
npm run dev
Hot Reload Not Working
Solution:

Bash

# Ensure watching is enabled
# Check file permissions
ls -la src/

# Restart dev mode
npm run dev

# Verify build succeeds
npm run build
Performance Tips
1. Exclude Large Directories
Add to .gitignore:

node_modules/
dist/
.next/
logs/
2. Use Incremental Compilation
In tsconfig.json:

JSON

{
  "compilerOptions": {
    "incremental": true
  }
}
3. Limit Watching
The dev server automatically excludes:

node_modules/
dist/
.next/
*.log
Connecting NitroStudio
Since Studio is now standalone:

Download NitroStudio from nitrostack.ai/studio
Start your project: npm run dev
Open Studio and select your project folder
Click Connect
Studio will connect to your MCP server and widget server automatically.

Advanced Usage
Add Widget Dependencies
To add a new package to your widgets:

Bash

npm run widget add @mui/material @emotion/react
Debug Mode
Enable verbose logging:

Bash

LOG_LEVEL=debug npm run dev
Custom Entry Point
By default, the server runs from src/index.ts. To use a different entry:

Bash

# In package.json
{
  "main": "src/custom-entry.ts"
}
Next Steps
Build Command
Install Command
Studio Standalone Setup
Testing Guide
Tip: Keep NitroStudio open while coding - it automatically refreshes when your server reloads!

Next
👋 Introduction
Build Command
Usage
Bash

nitrostack-cli build
What It Does
Compiles TypeScript to JavaScript
Bundles dependencies
Optimizes for production
Creates `dist/` directory
Output
dist/
├── index.js
├── modules/
└── ... (compiled code)
Production Deployment
Bash

nitrostack-cli build
node dist/index.js
Next Steps
Deployment Checklist
Docker Guide
Cloud Platforms
Next
👋 Introduction
Install Command
Overview
The install command runs npm install in both the root project directory and the src/widgets directory, ensuring all dependencies are properly installed.

Usage
Bash

nitrostack-cli install [options]
Options
Option	Description	Default
--skip-widgets	Skip installing widget dependencies	false
What It Does
When you run nitrostack-cli install:

Root Installation

Runs npm install in the project root
Installs SDK dependencies (nitrostack, zod, etc.)
Installs dev dependencies (typescript, @types/node)
Widget Installation (if src/widgets exists)

Runs npm install in src/widgets
Installs widget SDK (@nitrostack/widgets)
Installs Next.js and React dependencies
Examples
Basic Usage
Bash

nitrostack-cli install
Output:

┌──────────────────────────────────────────────────────────────────┐
│  NITROSTACK ━━ Install                                           │
│  Installing dependencies                                         │
└──────────────────────────────────────────────────────────────────┘

✔ Root dependencies installed
✔ Widget dependencies installed

┌──────────────────────────────────────────────────────────────────┐
│  ✓ Installation Complete                                         │
│                                                                  │
│  • Root packages: 45 packages                                    │
│  • Widget packages: 128 packages                                 │
└──────────────────────────────────────────────────────────────────┘
Skip Widgets
If you only want to install root dependencies:

Bash

nitrostack-cli install --skip-widgets
Using npm Script
Projects include a convenient npm script:

Bash

npm run install:all
This is equivalent to nitrostack-cli install.

When to Use
Use the install command when:

After cloning a project - Install all dependencies
After pulling updates - Sync dependencies with lock files
After clearing node_modules - Reinstall everything
Setting up CI/CD - Ensure consistent installations
Project Structure
The command expects this structure:

my-project/
├── package.json         # Root dependencies
├── package-lock.json    # Root lock file
├── src/
│   └── widgets/
│       ├── package.json       # Widget dependencies
│       └── package-lock.json  # Widget lock file
Comparison with npm install
Command	Root	Widgets
npm install	✓	✗
npm run install:all	✓	✓
nitrostack-cli install	✓	✓
nitrostack-cli install --skip-widgets	✓	✗
Troubleshooting
No Widgets Directory
If src/widgets doesn't exist, the command skips widget installation automatically:

✔ Root dependencies installed
ℹ No widgets directory found, skipping
Permission Errors
On Linux/macOS, if you encounter permission errors:

Bash

# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
Conflicting Versions
If you get peer dependency warnings:

Bash

# Use legacy peer deps mode
npm install --legacy-peer-deps
Or add to .npmrc:

legacy-peer-deps=true
Cache Issues
Clear npm cache if installation fails:

Bash

npm cache clean --force
nitrostack-cli install
CI/CD Integration
GitHub Actions
Yaml

- name: Install dependencies
  run: npx @nitrostack/cli install
Docker
Dockerfile

COPY package*.json ./
COPY src/widgets/package*.json ./src/widgets/
RUN npx @nitrostack/cli install
Related Commands
Upgrade Command - Update package versions
Dev Command - Start development server
Build Command - Build for production
Next Steps
Dev Command
Upgrade Command
Next
👋 Introduction
enerate Command
Overview
The generate command creates boilerplate code for common NitroStack components, saving time and ensuring consistency.

Usage
Bash

nitrostack-cli generate <type> [name] [options]
Types
Type	Description	Requires Name
types	Generate TypeScript types from tools	No
module	Generate a new module	Yes
tool	Generate a tool definition	Yes
resource	Generate a resource definition	Yes
prompt	Generate a prompt definition	Yes
guard	Generate an authentication guard	Yes
middleware	Generate middleware	Yes
interceptor	Generate an interceptor	Yes
pipe	Generate a pipe	Yes
filter	Generate an exception filter	Yes
service	Generate a service	Yes
Options
Option	Description
--module <name>	Specify module (for tools, resources, prompts)
--output <path>	Custom output path (for types)
--force	Overwrite existing files
Examples
Generate Types
Auto-generate TypeScript types from your tool definitions:

Bash

nitrostack-cli generate types
Output: src/types/generated-tools.ts

Typescript

export type GetProductInput = {
  product_id: string;
};

export type GetProductOutput = {
  id: string;
  name: string;
  price: number;
};

export interface ToolInputs {
  'get_product': GetProductInput;
}

export interface ToolOutputs {
  'get_product': GetProductOutput;
}
Custom output path:

Bash

nitrostack-cli generate types --output src/types/custom.ts
Generate Module
Create a new feature module:

Bash

nitrostack-cli generate module payments
Creates:

src/modules/payments/payments.module.ts
src/modules/payments/payments.tools.ts
src/modules/payments/payments.resources.ts
src/modules/payments/payments.prompts.ts
Generated Code:

Typescript

// payments.module.ts
import { Module } from '@nitrostack/core';
import { PaymentsTools } from './payments.tools.js';
import { PaymentsResources } from './payments.resources.js';
import { PaymentsPrompts } from './payments.prompts.js';

@Module({
  name: 'payments',
  description: 'Payments module',
  controllers: [PaymentsTools, PaymentsResources, PaymentsPrompts]
})
export class PaymentsModule {}
Generate Tool
Add a tool to an existing module:

Bash

nitrostack-cli generate tool process-payment --module payments
Creates: src/modules/payments/process-payment.tool.ts

Typescript

import { ToolDecorator as Tool, z, ExecutionContext } from '@nitrostack/core';

export class ProcessPaymentTool {
  @Tool({
    name: 'process_payment',
    description: 'TODO: Add description',
    inputSchema: z.object({
      // TODO: Add input fields
    })
  })
  async processPayment(input: any, context: ExecutionContext) {
    // TODO: Implement logic
    return {};
  }
}
Generate Resource
Bash

nitrostack-cli generate resource payment-status --module payments
Creates: src/modules/payments/payment-status.resource.ts

Typescript

import { ResourceDecorator as Resource, ExecutionContext } from '@nitrostack/core';

export class PaymentStatusResource {
  @Resource({
    uri: 'payment://status/{id}',
    name: 'Payment Status',
    description: 'TODO: Add description'
  })
  async getPaymentStatus(uri: string, context: ExecutionContext) {
    // Extract ID from URI
    const id = uri.split('/').pop();
    
    // TODO: Implement logic
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify({ id, status: 'pending' })
      }]
    };
  }
}
Generate Prompt
Bash

nitrostack-cli generate prompt payment-reminder --module payments
Creates: src/modules/payments/payment-reminder.prompt.ts

Typescript

import { PromptDecorator as Prompt, ExecutionContext } from '@nitrostack/core';

export class PaymentReminderPrompt {
  @Prompt({
    name: 'payment_reminder',
    description: 'TODO: Add description',
    arguments: [
      {
        name: 'customer_name',
        description: 'Customer name',
        required: true
      }
    ]
  })
  async getPaymentReminder(args: Record<string, string>, context: ExecutionContext) {
    return {
      messages: [
        {
          role: 'system',
          content: 'You are a payment reminder assistant.'
        },
        {
          role: 'user',
          content: `Create a payment reminder for ${args.customer_name}`
        }
      ]
    };
  }
}
Generate Guard
Create an authentication guard:

Bash

nitrostack-cli generate guard admin
Creates: src/guards/admin.guard.ts

Typescript

import { Guard, ExecutionContext } from '@nitrostack/core';

export class AdminGuard implements Guard {
  async canActivate(context: ExecutionContext): Promise<boolean> {
    // TODO: Implement admin check
    const user = context.auth?.user;
    return user?.role === 'admin';
  }
}
Generate Middleware
Bash

nitrostack-cli generate middleware logging
Creates: src/middleware/logging.middleware.ts

Typescript

import { Middleware, MiddlewareInterface, ExecutionContext } from '@nitrostack/core';

@Middleware()
export class LoggingMiddleware implements MiddlewareInterface {
  async use(context: ExecutionContext, next: () => Promise<any>) {
    const start = Date.now();
    console.log(`[${context.toolName}] Started`);
    
    const result = await next();
    
    const duration = Date.now() - start;
    console.log(`[${context.toolName}] Completed in ${duration}ms`);
    
    return result;
  }
}
Generate Interceptor
Bash

nitrostack-cli generate interceptor transform
Creates: src/interceptors/transform.interceptor.ts

Typescript

import { Interceptor, InterceptorInterface, ExecutionContext } from '@nitrostack/core';

@Interceptor()
export class TransformInterceptor implements InterceptorInterface {
  async intercept(context: ExecutionContext, next: () => Promise<any>) {
    const result = await next();
    
    return {
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    };
  }
}
Generate Pipe
Bash

nitrostack-cli generate pipe validation
Creates: src/pipes/validation.pipe.ts

Typescript

import { Pipe, PipeInterface, ArgumentMetadata } from '@nitrostack/core';

@Pipe()
export class ValidationPipe implements PipeInterface {
  transform(value: any, metadata: ArgumentMetadata) {
    // TODO: Implement validation
    return value;
  }
}
Generate Filter
Bash

nitrostack-cli generate filter http-exception
Creates: src/filters/http-exception.filter.ts

Typescript

import { ExceptionFilter, ExceptionFilterInterface, ExecutionContext } from '@nitrostack/core';

@ExceptionFilter()
export class HttpExceptionFilter implements ExceptionFilterInterface {
  catch(exception: any, context: ExecutionContext) {
    return {
      statusCode: exception.status || 500,
      message: exception.message || 'Internal server error',
      timestamp: new Date().toISOString(),
      tool: context.toolName
    };
  }
}
Generate Service
Bash

nitrostack-cli generate service email
Creates: src/services/email.service.ts

Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class EmailService {
  async send(to: string, subject: string, body: string) {
    // TODO: Implement email sending
    console.log(`Sending email to ${to}: ${subject}`);
  }
}
Workflow Examples
Adding a New Feature
Bash

# 1. Generate module
nitrostack-cli generate module notifications

# 2. Generate tools
nitrostack-cli generate tool send-notification --module notifications
nitrostack-cli generate tool get-notifications --module notifications

# 3. Generate service
nitrostack-cli generate service notification

# 4. Generate types
nitrostack-cli generate types

# 5. Register module in app.module.ts
# Import and add to imports array

# 6. Start dev mode
nitrostack-cli dev
Adding Authentication
Bash

# 1. Generate guard
nitrostack-cli generate guard jwt

# 2. Implement guard logic
# Edit src/guards/jwt.guard.ts

# 3. Use on tools
# @UseGuards(JWTGuard)

# 4. Test in Studio
nitrostack-cli dev
Refactoring to Services
Bash

# 1. Generate service
nitrostack-cli generate service user

# 2. Move business logic from tools to service
# 3. Inject service in tools via constructor
# 4. Register service in module providers
Best Practices
1. Generate Before Manual Creation
Always use generators for consistency:

Bash

# Good
nitrostack-cli generate module users

# Avoid
# Manually creating files
2. Regenerate Types Frequently
After changing tools:

Bash

nitrostack-cli generate types
This ensures type safety between backend and widgets.

3. Use Module Flag
Keep code organized:

Bash

# Good - organized
nitrostack-cli generate tool get-user --module users

# Avoid - scattered
nitrostack-cli generate tool get-user
4. Review Generated Code
Generators create boilerplate - customize it:

Typescript

// Generated
@Tool({
  name: 'my_tool',
  description: 'TODO: Add description',  // ← Update this
  inputSchema: z.object({
    // TODO: Add fields  // ← Add fields
  })
})
5. Commit Generated Files
Generated files are part of your codebase:

Bash

git add src/types/generated-tools.ts
git commit -m "chore: update generated types"
Troubleshooting
File Already Exists
Error: File already exists

Solution:

Bash

# Use --force to overwrite
nitrostack-cli generate tool my-tool --force

# Or rename/delete existing file
rm src/modules/my-module/my-tool.tool.ts
Module Not Found
Error: Module 'payments' not found

Solution:

Bash

# Create module first
nitrostack-cli generate module payments

# Then add tools
nitrostack-cli generate tool process-payment --module payments
Types Generation Failed
Error: No tool files found

Solution:

Bash

# Ensure tools exist
ls src/modules/*/tools.ts

# Check file naming
# Should be: *.tools.ts (not *.tool.ts)
Permission Denied
Error: EACCES: permission denied

Solution:

Bash

# Fix permissions
chmod +w src/

# Or run with sudo (not recommended)
sudo nitrostack-cli generate types
Advanced Usage
Custom Templates
Coming soon: Custom generator templates

Batch Generation
Bash

# Generate multiple at once
nitrostack-cli generate module payments && \
nitrostack-cli generate tool create-payment --module payments && \
nitrostack-cli generate tool get-payment --module payments && \
nitrostack-cli generate types
Integration with IDE
Many IDEs support running npm scripts:

JSON

{
  "scripts": {
    "gen:types": "nitrostack-cli generate types",
    "gen:module": "nitrostack-cli generate module"
  }
}
Next Steps
Testing Guide
Server Concepts
Tools Guide
Tip: Create aliases for frequent commands:

Bash

# In .bashrc or .zshrc
alias smg='nitrostack-cli generate'
alias smgt='nitrostack-cli generate types'
alias smgm='nitrostack-cli generate module'
Next
👋 Introduction
onfiguration Guide
nitrostack.config.ts
Create a `nitrostack.config.ts` file in your project root:

Typescript

export default {
  server: {
    name: 'my-mcp-server',
    version: '1.0.0',
    port: 3000
  },
  widgets: {
    port: 3001,
    devServer: true
  },
  logging: {
    level: 'info',
    file: 'logs/server.log'
  }
};
Environment Variables
Create a `.env` file:

Env

NODE_ENV=development
JWT_SECRET=your-secret-key
DATABASE_PATH=./data/database.db
PORT=3000
Next Steps
Dev Command
Build Command
Next
👋 Introduction
erver Concepts
Overview
NitroStack provides a NestJS-inspired architecture built around decorators, modules, and dependency injection. This guide covers the fundamental concepts required to build production-ready MCP servers.

Table of Contents
Application Bootstrap
Modules
Dependency Injection
Configuration
Execution Context
Lifecycle
Module Organization
Best Practices
Application Bootstrap
@McpApp Decorator
The @McpApp decorator marks your root module and configures the application:

Typescript

import { McpApp, Module, ConfigModule } from '@nitrostack/core';

@McpApp({
  module: AppModule,
  server: {
    name: 'my-mcp-server',
    version: '1.0.0'
  },
  logging: {
    level: 'info',
    file: 'logs/server.log'
  }
})
@Module({
  imports: [
    ConfigModule.forRoot(),
    JWTModule.forRoot({ secret: process.env.JWT_SECRET! }),
    ProductsModule,
    UsersModule
  ]
})
export class AppModule {}
McpApplicationFactory
Bootstrap your application using the factory pattern:

Typescript

import { McpApplicationFactory } from '@nitrostack/core';
import { AppModule } from './app.module.js';

async function bootstrap() {
  const server = await McpApplicationFactory.create(AppModule);
  await server.start();
}

bootstrap();
The factory performs the following initialization sequence:

Reads @McpApp metadata from the root module
Initializes the logging subsystem
Configures the dependency injection container
Registers all imported modules recursively
Builds and registers tools, resources, and prompts
Starts the MCP server transport
Modules
Module Architecture
Modules organize your application into cohesive, loosely-coupled units. Each module encapsulates related functionality and declares its dependencies explicitly.

Typescript

import { Module } from '@nitrostack/core';

@Module({
  name: 'products',
  description: 'Product catalog management',
  controllers: [ProductsTools, ProductsResources, ProductsPrompts],
  providers: [ProductService, DatabaseService],
  imports: [HttpModule],
  exports: [ProductService]
})
export class ProductsModule {}
Module Properties Reference
Property	Type	Description	Required
name	string	Unique module identifier	Yes
description	string	Human-readable description	No
controllers	Class[]	Tool, resource, and prompt classes	No
providers	Class[]	Services registered with the DI container	No
imports	Module[]	Modules whose exports are available	No
exports	Class[]	Providers available to importing modules	No
global	boolean	If true, providers are available globally	No
Controllers
Controllers contain your MCP primitives (tools, resources, and prompts):

Typescript

// products.tools.ts
import { ToolDecorator as Tool, ExecutionContext } from '@nitrostack/core';

export class ProductsTools {
  constructor(private productService: ProductService) {}

  @Tool({
    name: 'get_product',
    description: 'Retrieve product details by ID'
  })
  async getProduct(input: { product_id: string }, ctx: ExecutionContext) {
    return this.productService.findById(input.product_id);
  }
}

// products.resources.ts
import { ResourceDecorator as Resource, ExecutionContext } from '@nitrostack/core';

export class ProductsResources {
  constructor(private productService: ProductService) {}

  @Resource({
    uri: 'product://{id}',
    name: 'Product Details',
    mimeType: 'application/json'
  })
  async getProductResource(uri: string, ctx: ExecutionContext) {
    const id = uri.split('://')[1];
    const product = await this.productService.findById(id);
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(product, null, 2)
      }]
    };
  }
}

// products.prompts.ts
import { PromptDecorator as Prompt, ExecutionContext } from '@nitrostack/core';

export class ProductsPrompts {
  @Prompt({
    name: 'review_product',
    description: 'Generate a product review prompt'
  })
  async getReviewPrompt(args: { product_id: string }, ctx: ExecutionContext) {
    return [
      {
        role: 'user' as const,
        content: { type: 'text' as const, text: `Review product ${args.product_id}` }
      }
    ];
  }
}
Providers (Services)
Providers encapsulate business logic and can be injected into controllers or other providers:

Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class ProductService {
  constructor(private db: DatabaseService) {}

  async findById(id: string): Promise<Product | null> {
    return this.db.query('SELECT * FROM products WHERE id = $1', [id]);
  }

  async search(query: string, options?: SearchOptions): Promise<Product[]> {
    return this.db.query(
      'SELECT * FROM products WHERE name ILIKE $1 LIMIT $2 OFFSET $3',
      [`%${query}%`, options?.limit ?? 20, options?.offset ?? 0]
    );
  }

  async create(data: CreateProductDto): Promise<Product> {
    const result = await this.db.query(
      'INSERT INTO products (name, price, description) VALUES ($1, $2, $3) RETURNING *',
      [data.name, data.price, data.description]
    );
    return result[0];
  }
}
Module Imports and Exports
Imports allow a module to use providers exported by other modules:

Typescript

@Module({
  name: 'orders',
  imports: [ProductsModule, PaymentsModule],  // Use exports from these modules
  controllers: [OrdersTools],
  providers: [OrderService]
})
export class OrdersModule {}
Exports make providers available to importing modules:

Typescript

@Module({
  name: 'products',
  providers: [ProductService, InternalHelper],
  exports: [ProductService]  // Only ProductService is available to importers
})
export class ProductsModule {}
Dependency Injection
@Injectable Decorator
Mark classes for dependency injection:

Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class EmailService {
  constructor(private configService: ConfigService) {}

  async send(to: string, subject: string, body: string): Promise<void> {
    const smtpHost = this.configService.get('SMTP_HOST');
    // Implementation
  }
}
Constructor Injection
Dependencies are resolved and injected automatically via constructor parameters:

Typescript

export class UserTools {
  constructor(
    private userService: UserService,
    private emailService: EmailService,
    private auditService: AuditService
  ) {}

  @Tool({ name: 'create_user', description: 'Create a new user account' })
  async createUser(input: CreateUserInput, ctx: ExecutionContext) {
    const user = await this.userService.create(input);
    await this.emailService.send(user.email, 'Welcome', 'Account created');
    await this.auditService.log('user.created', { userId: user.id });
    return user;
  }
}
DI Container Behavior
The dependency injection container:

Resolves dependencies: Analyzes constructor parameters and resolves types
Creates instances: Instantiates classes with resolved dependencies
Manages lifecycle: Services are singleton by default (one instance per application)
Handles circular dependencies: Detects and reports circular dependency errors
Provider Scopes
By default, all providers are singleton scoped:

Typescript

@Injectable()
export class DatabaseService {
  // Single instance shared across the entire application
  private pool: Pool;

  constructor() {
    this.pool = new Pool(/* config */);
  }
}
Configuration
ConfigModule
The ConfigModule provides centralized configuration management:

Typescript

import { Module, ConfigModule } from '@nitrostack/core';

@Module({
  imports: [
    ConfigModule.forRoot({
      envFilePath: '.env',
      isGlobal: true,
      validate: (config) => {
        const required = ['DATABASE_URL', 'JWT_SECRET'];
        for (const key of required) {
          if (!config[key]) {
            throw new Error(`Missing required environment variable: ${key}`);
          }
        }
        return config;
      }
    })
  ]
})
export class AppModule {}
ConfigService
Access configuration values in your services:

Typescript

import { Injectable, ConfigService } from '@nitrostack/core';

@Injectable()
export class DatabaseService {
  private connectionString: string;

  constructor(private config: ConfigService) {
    this.connectionString = this.config.get('DATABASE_URL');
  }

  getPort(): number {
    return this.config.get('PORT', 3000);  // With default value
  }

  isProduction(): boolean {
    return this.config.get('NODE_ENV') === 'production';
  }
}
Execution Context
Every tool, resource, and prompt handler receives an ExecutionContext object:

Typescript

interface ExecutionContext {
  /** Authentication information (populated by guards) */
  auth?: {
    subject?: string;
    token?: string;
    [key: string]: unknown;
  };

  /** Logger instance for structured logging */
  logger: Logger;

  /** Name of the current tool (if applicable) */
  toolName?: string;

  /** Request identifier for tracing */
  requestId: string;

  /** Emit events to registered handlers */
  emit(event: string, data: unknown): void;

  /** Request metadata storage */
  metadata?: Record<string, unknown>;
}
Usage example:

Typescript

@Tool({ name: 'create_order', description: 'Create a new order' })
@UseGuards(JWTGuard)
async createOrder(input: CreateOrderInput, ctx: ExecutionContext) {
  const userId = ctx.auth?.subject;
  ctx.logger.info('Creating order', { userId, input });

  const order = await this.orderService.create(input, userId);
  ctx.emit('order.created', { orderId: order.id, userId });

  return order;
}
Lifecycle
Application Lifecycle
Bootstrap: McpApplicationFactory.create(AppModule) is called
Module Registration: Imports are resolved recursively, providers are registered
DI Container Setup: Dependency graph is built and validated
Server Initialization: Tools, resources, and prompts are registered
Server Start: Transport begins listening for requests
Request Lifecycle
Each incoming request follows this pipeline:

Request Arrives (STDIO/HTTP)
        │
        ▼
  Route to Handler
        │
        ▼
   Middleware (pre)
        │
        ▼
      Guards
        │
        ▼
       Pipes
        │
        ▼
  Handler Execution
        │
        ▼
    Interceptors
        │
        ▼
 Exception Filters
        │
        ▼
  Middleware (post)
        │
        ▼
   Send Response
Module Organization
Recommended Project Structure
src/
├── modules/
│   ├── auth/
│   │   ├── auth.module.ts
│   │   ├── auth.tools.ts
│   │   ├── auth.service.ts
│   │   └── guards/
│   │       └── jwt.guard.ts
│   ├── products/
│   │   ├── products.module.ts
│   │   ├── products.tools.ts
│   │   ├── products.resources.ts
│   │   ├── products.prompts.ts
│   │   ├── products.service.ts
│   │   └── dto/
│   │       ├── create-product.dto.ts
│   │       └── update-product.dto.ts
│   └── orders/
│       ├── orders.module.ts
│       ├── orders.tools.ts
│       └── orders.service.ts
├── common/
│   ├── middleware/
│   ├── interceptors/
│   ├── pipes/
│   └── filters/
├── app.module.ts
└── index.ts
Feature Modules
Organize code by business domain:

Typescript

// Feature module encapsulates all product-related functionality
@Module({
  name: 'products',
  controllers: [ProductsTools, ProductsResources],
  providers: [ProductService, ProductRepository],
  exports: [ProductService]
})
export class ProductsModule {}
Shared Modules
Create reusable modules for cross-cutting concerns:

Typescript

@Module({
  name: 'database',
  providers: [DatabaseService, TransactionManager],
  exports: [DatabaseService, TransactionManager],
  global: true  // Available to all modules without explicit import
})
export class DatabaseModule {}
Core Module
Essential application-wide services:

Typescript

@Module({
  name: 'core',
  providers: [Logger, CacheService, MetricsService],
  exports: [Logger, CacheService, MetricsService],
  global: true
})
export class CoreModule {}
Best Practices
1. Single Responsibility Modules
Each module should focus on a single business domain:

Typescript

// Recommended: Focused modules
ProductsModule   // Product catalog
OrdersModule     // Order processing
UsersModule      // User management
PaymentsModule   // Payment processing

// Avoid: Generic catch-all modules
ToolsModule      // Too broad
UtilsModule      // Unclear purpose
2. Encapsulate Business Logic in Services
Keep handlers thin; delegate logic to services:

Typescript

// Recommended
export class ProductsTools {
  constructor(private productService: ProductService) {}

  @Tool({ name: 'get_product' })
  async getProduct(input: { id: string }) {
    return this.productService.findById(input.id);
  }
}

// Avoid: Logic in handler
export class ProductsTools {
  @Tool({ name: 'get_product' })
  async getProduct(input: { id: string }) {
    const db = getDatabase();
    const result = await db.query('SELECT * FROM products WHERE id = $1', [input.id]);
    if (!result.rows[0]) throw new Error('Not found');
    return result.rows[0];
  }
}
3. Explicit Exports
Only export what other modules need:

Typescript

@Module({
  providers: [ProductService, ProductValidator, ProductMapper],
  exports: [ProductService]  // Only expose the service, not internal helpers
})
export class ProductsModule {}
4. Use ConfigService for Environment Variables
Never access process.env directly in services:

Typescript

// Recommended
@Injectable()
export class PaymentService {
  constructor(private config: ConfigService) {}

  private getApiKey(): string {
    return this.config.get('PAYMENT_API_KEY');
  }
}

// Avoid
@Injectable()
export class PaymentService {
  private apiKey = process.env.PAYMENT_API_KEY;  // Not testable
}
5. Consistent Module Structure
Follow a consistent file naming convention:

module-name/
├── module-name.module.ts      # Module definition
├── module-name.tools.ts       # Tool handlers
├── module-name.resources.ts   # Resource handlers
├── module-name.prompts.ts     # Prompt handlers
├── module-name.service.ts     # Business logic
├── module-name.repository.ts  # Data access (optional)
└── dto/                       # Data transfer objects
    ├── create-*.dto.ts
    └── update-*.dto.ts
Related Documentation
Tools Guide - Creating and configuring tools
Resources Guide - Exposing data resources
Dependency Injection - Advanced DI patterns
Testing Guide - Testing modules and services
Previous
⚡ Quick Start
Next
🛠️ Tools
Tools Guide
Overview
Tools are the primary mechanism for exposing functionality to AI models in the Model Context Protocol (MCP). They represent callable functions that AI agents can invoke to perform actions, retrieve data, or interact with external systems.

This guide covers tool definition, input validation, output schemas, behavioral annotations, execution context usage, and integration with NitroStack's middleware pipeline.

Table of Contents
Basic Tool Definition
Tool Decorator Options
Tool Annotations
Output Schema Validation
Input Validation with Zod
Execution Context
Middleware Integration
Caching and Rate Limiting
Dependency Injection
Error Handling
UI Widgets
Dynamic Tool Registration
Best Practices
Basic Tool Definition
Tools are defined using the @Tool decorator on class methods:

Typescript

import { ToolDecorator as Tool, z, ExecutionContext } from '@nitrostack/core';

export class WeatherTools {
  @Tool({
    name: 'get_weather',
    description: 'Retrieve current weather conditions for a specified location',
    inputSchema: z.object({
      city: z.string().describe('City name (e.g., "San Francisco")'),
      units: z.enum(['celsius', 'fahrenheit']).optional().default('celsius')
        .describe('Temperature unit preference')
    })
  })
  async getWeather(
    input: { city: string; units?: 'celsius' | 'fahrenheit' },
    context: ExecutionContext
  ) {
    context.logger.info('Fetching weather data', { city: input.city });

    const weather = await this.weatherService.getCurrentConditions(input.city);

    return {
      city: input.city,
      temperature: input.units === 'fahrenheit'
        ? this.toFahrenheit(weather.tempCelsius)
        : weather.tempCelsius,
      units: input.units ?? 'celsius',
      conditions: weather.conditions,
      humidity: weather.humidity,
      timestamp: new Date().toISOString()
    };
  }
}
Tool Decorator Options
Options Reference
Typescript

interface ToolOptions {
  /** Unique tool identifier (required) */
  name: string;

  /** Human-readable display name (optional) */
  title?: string;

  /** Clear description of what the tool does (required) */
  description: string;

  /** Zod schema for input validation */
  inputSchema?: ZodObject;

  /** Zod schema for output validation (optional) */
  outputSchema?: ZodObject;

  /** Behavioral hints for AI models and clients */
  annotations?: ToolAnnotations;

  /** UI status messages during tool execution (OpenAI Apps SDK) */
  invocation?: {
    invoking?: string;  // Shown while tool is running
    invoked?: string;   // Shown when tool completes
  };

  /** Example request/response for AI model guidance and widget preview */
  examples?: {
    request?: Record<string, unknown>;
    response?: Record<string, unknown>;
  };
}
Complete Example
Typescript

@Tool({
  name: 'create_user',
  title: 'Create User Account',
  description: 'Create a new user account with the provided details. Returns the created user object with generated ID.',
  inputSchema: z.object({
    email: z.string().email().describe('Valid email address for the account'),
    name: z.string().min(2).max(100).describe('Full name of the user'),
    role: z.enum(['user', 'admin', 'moderator']).default('user')
      .describe('User role determining access permissions'),
    metadata: z.record(z.string()).optional()
      .describe('Additional key-value pairs for custom attributes')
  }),
  outputSchema: z.object({
    id: z.string().describe('Generated user ID'),
    email: z.string(),
    name: z.string(),
    role: z.string(),
    createdAt: z.string()
  }),
  annotations: {
    destructiveHint: false,  // Creates new data, doesn't destroy
    idempotentHint: false,   // Creates new user each time
    readOnlyHint: false,     // Modifies system state
    openWorldHint: false     // Closed system operation
  },
  examples: {
    request: {
      email: 'jane.doe@example.com',
      name: 'Jane Doe',
      role: 'user'
    },
    response: {
      id: 'usr_abc123',
      email: 'jane.doe@example.com',
      name: 'Jane Doe',
      role: 'user',
      createdAt: '2024-01-15T10:30:00Z'
    }
  }
})
async createUser(input: CreateUserInput, ctx: ExecutionContext) {
  return this.userService.create(input);
}
Tool Annotations
Tool annotations provide behavioral hints to AI models and MCP clients about how a tool operates. These hints help clients make intelligent decisions about tool usage, such as whether to auto-approve certain operations or warn users about destructive actions.

Annotation Properties
Typescript

interface ToolAnnotations {
  /** 
   * If true, the tool may perform destructive updates (delete, overwrite).
   * If false, the tool only performs additive operations.
   * Default: true (assume destructive for safety)
   */
  destructiveHint?: boolean;

  /**
   * If true, calling the tool repeatedly with identical arguments
   * produces the same result with no additional side effects.
   * Default: false (assume not idempotent)
   */
  idempotentHint?: boolean;

  /**
   * If true, the tool does not modify any state - it only reads data.
   * Default: false (assume modifies state)
   */
  readOnlyHint?: boolean;

  /**
   * If true, the tool may interact with external systems or "open world"
   * entities beyond the local environment.
   * Default: true (assume external interactions possible)
   */
  openWorldHint?: boolean;
}
Annotation Examples by Use Case
Read-Only Data Retrieval:

Typescript

@Tool({
  name: 'get_user',
  title: 'Get User Profile',
  description: 'Retrieve user profile by ID',
  inputSchema: z.object({
    userId: z.string().describe('User ID')
  }),
  annotations: {
    readOnlyHint: true,      // No state modification
    idempotentHint: true,    // Same input = same output
    destructiveHint: false,  // No data destruction
    openWorldHint: false     // Internal database only
  }
})
async getUser(input: { userId: string }, ctx: ExecutionContext) {
  return this.userService.findById(input.userId);
}
Destructive Operation:

Typescript

@Tool({
  name: 'delete_user',
  title: 'Delete User Account',
  description: 'Permanently delete a user account and all associated data',
  inputSchema: z.object({
    userId: z.string().describe('User ID to delete')
  }),
  annotations: {
    destructiveHint: true,   // Permanently removes data
    idempotentHint: true,    // Deleting twice has same effect
    readOnlyHint: false,     // Modifies state
    openWorldHint: false     // Internal operation
  }
})
async deleteUser(input: { userId: string }, ctx: ExecutionContext) {
  return this.userService.delete(input.userId);
}
External API Call:

Typescript

@Tool({
  name: 'send_email',
  title: 'Send Email',
  description: 'Send an email via external email service',
  inputSchema: z.object({
    to: z.string().email(),
    subject: z.string(),
    body: z.string()
  }),
  annotations: {
    destructiveHint: false,  // Doesn't destroy data
    idempotentHint: false,   // Each call sends a new email
    readOnlyHint: false,     // Creates an email
    openWorldHint: true      // Interacts with external service
  }
})
async sendEmail(input: EmailInput, ctx: ExecutionContext) {
  return this.emailService.send(input);
}
Output Schema Validation
Output schemas define the expected structure of tool responses. They serve two purposes:

Documentation: Clients understand what data to expect
Validation: Runtime validation ensures responses match the schema
Basic Output Schema
Typescript

@Tool({
  name: 'get_product',
  title: 'Get Product Details',
  description: 'Retrieve product information by ID',
  inputSchema: z.object({
    productId: z.string()
  }),
  outputSchema: z.object({
    id: z.string(),
    name: z.string(),
    price: z.number(),
    currency: z.string(),
    inStock: z.boolean(),
    category: z.string().optional()
  })
})
async getProduct(input: { productId: string }, ctx: ExecutionContext) {
  return this.productService.findById(input.productId);
}
Complex Output Schema
Typescript

@Tool({
  name: 'search_products',
  title: 'Search Product Catalog',
  description: 'Search products with pagination',
  inputSchema: z.object({
    query: z.string(),
    page: z.number().default(1),
    limit: z.number().default(20)
  }),
  outputSchema: z.object({
    results: z.array(z.object({
      id: z.string(),
      name: z.string(),
      price: z.number(),
      relevanceScore: z.number()
    })),
    pagination: z.object({
      page: z.number(),
      limit: z.number(),
      total: z.number(),
      hasMore: z.boolean()
    })
  })
})
async searchProducts(input: SearchInput, ctx: ExecutionContext) {
  return this.searchService.query(input);
}
Input Validation with Zod
NitroStack uses Zod for runtime input validation. The schema is automatically converted to JSON Schema for MCP protocol compliance.

Primitive Types
Typescript

import { z } from '@nitrostack/core';

// String validation
z.string()
z.string().min(1).max(255)
z.string().email()
z.string().url()
z.string().uuid()
z.string().regex(/^[A-Z]{2}-\d{4}$/)

// Number validation
z.number()
z.number().int()
z.number().positive()
z.number().min(0).max(100)
z.number().multipleOf(0.01)  // Currency precision

// Boolean
z.boolean()

// Literal values
z.literal('active')
z.literal(42)
Complex Types
Typescript

// Enumerations
z.enum(['pending', 'processing', 'completed', 'failed'])

// Arrays
z.array(z.string())
z.array(z.number()).min(1).max(100)
z.array(z.object({ id: z.string() }))

// Objects
z.object({
  name: z.string(),
  address: z.object({
    street: z.string(),
    city: z.string(),
    postalCode: z.string()
  })
})

// Records (dynamic keys)
z.record(z.string())  // { [key: string]: string }
z.record(z.string(), z.number())  // { [key: string]: number }

// Unions
z.union([z.string(), z.number()])
z.discriminatedUnion('type', [
  z.object({ type: z.literal('email'), address: z.string().email() }),
  z.object({ type: z.literal('phone'), number: z.string() })
])
Modifiers
Typescript

// Optional fields
z.string().optional()  // string | undefined

// Nullable fields
z.string().nullable()  // string | null

// Default values
z.string().default('pending')
z.number().default(0)

// Transformations
z.string().transform(val => val.toLowerCase())
z.string().trim()
Complex Schema Example
Typescript

@Tool({
  name: 'create_order',
  description: 'Create a new order with line items and shipping details',
  inputSchema: z.object({
    customer: z.object({
      id: z.string().uuid().describe('Existing customer ID'),
      email: z.string().email().describe('Contact email for order updates')
    }),
    items: z.array(z.object({
      productId: z.string().describe('Product SKU or ID'),
      quantity: z.number().int().positive().describe('Quantity to order'),
      priceOverride: z.number().positive().optional()
        .describe('Optional price override for special pricing')
    })).min(1).describe('Order line items (at least one required)'),
    shipping: z.object({
      address: z.string().min(10).describe('Full street address'),
      city: z.string().describe('City name'),
      state: z.string().length(2).describe('Two-letter state code'),
      postalCode: z.string().regex(/^\d{5}(-\d{4})?$/).describe('ZIP code'),
      expedited: z.boolean().default(false).describe('Request expedited shipping')
    }),
    paymentMethod: z.enum(['card', 'ach', 'wire']).describe('Payment method'),
    notes: z.string().max(500).optional().describe('Special instructions')
  })
})
async createOrder(input: CreateOrderInput, ctx: ExecutionContext) {
  // Input is validated before handler execution
  return this.orderService.create(input);
}
Execution Context
Every tool handler receives an ExecutionContext object providing access to authentication, logging, and event emission.

Context Properties
Typescript

interface ExecutionContext {
  /** Authentication data populated by guards */
  auth?: {
    subject?: string;      // User/client identifier
    token?: string;        // Raw authentication token
    scopes?: string[];     // Permission scopes
    [key: string]: unknown;
  };

  /** Structured logger instance */
  logger: Logger;

  /** Current tool name */
  toolName?: string;

  /** Unique request identifier for tracing */
  requestId: string;

  /** Event emission function */
  emit(event: string, data: unknown): void;

  /** Request metadata (writable) */
  metadata?: Record<string, unknown>;
}
Usage Patterns
Typescript

@Tool({ name: 'process_payment' })
@UseGuards(JWTGuard)
async processPayment(input: PaymentInput, ctx: ExecutionContext) {
  // Access authenticated user
  const userId = ctx.auth?.subject;
  if (!userId) {
    throw new Error('Authentication required');
  }

  // Structured logging with context
  ctx.logger.info('Processing payment', {
    userId,
    amount: input.amount,
    requestId: ctx.requestId
  });

  try {
    const result = await this.paymentService.process(input, userId);

    // Emit event for async processing
    ctx.emit('payment.completed', {
      paymentId: result.id,
      userId,
      amount: input.amount
    });

    ctx.logger.info('Payment processed successfully', { paymentId: result.id });
    return result;
  } catch (error) {
    ctx.logger.error('Payment processing failed', {
      error: error.message,
      userId,
      amount: input.amount
    });
    throw error;
  }
}
Middleware Integration
Guards
Guards control access to tools based on authentication or authorization:

Typescript

import { UseGuards } from '@nitrostack/core';
import { JWTGuard } from './guards/jwt.guard.js';
import { RoleGuard } from './guards/role.guard.js';

// Single guard
@Tool({ name: 'get_profile' })
@UseGuards(JWTGuard)
async getProfile(input: {}, ctx: ExecutionContext) {
  return this.userService.findById(ctx.auth!.subject);
}

// Multiple guards (all must pass)
@Tool({ name: 'delete_user' })
@UseGuards(JWTGuard, RoleGuard('admin'))
async deleteUser(input: { userId: string }, ctx: ExecutionContext) {
  return this.userService.delete(input.userId);
}
Middleware
Middleware executes before and after the tool handler:

Typescript

import { UseMiddleware } from '@nitrostack/core';
import { LoggingMiddleware } from './middleware/logging.middleware.js';
import { TimingMiddleware } from './middleware/timing.middleware.js';

@Tool({ name: 'expensive_operation' })
@UseMiddleware(LoggingMiddleware, TimingMiddleware)
async expensiveOperation(input: OperationInput, ctx: ExecutionContext) {
  // Middleware executes in order: Logging -> Timing -> Handler -> Timing -> Logging
  return this.computeService.process(input);
}
Interceptors
Interceptors transform responses or add cross-cutting behavior:

Typescript

import { UseInterceptors } from '@nitrostack/core';
import { TransformInterceptor } from './interceptors/transform.interceptor.js';

@Tool({ name: 'get_data' })
@UseInterceptors(TransformInterceptor)
async getData(input: { id: string }, ctx: ExecutionContext) {
  return { value: 42 };
  // Interceptor transforms to: { success: true, data: { value: 42 }, timestamp: '...' }
}
Pipes
Pipes validate and transform input before handler execution:

Typescript

import { UsePipes } from '@nitrostack/core';
import { TrimPipe } from './pipes/trim.pipe.js';
import { ValidationPipe } from './pipes/validation.pipe.js';

@Tool({ name: 'search' })
@UsePipes(TrimPipe, ValidationPipe)
async search(input: { query: string }, ctx: ExecutionContext) {
  // Input strings are trimmed and validated
  return this.searchService.query(input.query);
}
Exception Filters
Exception filters handle errors and transform error responses:

Typescript

import { UseFilters } from '@nitrostack/core';
import { HttpExceptionFilter } from './filters/http-exception.filter.js';

@Tool({ name: 'risky_operation' })
@UseFilters(HttpExceptionFilter)
async riskyOperation(input: RiskyInput, ctx: ExecutionContext) {
  // Errors are caught and transformed by the filter
  return this.riskyService.execute(input);
}
Caching and Rate Limiting
Response Caching
Cache tool responses to improve performance:

Typescript

import { Cache } from '@nitrostack/core';

@Tool({ name: 'get_product' })
@Cache({
  ttl: 300,  // Cache for 5 minutes
  key: (input) => `product:${input.productId}`  // Custom cache key
})
async getProduct(input: { productId: string }, ctx: ExecutionContext) {
  return this.productService.findById(input.productId);
}

// Cache with event-based invalidation
@Tool({ name: 'get_user_profile' })
@Cache({
  ttl: 600,
  key: (input) => `user:${input.userId}:profile`,
  invalidateOn: ['user.updated', 'user.deleted']
})
async getUserProfile(input: { userId: string }, ctx: ExecutionContext) {
  return this.userService.getProfile(input.userId);
}
Rate Limiting
Protect tools from abuse with rate limiting:

Typescript

import { RateLimit } from '@nitrostack/core';

@Tool({ name: 'send_email' })
@RateLimit({
  requests: 10,
  window: '1m',  // 10 requests per minute
  key: (ctx) => ctx.auth?.subject || 'anonymous',  // Per-user limiting
  message: 'Email rate limit exceeded. Please wait before sending more emails.'
})
async sendEmail(input: EmailInput, ctx: ExecutionContext) {
  return this.emailService.send(input);
}

// Multiple rate limits
@Tool({ name: 'api_call' })
@RateLimit({ requests: 100, window: '1m' })   // Burst limit
@RateLimit({ requests: 1000, window: '1h' })  // Hourly limit
@RateLimit({ requests: 10000, window: '1d' }) // Daily limit
async apiCall(input: ApiInput, ctx: ExecutionContext) {
  return this.apiService.call(input);
}
Dependency Injection
Inject services into tool classes:

Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class ProductService {
  constructor(
    private db: DatabaseService,
    private cache: CacheService
  ) {}

  async findById(id: string): Promise<Product | null> {
    const cached = await this.cache.get(`product:${id}`);
    if (cached) return cached;

    const product = await this.db.query(
      'SELECT * FROM products WHERE id = $1',
      [id]
    );

    if (product) {
      await this.cache.set(`product:${id}`, product, 300);
    }

    return product;
  }
}

export class ProductTools {
  constructor(private productService: ProductService) {}

  @Tool({ name: 'get_product' })
  async getProduct(input: { productId: string }, ctx: ExecutionContext) {
    const product = await this.productService.findById(input.productId);
    if (!product) {
      throw new Error(`Product not found: ${input.productId}`);
    }
    return product;
  }
}
Error Handling
Standard Errors
Typescript

@Tool({ name: 'get_user' })
async getUser(input: { userId: string }, ctx: ExecutionContext) {
  const user = await this.userService.findById(input.userId);

  if (!user) {
    throw new Error(`User not found: ${input.userId}`);
  }

  return user;
}
Custom Error Classes
Typescript

export class NotFoundError extends Error {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`);
    this.name = 'NotFoundError';
  }
}

export class ValidationError extends Error {
  constructor(
    message: string,
    public readonly field: string,
    public readonly value: unknown
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

@Tool({ name: 'update_user' })
async updateUser(input: UpdateUserInput, ctx: ExecutionContext) {
  const user = await this.userService.findById(input.userId);
  if (!user) {
    throw new NotFoundError('User', input.userId);
  }

  if (input.email && !this.isValidEmail(input.email)) {
    throw new ValidationError('Invalid email format', 'email', input.email);
  }

  return this.userService.update(input.userId, input);
}
UI Widgets
Attach visual components to tool responses using the @Widget decorator.

Basic Widget Connection
Typescript

import { Widget } from '@nitrostack/core';

@Tool({
  name: 'get_order_summary',
  description: 'Get order summary with visual breakdown',
  inputSchema: z.object({
    orderId: z.string().describe('Order ID')
  })
})
@Widget('order-summary')  // Maps to src/widgets/app/order-summary/page.tsx
async getOrderSummary(input: { orderId: string }, ctx: ExecutionContext) {
  return {
    id: input.orderId,
    items: await this.orderService.getItems(input.orderId),
    total: await this.orderService.getTotal(input.orderId),
    status: await this.orderService.getStatus(input.orderId)
  };
}
Widget with Invocation Messages and Examples
For the best user experience, provide invocation messages and example data:

Typescript

@Tool({
  name: 'get_dashboard',
  title: 'User Dashboard',
  description: 'Get personalized dashboard with stats and recent activity',
  inputSchema: z.object({
    userId: z.string().describe('User ID')
  }),
  // Status messages shown in the UI during execution
  invocation: {
    invoking: 'Loading dashboard...',   // Shown while tool runs
    invoked: 'Dashboard ready'          // Shown when complete
  },
  // IMPORTANT: Example data is used for widget preview!
  examples: {
    request: { userId: 'user-123' },
    response: {
      user: { name: 'John Doe', avatar: '/avatars/john.jpg' },
      stats: { orders: 42, totalSpent: 1234.56 },
      recentOrders: [
        { id: 'order-1', total: 99.99, date: '2026-01-30' }
      ]
    }
  }
})
@Widget('user-dashboard')
async getDashboard(input: { userId: string }, ctx: ExecutionContext) {
  // Return data matching the example structure
  return { user: {...}, stats: {...}, recentOrders: [...] };
}
Important: The examples.response data is used by clients to render widget previews before the tool executes. Without it, the widget preview may not appear.

How Widget Metadata is Exposed
NitroStack exposes widget metadata in the tool's _meta field in multiple formats for compatibility:

JSON

{
  "name": "get_dashboard",
  "_meta": {
    "ui/template": "ui://widget/next-user-dashboard.html",
    "ui": { "resourceUri": "ui://widget/next-user-dashboard.html" },
    "openai/outputTemplate": "ui://widget/next-user-dashboard.html",
    "openai/toolInvocation/invoking": "Loading dashboard...",
    "openai/toolInvocation/invoked": "Dashboard ready",
    "tool/examples": { "request": {...}, "response": {...} }
  }
}
See the UI Widgets Guide for complete widget development documentation.

Dynamic Tool Registration
NitroStack supports dynamic tool registration and notifies connected clients when the tool list changes.

List Changed Notifications
When tools are added or removed at runtime, the server automatically sends a notifications/tools/list_changed notification to all connected clients. This enables dynamic tool discovery.

Typescript

import { McpApplicationFactory } from '@nitrostack/core';

// Access the server instance
const app = await McpApplicationFactory.create(AppModule);
const server = app.getServer();

// Notify clients after dynamic changes
server.notifyToolsListChanged();
Use Cases for Dynamic Tools
Feature flags: Enable/disable tools based on configuration
Permission-based: Show different tools based on user roles
Plugin systems: Load tools from external modules
A/B testing: Expose different tool sets to different clients
Best Practices
1. Write Clear Descriptions
Tool descriptions should be concise yet comprehensive:

Typescript

// Recommended: Clear, actionable description
@Tool({
  name: 'search_products',
  description: 'Search the product catalog by name, category, or price range. Returns paginated results with relevance scoring.'
})

// Avoid: Vague or minimal description
@Tool({
  name: 'search_products',
  description: 'Search products'
})
2. Document Schema Fields
Use .describe() on all schema fields:

Typescript

// Recommended: Documented fields
inputSchema: z.object({
  query: z.string().min(1).describe('Search query (product name, SKU, or keywords)'),
  category: z.string().optional().describe('Filter by category slug'),
  minPrice: z.number().optional().describe('Minimum price in USD'),
  maxPrice: z.number().optional().describe('Maximum price in USD'),
  page: z.number().int().positive().default(1).describe('Page number for pagination'),
  limit: z.number().int().min(1).max(100).default(20).describe('Results per page')
})

// Avoid: Undocumented fields
inputSchema: z.object({
  query: z.string(),
  category: z.string().optional(),
  minPrice: z.number().optional()
})
3. Provide Examples
Include realistic examples to help AI models understand expected inputs and outputs:

Typescript

@Tool({
  name: 'create_invoice',
  examples: {
    request: {
      customerId: 'cust_abc123',
      lineItems: [
        { description: 'Consulting services', amount: 5000, quantity: 1 }
      ],
      dueDate: '2024-02-15'
    },
    response: {
      id: 'inv_xyz789',
      number: 'INV-2024-0042',
      status: 'draft',
      total: 5000,
      createdAt: '2024-01-15T10:30:00Z'
    }
  }
})
4. Use Consistent Naming
Follow snake_case convention for tool names:

Typescript

// Recommended: snake_case with verb_noun pattern
'get_user'
'create_order'
'update_product'
'delete_invoice'
'search_customers'
'list_transactions'

// Avoid: Inconsistent casing or unclear names
'getUser'        // camelCase
'user'           // No verb
'doOperation'    // Unclear purpose
5. Delegate to Services
Keep tool handlers thin; business logic belongs in services:

Typescript

// Recommended: Thin handler
export class OrderTools {
  constructor(private orderService: OrderService) {}

  @Tool({ name: 'create_order' })
  async createOrder(input: CreateOrderInput, ctx: ExecutionContext) {
    return this.orderService.create(input, ctx.auth?.subject);
  }
}

// Avoid: Business logic in handler
export class OrderTools {
  @Tool({ name: 'create_order' })
  async createOrder(input: CreateOrderInput, ctx: ExecutionContext) {
    // Validation
    for (const item of input.items) {
      const product = await db.query('SELECT * FROM products WHERE id = $1', [item.productId]);
      if (!product) throw new Error('Product not found');
      if (product.stock < item.quantity) throw new Error('Insufficient stock');
    }
    // Calculate totals
    let total = 0;
    for (const item of input.items) {
      // ... complex calculation logic
    }
    // Insert order
    const result = await db.query('INSERT INTO orders ...');
    // ... more logic
  }
}
6. Handle Errors Gracefully
Provide meaningful error messages:

Typescript

@Tool({ name: 'transfer_funds' })
async transferFunds(input: TransferInput, ctx: ExecutionContext) {
  const sourceAccount = await this.accountService.findById(input.sourceId);
  if (!sourceAccount) {
    throw new Error(`Source account not found: ${input.sourceId}`);
  }

  if (sourceAccount.balance < input.amount) {
    throw new Error(
      `Insufficient funds. Available: ${sourceAccount.balance}, Requested: ${input.amount}`
    );
  }

  // Proceed with transfer
}
Returning Resource Links
Tools can return links to resources, allowing AI models to access additional context without embedding large data directly in the response.

Resource Link Type
Typescript

import type { ResourceLink } from '@nitrostack/core';

@Tool({
  name: 'create_report',
  title: 'Generate Report',
  description: 'Create a report and return a link to the full document'
})
async createReport(input: ReportInput, ctx: ExecutionContext) {
  const report = await this.reportService.generate(input);
  
  return {
    reportId: report.id,
    summary: report.summary,
    // Include a resource link for the full report
    fullReport: {
      type: 'resource_link',
      uri: `report://${report.id}`,
      name: 'Full Report',
      title: `${input.title} - Full Report`,
      description: 'Complete report with all data and visualizations',
      mimeType: 'application/json'
    } as ResourceLink
  };
}
Embedded Resources
For smaller data, embed the resource directly:

Typescript

import type { EmbeddedResource } from '@nitrostack/core';

@Tool({
  name: 'get_config',
  title: 'Get Configuration',
  description: 'Retrieve current configuration'
})
async getConfig(input: {}, ctx: ExecutionContext) {
  const config = await this.configService.get();
  
  return {
    version: config.version,
    embeddedConfig: {
      type: 'resource',
      resource: {
        uri: 'config://current',
        mimeType: 'application/json',
        text: JSON.stringify(config.settings, null, 2)
      }
    } as EmbeddedResource
  };
}
Related Documentation
Resources Guide - Exposing data as resources
Prompts Guide - Creating AI prompts
Middleware Guide - Request/response pipeline
Guards Guide - Access control
Interceptors Guide - Response transformation
Pipes Guide - Input validation and transformation
Caching Guide - Advanced caching strategies
Rate Limiting Guide - Protecting against abuse
Previous
🏗️ Server Concepts
Next
📚 Resources
Resources Guide
Overview
Resources in MCP expose data that AI models can read and reference during conversations. Unlike tools, which perform actions, resources provide static or semi-static data endpoints that describe available information.

This guide covers resource definition, annotations, URI templates, subscriptions, response formats, and integration with NitroStack's middleware pipeline.

Table of Contents
Basic Resource Definition
Resource Decorator Options
Resource Annotations
URI Templates
Resource Templates
Resource Subscriptions
Response Format
MIME Types
Middleware Integration
Dependency Injection
Dynamic Resource Registration
Best Practices
Basic Resource Definition
Resources are defined using the @Resource decorator on class methods:

Typescript

import { ResourceDecorator as Resource, ExecutionContext } from '@nitrostack/core';

export class ProductResources {
  constructor(private productService: ProductService) {}

  @Resource({
    uri: 'product://{id}',
    name: 'Product Details',
    description: 'Retrieve detailed product information including pricing and inventory',
    mimeType: 'application/json'
  })
  async getProduct(uri: string, context: ExecutionContext) {
    const id = this.extractId(uri, 'product://');
    const product = await this.productService.findById(id);

    if (!product) {
      throw new Error(`Product not found: ${id}`);
    }

    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(product, null, 2)
      }]
    };
  }

  private extractId(uri: string, prefix: string): string {
    return uri.replace(prefix, '');
  }
}
Resource Decorator Options
Options Reference
Typescript

interface ResourceOptions {
  /** URI template with optional parameters (required) */
  uri: string;

  /** Human-readable resource name (required) */
  name: string;

  /** Human-readable display title (optional) */
  title?: string;

  /** Description of what data the resource provides (required) */
  description: string;

  /** Content MIME type (default: 'text/plain') */
  mimeType?: string;

  /** Size of the resource in bytes (optional, for binary resources) */
  size?: number;

  /** Metadata hints for clients about how to use the resource */
  annotations?: ResourceAnnotations;

  /** Example response for documentation */
  examples?: {
    response?: unknown;
  };
}
Complete Example
Typescript

@Resource({
  uri: 'user://{userId}/profile',
  name: 'User Profile',
  title: 'User Profile Details',
  description: 'Complete user profile including account settings, preferences, and activity summary',
  mimeType: 'application/json',
  annotations: {
    audience: ['user', 'assistant'],
    priority: 0.8,
    lastModified: new Date().toISOString()
  },
  examples: {
    response: {
      id: 'usr_abc123',
      email: 'jane.doe@example.com',
      name: 'Jane Doe',
      preferences: {
        theme: 'dark',
        language: 'en',
        timezone: 'America/New_York'
      },
      stats: {
        ordersPlaced: 42,
        memberSince: '2023-01-15'
      }
    }
  }
})
async getUserProfile(uri: string, ctx: ExecutionContext) {
  const userId = this.extractParam(uri, /user:\/\/([^\/]+)\/profile/);
  const profile = await this.userService.getProfile(userId);

  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(profile, null, 2)
    }]
  };
}
Resource Annotations
Resource annotations provide metadata hints to AI models and MCP clients about how to use or display resources.

Annotation Properties
Typescript

interface ResourceAnnotations {
  /** 
   * Who should see this resource.
   * - 'user': For human consumption (UI display)
   * - 'assistant': For AI model context
   * Can include both for shared resources.
   */
  audience?: ('user' | 'assistant')[];

  /**
   * Importance of this resource (0.0 to 1.0).
   * Higher values indicate more important resources.
   * Clients may use this to prioritize display or context inclusion.
   */
  priority?: number;

  /**
   * ISO 8601 timestamp of when the resource was last modified.
   * Helps clients cache and invalidate resources appropriately.
   */
  lastModified?: string;
}
Annotation Examples
High-Priority Configuration:

Typescript

@Resource({
  uri: 'config://application',
  name: 'Application Configuration',
  title: 'App Config',
  description: 'Current application settings and feature flags',
  mimeType: 'application/json',
  annotations: {
    audience: ['assistant'],  // Primarily for AI context
    priority: 1.0,            // Highest priority
    lastModified: '2024-01-15T10:30:00Z'
  }
})
async getConfig(uri: string) {
  // ...
}
User-Facing Documentation:

Typescript

@Resource({
  uri: 'docs://api-reference',
  name: 'API Reference',
  title: 'API Documentation',
  description: 'Complete API documentation for developers',
  mimeType: 'text/markdown',
  annotations: {
    audience: ['user'],       // For human reading
    priority: 0.5,            // Medium priority
    lastModified: '2024-01-10T08:00:00Z'
  }
})
async getApiDocs(uri: string) {
  // ...
}
Shared Context Resource:

Typescript

@Resource({
  uri: 'dashboard://metrics',
  name: 'Dashboard Metrics',
  title: 'Live Metrics Dashboard',
  description: 'Real-time system metrics and KPIs',
  mimeType: 'application/json',
  annotations: {
    audience: ['user', 'assistant'],  // Both can use it
    priority: 0.9,
    lastModified: new Date().toISOString()
  }
})
async getDashboardMetrics(uri: string) {
  // ...
}
URI Templates
Static URIs
For singleton resources without parameters:

Typescript

@Resource({
  uri: 'config://application',
  name: 'Application Configuration',
  description: 'Current application configuration and feature flags'
})
async getAppConfig(uri: string, ctx: ExecutionContext) {
  const config = await this.configService.getAll();
  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(config, null, 2)
    }]
  };
}
Parameterized URIs
URIs can include dynamic parameters enclosed in curly braces:

Typescript

// Single parameter
@Resource({ uri: 'product://{id}', name: 'Product' })

// Multiple parameters
@Resource({ uri: 'order://{orderId}/item/{itemId}', name: 'Order Item' })

// Path-style parameter
@Resource({ uri: 'file:///{path}', name: 'File Contents' })
Parameter Extraction
Extract parameters from URIs using regular expressions:

Typescript

@Resource({
  uri: 'order://{orderId}/item/{itemId}',
  name: 'Order Line Item',
  description: 'Details for a specific item within an order'
})
async getOrderItem(uri: string, ctx: ExecutionContext) {
  const match = uri.match(/order:\/\/([^\/]+)\/item\/([^\/]+)/);
  if (!match) {
    throw new Error(`Invalid URI format: ${uri}`);
  }

  const [, orderId, itemId] = match;
  const item = await this.orderService.getItem(orderId, itemId);

  if (!item) {
    throw new Error(`Order item not found: ${orderId}/${itemId}`);
  }

  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(item, null, 2)
    }]
  };
}
URI Utility Helper
Consider creating a utility for parameter extraction:

Typescript

// utils/uri.ts
export function parseUri(uri: string, template: string): Record<string, string> {
  const paramNames: string[] = [];
  const regexPattern = template.replace(/\{(\w+)\}/g, (_, name) => {
    paramNames.push(name);
    return '([^/]+)';
  });

  const match = uri.match(new RegExp(`^${regexPattern}$`));
  if (!match) {
    throw new Error(`URI does not match template: ${uri}`);
  }

  const params: Record<string, string> = {};
  paramNames.forEach((name, index) => {
    params[name] = match[index + 1];
  });

  return params;
}

// Usage
@Resource({ uri: 'order://{orderId}/item/{itemId}' })
async getOrderItem(uri: string, ctx: ExecutionContext) {
  const params = parseUri(uri, 'order://{orderId}/item/{itemId}');
  const item = await this.orderService.getItem(params.orderId, params.itemId);
  // ...
}
Resource Templates
Resource templates define parameterized URI patterns that clients can use to discover and construct resource URIs. Unlike regular resources, templates describe a pattern rather than a concrete resource.

Defining Resource Templates
Typescript

import { createResourceTemplate } from '@nitrostack/core';

// In your module setup
const productTemplate = createResourceTemplate({
  uriTemplate: 'product://{productId}',
  name: 'Product Resource',
  title: 'Product Details Template',
  description: 'Template for accessing individual product resources',
  mimeType: 'application/json',
  annotations: {
    audience: ['assistant'],
    priority: 0.7
  }
});

// Register with server
server.resourceTemplate(productTemplate);
Template Parameters
Templates use curly brace syntax for parameters:

Typescript

// Single parameter
'product://{id}'

// Multiple parameters  
'user://{userId}/order/{orderId}'

// Path parameters
'file:///{path}'
Use Cases
Resource templates are useful when:

Dynamic resources: Resources that don't exist until requested (e.g., user-specific data)
Large datasets: Instead of listing all products, provide a template for accessing any product
API discovery: Help AI models understand available resource patterns
Resource Subscriptions
Clients can subscribe to resources to receive notifications when they change. This enables real-time updates without polling.

Server Capabilities
NitroStack declares subscription support in server capabilities:

Typescript

{
  capabilities: {
    resources: {
      subscribe: true,
      listChanged: true
    }
  }
}
Handling Subscriptions
When a client subscribes to a resource, your application can track subscriptions and notify clients of changes:

Typescript

import { McpApplicationFactory } from '@nitrostack/core';

const app = await McpApplicationFactory.create(AppModule);
const server = app.getServer();

// When a resource changes, notify subscribers
function onResourceUpdated(uri: string) {
  server.notifyResourceUpdated(uri);
}

// Example: Update product and notify
async function updateProduct(productId: string, data: ProductData) {
  await this.productRepo.update(productId, data);
  onResourceUpdated(`product://${productId}`);
}
Subscription Flow
Client subscribes: resources/subscribe with resource URI
Server tracks: Maintains list of subscribed URIs
Resource changes: Your code detects the change
Server notifies: Sends notifications/resources/updated with URI
Client refreshes: Fetches updated resource content
List Changed Notifications
When resources are added or removed, notify clients:

Typescript

// After adding a new resource
server.notifyResourcesListChanged();

// After removing a resource
server.notifyResourcesListChanged();
Response Format
Standard Response Structure
Resources must return an object with a contents array:

Typescript

return {
  contents: [
    {
      uri: string;           // The requested URI
      mimeType?: string;     // Content type
      text?: string;         // Text content
      blob?: Uint8Array;     // Binary content
    }
  ]
};
Single Content Response
Most resources return a single content item:

Typescript

return {
  contents: [{
    uri: 'product://prod-123',
    mimeType: 'application/json',
    text: JSON.stringify({
      id: 'prod-123',
      name: 'Widget',
      price: 29.99
    }, null, 2)
  }]
};
Multiple Content Response
Resources can return multiple content items:

Typescript

@Resource({
  uri: 'report://{id}',
  name: 'Report Bundle',
  description: 'Complete report with summary, data, and visualizations'
})
async getReport(uri: string, ctx: ExecutionContext) {
  const id = uri.replace('report://', '');
  const report = await this.reportService.generate(id);

  return {
    contents: [
      {
        uri: `${uri}/summary`,
        mimeType: 'text/plain',
        text: report.executiveSummary
      },
      {
        uri: `${uri}/data`,
        mimeType: 'application/json',
        text: JSON.stringify(report.data, null, 2)
      },
      {
        uri: `${uri}/metadata`,
        mimeType: 'application/json',
        text: JSON.stringify({
          generatedAt: report.timestamp,
          author: report.author,
          version: report.version
        }, null, 2)
      }
    ]
  };
}
MIME Types
Common MIME Types
MIME Type	Use Case
application/json	Structured data, API responses
text/plain	Plain text, logs
text/markdown	Documentation, formatted content
text/html	Rich formatted content
text/csv	Tabular data
application/xml	XML documents
image/png, image/jpeg	Images (use blob field)
Type-Specific Examples
Typescript

// JSON data
@Resource({
  uri: 'api://users',
  mimeType: 'application/json'
})
async getUsers(uri: string) {
  const users = await this.userService.findAll();
  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(users, null, 2)
    }]
  };
}

// Markdown documentation
@Resource({
  uri: 'docs://api-reference',
  mimeType: 'text/markdown'
})
async getApiDocs(uri: string) {
  const docs = await this.docsService.getApiReference();
  return {
    contents: [{
      uri,
      mimeType: 'text/markdown',
      text: docs
    }]
  };
}

// CSV export
@Resource({
  uri: 'export://transactions',
  mimeType: 'text/csv'
})
async getTransactionsCsv(uri: string) {
  const csv = await this.exportService.transactionsToCsv();
  return {
    contents: [{
      uri,
      mimeType: 'text/csv',
      text: csv
    }]
  };
}
Middleware Integration
Guards for Protected Resources
Typescript

import { UseGuards } from '@nitrostack/core';
import { JWTGuard } from './guards/jwt.guard.js';

@Resource({
  uri: 'user://{id}/private-data',
  name: 'Private User Data',
  description: 'Sensitive user data requiring authentication'
})
@UseGuards(JWTGuard)
async getPrivateData(uri: string, ctx: ExecutionContext) {
  const requesterId = ctx.auth?.subject;
  const targetId = uri.match(/user:\/\/([^\/]+)/)?.[1];

  // Authorization check
  if (requesterId !== targetId) {
    throw new Error('Access denied: You can only access your own data');
  }

  const data = await this.userService.getPrivateData(targetId);
  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(data, null, 2)
    }]
  };
}
Caching
Typescript

import { Cache } from '@nitrostack/core';

@Resource({
  uri: 'config://application',
  name: 'Application Config'
})
@Cache({ ttl: 3600 })  // Cache for 1 hour
async getConfig(uri: string) {
  const config = await this.configService.load();
  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(config, null, 2)
    }]
  };
}

// Cache with custom key
@Resource({ uri: 'weather://{city}' })
@Cache({
  ttl: 600,  // 10 minutes
  key: (uri) => `weather:${uri.replace('weather://', '')}`
})
async getWeather(uri: string) {
  // ...
}
UI Widgets
Typescript

import { Widget } from '@nitrostack/core';

@Resource({
  uri: 'dashboard://metrics',
  name: 'Dashboard Metrics'
})
@Widget('metrics-dashboard')  // Renders visual dashboard
async getDashboardMetrics(uri: string) {
  const metrics = await this.metricsService.getDashboard();
  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(metrics, null, 2)
    }]
  };
}
Dependency Injection
Inject services into resource classes:

Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class ProductRepository {
  constructor(private db: DatabaseService) {}

  async findById(id: string): Promise<Product | null> {
    return this.db.query('SELECT * FROM products WHERE id = $1', [id]);
  }

  async findAll(options?: ListOptions): Promise<Product[]> {
    return this.db.query(
      'SELECT * FROM products ORDER BY created_at DESC LIMIT $1 OFFSET $2',
      [options?.limit ?? 50, options?.offset ?? 0]
    );
  }
}

export class ProductResources {
  constructor(private productRepo: ProductRepository) {}

  @Resource({ uri: 'product://{id}', name: 'Product' })
  async getProduct(uri: string) {
    const id = uri.replace('product://', '');
    const product = await this.productRepo.findById(id);

    if (!product) {
      throw new Error(`Product not found: ${id}`);
    }

    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(product, null, 2)
      }]
    };
  }

  @Resource({ uri: 'products://catalog', name: 'Product Catalog' })
  @Cache({ ttl: 300 })
  async getCatalog(uri: string) {
    const products = await this.productRepo.findAll();
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(products, null, 2)
      }]
    };
  }
}
Dynamic Resource Registration
NitroStack supports dynamic resource registration at runtime, with automatic client notifications.

Adding Resources Dynamically
Typescript

import { McpApplicationFactory, createResource } from '@nitrostack/core';

const app = await McpApplicationFactory.create(AppModule);
const server = app.getServer();

// Create a new resource
const newResource = createResource({
  uri: 'dynamic://new-data',
  name: 'Dynamic Data',
  title: 'Dynamically Added Data',
  description: 'A resource added at runtime',
  mimeType: 'application/json',
  annotations: {
    audience: ['assistant'],
    priority: 0.5
  }
}, async (uri, context) => {
  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify({ data: 'dynamic content' })
    }]
  };
});

// Register and notify clients
server.resource(newResource);
server.notifyResourcesListChanged();
Use Cases
Plugin systems: Load resources from external modules
User-generated content: Create resources based on user data
Feature flags: Enable/disable resources dynamically
Multi-tenancy: Provide tenant-specific resources
Best Practices
1. Use Descriptive URI Schemes
Choose URI schemes that clearly indicate the resource type:

Typescript

// Recommended: Clear, domain-specific schemes
'product://{id}'
'user://{userId}/profile'
'order://{orderId}/invoice'
'config://application'
'docs://api-reference'

// Avoid: Generic or ambiguous schemes
'resource://{id}'
'data://{type}/{id}'
'get://{something}'
2. Set Appropriate MIME Types
Match the MIME type to the actual content:

Typescript

// Recommended: Accurate MIME types
@Resource({ uri: 'api://users', mimeType: 'application/json' })
@Resource({ uri: 'docs://readme', mimeType: 'text/markdown' })
@Resource({ uri: 'export://data', mimeType: 'text/csv' })

// Avoid: Using text/plain for everything
@Resource({ uri: 'api://users', mimeType: 'text/plain' })  // Incorrect for JSON
3. Validate URI Parameters
Always validate extracted parameters:

Typescript

@Resource({ uri: 'user://{id}' })
async getUser(uri: string) {
  const id = uri.replace('user://', '');

  // Validate parameter
  if (!id || id.length < 3) {
    throw new Error('Invalid user ID format');
  }

  const user = await this.userService.findById(id);
  if (!user) {
    throw new Error(`User not found: ${id}`);
  }

  return {
    contents: [{
      uri,
      mimeType: 'application/json',
      text: JSON.stringify(user, null, 2)
    }]
  };
}
4. Cache Appropriately
Cache static or slowly-changing resources:

Typescript

// Recommended: Cache static configuration
@Resource({ uri: 'config://app' })
@Cache({ ttl: 3600 })  // 1 hour - configuration rarely changes

// Recommended: Short cache for external APIs
@Resource({ uri: 'weather://{city}' })
@Cache({ ttl: 600 })  // 10 minutes - weather updates periodically

// Avoid: Long cache for volatile data
@Resource({ uri: 'stock://{symbol}' })
@Cache({ ttl: 3600 })  // Too long for real-time stock prices
5. Delegate to Services
Keep resource handlers thin:

Typescript

// Recommended: Delegate to service
export class ReportResources {
  constructor(private reportService: ReportService) {}

  @Resource({ uri: 'report://{id}' })
  async getReport(uri: string) {
    const id = uri.replace('report://', '');
    const report = await this.reportService.findById(id);
    return {
      contents: [{ uri, text: JSON.stringify(report, null, 2) }]
    };
  }
}

// Avoid: Business logic in handler
export class ReportResources {
  @Resource({ uri: 'report://{id}' })
  async getReport(uri: string) {
    const id = uri.replace('report://', '');
    const db = getDatabase();
    const rows = await db.query('SELECT * FROM reports WHERE id = $1', [id]);
    const report = rows[0];
    // ... complex transformation logic
    // ... aggregation logic
    return { contents: [{ uri, text: JSON.stringify(result) }] };
  }
}
6. Document with Examples
Provide example responses in decorator options:

Typescript

@Resource({
  uri: 'product://{id}',
  name: 'Product Details',
  description: 'Complete product information including pricing, inventory, and metadata',
  mimeType: 'application/json',
  examples: {
    response: {
      id: 'prod_abc123',
      name: 'Premium Widget',
      price: 49.99,
      currency: 'USD',
      inventory: { available: 150, reserved: 12 },
      metadata: { category: 'electronics', weight: '0.5kg' }
    }
  }
})
Related Documentation
Tools Guide - Creating callable tools
Prompts Guide - Creating AI prompts
Middleware Guide - Request/response pipeline
Guards Guide - Access control
Caching Guide - Advanced caching strategies
Events Guide - Event-driven updates
UI Widgets Guide - Visual components
Previous
🛠️ Tools
Next
💬 Prompts
Prompts Guide
Overview
Prompts provide pre-defined conversation templates that AI models can use to initiate structured interactions. They serve as context-rich starting points for specific tasks, ensuring consistent and effective AI conversations.

This guide covers prompt definition, argument handling, response formatting, dynamic registration, and integration patterns.

Table of Contents
Basic Prompt Definition
Prompt Decorator Options
Prompt Arguments
Response Format
Dynamic Prompts
Middleware Integration
Dependency Injection
Dynamic Prompt Registration
Best Practices
Basic Prompt Definition
Prompts are defined using the @Prompt decorator on class methods:

Typescript

import { PromptDecorator as Prompt, ExecutionContext } from '@nitrostack/core';

export class ProductPrompts {
  constructor(private productService: ProductService) {}

  @Prompt({
    name: 'product_review',
    description: 'Generate a structured product review request',
    arguments: [
      {
        name: 'product_id',
        description: 'The product identifier to review',
        required: true
      }
    ]
  })
  async getReviewPrompt(args: { product_id: string }, context: ExecutionContext) {
    const product = await this.productService.findById(args.product_id);

    if (!product) {
      throw new Error(`Product not found: ${args.product_id}`);
    }

    return [
      {
        role: 'user' as const,
        content: {
          type: 'text' as const,
          text: `Please provide a detailed review for: ${product.name}

Product Details:
- Category: ${product.category}
- Price: $${product.price}
- Description: ${product.description}

Review Criteria:
1. Quality and durability
2. Value for money
3. Key features and benefits
4. Potential improvements
5. Overall recommendation`
        }
      }
    ];
  }
}
Prompt Decorator Options
Options Reference
Typescript

interface PromptOptions {
  /** Unique prompt identifier (required) */
  name: string;

  /** Human-readable display title (optional) */
  title?: string;

  /** Description of the prompt's purpose (required) */
  description: string;

  /** Input parameters for the prompt */
  arguments?: Array<{
    name: string;
    description: string;
    required?: boolean;
  }>;
}
Complete Example
Typescript

@Prompt({
  name: 'code_review',
  title: 'Code Review Assistant',
  description: 'Generate a comprehensive code review checklist with language-specific best practices',
  arguments: [
    {
      name: 'language',
      description: 'Programming language (typescript, python, go, java)',
      required: true
    },
    {
      name: 'code',
      description: 'The code snippet to review',
      required: true
    },
    {
      name: 'focus_areas',
      description: 'Specific areas to focus on (security, performance, readability)',
      required: false
    }
  ]
})
async getCodeReviewPrompt(
  args: { language: string; code: string; focus_areas?: string },
  ctx: ExecutionContext
) {
  const focusAreas = args.focus_areas?.split(',').map(s => s.trim()) || [
    'correctness',
    'readability',
    'performance',
    'security'
  ];

  const checklistItems = this.getLanguageChecklist(args.language, focusAreas);

  return [
    {
      role: 'user' as const,
      content: `Review the following ${args.language} code:

\`\`\`${args.language}
${args.code}
\`\`\`

Focus Areas: ${focusAreas.join(', ')}

Review Checklist:
${checklistItems.map((item, i) => `${i + 1}. ${item}`).join('\n')}

Provide specific, actionable feedback for each applicable item.`
    }
  ];
}
Title vs Name
The title field provides a human-readable display name, while name serves as the unique identifier:

Typescript

@Prompt({
  name: 'station_briefing',      // Internal identifier (snake_case)
  title: 'Station Briefing',     // Display name for UI
  description: 'Generate operational briefing for station personnel'
})
Prompt Arguments
Required vs Optional Arguments
Typescript

@Prompt({
  name: 'data_analysis',
  description: 'Generate a data analysis request with configurable parameters',
  arguments: [
    {
      name: 'dataset',
      description: 'Identifier of the dataset to analyze',
      required: true  // Must be provided
    },
    {
      name: 'analysis_type',
      description: 'Type of analysis (descriptive, predictive, diagnostic)',
      required: false  // Optional with default
    },
    {
      name: 'output_format',
      description: 'Desired output format (summary, detailed, tabular)',
      required: false
    }
  ]
})
async getAnalysisPrompt(
  args: { dataset: string; analysis_type?: string; output_format?: string },
  ctx: ExecutionContext
) {
  const analysisType = args.analysis_type || 'descriptive';
  const outputFormat = args.output_format || 'summary';

  return [
    {
      role: 'user' as const,
      content: {
        type: 'text' as const,
        text: `Perform ${analysisType} analysis on dataset: ${args.dataset}

Output Format: ${outputFormat}

Please include:
- Key findings and insights
- Statistical summaries where applicable
- Visualizations recommendations
- Actionable conclusions`
      }
    }
  ];
}
Argument Validation
Typescript

@Prompt({
  name: 'report_generation',
  description: 'Generate a business report prompt',
  arguments: [
    { name: 'report_type', description: 'Type of report', required: true },
    { name: 'period', description: 'Reporting period', required: true }
  ]
})
async getReportPrompt(
  args: { report_type: string; period: string },
  ctx: ExecutionContext
) {
  // Validate report type
  const validTypes = ['sales', 'inventory', 'financial', 'operational'];
  if (!validTypes.includes(args.report_type)) {
    throw new Error(
      `Invalid report type: ${args.report_type}. Valid types: ${validTypes.join(', ')}`
    );
  }

  // Validate period format
  const periodRegex = /^(Q[1-4]-\d{4}|\d{4}-\d{2}|\d{4})$/;
  if (!periodRegex.test(args.period)) {
    throw new Error(
      `Invalid period format: ${args.period}. Expected: Q1-2024, 2024-01, or 2024`
    );
  }

  return [
    {
      role: 'user' as const,
      content: {
        type: 'text' as const,
        text: `Generate a ${args.report_type} report for period: ${args.period}`
      }
    }
  ];
}
Response Format
Standard Response Structure
Prompts return an array of message objects. Content can be a plain string or a structured object:

Typescript

// Simple string content (recommended)
return [
  {
    role: 'user' | 'assistant',
    content: string
  }
];

// Or structured content object
return [
  {
    role: 'user' | 'assistant',
    content: {
      type: 'text',
      text: string
    }
  }
];
Note: Use plain string content for simplicity. The server automatically wraps it in the proper MCP format.

Single Message Prompt
Typescript

@Prompt({ 
  name: 'simple_task', 
  title: 'Simple Task',
  description: 'Simple task prompt' 
})
async getSimplePrompt(args: { task: string }) {
  return [
    {
      role: 'user' as const,
      content: `Please help me with: ${args.task}`
    }
  ];
}
Multi-Turn Conversation Prompt
Typescript

@Prompt({
  name: 'interview_prep',
  title: 'Mock Interview',
  description: 'Start a mock interview session',
  arguments: [
    { name: 'role', description: 'Job role being interviewed for', required: true },
    { name: 'difficulty', description: 'Interview difficulty level', required: false }
  ]
})
async getInterviewPrompt(args: { role: string; difficulty?: string }) {
  const difficulty = args.difficulty || 'intermediate';

  return [
    {
      role: 'user' as const,
      content: `I want to practice for a ${args.role} interview. Please act as the interviewer.`
    },
    {
      role: 'assistant' as const,
      content: `I'll conduct a ${difficulty}-level interview for the ${args.role} position. Let's begin with an introduction. Please tell me about your background and why you're interested in this role.`
    },
    {
      role: 'user' as const,
      content: `I'm ready. Please start with the first question.`
    }
  ];
}
Structured Context Prompt
Typescript

@Prompt({
  name: 'bug_investigation',
  title: 'Debug Assistant',
  description: 'Provide debugging assistance with full context',
  arguments: [
    { name: 'error_message', required: true, description: 'The error message' },
    { name: 'stack_trace', required: false, description: 'Stack trace if available' },
    { name: 'environment', required: false, description: 'Runtime environment' }
  ]
})
async getBugPrompt(
  args: { error_message: string; stack_trace?: string; environment?: string }
) {
  let contextSection = `Error Message:
${args.error_message}`;

  if (args.stack_trace) {
    contextSection += `

Stack Trace:
\`\`\`
${args.stack_trace}
\`\`\``;
  }

  if (args.environment) {
    contextSection += `

Environment: ${args.environment}`;
  }

  return [
    {
      role: 'user' as const,
      content: `I'm encountering an error and need help debugging it.

${contextSection}

Please help me:
1. Understand what the error means
2. Identify the likely cause
3. Suggest potential fixes
4. Recommend debugging steps if the cause isn't clear`
    }
  ];
}
Dynamic Prompts
Data-Driven Prompts
Typescript

@Prompt({
  name: 'order_analysis',
  description: 'Analyze order and suggest optimizations',
  arguments: [
    { name: 'order_id', required: true, description: 'Order to analyze' }
  ]
})
async getOrderAnalysisPrompt(args: { order_id: string }, ctx: ExecutionContext) {
  const order = await this.orderService.findById(args.order_id);

  if (!order) {
    throw new Error(`Order not found: ${args.order_id}`);
  }

  const orderSummary = `
Order ID: ${order.id}
Customer: ${order.customerName}
Date: ${order.createdAt}
Status: ${order.status}

Items:
${order.items.map(item => `- ${item.name} x${item.quantity} @ $${item.price}`).join('\n')}

Subtotal: $${order.subtotal}
Tax: $${order.tax}
Shipping: $${order.shipping}
Total: $${order.total}`;

  return [
    {
      role: 'user' as const,
      content: {
        type: 'text' as const,
        text: `Analyze this order and provide recommendations:

${orderSummary}

Please provide:
1. Order efficiency analysis
2. Cross-sell opportunities
3. Customer retention suggestions
4. Fulfillment optimization tips`
      }
    }
  ];
}
Template-Based Prompts
Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class PromptTemplateService {
  private templates = new Map<string, (data: Record<string, unknown>) => string>();

  constructor() {
    this.registerDefaults();
  }

  private registerDefaults() {
    this.templates.set('email_draft', (data) => `
Draft a professional email:

To: ${data.recipient}
Subject: ${data.subject}
Context: ${data.context}
Tone: ${data.tone || 'professional'}

Requirements:
- Clear and concise
- Appropriate greeting and closing
- Action items if applicable`);

    this.templates.set('document_summary', (data) => `
Summarize the following document:

${data.content}

Summary Requirements:
- Maximum ${data.maxWords || 200} words
- Key points only
- Maintain original intent`);
  }

  render(templateName: string, data: Record<string, unknown>): string {
    const template = this.templates.get(templateName);
    if (!template) {
      throw new Error(`Template not found: ${templateName}`);
    }
    return template(data);
  }
}

export class CommunicationPrompts {
  constructor(private templateService: PromptTemplateService) {}

  @Prompt({
    name: 'compose_email',
    description: 'Draft a professional email',
    arguments: [
      { name: 'recipient', required: true, description: 'Email recipient' },
      { name: 'subject', required: true, description: 'Email subject' },
      { name: 'context', required: true, description: 'Context for the email' },
      { name: 'tone', required: false, description: 'Desired tone' }
    ]
  })
  async getEmailPrompt(
    args: { recipient: string; subject: string; context: string; tone?: string }
  ) {
    const text = this.templateService.render('email_draft', args);
    return [
      {
        role: 'user' as const,
        content: { type: 'text' as const, text }
      }
    ];
  }
}
Middleware Integration
Protected Prompts with Guards
Typescript

import { UseGuards } from '@nitrostack/core';
import { JWTGuard } from './guards/jwt.guard.js';

@Prompt({
  name: 'confidential_analysis',
  description: 'Generate analysis for confidential business data'
})
@UseGuards(JWTGuard)
async getConfidentialPrompt(args: { report_id: string }, ctx: ExecutionContext) {
  const userId = ctx.auth?.subject;
  ctx.logger.info('Confidential prompt accessed', { userId, reportId: args.report_id });

  const report = await this.reportService.getConfidential(args.report_id, userId);

  return [
    {
      role: 'user' as const,
      content: {
        type: 'text' as const,
        text: `Analyze this confidential report:\n\n${JSON.stringify(report, null, 2)}`
      }
    }
  ];
}
Dependency Injection
Injecting Services
Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class MetricsService {
  async getPerformanceMetrics(period: string): Promise<PerformanceMetrics> {
    // Load metrics from database
  }
}

@Injectable()
export class InsightService {
  async generateInsights(data: unknown): Promise<string[]> {
    // Generate AI-powered insights
  }
}

export class AnalyticsPrompts {
  constructor(
    private metricsService: MetricsService,
    private insightService: InsightService
  ) {}

  @Prompt({
    name: 'performance_review',
    description: 'Generate performance review analysis prompt',
    arguments: [
      { name: 'period', required: true, description: 'Review period' },
      { name: 'department', required: false, description: 'Department filter' }
    ]
  })
  async getPerformancePrompt(
    args: { period: string; department?: string },
    ctx: ExecutionContext
  ) {
    const metrics = await this.metricsService.getPerformanceMetrics(args.period);
    const preliminaryInsights = await this.insightService.generateInsights(metrics);

    return [
      {
        role: 'user' as const,
        content: {
          type: 'text' as const,
          text: `Review performance metrics for ${args.period}${args.department ? ` (${args.department})` : ''}:

Metrics:
${JSON.stringify(metrics, null, 2)}

Preliminary Insights:
${preliminaryInsights.map((insight, i) => `${i + 1}. ${insight}`).join('\n')}

Please provide:
1. Executive summary
2. Key achievements
3. Areas for improvement
4. Recommendations for next period`
        }
      }
    ];
  }
}
Dynamic Prompt Registration
NitroStack supports dynamic prompt registration at runtime, with automatic client notifications.

Adding Prompts Dynamically
Typescript

import { McpApplicationFactory } from '@nitrostack/core';

const app = await McpApplicationFactory.create(AppModule);
const server = app.getServer();

// After adding new prompts dynamically
server.notifyPromptsListChanged();
List Changed Notifications
When prompts are added or removed at runtime, the server sends a notifications/prompts/list_changed notification to all connected clients. This enables:

Dynamic content: Add prompts based on user context or preferences
A/B testing: Expose different prompts to different users
Plugin systems: Load prompts from external modules
Feature flags: Enable/disable prompts dynamically
Best Practices
1. Write Clear Descriptions
Typescript

// Recommended: Specific, actionable description
@Prompt({
  name: 'refactor_code',
  title: 'Code Refactoring Assistant',
  description: 'Generate refactoring suggestions with focus on clean code principles and design patterns'
})

// Avoid: Vague description
@Prompt({
  name: 'refactor_code',
  description: 'Refactor code'
})
2. Provide Structured Context
Typescript

// Recommended: Structured prompt with clear sections
return [{
  role: 'user' as const,
  content: {
    type: 'text' as const,
    text: `Task: Review and improve this API endpoint

Code:
\`\`\`typescript
${args.code}
\`\`\`

Review Criteria:
- Error handling completeness
- Input validation
- Security considerations
- Performance implications

Output Format:
- Issue description
- Severity (critical/warning/suggestion)
- Recommended fix
- Code example`
  }
}];

// Avoid: Unstructured prompt
return [{
  role: 'user' as const,
  content: {
    type: 'text' as const,
    text: `Review this: ${args.code}`
  }
}];
3. Validate Arguments Early
Typescript

@Prompt({ name: 'translate_document', description: 'Translate document content' })
async getTranslationPrompt(args: { text: string; target_language: string }) {
  // Validate early
  if (!args.text || args.text.trim().length === 0) {
    throw new Error('Text content is required for translation');
  }

  const supportedLanguages = ['en', 'es', 'fr', 'de', 'ja', 'zh'];
  if (!supportedLanguages.includes(args.target_language)) {
    throw new Error(
      `Unsupported language: ${args.target_language}. Supported: ${supportedLanguages.join(', ')}`
    );
  }

  // Proceed with validated input
  return [{
    role: 'user' as const,
    content: {
      type: 'text' as const,
      text: `Translate the following to ${args.target_language}:\n\n${args.text}`
    }
  }];
}
4. Use Consistent Naming
Typescript

// Recommended: snake_case, verb_noun or noun pattern
'generate_report'
'code_review'
'data_analysis'
'document_summary'

// Avoid: Inconsistent naming
'generateReport'    // camelCase
'Review'           // Single word, unclear
'do_stuff'         // Vague
5. Design for Reusability
Typescript

// Recommended: Parameterized, reusable prompts
@Prompt({
  name: 'document_review',
  arguments: [
    { name: 'document_type', required: true },
    { name: 'content', required: true },
    { name: 'review_focus', required: false }
  ]
})
async getDocumentReviewPrompt(args: DocumentReviewArgs) {
  // Works for contracts, proposals, reports, etc.
}

// Avoid: Overly specific prompts
@Prompt({ name: 'review_q1_2024_sales_report' })  // Too specific
Related Documentation
Tools Guide - Creating callable tools
Resources Guide - Exposing data resources
Middleware Guide - Request/response pipeline
Guards Guide - Access control
Dependency Injection - Service injection patterns
Events Guide - Event-driven architecture
Previous
📚 Resources
Next
🔧 Middleware
Middleware Guide
Overview
Middleware functions execute before and after tool, resource, and prompt handlers. They enable cross-cutting concerns such as logging, timing, authentication verification, request transformation, and error handling.

Middleware follows the "onion model" where each layer wraps around the next, with the handler at the center.

Table of Contents
Creating Middleware
Using Middleware
Execution Order
Common Patterns
Dependency Injection
Best Practices
Creating Middleware
Basic Middleware
Middleware implements the MiddlewareInterface:

Typescript

import { Middleware, MiddlewareInterface, ExecutionContext } from '@nitrostack/core';

@Middleware()
export class LoggingMiddleware implements MiddlewareInterface {
  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const startTime = Date.now();
    const toolName = context.toolName || 'unknown';

    context.logger.info(`Request started: ${toolName}`, {
      requestId: context.requestId,
      timestamp: new Date().toISOString()
    });

    try {
      // Execute next middleware or handler
      const result = await next();

      const duration = Date.now() - startTime;
      context.logger.info(`Request completed: ${toolName}`, {
        requestId: context.requestId,
        duration,
        success: true
      });

      return result;
    } catch (error) {
      const duration = Date.now() - startTime;
      context.logger.error(`Request failed: ${toolName}`, {
        requestId: context.requestId,
        duration,
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  }
}
Middleware Interface
Typescript

interface MiddlewareInterface {
  use(context: ExecutionContext, next: () => Promise<any>): Promise<any>;
}
Parameters:

context: The execution context with auth, logger, and metadata
next: Function to call the next middleware or handler
Return: The result from the handler (possibly transformed)

Using Middleware
On Individual Methods
Typescript

import { ToolDecorator as Tool, UseMiddleware } from '@nitrostack/core';
import { LoggingMiddleware } from './middleware/logging.middleware.js';

export class ProductTools {
  @Tool({ name: 'get_product' })
  @UseMiddleware(LoggingMiddleware)
  async getProduct(input: { productId: string }, ctx: ExecutionContext) {
    return this.productService.findById(input.productId);
  }
}
Multiple Middleware
Typescript

import { TimingMiddleware } from './middleware/timing.middleware.js';
import { ValidationMiddleware } from './middleware/validation.middleware.js';

@Tool({ name: 'create_order' })
@UseMiddleware(LoggingMiddleware, TimingMiddleware, ValidationMiddleware)
async createOrder(input: CreateOrderInput, ctx: ExecutionContext) {
  return this.orderService.create(input);
}
Execution Order
Middleware executes in declaration order, forming a pipeline:

Request
    │
    ▼
LoggingMiddleware (before)
    │
    ▼
TimingMiddleware (before)
    │
    ▼
ValidationMiddleware (before)
    │
    ▼
    Handler Execution
    │
    ▼
ValidationMiddleware (after)
    │
    ▼
TimingMiddleware (after)
    │
    ▼
LoggingMiddleware (after)
    │
    ▼
Response
Order Matters
Typescript

// Recommended order:
@UseMiddleware(
  RequestIdMiddleware,      // 1. Generate request ID first
  LoggingMiddleware,        // 2. Log with request ID
  AuthenticationMiddleware, // 3. Verify authentication
  ValidationMiddleware      // 4. Validate input
)
Common Patterns
Request ID Generation
Typescript

@Middleware()
export class RequestIdMiddleware implements MiddlewareInterface {
  private counter = 0;

  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 8);
    const sequence = (++this.counter).toString(36).padStart(4, '0');

    const requestId = `req_${timestamp}_${random}_${sequence}`;

    // Store in metadata for downstream use
    if (context.metadata) {
      context.metadata.requestId = requestId;
      context.metadata.requestTimestamp = new Date().toISOString();
    }

    return next();
  }
}
Performance Timing
Typescript

@Middleware()
export class TimingMiddleware implements MiddlewareInterface {
  private static readonly SLOW_THRESHOLD_MS = 1000;

  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const startTime = process.hrtime.bigint();

    try {
      const result = await next();

      this.recordTiming(context, startTime);
      return result;
    } catch (error) {
      this.recordTiming(context, startTime);
      throw error;
    }
  }

  private recordTiming(context: ExecutionContext, startTime: bigint): void {
    const endTime = process.hrtime.bigint();
    const durationMs = Number(endTime - startTime) / 1_000_000;

    if (context.metadata) {
      context.metadata.executionTimeMs = durationMs;
    }

    if (durationMs > TimingMiddleware.SLOW_THRESHOLD_MS) {
      context.logger.warn('Slow request detected', {
        toolName: context.toolName,
        duration: durationMs,
        threshold: TimingMiddleware.SLOW_THRESHOLD_MS
      });
    }
  }
}
Error Handling
Typescript

@Middleware()
export class ErrorHandlingMiddleware implements MiddlewareInterface {
  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    try {
      return await next();
    } catch (error) {
      // Log error with context
      context.logger.error('Request error', {
        toolName: context.toolName,
        requestId: context.metadata?.requestId,
        error: this.serializeError(error)
      });

      // Transform error for client
      if (error instanceof ValidationError) {
        return {
          error: true,
          code: 'VALIDATION_ERROR',
          message: error.message,
          details: error.details
        };
      }

      if (error instanceof NotFoundError) {
        return {
          error: true,
          code: 'NOT_FOUND',
          message: error.message
        };
      }

      // Unknown errors
      return {
        error: true,
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      };
    }
  }

  private serializeError(error: unknown): Record<string, unknown> {
    if (error instanceof Error) {
      return {
        name: error.name,
        message: error.message,
        stack: error.stack
      };
    }
    return { value: String(error) };
  }
}
Request Context Enrichment
Typescript

@Middleware()
export class ContextEnrichmentMiddleware implements MiddlewareInterface {
  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    if (context.metadata) {
      // Add environment information
      context.metadata.environment = process.env.NODE_ENV || 'development';
      context.metadata.serverVersion = process.env.APP_VERSION || '1.0.0';

      // Add user context if authenticated
      if (context.auth?.subject) {
        context.metadata.userId = context.auth.subject;
        context.metadata.userRoles = context.auth.roles || [];
      }
    }

    return next();
  }
}
Conditional Processing
Typescript

@Middleware()
export class ConditionalMiddleware implements MiddlewareInterface {
  private readonly skipTools = ['health_check', 'ping', 'version'];

  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    // Skip middleware for certain tools
    if (this.skipTools.includes(context.toolName || '')) {
      return next();
    }

    // Apply middleware logic only for non-skipped tools
    context.logger.info('Processing request', {
      toolName: context.toolName
    });

    return next();
  }
}
Metrics Collection
Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
@Middleware()
export class MetricsMiddleware implements MiddlewareInterface {
  private requestCounts = new Map<string, number>();
  private errorCounts = new Map<string, number>();
  private totalDuration = new Map<string, number>();

  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const toolName = context.toolName || 'unknown';
    const startTime = Date.now();

    // Increment request count
    this.requestCounts.set(toolName, (this.requestCounts.get(toolName) || 0) + 1);

    try {
      const result = await next();

      // Record duration
      const duration = Date.now() - startTime;
      this.totalDuration.set(toolName, (this.totalDuration.get(toolName) || 0) + duration);

      return result;
    } catch (error) {
      // Increment error count
      this.errorCounts.set(toolName, (this.errorCounts.get(toolName) || 0) + 1);
      throw error;
    }
  }

  getMetrics(): Record<string, unknown> {
    const tools: Record<string, unknown> = {};

    for (const [tool, count] of this.requestCounts) {
      tools[tool] = {
        requests: count,
        errors: this.errorCounts.get(tool) || 0,
        avgDuration: (this.totalDuration.get(tool) || 0) / count
      };
    }

    return { tools };
  }
}
Dependency Injection
Middleware can use dependency injection:

Typescript

import { Injectable, Middleware, MiddlewareInterface } from '@nitrostack/core';

@Injectable()
@Middleware()
export class AuditMiddleware implements MiddlewareInterface {
  constructor(
    private auditService: AuditService,
    private configService: ConfigService
  ) {}

  async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const shouldAudit = this.configService.get('ENABLE_AUDIT_LOG', true);

    if (!shouldAudit) {
      return next();
    }

    const startTime = Date.now();
    const auditEntry = {
      toolName: context.toolName,
      userId: context.auth?.subject,
      requestId: context.metadata?.requestId,
      timestamp: new Date().toISOString()
    };

    try {
      const result = await next();

      await this.auditService.log({
        ...auditEntry,
        status: 'success',
        duration: Date.now() - startTime
      });

      return result;
    } catch (error) {
      await this.auditService.log({
        ...auditEntry,
        status: 'error',
        duration: Date.now() - startTime,
        error: error instanceof Error ? error.message : String(error)
      });

      throw error;
    }
  }
}
Best Practices
1. Always Call next()
Middleware must call next() to continue the pipeline:

Typescript

// Correct: Always call next()
async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
  // Pre-processing
  const result = await next();  // Required
  // Post-processing
  return result;
}

// Incorrect: Missing next() call
async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
  return { error: 'Blocked' };  // Handler never executes
}
2. Handle Errors Properly
Always re-throw errors unless intentionally handling them:

Typescript

// Correct: Re-throw errors
async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
  try {
    return await next();
  } catch (error) {
    context.logger.error('Error occurred', { error });
    throw error;  // Re-throw for upstream handling
  }
}

// Incorrect: Swallowing errors
async use(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
  try {
    return await next();
  } catch (error) {
    return null;  // Error silently ignored
  }
}
3. Keep Middleware Focused
Each middleware should have a single responsibility:

Typescript

// Correct: Single responsibility
@Middleware()
export class LoggingMiddleware { /* Only logging */ }

@Middleware()
export class TimingMiddleware { /* Only timing */ }

@Middleware()
export class AuthMiddleware { /* Only auth */ }

// Incorrect: Multiple responsibilities
@Middleware()
export class EverythingMiddleware {
  async use(context, next) {
    // Logging
    // Timing
    // Auth
    // Validation
    // Caching
    // Too much!
  }
}
4. Use Dependency Injection
Inject services rather than creating instances:

Typescript

// Correct: Use DI
@Injectable()
@Middleware()
export class CacheMiddleware implements MiddlewareInterface {
  constructor(private cacheService: CacheService) {}
}

// Incorrect: Direct instantiation
@Middleware()
export class CacheMiddleware implements MiddlewareInterface {
  private cacheService = new CacheService();  // Untestable
}
5. Document Side Effects
Clearly document what the middleware modifies:

Typescript

/**
 * Timing Middleware
 *
 * Records execution timing in context.metadata.executionTimeMs
 * Logs warning if execution exceeds 1000ms threshold
 *
 * @modifies context.metadata.executionTimeMs
 */
@Middleware()
export class TimingMiddleware implements MiddlewareInterface {
  // Implementation
}
6. Order Middleware Thoughtfully
Place middleware in logical order:

Typescript

// Recommended order
@UseMiddleware(
  RequestIdMiddleware,      // First: Creates ID for tracing
  LoggingMiddleware,        // Second: Logs with request ID
  AuthenticationMiddleware, // Third: Verify credentials
  AuthorizationMiddleware,  // Fourth: Check permissions
  ValidationMiddleware,     // Fifth: Validate input
  CachingMiddleware         // Sixth: Check cache
)
Related Documentation
Interceptors Guide - Response transformation
Pipes Guide - Input validation
Error Handling - Exception filters
Best Practices - Architecture guidelines
Previous
💬 Prompts
Next
🎯 Interceptors
Interceptors Guide
Overview
Interceptors bind additional logic before and after handler execution. Unlike middleware, interceptors focus on transforming requests and responses, adding metadata, or implementing cross-cutting patterns like caching and response wrapping.

Table of Contents
Creating Interceptors
Using Interceptors
Common Patterns
Dependency Injection
Best Practices
Creating Interceptors
Basic Interceptor
Interceptors implement the InterceptorInterface:

Typescript

import { Interceptor, InterceptorInterface, ExecutionContext } from '@nitrostack/core';

@Interceptor()
export class ResponseWrapperInterceptor implements InterceptorInterface {
  async intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const startTime = Date.now();

    // Execute handler
    const result = await next();

    // Transform response
    return {
      success: true,
      data: result,
      metadata: {
        tool: context.toolName,
        requestId: context.metadata?.requestId || context.requestId,
        timestamp: new Date().toISOString(),
        duration: Date.now() - startTime
      }
    };
  }
}
Interceptor Interface
Typescript

interface InterceptorInterface {
  intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any>;
}
Parameters:

context: Execution context with auth, logger, and metadata
next: Function to call the handler
Return: Transformed response

Using Interceptors
On Individual Methods
Typescript

import { ToolDecorator as Tool, UseInterceptors } from '@nitrostack/core';
import { ResponseWrapperInterceptor } from './interceptors/response-wrapper.interceptor.js';

export class ProductTools {
  @Tool({ name: 'get_product' })
  @UseInterceptors(ResponseWrapperInterceptor)
  async getProduct(input: { productId: string }, ctx: ExecutionContext) {
    return this.productService.findById(input.productId);
    // Returns: { success: true, data: {...product}, metadata: {...} }
  }
}
Multiple Interceptors
Typescript

@Tool({ name: 'get_user' })
@UseInterceptors(
  ResponseWrapperInterceptor,
  DataMaskingInterceptor,
  CacheInterceptor
)
async getUser(input: { userId: string }, ctx: ExecutionContext) {
  return this.userService.findById(input.userId);
}
Common Patterns
Response Transformation
Typescript

@Interceptor()
export class TransformInterceptor implements InterceptorInterface {
  async intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const result = await next();
    return this.transformKeys(result);
  }

  private transformKeys(data: unknown): unknown {
    if (data === null || data === undefined) return data;

    if (Array.isArray(data)) {
      return data.map(item => this.transformKeys(item));
    }

    if (typeof data === 'object' && !(data instanceof Date)) {
      const transformed: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(data)) {
        // Convert snake_case to camelCase
        const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
        transformed[camelKey] = this.transformKeys(value);
      }
      return transformed;
    }

    return data;
  }
}
Sensitive Data Masking
Typescript

@Interceptor()
export class DataMaskingInterceptor implements InterceptorInterface {
  private static readonly SENSITIVE_FIELDS = [
    'password',
    'ssn',
    'socialSecurityNumber',
    'creditCard',
    'cardNumber',
    'cvv',
    'apiKey',
    'secretKey',
    'accessToken'
  ];

  async intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const result = await next();
    return this.maskSensitiveData(result);
  }

  private maskSensitiveData(data: unknown): unknown {
    if (data === null || data === undefined) return data;

    if (Array.isArray(data)) {
      return data.map(item => this.maskSensitiveData(item));
    }

    if (typeof data === 'object' && !(data instanceof Date)) {
      const masked: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(data)) {
        if (this.isSensitiveField(key)) {
          masked[key] = this.maskValue(key, value);
        } else {
          masked[key] = this.maskSensitiveData(value);
        }
      }
      return masked;
    }

    return data;
  }

  private isSensitiveField(field: string): boolean {
    const lowerField = field.toLowerCase();
    return DataMaskingInterceptor.SENSITIVE_FIELDS.some(
      sensitive => lowerField.includes(sensitive.toLowerCase())
    );
  }

  private maskValue(field: string, value: unknown): string {
    if (!value) return '***';
    const str = String(value);

    if (field.toLowerCase().includes('ssn')) {
      return `***-**-${str.slice(-4)}`;
    }

    if (field.toLowerCase().includes('card') || field.toLowerCase().includes('credit')) {
      return `****-****-****-${str.slice(-4)}`;
    }

    if (field.toLowerCase().includes('key') || field.toLowerCase().includes('token')) {
      if (str.length > 8) {
        return `${str.slice(0, 4)}...${str.slice(-4)}`;
      }
    }

    return '********';
  }
}
Response Caching
Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
@Interceptor()
export class CacheInterceptor implements InterceptorInterface {
  private cache = new Map<string, { data: unknown; expiresAt: number }>();

  async intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const cacheKey = this.generateCacheKey(context);

    // Check cache
    const cached = this.cache.get(cacheKey);
    if (cached && cached.expiresAt > Date.now()) {
      context.logger.info('Cache hit', { key: cacheKey });
      return cached.data;
    }

    // Execute handler
    const result = await next();

    // Store in cache (5 minute TTL)
    this.cache.set(cacheKey, {
      data: result,
      expiresAt: Date.now() + 5 * 60 * 1000
    });

    return result;
  }

  private generateCacheKey(context: ExecutionContext): string {
    const toolName = context.toolName || 'unknown';
    const input = JSON.stringify(context.metadata?.input || {});
    return `${toolName}:${input}`;
  }
}
Error Response Formatting
Typescript

@Interceptor()
export class ErrorFormatInterceptor implements InterceptorInterface {
  async intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    try {
      return await next();
    } catch (error) {
      return {
        success: false,
        error: {
          code: this.getErrorCode(error),
          message: error instanceof Error ? error.message : 'An error occurred',
          timestamp: new Date().toISOString(),
          requestId: context.metadata?.requestId
        }
      };
    }
  }

  private getErrorCode(error: unknown): string {
    if (error instanceof ValidationError) return 'VALIDATION_ERROR';
    if (error instanceof NotFoundError) return 'NOT_FOUND';
    if (error instanceof UnauthorizedError) return 'UNAUTHORIZED';
    return 'INTERNAL_ERROR';
  }
}
Pagination Wrapper
Typescript

@Interceptor()
export class PaginationInterceptor implements InterceptorInterface {
  async intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const result = await next();

    // Check if result is paginated data
    if (Array.isArray(result) && context.metadata?.input) {
      const input = context.metadata.input as {
        page?: number;
        limit?: number;
        total?: number;
      };

      const page = input.page || 1;
      const limit = input.limit || 20;

      return {
        data: result,
        pagination: {
          page,
          limit,
          total: input.total || result.length,
          hasMore: result.length === limit
        }
      };
    }

    return result;
  }
}
Dependency Injection
Interceptors support dependency injection:

Typescript

import { Injectable, Interceptor, InterceptorInterface } from '@nitrostack/core';

@Injectable()
@Interceptor()
export class AuditInterceptor implements InterceptorInterface {
  constructor(
    private auditService: AuditService,
    private configService: ConfigService
  ) {}

  async intercept(context: ExecutionContext, next: () => Promise<any>): Promise<any> {
    const startTime = Date.now();
    const shouldAudit = this.configService.get('ENABLE_AUDIT', true);

    const result = await next();

    if (shouldAudit) {
      await this.auditService.record({
        action: context.toolName,
        userId: context.auth?.subject,
        duration: Date.now() - startTime,
        timestamp: new Date()
      });
    }

    return result;
  }
}
Best Practices
1. Do Not Mutate Original Data
Return new objects instead of modifying the original:

Typescript

// Correct: Return new object
async intercept(context, next) {
  const result = await next();
  return {
    ...result,
    transformed: true
  };
}

// Incorrect: Mutating original
async intercept(context, next) {
  const result = await next();
  result.transformed = true;  // Mutation
  return result;
}
2. Handle Errors Gracefully
Decide whether to catch errors or let them propagate:

Typescript

// Transform errors
async intercept(context, next) {
  try {
    return await next();
  } catch (error) {
    return { error: true, message: error.message };
  }
}

// Or propagate with logging
async intercept(context, next) {
  try {
    return await next();
  } catch (error) {
    context.logger.error('Interceptor caught error', { error });
    throw error;  // Re-throw for upstream handling
  }
}
3. Keep Interceptors Focused
Each interceptor should have a single transformation purpose:

Typescript

// Correct: Focused interceptors
@Interceptor()
export class ResponseWrapperInterceptor { /* Wraps responses */ }

@Interceptor()
export class DataMaskingInterceptor { /* Masks sensitive data */ }

// Incorrect: Combined responsibilities
@Interceptor()
export class DoEverythingInterceptor {
  async intercept(context, next) {
    // Wrapping + masking + caching + logging
  }
}
4. Document Transformations
Clearly document what the interceptor modifies:

Typescript

/**
 * Response Wrapper Interceptor
 *
 * Transforms handler output into standardized response format:
 * {
 *   success: boolean,
 *   data: T,
 *   metadata: { tool, requestId, timestamp, duration }
 * }
 */
@Interceptor()
export class ResponseWrapperInterceptor implements InterceptorInterface {
  // Implementation
}
Related Documentation
Middleware Guide - Request/response pipeline
Pipes Guide - Input validation
Error Handling - Exception filters
Previous
🔧 Middleware
Next
🔐 Authentication
Dependency Injection Guide
Overview
NitroStack implements a dependency injection (DI) container that manages class instantiation and dependency resolution. This approach promotes loose coupling, improves testability, and enables modular application architecture.

Table of Contents
Core Concepts
Injectable Decorator
Constructor Injection
Module Providers
Service Lifecycle
Advanced Patterns
Testing with DI
Best Practices
Core Concepts
Dependency injection in NitroStack follows three principles:

Inversion of Control: Classes declare dependencies rather than creating them
Dependency Resolution: The container resolves and injects dependencies automatically
Singleton Scope: Services are instantiated once and shared across the application
Injectable Decorator
The @Injectable() decorator marks a class for dependency injection:

Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class UserService {
  constructor(
    private db: DatabaseService,
    private cache: CacheService
  ) {}

  async findById(id: string): Promise<User | null> {
    // Check cache first
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return cached;

    // Query database
    const user = await this.db.query('SELECT * FROM users WHERE id = $1', [id]);

    // Cache result
    if (user) {
      await this.cache.set(`user:${id}`, user, 300);
    }

    return user;
  }

  async create(data: CreateUserDto): Promise<User> {
    const user = await this.db.query(
      'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *',
      [data.email, data.name]
    );
    return user;
  }
}
Constructor Injection
Dependencies are injected through constructor parameters. The DI container analyzes parameter types and resolves them automatically:

Typescript

import { Injectable, ToolDecorator as Tool, ExecutionContext } from '@nitrostack/core';

@Injectable()
export class EmailService {
  constructor(private config: ConfigService) {}

  async send(to: string, subject: string, body: string): Promise<void> {
    const apiKey = this.config.get('EMAIL_API_KEY');
    // Send email implementation
  }
}

@Injectable()
export class NotificationService {
  constructor(
    private emailService: EmailService,
    private smsService: SmsService,
    private pushService: PushNotificationService
  ) {}

  async notifyUser(userId: string, message: string, channels: string[]): Promise<void> {
    const tasks = channels.map(channel => {
      switch (channel) {
        case 'email': return this.emailService.send(userId, 'Notification', message);
        case 'sms': return this.smsService.send(userId, message);
        case 'push': return this.pushService.send(userId, message);
        default: throw new Error(`Unknown channel: ${channel}`);
      }
    });

    await Promise.all(tasks);
  }
}

export class NotificationTools {
  constructor(private notificationService: NotificationService) {}

  @Tool({
    name: 'send_notification',
    description: 'Send a notification to a user through specified channels'
  })
  async sendNotification(
    input: { userId: string; message: string; channels: string[] },
    ctx: ExecutionContext
  ) {
    await this.notificationService.notifyUser(
      input.userId,
      input.message,
      input.channels
    );
    return { success: true };
  }
}
Module Providers
Providers are registered in module definitions:

Typescript

import { Module } from '@nitrostack/core';

@Module({
  name: 'users',
  controllers: [UserTools, UserResources],
  providers: [
    UserService,
    UserRepository,
    EmailService,
    ValidationService
  ],
  exports: [UserService]  // Make available to importing modules
})
export class UsersModule {}
Provider Registration
Typescript

// Standard provider (class reference)
providers: [UserService]

// The container will:
// 1. Analyze UserService constructor
// 2. Resolve all constructor parameters
// 3. Create a singleton instance
// 4. Inject into dependent classes
Exporting Providers
Export providers to make them available to other modules:

Typescript

@Module({
  name: 'database',
  providers: [DatabaseService, ConnectionPool, QueryBuilder],
  exports: [DatabaseService]  // Only DatabaseService is public
})
export class DatabaseModule {}

@Module({
  name: 'users',
  imports: [DatabaseModule],  // Import to use DatabaseService
  providers: [UserService],
  controllers: [UserTools]
})
export class UsersModule {}
Global Modules
Global modules make providers available everywhere without explicit imports:

Typescript

@Module({
  name: 'core',
  providers: [Logger, ConfigService, CacheService],
  exports: [Logger, ConfigService, CacheService],
  global: true  // Available to all modules
})
export class CoreModule {}
Service Lifecycle
Singleton Scope (Default)
By default, all services are singletons. One instance is created and shared:

Typescript

@Injectable()
export class DatabaseConnectionPool {
  private connections: Connection[] = [];

  constructor() {
    // Called once at application startup
    this.initializePool();
  }

  private initializePool(): void {
    // Create connection pool
  }

  async getConnection(): Promise<Connection> {
    // Return available connection
  }
}
Initialization Order
Services are initialized in dependency order:

Typescript

// 1. ConfigService (no dependencies)
@Injectable()
export class ConfigService {
  constructor() {
    // Initialized first
  }
}

// 2. DatabaseService (depends on ConfigService)
@Injectable()
export class DatabaseService {
  constructor(private config: ConfigService) {
    // Initialized second
  }
}

// 3. UserService (depends on DatabaseService)
@Injectable()
export class UserService {
  constructor(private db: DatabaseService) {
    // Initialized third
  }
}
Advanced Patterns
Service Interfaces
Define interfaces for better abstraction:

Typescript

// interfaces/storage.interface.ts
export interface StorageService {
  get(key: string): Promise<string | null>;
  set(key: string, value: string, ttl?: number): Promise<void>;
  delete(key: string): Promise<void>;
}

// services/redis-storage.service.ts
@Injectable()
export class RedisStorageService implements StorageService {
  constructor(private redis: RedisClient) {}

  async get(key: string): Promise<string | null> {
    return this.redis.get(key);
  }

  async set(key: string, value: string, ttl?: number): Promise<void> {
    if (ttl) {
      await this.redis.setex(key, ttl, value);
    } else {
      await this.redis.set(key, value);
    }
  }

  async delete(key: string): Promise<void> {
    await this.redis.del(key);
  }
}
Factory Patterns
Create services with complex initialization:

Typescript

@Injectable()
export class DatabaseServiceFactory {
  constructor(private config: ConfigService) {}

  createConnection(database: string): DatabaseConnection {
    const baseConfig = {
      host: this.config.get('DB_HOST'),
      port: this.config.get('DB_PORT'),
      user: this.config.get('DB_USER'),
      password: this.config.get('DB_PASSWORD')
    };

    return new DatabaseConnection({
      ...baseConfig,
      database
    });
  }
}

@Injectable()
export class MultiTenantDatabaseService {
  private connections = new Map<string, DatabaseConnection>();

  constructor(private factory: DatabaseServiceFactory) {}

  getConnection(tenantId: string): DatabaseConnection {
    if (!this.connections.has(tenantId)) {
      const connection = this.factory.createConnection(`tenant_${tenantId}`);
      this.connections.set(tenantId, connection);
    }
    return this.connections.get(tenantId)!;
  }
}
Composite Services
Combine multiple services into a facade:

Typescript

@Injectable()
export class OrderFacadeService {
  constructor(
    private orderService: OrderService,
    private inventoryService: InventoryService,
    private paymentService: PaymentService,
    private notificationService: NotificationService,
    private auditService: AuditService
  ) {}

  async processOrder(order: CreateOrderDto, userId: string): Promise<Order> {
    // Start transaction
    const orderRecord = await this.orderService.create(order, userId);

    try {
      // Reserve inventory
      await this.inventoryService.reserve(order.items);

      // Process payment
      await this.paymentService.charge(userId, orderRecord.total);

      // Finalize order
      await this.orderService.confirm(orderRecord.id);

      // Send confirmation
      await this.notificationService.sendOrderConfirmation(userId, orderRecord);

      // Audit log
      await this.auditService.log('order.created', { orderId: orderRecord.id, userId });

      return orderRecord;
    } catch (error) {
      // Rollback on failure
      await this.orderService.cancel(orderRecord.id);
      await this.inventoryService.release(order.items);
      throw error;
    }
  }
}
Testing with DI
Mock Injection
Create mock implementations for testing:

Typescript

// tests/mocks/user.service.mock.ts
export class MockUserService {
  private users = new Map<string, User>();

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }

  async create(data: CreateUserDto): Promise<User> {
    const user = {
      id: `usr_${Date.now()}`,
      ...data,
      createdAt: new Date()
    };
    this.users.set(user.id, user);
    return user;
  }

  // Helper for test setup
  seedUser(user: User): void {
    this.users.set(user.id, user);
  }

  clear(): void {
    this.users.clear();
  }
}
Test Setup
Typescript

// tests/user.tools.test.ts
import { createTestingModule } from '@nitrostack/core/testing';
import { UserTools } from '../src/user.tools.js';
import { MockUserService } from './mocks/user.service.mock.js';

describe('UserTools', () => {
  let tools: UserTools;
  let mockUserService: MockUserService;

  beforeEach(async () => {
    mockUserService = new MockUserService();

    const module = await createTestingModule({
      controllers: [UserTools],
      providers: [
        { provide: UserService, useValue: mockUserService }
      ]
    });

    tools = module.get(UserTools);
  });

  afterEach(() => {
    mockUserService.clear();
  });

  describe('get_user', () => {
    it('should return user when found', async () => {
      const testUser = {
        id: 'usr_123',
        email: 'test@example.com',
        name: 'Test User',
        createdAt: new Date()
      };
      mockUserService.seedUser(testUser);

      const result = await tools.getUser({ userId: 'usr_123' }, mockContext);

      expect(result).toEqual(testUser);
    });

    it('should throw error when user not found', async () => {
      await expect(
        tools.getUser({ userId: 'nonexistent' }, mockContext)
      ).rejects.toThrow('User not found');
    });
  });
});
Best Practices
1. Single Responsibility
Each service should have one clear purpose:

Typescript

// Recommended: Focused services
@Injectable()
export class UserValidationService {
  validateEmail(email: string): boolean { /* ... */ }
  validatePassword(password: string): ValidationResult { /* ... */ }
}

@Injectable()
export class UserAuthenticationService {
  async authenticate(email: string, password: string): Promise<AuthResult> { /* ... */ }
}

@Injectable()
export class UserProfileService {
  async getProfile(userId: string): Promise<UserProfile> { /* ... */ }
  async updateProfile(userId: string, data: UpdateProfileDto): Promise<UserProfile> { /* ... */ }
}

// Avoid: God service
@Injectable()
export class UserService {
  validateEmail() { /* ... */ }
  validatePassword() { /* ... */ }
  authenticate() { /* ... */ }
  getProfile() { /* ... */ }
  updateProfile() { /* ... */ }
  sendEmail() { /* ... */ }
  generateReport() { /* ... */ }
  // Too many responsibilities
}
2. Avoid Direct Instantiation
Let the DI container manage instances:

Typescript

// Recommended: Inject dependencies
@Injectable()
export class OrderService {
  constructor(private paymentService: PaymentService) {}

  async createOrder(data: OrderDto): Promise<Order> {
    await this.paymentService.charge(data.amount);
  }
}

// Avoid: Direct instantiation
@Injectable()
export class OrderService {
  private paymentService = new PaymentService();  // Bad!

  async createOrder(data: OrderDto): Promise<Order> {
    await this.paymentService.charge(data.amount);
  }
}
3. Program to Interfaces
Define clear contracts for services:

Typescript

// Recommended: Interface-based design
export interface PaymentProcessor {
  charge(amount: number, currency: string): Promise<PaymentResult>;
  refund(transactionId: string, amount: number): Promise<RefundResult>;
}

@Injectable()
export class StripePaymentService implements PaymentProcessor {
  async charge(amount: number, currency: string): Promise<PaymentResult> { /* ... */ }
  async refund(transactionId: string, amount: number): Promise<RefundResult> { /* ... */ }
}

// Easy to swap implementations
@Injectable()
export class PayPalPaymentService implements PaymentProcessor {
  async charge(amount: number, currency: string): Promise<PaymentResult> { /* ... */ }
  async refund(transactionId: string, amount: number): Promise<RefundResult> { /* ... */ }
}
4. Keep Services Stateless
Avoid mutable state in services:

Typescript

// Recommended: Stateless service
@Injectable()
export class PricingService {
  constructor(private config: ConfigService) {}

  calculatePrice(basePrice: number, quantity: number): number {
    const taxRate = this.config.get('TAX_RATE');
    return basePrice * quantity * (1 + taxRate);
  }
}

// Avoid: Stateful service
@Injectable()
export class PricingService {
  private lastCalculation: number = 0;  // Mutable state
  private cache: Map<string, number> = new Map();  // Be careful with caches

  calculatePrice(basePrice: number): number {
    this.lastCalculation = basePrice * 1.1;  // Side effect
    return this.lastCalculation;
  }
}
5. Explicit Dependencies
Declare all dependencies in the constructor:

Typescript

// Recommended: Explicit dependencies
@Injectable()
export class ReportService {
  constructor(
    private db: DatabaseService,
    private cache: CacheService,
    private logger: Logger
  ) {}
}

// Avoid: Hidden dependencies
@Injectable()
export class ReportService {
  generateReport(): Report {
    const db = getDatabaseInstance();  // Hidden dependency
    const data = db.query('...');
  }
}
Related Documentation
Server Concepts - Module architecture
Testing Guide - Testing with mocks
Best Practices - Architecture guidelines
Previous
🔐 Authentication
Next
🎨 UI Widgets
