# Agency-Swarm Project Reference

## IMPORTANT NOTE - AGENCY SWARM STRUCTURE
This project MUST follow the Agency Swarm framework structure while maintaining its functionality:

1. Required Structure:
   ```
   project_root/
   ├── main.py (renamed from agency.py)
   ├── requirements.txt
   ├── .env
   ├── .gitignore
   ├── README.md
   └── agents/
       ├── __init__.py
       └── [agent_folders]/
           ├── __init__.py
           ├── agent.py
           ├── instructions.md
           └── tools/
               ├── __init__.py
               └── [agent_tools].py
   ```

2. Tool Implementation Rules:
   - Each tool must inherit from `BaseTool`
   - Include proper docstrings
   - Define fields using pydantic
   - Implement the `run` method

3. Data Management:
   - Tools should handle their own data persistence
   - Avoid creating separate data directories
   - Use tool-specific storage methods

4. Current Refactoring Needs:
   - Rename `agency.py` to `main.py`
   - Move global tools into respective agent folders
   - Integrate infrastructure features into agent tools
   - Clean up root directory

## IMPORTANT NOTE - EXISTING SETUP
This project already has a complete setup with all necessary agents and tools. Before creating any new components:
1. Check the existing structure in `/agents` and `/tools` directories
2. Review the existing implementations
3. Modify existing components rather than creating duplicates
4. Follow the established patterns and conventions

## Project Overview
This is an advanced AI agent system built using the Agency-Swarm framework, designed to handle complex tasks through multiple specialized agents working in collaboration.

## Environment Setup
Required environment variables (.env):
```
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_GPT4O_DEPLOYMENT=gpt-4o
```

## Project Structure

### Core Components
- `agency.py` - Main agency configuration and initialization
- `config.py` - Configuration settings
- `requirements.txt` - Project dependencies
- `agency_manifesto.md` - Shared instructions for all agents
- `agency_data.db` - Database file
- `start_agency.sh` - Startup script

### Key Directories
1. `/agents` - Contains all agent implementations
   - TaskOrchestrator/
   - Research/
   - WebAutomation/
   - VisionAnalysis/
   - DesktopInteraction/

2. `/database` - Database related code
3. `/monitoring` - Monitoring and metrics
4. `/security` - Security and authentication
5. `/utils` - Utility functions
6. `/tests` - Test suite
7. `/backups` - Backup files
8. `/visualizations` - Visualization outputs
9. `/tools` - Global tools available to all agents

### Agent Structure
Each agent directory follows this structure:
```
agent_name/
├── __init__.py
├── agent_name.py
├── instructions.md
└── tools/
    └── [agent specific tools]
```

## Available Tools

### Global Tools
1. **Task Management**
   - TaskManagementTool.py
   - TaskAnalyticsTool.py
   - MessageAnalyticsTool.py

2. **Communication & Browser**
   - CommunicationTool.py
   - TavilySearchTool.py
   - BrowserTool.py

3. **Document & File Handling**
   - PDFTool.py
   - FileManagementTool.py
   - VisualizationTool.py

4. **Vision & Media**
   - AzureVisionTool.py
   - CameraTool.py
   - ScreenshotTool.py

5. **System Interaction**
   - ClipboardTool.py
   - ClickTool.py
   - KeyboardTool.py

6. **Speech & Audio**
   - SpeechToTextTool.py
   - SpeechTool.py

7. **Database**
   - database_manager.py

### Agent-Specific Tools

#### TaskOrchestrator
- TaskContextManager.py
- CommunicationTool.py
- UpdateBatcher.py

## Dependencies

### Core Dependencies
- agency-swarm (v0.4.2)
- openai (≥1.55.3)
- python-dotenv (1.0.1)
- httpx (0.26.0)

### Document Processing
- pdfkit (1.0.0)
- PyPDF2 (3.0.1)
- wkhtmltopdf (0.2)

### Web & Automation
- playwright (1.41.2)

### Data & Visualization
- plotly (5.24.1)
- pandas (2.2.3)
- numpy (2.2.1)

### Speech & Vision
- azure-cognitiveservices-speech (1.35.0)

### Monitoring & Logging
- python-logging (0.4.9.6)
- prometheus-client (0.17.1)

### Testing
- pytest (7.4.3)
- pytest-cov (4.1.0)

### Server
- gunicorn (21.2.0)

### Additional Dependencies
- pyautogui (for desktop automation)
- pillow (for image processing)
- opencv-python (for camera operations)
- pyperclip (for clipboard operations)
- keyboard (for keyboard control)
- mouse (for mouse control)

## Available Agents

### 1. TaskOrchestrator
- Main orchestrator agent
- Manages task distribution and coordination
- Entry point for user communication
- Custom tools for task context and updates

### 2. Research Agent
- Handles research-related tasks
- Information gathering and analysis
- Uses TavilySearchTool and BrowserTool

### 3. WebAutomation Agent
- Web scraping and automation
- Browser interaction tasks
- Utilizes Playwright for automation

### 4. VisionAnalysis Agent
- Image processing and analysis
- Visual data interpretation
- Uses AzureVisionTool and CameraTool

### 5. DesktopInteraction Agent
- Desktop automation tasks
- System interaction capabilities
- Uses ClickTool, KeyboardTool, and ScreenshotTool

## Infrastructure Features
1. **Monitoring**
   - Prometheus metrics integration
   - Health monitoring for agents
   - API request tracking

2. **Security**
   - Token-based authentication
   - Rate limiting
   - Security manager implementation

3. **Database**
   - SQLite database integration
   - Connection management
   - Data persistence

4. **Backup System**
   - Automated backup creation
   - Backup management utilities

5. **Logging**
   - Comprehensive logging configuration
   - Error tracking and alerting

## Starting the Project
1. Ensure all environment variables are set in `.env`
2. Install dependencies: `pip install -r requirements.txt`
3. Install additional system dependencies:
   ```bash
   # For PDF processing
   apt-get install wkhtmltopdf

   # For desktop automation
   apt-get install python3-tk python3-dev
   
   # For camera operations
   apt-get install libopencv-dev
   ```
4. Run the agency: `python agency.py` or `./start_agency.sh`

## Development Guidelines
1. All new agents should follow the established directory structure
2. Add new dependencies to requirements.txt
3. Update tests for new functionality
4. Follow the monitoring and logging patterns
5. Implement proper error handling and rate limiting
6. Use the backup system for critical operations

## Testing
- Run tests using pytest: `pytest tests/`
- Test coverage tracking enabled
- CI/CD integration via GitHub Actions

## Monitoring and Maintenance
- Monitor agent health via Prometheus metrics
- Check logs for errors and warnings
- Regular backup verification
- API rate limit monitoring 

## Complete Project Structure
```
Agency-Swarm/
├── .env                        # Environment variables
├── .env.template              # Template for environment variables
├── .gitignore                 # Git ignore rules
├── __init__.py               # Package initialization
├── agency.py                 # Main agency file
├── agency_data.db            # SQLite database
├── agency_manifesto.md       # Shared instructions for agents
├── assistant.txt             # Assistant configuration
├── best_camera_settings.json # Camera settings
├── camera_config.json        # Camera configuration
├── config.py                 # Configuration settings
├── Dockerfile                # Docker configuration
├── env_example.txt          # Example environment file
├── maestro.txt              # Maestro configuration
├── project_plan.md          # Project planning document
├── project_reference.md     # This reference document
├── requirements.txt         # Python dependencies
├── settings.json            # Project settings
├── start_agency.sh         # Startup script
├── test.pdf                # Test PDF file
├── test_screenshot.png     # Test screenshot
├── wkhtmltopdf.exe        # PDF generation binary

├── .github/                # GitHub configuration
│   └── workflows/         # GitHub Actions workflows

├── .venv/                 # Virtual environment (not tracked)

├── agents/                # Agent implementations
│   ├── TaskOrchestrator/
│   │   ├── __init__.py
│   │   ├── task_orchestrator_agent.py
│   │   ├── instructions.md
│   │   └── tools/
│   │       ├── TaskContextManager.py
│   │       ├── CommunicationTool.py
│   │       └── UpdateBatcher.py
│   ├── Research/
│   ├── WebAutomation/
│   ├── VisionAnalysis/
│   └── DesktopInteraction/

├── backups/              # Backup files directory

├── camera_captures/      # Camera capture storage
├── camera_tests/        # Camera test files

├── data/                # Data storage directory

├── database/           # Database related code
│   ├── __init__.py
│   ├── db.py
│   └── models/

├── logs/              # Log files directory

├── messages/          # Message storage

├── monitoring/        # Monitoring configuration
│   ├── __init__.py
│   ├── metrics.py
│   └── alerts.py

├── pdf_images/        # PDF-related images

├── screenshots/       # Screenshot storage

├── security/         # Security configuration
│   ├── __init__.py
│   └── auth.py

├── task_contexts/    # Task context storage

├── temp/            # Temporary files

├── tests/           # Test suite
│   ├── __init__.py
│   └── test_*.py

├── tools/           # Global tools
│   ├── __init__.py
│   ├── TaskManagementTool.py
│   ├── TaskAnalyticsTool.py
│   ├── MessageAnalyticsTool.py
│   ├── CommunicationTool.py
│   ├── TavilySearchTool.py
│   ├── BrowserTool.py
│   ├── PDFTool.py
│   ├── FileManagementTool.py
│   ├── VisualizationTool.py
│   ├── AzureVisionTool.py
│   ├── CameraTool.py
│   ├── ScreenshotTool.py
│   ├── ClipboardTool.py
│   ├── ClickTool.py
│   ├── KeyboardTool.py
│   ├── SpeechToTextTool.py
│   ├── SpeechTool.py
│   ├── database_manager.py
│   └── ExampleTool.py

├── updates/         # Update storage

├── utils/          # Utility functions
│   ├── __init__.py
│   ├── rate_limiter.py
│   └── backup.py

└── visualizations/ # Visualization outputs
``` 

# Project Structure

The project follows the Agency Swarm framework structure:

## Core Directories

### /agency
- `main.py` - Main entry point for the agency
- `agency_manifesto.md` - Shared instructions for all agents
- `config.py` - Configuration settings

### /agents
Each agent has its own directory with the following structure:
- `agent.py` - Agent class definition
- `instructions.md` - Agent-specific instructions
- `/tools` - Agent-specific tools
  - Tool implementation files
  - `__init__.py`

Current agents:
1. TaskOrchestrator
   - Tools: TaskContextManager, CommunicationTool, UpdateBatcher, TaskManagementTool, TaskAnalyticsTool, MessageAnalyticsTool
2. Research
   - Tools: TavilySearchTool, BrowserTool, PDFTool, FileManagementTool
3. WebAutomation
   - Tools: BrowserTool, FileManagementTool
4. VisionAnalysis
   - Tools: AzureVisionTool, CameraTool, VisualizationTool, ScreenshotTool, SpeechTool, SpeechToTextTool
5. DesktopInteraction
   - Tools: ClipboardTool, ClickTool, KeyboardTool

### /data
- Contains persistent data storage (e.g. agency.db)

### /docs
- Documentation files
- `project_reference.md` - This file
- `swarm-docs.md` - Additional documentation

### /tests
- Test files for various components

### Root Directory Files
- `.env` - Environment variables
- `requirements.txt` - Python dependencies

## Data Storage
- Persistent data is stored in `/data/agency.db`
- Temporary files are stored in `.agency/` hidden directory

## Important Notes

1. Agency Swarm Structure Guidelines:
   - Each agent must have its own directory under `/agents`
   - All tools must be in the agent's `/tools` directory
   - Each agent must have `agent.py` and `instructions.md`
   - Main agency code must be in `/agency/main.py`

2. Tool Implementation Rules:
   - Tools should be self-contained in their respective agent directories
   - Tools should follow the BaseTool pattern
   - Tools should handle their own data storage needs

3. Data Management:
   - Use SQLite database in `/data` for persistent storage
   - Use `.agency/` for temporary files
   - Clean up temporary files regularly

4. Testing:
   - Keep all tests in `/tests` directory
   - Each major component should have corresponding tests

5. Documentation:
   - Keep all documentation in `/docs`
   - Update this reference when making structural changes

## Recyclebin
The `/Recyclebin` directory contains files and directories that were part of the old structure and are kept for reference. These include:
- Configuration files
- Utility scripts
- Old monitoring and database implementations
- Test files and backups

These files can be safely removed once their functionality has been properly integrated into the new structure.