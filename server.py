#!/usr/bin/env python3
"""
Art Institute of Chicago MCP Server

Provides access to the Art Institute of Chicago's public API for artworks,
artists, exhibitions, galleries, and more.
"""

import asyncio
import logging
from typing import Any, Optional
from urllib.parse import urlencode

import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aic-mcp-server")

# API Configuration
BASE_URL = "https://api.artic.edu/api/v1"
DEFAULT_TIMEOUT = 30.0
MAX_RESULTS = 100

# Initialize MCP server
app = Server("art-institute-chicago")


class AICAPIError(Exception):
    """Custom exception for AIC API errors"""
    pass


async def make_api_request(
    endpoint: str,
    params: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """
    Make an async request to the AIC API.

    Args:
        endpoint: API endpoint path (without base URL)
        params: Query parameters

    Returns:
        JSON response from API

    Raises:
        AICAPIError: If the API request fails
    """
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    if params:
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            logger.info(f"Making request to {url} with params: {params}")
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
        raise AICAPIError(f"API request failed: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        raise AICAPIError(f"Failed to connect to API: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise AICAPIError(f"Unexpected error: {str(e)}")


def format_artwork_response(data: dict[str, Any]) -> str:
    """Format artwork data into readable text"""
    if "data" not in data:
        return "No artwork data found."

    # Handle single artwork vs list
    artworks = data["data"] if isinstance(data["data"], list) else [data["data"]]

    if not artworks:
        return "No artworks found."

    result = []
    for artwork in artworks[:10]:  # Limit to 10 results
        title = artwork.get("title", "Untitled")
        artist = artwork.get("artist_display", "Unknown artist")
        date = artwork.get("date_display", "Unknown date")
        medium = artwork.get("medium_display", "Unknown medium")
        place = artwork.get("place_of_origin", "Unknown origin")
        description = artwork.get("short_description") or artwork.get("description", "No description available")
        artwork_id = artwork.get("id", "Unknown")

        artwork_text = f"""
**{title}**
ID: {artwork_id}
Artist: {artist}
Date: {date}
Medium: {medium}
Origin: {place}
Description: {description[:300]}{'...' if len(description) > 300 else ''}
"""

        # Add image URL if available
        if artwork.get("image_id"):
            image_id = artwork["image_id"]
            # IIIF image URL - using medium size
            image_url = f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"
            artwork_text += f"Image: {image_url}\n"

        # Add web URL
        if artwork.get("id"):
            web_url = f"https://www.artic.edu/artworks/{artwork['id']}"
            artwork_text += f"View online: {web_url}\n"

        result.append(artwork_text)

    # Add pagination info if available
    if "pagination" in data:
        pagination = data["pagination"]
        total = pagination.get("total", 0)
        limit = pagination.get("limit", 0)
        current_page = pagination.get("current_page", 1)
        total_pages = pagination.get("total_pages", 1)

        result.append(f"\nShowing {len(artworks)} of {total} total results (Page {current_page}/{total_pages})")

    return "\n---\n".join(result)


def format_agent_response(data: dict[str, Any]) -> str:
    """Format agent/artist data into readable text"""
    if "data" not in data:
        return "No agent data found."

    agents = data["data"] if isinstance(data["data"], list) else [data["data"]]

    if not agents:
        return "No agents found."

    result = []
    for agent in agents[:10]:
        title = agent.get("title", "Unknown")
        birth_date = agent.get("birth_date", "Unknown")
        death_date = agent.get("death_date", "Unknown")
        description = agent.get("description", "No description available")
        agent_id = agent.get("id", "Unknown")

        agent_text = f"""
**{title}**
ID: {agent_id}
Birth: {birth_date}
Death: {death_date}
Description: {description[:300]}{'...' if len(description) > 300 else ''}
"""
        result.append(agent_text)

    if "pagination" in data:
        pagination = data["pagination"]
        total = pagination.get("total", 0)
        result.append(f"\nShowing {len(agents)} of {total} total results")

    return "\n---\n".join(result)


def format_exhibition_response(data: dict[str, Any]) -> str:
    """Format exhibition data into readable text"""
    if "data" not in data:
        return "No exhibition data found."

    exhibitions = data["data"] if isinstance(data["data"], list) else [data["data"]]

    if not exhibitions:
        return "No exhibitions found."

    result = []
    for exhibition in exhibitions[:10]:
        title = exhibition.get("title", "Untitled Exhibition")
        description = exhibition.get("short_description", "No description available")
        start_date = exhibition.get("aic_start_at", "Unknown")
        end_date = exhibition.get("aic_end_at", "Unknown")
        status = exhibition.get("status", "Unknown")
        gallery = exhibition.get("gallery_title", "Unknown location")
        exhibition_id = exhibition.get("id", "Unknown")

        exhibition_text = f"""
**{title}**
ID: {exhibition_id}
Status: {status}
Dates: {start_date} to {end_date}
Location: {gallery}
Description: {description[:300]}{'...' if len(description) > 300 else ''}
"""

        if exhibition.get("web_url"):
            exhibition_text += f"More info: {exhibition['web_url']}\n"

        result.append(exhibition_text)

    if "pagination" in data:
        pagination = data["pagination"]
        total = pagination.get("total", 0)
        result.append(f"\nShowing {len(exhibitions)} of {total} total results")

    return "\n---\n".join(result)


def format_gallery_response(data: dict[str, Any]) -> str:
    """Format gallery data into readable text"""
    if "data" not in data:
        return "No gallery data found."

    galleries = data["data"] if isinstance(data["data"], list) else [data["data"]]

    if not galleries:
        return "No galleries found."

    result = []
    for gallery in galleries[:20]:
        title = gallery.get("title", "Unknown Gallery")
        number = gallery.get("number", "Unknown")
        floor = gallery.get("floor", "Unknown")
        is_closed = gallery.get("is_closed", False)
        gallery_id = gallery.get("id", "Unknown")

        status = "Closed" if is_closed else "Open"

        gallery_text = f"""
**{title}**
ID: {gallery_id}
Gallery Number: {number}
Floor: {floor}
Status: {status}
"""
        result.append(gallery_text)

    if "pagination" in data:
        pagination = data["pagination"]
        total = pagination.get("total", 0)
        result.append(f"\nShowing {len(galleries)} of {total} total results")

    return "\n---\n".join(result)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the AIC API"""
    return [
        Tool(
            name="search_artworks",
            description=(
                "Search for artworks in the Art Institute of Chicago collection. "
                "Returns artwork details including title, artist, date, medium, description, and images. "
                "Supports full-text search across all artwork metadata."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'Monet', 'impressionism', 'landscape')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10, max: 100)",
                        "default": 10
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number for pagination (default: 1)",
                        "default": 1
                    },
                    "fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to return (e.g., 'title,artist_display,image_id')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_artwork",
            description=(
                "Get detailed information about a specific artwork by its ID. "
                "Returns complete artwork metadata including dimensions, provenance, exhibition history, and high-resolution images."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "artwork_id": {
                        "type": "integer",
                        "description": "The unique ID of the artwork"
                    },
                    "fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to return"
                    }
                },
                "required": ["artwork_id"]
            }
        ),
        Tool(
            name="search_agents",
            description=(
                "Search for artists, creators, and cultural agents. "
                "Returns biographical information including birth/death dates and descriptions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., artist name or cultural movement)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10, max: 100)",
                        "default": 10
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number for pagination (default: 1)",
                        "default": 1
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_agent",
            description="Get detailed information about a specific artist or cultural agent by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "integer",
                        "description": "The unique ID of the agent/artist"
                    }
                },
                "required": ["agent_id"]
            }
        ),
        Tool(
            name="search_exhibitions",
            description=(
                "Search for current, past, and upcoming exhibitions. "
                "Returns exhibition details including dates, locations, and descriptions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., exhibition theme or title)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10, max: 100)",
                        "default": 10
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number for pagination (default: 1)",
                        "default": 1
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_exhibition",
            description="Get detailed information about a specific exhibition by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "exhibition_id": {
                        "type": "integer",
                        "description": "The unique ID of the exhibition"
                    }
                },
                "required": ["exhibition_id"]
            }
        ),
        Tool(
            name="list_galleries",
            description=(
                "List museum galleries with their locations and current status. "
                "Useful for finding where artworks are displayed."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 20, max: 100)",
                        "default": 20
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number for pagination (default: 1)",
                        "default": 1
                    }
                }
            }
        ),
        Tool(
            name="get_gallery",
            description="Get detailed information about a specific gallery by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "gallery_id": {
                        "type": "integer",
                        "description": "The unique ID of the gallery"
                    }
                },
                "required": ["gallery_id"]
            }
        ),
        Tool(
            name="search_all",
            description=(
                "Search across all content types in the museum collection "
                "(artworks, agents, exhibitions, galleries, and more). "
                "Best for broad exploratory searches."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10, max: 100)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    try:
        if name == "search_artworks":
            query = arguments.get("query")
            limit = min(arguments.get("limit", 10), MAX_RESULTS)
            page = arguments.get("page", 1)
            fields = arguments.get("fields")

            params = {
                "q": query,
                "limit": limit,
                "page": page,
                "fields": fields
            }

            data = await make_api_request("artworks/search", params)
            response_text = format_artwork_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "get_artwork":
            artwork_id = arguments.get("artwork_id")
            fields = arguments.get("fields")

            params = {"fields": fields} if fields else None
            data = await make_api_request(f"artworks/{artwork_id}", params)
            response_text = format_artwork_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "search_agents":
            query = arguments.get("query")
            limit = min(arguments.get("limit", 10), MAX_RESULTS)
            page = arguments.get("page", 1)

            params = {
                "q": query,
                "limit": limit,
                "page": page
            }

            data = await make_api_request("agents/search", params)
            response_text = format_agent_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "get_agent":
            agent_id = arguments.get("agent_id")
            data = await make_api_request(f"agents/{agent_id}")
            response_text = format_agent_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "search_exhibitions":
            query = arguments.get("query")
            limit = min(arguments.get("limit", 10), MAX_RESULTS)
            page = arguments.get("page", 1)

            params = {
                "q": query,
                "limit": limit,
                "page": page
            }

            data = await make_api_request("exhibitions/search", params)
            response_text = format_exhibition_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "get_exhibition":
            exhibition_id = arguments.get("exhibition_id")
            data = await make_api_request(f"exhibitions/{exhibition_id}")
            response_text = format_exhibition_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "list_galleries":
            limit = min(arguments.get("limit", 20), MAX_RESULTS)
            page = arguments.get("page", 1)

            params = {
                "limit": limit,
                "page": page
            }

            data = await make_api_request("galleries", params)
            response_text = format_gallery_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "get_gallery":
            gallery_id = arguments.get("gallery_id")
            data = await make_api_request(f"galleries/{gallery_id}")
            response_text = format_gallery_response(data)

            return [TextContent(type="text", text=response_text)]

        elif name == "search_all":
            query = arguments.get("query")
            limit = min(arguments.get("limit", 10), MAX_RESULTS)

            params = {
                "q": query,
                "limit": limit
            }

            data = await make_api_request("search", params)

            # Format mixed results
            if "data" not in data or not data["data"]:
                return [TextContent(type="text", text="No results found.")]

            results = []
            for item in data["data"][:limit]:
                api_model = item.get("api_model", "unknown")
                title = item.get("title", "Untitled")
                item_id = item.get("id", "Unknown")

                results.append(f"**{title}** (Type: {api_model}, ID: {item_id})")

            response_text = "\n".join(results)
            if "pagination" in data:
                total = data["pagination"].get("total", 0)
                response_text += f"\n\nShowing {len(results)} of {total} total results"

            return [TextContent(type="text", text=response_text)]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except AICAPIError as e:
        logger.error(f"API error in {name}: {str(e)}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
    except Exception as e:
        logger.error(f"Unexpected error in {name}: {str(e)}")
        return [TextContent(
            type="text",
            text=f"Unexpected error: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
