from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import shutil
from pathlib import Path
import json

class FileManagementTool(BaseTool):
    """
    A tool for managing files and directories.
    Provides basic file operations like read, write, copy, move, and delete.
    """
    
    operation: str = Field(
        ...,
        description="Operation to perform: 'read', 'write', 'copy', 'move', 'delete', 'list', 'exists', 'info'"
    )
    
    path: str = Field(
        ...,
        description="Path to the file or directory to operate on"
    )
    
    content: str = Field(
        default=None,
        description="Content to write to file (for write operation)"
    )
    
    destination: str = Field(
        default=None,
        description="Destination path (for copy/move operations)"
    )

    def run(self):
        """
        Execute the requested file operation.
        """
        try:
            # Convert path to absolute path if relative
            path = os.path.abspath(self.path)
            
            # Check if path exists (except for write operation)
            if self.operation != 'write' and not os.path.exists(path):
                return f"Error: Path not found: {path}"
            
            if self.operation == 'read':
                if os.path.isfile(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    return f"Error: Not a file: {path}"
                    
            elif self.operation == 'write':
                if self.content is None:
                    return "Error: No content provided for write operation"
                    
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(path), exist_ok=True)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.content)
                return f"Successfully wrote to {path}"
                
            elif self.operation == 'copy':
                if self.destination is None:
                    return "Error: No destination provided for copy operation"
                    
                if os.path.isfile(path):
                    # Create destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(self.destination), exist_ok=True)
                    shutil.copy2(path, self.destination)
                    return f"Successfully copied {path} to {self.destination}"
                else:
                    shutil.copytree(path, self.destination)
                    return f"Successfully copied directory {path} to {self.destination}"
                    
            elif self.operation == 'move':
                if self.destination is None:
                    return "Error: No destination provided for move operation"
                    
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(self.destination), exist_ok=True)
                shutil.move(path, self.destination)
                return f"Successfully moved {path} to {self.destination}"
                
            elif self.operation == 'delete':
                if os.path.isfile(path):
                    os.remove(path)
                    return f"Successfully deleted file: {path}"
                else:
                    shutil.rmtree(path)
                    return f"Successfully deleted directory: {path}"
                    
            elif self.operation == 'list':
                if os.path.isdir(path):
                    items = []
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        items.append({
                            'name': item,
                            'type': 'directory' if os.path.isdir(item_path) else 'file',
                            'size': os.path.getsize(item_path),
                            'modified': os.path.getmtime(item_path)
                        })
                    return json.dumps(items, indent=2)
                else:
                    return f"Error: Not a directory: {path}"
                    
            elif self.operation == 'exists':
                return os.path.exists(path)
                
            elif self.operation == 'info':
                if os.path.exists(path):
                    info = {
                        'name': os.path.basename(path),
                        'type': 'directory' if os.path.isdir(path) else 'file',
                        'size': os.path.getsize(path),
                        'created': os.path.getctime(path),
                        'modified': os.path.getmtime(path),
                        'accessed': os.path.getatime(path),
                        'absolute_path': os.path.abspath(path)
                    }
                    return json.dumps(info, indent=2)
                else:
                    return f"Error: Path not found: {path}"
            
            else:
                return f"Error: Unknown operation: {self.operation}"
                
        except Exception as e:
            return f"Error during {self.operation} operation: {str(e)}"

if __name__ == "__main__":
    # Create test directory
    test_dir = "file_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    print("Testing FileManagementTool...")
    
    # Test write operation
    print("\nTesting write operation...")
    tool = FileManagementTool(
        operation="write",
        path=os.path.join(test_dir, "test.txt"),
        content="Hello, this is a test file!"
    )
    result = tool.run()
    print(result)
    
    # Test read operation
    print("\nTesting read operation...")
    tool = FileManagementTool(
        operation="read",
        path=os.path.join(test_dir, "test.txt")
    )
    result = tool.run()
    print(f"File content: {result}")
    
    # Test copy operation
    print("\nTesting copy operation...")
    tool = FileManagementTool(
        operation="copy",
        path=os.path.join(test_dir, "test.txt"),
        destination=os.path.join(test_dir, "test_copy.txt")
    )
    result = tool.run()
    print(result)
    
    # Test list operation
    print("\nTesting list operation...")
    tool = FileManagementTool(
        operation="list",
        path=test_dir
    )
    result = tool.run()
    print(f"Directory contents: {result}")
    
    # Test info operation
    print("\nTesting info operation...")
    tool = FileManagementTool(
        operation="info",
        path=os.path.join(test_dir, "test.txt")
    )
    result = tool.run()
    print(f"File info: {result}")
    
    # Test delete operation
    print("\nTesting delete operations...")
    for file in ["test.txt", "test_copy.txt"]:
        tool = FileManagementTool(
            operation="delete",
            path=os.path.join(test_dir, file)
        )
        result = tool.run()
        print(result)
    
    # Clean up
    print("\nCleaning up test directory...")
    shutil.rmtree(test_dir) 