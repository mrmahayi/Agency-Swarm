from agency_swarm.tools import BaseTool
from pydantic import Field
import pyperclip
import win32clipboard
from PIL import ImageGrab, Image
import io
import os
from typing import Optional, Literal

class ClipboardTool(BaseTool):
    """
    A tool for managing clipboard operations with support for text, images, and files.
    """
    
    operation: Literal['copy', 'paste', 'clear'] = Field(
        ...,
        description="Operation to perform: 'copy', 'paste', or 'clear'"
    )
    
    content_type: Literal['text', 'image', 'file'] = Field(
        default='text',
        description="Type of content to copy/paste: 'text', 'image', or 'file'"
    )
    
    content: Optional[str] = Field(
        None,
        description="Content to copy (for copy operation)"
    )
    
    file_path: Optional[str] = Field(
        None,
        description="Path to save pasted image or file path to copy"
    )
    
    def copy_text(self, text):
        """Copy text to clipboard."""
        pyperclip.copy(text)
        return f"Copied text to clipboard: {text[:50]}..."
        
    def paste_text(self):
        """Paste text from clipboard."""
        return pyperclip.paste()
        
    def copy_image(self, image_path):
        """Copy image to clipboard."""
        image = Image.open(image_path)
        output = io.BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]  # Remove BMP header
        output.close()
        
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        return f"Copied image from {image_path} to clipboard"
        
    def paste_image(self, save_path):
        """Paste image from clipboard and save it."""
        image = ImageGrab.grabclipboard()
        if image is None:
            return "No image found in clipboard"
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save image with appropriate format
        ext = os.path.splitext(save_path)[1].lower()
        if not ext:
            save_path += '.png'
            ext = '.png'
            
        if ext == '.jpg' or ext == '.jpeg':
            image = image.convert('RGB')
            
        image.save(save_path)
        return f"Saved clipboard image to {save_path}"
        
    def copy_file(self, file_path):
        """Copy file path to clipboard."""
        pyperclip.copy(os.path.abspath(file_path))
        return f"Copied file path to clipboard: {file_path}"
        
    def clear_clipboard(self):
        """Clear the clipboard."""
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        return "Clipboard cleared"
        
    def run(self):
        """Execute the requested clipboard operation."""
        try:
            if self.operation == 'clear':
                return self.clear_clipboard()
                
            elif self.operation == 'copy':
                if not self.content and not self.file_path:
                    return "Error: No content or file path provided for copy operation"
                    
                if self.content_type == 'text':
                    return self.copy_text(self.content)
                elif self.content_type == 'image':
                    if not self.file_path:
                        return "Error: File path required for copying image"
                    return self.copy_image(self.file_path)
                elif self.content_type == 'file':
                    if not self.file_path:
                        return "Error: File path required for copying file"
                    return self.copy_file(self.file_path)
                    
            elif self.operation == 'paste':
                if self.content_type == 'text':
                    return self.paste_text()
                elif self.content_type == 'image':
                    if not self.file_path:
                        return "Error: Save path required for pasting image"
                    return self.paste_image(self.file_path)
                elif self.content_type == 'file':
                    return self.paste_text()  # File paths are stored as text
                    
            return f"Error: Invalid operation {self.operation}"
            
        except Exception as e:
            return f"Error during {self.operation} operation: {str(e)}"

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
        content_type='text',
        content='Hello from clipboard!'
    )
    print(f"Copy result: {tool.run()}")
    
    # Paste text
    tool = ClipboardTool(
        operation='paste',
        content_type='text'
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
        content_type='image',
        file_path=test_image_path
    )
    print(f"Copy image result: {tool.run()}")
    
    # Paste image
    tool = ClipboardTool(
        operation='paste',
        content_type='image',
        file_path=os.path.join(test_dir, 'pasted.png')
    )
    print(f"Paste image result: {tool.run()}")
    
    # Test file operations
    print("\nTesting file operations...")
    
    # Copy file path
    tool = ClipboardTool(
        operation='copy',
        content_type='file',
        file_path=test_image_path
    )
    print(f"Copy file result: {tool.run()}")
    
    # Paste file path
    tool = ClipboardTool(
        operation='paste',
        content_type='file'
    )
    print(f"Paste file result: {tool.run()}")
    
    # Test clear operation
    print("\nTesting clear operation...")
    tool = ClipboardTool(operation='clear')
    print(f"Clear result: {tool.run()}")
    
    print("\nCleaning up test directory...")
    import shutil
    shutil.rmtree(test_dir) 