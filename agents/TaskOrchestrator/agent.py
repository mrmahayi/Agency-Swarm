import os
from agency_swarm import Agent
from .tools import (
    TaskContextManager, 
    CommunicationTool, 
    UpdateBatcher,
    SpeechTool,
    SpeechToTextTool
)

class TaskOrchestratorAgent(Agent):
    """Task Orchestrator Agent responsible for managing tasks and coordinating other agents."""
    
    def __init__(self):
        super().__init__(
            name="TaskOrchestrator",
            description="Manages tasks and coordinates other agents",
            instructions="./instructions.md",
            tools=[TaskContextManager, CommunicationTool, UpdateBatcher, SpeechTool, SpeechToTextTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def create_task(self, task_description):
        """Create a new task."""
        return self.tools["TaskContextManager"].run({"action": "create", "description": task_description})
        
    def send_message(self, message, target_agent):
        """Send a message to another agent."""
        return self.tools["CommunicationTool"].run({"message": message, "target": target_agent})
        
    def speak(self, text, voice_name="en-US-JennyNeural"):
        """Convert text to speech."""
        return self.tools["SpeechTool"].run({"text": text, "voice_name": voice_name})
        
    def listen(self, duration_seconds=10, detailed_output=False):
        """Listen and convert speech to text."""
        return self.tools["SpeechToTextTool"].run({"duration_seconds": duration_seconds, "detailed_output": detailed_output}) 