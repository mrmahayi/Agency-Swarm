from agency_swarm.tools import BaseTool
from pydantic import Field
import pyautogui
import os
from datetime import datetime

class ScreenshotTool(BaseTool):
    """
    A tool for capturing desktop screenshots using pyautogui.
    The screenshot will be saved in the specified directory.
    """
    
    save_path: str = Field(
        default="screenshots",
        description="Directory where screenshots will be saved"
    )

    def run(self):
        """
        Takes a screenshot of the entire desktop and saves it to the specified directory.
        Returns the path to the saved screenshot.
        """
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.save_path, filename)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        return filepath

if __name__ == "__main__":
    # Test the tool
    tool = ScreenshotTool()
    result = tool.run()
    print(f"Screenshot saved to: {result}") 