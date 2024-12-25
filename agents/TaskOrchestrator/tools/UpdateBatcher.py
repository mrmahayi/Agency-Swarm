from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import Field, PrivateAttr
from agency_swarm.tools import BaseTool
import json
from pathlib import Path

class UpdateBatcher(BaseTool):
    """
    A tool for batching updates and managing user communications efficiently.
    Collects updates and sends them in batches based on timing and priority.
    """
    
    operation: str = Field(
        ...,
        description="Operation to perform: 'add_update', 'get_batch', 'clear_batch', 'force_send'"
    )
    
    update_data: Optional[Dict] = Field(
        default=None,
        description="Update data including: {'content': str, 'priority': int, 'category': str, 'metadata': Dict}"
    )
    
    batch_settings: Optional[Dict] = Field(
        default=None,
        description="Batch settings including: {'max_batch_size': int, 'batch_timeout': int, 'min_priority': int}"
    )
    
    # Private attributes for file paths
    _updates_dir: Path = PrivateAttr()
    _current_batch_file: Path = PrivateAttr()
    _batch_history_file: Path = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._updates_dir = Path("updates")
        self._updates_dir.mkdir(exist_ok=True)
        self._current_batch_file = self._updates_dir / "current_batch.json"
        self._batch_history_file = self._updates_dir / "batch_history.json"
        
        # Initialize files if they don't exist
        if not self._current_batch_file.exists():
            self._save_data(self._current_batch_file, {
                "updates": [],
                "last_send": datetime.now().isoformat(),
                "batch_number": 0
            })
        if not self._batch_history_file.exists():
            self._save_data(self._batch_history_file, [])

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

    def _should_send_batch(self, batch_data: Dict) -> bool:
        """Determine if the current batch should be sent."""
        settings = self.batch_settings or {
            "max_batch_size": 5,
            "batch_timeout": 150,  # 2.5 minutes in seconds
            "min_priority": 3
        }
        
        updates = batch_data["updates"]
        if not updates:
            return False
        
        # Check batch size
        if len(updates) >= settings["max_batch_size"]:
            return True
        
        # Check high priority updates
        if any(update["priority"] <= settings["min_priority"] for update in updates):
            return True
        
        # Check timeout
        last_send = datetime.fromisoformat(batch_data["last_send"])
        if datetime.now() - last_send > timedelta(seconds=settings["batch_timeout"]):
            return True
        
        return False

    def _format_batch(self, updates: List[Dict]) -> str:
        """Format a batch of updates into a user-friendly message."""
        if not updates:
            return "No updates to report."
        
        # Group updates by category
        categories = {}
        for update in updates:
            category = update.get("category", "General")
            if category not in categories:
                categories[category] = []
            categories[category].append(update)
        
        # Format the message
        message = "Update Summary:\n\n"
        for category, category_updates in categories.items():
            message += f"## {category}\n"
            for update in sorted(category_updates, key=lambda x: x["priority"]):
                priority_marker = "❗" * (1 if update["priority"] >= 3 else 2)
                message += f"{priority_marker} {update['content']}\n"
            message += "\n"
        
        return message

    def _add_update(self) -> str:
        """Add a new update to the current batch."""
        if not self.update_data:
            return "Error: update_data is required for adding an update"
        
        batch_data = self._load_data(self._current_batch_file)
        
        update = {
            "id": f"upd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": self.update_data.get("content"),
            "priority": self.update_data.get("priority", 3),
            "category": self.update_data.get("category", "General"),
            "metadata": self.update_data.get("metadata", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        batch_data["updates"].append(update)
        self._save_data(self._current_batch_file, batch_data)
        
        if self._should_send_batch(batch_data):
            return self._send_batch()
        
        return f"Update added to batch (ID: {update['id']})"

    def _send_batch(self) -> str:
        """Send the current batch of updates."""
        batch_data = self._load_data(self._current_batch_file)
        if not batch_data["updates"]:
            return "No updates to send"
        
        # Format the batch message
        message = self._format_batch(batch_data["updates"])
        
        # Archive the batch
        history = self._load_data(self._batch_history_file)
        batch_data["batch_number"] += 1
        batch_data["sent_at"] = datetime.now().isoformat()
        history.append(batch_data)
        self._save_data(self._batch_history_file, history)
        
        # Clear the current batch
        self._save_data(self._current_batch_file, {
            "updates": [],
            "last_send": datetime.now().isoformat(),
            "batch_number": batch_data["batch_number"]
        })
        
        return message

    def _get_batch(self) -> str:
        """Get the current batch of updates without sending."""
        batch_data = self._load_data(self._current_batch_file)
        return self._format_batch(batch_data["updates"])

    def _clear_batch(self) -> str:
        """Clear the current batch without sending."""
        batch_data = self._load_data(self._current_batch_file)
        batch_number = batch_data["batch_number"]
        
        self._save_data(self._current_batch_file, {
            "updates": [],
            "last_send": datetime.now().isoformat(),
            "batch_number": batch_number
        })
        
        return "Current batch cleared"

    def run(self) -> str:
        """Execute the update batching operation."""
        operations = {
            "add_update": self._add_update,
            "get_batch": self._get_batch,
            "clear_batch": self._clear_batch,
            "force_send": self._send_batch
        }
        
        if self.operation not in operations:
            return f"Error: Invalid operation. Must be one of {list(operations.keys())}"
        
        return operations[self.operation]()

if __name__ == "__main__":
    # Test the update batching functionality
    tool = UpdateBatcher(
        operation="add_update",
        update_data={
            "content": "Test update",
            "priority": 2,
            "category": "Testing",
            "metadata": {"type": "test"}
        }
    )
    print("Adding update:", tool.run())
    
    tool = UpdateBatcher(
        operation="get_batch"
    )
    print("\nCurrent batch:", tool.run()) 