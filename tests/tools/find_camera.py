from tools.CameraTool import CameraTool
import json
import os

def save_camera_config(camera_index):
    """Save the selected camera index to a config file."""
    config = {"camera_index": camera_index}
    with open("camera_config.json", "w") as f:
        json.dump(config, f)
    print(f"\nCamera {camera_index} has been saved as the default camera.")

def main():
    print("Camera Detection Tool")
    print("====================")
    
    tool = CameraTool()
    available_cameras = tool.list_available_cameras()
    
    if not available_cameras:
        print("No cameras detected!")
        return
    
    print("\nDetected cameras:")
    for idx, details in available_cameras:
        print(f"\nCamera {idx}:")
        for key, value in details.items():
            print(f"  {key}: {value}")
        
        print("\nTesting this camera...")
        tool.test_camera(idx)
        
        response = input("\nIs this the correct camera? (y/n): ")
        if response.lower() == 'y':
            print(f"\nConfirming camera {idx}...")
            
            # Take a test photo
            tool = CameraTool(
                camera_index=idx,
                preview_duration=3,
                save_path="camera_captures"
            )
            result = tool.run()
            
            if not result.startswith("Error"):
                print(f"Test photo saved to: {result}")
                confirm = input("\nIs the test photo good? (y/n): ")
                if confirm.lower() == 'y':
                    save_camera_config(idx)
                    return
            
            print("Let's try another camera...")
        else:
            print("Trying next camera...")
    
    print("\nNo suitable camera was found.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCamera detection cancelled.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nCamera detection completed.") 