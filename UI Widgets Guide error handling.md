UI Widgets Guide
Overview
Widgets are Next.js components that render visual UI for tool and resource responses. They provide rich, interactive displays for data returned by your MCP server. NitroStack provides a modern Widget SDK with React hooks for building powerful, theme-aware widgets.

Quick Start
1. Create a Widget
Typescript

// src/widgets/app/product-card/page.tsx
'use client';

import { useWidgetSDK } from '@nitrostack/widgets';

interface ProductData {
  id: string;
  name: string;
  price: number;
  image_url?: string;
}

export default function ProductCard() {
  const { isReady, getToolOutput } = useWidgetSDK();
  
  if (!isReady) {
    return <div>Loading...</div>;
  }
  
  const product = getToolOutput<ProductData>();
  
  return (
    <div style={{
      background: '#000',
      color: '#fff',
      padding: '24px',
      borderRadius: '12px'
    }}>
      {product.image_url && (
        <img src={product.image_url} alt={product.name} />
      )}
      <h2>{product.name}</h2>
      <p>${product.price.toFixed(2)}</p>
    </div>
  );
}
2. Connect to Tool
Typescript

import { Tool, Widget } from '@nitrostack/core';

@Tool({
  name: 'get_product',
  description: 'Get product details',
  inputSchema: z.object({
    product_id: z.string()
  }),
  // Invocation status messages (shown during tool execution)
  invocation: {
    invoking: 'Loading product...',
    invoked: 'Product loaded'
  },
  // Example data for widget preview
  examples: {
    request: { product_id: 'prod-123' },
    response: {
      id: 'prod-123',
      name: 'Awesome Product',
      price: 99.99,
      image_url: 'https://example.com/image.jpg'
    }
  }
})
@Widget('product-card')
async getProduct(input: any, ctx: ExecutionContext) {
  return {
    id: input.product_id,
    name: 'Awesome Product',
    price: 99.99,
    image_url: 'https://example.com/image.jpg'
  };
}
Important: The examples.response data is used by clients to render widget previews before the tool is executed. Always provide realistic example data that matches your response structure.

Platform Compatibility
NitroStack widgets are compatible with both OpenAI Apps SDK and MCP Apps specifications:

Platform	API	Ready Event
OpenAI Apps SDK	window.openai	openai:ready
MCP Apps	window.__MCP_APP_CONTEXT__	mcp:ready
The Widget SDK handles this automatically - your widgets work on both platforms without changes.

Typescript

const { isReady } = useWidgetSDK();

// isReady checks for BOTH platforms automatically
if (isReady) {
  // Widget works on OpenAI ChatGPT AND MCP Apps clients
}
Modern Widget SDK
useWidgetSDK Hook
The primary way to build widgets. Provides access to all SDK functionality.

Typescript

import { useWidgetSDK } from '@nitrostack/widgets';

export default function MyWidget() {
  const { 
    isReady,           // SDK initialization status
    getToolOutput,     // Get tool response data
    callTool,          // Call other tools
    requestFullscreen, // Display controls
    setState,          // State management
    getTheme          // Theme information
  } = useWidgetSDK();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  return <div>{data.content}</div>;
}
Theme-Aware Widgets
Use useTheme() to create widgets that adapt to light/dark mode.

Typescript

import { useWidgetSDK, useTheme } from '@nitrostack/widgets';

export default function ThemedWidget() {
  const { isReady, getToolOutput } = useWidgetSDK();
  const theme = useTheme();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  const styles = {
    background: theme === 'dark' ? '#1a1a1a' : '#ffffff',
    color: theme === 'dark' ? '#ffffff' : '#000000',
    border: `1px solid ${theme === 'dark' ? '#333' : '#ddd'}`
  };
  
  return (
    <div style={styles}>
      <h2>{data.title}</h2>
      <p>{data.description}</p>
    </div>
  );
}
Responsive Widgets
Use useDisplayMode() to adapt to different display modes.

Typescript

import { useWidgetSDK, useDisplayMode } from '@nitrostack/widgets';

export default function ResponsiveWidget() {
  const { isReady, getToolOutput } = useWidgetSDK();
  const displayMode = useDisplayMode();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  const padding = displayMode === 'fullscreen' ? '48px' : '16px';
  const fontSize = displayMode === 'fullscreen' ? '24px' : '16px';
  
  return (
    <div style={{ padding, fontSize }}>
      <h1>{data.title}</h1>
      {displayMode === 'fullscreen' && (
        <div>Additional details shown in fullscreen</div>
      )}
    </div>
  );
}
Interactive Widgets
Calling Tools from Widgets
Typescript

import { useWidgetSDK } from '@nitrostack/widgets';

export default function InteractiveWidget() {
  const { isReady, getToolOutput, callTool, sendFollowUpMessage } = useWidgetSDK();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  const handleAction = async () => {
    const result = await callTool('process_item', { id: data.id });
    console.log('Result:', result);
  };
  
  const askQuestion = async () => {
    await sendFollowUpMessage('Tell me more about this item');
  };
  
  return (
    <div>
      <h2>{data.title}</h2>
      <button onClick={handleAction}>Process</button>
      <button onClick={askQuestion}>Learn More</button>
    </div>
  );
}
State Management
Use useWidgetState() for persistent widget state.

Typescript

import { useWidgetSDK, useWidgetState } from '@nitrostack/widgets';

interface FormState {
  name: string;
  email: string;
}

export default function StatefulWidget() {
  const { isReady, getToolOutput } = useWidgetSDK();
  const { state, setState } = useWidgetState<FormState>();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  const updateName = async (name: string) => {
    await setState({ ...state, name });
  };
  
  return (
    <div>
      <input 
        value={state?.name || ''} 
        onChange={(e) => updateName(e.target.value)}
        placeholder="Name"
      />
      <p>Current name: {state?.name}</p>
    </div>
  );
}
Display Controls
Typescript

import { useWidgetSDK } from '@nitrostack/widgets';

export default function ControlsWidget() {
  const { 
    isReady, 
    getToolOutput, 
    requestFullscreen, 
    requestInline,
    requestClose 
  } = useWidgetSDK();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  return (
    <div>
      <h2>{data.title}</h2>
      <button onClick={requestFullscreen}>Fullscreen</button>
      <button onClick={requestInline}>Inline</button>
      <button onClick={requestClose}>Close</button>
    </div>
  );
}
Complex Examples
Product Grid
Typescript

import { useWidgetSDK, useTheme } from '@nitrostack/widgets';

interface Product {
  id: string;
  name: string;
  price: number;
  image_url: string;
}

interface ProductGridData {
  products: Product[];
  pagination: {
    page: number;
    totalPages: number;
  };
}

export default function ProductsGrid() {
  const { isReady, getToolOutput } = useWidgetSDK();
  const theme = useTheme();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput<ProductGridData>();
  
  const containerStyle = {
    background: theme === 'dark' ? '#000' : '#fff',
    color: theme === 'dark' ? '#fff' : '#000',
    padding: '24px',
    borderRadius: '12px'
  };
  
  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '16px',
    marginTop: '16px'
  };
  
  const cardStyle = {
    background: theme === 'dark' ? '#1a1a1a' : '#f5f5f5',
    borderRadius: '8px',
    padding: '16px',
    border: `1px solid ${theme === 'dark' ? '#333' : '#ddd'}`
  };
  
  return (
    <div style={containerStyle}>
      <h2>Products (Page {data.pagination.page} of {data.pagination.totalPages})</h2>
      
      <div style={gridStyle}>
        {data.products.map((product) => (
          <div key={product.id} style={cardStyle}>
            <img
              src={product.image_url}
              alt={product.name}
              style={{
                width: '100%',
                height: '150px',
                objectFit: 'cover',
                borderRadius: '4px',
                marginBottom: '12px'
              }}
            />
            <h3 style={{ fontSize: '16px', marginBottom: '8px' }}>
              {product.name}
            </h3>
            <p style={{ fontSize: '20px', fontWeight: 'bold' }}>
              ${product.price.toFixed(2)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
Dashboard Widget
Typescript

import { useWidgetSDK, useTheme, useDisplayMode } from '@nitrostack/widgets';

interface DashboardData {
  user: {
    name: string;
    email: string;
    avatar?: string;
  };
  stats: {
    orders: number;
    spent: number;
    points: number;
  };
  recentOrders: Array<{
    id: string;
    total: number;
    date: string;
  }>;
}

export default function UserDashboard() {
  const { isReady, getToolOutput } = useWidgetSDK();
  const theme = useTheme();
  const displayMode = useDisplayMode();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput<DashboardData>();
  
  const isFullscreen = displayMode === 'fullscreen';
  
  const containerStyle = {
    background: theme === 'dark' ? '#000' : '#fff',
    color: theme === 'dark' ? '#fff' : '#000',
    padding: isFullscreen ? '48px' : '24px',
    borderRadius: '12px',
    maxWidth: isFullscreen ? '1200px' : '800px'
  };
  
  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '24px' }}>
        {data.user.avatar && (
          <img
            src={data.user.avatar}
            alt={data.user.name}
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              marginRight: '16px'
            }}
          />
        )}
        <div>
          <h2 style={{ marginBottom: '4px' }}>{data.user.name}</h2>
          <p style={{ color: theme === 'dark' ? '#999' : '#666' }}>
            {data.user.email}
          </p>
        </div>
      </div>
      
      {/* Stats */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '16px',
        marginBottom: '24px'
      }}>
        <StatCard label="Orders" value={data.stats.orders} theme={theme} />
        <StatCard label="Total Spent" value={`$${data.stats.spent}`} theme={theme} />
        <StatCard label="Points" value={data.stats.points} theme={theme} />
      </div>
      
      {/* Recent Orders */}
      <h3 style={{ marginBottom: '16px' }}>Recent Orders</h3>
      {data.recentOrders.map((order) => (
        <div
          key={order.id}
          style={{
            background: theme === 'dark' ? '#1a1a1a' : '#f5f5f5',
            padding: '16px',
            borderRadius: '8px',
            marginBottom: '12px',
            display: 'flex',
            justifyContent: 'space-between'
          }}
        >
          <span>Order #{order.id}</span>
          <span>${order.total.toFixed(2)}</span>
          <span style={{ color: theme === 'dark' ? '#999' : '#666' }}>
            {order.date}
          </span>
        </div>
      ))}
    </div>
  );
}

function StatCard({ label, value, theme }: { 
  label: string; 
  value: string | number;
  theme: 'light' | 'dark' | null;
}) {
  return (
    <div style={{
      background: theme === 'dark' ? '#1a1a1a' : '#f5f5f5',
      padding: '20px',
      borderRadius: '8px',
      textAlign: 'center'
    }}>
      <div style={{ fontSize: '28px', fontWeight: 'bold' }}>
        {value}
      </div>
      <div style={{ 
        color: theme === 'dark' ? '#999' : '#666', 
        marginTop: '8px' 
      }}>
        {label}
      </div>
    </div>
  );
}
Styling Widgets
Inline Styles (Recommended)
Use inline styles for widgets to ensure they work in iframes:

Typescript

const styles = {
  container: {
    background: '#000',
    color: '#fff',
    padding: '24px',
    borderRadius: '12px',
    fontFamily: 'system-ui, sans-serif'
  },
  heading: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '16px'
  },
  button: {
    background: '#007bff',
    color: '#fff',
    padding: '12px 24px',
    borderRadius: '8px',
    border: 'none',
    fontWeight: 'bold',
    cursor: 'pointer'
  }
};

export default function StyledWidget() {
  const { isReady, getToolOutput } = useWidgetSDK();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>{data.title}</h2>
      <button style={styles.button}>Click me</button>
    </div>
  );
}
Why Not Tailwind?
Tailwind CSS classes may not work in iframes due to CSS scope issues. Use inline styles for widgets.

Utility Functions
Device Detection
Typescript

import { 
  isPrimarilyTouchDevice, 
  isHoverAvailable,
  prefersReducedMotion 
} from '@nitrostack/widgets';

export default function AdaptiveWidget() {
  const { isReady, getToolOutput } = useWidgetSDK();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  const buttonSize = isPrimarilyTouchDevice() ? '48px' : '32px';
  const showHoverEffects = isHoverAvailable();
  const animate = !prefersReducedMotion();
  
  return (
    <button style={{ 
      height: buttonSize,
      transition: animate ? 'all 0.3s' : 'none'
    }}>
      {data.label}
    </button>
  );
}
Best Practices
1. Always Check isReady
Typescript

const { isReady } = useWidgetSDK();

if (!isReady) {
  return <div>Loading...</div>;
}
2. Use TypeScript
Typescript

interface ProductData {
  id: string;
  name: string;
  price: number;
}

const product = getToolOutput<ProductData>();
// TypeScript knows the shape of product
3. Handle Missing Data
Typescript

const data = getToolOutput();

if (!data) {
  return <div>No data available</div>;
}

// Safe to use data
return <div>{data.title}</div>;
4. Use Theme for Better UX
Typescript

const theme = useTheme();

const styles = {
  background: theme === 'dark' ? '#000' : '#fff',
  color: theme === 'dark' ? '#fff' : '#000'
};
5. Provide Example Data and Invocation Messages
Typescript

@Tool({
  name: 'get_product',
  description: 'Get product details',
  inputSchema: z.object({ product_id: z.string() }),
  // Status messages shown during execution
  invocation: {
    invoking: 'Loading product...',  // Shown while running
    invoked: 'Product loaded'        // Shown when complete
  },
  // Example data for widget preview (REQUIRED for widget preview)
  examples: {
    request: { product_id: 'prod-123' },
    response: { 
      id: 'prod-123', 
      name: 'Product', 
      price: 99.99,
      image_url: 'https://example.com/img.jpg'
    }
  }
})
@Widget('product-card')
Note: Without examples.response, the widget preview won't render in the client.

Debugging Widgets
Test Locally
Bash

cd src/widgets
npm run dev  # Runs on port 3001
Visit: http://localhost:3001/product-card?data={"id":"1","name":"Test"}

Check Studio
Bash

nitrostack-cli dev  # Studio on port 3000
Navigate to Tools page
Click "Enlarge" on a tool with a widget
Check browser console for errors
Legacy Patterns
withToolData HOC
Note: This is the legacy pattern. New widgets should use useWidgetSDK() instead.

Typescript

import { withToolData } from '@nitrostack/widgets';

function ProductCard({ data }) {
  return (
    <div>
      <h2>{data.name}</h2>
      <p>${data.price}</p>
    </div>
  );
}

export default withToolData(ProductCard);
For migration from withToolData to useWidgetSDK, see the Widget SDK Migration Guide.

Next Steps
Widget SDK Reference - Complete API documentation
Widget SDK Migration Guide - Migrate from withToolData
Tools Guide - Connect widgets to tools
Widget Examples Guide - Advanced examples
See Also
Type Generation
Studio Guide
Testing Guide
Previous
💉 Dependency Injection
Next
📋 Widget Manifest
Widget Manifest & UI Testing
Learn how to use the Widget Manifest system for independent frontend development and UI testing without needing a running backend.

📋 Table of Contents
Overview
What is a Widget Manifest?
Why Use Widget Manifests?
Manifest Structure
Creating a Widget Manifest
Viewing Widgets in Studio
Example Workflow
Best Practices
Troubleshooting
Overview
The Widget Manifest system enables independent frontend development by providing example data for UI widgets. Frontend developers can preview and test widgets in Studio's Resources tab without needing a live backend or tool execution.

What is a Widget Manifest?
A Widget Manifest is a JSON file (widget-manifest.json) that:

Lists all UI widgets in your project
Provides example data for each widget
Includes metadata like names, descriptions, and tags
Enables live previews in NitroStack Studio
It's located at: src/widgets/widget-manifest.json

Why Use Widget Manifests?
For Frontend Developers
Work Independently - Develop UI without waiting for backend
Instant Previews - See widgets render with realistic data
Multiple Examples - Test different UI states
No API Needed - Preview without running the MCP server

For Teams
Parallel Development - Frontend and backend teams work simultaneously
Better Communication - Shared understanding of data structures
Faster Iteration - Quick UI feedback loop
Documentation - Self-documenting widget examples

Manifest Structure
Basic Format
JSON

{
  "version": "1.0.0",
  "widgets": [
    {
      "uri": "/widget-name",
      "name": "Display Name",
      "description": "What this widget does",
      "examples": [
        {
          "name": "Example Name",
          "description": "Example description",
          "data": {
            "field1": "value1",
            "field2": "value2"
          }
        }
      ],
      "tags": ["category", "type"]
    }
  ],
  "generatedAt": "2025-01-24T00:00:00.000Z"
}
Field Descriptions
Field	Type	Required	Description
version	string	Yes	Manifest version (e.g., "1.0.0")
widgets	array	Yes	Array of widget definitions
generatedAt	string	No	ISO timestamp of generation
Widget Definition
Field	Type	Required	Description
uri	string	Yes	Widget route (e.g., "/product-card")
name	string	Yes	Display name for Studio
description	string	Yes	What the widget displays
examples	array	Yes	Array of example data objects
tags	array	No	Categorization tags
Example Object
Field	Type	Required	Description
name	string	Yes	Example name (shown in dropdown)
description	string	No	Example description
data	object	Yes	The actual data passed to widget
Creating a Widget Manifest
Step 1: Extract Tool Examples
Look at your tool definitions and extract the example responses:

Typescript

// auth.tools.ts
@Tool({
  name: 'login',
  examples: {
    request: { email: 'user@example.com', password: 'pass123' },
    response: {
      message: 'Login successful!',
      token: 'jwt_token_here',
      user: {
        id: 'user-1',
        email: 'user@example.com',
        name: 'John Doe'
      }
    }
  }
})
@Widget('login-result')
async login(input: any) { ... }
Step 2: Create Widget Entry
Use the response from examples as the data field:

JSON

{
  "uri": "/login-result",
  "name": "Login Result",
  "description": "Displays login success with user info and JWT token",
  "examples": [
    {
      "name": "Successful Login",
      "description": "Login for John Doe",
      "data": {
        "message": "Login successful!",
        "token": "jwt_token_here",
        "user": {
          "id": "user-1",
          "email": "user@example.com",
          "name": "John Doe"
        }
      }
    }
  ],
  "tags": ["auth", "login"]
}
Step 3: Add Multiple Examples (Optional)
Provide different UI states:

JSON

{
  "uri": "/product-card",
  "name": "Product Card",
  "description": "Displays product details",
  "examples": [
    {
      "name": "In Stock Product",
      "description": "Product with high stock",
      "data": {
        "product": { "name": "Laptop", "price": 999, "stock": 50 },
        "availability": "In Stock"
      }
    },
    {
      "name": "Low Stock Product",
      "description": "Product with low stock",
      "data": {
        "product": { "name": "Laptop", "price": 999, "stock": 2 },
        "availability": "In Stock",
        "stockMessage": "Only 2 left!"
      }
    },
    {
      "name": "Out of Stock",
      "description": "Unavailable product",
      "data": {
        "product": { "name": "Laptop", "price": 999, "stock": 0 },
        "availability": "Out of Stock"
      }
    }
  ],
  "tags": ["products", "details"]
}
Step 4: Save the Manifest
Place the file at: src/widgets/widget-manifest.json

Viewing Widgets in Studio
Accessing UI Widgets
Start your project:

Bash

npm run dev
Open Studio: http://localhost:3000

Navigate to Resources tab

See "UI Widgets" section at the top

UI Widgets Section Features
┌─────────────────────────────────────┐
│ 🎨 UI Widgets (16)                  │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 🔐 Login Result                 │ │
│ │ 1 example                       │ │
│ ├─────────────────────────────────┤ │
│ │ Displays login success...       │ │
│ │ /login-result                   │ │
│ │ #auth #login                    │ │ ← Tags
│ ├─────────────────────────────────┤ │
│ │ ┌─────────────────────────────┐ │ │
│ │ │ ✨ Successful Login          │ │ │ ← Example Name
│ │ │                             │ │ │
│ │ │  [Widget Preview]           │ │ │ ← Live Preview
│ │ │                             │ │ │
│ │ └─────────────────────────────┘ │ │
│ ├─────────────────────────────────┤ │
│ │ [Select Example ▼]              │ │ ← Example Selector
│ │ [⛶ Enlarge]                     │ │ ← Enlarge Button
│ └─────────────────────────────────┘ │
│                                     │
│ ... (more widgets)                  │
│                                     │
└─────────────────────────────────────┘
Interactive Features
Example Selector: Switch between different examples
Live Preview: Widget renders with selected example data
Enlarge Button: Open full-screen modal view
Search: Filter widgets by name or description
Example Workflow
Scenario: Adding a New Widget
Let's add a "User Profile" widget to an e-commerce app.

1. Create the Widget Component
TSX

// src/widgets/app/user-profile/page.tsx
'use client';

export default function UserProfile({ data }: { data: any }) {
  return (
    <div className="p-6 bg-white rounded-lg">
      <img 
        src={data.user.avatar} 
        alt={data.user.name}
        className="w-24 h-24 rounded-full"
      />
      <h2 className="text-2xl font-bold mt-4">{data.user.name}</h2>
      <p className="text-gray-600">{data.user.email}</p>
      <div className="mt-4">
        <p>Member since: {data.user.memberSince}</p>
        <p>Orders: {data.stats.totalOrders}</p>
      </div>
    </div>
  );
}
2. Define the Tool with Example
Typescript

// src/modules/users/users.tools.ts
@Tool({
  name: 'get_user_profile',
  description: 'Get user profile information',
  inputSchema: z.object({}),
  examples: {
    request: {},
    response: {
      user: {
        id: 'user-1',
        name: 'Emily Johnson',
        email: 'emily@example.com',
        avatar: 'https://example.com/avatar.jpg',
        memberSince: '2024-01-01'
      },
      stats: {
        totalOrders: 15,
        totalSpent: 1234.56
      }
    }
  }
})
@Widget('user-profile')
async getUserProfile(input: any, ctx: ExecutionContext) {
  // Tool implementation...
}
3. Add to Widget Manifest
JSON

{
  "uri": "/user-profile",
  "name": "User Profile",
  "description": "Displays user profile with stats",
  "examples": [
    {
      "name": "Emily's Profile",
      "description": "Profile for Emily Johnson",
      "data": {
        "user": {
          "id": "user-1",
          "name": "Emily Johnson",
          "email": "emily@example.com",
          "avatar": "https://example.com/avatar.jpg",
          "memberSince": "2024-01-01"
        },
        "stats": {
          "totalOrders": 15,
          "totalSpent": 1234.56
        }
      }
    },
    {
      "name": "New User Profile",
      "description": "Profile for a new user",
      "data": {
        "user": {
          "id": "user-2",
          "name": "John Doe",
          "email": "john@example.com",
          "avatar": "https://example.com/avatar2.jpg",
          "memberSince": "2025-01-20"
        },
        "stats": {
          "totalOrders": 0,
          "totalSpent": 0
        }
      }
    }
  ],
  "tags": ["users", "profile"]
}
4. Preview in Studio
Restart dev server (rebuilds): npm run dev
Open Studio → Resources tab
Find "User Profile" in UI Widgets section
Switch between examples using dropdown
Click Enlarge for full view
5. Iterate on UI
Now you can:

Adjust styles in user-profile/page.tsx
See changes instantly with hot reload
Test with different example data
No backend needed!
Best Practices
Data Quality
Use Realistic Data

JSON

{
  "data": {
    "product": {
      "name": "Wireless Bluetooth Headphones",
      "price": 79.99,
      "image_url": "https://cdn.example.com/headphones.jpg"
    }
  }
}
Don't Use Placeholder Data

JSON

{
  "data": {
    "product": {
      "name": "Product Name",
      "price": 0,
      "image_url": "image.jpg"
    }
  }
}
Example Naming
Descriptive Names

"In Stock Product"
"Low Stock Warning"
"Out of Stock"
Generic Names

"Example 1"
"Test"
"Data"
Data Consistency
Match Tool Output Structure

Typescript

// Tool returns this:
return {
  items: [...],
  total: 123.45,
  itemCount: 3
};

// Manifest should have:
{
  "data": {
    "items": [...],
    "total": 123.45,
    "itemCount": 3
  }
}
Multiple Examples
Provide examples for different UI states:

Empty states (no data)
Loading states (if applicable)
Error states (if applicable)
Success states (normal operation)
Edge cases (very long text, many items, etc.)
Tags
Use consistent, lowercase tags:

JSON

{
  "tags": ["auth", "login", "user"]
}
Common tag categories:

Module: auth, products, cart, orders
Type: list, details, form, confirmation
Action: create, update, delete, view
Troubleshooting
Widgets Not Appearing in Studio
Problem: Resources tab doesn't show UI Widgets section

Solutions:

Check manifest exists at src/widgets/widget-manifest.json
Verify JSON is valid (no syntax errors)
Rebuild the project: npm run build
Restart dev server: npm run dev
Widget Preview Not Loading
Problem: Preview shows "No widget URI available"

Solutions:

Check uri field matches your widget folder name
Verify widget component exists at src/widgets/app{uri}/page.tsx
Check uri starts with / (e.g., /product-card)
Wrong Data Displayed
Problem: Widget shows incorrect or malformed data

Solutions:

Compare manifest data structure with tool's example response
Check for typos in field names
Ensure nested objects match exactly
Verify data types (string vs number)
Example Selector Not Working
Problem: Dropdown doesn't update preview

Solutions:

Check multiple examples exist in widget definition
Ensure each example has unique name
Clear browser cache and reload
Check browser console for errors
Enlarge Button Not Working
Problem: Modal doesn't open or opens delayed

Solutions:

Verify EnlargeModal is in root layout
Check Zustand store is properly configured
Try clicking once and waiting a moment
Check browser console for errors
Advanced Features
Dynamic Example Generation
For large datasets, you can generate examples programmatically:

Javascript

// generate-manifest.js
const products = require('./data/products.json');

const manifest = {
  version: "1.0.0",
  widgets: [
    {
      uri: "/products-grid",
      name: "Products Grid",
      description: "Browse products",
      examples: [
        {
          name: "Electronics",
          data: {
            products: products.filter(p => p.category === 'Electronics').slice(0, 10)
          }
        },
        {
          name: "Clothing",
          data: {
            products: products.filter(p => p.category === 'Clothing').slice(0, 10)
          }
        }
      ],
      tags: ["products", "grid"]
    }
  ]
};

require('fs').writeFileSync(
  'src/widgets/widget-manifest.json',
  JSON.stringify(manifest, null, 2)
);
Run: node generate-manifest.js

TypeScript Type Safety
Define types for your manifest:

Typescript

// widget-manifest.d.ts
export interface WidgetExample {
  name: string;
  description?: string;
  data: Record<string, any>;
}

export interface WidgetMetadata {
  uri: string;
  name: string;
  description: string;
  examples: WidgetExample[];
  tags?: string[];
}

export interface WidgetManifest {
  version: string;
  widgets: WidgetMetadata[];
  generatedAt?: string;
}
Use with defineWidgetMetadata helper (available in SDK):

Typescript

import { defineWidgetMetadata } from '@nitrostack/widgets';

const widget = defineWidgetMetadata({
  uri: '/product-card',
  name: 'Product Card',
  description: 'Display product details',
  examples: [{ name: 'Example', data: {} }],
  tags: ['products']
});
Next Steps
Learn More: Check out the UI Widgets Guide
See Templates: Explore templates/typescript-auth for a complete example
Join Community: Share your widgets and get help
Need Help? If you encounter issues not covered here, please open an issue on GitHub or join our community Discord.

Previous
🎨 UI Widgets
Next
⚡ Caching
Widget SDK API Reference
Overview
The NitroStack Widget SDK provides a modern, type-safe API for building interactive widgets that integrate with MCP servers and ChatGPT. The SDK offers React hooks, a singleton SDK class, and utility functions for common widget operations.

Compatibility: The Widget SDK supports both OpenAI Apps SDK (window.openai) and MCP Apps (window.__MCP_APP_CONTEXT__) specifications. NitroStack handles this internally - your widgets work seamlessly on both platforms.

Quick Start
Typescript

'use client';

import { useWidgetSDK, useTheme } from '@nitrostack/widgets';

export default function MyWidget() {
  const { isReady, callTool, getToolOutput } = useWidgetSDK();
  const theme = useTheme();
  
  if (!isReady) return <div>Loading...</div>;
  
  const data = getToolOutput();
  
  return (
    <div style={{ 
      background: theme === 'dark' ? '#000' : '#fff',
      color: theme === 'dark' ? '#fff' : '#000'
    }}>
      <h1>{data.title}</h1>
    </div>
  );
}
Core Hooks
useWidgetSDK()
Primary hook for accessing all Widget SDK functionality.

Returns:

Typescript

{
  sdk: WidgetSDK;
  isReady: boolean;
  
  // State Management
  setState: (state: any) => Promise<void>;
  getState: () => any;
  
  // Tool Calling
  callTool: (name: string, args?: Record<string, unknown>) => Promise<CallToolResponse>;
  
  // Display Controls
  requestFullscreen: () => Promise<void>;
  requestInline: () => Promise<void>;
  requestPip: () => Promise<void>;
  requestDisplayMode: (mode: DisplayMode) => Promise<{ mode: DisplayMode }>;
  requestClose: () => void;
  
  // Navigation
  openExternal: (url: string) => void;
  sendFollowUpMessage: (prompt: string) => Promise<void>;
  
  // Data Access
  getToolInput: <T>() => T | null;
  getToolOutput: <T>() => T | null;
  getToolResponseMetadata: <T>() => T | null;
  getTheme: () => 'light' | 'dark';
  getMaxHeight: () => number;
  getDisplayMode: () => DisplayMode;
  getUserAgent: () => UserAgent | null;
  getLocale: () => string;
  getSafeArea: () => SafeArea | null;
}
Example:

Typescript

function InteractiveWidget() {
  const { isReady, callTool, getToolOutput, requestFullscreen } = useWidgetSDK();
  
  const handleAction = async () => {
    const result = await callTool('process_data', { id: '123' });
    console.log('Tool result:', result);
  };
  
  return (
    <div>
      <button onClick={handleAction}>Process</button>
      <button onClick={requestFullscreen}>Fullscreen</button>
    </div>
  );
}
useTheme()
Get the current theme (light or dark mode).

Returns: 'light' | 'dark' | null

Example:

Typescript

function ThemedWidget() {
  const theme = useTheme();
  
  const styles = {
    background: theme === 'dark' ? '#1a1a1a' : '#ffffff',
    color: theme === 'dark' ? '#ffffff' : '#000000',
    border: `1px solid ${theme === 'dark' ? '#333' : '#ddd'}`
  };
  
  return <div style={styles}>Theme-aware content</div>;
}
useDisplayMode()
Get the current display mode.

Returns: 'inline' | 'fullscreen' | 'pip' | null

Example:

Typescript

function ResponsiveWidget() {
  const displayMode = useDisplayMode();
  
  const padding = displayMode === 'fullscreen' ? '48px' : '16px';
  const fontSize = displayMode === 'fullscreen' ? '24px' : '16px';
  
  return (
    <div style={{ padding, fontSize }}>
      {displayMode === 'fullscreen' ? 'Fullscreen View' : 'Compact View'}
    </div>
  );
}
useMaxHeight()
Get the maximum height constraint for the widget.

Returns: number | null

Example:

Typescript

function ScrollableWidget() {
  const maxHeight = useMaxHeight();
  
  return (
    <div style={{ 
      maxHeight: maxHeight ? `${maxHeight}px` : 'none',
      overflow: 'auto'
    }}>
      <LongContent />
    </div>
  );
}
useWidgetState()
Manage persistent widget state with automatic synchronization.

Returns:

Typescript

{
  state: T | null;
  setState: (value: T | ((prev: T) => T)) => Promise<void>;
  isLoading: boolean;
}
Example:

Typescript

interface FormState {
  name: string;
  email: string;
}

function StatefulWidget() {
  const { state, setState, isLoading } = useWidgetState<FormState>();
  
  const updateName = (name: string) => {
    setState(prev => ({ ...prev, name }));
  };
  
  return (
    <div>
      <input 
        value={state?.name || ''} 
        onChange={(e) => updateName(e.target.value)}
      />
    </div>
  );
}
useOpenAiGlobal()
Subscribe to specific window.openai properties with automatic re-rendering on changes.

Parameters:

key: keyof OpenAiGlobals - Property to subscribe to
Returns: Property value or null

Example:

Typescript

function LocaleWidget() {
  const locale = useOpenAiGlobal('locale');
  const userAgent = useOpenAiGlobal('userAgent');
  
  return (
    <div>
      <p>Locale: {locale}</p>
      <p>Device: {userAgent?.deviceType}</p>
    </div>
  );
}
WidgetSDK Class
Singleton class providing direct access to all widget functionality.

getInstance()
Get the global SDK instance.

Returns: WidgetSDK

Example:

Typescript

import { getWidgetSDK } from '@nitrostack/widgets';

const sdk = getWidgetSDK();
isReady()
Check if the SDK is initialized and ready to use. Works with both OpenAI Apps SDK and MCP Apps.

Returns: boolean

Example:

Typescript

const sdk = getWidgetSDK();
if (sdk.isReady()) {
  const theme = sdk.getTheme();
}
isOpenAI()
Check if running in OpenAI Apps SDK context (window.openai).

Returns: boolean

Example:

Typescript

const sdk = getWidgetSDK();
if (sdk.isOpenAI()) {
  // OpenAI-specific features available
}
isMcpApps()
Check if running in MCP Apps context (window.__MCP_APP_CONTEXT__).

Returns: boolean

Example:

Typescript

const sdk = getWidgetSDK();
if (sdk.isMcpApps()) {
  // MCP Apps-specific features available
}
waitForReady()
Wait for the SDK to be ready with optional timeout.

Parameters:

timeout?: number - Timeout in milliseconds (default: 5000)
Returns: Promise<void>

Example:

Typescript

const sdk = getWidgetSDK();
try {
  await sdk.waitForReady(3000);
  console.log('SDK ready');
} catch (error) {
  console.error('SDK initialization timeout');
}
State Management
setState()
Set widget state with persistence.

Parameters:

state: any - State object to persist
Returns: Promise<void>

Example:

Typescript

const { setState } = useWidgetSDK();

await setState({ 
  selectedItems: [1, 2, 3],
  filters: { category: 'electronics' }
});
getState()
Get current widget state.

Returns: any | null

Example:

Typescript

const { getState } = useWidgetSDK();
const currentState = getState();
Tool Calling
callTool()
Call an MCP tool from within the widget.

Parameters:

name: string - Tool name
args?: Record<string, unknown> - Tool arguments
Returns: Promise<CallToolResponse>

Example:

Typescript

const { callTool } = useWidgetSDK();

const result = await callTool('search_products', {
  query: 'laptop',
  limit: 10
});

console.log('Products:', result.content);
Display Controls
requestFullscreen()
Request fullscreen display mode.

Returns: Promise<void>

Example:

Typescript

const { requestFullscreen } = useWidgetSDK();

<button onClick={requestFullscreen}>
  Expand to Fullscreen
</button>
requestInline()
Request inline display mode.

Returns: Promise<void>

requestPip()
Request picture-in-picture display mode.

Returns: Promise<void>

requestDisplayMode()
Request specific display mode.

Parameters:

mode: DisplayMode - 'inline' | 'fullscreen' | 'pip'
Returns: Promise<{ mode: DisplayMode }>

Example:

Typescript

const { requestDisplayMode } = useWidgetSDK();

await requestDisplayMode('fullscreen');
requestClose()
Close the widget.

Returns: void

Example:

Typescript

const { requestClose } = useWidgetSDK();

<button onClick={requestClose}>Close</button>
Navigation
openExternal()
Open a URL in an external browser.

Parameters:

url: string - URL to open
Returns: void

Example:

Typescript

const { openExternal } = useWidgetSDK();

<a onClick={() => openExternal('https://example.com')}>
  Visit Website
</a>
sendFollowUpMessage()
Send a follow-up message to the chat.

Parameters:

prompt: string - Message to send
Returns: Promise<void>

Example:

Typescript

const { sendFollowUpMessage } = useWidgetSDK();

const askForMore = async () => {
  await sendFollowUpMessage('Show me more products like this');
};
Data Access
getToolInput()
Get the input parameters passed to the tool.

Type Parameter: T - Type of input data

Returns: T | null

Example:

Typescript

interface SearchInput {
  query: string;
  filters: string[];
}

const { getToolInput } = useWidgetSDK();
const input = getToolInput<SearchInput>();

console.log('Search query:', input?.query);
getToolOutput()
Get the output data from the tool.

Type Parameter: T - Type of output data

Returns: T | null

Example:

Typescript

interface ProductData {
  id: string;
  name: string;
  price: number;
}

const { getToolOutput } = useWidgetSDK();
const product = getToolOutput<ProductData>();
getToolResponseMetadata()
Get metadata about the tool response.

Type Parameter: T - Type of metadata

Returns: T | null

getTheme()
Get current theme.

Returns: 'light' | 'dark'

getMaxHeight()
Get maximum height constraint.

Returns: number

getDisplayMode()
Get current display mode.

Returns: DisplayMode

getUserAgent()
Get user agent information.

Returns: UserAgent | null

Example:

Typescript

const { getUserAgent } = useWidgetSDK();
const ua = getUserAgent();

if (ua?.deviceType === 'mobile') {
  // Show mobile-optimized UI
}
getLocale()
Get user's locale.

Returns: string

Example:

Typescript

const { getLocale } = useWidgetSDK();
const locale = getLocale(); // e.g., 'en-US'
getSafeArea()
Get safe area insets for the widget.

Returns: SafeArea | null

Utility Functions
prefersReducedMotion()
Check if user prefers reduced motion.

Returns: boolean

Example:

Typescript

import { prefersReducedMotion } from '@nitrostack/widgets';

const shouldAnimate = !prefersReducedMotion();
isPrimarilyTouchDevice()
Check if device is primarily touch-based.

Returns: boolean

Example:

Typescript

import { isPrimarilyTouchDevice } from '@nitrostack/widgets';

const buttonSize = isPrimarilyTouchDevice() ? '48px' : '32px';
isHoverAvailable()
Check if hover interactions are available.

Returns: boolean

Example:

Typescript

import { isHoverAvailable } from '@nitrostack/widgets';

const showTooltipOnHover = isHoverAvailable();
prefersDarkColorScheme()
Check if user prefers dark color scheme.

Returns: boolean

Example:

Typescript

import { prefersDarkColorScheme } from '@nitrostack/widgets';

const defaultTheme = prefersDarkColorScheme() ? 'dark' : 'light';
Type Definitions
DisplayMode
Typescript

type DisplayMode = 'inline' | 'fullscreen' | 'pip';
Theme
Typescript

type Theme = 'light' | 'dark';
CallToolResponse
Typescript

interface CallToolResponse {
  result: string;              // Primary result as string
  structuredContent?: unknown; // Optional structured content (OpenAI Apps SDK)
  isError?: boolean;           // Error indicator
}
UserAgent
Typescript

interface UserAgent {
  deviceType: DeviceType;
  browser: string;
  os: string;
}

type DeviceType = 'mobile' | 'tablet' | 'desktop';
SafeArea
Typescript

interface SafeArea {
  insets: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };
}
McpAppContext (MCP Apps Compatibility)
Typescript

interface McpAppContext<ToolInput = unknown, ToolOutput = unknown> {
  toolInput: ToolInput;
  toolOutput: ToolOutput | null;
  theme: Theme;
  locale: string;
  displayMode: DisplayMode;
  maxHeight: number;
}
McpAppAPI (MCP Apps Compatibility)
Typescript

interface McpAppAPI {
  callTool: (name: string, args: Record<string, unknown>) => Promise<CallToolResponse>;
  requestDisplayMode: (args: { mode: DisplayMode }) => Promise<{ mode: DisplayMode }>;
  requestClose(): void;
  openExternal(payload: { href: string }): void;
}
Components
WidgetLayout
Wrapper component that provides consistent layout and theme integration.

Props:

Typescript

interface WidgetLayoutProps {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}
Example:

Typescript

import { WidgetLayout } from '@nitrostack/widgets';

export default function MyWidget() {
  return (
    <WidgetLayout>
      <h1>My Widget</h1>
      <p>Content automatically adapts to theme</p>
    </WidgetLayout>
  );
}
Legacy API
withToolData()
Higher-Order Component for automatic data fetching (legacy pattern).

Note: This is maintained for backward compatibility. New widgets should use useWidgetSDK() instead.

Example:

Typescript

import { withToolData } from '@nitrostack/widgets';

function MyWidget({ data }) {
  return <div>{data.title}</div>;
}

export default withToolData(MyWidget);
Best Practices
1. Always Check isReady
Typescript

const { isReady, getToolOutput } = useWidgetSDK();

if (!isReady) {
  return <div>Loading...</div>;
}

const data = getToolOutput();
2. Use Type Parameters
Typescript

interface ProductData {
  id: string;
  name: string;
  price: number;
}

const product = getToolOutput<ProductData>();
// TypeScript knows the shape of product
3. Handle Null Values
Typescript

const theme = useTheme();
const bgColor = theme === 'dark' ? '#000' : '#fff';
// Default to light theme if null
4. Combine Hooks for Responsive Design
Typescript

function AdaptiveWidget() {
  const theme = useTheme();
  const displayMode = useDisplayMode();
  const maxHeight = useMaxHeight();
  
  const styles = {
    background: theme === 'dark' ? '#000' : '#fff',
    padding: displayMode === 'fullscreen' ? '48px' : '16px',
    maxHeight: maxHeight ? `${maxHeight}px` : 'none'
  };
  
  return <div style={styles}>Adaptive content</div>;
}
Migration from withToolData
See Widget SDK Migration Guide for detailed migration instructions.

See Also
UI Widgets Guide
Tools Guide
Widget Examples Guide
Next
👋 Introduction
File Upload Guide
Overview
NitroStack supports file uploads through base64-encoded content passed to tools. This guide explains how to handle file uploads in your MCP tools, including processing images, documents, and other file types.

How File Uploads Work
When a user uploads a file through an MCP client (like NitroStudio), the file is:

Encoded as base64 string
Passed to the tool via input parameters
Decoded and processed by your tool
Tool Schema for File Uploads
Define your tool's input schema to accept file data:

Typescript

import { ToolDecorator as Tool, ExecutionContext, z } from '@nitrostack/core';
import * as fs from 'fs';
import * as path from 'path';

export class FileTools {
  @Tool({
    name: 'process_file',
    description: 'Process an uploaded file',
    inputSchema: z.object({
      file_name: z.string().describe('Name of the uploaded file'),
      file_type: z.string().describe('MIME type of the uploaded file'),
      file_content: z.string().describe('Base64 encoded file content')
    })
  })
  async processFile(input: any, ctx: ExecutionContext) {
    // File processing logic here
  }
}
Decoding Base64 Files
Files can be sent in two formats:

Format 1: Data URL
data:image/png;base64,iVBORw0KGgo...
Format 2: Raw Base64
iVBORw0KGgo...
Universal Decoder
Handle both formats with this pattern:

Typescript

function decodeBase64File(content: string): Buffer {
  // Check for data URL format
  const matches = content.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
  
  if (matches && matches.length === 3) {
    // Data URL format - extract base64 portion
    return Buffer.from(matches[2], 'base64');
  } else {
    // Raw base64 format
    return Buffer.from(content, 'base64');
  }
}
Complete File Upload Example
Here's a complete example from the starter template:

Typescript

import { ToolDecorator as Tool, ExecutionContext, z } from '@nitrostack/core';
import * as fs from 'fs';
import * as path from 'path';

export class FileTools {
  @Tool({
    name: 'convert_temperature',
    description: 'Convert temperature units based on file content or direct input',
    inputSchema: z.object({
      file_name: z.string().describe('Name of the uploaded file'),
      file_type: z.string().describe('MIME type of the uploaded file'),
      file_content: z.string().describe('Base64 encoded file content'),
      value: z.number().optional().describe('Temperature value to convert'),
      from_unit: z.enum(['C', 'F']).optional().describe('Unit to convert from'),
      to_unit: z.enum(['C', 'F']).optional().describe('Unit to convert to')
    })
  })
  async convertTemperature(input: any, ctx: ExecutionContext) {
    ctx.logger.info('Processing file', {
      name: input.file_name,
      type: input.file_type
    });

    // Create uploads directory
    const uploadsDir = path.join(process.cwd(), 'uploads');
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir, { recursive: true });
    }

    const filePath = path.join(uploadsDir, input.file_name);

    // Decode and save file
    if (input.file_content) {
      try {
        const matches = input.file_content.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
        let buffer;

        if (matches && matches.length === 3) {
          buffer = Buffer.from(matches[2], 'base64');
        } else {
          buffer = Buffer.from(input.file_content, 'base64');
        }

        fs.writeFileSync(filePath, buffer);
        ctx.logger.info(`Saved file to ${filePath}`);
      } catch (e) {
        ctx.logger.error('Failed to save file', { 
          error: e instanceof Error ? e.message : String(e) 
        });
      }
    }

    return {
      status: 'success',
      message: `File ${input.file_name} processed successfully`,
      saved_path: filePath,
      file_type: input.file_type
    };
  }
}
Processing Different File Types
Images
Typescript

import sharp from 'sharp';  // npm install sharp

@Tool({
  name: 'process_image',
  description: 'Process and resize an uploaded image',
  inputSchema: z.object({
    file_name: z.string(),
    file_type: z.string(),
    file_content: z.string(),
    width: z.number().optional().describe('Target width'),
    height: z.number().optional().describe('Target height')
  })
})
async processImage(input: any, ctx: ExecutionContext) {
  const buffer = this.decodeBase64(input.file_content);
  
  // Validate image type
  if (!input.file_type.startsWith('image/')) {
    throw new Error('File must be an image');
  }
  
  // Process with sharp
  const processed = await sharp(buffer)
    .resize(input.width || 800, input.height || 600)
    .toBuffer();
  
  // Save processed image
  const outputPath = path.join('uploads', `processed_${input.file_name}`);
  fs.writeFileSync(outputPath, processed);
  
  return {
    status: 'success',
    original_size: buffer.length,
    processed_size: processed.length,
    output_path: outputPath
  };
}
PDFs
Typescript

import pdf from 'pdf-parse';  // npm install pdf-parse

@Tool({
  name: 'extract_pdf_text',
  description: 'Extract text from a PDF file',
  inputSchema: z.object({
    file_name: z.string(),
    file_type: z.string(),
    file_content: z.string()
  })
})
async extractPdfText(input: any, ctx: ExecutionContext) {
  const buffer = this.decodeBase64(input.file_content);
  
  if (input.file_type !== 'application/pdf') {
    throw new Error('File must be a PDF');
  }
  
  const data = await pdf(buffer);
  
  return {
    status: 'success',
    pages: data.numpages,
    text: data.text,
    info: data.info
  };
}
CSV Files
Typescript

import { parse } from 'csv-parse/sync';  // npm install csv-parse

@Tool({
  name: 'parse_csv',
  description: 'Parse a CSV file and return data',
  inputSchema: z.object({
    file_name: z.string(),
    file_type: z.string(),
    file_content: z.string(),
    has_headers: z.boolean().default(true)
  })
})
async parseCsv(input: any, ctx: ExecutionContext) {
  const buffer = this.decodeBase64(input.file_content);
  const content = buffer.toString('utf-8');
  
  const records = parse(content, {
    columns: input.has_headers,
    skip_empty_lines: true
  });
  
  return {
    status: 'success',
    row_count: records.length,
    data: records
  };
}
File Validation
Always validate uploaded files:

Typescript

interface FileValidation {
  maxSize?: number;        // Max file size in bytes
  allowedTypes?: string[]; // Allowed MIME types
  allowedExtensions?: string[]; // Allowed extensions
}

function validateFile(
  fileName: string,
  fileType: string,
  content: string,
  validation: FileValidation
): void {
  // Check extension
  if (validation.allowedExtensions) {
    const ext = path.extname(fileName).toLowerCase();
    if (!validation.allowedExtensions.includes(ext)) {
      throw new Error(`File extension ${ext} not allowed`);
    }
  }
  
  // Check MIME type
  if (validation.allowedTypes) {
    if (!validation.allowedTypes.includes(fileType)) {
      throw new Error(`File type ${fileType} not allowed`);
    }
  }
  
  // Check size (base64 is ~33% larger than original)
  if (validation.maxSize) {
    const estimatedSize = (content.length * 3) / 4;
    if (estimatedSize > validation.maxSize) {
      throw new Error(`File exceeds maximum size of ${validation.maxSize} bytes`);
    }
  }
}
Usage
Typescript

@Tool({
  name: 'upload_document',
  description: 'Upload a document',
  inputSchema: z.object({
    file_name: z.string(),
    file_type: z.string(),
    file_content: z.string()
  })
})
async uploadDocument(input: any, ctx: ExecutionContext) {
  // Validate file
  validateFile(input.file_name, input.file_type, input.file_content, {
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['application/pdf', 'image/png', 'image/jpeg'],
    allowedExtensions: ['.pdf', '.png', '.jpg', '.jpeg']
  });
  
  // Process file...
}
Security Best Practices
1. Sanitize File Names
Typescript

function sanitizeFileName(fileName: string): string {
  // Remove path traversal attempts
  let safe = fileName.replace(/\.\./g, '');
  
  // Remove special characters
  safe = safe.replace(/[^a-zA-Z0-9._-]/g, '_');
  
  // Limit length
  if (safe.length > 255) {
    const ext = path.extname(safe);
    safe = safe.substring(0, 255 - ext.length) + ext;
  }
  
  return safe;
}
2. Use Dedicated Upload Directory
Typescript

const UPLOAD_DIR = path.join(process.cwd(), 'uploads');

// Ensure uploads stay in designated directory
function getSecureUploadPath(fileName: string): string {
  const safeName = sanitizeFileName(fileName);
  const uploadPath = path.join(UPLOAD_DIR, safeName);
  
  // Verify path is still within upload directory
  if (!uploadPath.startsWith(UPLOAD_DIR)) {
    throw new Error('Invalid file path');
  }
  
  return uploadPath;
}
3. Scan for Malware
For production systems, consider scanning uploads:

Typescript

import { scanFile } from 'your-antivirus-scanner';

async function processUpload(content: string, fileName: string) {
  const buffer = decodeBase64(content);
  const tempPath = path.join('/tmp', fileName);
  
  fs.writeFileSync(tempPath, buffer);
  
  const scanResult = await scanFile(tempPath);
  if (scanResult.infected) {
    fs.unlinkSync(tempPath);
    throw new Error('Malware detected in uploaded file');
  }
  
  // Move to final location
  // ...
}
4. Limit File Sizes
Set reasonable limits:

Typescript

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

if (buffer.length > MAX_FILE_SIZE) {
  throw new Error(`File size exceeds limit of ${MAX_FILE_SIZE / 1024 / 1024}MB`);
}
Storing Files
Local Storage
Typescript

const uploadsDir = path.join(process.cwd(), 'uploads');
fs.writeFileSync(path.join(uploadsDir, fileName), buffer);
Cloud Storage (S3)
Typescript

import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const s3 = new S3Client({ region: 'us-east-1' });

async function uploadToS3(buffer: Buffer, key: string) {
  await s3.send(new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    Body: buffer
  }));
  
  return `s3://${process.env.S3_BUCKET}/${key}`;
}
Testing File Uploads
In NitroStudio
Open the Chat interface
Click the attachment icon
Select a file
Send your message
The file will be encoded and sent to your tool.

Manual Testing
Typescript

// Test with base64 encoded file
const testInput = {
  file_name: 'test.txt',
  file_type: 'text/plain',
  file_content: Buffer.from('Hello, World!').toString('base64')
};

const result = await tool.processFile(testInput, ctx);
Troubleshooting
File Not Decoding
Issue: Base64 decoding fails

Solution: Check for padding issues:

Typescript

function fixBase64Padding(str: string): string {
  // Add missing padding
  while (str.length % 4) {
    str += '=';
  }
  return str;
}
Memory Issues with Large Files
Issue: Large files cause memory problems

Solution: Use streaming for large files:

Typescript

import { Readable } from 'stream';

function base64ToStream(base64: string): Readable {
  const buffer = Buffer.from(base64, 'base64');
  return Readable.from(buffer);
}
File Extension Mismatch
Issue: MIME type doesn't match extension

Solution: Validate both and trust MIME type:

Typescript

const mimeToExt: Record<string, string> = {
  'image/png': '.png',
  'image/jpeg': '.jpg',
  'application/pdf': '.pdf'
};

const expectedExt = mimeToExt[input.file_type];
const actualExt = path.extname(input.file_name);

if (expectedExt !== actualExt) {
  ctx.logger.warn(`Extension mismatch: expected ${expectedExt}, got ${actualExt}`);
}
Next Steps
Tools Guide
Widget SDK Reference
Best Practices
Next
👋 Introduction
Caching Guide
Overview
NitroStack provides built-in caching capabilities to improve performance and reduce redundant operations. Use the @Cache decorator to automatically cache tool responses.

Basic Caching
Using @Cache Decorator
Typescript

import { Tool, Cache } from '@nitrostack/core';

@Tool({ name: 'get_config' })
@Cache({ ttl: 3600 })  // Cache for 1 hour
async getConfig(input: any, ctx: ExecutionContext) {
  const config = await this.configService.load();
  return config;
}
Cache Options
Typescript

interface CacheOptions {
  ttl: number;                              // Time to live in seconds
  key?: (input: any) => string;            // Custom cache key function
  invalidateOn?: string[];                 // Events that invalidate cache
}
TTL (Time To Live)
Common TTL Values
Typescript

// 5 minutes - frequently changing data
@Cache({ ttl: 300 })

// 1 hour - semi-static data
@Cache({ ttl: 3600 })

// 1 day - static configuration
@Cache({ ttl: 86400 })

// 1 week - rarely changing data
@Cache({ ttl: 604800 })
Dynamic TTL
Typescript

@Tool({ name: 'get_weather' })
@Cache({
  ttl: (input) => {
    // Cache current weather for 10 minutes
    // Cache forecast for 1 hour
    return input.type === 'current' ? 600 : 3600;
  }
})
async getWeather(input: any) {
  // ...
}
Custom Cache Keys
Simple Key
Typescript

@Tool({ name: 'get_product' })
@Cache({
  ttl: 600,
  key: (input) => `product:${input.product_id}`
})
async getProduct(input: any) {
  return await this.productService.findById(input.product_id);
}
Composite Key
Typescript

@Tool({ name: 'search_products' })
@Cache({
  ttl: 300,
  key: (input) => `products:${input.category}:${input.page}:${input.sort}`
})
async searchProducts(input: any) {
  return await this.productService.search(input);
}
User-Specific Cache
Typescript

@Tool({ name: 'get_recommendations' })
@UseGuards(JWTGuard)
@Cache({
  ttl: 1800,
  key: (input, ctx) => `recommendations:${ctx.auth?.subject}`
})
async getRecommendations(input: any, ctx: ExecutionContext) {
  const userId = ctx.auth?.subject;
  return await this.recommendationService.getFor(userId);
}
Cache Invalidation
Event-Based Invalidation
Typescript

@Tool({ name: 'get_product' })
@Cache({
  ttl: 3600,
  key: (input) => `product:${input.id}`,
  invalidateOn: ['product.updated', 'product.deleted']
})
async getProduct(input: any) {
  // Cache invalidated when these events are emitted
}

@Tool({ name: 'update_product' })
async updateProduct(input: any, ctx: ExecutionContext) {
  const product = await this.productService.update(input);
  
  // Invalidate cache
  ctx.emit('product.updated', { id: product.id });
  
  return product;
}
Manual Invalidation
Typescript

@Injectable()
export class CacheService {
  async invalidate(key: string): Promise<void> {
    // Remove from cache
  }
  
  async invalidatePattern(pattern: string): Promise<void> {
    // Remove all keys matching pattern
    // e.g., 'product:*'
  }
  
  async clear(): Promise<void> {
    // Clear entire cache
  }
}

// Usage
@Tool({ name: 'clear_cache' })
@UseGuards(AdminGuard)
async clearCache(input: any) {
  await this.cacheService.clear();
  return { success: true };
}
Cache Strategies
Cache-Aside (Lazy Loading)
Typescript

@Injectable()
export class ProductService {
  constructor(
    private db: DatabaseService,
    private cache: CacheService
  ) {}
  
  async findById(id: string) {
    // Check cache first
    const cached = await this.cache.get(`product:${id}`);
    if (cached) return cached;
    
    // Load from database
    const product = await this.db.queryOne(
      'SELECT * FROM products WHERE id = ?',
      [id]
    );
    
    // Store in cache
    await this.cache.set(`product:${id}`, product, 3600);
    
    return product;
  }
}
Write-Through
Typescript

async updateProduct(id: string, data: any) {
  // Update database
  await this.db.execute(
    'UPDATE products SET name = ? WHERE id = ?',
    [data.name, id]
  );
  
  // Update cache immediately
  const product = await this.db.queryOne(
    'SELECT * FROM products WHERE id = ?',
    [id]
  );
  await this.cache.set(`product:${id}`, product, 3600);
  
  return product;
}
Write-Behind
Typescript

async updateProduct(id: string, data: any) {
  // Update cache immediately
  await this.cache.set(`product:${id}`, data, 3600);
  
  // Queue database update
  await this.queue.add('update-product', { id, data });
  
  return data;
}
Cache Storage Backends
In-Memory (Default)
Typescript

// Fast but not persistent
// Lost on server restart
// Single-server only
Redis
Typescript

import { createClient } from 'redis';

@Injectable()
export class RedisCacheService {
  private client = createClient({
    url: process.env.REDIS_URL
  });
  
  async get(key: string): Promise<any> {
    const value = await this.client.get(key);
    return value ? JSON.parse(value) : null;
  }
  
  async set(key: string, value: any, ttl: number): Promise<void> {
    await this.client.setEx(
      key,
      ttl,
      JSON.stringify(value)
    );
  }
}
Memcached
Typescript

import Memcached from 'memcached';

@Injectable()
export class MemcachedService {
  private client = new Memcached(process.env.MEMCACHED_SERVERS);
  
  async get(key: string): Promise<any> {
    return new Promise((resolve) => {
      this.client.get(key, (err, data) => {
        resolve(err ? null : data);
      });
    });
  }
}
Best Practices
1. Set Appropriate TTL
Typescript

// Good - Match data volatility
@Cache({ ttl: 300 })  // 5 min for frequently changing data
@Cache({ ttl: 3600 }) // 1 hour for semi-static data
@Cache({ ttl: 86400 }) // 1 day for static data

// Avoid - Too long for dynamic data
@Cache({ ttl: 86400 })  // 1 day for stock prices
2. Use Specific Cache Keys
Typescript

// Good - Specific keys
key: (input) => `product:${input.id}:${input.locale}`

// Avoid - Generic keys
key: (input) => `data:${input.id}`
3. Cache Expensive Operations
Typescript

// Good - Cache database queries
@Cache({ ttl: 600 })
async searchProducts(input: any) {
  return await this.db.query(/* complex query */);
}

// Avoid - Caching simple operations
@Cache({ ttl: 600 })
async addNumbers(input: any) {
  return input.a + input.b;
}
4. Invalidate on Updates
Typescript

// Good - Invalidate when data changes
@Tool({ name: 'get_user' })
@Cache({
  ttl: 3600,
  invalidateOn: ['user.updated']
})

// Avoid - No invalidation strategy
@Tool({ name: 'get_user' })
@Cache({ ttl: 3600 })  // Stale data possible
5. Monitor Cache Metrics
Typescript

@Injectable()
export class CacheService {
  private hits = 0;
  private misses = 0;
  
  async get(key: string): Promise<any> {
    const value = await this.storage.get(key);
    
    if (value) {
      this.hits++;
    } else {
      this.misses++;
    }
    
    return value;
  }
  
  getMetrics() {
    const total = this.hits + this.misses;
    return {
      hits: this.hits,
      misses: this.misses,
      hitRate: total > 0 ? this.hits / total : 0
    };
  }
}
Performance Tips
1. Cache Hierarchies
Typescript

// L1: In-memory cache (fastest)
// L2: Redis cache (fast)
// L3: Database (slowest)

async findProduct(id: string) {
  // Check L1
  let product = this.memoryCache.get(id);
  if (product) return product;
  
  // Check L2
  product = await this.redisCache.get(id);
  if (product) {
    this.memoryCache.set(id, product);
    return product;
  }
  
  // Check L3
  product = await this.db.findById(id);
  await this.redisCache.set(id, product);
  this.memoryCache.set(id, product);
  
  return product;
}
2. Cache Warm-Up
Typescript

async onApplicationStart() {
  // Pre-load frequently accessed data
  const popular = await this.db.query(
    'SELECT * FROM products ORDER BY views DESC LIMIT 100'
  );
  
  for (const product of popular) {
    await this.cache.set(`product:${product.id}`, product, 3600);
  }
}
3. Compression
Typescript

import { compress, decompress } from 'lz-string';

async set(key: string, value: any, ttl: number) {
  const compressed = compress(JSON.stringify(value));
  await this.storage.set(key, compressed, ttl);
}

async get(key: string) {
  const compressed = await this.storage.get(key);
  return compressed ? JSON.parse(decompress(compressed)) : null;
}
Troubleshooting
Cache Not Working
Check TTL is set
Verify cache service is injected
Check cache key is consistent
Monitor cache hit/miss ratio
Stale Data
Reduce TTL
Implement invalidation
Use event-based clearing
Add version to cache keys
Memory Issues
Set max cache size
Implement LRU eviction
Use external cache (Redis)
Reduce TTL
Next Steps
Rate Limiting Guide
Performance Guide
Best Practices
Tip: Start with conservative TTLs and increase based on monitoring. It's easier to extend cache duration than to deal with stale data!

Previous
📋 Widget Manifest
Next
🚦 Rate Limiting
Rate Limiting Guide
Overview
Rate limiting protects your MCP server from abuse by restricting the number of requests users can make within a time window. NitroStack provides built-in rate limiting via the @RateLimit decorator.

Basic Rate Limiting
Using @RateLimit Decorator
Typescript

import { Tool, RateLimit } from '@nitrostack/core';

@Tool({ name: 'send_email' })
@RateLimit({ requests: 10, window: '1m' })  // 10 requests per minute
async sendEmail(input: any, ctx: ExecutionContext) {
  await this.emailService.send(input);
  return { success: true };
}
Rate Limit Options
Typescript

interface RateLimitOptions {
  requests: number;                        // Max requests allowed
  window: string;                          // Time window ('1m', '1h', '1d')
  key?: (ctx: ExecutionContext) => string; // Custom rate limit key
  message?: string;                        // Custom error message
  skipSuccessfulRequests?: boolean;        // Only count failed requests
  skipFailedRequests?: boolean;            // Only count successful requests
}
Time Windows
Common Windows
Typescript

// Per minute
@RateLimit({ requests: 60, window: '1m' })

// Per hour
@RateLimit({ requests: 1000, window: '1h' })

// Per day
@RateLimit({ requests: 10000, window: '1d' })

// Per week
@RateLimit({ requests: 50000, window: '7d' })
Window Formats
Typescript

'1s'   // 1 second
'30s'  // 30 seconds
'1m'   // 1 minute
'5m'   // 5 minutes
'1h'   // 1 hour
'12h'  // 12 hours
'1d'   // 1 day
'7d'   // 7 days
Rate Limit Keys
Default (IP-Based)
Typescript

// Limits by IP address
@RateLimit({ requests: 100, window: '1h' })
User-Based
Typescript

@Tool({ name: 'create_post' })
@UseGuards(JWTGuard)
@RateLimit({
  requests: 50,
  window: '1h',
  key: (ctx) => ctx.auth?.subject || 'anonymous'
})
async createPost(input: any, ctx: ExecutionContext) {
  // Each user has their own limit
}
API Key-Based
Typescript

@Tool({ name: 'api_call' })
@UseGuards(ApiKeyGuard)
@RateLimit({
  requests: 1000,
  window: '1h',
  key: (ctx) => ctx.auth?.keyId || 'unknown'
})
async apiCall(input: any, ctx: ExecutionContext) {
  // Each API key has its own limit
}
Custom Key
Typescript

@Tool({ name: 'search' })
@RateLimit({
  requests: 10,
  window: '1m',
  key: (ctx) => {
    const userId = ctx.auth?.subject;
    const endpoint = ctx.toolName;
    return `${userId}:${endpoint}`;
  }
})
async search(input: any, ctx: ExecutionContext) {
  // Limit per user per endpoint
}
Tiered Rate Limits
By User Role
Typescript

@Tool({ name: 'api_request' })
@UseGuards(JWTGuard)
@RateLimit({
  requests: (ctx) => {
    const role = ctx.auth?.role;
    if (role === 'premium') return 10000;
    if (role === 'pro') return 1000;
    return 100; // free tier
  },
  window: '1h'
})
async apiRequest(input: any, ctx: ExecutionContext) {
  // Different limits based on subscription
}
By Plan
Typescript

const RATE_LIMITS = {
  free: { requests: 100, window: '1h' },
  basic: { requests: 1000, window: '1h' },
  premium: { requests: 10000, window: '1h' },
  enterprise: { requests: 100000, window: '1h' }
};

@Tool({ name: 'advanced_feature' })
@UseGuards(JWTGuard)
@RateLimit((ctx) => {
  const plan = ctx.auth?.plan || 'free';
  return RATE_LIMITS[plan];
})
async advancedFeature(input: any, ctx: ExecutionContext) {
  // Dynamic limits based on plan
}
Multiple Rate Limits
Stacked Limits
Typescript

@Tool({ name: 'expensive_operation' })
@RateLimit({ requests: 10, window: '1m' })    // Per minute
@RateLimit({ requests: 100, window: '1h' })   // Per hour
@RateLimit({ requests: 1000, window: '1d' })  // Per day
async expensiveOperation(input: any) {
  // Must pass all rate limit checks
}
Error Handling
Custom Error Messages
Typescript

@RateLimit({
  requests: 10,
  window: '1m',
  message: 'Too many requests. Please wait before trying again.'
})
With Retry Information
Typescript

@RateLimit({
  requests: 10,
  window: '1m',
  message: (remaining, resetAt) => 
    `Rate limit exceeded. ${remaining} requests remaining. Resets at ${resetAt}`
})
Advanced Patterns
Burst Allowance
Typescript

@Injectable()
export class BurstRateLimiter {
  @RateLimit({ requests: 10, window: '1s' })   // Burst
  @RateLimit({ requests: 100, window: '1m' })  // Sustained
  async handleRequest() {
    // Allows bursts but limits sustained load
  }
}
Adaptive Rate Limiting
Typescript

@Injectable()
export class AdaptiveRateLimiter {
  private systemLoad = 0;
  
  @RateLimit({
    requests: (ctx) => {
      // Reduce limits under high load
      if (this.systemLoad > 0.8) return 50;
      if (this.systemLoad > 0.5) return 100;
      return 200;
    },
    window: '1m'
  })
  async handleRequest() {
    // Limits adjust based on system load
  }
}
Geographic Rate Limiting
Typescript

@RateLimit({
  requests: (ctx) => {
    const region = ctx.metadata.region;
    // Higher limits for preferred regions
    if (region === 'us-east') return 1000;
    return 100;
  },
  window: '1h'
})
Storage Backends
In-Memory (Default)
Typescript

// Fast but not distributed
// Lost on restart
// Single-server only
Redis
Typescript

import { createClient } from 'redis';

@Injectable()
export class RedisRateLimiter {
  private client = createClient({
    url: process.env.REDIS_URL
  });
  
  async checkLimit(key: string, limit: number, window: number): Promise<boolean> {
    const current = await this.client.incr(key);
    
    if (current === 1) {
      // First request, set expiry
      await this.client.expire(key, window);
    }
    
    return current <= limit;
  }
  
  async getRemainingQuota(key: string, limit: number): Promise<number> {
    const current = await this.client.get(key);
    return limit - (parseInt(current || '0'));
  }
}
Distributed Rate Limiting
Typescript

@Injectable()
export class DistributedRateLimiter {
  constructor(private redis: RedisService) {}
  
  async checkLimit(
    userId: string,
    limit: number,
    window: number
  ): Promise<boolean> {
    const key = `rate_limit:${userId}`;
    
    // Use Redis sliding window
    const now = Date.now();
    const windowStart = now - (window * 1000);
    
    // Remove old entries
    await this.redis.zremrangebyscore(key, 0, windowStart);
    
    // Count current requests
    const count = await this.redis.zcard(key);
    
    if (count >= limit) {
      return false;
    }
    
    // Add new request
    await this.redis.zadd(key, now, `${now}-${Math.random()}`);
    await this.redis.expire(key, window);
    
    return true;
  }
}
Response Headers
Include Rate Limit Info
Typescript

@Tool({ name: 'api_endpoint' })
@RateLimit({ requests: 100, window: '1h' })
async apiEndpoint(input: any, ctx: ExecutionContext) {
  const result = await this.processRequest(input);
  
  // Add rate limit headers
  ctx.metadata.rateLimitLimit = 100;
  ctx.metadata.rateLimitRemaining = await this.getRemainingQuota(ctx);
  ctx.metadata.rateLimitReset = await this.getResetTime(ctx);
  
  return result;
}
Monitoring
Track Rate Limit Events
Typescript

@Tool({ name: 'monitored_tool' })
@RateLimit({ requests: 100, window: '1h' })
async monitoredTool(input: any, ctx: ExecutionContext) {
  try {
    return await this.process(input);
  } catch (error) {
    if (error.code === 'RATE_LIMIT_EXCEEDED') {
      ctx.emit('rate_limit.exceeded', {
        userId: ctx.auth?.subject,
        tool: ctx.toolName,
        limit: 100
      });
    }
    throw error;
  }
}
Metrics Collection
Typescript

@Injectable()
export class RateLimitMetrics {
  private exceeded = 0;
  private allowed = 0;
  
  @OnEvent('rate_limit.exceeded')
  handleExceeded() {
    this.exceeded++;
  }
  
  @OnEvent('rate_limit.allowed')
  handleAllowed() {
    this.allowed++;
  }
  
  getMetrics() {
    const total = this.exceeded + this.allowed;
    return {
      exceeded: this.exceeded,
      allowed: this.allowed,
      rejectionRate: total > 0 ? this.exceeded / total : 0
    };
  }
}
Best Practices
1. Set Appropriate Limits
Typescript

// Good - Match resource consumption
@RateLimit({ requests: 1, window: '5s' })    // Very expensive operation
@RateLimit({ requests: 100, window: '1h' })  // Moderate operation
@RateLimit({ requests: 1000, window: '1h' }) // Light operation

// Avoid - Too restrictive or too lenient
@RateLimit({ requests: 1, window: '1h' })    // Too strict
@RateLimit({ requests: 1000000, window: '1s' }) // Too lenient
2. Use Per-User Limits
Typescript

// Good - Per user
@RateLimit({
  requests: 100,
  window: '1h',
  key: (ctx) => ctx.auth?.subject || ctx.metadata.ip
})

// Avoid - Global limit (DDoS vulnerable)
@RateLimit({ requests: 1000, window: '1h' })
3. Provide Clear Errors
Typescript

// Good - Helpful message
@RateLimit({
  requests: 10,
  window: '1m',
  message: 'Rate limit: 10 requests per minute. Please slow down.'
})

// Avoid - Generic message
@RateLimit({
  requests: 10,
  window: '1m',
  message: 'Error'
})
4. Monitor and Adjust
Typescript

// Track metrics
@OnEvent('rate_limit.exceeded')
async handleExceeded(data: any) {
  await this.metrics.record('rate_limit_exceeded', {
    userId: data.userId,
    endpoint: data.tool
  });
  
  // Alert if too many users hitting limits
  if (await this.metrics.getExceededRate() > 0.1) {
    await this.alerts.send('Rate limits may be too strict');
  }
}
5. Implement Graceful Degradation
Typescript

@Tool({ name: 'search' })
@RateLimit({ requests: 100, window: '1h' })
async search(input: any, ctx: ExecutionContext) {
  try {
    return await this.fullSearch(input);
  } catch (error) {
    if (error.code === 'RATE_LIMIT_EXCEEDED') {
      // Fall back to basic search
      return await this.basicSearch(input);
    }
    throw error;
  }
}
Common Patterns
Email Sending
Typescript

@Tool({ name: 'send_email' })
@RateLimit({ requests: 10, window: '1m' })   // Per minute
@RateLimit({ requests: 100, window: '1h' })  // Per hour
@RateLimit({ requests: 500, window: '1d' })  // Per day
async sendEmail(input: any) {
  // Prevent email spam
}
API Calls
Typescript

@Tool({ name: 'external_api' })
@RateLimit({
  requests: 50,
  window: '1m',
  key: (ctx) => ctx.auth?.apiKey || 'anonymous'
})
async callExternalApi(input: any) {
  // Comply with external API limits
}
File Uploads
Typescript

@Tool({ name: 'upload_file' })
@RateLimit({ requests: 5, window: '1m' })  // Prevent abuse
async uploadFile(input: any) {
  // Limit upload frequency
}
Troubleshooting
Users Hitting Limits
Check if limits are too strict
Verify window is appropriate
Consider tiered plans
Monitor legitimate usage patterns
Limits Not Working
Verify decorator is applied
Check rate limit key is correct
Ensure storage backend is working
Test with multiple requests
Performance Issues
Use Redis for distributed systems
Implement sliding windows
Clean up expired keys
Monitor storage size
Next Steps
Caching Guide
Performance Guide
Security Best Practices
Tip: Start with generous limits and tighten based on actual usage patterns and resource availability!

Previous
⚡ Caching
Next
💻 CLI Reference
MCP Tasks Guide
The Model Context Protocol (MCP) Tasks specification enables long-running, asynchronous operations in MCP servers. Unlike standard tool calls, which are expected to return results within a few seconds, tasks allow for operations that might take minutes or even longer—such as data processing, heavy auditing, or multi-step human-in-the-loop workflows.

NitroStack provides a first-class implementation of MCP Tasks, handling the complex state management, polling, and notifications automatically so you can focus on your tool logic.

Overview
A standard MCP tool call is synchronous: the client waits for the server to finish and send back a response. If the operation is slow, the transport (like SSE or STDIO) might time out, or the user interface might freeze.

MCP Tasks solve this by:

Immediate Acceptance: The server returns a taskId immediately.
Asynchronous Execution: The tool continues running in the background.
Progress Reporting: The server sends updates about what it's doing.
Cooperative Cancellation: Clients can cancel tasks mid-flight.
Flexible Retrieval: Results can be polled or retrieved via a blocking call once done.
Configuration
To enable tasks for a tool, use the taskSupport option in the @Tool decorator.

Task Support Levels
Value	Behavior
'forbidden'	(Default) The tool cannot be called as a task. Sending a task request returns an error.
'optional'	The tool can be called normally (sync) OR as a task (async).
'required'	The tool must be called as a task. Normal calls return an error.
Example
Typescript

import { ToolDecorator as Tool, z } from '@nitrostack/core';

export class MyTools {
  @Tool({
    name: 'heavy_audit',
    description: 'Performs a complex system audit',
    inputSchema: z.object({ level: z.string() }),
    taskSupport: 'optional' // Can run as a task or sync
  })
  async audit(args: any, ctx: ExecutionContext) {
    // ... logic ...
  }
}
Implementation
When a tool is invoked as a task, NitroStack populates ctx.task in the ExecutionContext. Use this object to interact with the task lifecycle.

Reporting Progress
Keep the user informed by sending status messages during execution.

Typescript

@Tool({ name: 'import_data', taskSupport: 'required' })
async importData(args: any, ctx: ExecutionContext) {
  if (ctx.task) {
    ctx.task.updateProgress('Connecting to database...');
    // ... work ...
    ctx.task.updateProgress('Scanning records...');
    // ... work ...
    ctx.task.updateProgress('Processing batch 1 of 10...');
  }
  return { imported: 100 };
}
Requesting Input
If the task requires human feedback (e.g., "Confirm delete?" or "Provide API key"), transition the task to the input_required state.

Typescript

ctx.task.requestInput('System detected a conflict. Should we overwrite? (yes/no)');
Supporting Cancellation
Tasks can be cancelled by the client. Well-behaved tools check for cancellation periodically and clean up resources.

Typescript

for (const item of items) {
  // Throws a TaskCancelledError if client requested cancellation
  ctx.task?.throwIfCancelled();
  
  // Or check boolean for manual cleanup
  if (ctx.task?.isCancelled) {
    await this.cleanup();
    ctx.task.throwIfCancelled();
  }

  await this.process(item);
}
Client Usage
Clients that support MCP Tasks follow a refined protocol flow.

1. Initiating a Task
Clients add a task: {} parameter to the tools/call request.

JSON

{
  "method": "tools/call",
  "params": {
    "name": "heavy_audit",
    "arguments": { "level": "full" },
    "task": { "ttl": 300000 }
  }
}
Server Response (Immediate):

JSON

{
  "task": {
    "taskId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "status": "working",
    "pollInterval": 2000
  }
}
2. Monitoring Status
Clients can poll for updates using tasks/get.

JSON

{
  "method": "tasks/get",
  "params": { "taskId": "f47ac10b..." }
}
Response:

JSON

{
  "taskId": "f47ac10b...",
  "status": "working",
  "statusMessage": "Processing batch 1 of 10...",
  "lastUpdatedAt": "2024-01-01T12:00:05Z"
}
3. Retrieving Results
The tasks/result method blocks until the task reaches a terminal state (completed, failed, or cancelled).

JSON

{
  "method": "tasks/result",
  "params": { "taskId": "f47ac10b..." }
}
Complete Example: Batch Quality Audit
This example demonstrates a tool that audits multiple records, provides progress updates, and supports cancellation.

Typescript

import { ToolDecorator as Tool, z, ExecutionContext, Injectable } from '@nitrostack/core';
import { AuditService } from './audit.service.js';

@Injectable({ deps: [AuditService] })
export class AuditTools {
  constructor(private readonly auditService: AuditService) {}

  @Tool({
    name: 'run_batch_audit',
    description: 'Audits a batch of resource records for compliance.',
    taskSupport: 'optional',
    inputSchema: z.object({
      batchId: z.string(),
      checkDepth: z.enum(['shallow', 'deep']).default('shallow')
    })
  })
  async runAudit(args: any, ctx: ExecutionContext) {
    const records = await this.auditService.getBatch(args.batchId);
    const results = [];

    ctx.logger.info(`Starting audit for batch ${args.batchId}`);

    for (let i = 0; i < records.length; i++) {
      // Step 1: Check for cancellation
      ctx.task?.throwIfCancelled();

      // Step 2: Update progress
      ctx.task?.updateProgress(`Auditing record ${i + 1} of ${records.length}...`);

      // Step 3: Perform work
      const result = await this.auditService.checkRecord(records[i], args.checkDepth);
      results.push(result);
    }

    return {
      batchId: args.batchId,
      totalAudited: records.length,
      complianceScore: this.calculateScore(results)
    };
  }

  private calculateScore(results: any[]): number {
    // ... scoring logic ...
    return 95;
  }
}
Best Practices
Check for Cancellation: Always call ctx.task.throwIfCancelled() inside loops or before expensive operations.
Granular Updates: Send progress messages frequently enough to be helpful, but avoid excessive noise (e.g., every 1-2 seconds is usually ideal).
Handle Sync Fallback: If taskSupport is 'optional', ensure your tool works correctly even when ctx.task is undefined (i.e., it runs synchronously).
Use Timeouts: Servers automatically clean up tasks after their TTL (Time To Live). Default TTL is 5 minutes unless specified by the client.
Next
👋 Introduction
Error Handling Guide
Overview
Effective error handling is essential for building robust MCP servers. NitroStack provides exception filters and standardized error patterns to help you handle errors gracefully and provide meaningful feedback to AI models.

Table of Contents
Throwing Errors
Custom Error Classes
Exception Filters
Error Response Patterns
Logging Errors
Best Practices
Throwing Errors
Standard Errors
Typescript

import { ToolDecorator as Tool, ExecutionContext } from '@nitrostack/core';

export class UserTools {
  @Tool({ name: 'get_user' })
  async getUser(input: { userId: string }, ctx: ExecutionContext) {
    const user = await this.userService.findById(input.userId);

    if (!user) {
      throw new Error(`User not found: ${input.userId}`);
    }

    return user;
  }
}
Error with Context
Typescript

@Tool({ name: 'transfer_funds' })
async transferFunds(
  input: { fromAccount: string; toAccount: string; amount: number },
  ctx: ExecutionContext
) {
  const sourceAccount = await this.accountService.findById(input.fromAccount);

  if (!sourceAccount) {
    throw new Error(`Source account not found: ${input.fromAccount}`);
  }

  if (sourceAccount.balance < input.amount) {
    throw new Error(
      `Insufficient funds. Available: ${sourceAccount.balance}, Requested: ${input.amount}`
    );
  }

  return this.accountService.transfer(input);
}
Custom Error Classes
Domain-Specific Errors
Typescript

// errors/not-found.error.ts
export class NotFoundError extends Error {
  public readonly resourceType: string;
  public readonly resourceId: string;

  constructor(resourceType: string, resourceId: string) {
    super(`${resourceType} not found: ${resourceId}`);
    this.name = 'NotFoundError';
    this.resourceType = resourceType;
    this.resourceId = resourceId;
  }
}

// errors/validation.error.ts
export class ValidationError extends Error {
  public readonly field: string;
  public readonly value: unknown;
  public readonly constraint: string;

  constructor(field: string, value: unknown, constraint: string) {
    super(`Validation failed for ${field}: ${constraint}`);
    this.name = 'ValidationError';
    this.field = field;
    this.value = value;
    this.constraint = constraint;
  }
}

// errors/authorization.error.ts
export class AuthorizationError extends Error {
  public readonly requiredPermission: string;
  public readonly userId?: string;

  constructor(requiredPermission: string, userId?: string) {
    super(`Access denied. Required permission: ${requiredPermission}`);
    this.name = 'AuthorizationError';
    this.requiredPermission = requiredPermission;
    this.userId = userId;
  }
}

// errors/business-rule.error.ts
export class BusinessRuleError extends Error {
  public readonly rule: string;
  public readonly context: Record<string, unknown>;

  constructor(rule: string, message: string, context: Record<string, unknown> = {}) {
    super(message);
    this.name = 'BusinessRuleError';
    this.rule = rule;
    this.context = context;
  }
}
Using Custom Errors
Typescript

import { NotFoundError, ValidationError, BusinessRuleError } from './errors/index.js';

@Tool({ name: 'update_order' })
async updateOrder(
  input: { orderId: string; status: string },
  ctx: ExecutionContext
) {
  const order = await this.orderService.findById(input.orderId);

  if (!order) {
    throw new NotFoundError('Order', input.orderId);
  }

  const validStatuses = ['pending', 'processing', 'shipped', 'delivered'];
  if (!validStatuses.includes(input.status)) {
    throw new ValidationError(
      'status',
      input.status,
      `Must be one of: ${validStatuses.join(', ')}`
    );
  }

  if (order.status === 'delivered' && input.status !== 'delivered') {
    throw new BusinessRuleError(
      'ORDER_ALREADY_DELIVERED',
      'Cannot change status of a delivered order',
      { orderId: order.id, currentStatus: order.status }
    );
  }

  return this.orderService.updateStatus(input.orderId, input.status);
}
Exception Filters
Creating an Exception Filter
Typescript

import { ExceptionFilter, ExceptionFilterInterface, ExecutionContext } from '@nitrostack/core';

@ExceptionFilter()
export class GlobalExceptionFilter implements ExceptionFilterInterface {
  catch(exception: unknown, context: ExecutionContext): any {
    const timestamp = new Date().toISOString();
    const requestId = context.metadata?.requestId || context.requestId;

    // Log the error
    context.logger.error('Exception caught', {
      requestId,
      toolName: context.toolName,
      error: this.serializeError(exception)
    });

    // Handle specific error types
    if (exception instanceof NotFoundError) {
      return {
        error: true,
        code: 'NOT_FOUND',
        message: exception.message,
        details: {
          resourceType: exception.resourceType,
          resourceId: exception.resourceId
        },
        timestamp,
        requestId
      };
    }

    if (exception instanceof ValidationError) {
      return {
        error: true,
        code: 'VALIDATION_ERROR',
        message: exception.message,
        details: {
          field: exception.field,
          constraint: exception.constraint
        },
        timestamp,
        requestId
      };
    }

    if (exception instanceof AuthorizationError) {
      return {
        error: true,
        code: 'FORBIDDEN',
        message: 'Access denied',
        timestamp,
        requestId
      };
    }

    if (exception instanceof BusinessRuleError) {
      return {
        error: true,
        code: exception.rule,
        message: exception.message,
        details: exception.context,
        timestamp,
        requestId
      };
    }

    // Generic error handling
    return {
      error: true,
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      timestamp,
      requestId
    };
  }

  private serializeError(error: unknown): Record<string, unknown> {
    if (error instanceof Error) {
      return {
        name: error.name,
        message: error.message,
        stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
      };
    }
    return { value: String(error) };
  }
}
Using Exception Filters
Typescript

import { UseFilters } from '@nitrostack/core';
import { GlobalExceptionFilter } from './filters/global-exception.filter.js';

@Tool({ name: 'risky_operation' })
@UseFilters(GlobalExceptionFilter)
async riskyOperation(input: RiskyInput, ctx: ExecutionContext) {
  // Errors are caught and formatted by the filter
  return this.riskyService.execute(input);
}
Specialized Filters
Typescript

@ExceptionFilter()
export class DatabaseExceptionFilter implements ExceptionFilterInterface {
  catch(exception: unknown, context: ExecutionContext): any {
    if (this.isDatabaseError(exception)) {
      context.logger.error('Database error', {
        code: exception.code,
        message: exception.message
      });

      // Handle specific database errors
      if (exception.code === 'UNIQUE_VIOLATION') {
        return {
          error: true,
          code: 'DUPLICATE_ENTRY',
          message: 'A record with this value already exists'
        };
      }

      if (exception.code === 'FOREIGN_KEY_VIOLATION') {
        return {
          error: true,
          code: 'REFERENCE_ERROR',
          message: 'Referenced record does not exist'
        };
      }

      return {
        error: true,
        code: 'DATABASE_ERROR',
        message: 'A database error occurred'
      };
    }

    // Re-throw non-database errors
    throw exception;
  }

  private isDatabaseError(error: unknown): error is DatabaseError {
    return error instanceof Error && 'code' in error;
  }
}
Error Response Patterns
Standardized Error Response
Typescript

interface ErrorResponse {
  error: true;
  code: string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: string;
  requestId?: string;
}

// Example responses:

// Not found
{
  error: true,
  code: 'NOT_FOUND',
  message: 'User not found: usr_abc123',
  details: { resourceType: 'User', resourceId: 'usr_abc123' },
  timestamp: '2024-01-15T10:30:00Z',
  requestId: 'req_xyz789'
}

// Validation error
{
  error: true,
  code: 'VALIDATION_ERROR',
  message: 'Validation failed for email: Must be a valid email address',
  details: { field: 'email', constraint: 'Must be a valid email address' },
  timestamp: '2024-01-15T10:30:00Z',
  requestId: 'req_xyz789'
}

// Business rule violation
{
  error: true,
  code: 'INSUFFICIENT_FUNDS',
  message: 'Insufficient funds for transfer',
  details: { available: 100.00, requested: 150.00 },
  timestamp: '2024-01-15T10:30:00Z',
  requestId: 'req_xyz789'
}
Error Codes Enumeration
Typescript

export const ErrorCodes = {
  // Client errors (4xx equivalent)
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  CONFLICT: 'CONFLICT',
  RATE_LIMITED: 'RATE_LIMITED',

  // Business errors
  INSUFFICIENT_FUNDS: 'INSUFFICIENT_FUNDS',
  ORDER_ALREADY_SHIPPED: 'ORDER_ALREADY_SHIPPED',
  INVENTORY_EXHAUSTED: 'INVENTORY_EXHAUSTED',

  // Server errors (5xx equivalent)
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  DATABASE_ERROR: 'DATABASE_ERROR',
  EXTERNAL_SERVICE_ERROR: 'EXTERNAL_SERVICE_ERROR'
} as const;
Logging Errors
Structured Error Logging
Typescript

@Tool({ name: 'process_payment' })
async processPayment(input: PaymentInput, ctx: ExecutionContext) {
  try {
    return await this.paymentService.process(input);
  } catch (error) {
    // Log with full context
    ctx.logger.error('Payment processing failed', {
      requestId: ctx.requestId,
      userId: ctx.auth?.subject,
      amount: input.amount,
      error: {
        name: error instanceof Error ? error.name : 'Unknown',
        message: error instanceof Error ? error.message : String(error),
        stack: error instanceof Error ? error.stack : undefined
      }
    });

    // Re-throw for filter handling
    throw error;
  }
}
Error Monitoring Integration
Typescript

import { Injectable } from '@nitrostack/core';

@Injectable()
export class ErrorReporter {
  constructor(private config: ConfigService) {}

  report(error: Error, context: Record<string, unknown>): void {
    // Log locally
    console.error('Error reported:', error.message, context);

    // Send to monitoring service in production
    if (this.config.get('NODE_ENV') === 'production') {
      // Integration with error tracking services
      // e.g., Sentry, DataDog, etc.
    }
  }
}
Best Practices
1. Use Specific Error Types
Typescript

// Recommended: Specific error types
throw new NotFoundError('User', userId);
throw new ValidationError('email', email, 'Invalid format');
throw new AuthorizationError('admin:write');

// Avoid: Generic errors
throw new Error('Something went wrong');
throw new Error('Invalid');
2. Include Context in Errors
Typescript

// Recommended: Contextual information
throw new Error(
  `Failed to process order ${orderId}. Item ${itemId} is out of stock.`
);

// Avoid: Vague messages
throw new Error('Order failed');
3. Log Before Re-throwing
Typescript

// Recommended: Log with context
try {
  await this.externalService.call(input);
} catch (error) {
  ctx.logger.error('External service call failed', {
    service: 'PaymentGateway',
    input,
    error
  });
  throw error;
}

// Avoid: Silent re-throw
try {
  await this.externalService.call(input);
} catch (error) {
  throw error;  // No logging
}
4. Do Not Expose Internal Details
Typescript

// Recommended: Safe error response
return {
  error: true,
  code: 'DATABASE_ERROR',
  message: 'A database error occurred'
};

// Avoid: Exposing internals
return {
  error: true,
  message: 'FATAL: password authentication failed for user "admin"',
  stack: error.stack  // Never expose in production
};
5. Use Exception Filters Consistently
Typescript

// Recommended: Centralized handling
@ExceptionFilter()
export class GlobalExceptionFilter {
  catch(exception: unknown, context: ExecutionContext) {
    // Consistent error handling for all errors
  }
}

// Apply globally or per-handler
@UseFilters(GlobalExceptionFilter)
export class UserTools { }
6. Test Error Scenarios
Typescript

describe('UserTools', () => {
  describe('getUser', () => {
    it('should throw NotFoundError when user does not exist', async () => {
      mockUserService.findById.mockResolvedValue(null);

      await expect(tools.getUser({ userId: 'invalid' }, ctx))
        .rejects.toThrow(NotFoundError);
    });

    it('should include user ID in error message', async () => {
      mockUserService.findById.mockResolvedValue(null);

      await expect(tools.getUser({ userId: 'usr_123' }, ctx))
        .rejects.toThrow('User not found: usr_123');
    });
  });
});
Related Documentation
Middleware Guide - Error handling middleware
Interceptors Guide - Error transformation
Testing Guide - Testing error scenarios
Next
👋 Introduction
Documentation