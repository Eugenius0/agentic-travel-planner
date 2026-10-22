import os

from langchain_mcp_adapters.client import MultiServerMCPClient


def create_mcp_client() -> MultiServerMCPClient:
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable is not configured")

    return MultiServerMCPClient(
        {
            "tavily": {
                "transport": "streamable_http",
                "url": "https://mcp.tavily.com/mcp/",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                },
            }
        }
    )
