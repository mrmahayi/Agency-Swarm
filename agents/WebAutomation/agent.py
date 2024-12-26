import os
from agency_swarm import Agent
from .tools import BrowserTool, FileManagementTool

class WebAutomationAgent(Agent):
    """Web Automation Agent responsible for browser interactions and web tasks."""
    
    def __init__(self):
        super().__init__(
            name="WebAutomation",
            description="Handles web automation tasks and browser interactions",
            instructions="./instructions.md",
            tools=[BrowserTool, FileManagementTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def navigate_to(self, url):
        """Navigate to a URL."""
        return self.tools["BrowserTool"].run({"action": "navigate", "url": url})
        
    def click_element(self, selector):
        """Click an element on the page."""
        return self.tools["BrowserTool"].run({"action": "click", "selector": selector})

    def download_file(self, url, save_path):
        """Download a file from a URL."""
        return self.tools["FileManagementTool"].run({"action": "download", "url": url, "save_path": save_path})

    def upload_file(self, file_path, selector):
        """Upload a file using a file input element."""
        return self.tools["FileManagementTool"].run({"action": "upload", "file_path": file_path, "selector": selector})
