import os
from agency_swarm import Agent

class DesktopInteractionAgent(Agent):
    """
    Agent responsible for desktop automation and system interaction tasks.
    """
    def __init__(self):
        super().__init__(
            name="DesktopInteraction",
            description="Manages desktop automation and system interactions",
            instructions="./instructions.md",
            tools=[],  # Add desktop interaction tools here
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        ) 