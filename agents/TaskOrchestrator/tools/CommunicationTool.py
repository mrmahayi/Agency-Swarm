from agency_swarm.tools import BaseTool
from pydantic import Field, PrivateAttr
from datetime import datetime
from pathlib import Path
import json
import uuid
import os
from typing import Dict, Optional, List

class CommunicationTool(BaseTool):
    """
    Enhanced tool for managing verbose communication between agents.
    Provides detailed message tracking, context preservation, and comprehensive logging.
    """
    
    operation: str = Field(
        ...,
        description="Operation to perform: 'send_message', 'broadcast', 'get_messages', 'mark_read', 'get_unread', 'get_thread', 'update_status', 'get_context'"
    )
    
    message_data: Optional[Dict] = Field(
        default=None,
        description="""
        Message data including:
        - from_agent: str - Sender agent ID
        - to_agent: str - Recipient agent ID
        - content: str - Message content
        - priority: int (1-5) - Message priority
        - context: Dict - Additional context (task_id, related_messages, etc.)
        - metadata: Dict - Message metadata (type, category, tags, etc.)
        - action_required: bool - Whether the message requires action
        - expected_response: str - Type of response expected
        - deadline: str - ISO datetime for required response
        """
    )
    
    agent_id: Optional[str] = Field(
        default=None,
        description="Agent ID for retrieving messages"
    )
    
    message_id: Optional[str] = Field(
        default=None,
        description="Message ID for operations on specific messages"
    )
    
    thread_id: Optional[str] = Field(
        default=None,
        description="Thread ID for thread-related operations"
    )
    
    # Private attributes for file paths
    _messages_dir: Path = PrivateAttr()
    _messages_file: Path = PrivateAttr()
    _context_file: Path = PrivateAttr()
    
    def __init__(self, **data):
        super().__init__(**data)
        # Initialize directories and files
        self._messages_dir = Path("messages")
        self._messages_dir.mkdir(exist_ok=True)
        self._messages_file = self._messages_dir / "messages.json"
        self._context_file = self._messages_dir / "context.json"
        
        # Initialize files if they don't exist
        if not self._messages_file.exists():
            self._save_messages({})
        if not self._context_file.exists():
            self._save_context({})
    
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
    
    def _load_context(self) -> Dict:
        """Load context information from JSON file."""
        if self._context_file.exists():
            with open(self._context_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_context(self, context: Dict):
        """Save context information to JSON file."""
        with open(self._context_file, 'w') as f:
            json.dump(context, f, indent=2)
    
    def _create_message_object(self, message_data: Dict) -> Dict:
        """Create a detailed message object with metadata and context."""
        message_id = self._generate_message_id()
        thread_id = message_data.get('thread_id', message_id)
        
        return {
            "id": message_id,
            "thread_id": thread_id,
            "timestamp": datetime.now().isoformat(),
            "from_agent": message_data.get("from_agent"),
            "to_agent": message_data.get("to_agent"),
            "content": message_data.get("content"),
            "priority": message_data.get("priority", 3),
            "status": "unread",
            "context": {
                "task_id": message_data.get("context", {}).get("task_id"),
                "related_messages": message_data.get("context", {}).get("related_messages", []),
                "conversation_state": message_data.get("context", {}).get("conversation_state", {}),
                "environment_state": message_data.get("context", {}).get("environment_state", {})
            },
            "metadata": {
                "type": message_data.get("metadata", {}).get("type", "general"),
                "category": message_data.get("metadata", {}).get("category", "information"),
                "tags": message_data.get("metadata", {}).get("tags", []),
                "source_context": message_data.get("metadata", {}).get("source_context", {}),
                "importance": message_data.get("metadata", {}).get("importance", "normal")
            },
            "action_required": message_data.get("action_required", False),
            "expected_response": message_data.get("expected_response"),
            "deadline": message_data.get("deadline"),
            "read_timestamp": None,
            "response_timestamp": None,
            "status_history": [{
                "status": "created",
                "timestamp": datetime.now().isoformat(),
                "details": "Message created"
            }]
        }
    
    def run(self):
        """Execute the requested communication operation with enhanced verbosity."""
        try:
            if self.operation == "send_message":
                if not self.message_data:
                    return "Error: message_data is required for sending a message"
                
                # Create detailed message object
                message = self._create_message_object(self.message_data)
                
                # Save message
                messages = self._load_messages()
                messages[message["id"]] = message
                self._save_messages(messages)
                
                # Update context
                context = self._load_context()
                if message["thread_id"] not in context:
                    context[message["thread_id"]] = {
                        "created_at": message["timestamp"],
                        "last_updated": message["timestamp"],
                        "participants": [message["from_agent"], message["to_agent"]],
                        "message_count": 1,
                        "status": "active",
                        "summary": f"Thread started by {message['from_agent']}"
                    }
                else:
                    context[message["thread_id"]]["last_updated"] = message["timestamp"]
                    context[message["thread_id"]]["message_count"] += 1
                    if message["to_agent"] not in context[message["thread_id"]]["participants"]:
                        context[message["thread_id"]]["participants"].append(message["to_agent"])
                
                self._save_context(context)
                
                return json.dumps({
                    "status": "success",
                    "message": "Message sent successfully",
                    "message_id": message["id"],
                    "thread_id": message["thread_id"],
                    "timestamp": message["timestamp"],
                    "details": message
                }, indent=2)
            
            elif self.operation == "get_thread":
                if not self.thread_id:
                    return "Error: thread_id is required for retrieving thread"
                
                messages = self._load_messages()
                context = self._load_context()
                
                thread_messages = {
                    k: v for k, v in messages.items()
                    if v["thread_id"] == self.thread_id
                }
                
                thread_context = context.get(self.thread_id, {})
                
                return json.dumps({
                    "thread_id": self.thread_id,
                    "context": thread_context,
                    "messages": thread_messages,
                    "message_count": len(thread_messages)
                }, indent=2)
            
            elif self.operation == "update_status":
                if not self.message_id or not self.message_data or "status" not in self.message_data:
                    return "Error: message_id and new status are required"
                
                messages = self._load_messages()
                if self.message_id not in messages:
                    return f"Error: Message {self.message_id} not found"
                
                message = messages[self.message_id]
                new_status = self.message_data["status"]
                
                # Update status and add to history
                message["status"] = new_status
                message["status_history"].append({
                    "status": new_status,
                    "timestamp": datetime.now().isoformat(),
                    "details": self.message_data.get("status_details", "Status updated")
                })
                
                # Update specific timestamps based on status
                if new_status == "read":
                    message["read_timestamp"] = datetime.now().isoformat()
                elif new_status == "responded":
                    message["response_timestamp"] = datetime.now().isoformat()
                
                self._save_messages(messages)
                
                return json.dumps({
                    "status": "success",
                    "message": f"Message {self.message_id} status updated to {new_status}",
                    "details": message
                }, indent=2)
            
            elif self.operation == "get_context":
                if not self.agent_id:
                    return "Error: agent_id is required for getting context"
                
                messages = self._load_messages()
                context = self._load_context()
                
                # Get all threads involving the agent
                agent_threads = {
                    thread_id: thread_data
                    for thread_id, thread_data in context.items()
                    if self.agent_id in thread_data["participants"]
                }
                
                # Get recent messages involving the agent
                recent_messages = {
                    msg_id: msg
                    for msg_id, msg in messages.items()
                    if msg["from_agent"] == self.agent_id or msg["to_agent"] == self.agent_id
                }
                
                return json.dumps({
                    "agent_id": self.agent_id,
                    "active_threads": agent_threads,
                    "recent_messages": recent_messages,
                    "thread_count": len(agent_threads),
                    "unread_count": sum(1 for msg in recent_messages.values() 
                                     if msg["to_agent"] == self.agent_id and msg["status"] == "unread")
                }, indent=2)
            
            # Existing operations remain but use enhanced message object
            elif self.operation == "get_messages":
                return self._get_messages()
            elif self.operation == "mark_read":
                return self._mark_read()
            elif self.operation == "get_unread":
                return self._get_unread()
            else:
                return f"Error: Unknown operation {self.operation}"
                
        except Exception as e:
            return f"Error during {self.operation} operation: {str(e)}"

if __name__ == "__main__":
    # Test the enhanced communication functionality
    print("Testing Enhanced CommunicationTool...")
    
    # Test sending a detailed message
    print("\nTesting send_message with enhanced context...")
    tool = CommunicationTool(
        operation="send_message",
        message_data={
            "from_agent": "TaskOrchestrator",
            "to_agent": "WebAutomation",
            "content": "Begin performance analysis of example.com",
            "priority": 2,
            "context": {
                "task_id": "task_123",
                "conversation_state": {
                    "current_phase": "initialization",
                    "previous_action": "task_assignment"
                },
                "environment_state": {
                    "system_load": "normal",
                    "available_resources": ["chrome_browser", "network_monitor"]
                }
            },
            "metadata": {
                "type": "task_assignment",
                "category": "performance_analysis",
                "tags": ["web_performance", "automation", "analysis"],
                "importance": "high"
            },
            "action_required": True,
            "expected_response": "acknowledgment",
            "deadline": (datetime.now() + timedelta(minutes=5)).isoformat()
        }
    )
    result = tool.run()
    print(result)
    message_data = json.loads(result)
    message_id = message_data["message_id"]
    thread_id = message_data["thread_id"]
    
    # Test getting thread context
    print("\nTesting get_thread...")
    tool = CommunicationTool(
        operation="get_thread",
        thread_id=thread_id
    )
    result = tool.run()
    print(result)
    
    # Test updating message status
    print("\nTesting update_status...")
    tool = CommunicationTool(
        operation="update_status",
        message_id=message_id,
        message_data={
            "status": "acknowledged",
            "status_details": "Task received and acknowledged by WebAutomation agent"
        }
    )
    result = tool.run()
    print(result)
    
    # Test getting agent context
    print("\nTesting get_context...")
    tool = CommunicationTool(
        operation="get_context",
        agent_id="WebAutomation"
    )
    result = tool.run()
    print(result)
    
    # Clean up test files
    print("\nCleaning up test files...")
    import shutil
    if os.path.exists("messages"):
        shutil.rmtree("messages") 