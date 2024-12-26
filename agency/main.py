import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from dotenv import load_dotenv
import httpx
from openai import AzureOpenAI
from agency_swarm import Agency
from agency_swarm.util import set_openai_client

from agents.TaskOrchestrator.agent import TaskOrchestratorAgent
from agents.VisionAnalysis.agent import VisionAnalysisAgent
from agents.DesktopInteraction.agent import DesktopInteractionAgent
from agents.WebAutomation.agent import WebAutomationAgent
from agents.Research.agent import ResearchAgent

# Load environment variables
load_dotenv()

# Print environment variables for debugging
print("Environment variables:")
print(f"AZURE_OPENAI_KEY: {os.getenv('AZURE_OPENAI_KEY')[:10] if os.getenv('AZURE_OPENAI_KEY') else 'Not set'}...")
print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION')}")
print(f"AZURE_OPENAI_GPT4O_DEPLOYMENT: {os.getenv('AZURE_OPENAI_GPT4O_DEPLOYMENT')}")

# Create a custom httpx client without proxies
http_client = httpx.Client(timeout=30.0)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    http_client=http_client,
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

# Test Azure OpenAI connection
try:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
        messages=[{"role": "user", "content": "Hello, are you working?"}],
        max_tokens=50
    )
    print("\nAzure OpenAI Test Response:", response.choices[0].message.content)
except Exception as e:
    print("\nError testing Azure OpenAI connection:", str(e))
    raise

# Set up OpenAI client for Agency Swarm
set_openai_client(client)

# Initialize agents
task_orchestrator = TaskOrchestratorAgent()
vision_analysis = VisionAnalysisAgent()
desktop_interaction = DesktopInteractionAgent()
web_automation = WebAutomationAgent()
research = ResearchAgent()

# Create agency with communication flows
agency = Agency([
    task_orchestrator,  # TaskOrchestrator is the entry point
    [task_orchestrator, vision_analysis],  # TaskOrchestrator can communicate with VisionAnalysis
    [task_orchestrator, desktop_interaction],  # TaskOrchestrator can communicate with DesktopInteraction
    [task_orchestrator, web_automation],  # TaskOrchestrator can communicate with WebAutomation
    [task_orchestrator, research],  # TaskOrchestrator can communicate with Research
    [vision_analysis, desktop_interaction],  # VisionAnalysis can communicate with DesktopInteraction
    [web_automation, research]  # WebAutomation can communicate with Research
], shared_instructions="agency/agency_manifesto.md")

if __name__ == "__main__":
    # Start the agency
    agency.run_demo() 