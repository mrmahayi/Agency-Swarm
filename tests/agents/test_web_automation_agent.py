import unittest
from unittest.mock import Mock, patch
import os
import pytest
from agency_swarm import Agent
from agency_swarm.util import set_openai_key

# Mock required modules
playwright_mock = Mock()
playwright_mock.sync_api = Mock()
playwright_mock.sync_api.sync_playwright = Mock()

import sys
sys.modules['playwright'] = playwright_mock
sys.modules['playwright.sync_api'] = playwright_mock.sync_api

from agents.WebAutomation.agent import WebAutomationAgent

class TestWebAutomationAgent(unittest.TestCase):
    @patch('agency_swarm.agents.agent.get_openai_client')
    def setUp(self, mock_get_client):
        """Set up test environment"""
        # Mock environment variables
        os.environ['AZURE_OPENAI_KEY'] = 'test_key'
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'test_endpoint'
        os.environ['AZURE_OPENAI_API_VERSION'] = 'test_version'
        os.environ['AZURE_OPENAI_GPT4O_DEPLOYMENT'] = 'test_deployment'
        
        # Set OpenAI key
        set_openai_key('test_key')
        
        # Mock OpenAI client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Initialize the agent
        self.agent = WebAutomationAgent()
        
        # Create mock tools
        self.mock_browser_tool = Mock()
        self.mock_browser_tool.run = Mock(return_value={"status": "success", "content": "Test content"})
        
        self.mock_file_tool = Mock()
        self.mock_file_tool.run = Mock(return_value={"status": "success"})
        
        # Replace tools in agent
        self.agent.tools = {
            "BrowserTool": self.mock_browser_tool,
            "FileManagementTool": self.mock_file_tool
        }

    def test_agent_initialization(self):
        """Test if the agent initializes correctly with all required tools"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, Agent)
        
        # Verify required tools are present
        tools = self.agent.tools
        self.assertIn("BrowserTool", tools)
        self.assertIn("FileManagementTool", tools)
        
    def test_web_navigation(self):
        """Test web navigation functionality"""
        result = self.agent.navigate_to("http://test.com")
        self.assertEqual(result["status"], "success")
        self.mock_browser_tool.run.assert_called_once()
        
    def test_web_interaction(self):
        """Test web interaction functionality"""
        result = self.agent.click_element("#test-button")
        self.assertEqual(result["status"], "success")
        self.mock_browser_tool.run.assert_called()

    def test_file_download(self):
        """Test file download functionality"""
        result = self.agent.download_file("http://test.com/file.pdf", "downloads/file.pdf")
        self.assertEqual(result["status"], "success")
        self.mock_file_tool.run.assert_called_once_with({
            "action": "download",
            "url": "http://test.com/file.pdf",
            "save_path": "downloads/file.pdf"
        })

    def test_file_upload(self):
        """Test file upload functionality"""
        result = self.agent.upload_file("uploads/test.pdf", "#file-input")
        self.assertEqual(result["status"], "success")
        self.mock_file_tool.run.assert_called_once_with({
            "action": "upload",
            "file_path": "uploads/test.pdf",
            "selector": "#file-input"
        })

if __name__ == '__main__':
    unittest.main() 