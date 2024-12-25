import os
from agency_swarm import Agent
from tools.BrowserTool import BrowserTool
from tools.CommunicationTool import CommunicationTool
from tools.TaskManagementTool import TaskManagementTool
from tools.MessageAnalyticsTool import MessageAnalyticsTool
from tools.PDFTool import PDFTool
import json
from datetime import datetime

class WebAutomationAgent(Agent):
    """
    Agent responsible for web automation tasks.
    """
    def __init__(self):
        super().__init__(
            name="WebAutomation",
            description="Handles web automation tasks and browser interactions",
            instructions="./instructions.md",
            tools=[
                BrowserTool,
                CommunicationTool,
                TaskManagementTool,
                MessageAnalyticsTool,
                PDFTool
            ],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
        # Initialize state
        self.current_task = None
        self.browser_context = {}
        self.conversation_history = []
    
    def chat(self, message: str) -> str:
        """
        Process incoming chat messages and return appropriate responses.
        Analyzes message intent and performs necessary web automation tasks.
        """
        try:
            # Add message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Analyze message intent
            message_tool = MessageAnalyticsTool(
                message=message,
                operation="analyze_intent"
            )
            intents = json.loads(message_tool.run())
            
            # Extract entities from message
            entity_tool = MessageAnalyticsTool(
                message=message,
                operation="extract_entities"
            )
            entities = json.loads(entity_tool.run())
            
            # Process message based on intent
            response = self._process_intents(intents, entities, message)
            
            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.conversation_history.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().isoformat(),
                "error": True
            })
            return error_msg
    
    def _process_intents(self, intents: list, entities: dict, message: str) -> str:
        """Process message intents and generate appropriate response."""
        try:
            # Handle navigation
            if any(intent in intents for intent in ["navigate", "visit", "open_url"]):
                return self._handle_navigation(message, entities)
            
            # Handle clicking
            elif any(intent in intents for intent in ["click", "press", "select"]):
                return self._handle_clicking(message, entities)
            
            # Handle typing
            elif any(intent in intents for intent in ["type", "input", "enter"]):
                return self._handle_typing(message, entities)
            
            # Handle scraping
            elif any(intent in intents for intent in ["scrape", "extract", "get"]):
                return self._handle_scraping(message, entities)
            
            # Handle PDF generation
            elif any(intent in intents for intent in ["pdf", "save", "export"]):
                return self._handle_pdf_generation(message, entities)
            
            # Handle help request
            elif "help" in message.lower():
                return self._handle_help_request()
            
            else:
                return (
                    "I can help you with web automation tasks like:\n"
                    "- Navigating to URLs\n"
                    "- Clicking elements\n"
                    "- Typing text\n"
                    "- Scraping content\n"
                    "- Generating PDFs\n\n"
                    "What would you like me to do?"
                )
        
        except Exception as e:
            return f"Error processing intents: {str(e)}"
    
    def _handle_navigation(self, message: str, entities: dict) -> str:
        """Handle web navigation requests."""
        try:
            # Extract URL from entities or message
            url = entities.get("url")
            if not url:
                # Look for URL patterns
                import re
                patterns = [
                    r'"(https?://[^"]+)"',
                    r'url\s*=\s*(https?://\S+)',
                    r'go to\s+(https?://\S+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        url = match.group(1)
                        break
            
            if not url:
                return "Could not determine URL to navigate to"
            
            # Navigate using BrowserTool
            browser_tool = BrowserTool(
                operation="navigate",
                url=url
            )
            result = browser_tool.run()
            
            # Update browser context
            self.browser_context["navigation"] = {
                "timestamp": datetime.now().isoformat(),
                "url": url,
                "result": result
            }
            
            return f"Navigated to {url}: {result}"
            
        except Exception as e:
            return f"Error navigating: {str(e)}"
    
    def _handle_clicking(self, message: str, entities: dict) -> str:
        """Handle element clicking requests."""
        try:
            # Extract selector from entities or message
            selector = entities.get("selector")
            if not selector:
                # Look for selector patterns
                import re
                patterns = [
                    r'"([^"]+)"',
                    r'selector\s*=\s*([^\s]+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        selector = match.group(1)
                        break
            
            if not selector:
                return "Could not determine element to click"
            
            # Click using BrowserTool
            browser_tool = BrowserTool(
                operation="click",
                selector=selector
            )
            result = browser_tool.run()
            
            # Update browser context
            self.browser_context["click"] = {
                "timestamp": datetime.now().isoformat(),
                "selector": selector,
                "result": result
            }
            
            return f"Clicked element {selector}: {result}"
            
        except Exception as e:
            return f"Error clicking: {str(e)}"
    
    def _handle_typing(self, message: str, entities: dict) -> str:
        """Handle text input requests."""
        try:
            # Extract selector and text from entities or message
            selector = entities.get("selector")
            text = entities.get("text")
            
            if not selector or not text:
                # Look for selector and text patterns
                import re
                selector_match = re.search(r'into\s+"([^"]+)"', message)
                text_match = re.search(r'type\s+"([^"]+)"', message)
                
                if selector_match:
                    selector = selector_match.group(1)
                if text_match:
                    text = text_match.group(1)
            
            if not selector or not text:
                return "Could not determine element or text to type"
            
            # Type using BrowserTool
            browser_tool = BrowserTool(
                operation="type",
                selector=selector,
                text=text
            )
            result = browser_tool.run()
            
            # Update browser context
            self.browser_context["type"] = {
                "timestamp": datetime.now().isoformat(),
                "selector": selector,
                "text": text,
                "result": result
            }
            
            return f"Typed text into {selector}: {result}"
            
        except Exception as e:
            return f"Error typing: {str(e)}"
    
    def _handle_scraping(self, message: str, entities: dict) -> str:
        """Handle content scraping requests."""
        try:
            # Extract selector from entities or message
            selector = entities.get("selector")
            if not selector:
                # Look for selector patterns
                import re
                patterns = [
                    r'"([^"]+)"',
                    r'selector\s*=\s*([^\s]+)',
                    r'from\s+"([^"]+)"'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        selector = match.group(1)
                        break
            
            if not selector:
                return "Could not determine element to scrape"
            
            # Scrape using BrowserTool
            browser_tool = BrowserTool(
                operation="scrape",
                selector=selector
            )
            result = browser_tool.run()
            
            # Update browser context
            self.browser_context["scrape"] = {
                "timestamp": datetime.now().isoformat(),
                "selector": selector,
                "result": result
            }
            
            return f"Scraped content from {selector}:\n{result}"
            
        except Exception as e:
            return f"Error scraping: {str(e)}"
    
    def _handle_pdf_generation(self, message: str, entities: dict) -> str:
        """Handle PDF generation requests."""
        try:
            # Get current URL from browser context
            url = self.browser_context.get("navigation", {}).get("url")
            if not url:
                return "No active page to generate PDF from"
            
            # Generate PDF using PDFTool
            pdf_tool = PDFTool(
                operation="generate",
                url=url,
                output_path=f"pdfs/page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            result = pdf_tool.run()
            
            # Update browser context
            self.browser_context["pdf"] = {
                "timestamp": datetime.now().isoformat(),
                "url": url,
                "result": result
            }
            
            return f"Generated PDF: {result}"
            
        except Exception as e:
            return f"Error generating PDF: {str(e)}"
    
    def _handle_help_request(self) -> str:
        """Handle help requests."""
        return """
Available commands:
- Navigate: "Go to [URL]" or "Visit [URL]"
- Click: "Click element [selector]" or "Press [selector]"
- Type: "Type [text] into [selector]"
- Scrape: "Get content from [selector]" or "Extract [selector]"
- PDF: "Generate PDF" or "Save as PDF"

Examples:
- "Go to https://example.com"
- "Click element #submit-button"
- "Type 'Hello, World!' into #search-input"
- "Get content from .main-content"
- "Generate PDF of current page"
"""

if __name__ == "__main__":
    # Test the WebAutomationAgent
    agent = WebAutomationAgent()
    
    print("Testing WebAutomationAgent...")
    
    # Test navigation
    print("\nTesting navigation:")
    response = agent.chat('Go to "https://example.com"')
    print(response)
    
    # Test clicking
    print("\nTesting clicking:")
    response = agent.chat('Click element "#submit-button"')
    print(response)
    
    # Test typing
    print("\nTesting typing:")
    response = agent.chat('Type "Hello, World!" into "#search-input"')
    print(response)
    
    # Test scraping
    print("\nTesting scraping:")
    response = agent.chat('Get content from ".main-content"')
    print(response)
    
    # Test PDF generation
    print("\nTesting PDF generation:")
    response = agent.chat("Generate PDF of current page")
    print(response) 