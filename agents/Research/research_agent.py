import os
from agency_swarm import Agent
from tools.TavilySearchTool import TavilySearchTool
from tools.CommunicationTool import CommunicationTool
from tools.TaskManagementTool import TaskManagementTool
from tools.MessageAnalyticsTool import MessageAnalyticsTool
from tools.PDFTool import PDFTool
import json
from datetime import datetime

class ResearchAgent(Agent):
    """
    Agent responsible for research and information gathering tasks.
    """
    def __init__(self):
        super().__init__(
            name="Research",
            description="Conducts research and information gathering tasks",
            instructions="./instructions.md",
            tools=[
                TavilySearchTool,
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
        self.research_context = {}
        self.conversation_history = []
    
    def chat(self, message: str) -> str:
        """
        Process incoming chat messages and return appropriate responses.
        Analyzes message intent and performs necessary research tasks.
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
            # Handle search requests
            if any(intent in intents for intent in ["search", "find", "research"]):
                return self._handle_search(message, entities)
            
            # Handle information requests
            elif any(intent in intents for intent in ["info", "details", "explain"]):
                return self._handle_info_request(message, entities)
            
            # Handle summarization requests
            elif any(intent in intents for intent in ["summarize", "summary"]):
                return self._handle_summarization(message, entities)
            
            # Handle report generation
            elif any(intent in intents for intent in ["report", "document"]):
                return self._handle_report_generation(message, entities)
            
            # Handle help request
            elif "help" in message.lower():
                return self._handle_help_request()
            
            else:
                return (
                    "I can help you with research tasks like:\n"
                    "- Searching for information\n"
                    "- Getting detailed explanations\n"
                    "- Summarizing content\n"
                    "- Generating reports\n\n"
                    "What would you like me to research?"
                )
        
        except Exception as e:
            return f"Error processing intents: {str(e)}"
    
    def _handle_search(self, message: str, entities: dict) -> str:
        """Handle search requests."""
        try:
            # Extract search query from entities or message
            query = entities.get("query")
            if not query:
                # Look for query patterns
                import re
                patterns = [
                    r'"([^"]+)"',
                    r'search for\s+(.+)',
                    r'find\s+(.+)',
                    r'research\s+(.+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        query = match.group(1)
                        break
            
            if not query:
                return "Could not determine what to search for"
            
            # Perform search using TavilySearchTool
            search_tool = TavilySearchTool(
                query=query,
                max_results=5
            )
            results = json.loads(search_tool.run())
            
            # Update research context
            self.research_context["search"] = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "results": results
            }
            
            # Format results
            formatted_results = "Search results:\n\n"
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. {result['title']}\n"
                formatted_results += f"   URL: {result['url']}\n"
                formatted_results += f"   Summary: {result['snippet']}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Error searching: {str(e)}"
    
    def _handle_info_request(self, message: str, entities: dict) -> str:
        """Handle information requests."""
        try:
            # Extract topic from entities or message
            topic = entities.get("topic")
            if not topic:
                # Look for topic patterns
                import re
                patterns = [
                    r'"([^"]+)"',
                    r'about\s+(.+)',
                    r'explain\s+(.+)',
                    r'details\s+(?:about|on)\s+(.+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        topic = match.group(1)
                        break
            
            if not topic:
                return "Could not determine what to get information about"
            
            # Search for information using TavilySearchTool
            search_tool = TavilySearchTool(
                query=f"detailed information about {topic}",
                max_results=3
            )
            results = json.loads(search_tool.run())
            
            # Update research context
            self.research_context["info"] = {
                "timestamp": datetime.now().isoformat(),
                "topic": topic,
                "results": results
            }
            
            # Combine and format information
            info = f"Information about {topic}:\n\n"
            for result in results:
                info += f"Source: {result['title']}\n"
                info += f"{result['snippet']}\n\n"
            
            return info
            
        except Exception as e:
            return f"Error getting information: {str(e)}"
    
    def _handle_summarization(self, message: str, entities: dict) -> str:
        """Handle summarization requests."""
        try:
            # Extract content from research context
            if not self.research_context:
                return "No recent research content to summarize"
            
            # Get most recent research results
            latest_results = None
            if "search" in self.research_context:
                latest_results = self.research_context["search"]["results"]
            elif "info" in self.research_context:
                latest_results = self.research_context["info"]["results"]
            
            if not latest_results:
                return "No content available to summarize"
            
            # Combine content for summarization
            content = ""
            for result in latest_results:
                content += f"{result['title']}\n{result['snippet']}\n\n"
            
            # Use MessageAnalyticsTool for summarization
            analytics_tool = MessageAnalyticsTool(
                operation="summarize",
                text=content
            )
            summary = analytics_tool.run()
            
            # Update research context
            self.research_context["summary"] = {
                "timestamp": datetime.now().isoformat(),
                "content": content,
                "summary": summary
            }
            
            return f"Summary:\n\n{summary}"
            
        except Exception as e:
            return f"Error summarizing: {str(e)}"
    
    def _handle_report_generation(self, message: str, entities: dict) -> str:
        """Handle report generation requests."""
        try:
            # Check if we have content to generate report from
            if not self.research_context:
                return "No research content available for report generation"
            
            # Compile report content
            report_content = "Research Report\n\n"
            
            if "search" in self.research_context:
                report_content += "Search Results:\n"
                for result in self.research_context["search"]["results"]:
                    report_content += f"- {result['title']}\n"
                    report_content += f"  {result['snippet']}\n\n"
            
            if "info" in self.research_context:
                report_content += "Detailed Information:\n"
                for result in self.research_context["info"]["results"]:
                    report_content += f"- {result['title']}\n"
                    report_content += f"  {result['snippet']}\n\n"
            
            if "summary" in self.research_context:
                report_content += "Summary:\n"
                report_content += self.research_context["summary"]["summary"]
            
            # Generate PDF using PDFTool
            pdf_tool = PDFTool(
                operation="generate",
                content=report_content,
                output_path=f"reports/research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            result = pdf_tool.run()
            
            # Update research context
            self.research_context["report"] = {
                "timestamp": datetime.now().isoformat(),
                "content": report_content,
                "result": result
            }
            
            return f"Generated research report: {result}"
            
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def _handle_help_request(self) -> str:
        """Handle help requests."""
        return """
Available commands:
- Search: "Search for [query]" or "Find information about [topic]"
- Info: "Get details about [topic]" or "Explain [topic]"
- Summarize: "Summarize the results" or "Give me a summary"
- Report: "Generate report" or "Create research document"

Examples:
- "Search for artificial intelligence trends"
- "Get information about quantum computing"
- "Summarize the search results"
- "Generate a research report"
"""

if __name__ == "__main__":
    # Test the ResearchAgent
    agent = ResearchAgent()
    
    print("Testing ResearchAgent...")
    
    # Test search
    print("\nTesting search:")
    response = agent.chat('Search for "artificial intelligence trends"')
    print(response)
    
    # Test info request
    print("\nTesting info request:")
    response = agent.chat('Get information about quantum computing')
    print(response)
    
    # Test summarization
    print("\nTesting summarization:")
    response = agent.chat('Summarize the results')
    print(response)
    
    # Test report generation
    print("\nTesting report generation:")
    response = agent.chat('Generate a research report')
    print(response) 