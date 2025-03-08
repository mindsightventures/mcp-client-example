# MCP Client Example

[![CI](https://github.com/mindsightventures/mcp-client-example/actions/workflows/ci.yml/badge.svg)](https://github.com/mindsightventures/mcp-client-example/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/mindsightventures/mcp-client-example/graph/badge.svg?token=JpRATuPYad)](https://codecov.io/gh/mindsightventures/mcp-client-example)

A Python client for the [Model Control Protocol (MCP)](https://github.com/anthropics/anthropic-tools/tree/main/mcp) that allows you to connect to MCP servers and use their tools with Claude.

## Features

- Connect to any MCP server (Python or JavaScript)
- Automatically discover available tools
- Process user queries using Claude and execute tool calls
- Interactive chat loop for testing

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/mindsightventures/mcp-client-example.git
cd mcp-client-example

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# For development, install dev dependencies
uv pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

## Configuration

Create a `.env` file in the root directory with your Anthropic API key:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### Running the Client

To run the client, you need to provide the path to an MCP server script:

```bash
# Run the client with a Python MCP server
python -m mcp_client path/to/server.py

# Run the client with a JavaScript MCP server
python -m mcp_client path/to/server.js
```

### Example with Weather MCP Server

This example shows how to use the client with the [MCP Server Example](https://github.com/mindsightventures/mcp-server-example):

1. First, clone and run the MCP server in one terminal:

```bash
git clone https://github.com/mindsightventures/mcp-server-example.git
cd mcp-server-example
uv run src/weather/weather.py
```

2. Then, in another terminal, run the MCP client:

```bash
cd mcp-client-example
python -m mcp_client ../mcp-server-example/src/weather/weather.py
```

3. Now you can ask questions about the weather:

```bash
Query: what is the weather in New York?
```

## Development

### Running Tests

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src
```

### Code Quality

This project uses several tools to ensure code quality:

- **black**: Code formatter
- **isort**: Import sorter
- **ruff**: Linter
- **mypy**: Type checker

You can run these tools manually:

```bash
uv run black src
uv run isort src
uv run ruff check src
uv run mypy src
```

Or use pre-commit to run them automatically before each commit:

```bash
pre-commit run --all-files
```

## License

MIT
