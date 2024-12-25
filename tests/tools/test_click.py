from DesktopVisionAgent.tools import ClickTool
import pyautogui

def main():
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    print(f"Screen size: {screen_width}x{screen_height}")
    
    # Test different click types at different locations
    
    # Left click at center
    print("\nTesting left click at center:")
    tool = ClickTool(x=screen_width//2, y=screen_height//2)
    result = tool.run()
    print(result)
    
    # Right click at top-right corner
    print("\nTesting right click at top-right corner:")
    tool = ClickTool(
        x=screen_width-100, 
        y=100, 
        click_type="right",
        duration=0.5  # slower movement to see it better
    )
    result = tool.run()
    print(result)
    
    # Double click at bottom-left corner
    print("\nTesting double click at bottom-left corner:")
    tool = ClickTool(
        x=100, 
        y=screen_height-100, 
        click_type="double",
        duration=0.5
    )
    result = tool.run()
    print(result)

if __name__ == "__main__":
    print("Starting click tests...")
    print("Note: Move your mouse to see the automated movements")
    print("Press Ctrl+C to stop the test")
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest stopped by user")