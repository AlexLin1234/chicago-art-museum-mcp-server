# Contributing to Art Institute of Chicago MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Submit a pull request

## Development Setup

### Install Development Dependencies

```bash
# Clone your fork
git clone https://github.com/your-username/chicago-art-museum-mcp-server.git
cd chicago-art-museum-mcp-server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run basic connectivity tests
python test_server.py

# Run full test suite (when available)
pytest
```

### Code Quality

This project uses Black for formatting and Ruff for linting:

```bash
# Format code
black .

# Check linting
ruff check .

# Fix auto-fixable linting issues
ruff check --fix .
```

## Code Style Guidelines

- **Python Version**: Target Python 3.10+
- **Line Length**: Maximum 100 characters
- **Formatting**: Use Black with default settings
- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Use Google-style docstrings for all public functions

### Example Function

```python
async def search_artworks(
    query: str,
    limit: int = 10,
    page: int = 1
) -> dict[str, Any]:
    """
    Search for artworks in the collection.

    Args:
        query: Search query string
        limit: Maximum number of results to return
        page: Page number for pagination

    Returns:
        Dictionary containing search results and pagination info

    Raises:
        AICAPIError: If the API request fails
    """
    # Implementation here
    pass
```

## Adding New Features

### Adding a New Tool

1. **Define the tool** in the `list_tools()` function:

```python
Tool(
    name="your_new_tool",
    description="Clear description of what this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description of param1"
            }
        },
        "required": ["param1"]
    }
)
```

2. **Implement the handler** in the `call_tool()` function:

```python
elif name == "your_new_tool":
    param1 = arguments.get("param1")
    data = await make_api_request("endpoint", {"param": param1})
    response_text = format_response(data)
    return [TextContent(type="text", text=response_text)]
```

3. **Add a formatter function** if needed:

```python
def format_your_data(data: dict[str, Any]) -> str:
    """Format your data type into readable text"""
    # Implementation here
    pass
```

4. **Update documentation**:
   - Add tool description to README.md
   - Add usage examples to EXAMPLES.md
   - Update QUICKSTART.md if relevant

### Adding API Endpoints

When adding support for new API endpoints:

1. Review the [API documentation](https://api.artic.edu/docs/)
2. Understand the endpoint's parameters and response format
3. Create appropriate formatter functions
4. Add comprehensive error handling
5. Update documentation

## Testing Guidelines

### Manual Testing

Before submitting a PR, test your changes:

```bash
# Test the API connection
python test_server.py

# Test with Claude Desktop
# 1. Update your claude_desktop_config.json to point to your development version
# 2. Restart Claude Desktop
# 3. Test the new functionality with various prompts
```

### Test Coverage

When adding new features, consider adding:

- Unit tests for utility functions
- Integration tests for API calls
- Edge case testing
- Error handling verification

## Documentation

Good documentation is crucial. When contributing:

### Code Comments

- Comment complex logic
- Explain "why" not "what"
- Keep comments up to date

### README Updates

Update README.md when adding:
- New tools or features
- New configuration options
- New requirements or dependencies

### Examples

Add usage examples to EXAMPLES.md for:
- New tools
- Complex use cases
- Common workflows

## Pull Request Process

1. **Create a descriptive PR title**
   - Good: "Add support for artwork categories search"
   - Bad: "Update server.py"

2. **Write a clear description**
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?

3. **Keep PRs focused**
   - One feature or fix per PR
   - Avoid mixing refactoring with new features

4. **Update documentation**
   - Update README.md
   - Add examples if applicable
   - Update CHANGELOG if exists

5. **Ensure code quality**
   - Run Black and Ruff
   - Test thoroughly
   - No commented-out code

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify it's not a configuration problem
3. Test with the latest version

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Configure server with...
2. Run command...
3. See error...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.11.5]
- MCP SDK version: [e.g., 1.1.2]

**Error Messages**
```
Paste any error messages here
```

**Additional Context**
Any other relevant information
```

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists
2. Check if it's already been requested
3. Provide a clear use case
4. Explain how it benefits users

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How could this be implemented?

**Alternatives Considered**
Other ways to achieve this goal

**Additional Context**
Any other relevant information
```

## API Considerations

### Rate Limiting

While the AIC API doesn't have explicit rate limits, be considerate:

- Don't make excessive requests
- Implement appropriate delays if needed
- Cache results when possible

### Error Handling

Always handle API errors gracefully:

```python
try:
    data = await make_api_request(endpoint, params)
except AICAPIError as e:
    logger.error(f"API error: {str(e)}")
    return [TextContent(type="text", text=f"Error: {str(e)}")]
```

### Data Validation

Validate user input before making API calls:

```python
if limit < 1 or limit > MAX_RESULTS:
    return [TextContent(
        type="text",
        text=f"Limit must be between 1 and {MAX_RESULTS}"
    )]
```

## Code Review Process

All contributions go through code review. Reviewers will check for:

- Code quality and style
- Documentation completeness
- Test coverage
- Error handling
- Performance considerations
- Security implications

## Questions?

If you have questions:

- Open a discussion on GitHub
- Comment on relevant issues
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes for significant contributions
- README acknowledgments section

---

Thank you for contributing to make this project better! 🎨
