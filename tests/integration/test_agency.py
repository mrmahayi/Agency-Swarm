import unittest
import os
from unittest.mock import Mock, patch
from agency import validate_environment, initialize_openai_client, initialize_agency

class TestAgency(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        os.environ['AZURE_OPENAI_KEY'] = 'test_key'
        os.environ['AZURE_OPENAI_ENDPOINT'] = 'test_endpoint'
        os.environ['AZURE_OPENAI_API_VERSION'] = 'test_version'
        os.environ['AZURE_OPENAI_GPT4O_DEPLOYMENT'] = 'test_deployment'

    def test_validate_environment(self):
        # Test environment validation
        validate_environment()  # Should not raise any exception

        # Test missing variable
        del os.environ['AZURE_OPENAI_KEY']
        with self.assertRaises(EnvironmentError):
            validate_environment()

    @patch('openai.AzureOpenAI')
    def test_initialize_openai_client(self, mock_azure):
        # Mock the OpenAI client
        mock_client = Mock()
        mock_azure.return_value = mock_client
        
        # Test client initialization
        client = initialize_openai_client()
        self.assertIsNotNone(client)

    @patch('agency_swarm.Agency')
    def test_initialize_agency(self, mock_agency):
        # Mock the Agency class
        mock_agency_instance = Mock()
        mock_agency.return_value = mock_agency_instance
        
        # Test agency initialization
        agency, task_orchestrator = initialize_agency()
        self.assertIsNotNone(agency)
        self.assertIsNotNone(task_orchestrator)

if __name__ == '__main__':
    unittest.main() 