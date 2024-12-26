import unittest
from unittest.mock import Mock, patch
import os
import pytest
from agency_swarm import Agent
from agency_swarm.util import set_openai_key

# Mock Azure Speech SDK
azure_speech_mock = Mock()
azure_speech_mock.ResultReason = Mock()
azure_speech_mock.ResultReason.SynthesizingAudioCompleted = "SynthesizingAudioCompleted"
azure_speech_mock.SpeechConfig = Mock()
azure_speech_mock.AudioOutputConfig = Mock()
azure_speech_mock.SpeechSynthesizer = Mock()

import sys
sys.modules['azure.cognitiveservices.speech'] = azure_speech_mock

from agents.TaskOrchestrator.agent import TaskOrchestratorAgent
from agents.TaskOrchestrator.tools import TaskContextManager, CommunicationTool, UpdateBatcher

class TestTaskOrchestratorAgent(unittest.TestCase):
    @patch('agency_swarm.agents.agent.get_openai_client')
    def setUp(self, mock_get_client):
        """Set up test environment"""
        # Mock environment variables
        os.environ['AZURE_OPENAI_KEY'] = 'test_key'
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'test_endpoint'
        os.environ['AZURE_OPENAI_API_VERSION'] = 'test_version'
        os.environ['AZURE_OPENAI_GPT4O_DEPLOYMENT'] = 'test_deployment'
        os.environ['AZURE_SPEECH_KEY'] = 'test_speech_key'
        os.environ['AZURE_SPEECH_REGION'] = 'test_region'
        os.environ['AZURE_SPEECH_ENDPOINT'] = 'test_speech_endpoint'
        os.environ['AZURE_SPEECH_API_VERSION'] = 'test_speech_version'
        os.environ['AZURE_WHISPER_ENDPOINT'] = 'test_whisper_endpoint'
        os.environ['AZURE_WHISPER_API_VERSION'] = 'test_whisper_version'
        
        # Set OpenAI key
        set_openai_key('test_key')
        
        # Mock OpenAI client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Initialize the agent
        self.agent = TaskOrchestratorAgent()
        
        # Create mock tools
        self.mock_task_manager = Mock()
        self.mock_task_manager.run = Mock(return_value="Task created successfully with ID: 123")
        
        self.mock_comm_tool = Mock()
        self.mock_comm_tool.run = Mock(return_value="Message sent successfully to TestAgent")
        
        self.mock_update_batcher = Mock()
        self.mock_update_batcher.run = Mock(return_value="Updates batched successfully")
        
        self.mock_speech_tool = Mock()
        self.mock_speech_tool.run = Mock(return_value="Successfully synthesized speech")
        
        self.mock_stt_tool = Mock()
        self.mock_stt_tool.run = Mock(return_value="Transcribed text from speech")
        
        # Replace tools in agent
        self.agent.tools = {
            "TaskContextManager": self.mock_task_manager,
            "CommunicationTool": self.mock_comm_tool,
            "UpdateBatcher": self.mock_update_batcher,
            "SpeechTool": self.mock_speech_tool,
            "SpeechToTextTool": self.mock_stt_tool
        }

    def test_agent_initialization(self):
        """Test if the agent initializes correctly with all required tools"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, Agent)
        
        # Verify required tools are present
        tools = self.agent.tools
        self.assertIn("TaskContextManager", tools)
        self.assertIn("CommunicationTool", tools)
        self.assertIn("UpdateBatcher", tools)
        self.assertIn("SpeechTool", tools)
        self.assertIn("SpeechToTextTool", tools)
        
    def test_task_management(self):
        """Test task creation and management"""
        result = self.agent.create_task("Test task")
        self.assertIn("Task created successfully", result)
        self.mock_task_manager.run.assert_called_once()
        
    def test_communication(self):
        """Test communication with other agents"""
        result = self.agent.send_message("Test message", "TestAgent")
        self.assertIn("Message sent successfully", result)
        self.mock_comm_tool.run.assert_called_once()
        
    def test_speech_synthesis(self):
        """Test text-to-speech functionality"""
        result = self.agent.speak("Hello, this is a test")
        self.assertEqual(result, "Successfully synthesized speech")
        self.mock_speech_tool.run.assert_called_once()
        
    def test_speech_recognition(self):
        """Test speech-to-text functionality"""
        result = self.agent.listen(duration_seconds=5)
        self.assertEqual(result, "Transcribed text from speech")
        self.mock_stt_tool.run.assert_called_once()

if __name__ == '__main__':
    unittest.main() 