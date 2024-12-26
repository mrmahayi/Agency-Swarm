import os
from agency_swarm import Agent
from .tools.KeyboardTool import KeyboardTool
from .tools.ClickTool import ClickTool
from .tools.ClipboardTool import ClipboardTool
from .tools.ScreenshotTool import ScreenshotTool

class DesktopInteractionAgent(Agent):
    """Desktop Interaction Agent responsible for controlling keyboard, mouse, clipboard, and screen capture interactions."""
    
    def __init__(self):
        super().__init__(
            name="DesktopInteraction",
            description="Controls keyboard, mouse, clipboard, and screen capture interactions",
            instructions="./instructions.md",
            tools=[KeyboardTool, ClickTool, ClipboardTool, ScreenshotTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def type_text(self, text):
        """Type text using keyboard."""
        return self.tools["KeyboardTool"].run({"action": "type", "text": text})
        
    def press_key(self, key):
        """Press a specific key."""
        return self.tools["KeyboardTool"].run({"action": "press", "key": key})
        
    def click_at_position(self, x, y, button="left", clicks=1):
        """Click at specific coordinates."""
        return self.tools["ClickTool"].run({"x": x, "y": y, "button": button, "clicks": clicks})
        
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        return self.tools["ClipboardTool"].run({"operation": "copy", "text": text})
        
    def paste_from_clipboard(self):
        """Paste text from clipboard."""
        return self.tools["ClipboardTool"].run({"operation": "paste"})

    def take_screenshot(self, region=None, save_path="screenshots"):
        """Take a screenshot of the screen or specified region."""
        return self.tools["ScreenshotTool"].run({"region": region, "save_path": save_path})
