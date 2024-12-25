from agency_swarm.tools import BaseTool
from pydantic import Field, PrivateAttr
import cv2
import time
import numpy as np
import os

class CameraTool(BaseTool):
    """
    A tool for capturing images from the webcam with optimized settings.
    """
    
    image_path: str = Field(
        default="camera_captures/capture.jpg",
        description="Path where the captured image will be saved."
    )
    
    _camera = PrivateAttr(default=None)
    _optimal_settings = PrivateAttr(default={
        'width': 1280,
        'height': 720,
        'brightness': 128,
        'contrast': 192
    })
    
    def setup_camera(self):
        """Initialize the camera with optimal settings."""
        if self._camera is not None:
            self._camera.release()
            
        for camera_index in range(2):
            camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            if camera.isOpened():
                # Set resolution
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, self._optimal_settings['width'])
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self._optimal_settings['height'])
                
                # Set optimal brightness and contrast
                camera.set(cv2.CAP_PROP_BRIGHTNESS, self._optimal_settings['brightness'])
                camera.set(cv2.CAP_PROP_CONTRAST, self._optimal_settings['contrast'])
                
                # Verify settings
                ret, frame = camera.read()
                if ret and frame is not None:
                    self._camera = camera
                    return True
                else:
                    camera.release()
        return False
        
    def run(self):
        """Capture an image with optimal settings."""
        try:
            if self._camera is None and not self.setup_camera():
                return "Failed to initialize camera"
                
            # Wait for camera to adjust
            time.sleep(0.2)
            
            # Capture frame
            ret, frame = self._camera.read()
            if not ret or frame is None:
                return "Failed to capture image"
                
            # Create output directory if needed
            os.makedirs(os.path.dirname(self.image_path), exist_ok=True)
            
            # Save image
            cv2.imwrite(self.image_path, frame)
            return f"Image saved to {self.image_path}"
            
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            self.cleanup()
        
    def cleanup(self):
        """Release camera resources."""
        if self._camera is not None:
            self._camera.release()
            self._camera = None
            cv2.destroyAllWindows()
            
    def __del__(self):
        """Ensure cleanup on deletion."""
        self.cleanup()

if __name__ == "__main__":
    # Test the tool
    tool = CameraTool()
    try:
        print("Testing camera with optimal settings...")
        result = tool.run()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        tool.cleanup() 