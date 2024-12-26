from agency_swarm.tools import BaseTool
from pydantic import Field
import pyautogui
import os
from datetime import datetime

class ScreenshotTool(BaseTool):
    """
    Tool for capturing screenshots of the entire screen or specific regions.
    Uses pyautogui to take screenshots and saves them to a specified directory.
    """
    
    region: tuple = Field(
        default=None,
        description="Optional tuple of (left, top, width, height) for capturing a specific region. None for full screen."
    )
    
    save_path: str = Field(
        default="screenshots",
        description="Directory path where screenshots will be saved."
    )

    def run(self):
        """Take a screenshot and save it to the specified directory."""
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.save_path, filename)
        
        try:
            # Take screenshot
            if self.region:
                screenshot = pyautogui.screenshot(region=self.region)
            else:
                screenshot = pyautogui.screenshot()
                
            # Save screenshot
            screenshot.save(filepath)
            return f"Screenshot saved successfully to {filepath}"
            
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    tool = ScreenshotTool()
    print(tool.run()) 