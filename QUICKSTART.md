# Quick Start Guide

Get the Art Institute of Chicago MCP server running in 5 minutes!

## Step 1: Install Python

Make sure you have Python 3.10 or higher installed:

```bash
python --version
```

If you need to install Python, download it from [python.org](https://www.python.org/downloads/).

## Step 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/chicago-art-museum-mcp-server.git
cd chicago-art-museum-mcp-server

# Install dependencies
pip install -e .
```

## Step 3: Test the Server

Run the test script to verify everything works:

```bash
python test_server.py
```

You should see:
```
✓ All tests passed successfully!
```

## Step 4: Configure Claude Desktop

### Windows

1. Open: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this configuration (update the path):
```json
{
  "mcpServers": {
    "art-institute-chicago": {
      "command": "python",
      "args": [
        "C:\\Users\\YourUsername\\chicago-art-museum-mcp-server\\server.py"
      ]
    }
  }
}
```

### macOS/Linux

1. Open: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add this configuration (update the path):
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

## Step 5: Restart Claude Desktop

Completely quit and restart Claude Desktop.

## Step 6: Test in Claude

Try these prompts:

```
Search for artworks by Monet in the Art Institute of Chicago.
```

```
Tell me about artwork ID 27992 from the Art Institute of Chicago.
```

```
What exhibitions are at the Art Institute of Chicago?
```

## Troubleshooting

### "Module not found" error

Make sure you installed dependencies:
```bash
pip install -e .
```

### Server doesn't appear in Claude

1. Check the path in your config file is correct
2. Make sure you completely quit and restarted Claude Desktop
3. Check Claude Desktop's logs for errors

### Connection errors

- Verify you have internet access
- Test the API directly: https://api.artic.edu/api/v1/artworks/27992
- Check your firewall settings

## Next Steps

- Read [EXAMPLES.md](EXAMPLES.md) for usage examples
- See [README.md](README.md) for complete documentation
- Explore the [Art Institute of Chicago API docs](https://api.artic.edu/docs/)

## Need Help?

- Check the [README troubleshooting section](README.md#troubleshooting)
- Open an issue on GitHub
- Review the API documentation

---

**That's it! You're ready to explore over 117,000 artworks with Claude!** 🎨
