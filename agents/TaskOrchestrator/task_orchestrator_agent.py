import os
from dotenv import load_dotenv
import httpx
from openai import AzureOpenAI
from tools.TaskManagementTool import TaskManagementTool
from tools.TaskAnalyticsTool import TaskAnalyticsTool
from tools.MessageAnalyticsTool import MessageAnalyticsTool
from tools.CommunicationTool import CommunicationTool
import json
from datetime import datetime

class TaskOrchestratorAgent:
    """
    Agent responsible for managing tasks and coordinating other agents.
    """
    def __init__(self, client=None):
        load_dotenv()
        
        # Initialize Azure OpenAI client if not provided
        if client is None:
            http_client = httpx.Client(timeout=30.0)
            self.client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                http_client=http_client
            )
        else:
            self.client = client
            
        self.model = os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT")
        self.tools = [
            TaskManagementTool,
            TaskAnalyticsTool,
            MessageAnalyticsTool,
            CommunicationTool
        ]
        self.conversation_history = []
        self.task_context = {}
        
        # Load instructions
        with open("./instructions.md", "r") as f:
            self.instructions = f.read()

    def chat(self, message: str, token=None) -> str:
        """
        Process chat messages and manage tasks.
        
        Args:
            message (str): The incoming chat message
            token (str, optional): Authentication token
            
        Returns:
            str: Response message
        """
        try:
            # Add message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Create messages array for Azure OpenAI
            messages = [
                {"role": "system", "content": self.instructions},
                *[{"role": msg["role"], "content": msg["content"]} 
                  for msg in self.conversation_history[-10:]]  # Keep last 10 messages
            ]
            
            # Get response from Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response content
            response_content = response.choices[0].message.content
            
            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_content,
                "timestamp": datetime.now().isoformat()
            })
            
            return response_content
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.conversation_history.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().isoformat(),
                "error": True
            })
            return error_msg

if __name__ == "__main__":
    # Test the TaskOrchestratorAgent
    agent = TaskOrchestratorAgent()
    
    print("\nTesting greeting:")
    print(agent.chat("hi"))
    
    print("\nTesting task creation:")
    print(agent.chat("Create a task to implement new feature with high priority"))
    
    print("\nTesting task update:")
    print(agent.chat("Update task 1 with status in_progress"))
    
    print("\nTesting task listing:")
    print(agent.chat("List all tasks")) 