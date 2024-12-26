import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

import os
from dotenv import load_dotenv
from agency_swarm import Agency
from agents.task_orchestrator.task_orchestrator_agent import TaskOrchestratorAgent
from agents.research.research_agent import ResearchAgent
from agents.vision_analysis.vision_analysis_agent import VisionAnalysisAgent
from agents.desktop_interaction.desktop_interaction_agent import DesktopInteractionAgent
from agents.web_automation.web_automation_agent import WebAutomationAgent
from utils.backup import backup_manager

def main():
    # Load environment variables
    load_dotenv()
    
    # Create backup of database
    backup_manager.create_backup()
    
    # Initialize agents
    task_orchestrator = TaskOrchestratorAgent()
    research = ResearchAgent()
    vision = VisionAnalysisAgent()
    desktop = DesktopInteractionAgent()
    web = WebAutomationAgent()
    
    # Create agency with communication flows
    agency = Agency(
        [
            task_orchestrator,  # Entry point for user communication
            [task_orchestrator, research],  # Task Orchestrator can communicate with Research
            [task_orchestrator, vision],  # Task Orchestrator can communicate with Vision
            [task_orchestrator, desktop],  # Task Orchestrator can communicate with Desktop
            [task_orchestrator, web],  # Task Orchestrator can communicate with Web
            [research, web],  # Research can communicate with Web
            [vision, desktop]  # Vision can communicate with Desktop
        ],
        shared_instructions="agency/agency_manifesto.md"
    )
    
    # Run the agency
    agency.run_demo()

if __name__ == "__main__":
    main() 