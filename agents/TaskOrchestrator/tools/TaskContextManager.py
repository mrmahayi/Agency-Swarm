from datetime import datetime
from typing import Dict, List, Optional, Set
from pydantic import Field, PrivateAttr
from agency_swarm.tools import BaseTool
import json
from pathlib import Path
import uuid

class TaskContextManager(BaseTool):
    """
    A tool for managing task contexts, relationships, and agent assignments.
    Tracks active tasks, dependencies, and task progress across the agency.
    """
    
    operation: str = Field(
        ...,
        description="Operation to perform: 'create_task', 'update_task', 'get_task', 'assign_task', 'get_agent_tasks', 'add_dependency', 'get_dependencies'"
    )
    
    task_data: Optional[Dict] = Field(
        default=None,
        description="Task data including: {'task_id': str, 'description': str, 'status': str, 'priority': int, 'deadline': str, 'metadata': Dict}"
    )
    
    agent_id: Optional[str] = Field(
        default=None,
        description="Agent ID for task assignments and queries"
    )
    
    task_id: Optional[str] = Field(
        default=None,
        description="Task ID for specific task operations"
    )
    
    dependency_data: Optional[Dict] = Field(
        default=None,
        description="Dependency data: {'task_id': str, 'depends_on': List[str]}"
    )
    
    # Private attributes for file paths
    _context_dir: Path = PrivateAttr()
    _tasks_file: Path = PrivateAttr()
    _assignments_file: Path = PrivateAttr()
    _dependencies_file: Path = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._context_dir = Path("task_contexts")
        self._context_dir.mkdir(exist_ok=True)
        self._tasks_file = self._context_dir / "tasks.json"
        self._assignments_file = self._context_dir / "assignments.json"
        self._dependencies_file = self._context_dir / "dependencies.json"
        
        # Initialize files if they don't exist
        if not self._tasks_file.exists():
            self._save_data(self._tasks_file, {})
        if not self._assignments_file.exists():
            self._save_data(self._assignments_file, {})
        if not self._dependencies_file.exists():
            self._save_data(self._dependencies_file, {})

    def _save_data(self, file_path: Path, data: Dict):
        """Save data to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_data(self, file_path: Path) -> Dict:
        """Load data from JSON file."""
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}

    def _generate_task_id(self) -> str:
        """Generate a unique task ID using timestamp and UUID."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        unique_id = uuid.uuid4().hex[:8]
        return f"task_{timestamp}_{unique_id}"

    def _create_task(self) -> str:
        """Create a new task and store its context."""
        if not self.task_data:
            return "Error: task_data is required for creating a task"
        
        tasks = self._load_data(self._tasks_file)
        task_id = self._generate_task_id()
        
        task = {
            "id": task_id,
            "description": self.task_data.get("description"),
            "status": self.task_data.get("status", "pending"),
            "priority": self.task_data.get("priority", 3),
            "created_at": datetime.now().isoformat(),
            "deadline": self.task_data.get("deadline"),
            "metadata": {
                "type": self.task_data.get("type", "general"),
                "source": self.task_data.get("source", "user"),
                "parent_task": self.task_data.get("parent_task"),
                "dependencies": self.task_data.get("dependencies", []),
                "tags": self.task_data.get("tags", []),
                "estimated_duration": self.task_data.get("estimated_duration"),
                "actual_duration": None,
                "custom_data": self.task_data.get("custom_data", {})
            },
            "last_updated": datetime.now().isoformat(),
            "status_history": [
                {
                    "status": "pending",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Task created"
                }
            ]
        }
        
        tasks[task_id] = task
        self._save_data(self._tasks_file, tasks)
        return f"Task created successfully with ID: {task_id}"

    def _update_task(self) -> str:
        """Update an existing task's context."""
        if not self.task_id or not self.task_data:
            return "Error: task_id and task_data are required for updating a task"
        
        tasks = self._load_data(self._tasks_file)
        if self.task_id not in tasks:
            return f"Error: Task {self.task_id} not found"
        
        task = tasks[self.task_id]
        current_status = task.get("status")
        new_status = self.task_data.get("status")
        
        # Update basic fields
        task.update({
            k: v for k, v in self.task_data.items()
            if k in ["description", "priority", "deadline"]
        })
        
        # Update metadata if provided
        if "metadata" in self.task_data:
            task["metadata"].update(self.task_data["metadata"])
        
        # Update status and add to history if changed
        if new_status and new_status != current_status:
            task["status"] = new_status
            task["status_history"].append({
                "status": new_status,
                "timestamp": datetime.now().isoformat(),
                "message": self.task_data.get("status_message", f"Status changed to {new_status}")
            })
        
        # Update timestamps
        task["last_updated"] = datetime.now().isoformat()
        if new_status == "completed":
            task["metadata"]["actual_duration"] = (
                datetime.now() - datetime.fromisoformat(task["created_at"])
            ).total_seconds()
        
        tasks[self.task_id] = task
        self._save_data(self._tasks_file, tasks)
        return f"Task {self.task_id} updated successfully"

    def _assign_task(self) -> str:
        """Assign a task to an agent."""
        if not self.task_id or not self.agent_id:
            return "Error: task_id and agent_id are required for task assignment"
        
        assignments = self._load_data(self._assignments_file)
        if self.task_id not in assignments:
            assignments[self.task_id] = []
        
        if self.agent_id not in assignments[self.task_id]:
            assignments[self.task_id].append(self.agent_id)
            self._save_data(self._assignments_file, assignments)
            return f"Task {self.task_id} assigned to agent {self.agent_id}"
        return f"Task {self.task_id} is already assigned to agent {self.agent_id}"

    def _get_agent_tasks(self) -> str:
        """Get all tasks assigned to an agent."""
        if not self.agent_id:
            return "Error: agent_id is required for getting agent tasks"
        
        assignments = self._load_data(self._assignments_file)
        tasks = self._load_data(self._tasks_file)
        
        agent_tasks = []
        for task_id, agents in assignments.items():
            if self.agent_id in agents and task_id in tasks:
                agent_tasks.append(tasks[task_id])
        
        return json.dumps(agent_tasks, indent=2)

    def _add_dependency(self) -> str:
        """Add task dependencies."""
        if not self.dependency_data:
            return "Error: dependency_data is required for adding dependencies"
        
        dependencies = self._load_data(self._dependencies_file)
        task_id = self.dependency_data.get("task_id")
        depends_on = self.dependency_data.get("depends_on", [])
        
        if not task_id or not depends_on:
            return "Error: task_id and depends_on list are required"
        
        if task_id not in dependencies:
            dependencies[task_id] = []
        
        dependencies[task_id].extend([dep for dep in depends_on if dep not in dependencies[task_id]])
        self._save_data(self._dependencies_file, dependencies)
        return f"Dependencies added successfully for task {task_id}"

    def _get_dependencies(self) -> str:
        """Get dependencies for a task."""
        if not self.task_id:
            return "Error: task_id is required for getting dependencies"
        
        dependencies = self._load_data(self._dependencies_file)
        task_deps = dependencies.get(self.task_id, [])
        return json.dumps(task_deps, indent=2)

    def run(self) -> str:
        """Execute the task context operation."""
        operations = {
            "create_task": self._create_task,
            "update_task": self._update_task,
            "assign_task": self._assign_task,
            "get_agent_tasks": self._get_agent_tasks,
            "add_dependency": self._add_dependency,
            "get_dependencies": self._get_dependencies
        }
        
        if self.operation not in operations:
            return f"Error: Invalid operation. Must be one of {list(operations.keys())}"
        
        return operations[self.operation]()

if __name__ == "__main__":
    # Test the task context management functionality
    tool = TaskContextManager(
        operation="create_task",
        task_data={
            "description": "Test task",
            "priority": 1,
            "deadline": "2024-12-31T23:59:59",
            "metadata": {"type": "test"}
        }
    )
    print("Creating task:", tool.run())
    
    tool = TaskContextManager(
        operation="get_agent_tasks",
        agent_id="AgentA"
    )
    print("\nGetting tasks for AgentA:", tool.run()) 