import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

from app.research_agent import (
    MAX_RESEARCH_SEARCHES,
    create_research_agent,
)


def test_research_agent_search_limit():
    async def run_test():
        mock_search = MagicMock()
        mock_search.name = "tavily_search"
        mock_search.description = "Search the web"
        mock_search.args_schema = {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"],
        }
        mock_search.ainvoke = AsyncMock(return_value="Mocked Tavily search results")

        mock_client = MagicMock()
        mock_client.get_tools = AsyncMock(return_value=[mock_search])

        with (
            patch(
                "app.research_agent.create_mcp_client",
                return_value=mock_client,
            ),
            patch("app.research_agent.create_llm"),
        ):
            _, tools = await create_research_agent()

        search_tool = tools[0]

        for index in range(MAX_RESEARCH_SEARCHES + 1):
            await search_tool.ainvoke(
                {
                    "query": f"Stockholm attractions {index}",
                }
            )

        assert mock_search.ainvoke.await_count == MAX_RESEARCH_SEARCHES

        blocked_result = await search_tool.ainvoke(
            {
                "query": "One more search",
            }
        )

        assert "Search limit reached" in blocked_result

    asyncio.run(run_test())


def test_research_agent_handles_search_failure():
    async def run_test():
        mock_search = MagicMock()
        mock_search.name = "tavily_search"
        mock_search.description = "Search the web"
        mock_search.ainvoke = AsyncMock(
            side_effect=RuntimeError("HTTP 429: Rate limit exceeded")
        )

        mock_client = MagicMock()
        mock_client.get_tools = AsyncMock(return_value=[mock_search])

        with (
            patch(
                "app.research_agent.create_mcp_client",
                return_value=mock_client,
            ),
            patch("app.research_agent.create_llm"),
        ):
            _, tools = await create_research_agent()

        result = await tools[0].ainvoke({"query": "Stockholm museums"})

        assert "429" in result
        assert "Search failed" in result

    asyncio.run(run_test())


def test_research_agent_handles_error_response():
    async def run_test():
        mock_search = MagicMock()
        mock_search.name = "tavily_search"
        mock_search.description = "Search the web"
        mock_search.ainvoke = AsyncMock(
            return_value=[
                {
                    "type": "text",
                    "text": '{"error": "HTTP 429: Rate limit exceeded"}',
                }
            ]
        )

        mock_client = MagicMock()
        mock_client.get_tools = AsyncMock(return_value=[mock_search])

        with (
            patch(
                "app.research_agent.create_mcp_client",
                return_value=mock_client,
            ),
            patch("app.research_agent.create_llm"),
        ):
            _, tools = await create_research_agent()

        result = await tools[0].ainvoke({"query": "Stockholm museums"})

        assert "Search failed" in result
        assert "429" in result
        assert mock_search.ainvoke.await_count == 1

    asyncio.run(run_test())


def test_research_agent_extracts_sources():
    async def run_test():
        mock_search = MagicMock()
        mock_search.name = "tavily_search"
        mock_search.description = "Search the web"
        mock_search.ainvoke = AsyncMock(
            return_value=[
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "results": [
                                {
                                    "title": "Vasa Museum",
                                    "url": "https://www.vasamuseet.se",
                                    "content": "A maritime museum in Stockholm.",
                                },
                                {
                                    "title": "Nordic Museum",
                                    "url": "https://www.nordiskamuseet.se",
                                    "content": "A museum of Swedish culture.",
                                },
                            ]
                        }
                    ),
                }
            ]
        )

        mock_client = MagicMock()
        mock_client.get_tools = AsyncMock(return_value=[mock_search])

        with (
            patch(
                "app.research_agent.create_mcp_client",
                return_value=mock_client,
            ),
            patch("app.research_agent.create_llm"),
        ):
            _, tools = await create_research_agent()

        result = await tools[0].ainvoke({"query": "Stockholm museums"})

        sources = json.loads(result)

        assert len(sources) == 2
        assert sources[0]["title"] == "Vasa Museum"
        assert sources[0]["url"] == "https://www.vasamuseet.se"
        assert sources[1]["title"] == "Nordic Museum"
        assert sources[1]["content"] == "A museum of Swedish culture."

        mock_search.ainvoke.assert_awaited_once_with(
            {
                "query": "Stockholm museums",
                "search_depth": "basic",
                "max_results": 3,
            }
        )

    asyncio.run(run_test())
