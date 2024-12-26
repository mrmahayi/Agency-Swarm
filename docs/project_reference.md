# Agency-Swarm Project Reference

## Project Overview
This is an advanced AI agent system with a modern React frontend, built using the Agency-Swarm framework and designed to handle complex tasks through multiple specialized agents working in collaboration.

## Environment Setup

### Backend Environment (.env)
```
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_GPT4O_DEPLOYMENT=gpt-4o
```

### Frontend Environment (.env)
```
VITE_API_URL=your_backend_url
VITE_WS_URL=your_websocket_url
```

## Project Structure

```
Agency-Swarm/
├── frontend/                # Frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── agents/    # Agent-specific components
│   │   │   ├── results/   # Result display components
│   │   │   ├── AgentCard.tsx
│   │   │   ├── CommandInput.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Logo.tsx
│   │   │   ├── ResultsDisplay.tsx
│   │   │   └── ThemeToggle.tsx
│   │   ├── data/          # Data models and constants
│   │   ├── types/         # TypeScript definitions
│   │   ├── utils/         # Utility functions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/            # Static assets
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/               # Backend application
│   ├── agents/           # Agent implementations
│   │   ├── TaskOrchestrator/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── instructions.md
│   │   │   └── tools/
│   │   ├── Research/
│   │   ├── WebAutomation/
│   │   ├── VisionAnalysis/
│   │   └── DesktopInteraction/
│   │
│   ├── api/              # API endpoints
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── websockets.py
│   │
│   ├── database/         # Database related code
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── manager.py
│   │
│   ├── monitoring/       # Monitoring configuration
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   └── alerts.py
│   │
│   ├── security/        # Security configuration
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   ├── utils/          # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py
│   │
│   └── main.py         # Main application entry
│
├── tests/              # Test suite
│   ├── frontend/      # Frontend tests
│   │   ├── components/
│   │   └── integration/
│   │
│   ├── backend/       # Backend tests
│   │   ├── agents/
│   │   ├── tools/
│   │   └── integration/
│   │
│   └── e2e/          # End-to-end tests
│
├── docs/             # Documentation
│   ├── frontend/
│   ├── backend/
│   └── api/
│
└── docker/          # Docker configuration
    ├── frontend/
    └── backend/
```

## Frontend Components

### Core Components
1. **AgentCard**
   - Displays agent status and controls
   - Real-time updates via WebSocket
   - Action buttons for agent control

2. **CommandInput**
   - Natural language command interface
   - Command history and suggestions
   - Auto-complete functionality

3. **ResultsDisplay**
   - Multi-format result visualization
   - Support for text, images, and web content
   - Export capabilities

4. **ThemeToggle**
   - Light/dark mode switching
   - Theme persistence
   - System preference detection

### State Management
- React Context for global state
- Local state for component-specific data
- WebSocket for real-time updates

## Backend Components

### Core Agents

1. **TaskOrchestrator**
   - Main orchestrator agent
   - Task distribution and coordination
   - Communication management

2. **Research Agent**
   - Information gathering
   - Web search capabilities
   - Data analysis

3. **WebAutomation Agent**
   - Browser automation
   - Web scraping
   - Form interaction

4. **VisionAnalysis Agent**
   - Image processing
   - OCR capabilities
   - Visual analysis

5. **DesktopInteraction Agent**
   - System automation
   - File operations
   - UI interaction

### Available Tools

1. **Vision & Media**
   - AzureVisionTool
   - CameraTool
   - ScreenshotTool

2. **System Interaction**
   - ClipboardTool
   - ClickTool
   - KeyboardTool

3. **Speech & Audio**
   - SpeechToTextTool
   - TextToSpeechTool

4. **Browser & Research**
   - BrowserTool
   - TavilySearchTool

## API Integration

### REST Endpoints
```
POST /api/command       # Submit new command
GET  /api/agents        # Get agent status
GET  /api/results       # Get task results
POST /api/upload        # Upload files
```

### WebSocket Events
```
agent_status    # Real-time agent status updates
task_progress   # Task progress notifications
command_result  # Command execution results
error_event     # Error notifications
```

## Dependencies

### Frontend Dependencies
```json
{
  "dependencies": {
    // UI Components & Styling
    "@headlessui/react": "^1.7.18",    // Accessible UI components
    "@heroicons/react": "^2.1.1",      // Icon set
    "@tailwindcss/forms": "^0.5.7",    // Form styling
    "framer-motion": "^10.18.0",       // Animations
    "tailwindcss-animate": "^1.0.7",   // Animation utilities

    // State Management & Data Fetching
    "react-query": "^3.39.3",          // Server state management
    "zustand": "^4.4.7",               // Client state management
    "socket.io-client": "^4.7.4",      // WebSocket client
    "axios": "^1.6.5",                 // HTTP client

    // Forms & Validation
    "react-hook-form": "^7.49.3",      // Form handling
    "zod": "^3.22.4",                  // Schema validation

    // Routing & Navigation
    "react-router-dom": "^6.21.2",     // Client-side routing

    // Utilities
    "date-fns": "^3.2.0",             // Date manipulation
    "clsx": "^2.1.0",                 // Class utilities
    "tailwind-merge": "^2.2.0",       // Tailwind class merging
    "react-error-boundary": "^4.0.12", // Error handling
    "react-hot-toast": "^2.4.1"       // Toast notifications
  }
}
```

### Backend Dependencies
```
agency-swarm==0.4.2
openai>=1.55.3
python-dotenv==1.0.1
httpx==0.26.0
fastapi==0.109.0
websockets==12.0
```

## Development Setup

### Frontend Setup
   ```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python main.py
```

## Testing

### Frontend Testing
```bash
cd frontend
npm run test        # Unit tests
npm run test:e2e    # E2E tests
```

### Backend Testing
```bash
cd backend
pytest tests/       # All tests
pytest tests/agents # Agent tests only
```

## Security Considerations

1. **Authentication**
   - JWT-based authentication
   - API key management
   - Session handling

2. **Data Protection**
   - Input sanitization
   - XSS prevention
   - CSRF protection

3. **API Security**
   - Rate limiting
   - Request validation
   - Error handling

## Deployment

### Frontend Deployment
- Build optimization
- Asset compression
- CDN integration
- Docker containerization

### Backend Deployment
- Environment configuration
- Database setup
- WebSocket setup
- Docker containerization

## Monitoring

1. **Frontend Monitoring**
   - Performance metrics
   - Error tracking
   - User analytics

2. **Backend Monitoring**
   - Agent status
   - System resources
   - API metrics
   - Error logging

## Documentation

### API Documentation
- OpenAPI/Swagger documentation
- WebSocket event documentation
- Authentication flows
- Error codes

### Component Documentation
- Component props
- State management
- Event handling
- Styling guide

## Best Practices

### Frontend Best Practices
1. Use TypeScript for type safety
2. Follow React hooks guidelines
3. Implement proper error boundaries
4. Optimize bundle size
5. Follow accessibility guidelines

### Backend Best Practices
1. Follow Agency Swarm patterns
2. Implement proper logging
3. Handle errors gracefully
4. Document API endpoints
5. Maintain test coverage

## Maintenance

### Regular Tasks
1. Dependency updates
2. Security patches
3. Performance monitoring
4. Documentation updates

### Backup Procedures
1. Database backups
2. Configuration backups
3. User data protection
4. Version control

## Frontend Stack

### Core Technologies
1. **Framework & UI**
   - React 18 with TypeScript
   - TailwindCSS for styling
   - HeadlessUI for accessible components
   - Framer Motion for animations
   - HeroIcons for iconography

2. **State Management & Data Fetching**
   - Zustand for global state
   - React Query for server state
   - Socket.IO for real-time updates
   - React Hook Form for form management
   - Zod for schema validation

3. **Development Tools**
   - Vite for build tooling
   - TypeScript for type safety
   - ESLint & Prettier for code quality
   - Vitest for unit testing
   - Cypress for E2E testing

### Frontend Dependencies

```json
{
  "dependencies": {
    // UI Components & Styling
    "@headlessui/react": "^1.7.18",    // Accessible UI components
    "@heroicons/react": "^2.1.1",      // Icon set
    "@tailwindcss/forms": "^0.5.7",    // Form styling
    "framer-motion": "^10.18.0",       // Animations
    "tailwindcss-animate": "^1.0.7",   // Animation utilities

    // State Management & Data Fetching
    "react-query": "^3.39.3",          // Server state management
    "zustand": "^4.4.7",               // Client state management
    "socket.io-client": "^4.7.4",      // WebSocket client
    "axios": "^1.6.5",                 // HTTP client

    // Forms & Validation
    "react-hook-form": "^7.49.3",      // Form handling
    "zod": "^3.22.4",                  // Schema validation

    // Routing & Navigation
    "react-router-dom": "^6.21.2",     // Client-side routing

    // Utilities
    "date-fns": "^3.2.0",             // Date manipulation
    "clsx": "^2.1.0",                 // Class utilities
    "tailwind-merge": "^2.2.0",       // Tailwind class merging
    "react-error-boundary": "^4.0.12", // Error handling
    "react-hot-toast": "^2.4.1"       // Toast notifications
  }
}
```

### Development Scripts
```bash
# Development
npm run dev          # Start development server

# Building
npm run build        # Production build
npm run preview      # Preview production build

# Testing
npm run test         # Run tests in watch mode
npm run test:unit    # Run unit tests
npm run test:e2e     # Run end-to-end tests
npm run test:coverage # Run tests with coverage

# Linting
npm run lint         # Lint code
```

### Frontend Features

1. **Component Architecture**
   - Functional components with hooks
   - TypeScript for type safety
   - Modular and reusable design
   - Accessible by default (ARIA)

2. **State Management**
   - Zustand for simple global state
   - React Query for server cache
   - Context for theme/auth
   - Local state with useState

3. **Real-time Updates**
   - WebSocket integration
   - Live agent status
   - Task progress tracking
   - Instant notifications

4. **Form Handling**
   - React Hook Form integration
   - Zod schema validation
   - Error handling
   - Accessibility features

5. **Styling System**
   - TailwindCSS utilities
   - Dark/light theme
   - Responsive design
   - Custom animations

6. **Testing Strategy**
   - Unit tests with Vitest
   - Component testing with Testing Library
   - E2E tests with Cypress
   - Coverage reporting

### Development Workflow

1. **Setup**
   ```bash
   git clone <repository>
   cd frontend
   npm install
   ```

2. **Development**
   ```bash
   # Start development server
   npm run dev

   # Run tests in watch mode
   npm run test

   # Lint code
   npm run lint
   ```

3. **Production**
   ```bash
   # Build for production
   npm run build

   # Preview production build
   npm run preview
   ```

### Best Practices

1. **Component Development**
   - Use TypeScript for all components
   - Follow React hooks guidelines
   - Implement error boundaries
   - Maintain accessibility

2. **State Management**
   - Use Zustand for global state
   - React Query for API data
   - Local state when possible
   - Context for theme/auth

3. **Testing**
   - Write tests for all components
   - Maintain high coverage
   - Test user interactions
   - Mock external services

4. **Performance**
   - Lazy load components
   - Optimize images
   - Minimize bundle size
   - Cache API responses