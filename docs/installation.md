# Installation Guide

This guide provides detailed instructions for installing and configuring the vnstock MCP server for Claude Desktop integration.

## System Requirements

Before installing the vnstock MCP server, ensure your system meets the following requirements:

- Python 3.8 or higher installed on your system
- Claude Desktop application properly configured and running
- Stable internet connection for accessing Vietnamese stock market data
- Administrative privileges for package installation (may be required)

## Installation Methods

### Method 1: Direct GitHub Installation

The simplest installation method uses pip to install directly from the GitHub repository:

```bash
pip install git+https://github.com/vietnh/vnstock-mcp-server.git
```

This command downloads the latest version from the main branch and installs all required dependencies automatically.

### Method 2: Development Installation

For users who want to modify the code or contribute to the project:

```bash
git clone https://github.com/vietnh/vnstock-mcp-server.git
cd vnstock-mcp-server
pip install -e .
```

The `-e` flag installs the package in editable mode, allowing you to make changes to the code that take effect immediately.

### Method 3: Virtual Environment Installation

For isolated dependency management, create a virtual environment:

```bash
python -m venv vnstock-env
vnstock-env\Scripts\activate  # Windows
source vnstock-env/bin/activate  # macOS/Linux

pip install git+https://github.com/vietnh/vnstock-mcp-server.git
```

## Dependency Installation

If you encounter dependency issues, install requirements manually:

```bash
pip install vnstock>=3.2.0 mcp>=0.1.0 pandas>=1.5.0
```

## Claude Desktop Configuration

After successful installation, configure Claude Desktop to recognize the MCP server.

### Locate Configuration File

Find your Claude Desktop configuration file at:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Add Server Configuration

Edit the configuration file to include the vnstock server:

```json
{
  "mcpServers": {
    "vnstock": {
      "command": "vnstock-mcp-server",
      "args": []
    }
  }
}
```

## Verification Steps

After installation and configuration, verify the setup:

1. Restart Claude Desktop completely
2. Check that the vnstock MCP server appears as "online" in Claude Desktop
3. Test basic functionality by asking Claude about Vietnamese stock prices
4. Review any error messages in Claude Desktop logs if connection fails

## Troubleshooting Common Issues

### MCP Server Offline

If the server appears offline in Claude Desktop:

- Verify Python environment has access to installed packages
- Check that all dependencies are properly installed
- Ensure Claude Desktop configuration syntax is correct
- Restart Claude Desktop after making configuration changes

### Import Errors

For vnstock import failures:

- Confirm vnstock installation: `pip show vnstock`
- Update to latest version: `pip install -U vnstock`
- Check internet connectivity for market data access

### Permission Issues

If installation fails due to permissions:

- Use `pip install --user` for user-specific installation
- Run command prompt as administrator on Windows
- Use `sudo` with caution on macOS/Linux systems

### Version Conflicts

For dependency version conflicts:

- Create isolated virtual environment
- Update pip to latest version: `pip install -U pip`
- Install specific package versions if needed

## Next Steps

After successful installation, proceed to the usage guide to learn how to interact with Vietnamese stock market data through Claude Desktop.
