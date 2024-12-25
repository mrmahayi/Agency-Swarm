from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from datetime import datetime
from typing import Optional, Dict, List, Any

class MessageAnalyticsTool(BaseTool):
    """
    Tool for analyzing message content, determining intent, and extracting relevant information.
    """
    
    message: str = Field(
        ...,
        description="The message to analyze"
    )
    
    operation: str = Field(
        ...,
        description="The operation to perform: analyze_intent, extract_entities, analyze_sentiment"
    )
    
    def run(self) -> str:
        """Execute the message analysis operation."""
        try:
            if self.operation == "analyze_intent":
                return self._analyze_intent()
            elif self.operation == "extract_entities":
                return self._extract_entities()
            elif self.operation == "analyze_sentiment":
                return self._analyze_sentiment()
            else:
                return f"Unknown operation: {self.operation}"
        
        except Exception as e:
            return f"Error in MessageAnalyticsTool: {str(e)}"
    
    def _analyze_intent(self) -> str:
        """Analyze the intent of the message."""
        message_lower = self.message.lower()
        intents = []
        
        # Task creation patterns
        task_creation_patterns = [
            "create", "make", "start", "begin", "initiate",
            "need to", "want to", "would like to",
            "can you", "please", "help"
        ]
        
        # Task status patterns
        task_status_patterns = [
            "status", "progress", "update", "how is",
            "what's happening", "where are we",
            "check", "track", "monitor"
        ]
        
        # Task update patterns
        task_update_patterns = [
            "update", "change", "modify", "edit",
            "revise", "adjust", "set", "mark as"
        ]
        
        # Check for task creation intent
        if any(pattern in message_lower for pattern in task_creation_patterns):
            intents.append("task_creation")
        
        # Check for task status intent
        if any(pattern in message_lower for pattern in task_status_patterns):
            intents.append("task_status")
        
        # Check for task update intent
        if any(pattern in message_lower for pattern in task_update_patterns):
            intents.append("task_update")
        
        # If no specific intent is found, mark as general query
        if not intents:
            intents.append("general_query")
        
        return json.dumps(intents)
    
    def _extract_entities(self) -> str:
        """Extract entities from the message."""
        entities = {
            "task_ids": [],
            "agent_names": [],
            "dates": [],
            "priorities": [],
            "urls": []
        }
        
        message_words = self.message.split()
        
        # Extract task IDs
        import re
        task_ids = re.findall(r'task_\d{8}_\d{6}(?:_[a-f0-9]+)?', self.message)
        if task_ids:
            entities["task_ids"] = task_ids
        
        # Extract agent names
        agent_patterns = [
            "TaskOrchestrator",
            "WebAutomation",
            "DesktopInteraction",
            "VisionAnalysis",
            "Research"
        ]
        for word in message_words:
            if word in agent_patterns:
                entities["agent_names"].append(word)
        
        # Extract dates
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}'   # DD-MM-YYYY
        ]
        for pattern in date_patterns:
            dates = re.findall(pattern, self.message)
            entities["dates"].extend(dates)
        
        # Extract priorities
        priority_patterns = [
            r'priority[: ]*(\d)',
            r'p(\d)',
            r'urgent',
            r'high priority',
            r'low priority'
        ]
        for pattern in priority_patterns:
            priorities = re.findall(pattern, self.message.lower())
            if priorities:
                entities["priorities"].extend(priorities)
        
        # Extract URLs
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*', self.message)
        if urls:
            entities["urls"] = urls
        
        return json.dumps(entities, indent=2)
    
    def _analyze_sentiment(self) -> str:
        """Analyze the sentiment of the message."""
        message_lower = self.message.lower()
        
        # Simple sentiment analysis based on keyword matching
        positive_words = [
            "good", "great", "excellent", "amazing", "wonderful",
            "fantastic", "perfect", "thanks", "thank you", "pleased",
            "happy", "successful", "success", "well done"
        ]
        
        negative_words = [
            "bad", "poor", "terrible", "awful", "horrible",
            "failed", "failure", "error", "problem", "issue",
            "wrong", "broken", "not working", "disappointed"
        ]
        
        urgent_words = [
            "urgent", "asap", "emergency", "immediately", "critical",
            "important", "priority", "urgent", "rush"
        ]
        
        # Count sentiment words
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        urgent_count = sum(1 for word in urgent_words if word in message_lower)
        
        # Determine overall sentiment
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Add urgency if urgent words are found
        urgency = "urgent" if urgent_count > 0 else "normal"
        
        result = {
            "sentiment": sentiment,
            "urgency": urgency,
            "metrics": {
                "positive_words": positive_count,
                "negative_words": negative_count,
                "urgent_words": urgent_count
            }
        }
        
        return json.dumps(result, indent=2)

if __name__ == "__main__":
    # Test the tool
    test_messages = [
        "Can you create a new task to analyze our website performance?",
        "What's the status of task_20241225_123456?",
        "Please update task_20241225_123456 to completed",
        "I need urgent help with the WebAutomation agent",
        "Great job on completing the task! The results are excellent.",
        "There's an error in the task execution, please fix it ASAP."
    ]
    
    print("Testing MessageAnalyticsTool...")
    for message in test_messages:
        print(f"\nTest message: {message}")
        
        # Test intent analysis
        tool = MessageAnalyticsTool(
            message=message,
            operation="analyze_intent"
        )
        print("\nIntent analysis:")
        print(tool.run())
        
        # Test entity extraction
        tool = MessageAnalyticsTool(
            message=message,
            operation="extract_entities"
        )
        print("\nEntity extraction:")
        print(tool.run())
        
        # Test sentiment analysis
        tool = MessageAnalyticsTool(
            message=message,
            operation="analyze_sentiment"
        )
        print("\nSentiment analysis:")
        print(tool.run()) 