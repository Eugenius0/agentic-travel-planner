import json

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from app.llm import create_llm
from app.mcp import create_mcp_client

MAX_RESEARCH_SEARCHES = 1
MAX_AGENT_STEPS = 12


class ResearchSearchInput(BaseModel):
    query: str = Field(
        description="A short search query for researching travel attractions."
    )


async def create_research_agent():
    client = create_mcp_client()
    tools = await client.get_tools()

    search_tool = next(
        (tool for tool in tools if tool.name == "tavily_search"),
        None,
    )

    if search_tool is None:
        raise ValueError("Tavily search tool is unavailable.")

    search_count = 0

    async def limited_search(query: str) -> str:
        nonlocal search_count

        if search_count >= MAX_RESEARCH_SEARCHES:
            return "Search limit reached. Use existing research to finish."

        search_count += 1

        try:
            result = await search_tool.ainvoke(
                {
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 3,
                }
            )
        except Exception as exc:
            return f"Search failed: {type(exc).__name__}: {exc}"

        # Handle errors returned as normal MCP responses.
        if isinstance(result, list):
            for block in result:
                if not isinstance(block, dict):
                    continue

                if block.get("isError"):
                    return f"Search failed: {str(block)[:500]}"

                if block.get("type") == "text":
                    text = block.get("text", "")

                    try:
                        data = json.loads(text)
                    except (ValueError, TypeError):
                        continue

                    if isinstance(data, dict) and data.get("error"):
                        return f"Search failed: {str(data['error'])[:500]}"

        # Extract only useful source information to reduce token usage.
        sources = []

        if isinstance(result, list):
            for block in result:
                if not isinstance(block, dict) or block.get("type") != "text":
                    continue

                try:
                    data = json.loads(block.get("text", ""))
                except (ValueError, TypeError):
                    continue

                if not isinstance(data, dict):
                    continue

                for item in data.get("results", [])[:3]:
                    sources.append(
                        {
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "content": item.get("content", "")[:300],
                        }
                    )

        if not sources:
            return "Search returned no usable sources."

        return json.dumps(sources, ensure_ascii=False)

    limited_tool = StructuredTool.from_function(
        coroutine=limited_search,
        name="tavily_search",
        description="Search the web for travel attractions using a query.",
        args_schema=ResearchSearchInput,
    )

    return create_llm(max_tokens=250), [limited_tool]


async def run_research_agent(
    destination: str,
    interests: list[str],
) -> str:
    llm, tools = await create_research_agent()

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are a travel research specialist. "
            "Research attractions and activities relevant to the destination "
            "and traveler's interests. "
            "Use Tavily search to find reliable information about attractions, "
            "admission prices, and opening hours. "
            "Prefer official tourism and attraction websites. "
            "Include source URLs in your final research summary. "
            "Never invent prices or opening hours. "
            "Keep your final summary concise and factual. "
            f"You may perform up to {MAX_RESEARCH_SEARCHES} search(es). "
            "When the search limit is reached, finish using existing results. "
            "If a search fails, clearly state that the information is unverified."
        ),
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Research travel activities in {destination}. "
                        f"Interests: {', '.join(interests)}. "
                        "Find relevant attractions, approximate admission costs, "
                        "opening hours where available, and source URLs."
                    ),
                }
            ]
        },
        config={"recursion_limit": MAX_AGENT_STEPS},
    )

    return result["messages"][-1].content
