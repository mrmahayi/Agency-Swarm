from DesktopVisionAgent.tools import KeyboardTool
import time

def main():
    print("Testing KeyboardTool functionality...")
    
    # Test human-like typing
    print("\n1. Testing human-like typing:")
    print("Opening Notepad and typing some text...")
    
    # Press Windows key + R to open Run dialog
    tool = KeyboardTool(text="win+r", action="hotkey")
    tool.run()
    time.sleep(0.5)
    
    # Type 'notepad' and press enter
    tool = KeyboardTool(text="notepad", action="type")
    tool.run()
    time.sleep(0.5)
    tool = KeyboardTool(text="enter", action="press")
    tool.run()
    time.sleep(1)  # Wait for Notepad to open
    
    # Type some text with human-like timing
    text = "Hello! This is a demonstration of human-like typing. Notice the natural variations in typing speed and the pauses between words."
    tool = KeyboardTool(
        text=text,
        action="type",
        typing_speed=(0.05, 0.15),  # Slightly faster typing
        pause_range=(0.2, 0.4)      # Shorter word pauses
    )
    result = tool.run()
    print(result)
    
    # Test key combinations
    print("\n2. Testing key combinations:")
    time.sleep(1)
    
    # Select all text (Ctrl+A)
    print("Selecting all text...")
    tool = KeyboardTool(text="ctrl+a", action="hotkey")
    result = tool.run()
    print(result)
    time.sleep(0.5)
    
    # Copy text (Ctrl+C)
    print("Copying text...")
    tool = KeyboardTool(text="ctrl+c", action="hotkey")
    result = tool.run()
    print(result)
    time.sleep(0.5)
    
    # Press End key to move to end
    print("Moving to end of text...")
    tool = KeyboardTool(text="end", action="press")
    result = tool.run()
    print(result)
    time.sleep(0.5)
    
    # Press Enter twice
    tool = KeyboardTool(text="enter", action="press")
    tool.run()
    tool.run()
    
    # Paste text (Ctrl+V)
    print("Pasting text...")
    tool = KeyboardTool(text="ctrl+v", action="hotkey")
    result = tool.run()
    print(result)

if __name__ == "__main__":
    print("Starting keyboard simulation test...")
    print("Note: This test will open Notepad and perform typing operations.")
    print("Press Ctrl+C to stop the test")
    try:
        main()
        print("\nTest completed successfully!")
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}") 