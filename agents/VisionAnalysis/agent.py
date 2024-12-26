import os
from agency_swarm import Agent
from .tools.AzureVisionTool import AzureVisionTool
from .tools.CameraTool import CameraTool

class VisionAnalysisAgent(Agent):
    """Vision Analysis Agent responsible for analyzing images and visual data."""
    
    def __init__(self):
        super().__init__(
            name="VisionAnalysis",
            description="Analyzes images and visual data",
            instructions="./instructions.md",
            tools=[AzureVisionTool, CameraTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def analyze_image(self, image_path):
        """Analyze an image."""
        tool = AzureVisionTool(image_path=image_path)
        return tool.run()
        
    def capture_image(self, camera_id=0, save_path=None):
        """Capture an image using the camera."""
        tool = CameraTool(camera_id=camera_id, save_path=save_path)
        return tool.run()
