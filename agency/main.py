import os
import logging
from dotenv import load_dotenv
import httpx
from openai import AzureOpenAI
from agents.TaskOrchestrator.task_orchestrator_agent import TaskOrchestratorAgent
from database.db import db
from monitoring.metrics import initialize_monitoring, API_REQUESTS, AGENT_HEALTH
from utils.rate_limiter import API_RATE_LIMITER
from security.auth import security_manager
from utils.backup import backup_manager
from monitoring.alerts import alert_manager
import logging.config
from config import LOGGING_CONFIG

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def initialize_services():
    """Initialize all required services"""
    try:
        # Initialize monitoring
        initialize_monitoring()
        
        # Test database connection
        db.get_connection()
        
        # Create initial backup
        backup_manager.create_backup()
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.critical(f"Failed to initialize services: {str(e)}")
        raise

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Print environment variables for debugging
        print("Environment variables:")
        print(f"AZURE_OPENAI_KEY: {os.getenv('AZURE_OPENAI_KEY')[:10]}...")
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
            http_client=http_client
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
        
        # Initialize services
        initialize_services()
        
        # Initialize agents with authentication
        task_orchestrator = TaskOrchestratorAgent(client=client)
        token = security_manager.generate_token("task_orchestrator")
        
        # Set up health monitoring for agents
        AGENT_HEALTH.labels(agent_name="task_orchestrator").set(1)
        
        # Start interactive session with rate limiting
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() == "exit":
                    break
                
                # Apply rate limiting
                if not API_RATE_LIMITER.is_allowed("user_input"):
                    print("Rate limit exceeded. Please wait.")
                    continue
                
                # Track API requests
                API_REQUESTS.labels(endpoint="chat").inc()
                
                response = task_orchestrator.chat(user_input, token=token)
                print("TaskOrchestrator:", response)
                
            except KeyboardInterrupt:
                logger.info("Session terminated by user")
                break
            except Exception as e:
                logger.error(f"Error during chat: {str(e)}")
                alert_manager.send_alert("error_rate", str(e))
                continue
                
    except Exception as e:
        logger.critical(f"Critical error in main: {str(e)}")
        alert_manager.send_alert("critical_error", str(e))
        raise
    finally:
        # Create backup before shutting down
        backup_manager.create_backup()
        logger.info("Session ended")

if __name__ == "__main__":
    main() 