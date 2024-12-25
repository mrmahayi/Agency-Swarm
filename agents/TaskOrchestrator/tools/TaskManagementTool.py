from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class TaskManagementTool(BaseTool):
    """
    Tool for managing tasks, including creation, updates, and status tracking.
    """
    operation: str = Field(
        ...,
        description="The operation to perform: create, update, delete, get, list"
    )
    task_data: Dict = Field(
        default={},
        description="Task data for create/update operations"
    )
    task_id: Optional[str] = Field(
        default=None,
        description="Task ID for get/update/delete operations"
    )

    def __init__(self, **data):
        super().__init__(**data)
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        self.tasks_path = "data/tasks.json"
        self._initialize_tasks_file()

    def _initialize_tasks_file(self):
        """Initialize tasks file if it doesn't exist."""
        if not os.path.exists(self.tasks_path):
            with open(self.tasks_path, 'w') as f:
                json.dump({"tasks": {}}, f)

    def _load_tasks(self) -> Dict:
        """Load tasks from file."""
        try:
            with open(self.tasks_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"tasks": {}}

    def _save_tasks(self, tasks_data: Dict):
        """Save tasks to file."""
        with open(self.tasks_path, 'w') as f:
            json.dump(tasks_data, f, indent=2)

    def run(self) -> str:
        """
        Execute the task management operation.
        
        Returns:
            str: Result of the operation
        """
        try:
            if self.operation == "create":
                return self._create_task()
            elif self.operation == "update":
                return self._update_task()
            elif self.operation == "delete":
                return self._delete_task()
            elif self.operation == "get":
                return self._get_task()
            elif self.operation == "list":
                return self._list_tasks()
            else:
                return f"Unknown operation: {self.operation}"
        except Exception as e:
            return f"Error executing operation: {str(e)}"

    def _create_task(self) -> str:
        """Create a new task."""
        tasks_data = self._load_tasks()
        
        # Generate task ID if not provided
        if "id" not in self.task_data:
            task_id = f"task_{len(tasks_data['tasks']) + 1}"
            self.task_data["id"] = task_id
        else:
            task_id = self.task_data["id"]
        
        # Add timestamps if not provided
        if "created_at" not in self.task_data:
            self.task_data["created_at"] = datetime.now().isoformat()
        if "updated_at" not in self.task_data:
            self.task_data["updated_at"] = datetime.now().isoformat()
        
        # Store task
        tasks_data["tasks"][task_id] = self.task_data
        self._save_tasks(tasks_data)
        
        return f"Task {task_id} created successfully"

    def _update_task(self) -> str:
        """Update an existing task."""
        if not self.task_id and "id" not in self.task_data:
            return "Task ID is required for update operation"
        
        task_id = self.task_id or self.task_data["id"]
        tasks_data = self._load_tasks()
        
        if task_id not in tasks_data["tasks"]:
            return f"Task {task_id} not found"
        
        # Update task data
        tasks_data["tasks"][task_id].update(self.task_data)
        tasks_data["tasks"][task_id]["updated_at"] = datetime.now().isoformat()
        
        self._save_tasks(tasks_data)
        return f"Task {task_id} updated successfully"

    def _delete_task(self) -> str:
        """Delete a task."""
        if not self.task_id:
            return "Task ID is required for delete operation"
        
        tasks_data = self._load_tasks()
        
        if self.task_id not in tasks_data["tasks"]:
            return f"Task {self.task_id} not found"
        
        del tasks_data["tasks"][self.task_id]
        self._save_tasks(tasks_data)
        
        return f"Task {self.task_id} deleted successfully"

    def _get_task(self) -> str:
        """Get task details."""
        if not self.task_id:
            return "Task ID is required for get operation"
        
        tasks_data = self._load_tasks()
        
        if self.task_id not in tasks_data["tasks"]:
            return f"Task {self.task_id} not found"
        
        return json.dumps(tasks_data["tasks"][self.task_id], indent=2)

    def _list_tasks(self) -> str:
        """List all tasks."""
        tasks_data = self._load_tasks()
        return json.dumps({"tasks": list(tasks_data["tasks"].values())}, indent=2)

if __name__ == "__main__":
    # Test the TaskManagementTool
    
    # Test task creation
    print("\nTesting task creation:")
    tool = TaskManagementTool(
        operation="create",
        task_data={
            "description": "Test task",
            "status": "pending",
            "priority": "high"
        }
    )
    print(tool.run())
    
    # Test task update
    print("\nTesting task update:")
    tool = TaskManagementTool(
        operation="update",
        task_id="task_1",
        task_data={
            "status": "in_progress"
        }
    )
    print(tool.run())
    
    # Test task listing
    print("\nTesting task listing:")
    tool = TaskManagementTool(operation="list")
    print(tool.run()) 