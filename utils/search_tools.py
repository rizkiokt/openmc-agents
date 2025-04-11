from typing import Dict, Any, List, Optional
from langchain.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
import numpy as np
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ReactorDesignSearchTool(BaseTool):
    name: str = "reactor_design_search"
    description: str = "Searches for reactor design information and specifications"
    search_tool: DuckDuckGoSearchRun = None
    
    def __init__(self):
        super().__init__()
        self.search_tool = DuckDuckGoSearchRun()
        logger.debug("Initialized ReactorDesignSearchTool")
    
    def _format_query(self, query: Any) -> str:
        """
        Format the query into a search string.
        
        Args:
            query: Input query (can be string or dict)
            
        Returns:
            Formatted search string
        """
        if isinstance(query, dict):
            # Extract key information from the dictionary
            reactor_type = query.get('reactor_type', '')
            fuel_type = query.get('fuel_type', '')
            geom_type = query.get('geom_type', '')
            additional_info = query.get('Additional_info', '')
            
            # Create a natural language search string
            formatted = f"{reactor_type} {fuel_type} {geom_type} {additional_info}"
            logger.debug(f"Formatted dictionary query: {formatted}")
            return formatted
        logger.debug(f"Using string query as is: {query}")
        return str(query)
    
    def _run(self, query: str) -> Dict[str, Any]:
        """
        Search for reactor design information.
        
        Args:
            query: Search query string or dict
            
        Returns:
            Dictionary containing search results
        """
        logger.debug(f"Received search request: {query}")
        
        # Format the query
        formatted_query = query if isinstance(query, str) else self._format_query(query)
        logger.debug(f"Formatted search query: {formatted_query}")
        
        # Create focused search queries
        search_queries = [
            f"{formatted_query} reactor design specifications",
            f"{formatted_query} fuel assembly layout",
            f"{formatted_query} material specifications",
            f"{formatted_query} fuel geometry"
        ]
        
        logger.debug("Performing searches with queries:")
        for q in search_queries:
            logger.debug(f"  - {q}")
        
        # Perform searches
        search_results = []
        for search_query in search_queries:
            logger.debug(f"Searching for: {search_query}")
            result = self.search_tool.invoke(search_query)
            logger.debug(f"Search result: {result[:100]}...")  # Log first 100 chars of result
            search_results.append({
                "title": f"Search results for: {search_query}",
                "body": result
            })
        
        logger.debug(f"Returning {len(search_results)} search results")
        return {
            "search_results": search_results
        }
    
    async def _arun(self, query: str) -> Dict[str, Any]:
        logger.debug(f"Async search request: {query}")
        return self._run(query)

def create_search_tools() -> List[BaseTool]:
    """
    Create a list of search tools.
    
    Returns:
        List of BaseTool instances
    """
    return [
        ReactorDesignSearchTool()
    ]

def search_reactor_design(query: str) -> Dict[str, Any]:
    """
    Search for reactor design information.
    
    Args:
        query: Search query
        
    Returns:
        Dictionary containing search results
    """
    tool = ReactorDesignSearchTool()
    return tool._run(query) 