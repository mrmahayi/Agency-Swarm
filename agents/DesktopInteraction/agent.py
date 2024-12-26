import os
from agency_swarm import Agent
from .tools import ClipboardTool, ClickTool, KeyboardTool

class DesktopInteractionAgent(Agent):
    """Desktop Interaction Agent responsible for system automation tasks."""
    
    def __init__(self):
        super().__init__(
            name="DesktopInteraction",
            description="Manages desktop automation and system interactions",
            instructions="./instructions.md",
            tools=[ClipboardTool, ClickTool, KeyboardTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        return self.tools["ClipboardTool"].run({"action": "copy", "text": text})
        
    def click_at_position(self, x, y):
        """Click at a specific position."""
        return self.tools["ClickTool"].run({"action": "click", "x": x, "y": y})

    def type_text(self, text):
        """Type text using keyboard."""
        return self.tools["KeyboardTool"].run({"action": "type", "text": text})

    def press_key(self, key):
        """Press a specific key."""
        return self.tools["KeyboardTool"].run({"action": "press", "key": key})
