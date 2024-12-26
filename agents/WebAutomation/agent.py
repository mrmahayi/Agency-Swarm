import os
from agency_swarm import Agent
from .tools.BrowserTool import BrowserTool
from .tools.FileManagementTool import FileManagementTool

class WebAutomationAgent(Agent):
    """Web Automation Agent responsible for browser automation and file management."""
    
    def __init__(self):
        super().__init__(
            name="WebAutomation",
            description="Automates web browser interactions and manages files",
            instructions="./instructions.md",
            tools=[BrowserTool, FileManagementTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def browse(self, url, action="navigate"):
        """Perform browser actions."""
        tool = BrowserTool(url=url, action=action)
        return tool.run()
        
    def manage_file(self, action, file_path, content=None):
        """Manage files (read, write, delete)."""
        tool = FileManagementTool(action=action, file_path=file_path, content=content)
        return tool.run()
