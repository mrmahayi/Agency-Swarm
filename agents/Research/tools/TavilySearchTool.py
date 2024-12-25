from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import json
from typing import Optional, List
import httpx

class TavilySearchTool(BaseTool):
    """
    A tool for performing comprehensive online research using Tavily's search API.
    Optimized for LLMs and RAG applications.
    """
    
    query: str = Field(
        ..., 
        description="The search query or research question"
    )
    
    search_depth: str = Field(
        "basic",  # or "advanced" for more comprehensive search
        description="The depth of search to perform: 'basic' for quick results, 'advanced' for comprehensive research"
    )
    
    include_domains: Optional[List[str]] = Field(
        None,
        description="List of domains to specifically include in the search"
    )
    
    exclude_domains: Optional[List[str]] = Field(
        None,
        description="List of domains to exclude from the search"
    )
    
    max_results: int = Field(
        5,
        description="Maximum number of results to return"
    )
    
    search_type: str = Field(
        "search",  # or "research" for comprehensive research
        description="Type of search to perform: 'search' for regular search, 'research' for comprehensive research"
    )

    def run(self):
        """
        Execute the search using Tavily's API and return the results.
        """
        try:
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                return "Error: TAVILY_API_KEY not found in environment variables"
            
            # Prepare the request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"  # Updated authorization header
            }
            
            # Build the request payload
            payload = {
                "query": self.query,
                "include_answer": True,
                "include_raw_content": False,
                "max_results": self.max_results
            }
            
            # Add search depth if advanced
            if self.search_depth == "advanced":
                payload["search_depth"] = "advanced"
            
            # Add optional parameters if provided
            if self.include_domains:
                payload["include_domains"] = self.include_domains
            if self.exclude_domains:
                payload["exclude_domains"] = self.exclude_domains
            
            # Use the search endpoint for all requests (API v1)
            endpoint = "https://api.tavily.com/search"
            
            # Make the request
            with httpx.Client(timeout=30.0) as client:
                response = client.post(endpoint, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    return json.dumps({
                        "results": result.get("results", []),
                        "answer": result.get("answer", ""),
                        "topic": result.get("topic", "")
                    }, indent=2)
                else:
                    return f"Error: Tavily API returned status code {response.status_code}\nResponse: {response.text}"
                    
        except Exception as e:
            return f"Error during Tavily search: {str(e)}"

if __name__ == "__main__":
    # Test basic search
    tool = TavilySearchTool(
        query="What is artificial intelligence?",
        search_depth="basic",
        max_results=3
    )
    print("Basic Search Results:", tool.run())
    
    # Test comprehensive research
    tool = TavilySearchTool(
        query="Explain the impact of AI on healthcare",
        search_depth="advanced",
        max_results=5
    )
    print("\nComprehensive Research Results:", tool.run()) 