from agency_swarm.tools import BaseTool
from pydantic import Field
import pyautogui
import random
import time

class KeyboardTool(BaseTool):
    """
    A tool for simulating human-like keyboard input using pyautogui.
    Can type text with variable speed and natural delays, press individual keys,
    or execute key combinations.
    """
    
    text: str = Field(
        default="",
        description="Text to type or key(s) to press (e.g., 'Hello' or 'enter' or 'ctrl+c')"
    )
    
    action: str = Field(
        default="type",
        description="Action to perform: 'type' for typing text, 'press' for pressing keys, 'hotkey' for key combinations"
    )
    
    typing_speed: tuple = Field(
        default=(0.08, 0.15),
        description="Range for random delay between keystrokes in seconds (min, max)"
    )
    
    pause_range: tuple = Field(
        default=(0.2, 0.5),
        description="Range for random pauses between words in seconds (min, max)"
    )

    def _random_delay(self, min_delay, max_delay):
        """Add a random delay within the specified range"""
        time.sleep(random.uniform(min_delay, max_delay))

    def _type_human_like(self, text):
        """Type text with human-like variations in speed"""
        words = text.split()
        
        for i, word in enumerate(words):
            # Type each character with random delay
            for char in word:
                pyautogui.write(char)
                self._random_delay(*self.typing_speed)
            
            # Add space after word (except for last word)
            if i < len(words) - 1:
                pyautogui.press('space')
                # Longer pause between words
                self._random_delay(*self.pause_range)

    def run(self):
        """
        Executes the keyboard action based on the specified parameters.
        Returns a description of the action performed.
        """
        try:
            # Fail-safe enabled by default in pyautogui
            if self.action == "type":
                if not self.text:
                    return "Error: No text provided for typing"
                self._type_human_like(self.text)
                return f"Typed text: '{self.text}'"
                
            elif self.action == "press":
                if not self.text:
                    return "Error: No key specified for pressing"
                pyautogui.press(self.text)
                return f"Pressed key: {self.text}"
                
            elif self.action == "hotkey":
                if not self.text:
                    return "Error: No key combination specified"
                # Split the combination and pass as separate arguments
                keys = self.text.lower().split('+')
                pyautogui.hotkey(*keys)
                return f"Executed hotkey: {self.text}"
            
            else:
                return f"Error: Invalid action '{self.action}'"
                
        except Exception as e:
            return f"Error performing keyboard action: {str(e)}"

if __name__ == "__main__":
    # Test typing
    print("Testing typing...")
    tool = KeyboardTool(
        text="Hello, this is a test of human-like typing!",
        action="type"
    )
    result = tool.run()
    print(result)
    
    # Test key press
    time.sleep(1)
    print("\nTesting key press...")
    tool = KeyboardTool(text="enter", action="press")
    result = tool.run()
    print(result)
    
    # Test hotkey
    time.sleep(1)
    print("\nTesting hotkey...")
    tool = KeyboardTool(text="ctrl+a", action="hotkey")
    result = tool.run()
    print(result) 