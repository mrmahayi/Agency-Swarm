from datetime import datetime
import json
from pathlib import Path
import uuid
from typing import Dict, Optional
from pydantic import Field, PrivateAttr
from agency_swarm.tools import BaseTool

class CommunicationTool(BaseTool):
    """
    A tool for managing communication between agents.
    Provides capabilities for sending messages, broadcasting, and maintaining communication logs.
    """
    
    operation: str = Field(
        ...,
        description="Operation to perform: 'send_message', 'broadcast', 'get_messages', 'mark_read', 'get_unread'"
    )
    
    message_data: Optional[Dict] = Field(
        default=None,
        description="Message data including: {'from_agent': str, 'to_agent': str, 'content': str, 'priority': int (1-5), 'metadata': Dict}"
    )
    
    agent_id: Optional[str] = Field(
        default=None,
        description="Agent ID for retrieving messages"
    )
    
    message_id: Optional[str] = Field(
        default=None,
        description="Message ID for operations on specific messages"
    )
    
    # Private attributes for file paths
    _messages_dir: Path = PrivateAttr()
    _messages_file: Path = PrivateAttr()
    
    def __init__(self, **data):
        super().__init__(**data)
        # Initialize messages directory
        self._messages_dir = Path("messages")
        self._messages_dir.mkdir(exist_ok=True)
        self._messages_file = self._messages_dir / "messages.json"
        if not self._messages_file.exists():
            self._save_messages({})
    
    def _generate_message_id(self) -> str:
        """Generate a unique message ID using timestamp and UUID."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        return f"msg_{timestamp}_{unique_id}"
    
    def _load_messages(self) -> Dict:
        """Load messages from JSON file."""
        if self._messages_file.exists():
            with open(self._messages_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_messages(self, messages: Dict):
        """Save messages to JSON file."""
        with open(self._messages_file, 'w') as f:
            json.dump(messages, f, indent=2)
    
    def _send_message(self) -> str:
        """Send a message from one agent to another."""
        if not self.message_data:
            return "Error: message_data is required for sending a message"
        
        message_id = self._generate_message_id()
        
        message = {
            "id": message_id,
            "timestamp": datetime.now().isoformat(),
            "from_agent": self.message_data.get("from_agent"),
            "to_agent": self.message_data.get("to_agent"),
            "content": self.message_data.get("content"),
            "priority": self.message_data.get("priority", "normal"),
            "type": self.message_data.get("type", "general"),
            "status": "unread"
        }
        
        messages = self._load_messages()
        messages[message_id] = message
        self._save_messages(messages)
        
        return f"Message sent successfully with ID: {message_id}"

    def _get_messages(self) -> str:
        """Get all messages for a specific agent."""
        if not self.agent_id:
            return "Error: agent_id is required for getting messages"
        
        messages = self._load_messages()
        agent_messages = [
            msg for msg in messages.values()
            if msg["to_agent"] == self.agent_id
        ]
        return json.dumps(agent_messages, indent=2)
    
    def _mark_read(self) -> str:
        """Mark a message as read."""
        if not self.message_id:
            return "Error: message_id is required for marking messages as read"
        
        messages = self._load_messages()
        if self.message_id in messages:
            messages[self.message_id]["status"] = "read"
            self._save_messages(messages)
            return f"Message {self.message_id} marked as read"
        return f"Error: Message {self.message_id} not found"
    
    def _get_unread(self) -> str:
        """Get unread messages for an agent."""
        if not self.agent_id:
            return "Error: agent_id is required for getting unread messages"
        
        messages = self._load_messages()
        unread_messages = [
            msg for msg in messages.values()
            if msg["to_agent"] == self.agent_id and msg["status"] == "unread"
        ]
        return json.dumps(unread_messages, indent=2)
    
    def run(self) -> str:
        """Execute the communication operation."""
        operations = {
            "send_message": self._send_message,
            "get_messages": self._get_messages,
            "mark_read": self._mark_read,
            "get_unread": self._get_unread
        }
        
        if self.operation not in operations:
            return f"Error: Invalid operation. Must be one of {list(operations.keys())}"
        
        return operations[self.operation]()

if __name__ == "__main__":
    # Test the communication functionality
    tool = CommunicationTool(
        operation="send_message",
        message_data={
            "from_agent": "AgentA",
            "to_agent": "AgentB",
            "content": "Test message",
            "priority": "high",
            "type": "task"
        }
    )
    print("Sending message:", tool.run())
    
    tool = CommunicationTool(
        operation="get_messages",
        agent_id="AgentB"
    )
    print("\nGetting messages for AgentB:", tool.run()) 