# Agency-Swarm Backend Documentation

## Overview

The backend of the Agency-Swarm project is designed to manage a multi-agent system capable of handling complex tasks through collaboration. It is built using FastAPI and integrates with Azure OpenAI for advanced AI capabilities.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python
- **WebSocket**: websockets library
- **HTTP Client**: httpx
- **Environment Management**: python-dotenv

## Project Structure

```
backend/
├── agents/                # Agent implementations
│   ├── TaskOrchestrator/  # Task management and coordination
│   ├── VisionAnalysis/    # Image and visual processing
│   ├── DesktopInteraction/# System interaction automation
│   ├── WebAutomation/     # Web browsing and file management
│   └── Research/          # Information gathering and analysis
├── api/                   # API endpoints
│   ├── routes.py          # REST API routes
│   └── websockets.py      # WebSocket handling
├── database/              # Database interactions
│   ├── models.py          # Database models
│   └── manager.py         # Database manager
├── monitoring/            # Monitoring and metrics
│   ├── metrics.py         # Metrics collection
│   └── alerts.py          # Alerting system
├── security/              # Security configurations
│   └── auth.py            # Authentication logic
├── utils/                 # Utility functions
│   └── helpers.py         # Helper functions
└── main.py                # Main application entry point
```

## Core Components

### Agents

1. **TaskOrchestrator Agent**
   - **Location**: `agents/TaskOrchestrator/`
   - **Description**: Manages tasks and coordinates other agents.
   - **Tools**:
     - `TaskContextManager`: Task creation, updates, assignments, and dependencies.
     - `UpdateBatcher`: Message and update management between agents.
     - `SpeechTool`: Text-to-speech conversion.
     - `SpeechToTextTool`: Speech-to-text conversion.

2. **VisionAnalysis Agent**
   - **Location**: `agents/VisionAnalysis/`
   - **Description**: Processes and analyzes visual information.
   - **Tools**:
     - `AzureVisionTool`: Image analysis using Azure Vision API.
     - `CameraTool`: Camera control and image capture.

3. **DesktopInteraction Agent**
   - **Location**: `agents/DesktopInteraction/`
   - **Description**: Controls keyboard, mouse, and clipboard interactions.
   - **Tools**:
     - `KeyboardTool`: Keyboard input simulation.
     - `ClickTool`: Mouse click and movement control.
     - `ClipboardTool`: Clipboard content management.

4. **WebAutomation Agent**
   - **Location**: `agents/WebAutomation/`
   - **Description**: Automates web browser interactions and manages files.
   - **Tools**:
     - `BrowserTool`: Web browser automation and control.
     - `FileManagementTool`: File system operations.

5. **Research Agent**
   - **Location**: `agents/Research/`
   - **Description**: Gathers and analyzes information from various sources.
   - **Tools**:
     - `TavilySearchTool`: Web search functionality.
     - `BrowserTool`: Web page interaction and scraping.
     - `PDFTool`: PDF file processing.
     - `FileManagementTool`: File operations for research data.

## Communication Flows

- **TaskOrchestrator**: Entry point for communication, directing tasks to other agents.
- **Research**: Communicates with WebAutomation for data gathering.
- **VisionAnalysis**: Communicates with DesktopInteraction for visual data processing.

## Environment Setup

Required environment variables in `.env`:

```
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_GPT4O_DEPLOYMENT=gpt-4o
```

## Key Features

1. **Task Management**: Centralized task orchestration and tracking.
2. **Visual Processing**: Image analysis and camera control.
3. **System Automation**: Desktop and web interaction automation.
4. **Research Capabilities**: Information gathering and analysis.
5. **Inter-agent Communication**: Structured message passing between agents.

## Testing

Each agent has its own test suite in the `tests/agents/` directory:

- `test_task_orchestrator.py`
- `test_vision_analysis_agent.py`
- `test_desktop_interaction_agent.py`
- `test_web_automation_agent.py`
- `test_research_agent.py`

Plus agency-level tests in `tests/test_agency.py`. 