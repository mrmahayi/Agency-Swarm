import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
from agency_swarm.agency import Agency
from agency_swarm.util import set_openai_key
from agency_swarm.tools import BaseTool
from pydantic import Field

# Import agents
from agents.TaskOrchestrator.agent import TaskOrchestratorAgent
from agents.Research.agent import ResearchAgent
from agents.VisionAnalysis.agent import VisionAnalysisAgent
from agents.DesktopInteraction.agent import DesktopInteractionAgent
from agents.WebAutomation.agent import WebAutomationAgent

# Mock tool for testing
class MockTool(BaseTool):
    """A mock tool for testing."""
    test_field: str = Field(..., description="Test field")

    def run(self):
        """Mock run method."""
        return "Mock tool executed"

class TestAgency(unittest.TestCase):
    """Test cases for Agency class."""

    @patch('agency_swarm.agents.agent.get_openai_client')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "TaskOrchestratorAgent", "id": "test_id", "model": "test_model", "temperature": 0.7, "max_tokens": 1000}]')
    def setUp(self, mock_file, mock_get_client):
        """Set up test environment"""
        # Mock environment variables
        os.environ['AZURE_OPENAI_KEY'] = 'test_key'
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'test_endpoint'
        os.environ['AZURE_OPENAI_API_VERSION'] = 'test_version'
        os.environ['AZURE_OPENAI_GPT4O_DEPLOYMENT'] = 'test_deployment'

        # Set OpenAI key
        set_openai_key('test_key')

        # Mock OpenAI client and its responses
        mock_assistant = MagicMock()
        mock_assistant.id = "test_assistant_id"
        mock_assistant.model_dump.return_value = {
            "id": "test_assistant_id",
            "name": "test_assistant",
            "model": "test_model"
        }

        mock_client = MagicMock()
        mock_client.beta.assistants.create.return_value = mock_assistant
        mock_client.beta.assistants.list.return_value.data = [mock_assistant]
        mock_get_client.return_value = mock_client

        # Initialize agents with mock tools
        self.task_orchestrator = TaskOrchestratorAgent()
        self.task_orchestrator.tools = [MockTool]

        self.research = ResearchAgent()
        self.research.tools = [MockTool]

        self.vision = VisionAnalysisAgent()
        self.vision.tools = [MockTool]

        self.desktop = DesktopInteractionAgent()
        self.desktop.tools = [MockTool]

        self.web = WebAutomationAgent()
        self.web.tools = [MockTool]

        # Create agency
        self.agency = Agency(
            [
                self.task_orchestrator,  # Entry point for user communication
                [self.task_orchestrator, self.research],  # Task Orchestrator can communicate with Research
                [self.task_orchestrator, self.vision],  # Task Orchestrator can communicate with Vision
                [self.task_orchestrator, self.desktop],  # Task Orchestrator can communicate with Desktop
                [self.task_orchestrator, self.web],  # Task Orchestrator can communicate with Web
                [self.research, self.web],  # Research can communicate with Web
                [self.vision, self.desktop]  # Vision can communicate with Desktop
            ],
            shared_instructions="agency/agency_manifesto.md"
        )

    def test_agency_initialization(self):
        """Test agency initialization."""
        self.assertIsInstance(self.agency, Agency)
        self.assertEqual(len(self.agency.agents), 5)  # Total number of agents
        self.assertEqual(self.agency.agents[0], self.task_orchestrator)  # Entry point agent

    def test_communication_flows(self):
        """Test communication flows between agents."""
        # Test Task Orchestrator communication flows
        task_orchestrator_threads = self.agency.agents_and_threads[self.task_orchestrator.name]
        self.assertIn(self.research.name, task_orchestrator_threads)
        self.assertIn(self.vision.name, task_orchestrator_threads)
        self.assertIn(self.desktop.name, task_orchestrator_threads)
        self.assertIn(self.web.name, task_orchestrator_threads)

        # Test Research Agent communication flows
        research_threads = self.agency.agents_and_threads[self.research.name]
        self.assertIn(self.web.name, research_threads)

        # Test Vision Agent communication flows
        vision_threads = self.agency.agents_and_threads[self.vision.name]
        self.assertIn(self.desktop.name, vision_threads)

    def test_shared_instructions(self):
        """Test shared instructions are properly loaded."""
        self.assertIsNotNone(self.agency.shared_instructions)
        self.assertIsInstance(self.agency.shared_instructions, str)

    def test_task_execution(self):
        """Test task execution through the agency."""
        # Mock the run method of MockTool
        MockTool.run = MagicMock(return_value="Task executed successfully")

        # Test task execution
        tool = self.agency.agents[0].tools[0](test_field="test value")
        result = tool.run()
        self.assertEqual(result, "Task executed successfully")

if __name__ == '__main__':
    unittest.main() 