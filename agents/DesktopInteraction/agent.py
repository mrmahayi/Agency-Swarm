import os
from agency_swarm import Agent
from .tools.KeyboardTool import KeyboardTool
from .tools.ClickTool import ClickTool
from .tools.ClipboardTool import ClipboardTool

class DesktopInteractionAgent(Agent):
    """Desktop Interaction Agent responsible for controlling keyboard, mouse, and clipboard interactions."""
    
    def __init__(self):
        super().__init__(
            name="DesktopInteraction",
            description="Controls keyboard, mouse, and clipboard interactions",
            instructions="./instructions.md",
            tools=[KeyboardTool, ClickTool, ClipboardTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def keyboard_action(self, action, keys=None):
        """Perform keyboard actions."""
        tool = KeyboardTool(action=action, keys=keys)
        return tool.run()
        
    def click_action(self, x=None, y=None, button="left", clicks=1):
        """Perform mouse click actions."""
        tool = ClickTool(x=x, y=y, button=button, clicks=clicks)
        return tool.run()
        
    def clipboard_action(self, action, text=None):
        """Perform clipboard actions."""
        tool = ClipboardTool(action=action, text=text)
        return tool.run()
