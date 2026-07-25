Starter Template
Overview
The Starter Template is a minimal NitroStack project designed for learning core concepts. It features a simple calculator with one module, demonstrating tools, resources, prompts, and widgets without authentication or database complexity.

What's Included
Calculator Module - Single feature module with all NitroStack primitives
Tools - calculate tool for arithmetic operations (add, subtract, multiply, divide)
Resources - calculator://operations listing available operations
Prompts - calculator_help for usage instructions
Widgets - Two Next.js widgets for results and operations display
No Authentication - Focus on learning without auth complexity
No Database - Pure computation example
Quick Start
Create Project
Bash

npx nitrostack@latest init my-calculator --template typescript-starter
cd my-calculator
npm run dev
The CLI automatically installs dependencies, builds widgets, and starts:

MCP Server (STDIO + HTTP on port 3002)
Studio on http://localhost:3000
Widget Dev Server on http://localhost:3001
Project Structure
src/
├── modules/
│   └── calculator/
│       ├── calculator.module.ts       # Module definition
│       ├── calculator.tools.ts        # Tool with @Tool decorator
│       ├── calculator.resources.ts    # Resource endpoint
│       └── calculator.prompts.ts      # Prompt template
├── widgets/
│   └── app/
│       ├── calculator-result/         # Result widget
│       └── calculator-operations/     # Operations list widget
├── app.module.ts                      # Root module
└── index.ts                           # Bootstrap
Features
Calculate Tool
Performs basic arithmetic with input validation:

Typescript

@Tool({
  name: 'calculate',
  description: 'Perform basic arithmetic calculations',
  inputSchema: z.object({
    operation: z.enum(['add', 'subtract', 'multiply', 'divide']),
    a: z.number(),
    b: z.number()
  }),
  examples: {
    request: { operation: 'add', a: 5, b: 3 },
    response: { result: 8, expression: '5 + 3 = 8' }
  }
})
@Widget('calculator-result')
async calculate(input: any, ctx: ExecutionContext) {
  // Implementation
}
Calculator Resource
Lists all available operations with examples:

Typescript

@Resource({
  uri: 'calculator://operations',
  name: 'Calculator Operations',
  mimeType: 'application/json'
})
@Widget('calculator-operations')
async getOperations(uri: string, ctx: ExecutionContext) {
  return { contents: [/* operations */] };
}
Help Prompt
Provides usage instructions:

Typescript

@Prompt({
  name: 'calculator_help',
  arguments: [/* args */]
})
async getHelp(args: any, ctx: ExecutionContext) {
  return { messages: [/* help messages */] };
}
Widgets
Calculator Result Widget
Gradient background with operation icon
Number breakdown display
Smooth animations
Theme-aware styling
Calculator Operations Widget
Grid layout of all operations
Color-coded by operation type
Example usage for each operation
Learning Path
This template teaches:

Module Organization - Feature module structure
Tool Creation - Using @Tool decorator with validation
Resources - Exposing data endpoints
Prompts - Creating conversation templates
Widgets - Building UI components
Examples - Providing request/response examples
Validation - Using Zod schemas
Example Usage
Basic Calculation
User: "What's 12 times 8?"
AI: Calls calculate(operation="multiply", a=12, b=8)
Result: Widget showing "12 × 8 = 96"
Get Help
User: "How do I use the calculator?"
AI: Uses calculator_help prompt
Result: Complete usage instructions
List Operations
User: "What operations are available?"
AI: Fetches calculator://operations resource
Result: Widget showing all 4 operations
Extending the Template
Add More Operations
Edit calculator.tools.ts to add new operations to the enum and implementation.

Add History Feature
Create a service to store calculations
Add a get_history tool
Create a history widget
Add More Modules
Bash

npx @nitrostack/cli generate module converter
Commands
Bash

npm run dev              # Start dev server with Studio
npm run build            # Build for production
npm start                # Run production server
npm run widget <command> # Run command in widgets directory
Next Steps
OAuth Template - Authentication patterns
Pizzaz Template - Advanced widget features
Quick Start Guide - Build your first server
Server Concepts - Module architecture
Tools Guide - Advanced patterns
UI Widgets Guide - UI development
Use Cases
Perfect starting point for:

Unit converters (temperature, currency)
Text tools (string manipulation, formatting)
Data processors (JSON, CSV, XML parsing)
Simple APIs (weather, jokes, facts)
Utilities (date/time, UUID generation)
Next
👋 Introduction
OAuth 2.1 Template
Overview
The OAuth 2.1 Template demonstrates enterprise-grade authentication with a complete flight booking system. It showcases OAuth 2.1 integration, protected tools, and interactive widgets for searching flights, viewing details, and managing bookings.

What's Included
OAuth 2.1 Authentication - Complete Auth0 integration with token management
Flight Booking Module - Search, book, and manage flight reservations
7 Protected Tools - All require authentication
7 Interactive Widgets - Rich UI for flight search, selection, and booking
Duffel API Integration - Real flight data (API key required)
Token Refresh - Automatic token renewal
Protected Resources - Flight booking guide and airline codes
Quick Start
Create Project
Bash

npx nitrostack@latest init my-flights --template typescript-oauth
cd my-flights
Configure OAuth
Copy .env.example to .env

Set up Auth0 (or your OAuth provider):

Create an application
Configure callback URLs
Get client credentials
Update .env:

Bash

RESOURCE_URI=https://your-api
AUTH_SERVER_URL=https://your-auth0-domain.auth0.com
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
AUDIENCE=https://your-api
(Optional) Add Duffel API key for real flight data:
Bash

DUFFEL_API_KEY=your_duffel_api_key
Run Development
Bash

npm run dev
Starts:

MCP Server with OAuth on HTTP (port 3002)
Studio on http://localhost:3000
Widget Dev Server on http://localhost:3001
Project Structure
src/
├── modules/
│   └── flights/
│       ├── flights.module.ts          # Module definition
│       ├── flights.tools.ts           # Flight search/booking tools
│       ├── booking.tools.ts           # Order management tools
│       ├── flights.resources.ts       # Flight resources
│       └── flights.prompts.ts         # Conversation templates
├── services/
│   └── duffel.service.ts              # Duffel API integration
├── guards/
│   └── oauth.guard.ts                 # OAuth protection
├── widgets/
│   └── app/
│       ├── flight-search-results/     # Search results grid
│       ├── flight-details/            # Flight information
│       ├── airport-search/            # Airport autocomplete
│       ├── seat-selection/            # Seat map
│       ├── order-summary/             # Booking confirmation
│       ├── payment-confirmation/      # Payment success
│       └── order-cancellation/        # Cancellation status
├── app.module.ts                      # Root module with OAuth
└── index.ts                           # Bootstrap
Features
Protected Tools
All tools require valid OAuth token:

Typescript

@UseGuards(OAuthGuard)
@Tool({
  name: 'search_flights',
  description: 'Search for flights between airports'
})
async searchFlights(input: any, ctx: ExecutionContext) {
  // Only accessible with valid token
}
Flight Search
Search flights with filters:

Origin and destination airports
Departure and return dates
Number of passengers
Cabin class (economy, business, first)
Airport Search
Autocomplete airport search with:

City and airport name matching
IATA code lookup
Country filtering
Flight Details
View comprehensive flight information:

Airline and flight numbers
Departure/arrival times
Duration and layovers
Aircraft type
Baggage allowance
Seat Selection
Interactive seat map showing:

Available seats
Seat types (window, aisle, middle)
Extra legroom seats
Occupied seats
Order Management
Create bookings (hold or payment)
View order details
Cancel orders
Get seat maps
Widgets
Flight Search Results Widget
Grid layout of available flights
Price comparison
Duration and stops display
Select flight action
Flight Details Widget
Complete itinerary
Segment breakdown
Pricing information
Booking action
Airport Search Widget
Autocomplete search
Airport details
IATA codes
Selection interface
Seat Selection Widget
Interactive seat map
Seat type indicators
Selection state
Confirmation
Order Summary Widget
Booking confirmation
Passenger details
Payment status
Order reference
OAuth Flow
User Initiates: User tries to use a protected tool
Auth Challenge: Server returns OAuth authorization URL
User Authorizes: User completes OAuth flow in browser
Token Exchange: Server exchanges code for access token
Tool Access: User can now access protected tools
Token Refresh: Automatic renewal when token expires
Configuration
OAuth Providers
Supports any OAuth 2.1 compliant provider:

Auth0
Okta
Azure AD
Google
Custom providers
Environment Variables
Bash

# OAuth Configuration
RESOURCE_URI=https://your-api
AUTH_SERVER_URL=https://provider.com
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
AUDIENCE=https://your-api
SCOPES=read,write,admin

# Duffel API (Optional)
DUFFEL_API_KEY=your_key

# Server Configuration
PORT=3002
NODE_ENV=development
Example Usage
Search Flights
User: "Find flights from NYC to LAX next week"
AI: Calls search_flights (requires auth)
Result: Widget showing available flights with prices
View Flight Details
User: "Show me details for the first flight"
AI: Calls get_flight_details
Result: Widget with complete flight information
Book Flight
User: "Book this flight for 2 passengers"
AI: Calls create_order
Result: Widget with booking confirmation
Extending the Template
Add More Airlines
Integrate additional flight APIs in duffel.service.ts.

Add Payment Processing
Integrate payment provider (Stripe, PayPal)
Add payment tools
Create payment widgets
Add User Profiles
Create user service
Add profile tools
Store booking history
Commands
Bash

npm run dev              # Start dev server with Studio
npm run build            # Build for production
npm start                # Run production server
Security
OAuth 2.1 compliant
Secure token storage
Automatic token refresh
PKCE support
Scope-based access control
Next Steps
OAuth 2.1 Guide
Authentication Overview
Guards API Reference
Starter Template - Learn the basics
Pizzaz Template - Widget features
Use Cases
Perfect for building:

Travel booking systems
E-commerce platforms
SaaS applications
Enterprise integrations
Protected API access
Next
👋 Introduction
Pizzaz Template
Overview
The Pizzaz Template showcases advanced Widget SDK features through an interactive pizza shop finder. It demonstrates theme awareness, state persistence, responsive layouts, and external integrations with Mapbox for interactive maps.

What's Included
Pizza Shop Module - Complete shop discovery system
3 Interactive Widgets - Map, list, and detail views
Widget SDK Features - Theme, state, display mode, and height management
Mapbox Integration - Interactive maps with custom markers
State Persistence - Favorites and preferences across sessions
Responsive Design - Adapts to different display modes
No Authentication - Focus on widget development
Quick Start
Create Project
Bash

npx nitrostack@latest init my-pizzaz --template typescript-pizzaz
cd my-pizzaz
Configure Mapbox (Optional)
Get free API key from Mapbox
Create .env:
Bash

NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
Note: Template works without Mapbox, but map widget will show error.

Run Development
Bash

npm run dev
Project Structure
src/
├── modules/
│   └── pizzaz/
│       ├── pizzaz.module.ts           # Module definition
│       ├── pizzaz.tools.ts            # Shop discovery tools
│       ├── pizzaz.service.ts          # Business logic
│       └── pizzaz.data.ts             # Shop data
├── widgets/
│   └── app/
│       ├── pizza-map/                 # Interactive map widget
│       ├── pizza-list/                # Grid/list view widget
│       └── pizza-shop/                # Shop detail widget
│   └── components/
│       ├── PizzaCard.tsx              # Reusable card component
│       └── CompactShopCard.tsx        # Compact card variant
└── index.ts                           # Bootstrap
Widget SDK Features
Theme Awareness
Automatic dark mode support:

Typescript

import { useTheme } from '@nitrostack/widgets';

const theme = useTheme(); // 'light' | 'dark'
const bgColor = theme === 'dark' ? '#000' : '#fff';
State Persistence
Persistent favorites and preferences:

Typescript

import { useWidgetState } from '@nitrostack/widgets';

const { state, setState } = useWidgetState<{
  favorites: string[];
  viewMode: 'grid' | 'list';
}>();

// State persists across widget reloads
setState({ ...state, favorites: [...state.favorites, shopId] });
Responsive Layouts
Height-aware layouts:

Typescript

import { useMaxHeight } from '@nitrostack/widgets';

const maxHeight = useMaxHeight();
return <div style={{ maxHeight }}>{content}</div>;
Display Mode Adaptation
Fullscreen mode detection:

Typescript

import { useDisplayMode } from '@nitrostack/widgets';

const displayMode = useDisplayMode(); // 'inline' | 'pip' | 'fullscreen'
const showSidebar = displayMode === 'fullscreen';
External Links
Open URLs in browser:

Typescript

import { useWidgetSDK } from '@nitrostack/widgets';

const { openExternal } = useWidgetSDK();
openExternal('https://example.com');
Widgets
Pizza Map Widget
Interactive Mapbox map featuring:

Custom shop markers
Shop sidebar with quick selection
Fullscreen mode support
Persistent favorites
Theme-aware map styles (light/dark)
Pizza List Widget
Filterable shop list with:

Grid/list view toggle
Sorting by rating, name, or price
Favorites tracking
Responsive layout
Filter panel
Pizza Shop Widget
Detailed shop information:

Hero image with overlay
Contact actions (call, directions, website)
Specialties showcase
Related shops recommendations
External link handling
Tools
show_pizza_map
Display shops on interactive map:

All shops with markers
Sidebar navigation
Fullscreen recommended
show_pizza_list
Show filterable list:

Grid or list view
Sort and filter options
Favorites management
show_pizza_shop
Display shop details:

Complete information
Contact actions
Related recommendations
Customization
Adding Shops
Edit src/modules/pizzaz/pizzaz.data.ts:

Typescript

export const PIZZA_SHOPS: PizzaShop[] = [
  {
    id: 'my-shop',
    name: 'My Pizza Shop',
    description: 'Amazing pizza!',
    address: '123 Main St, City, State 12345',
    coords: [-122.4194, 37.7749], // [lng, lat]
    rating: 4.5,
    reviews: 100,
    priceLevel: 2,
    cuisine: ['Italian', 'Pizza'],
    hours: { open: '11:00 AM', close: '10:00 PM' },
    phone: '(555) 123-4567',
    website: 'https://example.com',
    image: 'https://images.unsplash.com/photo-...',
    specialties: ['Margherita', 'Pepperoni'],
    openNow: true,
  }
];
Changing Map Style
Edit src/widgets/app/pizza-map/page.tsx:

Typescript

style: isDark 
  ? 'mapbox://styles/mapbox/dark-v11'
  : 'mapbox://styles/mapbox/streets-v12'
Adding Filters
Edit src/modules/pizzaz/pizzaz.service.ts to add filter options.

Example Usage
View Map
User: "Show me pizza shops on a map"
AI: Calls show_pizza_map
Result: Interactive map with all shops
List Shops
User: "List all pizza shops"
AI: Calls show_pizza_list
Result: Grid view with sorting and filtering
Shop Details
User: "Show me details for Tony's Pizza"
AI: Calls show_pizza_shop
Result: Complete shop information with actions
Learning Objectives
This template demonstrates:

Widget SDK - All major SDK features
Theme Integration - Dark mode support
State Management - Persistent user preferences
Responsive Design - Display mode adaptation
External APIs - Mapbox integration
Component Reuse - Shared components
User Interactions - Favorites, sorting, filtering
Commands
Bash

npm run dev              # Start dev server with Studio
npm run build            # Build for production
npm start                # Run production server
npm run widget dev       # Widget dev server only
Deployment
Build Widgets
Bash

cd src/widgets && npm run build
Widget HTML files will be in src/widgets/out/.

ChatGPT Deployment
Widgets work identically in OpenAI ChatGPT with zero code changes.

Next Steps
Widget SDK Reference
UI Widgets Guide
File Upload Guide
Starter Template - Learn the basics
OAuth Template - Authentication
Use Cases
Perfect for building:

Location-based services
Shop/restaurant finders
Interactive maps
Filterable catalogs
Review systems
Next
👋 Introduction
