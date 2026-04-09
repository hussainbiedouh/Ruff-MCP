# Ruff MCP Server

A Model Context Protocol (MCP) server that provides Ruff Python linter and formatter tools for AI assistants.

## Features

- **ruff_check** - Run ruff linter on Python files/directories
- **ruff_format** - Format Python code with ruff
- **ruff_fix** - Auto-fix linting issues

## Installation

### Prerequisites

- Python 3.10+
- [Ruff](https://github.com/astral-sh/ruff) installed

### Setup

```bash
# Clone the repository
git clone https://github.com/hussainbiedouh/Ruff-MCP.git
cd Ruff-MCP

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install
pip install -e .
```

## Usage

### Run the MCP Server

```bash
ruff-mcp
```

Or with Python:

```bash
python -m ruff_mcp
```

### Configuration

Configure in your MCP client (e.g., OpenCode):

```json
{
  "mcp": {
    "ruff-mcp": {
      "type": "local",
      "command": ["path/to/.venv/Scripts/python.exe", "-m", "ruff_mcp"]
    }
  }
}
```

## Tools

### ruff_check

Run ruff linter on files or directories.

```json
{
  "name": "ruff_check",
  "arguments": {
    "path": "src/",
    "fix": false,
    "output_format": "text"
  }
}
```

### ruff_format

Format Python code.

```json
{
  "name": "ruff_format",
  "arguments": {
    "path": "src/",
    "check": false,
    "diff": false
  }
}
```

### ruff_fix

Auto-fix linting issues.

```json
{
  "name": "ruff_fix",
  "arguments": {
    "path": "src/",
    "unsafe": false
  }
}
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
```

## License

MIT
