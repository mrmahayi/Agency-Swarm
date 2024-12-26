import os
from agency_swarm import Agent
from .tools.TaskContextManager import TaskContextManager
from .tools.UpdateBatcher import UpdateBatcher
from .tools.SpeechTool import SpeechTool
from .tools.SpeechToTextTool import SpeechToTextTool

class TaskOrchestratorAgent(Agent):
    """Task Orchestrator Agent responsible for managing tasks and coordinating other agents."""
    
    def __init__(self):
        super().__init__(
            name="TaskOrchestrator",
            description="Manages tasks and coordinates other agents",
            instructions="./instructions.md",
            tools=[TaskContextManager, UpdateBatcher, SpeechTool, SpeechToTextTool],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
    def create_task(self, task_description):
        """Create a new task."""
        tool = TaskContextManager(operation="create_task")
        return tool.run({"action": "create", "description": task_description})
        
    def send_message(self, message, target_agent):
        """Send a message to another agent."""
        tool = UpdateBatcher(operation="add_update")
        return tool.run({"operation": "add_update", "update_data": {"content": message, "target": target_agent}})
        
    def speak(self, text, voice_name="en-US-JennyNeural"):
        """Convert text to speech."""
        tool = SpeechTool(text=text, voice_name=voice_name)
        return tool.run()
        
    def listen(self, duration_seconds=10, detailed_output=False):
        """Listen and convert speech to text."""
        tool = SpeechToTextTool(duration_seconds=duration_seconds, detailed_output=detailed_output)
        return tool.run() 