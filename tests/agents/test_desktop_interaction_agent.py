import unittest
from unittest.mock import Mock, patch
import os
import pytest
from agency_swarm import Agent
from agency_swarm.util import set_openai_key

# Mock required modules
pyautogui_mock = Mock()
pyperclip_mock = Mock()

import sys
sys.modules['pyautogui'] = pyautogui_mock
sys.modules['pyperclip'] = pyperclip_mock

from agents.DesktopInteraction.agent import DesktopInteractionAgent

class TestDesktopInteractionAgent(unittest.TestCase):
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
        self.agent = DesktopInteractionAgent()
        
        # Create mock tools
        self.mock_clipboard_tool = Mock()
        self.mock_clipboard_tool.run = Mock(return_value={"status": "success"})
        
        self.mock_click_tool = Mock()
        self.mock_click_tool.run = Mock(return_value={"status": "success"})
        
        self.mock_keyboard_tool = Mock()
        self.mock_keyboard_tool.run = Mock(return_value={"status": "success"})
        
        # Replace tools in agent
        self.agent.tools = {
            "ClipboardTool": self.mock_clipboard_tool,
            "ClickTool": self.mock_click_tool,
            "KeyboardTool": self.mock_keyboard_tool
        }

    def test_agent_initialization(self):
        """Test if the agent initializes correctly with all required tools"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, Agent)
        
        # Verify required tools are present
        tools = self.agent.tools
        self.assertIn("ClipboardTool", tools)
        self.assertIn("ClickTool", tools)
        self.assertIn("KeyboardTool", tools)
        
    def test_clipboard_operations(self):
        """Test clipboard functionality"""
        result = self.agent.copy_to_clipboard("test text")
        self.assertEqual(result["status"], "success")
        self.mock_clipboard_tool.run.assert_called_once()
        
    def test_mouse_operations(self):
        """Test mouse click functionality"""
        result = self.agent.click_at_position(100, 200)
        self.assertEqual(result["status"], "success")
        self.mock_click_tool.run.assert_called_once()

    def test_keyboard_typing(self):
        """Test keyboard typing functionality"""
        result = self.agent.type_text("test text")
        self.assertEqual(result["status"], "success")
        self.mock_keyboard_tool.run.assert_called_once_with({"action": "type", "text": "test text"})

    def test_keyboard_key_press(self):
        """Test keyboard key press functionality"""
        result = self.agent.press_key("enter")
        self.assertEqual(result["status"], "success")
        self.mock_keyboard_tool.run.assert_called_once_with({"action": "press", "key": "enter"})

if __name__ == '__main__':
    unittest.main() 