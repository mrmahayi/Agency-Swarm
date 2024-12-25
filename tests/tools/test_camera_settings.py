from tools.CameraTool import CameraTool
import cv2
import time
import numpy as np
import json
import os

def setup_camera_hd():
    """Setup camera in HD resolution."""
    for camera_index in range(2):
        print(f"\nTrying camera index {camera_index}...")
        camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if camera.isOpened():
            # Set HD resolution
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            # Verify settings
            ret, frame = camera.read()
            if ret and frame is not None:
                actual_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
                actual_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
                print(f"Successfully opened camera {camera_index}")
                print(f"Resolution: {actual_width}x{actual_height}")
                return camera
            else:
                print(f"Camera {camera_index} opened but couldn't read frame")
                camera.release()
        else:
            print(f"Could not open camera {camera_index}")
    return None

def test_settings(camera, brightness, contrast):
    """Test specific brightness and contrast settings."""
    try:
        # Set settings
        camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        camera.set(cv2.CAP_PROP_CONTRAST, contrast)
        
        # Wait for camera to adjust
        time.sleep(0.2)
        
        # Capture frame
        ret, frame = camera.read()
        if not ret or frame is None:
            print(f"Failed to capture with BR={brightness}, CO={contrast}")
            return None
            
        return frame
    except Exception as e:
        print(f"Error testing settings BR={brightness}, CO={contrast}: {str(e)}")
        return None

def save_test_image(frame, brightness, contrast, folder='camera_tests'):
    """Save test image with settings in filename."""
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{folder}/test_BR{brightness}_CO{contrast}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Saved {filename}")
    return filename

def create_grid_image(images, labels, grid_size=(3, 3)):
    """Create a grid of images for comparison."""
    rows, cols = grid_size
    cell_height = images[0].shape[0] // rows
    cell_width = images[0].shape[1] // cols
    
    # Create blank grid
    grid = np.zeros((cell_height * rows, cell_width * cols, 3), dtype=np.uint8)
    
    # Fill grid with resized images
    for idx, (img, label) in enumerate(zip(images, labels)):
        if idx >= rows * cols:
            break
            
        i, j = idx // cols, idx % cols
        resized = cv2.resize(img, (cell_width, cell_height))
        grid[i*cell_height:(i+1)*cell_height, j*cell_width:(j+1)*cell_width] = resized
        
        # Add label
        cv2.putText(grid, label, 
                   (j*cell_width + 10, i*cell_height + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return grid

def main():
    print("Camera Settings Test (HD)")
    print("=========================")
    
    # Setup camera
    camera = setup_camera_hd()
    if camera is None:
        print("Error: Could not setup camera in HD mode")
        return

    # Create preview window
    cv2.namedWindow('Settings Test', cv2.WINDOW_NORMAL)
    
    try:
        # Test combinations
        test_images = []
        test_labels = []
        
        # Test brightness and contrast variations
        brightness_values = [64, 128, 192]  # Low, Medium, High
        contrast_values = [64, 128, 192]    # Low, Medium, High
        
        print("\nTesting brightness and contrast combinations...")
        for brightness in brightness_values:
            for contrast in contrast_values:
                print(f"\nTesting BR={brightness}, CO={contrast}")
                
                frame = test_settings(camera, brightness, contrast)
                if frame is not None:
                    # Save individual image
                    filename = save_test_image(frame, brightness, contrast)
                    
                    # Add to collection for grid
                    test_images.append(frame)
                    test_labels.append(f"BR={brightness}\nCO={contrast}")
                    
                    # Show preview
                    cv2.imshow('Settings Test', frame)
                    if cv2.waitKey(500) & 0xFF == ord('q'):
                        break
        
        # Create and save comparison grid
        if test_images:
            grid = create_grid_image(test_images, test_labels)
            cv2.imwrite('camera_tests/comparison_grid.jpg', grid)
            print("\nSaved comparison grid to camera_tests/comparison_grid.jpg")
            
            # Show grid
            cv2.imshow('Settings Test', grid)
            print("\nShowing comparison grid (press 'q' to exit)...")
            while True:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
    finally:
        if camera is not None:
            camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        cv2.destroyAllWindows() 