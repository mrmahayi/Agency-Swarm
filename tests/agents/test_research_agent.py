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

pypdf_mock = Mock()
pypdf_mock.PdfReader = Mock()

import sys
sys.modules['playwright'] = playwright_mock
sys.modules['playwright.sync_api'] = playwright_mock.sync_api
sys.modules['pypdf'] = pypdf_mock

from agents.Research.agent import ResearchAgent

class TestResearchAgent(unittest.TestCase):
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
        self.agent = ResearchAgent()
        
        # Create mock tools
        self.mock_search_tool = Mock()
        self.mock_search_tool.run = Mock(return_value={"results": [{"title": "Test", "url": "http://test.com"}]})
        
        self.mock_browser_tool = Mock()
        self.mock_browser_tool.run = Mock(return_value={"status": "success", "content": "Test content"})
        
        self.mock_pdf_tool = Mock()
        self.mock_pdf_tool.run = Mock(return_value="PDF processed successfully")
        
        self.mock_file_tool = Mock()
        self.mock_file_tool.run = Mock(return_value="File operation successful")
        
        # Replace tools in agent
        self.agent.tools = {
            "TavilySearchTool": self.mock_search_tool,
            "BrowserTool": self.mock_browser_tool,
            "PDFTool": self.mock_pdf_tool,
            "FileManagementTool": self.mock_file_tool
        }

    def test_agent_initialization(self):
        """Test if the agent initializes correctly with all required tools"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, Agent)
        
        # Verify required tools are present
        tools = self.agent.tools
        self.assertIn("TavilySearchTool", tools)
        self.assertIn("BrowserTool", tools)
        self.assertIn("PDFTool", tools)
        self.assertIn("FileManagementTool", tools)
        
    def test_search_functionality(self):
        """Test search functionality"""
        result = self.agent.search("test query")
        self.assertIn("results", result)
        self.mock_search_tool.run.assert_called_once()
        
    def test_browser_functionality(self):
        """Test browser automation"""
        result = self.agent.browse("http://test.com")
        self.assertEqual(result["status"], "success")
        self.mock_browser_tool.run.assert_called_once()

    def test_pdf_functionality(self):
        """Test PDF processing"""
        result = self.agent.read_pdf("test.pdf")
        self.assertEqual(result, "PDF processed successfully")
        self.mock_pdf_tool.run.assert_called_once_with({
            "action": "read",
            "file_path": "test.pdf"
        })

    def test_file_management(self):
        """Test file management operations"""
        result = self.agent.save_file("Test content", "test.txt")
        self.assertEqual(result, "File operation successful")
        self.mock_file_tool.run.assert_called_once_with({
            "action": "save",
            "content": "Test content",
            "file_path": "test.txt"
        })

if __name__ == '__main__':
    unittest.main() 