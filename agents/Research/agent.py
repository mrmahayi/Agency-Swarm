import os
from agency_swarm import Agent
from .tools import TavilySearchTool, BrowserTool, PDFTool, FileManagementTool

class ResearchAgent(Agent):
    """Research Agent responsible for information gathering and analysis."""
    
    def __init__(self):
        super().__init__(
            name="Research",
            description="Handles research tasks and information gathering",
            instructions="./instructions.md",
            tools=[TavilySearchTool, BrowserTool, PDFTool, FileManagementTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def search(self, query):
        """Perform a search query."""
        return self.tools["TavilySearchTool"].run({"query": query})
        
    def browse(self, url):
        """Browse a webpage."""
        return self.tools["BrowserTool"].run({"url": url, "action": "browse"})

    def read_pdf(self, file_path):
        """Read and extract text from a PDF file."""
        return self.tools["PDFTool"].run({"action": "read", "file_path": file_path})

    def save_file(self, content, file_path):
        """Save content to a file."""
        return self.tools["FileManagementTool"].run({"action": "save", "content": content, "file_path": file_path})
