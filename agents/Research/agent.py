import os
from agency_swarm import Agent
from .tools.TavilySearchTool import TavilySearchTool
from .tools.BrowserTool import BrowserTool
from .tools.PDFTool import PDFTool
from .tools.FileManagementTool import FileManagementTool

class ResearchAgent(Agent):
    """Research Agent responsible for gathering and analyzing information."""
    
    def __init__(self):
        super().__init__(
            name="Research",
            description="Gathers and analyzes information",
            instructions="./instructions.md",
            tools=[TavilySearchTool, BrowserTool, PDFTool, FileManagementTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def search_web(self, query, max_results=5):
        """Search the web using Tavily."""
        tool = TavilySearchTool(query=query, max_results=max_results)
        return tool.run()
        
    def browse_url(self, url, action="read"):
        """Browse a URL and perform actions."""
        tool = BrowserTool(url=url, action=action)
        return tool.run()
        
    def read_pdf(self, file_path):
        """Read and extract text from a PDF file."""
        tool = PDFTool(file_path=file_path)
        return tool.run()
        
    def manage_file(self, action, file_path, content=None):
        """Manage files (read, write, delete)."""
        tool = FileManagementTool(action=action, file_path=file_path, content=content)
        return tool.run()
