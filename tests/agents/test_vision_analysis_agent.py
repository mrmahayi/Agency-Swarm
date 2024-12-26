import unittest
from unittest.mock import Mock, patch
import os
import pytest
from agency_swarm import Agent
from agency_swarm.util import set_openai_key

# Mock required modules
cv2_mock = Mock()
cv2_mock.VideoCapture = Mock()
cv2_mock.VideoCapture.return_value.read = Mock(return_value=(True, "test_image"))
cv2_mock.imwrite = Mock(return_value=True)
cv2_mock.__version__ = '4.0.0'

import sys
sys.modules['cv2'] = cv2_mock

# Mock plotly
plotly_mock = Mock()
sys.modules['plotly'] = plotly_mock
sys.modules['plotly.graph_objects'] = Mock()
sys.modules['plotly.express'] = Mock()

# Mock pyautogui
pyautogui_mock = Mock()
pyautogui_mock.screenshot = Mock()
pyautogui_mock.screenshot.return_value.save = Mock()
sys.modules['pyautogui'] = pyautogui_mock

from agents.VisionAnalysis.agent import VisionAnalysisAgent

class TestVisionAnalysisAgent(unittest.TestCase):
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
        self.agent = VisionAnalysisAgent()
        
        # Create mock tools
        self.mock_vision_tool = Mock()
        self.mock_vision_tool.run = Mock(return_value={"description": "A test image", "tags": ["test"]})
        
        self.mock_camera_tool = Mock()
        self.mock_camera_tool.run = Mock(return_value={"status": "success", "image_path": "test_capture.jpg"})
        
        self.mock_visualization_tool = Mock()
        self.mock_visualization_tool.run = Mock(return_value="visualization.html")
        
        self.mock_screenshot_tool = Mock()
        self.mock_screenshot_tool.run = Mock(return_value="screenshot.png")
        
        # Replace tools in agent
        self.agent.tools = {
            "AzureVisionTool": self.mock_vision_tool,
            "CameraTool": self.mock_camera_tool,
            "VisualizationTool": self.mock_visualization_tool,
            "ScreenshotTool": self.mock_screenshot_tool
        }

    def test_agent_initialization(self):
        """Test if the agent initializes correctly with all required tools"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, Agent)
        
        # Verify required tools are present
        tools = self.agent.tools
        self.assertIn("AzureVisionTool", tools)
        self.assertIn("CameraTool", tools)
        self.assertIn("VisualizationTool", tools)
        self.assertIn("ScreenshotTool", tools)
        
    def test_image_analysis(self):
        """Test image analysis functionality"""
        result = self.agent.analyze_image("test_image.jpg")
        self.assertIn("description", result)
        self.mock_vision_tool.run.assert_called_once()
        
    def test_camera_functionality(self):
        """Test camera operations"""
        result = self.agent.capture_image()
        self.assertEqual(result["status"], "success")
        self.mock_camera_tool.run.assert_called_once()

    def test_visualization_functionality(self):
        """Test visualization functionality"""
        result = self.agent.create_visualization("workload_distribution")
        self.assertEqual(result, "visualization.html")
        self.mock_visualization_tool.run.assert_called_once()

    def test_screenshot_functionality(self):
        """Test screenshot functionality"""
        result = self.agent.take_screenshot()
        self.assertEqual(result, "screenshot.png")
        self.mock_screenshot_tool.run.assert_called_once()

if __name__ == '__main__':
    unittest.main() 