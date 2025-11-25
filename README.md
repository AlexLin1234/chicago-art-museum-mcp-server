# Art Institute of Chicago MCP Server

A Model Context Protocol (MCP) server that provides access to the [Art Institute of Chicago's public API](https://api.artic.edu/docs/). This server enables AI assistants like Claude to search and retrieve information about artworks, artists, exhibitions, galleries, and more from one of the world's premier art museums.

## Features

- **Artwork Search**: Search the museum's extensive collection with full-text queries
- **Artwork Details**: Get comprehensive information about specific artworks including images, provenance, and exhibition history
- **Artist Information**: Search for and retrieve biographical information about artists and cultural agents
- **Exhibition Data**: Access current, past, and upcoming exhibition information
- **Gallery Information**: Browse museum galleries and their locations
- **Universal Search**: Search across all content types simultaneously

## Available Tools

### `search_artworks`
Search for artworks with support for pagination and field filtering.
```json
{
  "query": "Monet water lilies",
  "limit": 10,
  "page": 1,
  "fields": "title,artist_display,image_id"
}
```

### `get_artwork`
Get detailed information about a specific artwork by ID.
```json
{
  "artwork_id": 27992,
  "fields": "title,artist_display,date_display,medium_display,dimensions,description,image_id"
}
```

### `search_agents`
Search for artists, creators, and cultural agents.
```json
{
  "query": "Pablo Picasso",
  "limit": 5
}
```

### `get_agent`
Get detailed information about a specific artist or agent by ID.
```json
{
  "agent_id": 36198
}
```

### `search_exhibitions`
Search for museum exhibitions.
```json
{
  "query": "impressionism",
  "limit": 10
}
```

### `get_exhibition`
Get detailed information about a specific exhibition by ID.
```json
{
  "exhibition_id": 9328
}
```

### `list_galleries`
List museum galleries with location and status information.
```json
{
  "limit": 20,
  "page": 1
}
```

### `get_gallery`
Get information about a specific gallery by ID.
```json
{
  "gallery_id": 2147483649
}
```

### `search_all`
Search across all content types (artworks, agents, exhibitions, etc.).
```json
{
  "query": "Renaissance",
  "limit": 15
}
```

## Installation

### Prerequisites

- Python 3.10 or higher
- [Claude Desktop](https://claude.ai/download) or another MCP-compatible client
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chicago-art-museum-mcp-server.git
   cd chicago-art-museum-mcp-server
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Test the installation**
   ```bash
   python server.py
   ```
   The server should start without errors. Press `Ctrl+C` to stop.

## Configuration for Claude Desktop

### Windows

1. Open or create the Claude Desktop configuration file:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add the MCP server configuration:
   ```json
   {
     "mcpServers": {
       "art-institute-chicago": {
         "command": "python",
         "args": [
           "C:\\path\\to\\chicago-art-museum-mcp-server\\server.py"
         ]
       }
     }
   }
   ```

3. **Important**: Replace `C:\\path\\to\\chicago-art-museum-mcp-server` with the actual path to where you cloned the repository. Use double backslashes (`\\`) for Windows paths.

### macOS

1. Open or create the Claude Desktop configuration file:
   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. Add the MCP server configuration:
   ```json
   {
     "mcpServers": {
       "art-institute-chicago": {
         "command": "python3",
         "args": [
           "/path/to/chicago-art-museum-mcp-server/server.py"
         ]
       }
     }
   }
   ```

3. Replace `/path/to/chicago-art-museum-mcp-server` with the actual path to where you cloned the repository.

### Using Virtual Environment (Recommended)

If you created a virtual environment, you should use the Python interpreter from within that environment:

**Windows:**
```json
{
  "mcpServers": {
    "art-institute-chicago": {
      "command": "C:\\path\\to\\chicago-art-museum-mcp-server\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\chicago-art-museum-mcp-server\\server.py"
      ]
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "art-institute-chicago": {
      "command": "/path/to/chicago-art-museum-mcp-server/venv/bin/python",
      "args": [
        "/path/to/chicago-art-museum-mcp-server/server.py"
      ]
    }
  }
}
```

### Restart Claude Desktop

After updating the configuration file, restart Claude Desktop for the changes to take effect.

## Usage Examples

Once configured, you can interact with the Art Institute of Chicago API through Claude. Here are some example prompts:

### Searching for Artworks
```
Search for artworks by Vincent van Gogh in the Art Institute of Chicago collection.
```

### Getting Artwork Details
```
Get detailed information about artwork ID 27992 from the Art Institute of Chicago.
```

### Exploring Exhibitions
```
What exhibitions at the Art Institute of Chicago feature impressionist art?
```

### Finding Artist Information
```
Tell me about the artist Georgia O'Keeffe using the Art Institute of Chicago database.
```

### Gallery Information
```
List the galleries at the Art Institute of Chicago and their locations.
```

## API Information

This server uses the [Art Institute of Chicago's public API](https://api.artic.edu/docs/). The API:

- Requires no authentication
- Has no rate limiting for reasonable use
- Provides access to over 117,000 artworks
- Includes high-resolution images via IIIF
- Updates regularly with new content

For more detailed API documentation, visit: https://api.artic.edu/docs/

## Troubleshooting

### Server doesn't start in Claude Desktop

1. Verify the path to `server.py` is correct in your configuration
2. Check that Python is installed and accessible from the command line
3. Ensure all dependencies are installed (`pip install -e .`)
4. Look at the Claude Desktop logs for error messages

### Import errors

Make sure you've installed the package:
```bash
pip install -e .
```

### Connection errors

- Check your internet connection
- Verify that `api.artic.edu` is accessible
- The API requires HTTPS; ensure your firewall allows outbound HTTPS connections

### No results returned

- Try broader search terms
- Check that the artwork/agent/exhibition ID is correct
- Some resources may have limited metadata

## Development

### Running Tests

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

### Code Formatting

This project uses Black and Ruff for code formatting and linting:

```bash
# Format code
black .

# Lint code
ruff check .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data provided by the [Art Institute of Chicago](https://www.artic.edu/) via their public API
- Built using the [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [API documentation](https://api.artic.edu/docs/)
3. Open an issue in this repository

## API Terms of Service

Please review the Art Institute of Chicago's [Terms and Conditions](https://www.artic.edu/terms) when using this server. The data is provided for educational and personal use.
