import os
from agency_swarm import Agent
from .tools import AzureVisionTool, CameraTool, VisualizationTool, ScreenshotTool

class VisionAnalysisAgent(Agent):
    """Vision Analysis Agent responsible for image processing and analysis."""
    
    def __init__(self):
        super().__init__(
            name="VisionAnalysis",
            description="Processes and analyzes visual content",
            instructions="./instructions.md",
            tools=[AzureVisionTool, CameraTool, VisualizationTool, ScreenshotTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def analyze_image(self, image_path):
        """Analyze an image."""
        return self.tools["AzureVisionTool"].run({"operation": "analyze", "image_path": image_path})
        
    def capture_image(self):
        """Capture an image using the camera."""
        return self.tools["CameraTool"].run({"operation": "capture"})

    def create_visualization(self, visualization_type):
        """Create a visualization."""
        return self.tools["VisualizationTool"].run({"visualization_type": visualization_type})

    def take_screenshot(self):
        """Take a screenshot of the desktop."""
        return self.tools["ScreenshotTool"].run()
