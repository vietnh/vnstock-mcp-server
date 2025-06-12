# Vnstock MCP Server

A comprehensive Model Context Protocol (MCP) server that provides seamless access to Vietnamese stock market data through the vnstock library. This server enables Claude Desktop to retrieve real-time stock prices, historical data, company fundamentals, and market analysis for Vietnamese securities through simple NPX execution.

## Key Features

The vnstock MCP server delivers eight specialized tools for Vietnamese market analysis, including current stock price retrieval with OHLC data and volume information, comprehensive historical price data with multiple timeframe options, detailed company information and fundamental metrics, complete financial statement access including balance sheet, income statement, and cash flow data, performance tracking for VNINDEX, HNX30, VN30, and UPCOM indices, comprehensive directory of listed companies across Vietnamese exchanges, foreign investor trading activity and sentiment analysis, and intelligent search capabilities for companies and symbols.

## System Requirements

The system requires Node.js 14.0 or higher for NPX execution, Python 3.8 or higher for market data processing, Claude Desktop application for MCP integration, and an active internet connection for real-time market data access. These requirements ensure optimal performance and compatibility across different operating environments.

## Installation and Execution

### NPX Remote Execution (Recommended)

Execute the vnstock MCP server directly using NPX without local installation requirements. This approach provides immediate access to Vietnamese market data capabilities while automatically managing dependencies and updates.

```bash
# Start the MCP server directly
npx vnstock-mcp-server

# Test system requirements
npx vnstock-mcp-server --test

# Display help information
npx vnstock-mcp-server --help

# Install Python dependencies manually if needed
npx vnstock-mcp-server --install-deps
```

### Global Package Installation

Install the package globally for improved startup performance and offline availability. This method provides faster execution times for frequently used MCP server operations.

```bash
# Install globally
npm install -g vnstock-mcp-server

# Execute after global installation
vnstock-mcp-server
```

### Local Development Installation

Clone the repository for development purposes or custom modifications to the MCP server implementation.

```bash
git clone https://github.com/vietnh/vnstock-mcp-server.git
cd vnstock-mcp-server
npm install
npm start
```

## Claude Desktop Configuration

Configure Claude Desktop to recognize and utilize the vnstock MCP server through your MCP settings file. The configuration varies based on your chosen installation method and provides flexible integration options.

### NPX-Based Configuration

Configure Claude Desktop to execute the MCP server using NPX for automatic dependency management and updates.

```json
{
  "mcpServers": {
    "vnstock": {
      "command": "npx",
      "args": ["vnstock-mcp-server"]
    }
  }
}
```

### Global Installation Configuration

Configure Claude Desktop for globally installed packages to achieve optimal startup performance.

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

### Configuration File Locations

The Claude Desktop configuration file location varies by operating system. On Windows systems, locate the file at `%APPDATA%\Claude\claude_desktop_config.json`. macOS users should access `~/Library/Application Support/Claude/claude_desktop_config.json`. Linux installations utilize `~/.config/Claude/claude_desktop_config.json`.

## Natural Language Usage Examples

After successful installation and configuration, interact with Vietnamese stock market data through Claude Desktop using conversational queries that automatically trigger appropriate MCP server tools.

### Stock Price Analysis

Request current market information using natural language queries such as "What is the current price of VIC stock?" or "Show me today's trading data for VCB" or "Get the latest price information for MSN with volume analysis."

### Historical Data Research

Analyze market trends using time-based queries including "Retrieve 30 days of historical data for TCB" or "Show me weekly price data for VIC from January to March 2025" or "Get monthly historical data for VNM over the past year for trend analysis."

### Company Fundamental Analysis

Research Vietnamese companies using comprehensive queries such as "Give me an overview of Vinamilk company including financial metrics" or "Show financial statements for Techcombank with quarterly breakdowns" or "What are the key financial ratios for VIC compared to industry averages?"

### Market Performance Monitoring

Track broader market performance through index queries like "How is the VNINDEX performing today compared to recent trends?" or "List all banking companies on HOSE with market capitalization data" or "Search for companies in the technology sector with growth potential."

## Available MCP Tools

### Stock Price Retrieval Tool

Delivers current stock price and comprehensive trading information for Vietnamese securities. The tool requires a stock symbol parameter such as "VIC", "VCB", or "MSN" and returns opening, high, low, and closing prices along with volume data and calculated change metrics.

### Historical Data Analysis Tool

Provides extensive historical price data for technical analysis and charting applications. The tool accepts a required stock symbol parameter and optional start date, end date, and resolution parameters. Resolution options include "1D" for daily data, "1W" for weekly aggregation, and "1M" for monthly summaries.

### Company Overview Tool

Delivers comprehensive company information and fundamental analysis data. The tool requires a stock symbol parameter and returns detailed business descriptions, industry classifications, financial metrics, and market positioning information.

### Financial Statement Access Tool

Provides complete financial statement analysis capabilities for fundamental research. The tool accepts a required stock symbol parameter and optional report type selections including "BalanceSheet", "IncomeStatement", or "CashFlow" with frequency options of "Quarterly" or "Yearly" reporting periods.

### Company Directory Tool

Enables comprehensive market screening across Vietnamese stock exchanges. The tool accepts optional exchange parameters including "HOSE", "HNX", "UPCOM", or "ALL" along with optional sector filtering capabilities for targeted company discovery.

### Market Index Monitoring Tool

Supplies current market indices information and performance analytics. The tool accepts optional index parameters including "VNINDEX", "HNX30", "UPCOM", or "VN30" and returns current values, change calculations, and recent performance trends.

### Foreign Investment Analysis Tool

Delivers foreign investor trading data for market sentiment analysis. The tool accepts optional stock symbol or market index parameters along with configurable start date and end date parameters for custom timeframe analysis.

### Intelligent Stock Search Tool

Enables fuzzy matching search capabilities for stocks by company name or symbol. The tool requires a search query parameter and accepts an optional limit parameter to control the maximum number of results returned.

## System Diagnostics and Troubleshooting

### Connection Issues Resolution

If Claude Desktop displays the MCP server as offline, verify that all system requirements are met by executing the test command. Check the Claude Desktop configuration file syntax for proper JSON formatting. Restart Claude Desktop completely after making configuration changes. Review system logs for specific error messages that indicate the nature of connection problems.

### Dependency Management

For vnstock import failures, ensure the vnstock library is properly installed by running the dependency installation command. Verify Python environment compatibility with version 3.8 or higher. Check internet connectivity for reliable market data access from Vietnamese exchanges.

### Performance Optimization

Market data requests may experience latency variations during high-traffic periods when Vietnamese exchanges experience heavy trading volumes. Historical data queries for extended periods may require additional processing time depending on the requested timeframe and data volume. Some MCP tools may encounter rate limiting from upstream data providers during peak usage periods.

## Technical Dependencies

The system relies on vnstock library version 3.2.0 or higher for Vietnamese stock market data access, MCP framework version 0.1.0 or higher for protocol implementation, pandas library version 1.5.0 or higher for data manipulation and analysis, and asyncio-compat version 0.2.0 or higher for asynchronous programming support.

## Development and Contribution

Contributions to the vnstock MCP server are welcome through the GitHub repository. Submit pull requests for feature enhancements, report bugs through the issue tracker, or suggest improvements for market data analysis capabilities. The open-source nature of the project enables community-driven development and continuous improvement.

## Professional Support

For questions, technical issues, or feature requests, create an issue in the GitHub repository or contact the project maintainer. The repository includes comprehensive documentation, troubleshooting guides, and community support resources for optimal user experience.

## Acknowledgments and Licensing

This project builds upon the vnstock library developed by thinh-vu and implements the Model Context Protocol by Anthropic for seamless Claude Desktop integration. The software is licensed under the MIT License, providing flexible usage rights for both personal and commercial applications.

## Important Disclaimer

This software is provided for research and educational purposes. Users bear full responsibility for compliance with relevant financial data usage policies and regulations. The authors assume no responsibility for financial decisions made based on data provided by this software, and users should conduct independent verification of market data for investment purposes.
