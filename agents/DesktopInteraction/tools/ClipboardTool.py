from agency_swarm.tools import BaseTool
from pydantic import Field
import pyperclip
import os
from PIL import Image

class ClipboardTool(BaseTool):
    """Tool for managing clipboard operations."""
    
    operation: str = Field(
        ...,
        description="The clipboard operation to perform: 'copy' or 'paste'"
    )
    
    text: str = Field(
        None,
        description="Text to copy to clipboard (only required for 'copy' operation)"
    )

    def run(self):
        """Execute the clipboard operation."""
        try:
            if self.operation == "copy":
                if not self.text:
                    return {"status": "error", "message": "Text is required for copy operation"}
                pyperclip.copy(self.text)
                return {"status": "success", "message": "Text copied to clipboard"}
            elif self.operation == "paste":
                text = pyperclip.paste()
                return {"status": "success", "message": "Text pasted from clipboard", "text": text}
            else:
                return {"status": "error", "message": f"Invalid operation: {self.operation}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test the tool with various operations
    test_dir = "clipboard_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    print("Testing ClipboardTool...")
    
    # Test text operations
    print("\nTesting text operations...")
    
    # Copy text
    tool = ClipboardTool(
        operation='copy',
        text='Hello from clipboard!'
    )
    print(f"Copy result: {tool.run()}")
    
    # Paste text
    tool = ClipboardTool(
        operation='paste'
    )
    print(f"Paste result: {tool.run()}")
    
    # Test image operations
    print("\nTesting image operations...")
    
    # Create a test image
    test_image = Image.new('RGB', (100, 100), color='red')
    test_image_path = os.path.join(test_dir, 'test.png')
    test_image.save(test_image_path)
    
    # Copy image
    tool = ClipboardTool(
        operation='copy',
        text=test_image_path
    )
    print(f"Copy image result: {tool.run()}")
    
    # Paste image
    tool = ClipboardTool(
        operation='paste',
        text=os.path.join(test_dir, 'pasted.png')
    )
    print(f"Paste image result: {tool.run()}")
    
    # Test file operations
    print("\nTesting file operations...")
    
    # Copy file path
    tool = ClipboardTool(
        operation='copy',
        text=test_image_path
    )
    print(f"Copy file result: {tool.run()}")
    
    # Paste file path
    tool = ClipboardTool(
        operation='paste'
    )
    print(f"Paste file result: {tool.run()}")
    
    # Test clear operation
    print("\nTesting clear operation...")
    tool = ClipboardTool(operation='clear')
    print(f"Clear result: {tool.run()}")
    
    print("\nCleaning up test directory...")
    import shutil
    shutil.rmtree(test_dir) 