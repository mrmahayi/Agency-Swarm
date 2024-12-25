# Agency Swarm

Agency Swarm is a framework for creating collaborative AI agent swarms using Azure OpenAI. It enables the creation of specialized agents that work together to accomplish complex tasks.

## Features

- **Azure OpenAI Integration**: Built-in support for Azure OpenAI's powerful language models
- **Multi-Agent System**: Create specialized agents for different tasks
- **Tool Framework**: Extensible tool system for agent capabilities
- **Automated Testing**: Comprehensive test suite for agents and tools
- **Modern Architecture**: Clean, modular, and maintainable codebase

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/mrmahayi/Agency-Swarm.git
cd Agency-Swarm
```

2. Set up your virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Azure OpenAI:
   - Copy `.env.template` to `.env`
   - Add your Azure OpenAI credentials:
```env
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_GPT4O_DEPLOYMENT=gpt-4o
```

5. Run the tests:
```bash
python -m pytest tests/
```

## Project Structure

```
project_root/
├── main.py                 # Main entry point
├── requirements.txt        # Project dependencies
├── docs/                  # Documentation
├── tests/                 # Test suite
│   ├── agents/           # Agent tests
│   ├── tools/            # Tool tests
│   └── integration/      # Integration tests
└── agents/               # Agent implementations
    └── [agent_folders]/  # Individual agent folders
```

## Available Agents

1. **Task Orchestrator**
   - Manages task distribution and coordination
   - Handles inter-agent communication
   - Tracks task progress and analytics

2. **Research Agent**
   - Web search and information gathering
   - PDF processing and analysis
   - File management

3. **Vision Analysis Agent**
   - Camera integration
   - Image processing
   - OCR capabilities

4. **Desktop Interaction Agent**
   - Mouse and keyboard control
   - Screenshot capabilities
   - Clipboard management

5. **Web Automation Agent**
   - Browser automation
   - Web scraping
   - Form filling

## Development

### Creating a New Agent

1. Use the provided template:
```bash
agency-swarm create-agent-template --name "AgentName" --description "Agent Description"
```

2. Implement the required methods in the agent class
3. Add necessary tools in the agent's tools folder
4. Create tests in the `/tests/agents/` directory

### Adding New Tools

1. Create a new tool class inheriting from `BaseTool`
2. Implement the required methods
3. Add comprehensive tests
4. Update documentation

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific test categories:
```bash
python -m pytest tests/agents/    # Test agents
python -m pytest tests/tools/     # Test tools
python -m pytest tests/integration/ # Test integration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Azure OpenAI
- Inspired by the Agency Swarm framework
- Thanks to all contributors 