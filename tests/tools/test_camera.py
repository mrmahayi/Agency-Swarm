from tools.CameraTool import CameraTool
import time
import os

def main():
    print("Testing Camera Tool functionality...")
    
    # First, detect available cameras
    tool = CameraTool()
    available_cameras = tool.list_available_cameras()
    
    if not available_cameras:
        print("No cameras detected!")
        return
    
    print("\nDetected cameras:")
    for idx, name in available_cameras:
        print(f"Camera {idx}: {name}")
    
    # Use the first available camera for tests
    camera_index = available_cameras[0][0]
    print(f"\nUsing camera {camera_index} for tests...")
    
    # Test 1: Quick capture without preview
    print("\nTest 1: Quick capture")
    print("Taking a photo immediately...")
    
    tool = CameraTool(
        camera_index=camera_index,
        preview_duration=0,
        save_path="camera_captures"
    )
    result = tool.run()
    print(f"Capture result: {result}")
    
    time.sleep(2)  # Pause between tests
    
    # Test 2: Capture with preview
    print("\nTest 2: Capture with preview")
    print("Starting 3-second preview before capture...")
    print("Press 'q' to capture early, 'r' to refocus")
    
    tool = CameraTool(
        camera_index=camera_index,
        preview_duration=3,
        save_path="camera_captures"
    )
    result = tool.run()
    print(f"Capture result: {result}")
    
    time.sleep(2)  # Pause between tests
    
    # Test 3: Multiple quick captures
    print("\nTest 3: Multiple quick captures")
    print("Taking 3 photos in succession...")
    
    captured_files = []
    for i in range(3):
        print(f"\nCapture {i+1}/3...")
        tool = CameraTool(
            camera_index=camera_index,
            preview_duration=0,
            save_path="camera_captures"
        )
        result = tool.run()
        captured_files.append(result)
        time.sleep(1)  # Brief pause between captures
    
    print("\nCaptured files:")
    for file in captured_files:
        print(f"- {file}")
    
    # If multiple cameras are available, test switching between them
    if len(available_cameras) > 1:
        print("\nTest 4: Testing different cameras")
        for idx, name in available_cameras[1:]:  # Skip the first camera as we already tested it
            print(f"\nTesting camera {idx}: {name}")
            tool = CameraTool(
                camera_index=idx,
                preview_duration=3,  # Show preview for each camera
                save_path="camera_captures"
            )
            result = tool.run()
            print(f"Capture result: {result}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
        print("\nCamera tests completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nTest session ended.") 