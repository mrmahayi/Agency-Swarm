from agency_swarm.tools import BaseTool
from pydantic import Field
import pyautogui
import time

class ClickTool(BaseTool):
    """
    A tool for clicking at specific coordinates on the desktop using pyautogui.
    Can perform left click, right click, or double click at the specified location.
    """
    
    x: int = Field(
        ...,
        description="X coordinate for the click location"
    )
    
    y: int = Field(
        ...,
        description="Y coordinate for the click location"
    )
    
    click_type: str = Field(
        default="left",
        description="Type of click to perform: 'left', 'right', or 'double'"
    )
    
    duration: float = Field(
        default=0.2,
        description="Duration of mouse movement to the target location (in seconds)"
    )

    def run(self):
        """
        Moves the mouse to the specified coordinates and performs the requested click action.
        Returns a description of the action performed.
        """
        try:
            # Move mouse to position
            pyautogui.moveTo(self.x, self.y, duration=self.duration)
            
            # Perform the click based on type
            if self.click_type == "right":
                pyautogui.rightClick()
                action = "Right clicked"
            elif self.click_type == "double":
                pyautogui.doubleClick()
                action = "Double clicked"
            else:  # default to left click
                pyautogui.click()
                action = "Left clicked"
            
            return f"{action} at coordinates ({self.x}, {self.y})"
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return f"Error performing click: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    # Move to center of screen and left click
    screen_width, screen_height = pyautogui.size()
    tool = ClickTool(x=screen_width//2, y=screen_height//2)
    result = tool.run()
    print(result)
    
    # Wait a bit and then right click
    time.sleep(1)
    tool = ClickTool(x=screen_width//2, y=screen_height//2, click_type="right")
    result = tool.run()
    print(result) 