# Vnstock MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to Vietnamese stock market data through the vnstock library. This server enables Claude Desktop to retrieve real-time stock prices, historical data, company fundamentals, and market analysis for Vietnamese securities.

## Features

The vnstock MCP server provides eight specialized tools for Vietnamese market analysis:

- **Stock Price Retrieval**: Current stock prices with OHLC data and volume information
- **Historical Data Analysis**: Comprehensive historical price data with multiple timeframe options
- **Company Overview**: Detailed company information and fundamental metrics
- **Financial Statements**: Balance sheet, income statement, and cash flow data
- **Market Indices**: VNINDEX, HNX30, VN30, and UPCOM performance tracking
- **Company Listings**: Complete directory of listed companies across Vietnamese exchanges
- **Foreign Trading Data**: Foreign investor trading activity and sentiment analysis
- **Stock Search**: Intelligent search capabilities for companies and symbols

## Prerequisites

- Python 3.8 or higher
- Claude Desktop application
- Active internet connection for market data access

## Installation

### Method 1: Direct Installation from GitHub

Install the MCP server directly from this repository:

```bash
pip install git+https://github.com/vietnh/vnstock-mcp-server.git
```

### Method 2: Clone and Install

Clone the repository and install locally:

```bash
git clone https://github.com/vietnh/vnstock-mcp-server.git
cd vnstock-mcp-server
pip install -e .
```

### Method 3: Requirements File Installation

For environments requiring specific dependency management:

```bash
git clone https://github.com/vietnh/vnstock-mcp-server.git
cd vnstock-mcp-server
pip install -r requirements.txt
```

## Configuration

### Claude Desktop Configuration

Add the following configuration to your Claude Desktop MCP settings file:

#### For Package Installation:
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

#### For Repository Installation:
```json
{
  "mcpServers": {
    "vnstock": {
      "command": "python",
      "args": ["-m", "vnstock_mcp_server"]
    }
  }
}
```

### Configuration File Location

The Claude Desktop configuration file is typically located at:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Usage Examples

After successful installation and configuration, you can interact with Vietnamese stock market data through Claude Desktop using natural language queries:

### Stock Price Queries
- "What is the current price of VIC stock?"
- "Show me today's trading data for VCB"
- "Get the latest price information for MSN"

### Historical Data Analysis
- "Retrieve 30 days of historical data for TCB"
- "Show me weekly price data for VIC from January to March 2025"
- "Get monthly historical data for VNM over the past year"

### Company Research
- "Give me an overview of Vinamilk company"
- "Show financial statements for Techcombank"
- "What are the key financial ratios for VIC?"

### Market Analysis
- "How is the VNINDEX performing today?"
- "List all banking companies on HOSE"
- "Search for companies in the technology sector"

## Available Tools

### get_stock_price
Retrieves current stock price and basic trading information for Vietnamese stocks.

**Parameters:**
- `symbol` (required): Stock symbol (e.g., "VIC", "VCB", "MSN")

### get_historical_data
Provides historical price data for technical analysis and charting.

**Parameters:**
- `symbol` (required): Stock symbol
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `resolution` (optional): Data resolution ("1D", "1W", "1M")

### get_company_overview
Delivers comprehensive company information and fundamental data.

**Parameters:**
- `symbol` (required): Stock symbol

### get_financial_data
Accesses financial statements and ratios for fundamental analysis.

**Parameters:**
- `symbol` (required): Stock symbol
- `report_type` (optional): "BalanceSheet", "IncomeStatement", or "CashFlow"
- `frequency` (optional): "Quarterly" or "Yearly"

### list_companies
Provides listings of companies across Vietnamese stock exchanges.

**Parameters:**
- `exchange` (optional): "HOSE", "HNX", "UPCOM", or "ALL"
- `sector` (optional): Industry sector filter

### get_market_overview
Supplies market indices information and performance metrics.

**Parameters:**
- `index` (optional): "VNINDEX", "HNX30", "UPCOM", or "VN30"

### get_foreign_trading
Delivers foreign investor trading data for market sentiment analysis.

**Parameters:**
- `symbol` (optional): Stock symbol or market index
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

### search_stocks
Enables fuzzy matching search for stocks by company name or symbol.

**Parameters:**
- `query` (required): Search query (company name or symbol)
- `limit` (optional): Maximum number of results to return

## Troubleshooting

### Connection Issues
If Claude Desktop shows the MCP server as offline:

1. Verify that all dependencies are properly installed
2. Check the Claude Desktop configuration file syntax
3. Restart Claude Desktop after configuration changes
4. Review system logs for specific error messages

### Import Errors
For vnstock import failures:

1. Ensure vnstock is installed: `pip install -U vnstock`
2. Verify Python environment compatibility
3. Check internet connectivity for market data access

### Performance Considerations
- Market data requests may experience latency during high-traffic periods
- Historical data queries for extended periods may require additional processing time
- Some functions may have rate limiting from upstream data providers

## Dependencies

- **vnstock**: Vietnamese stock market data library (>=3.2.0)
- **mcp**: Model Context Protocol framework (>=0.1.0)
- **pandas**: Data manipulation and analysis (>=1.5.0)
- **asyncio-compat**: Asynchronous programming support (>=0.2.0)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest enhancements through the GitHub issue tracker.

## Support

For questions, issues, or feature requests, please create an issue in the GitHub repository or contact the maintainer.

## Acknowledgments

- Built on the vnstock library by [thinh-vu](https://github.com/thinh-vu/vnstock)
- Implements the Model Context Protocol by Anthropic
- Designed for integration with Claude Desktop

## Disclaimer

This software is provided for research and educational purposes. Users are responsible for compliance with relevant financial data usage policies and regulations. The authors are not responsible for any financial decisions made based on data provided by this software.
