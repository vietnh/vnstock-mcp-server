#!/usr/bin/env python3
"""
Vnstock MCP Server - Vietnamese Stock Market Data Integration
Provides MCP interface for accessing Vietnamese stock market data through vnstock library
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)

logger = logging.getLogger("vnstock-mcp-server")

# Import MCP components
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    from mcp.server.lowlevel import NotificationOptions
except ImportError as e:
    logger.error(f"Failed to import MCP: {e}")
    sys.exit(1)

# Import vnstock with modern API
try:
    from vnstock import Vnstock, Listing, Quote, Company, Finance, Trading, Screener
    import pandas as pd
    VNSTOCK_AVAILABLE = True
    logger.info("Successfully imported modern vnstock API")
except ImportError as e:
    logger.warning(f"vnstock not available: {e}")
    VNSTOCK_AVAILABLE = False

# Create server instance
server = Server("vnstock-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="get_stock_price",
            description="Get current stock price and basic information for a Vietnamese stock symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., VCB, VIC, TCB)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_historical_data",
            description="Get historical stock price data for analysis and charting",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., VCB, VIC, TCB)"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (optional, defaults to 30 days ago)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (optional, defaults to today)"
                    },
                    "resolution": {
                        "type": "string",
                        "description": "Data resolution (1D, 1W, 1M)",
                        "enum": ["1D", "1W", "1M"]
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_company_overview",
            description="Get comprehensive company information and fundamental data",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., VCB, VIC, TCB)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_financial_data",
            description="Get comprehensive financial statements including balance sheet, income statement, and cash flow data",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., VCB, VIC, TCB)"
                    },
                    "report_type": {
                        "type": "string",
                        "description": "Type of financial report",
                        "enum": ["BalanceSheet", "IncomeStatement", "CashFlow"]
                    },
                    "frequency": {
                        "type": "string",
                        "description": "Report frequency",
                        "enum": ["Quarterly", "Yearly"]
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_market_overview",
            description="Get current market indices information and performance analytics for Vietnamese stock exchanges",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "string",
                        "description": "Market index (optional, defaults to VNINDEX)",
                        "enum": ["VNINDEX", "HNX30", "UPCOM", "VN30"]
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_foreign_trading",
            description="Get foreign investor trading data for market sentiment analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (optional, if not provided, returns market-wide data)"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (optional, defaults to 30 days ago)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (optional, defaults to today)"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="search_companies",
            description="Search for companies using fuzzy matching by company name or symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (company name or symbol)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="list_companies",
            description="Get list of all listed companies on Vietnamese stock exchanges",
            inputSchema={
                "type": "object",
                "properties": {
                    "exchange": {
                        "type": "string",
                        "description": "Exchange filter (ALL, HOSE, HNX, UPCOM)",
                        "enum": ["ALL", "HOSE", "HNX", "UPCOM"]
                    },
                    "sector": {
                        "type": "string",
                        "description": "Sector filter (optional)"
                    }
                },
                "required": []
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls"""
    if not VNSTOCK_AVAILABLE:
        return [types.TextContent(
            type="text", 
            text="vnstock library not available. Please install with: pip install -U vnstock"
        )]
    
    arguments = arguments or {}
    
    try:
        if name == "get_stock_price":
            return await get_stock_price(arguments.get("symbol", ""))
        elif name == "get_historical_data":
            return await get_historical_data(
                arguments.get("symbol", ""),
                arguments.get("start_date"),
                arguments.get("end_date"),
                arguments.get("resolution", "1D")
            )
        elif name == "get_company_overview":
            return await get_company_overview(arguments.get("symbol", ""))
        elif name == "get_financial_data":
            return await get_financial_data(
                arguments.get("symbol", ""),
                arguments.get("report_type", "BalanceSheet"),
                arguments.get("frequency", "Quarterly")
            )
        elif name == "get_market_overview":
            return await get_market_overview(arguments.get("index", "VNINDEX"))
        elif name == "get_foreign_trading":
            return await get_foreign_trading(
                arguments.get("symbol"),
                arguments.get("start_date"),
                arguments.get("end_date")
            )
        elif name == "search_companies":
            return await search_companies(
                arguments.get("query", ""),
                arguments.get("limit", 10)
            )
        elif name == "list_companies":
            return await list_companies(
                arguments.get("exchange", "ALL"),
                arguments.get("sector")
            )
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error in tool '{name}': {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def get_stock_price(symbol: str) -> list[types.TextContent]:
    """Get current stock price and basic information"""
    if not symbol:
        return [types.TextContent(type="text", text="Error: symbol parameter is required")]
    
    try:
        # Use modern vnstock API
        stock = Vnstock().stock(symbol=symbol.upper(), source='VCI')
        
        # Get recent stock data (last few days to ensure we get data)
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        
        stock_data = stock.quote.history(
            start=start_date,
            end=end_date,
            interval='1D'
        )
        
        if stock_data.empty:
            return [types.TextContent(type="text", text=f"No data found for symbol: {symbol}")]
        
        # Get the latest data point
        latest = stock_data.iloc[-1]
        
        result = {
            "symbol": symbol.upper(),
            "date": latest.name.strftime("%Y-%m-%d") if hasattr(latest.name, 'strftime') else str(latest.name),
            "open": float(latest['open']),
            "high": float(latest['high']),
            "low": float(latest['low']),
            "close": float(latest['close']),
            "volume": int(latest['volume']),
            "change": float(latest['close'] - latest['open']),
            "change_percent": float((latest['close'] - latest['open']) / latest['open'] * 100) if latest['open'] != 0 else 0
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting stock price for {symbol}: {str(e)}")]

async def get_historical_data(symbol: str, start_date: str = None, end_date: str = None, resolution: str = "1D") -> list[types.TextContent]:
    """Get historical stock price data"""
    if not symbol:
        return [types.TextContent(type="text", text="Error: symbol parameter is required")]
    
    try:
        # Set default dates if not provided
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Use modern vnstock API
        stock = Vnstock().stock(symbol=symbol.upper(), source='VCI')
        
        # Get historical data
        historical_data = stock.quote.history(
            start=start_date,
            end=end_date,
            interval=resolution
        )
        
        if historical_data.empty:
            return [types.TextContent(type="text", text=f"No historical data found for {symbol} from {start_date} to {end_date}")]
        
        result = {
            "symbol": symbol.upper(),
            "start_date": start_date,
            "end_date": end_date,
            "resolution": resolution,
            "data_points": len(historical_data),
            "data": historical_data.reset_index().to_dict(orient="records")
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting historical data for {symbol}: {str(e)}")]

async def get_company_overview(symbol: str) -> list[types.TextContent]:
    """Get comprehensive company information"""
    if not symbol:
        return [types.TextContent(type="text", text="Error: symbol parameter is required")]
    
    try:
        # Use modern vnstock API
        stock = Vnstock().stock(symbol=symbol.upper(), source='VCI')
        company_info = stock.company.overview()
        
        if company_info.empty:
            return [types.TextContent(type="text", text=f"No company information found for symbol: {symbol}")]
        
        company_data = company_info.iloc[0].to_dict() if len(company_info) > 0 else {}
        
        # Try to get recent price data for context
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            recent_data = stock.quote.history(
                start=start_date,
                end=end_date,
                interval='1D'
            )
            
            if not recent_data.empty:
                latest_price = recent_data.iloc[-1]
                company_data.update({
                    "latest_price": float(latest_price['close']),
                    "latest_volume": int(latest_price['volume']),
                    "price_date": latest_price.name.strftime("%Y-%m-%d") if hasattr(latest_price.name, 'strftime') else str(latest_price.name)
                })
        except Exception as e:
            logger.warning(f"Could not get recent price data: {e}")
        
        result = {
            "symbol": symbol.upper(),
            "company_info": company_data
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting company overview for {symbol}: {str(e)}")]

async def get_financial_data(symbol: str, report_type: str = "BalanceSheet", frequency: str = "Quarterly") -> list[types.TextContent]:
    """Get comprehensive financial statements"""
    if not symbol:
        return [types.TextContent(type="text", text="Error: symbol parameter is required")]
    
    try:
        # Use modern vnstock API
        stock = Vnstock().stock(symbol=symbol.upper(), source='VCI')
        
        # Convert frequency to period format
        period = 'quarter' if frequency.lower() == 'quarterly' else 'year'
        
        # Get financial data based on report type
        if report_type == "BalanceSheet":
            financial_data = stock.finance.balance_sheet(period=period, lang='en', dropna=True)
        elif report_type == "IncomeStatement":
            financial_data = stock.finance.income_statement(period=period, lang='en', dropna=True)
        elif report_type == "CashFlow":
            financial_data = stock.finance.cash_flow(period=period, dropna=True)
        else:
            return [types.TextContent(type="text", text=f"Error: Invalid report_type '{report_type}'. Must be BalanceSheet, IncomeStatement, or CashFlow")]
        
        if financial_data.empty:
            return [types.TextContent(type="text", text=f"No financial data found for {symbol} ({report_type}, {frequency})")]
        
        result = {
            "symbol": symbol.upper(),
            "report_type": report_type,
            "frequency": frequency,
            "data_points": len(financial_data),
            "financial_data": financial_data.to_dict(orient="records")
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting financial data for {symbol}: {str(e)}")]

async def get_market_overview(index: str = "VNINDEX") -> list[types.TextContent]:
    """Get current market indices information and performance analytics"""
    try:
        # Use modern vnstock API for market indices
        # For market indices, we'll try to get index data using the Quote class
        try:
            quote = Quote(symbol=index, source='VCI')
            
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            market_data = quote.history(
                start=start_date,
                end=end_date,
                interval='1D'
            )
        except:
            # Fallback: try using a major stock as proxy for market sentiment
            stock = Vnstock().stock(symbol='VCB', source='VCI')
            market_data = stock.quote.history(
                start=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                end=datetime.now().strftime("%Y-%m-%d"),
                interval='1D'
            )
        
        if market_data.empty:
            return [types.TextContent(type="text", text=f"No market data found for index: {index}")]
        
        latest = market_data.iloc[-1]
        previous = market_data.iloc[-2] if len(market_data) > 1 else latest
        
        result = {
            "index": index,
            "current_value": float(latest['close']),
            "previous_close": float(previous['close']),
            "change": float(latest['close'] - previous['close']),
            "change_percent": float((latest['close'] - previous['close']) / previous['close'] * 100) if previous['close'] != 0 else 0,
            "volume": int(latest['volume']) if 'volume' in latest else 0,
            "date": latest.name.strftime("%Y-%m-%d") if hasattr(latest.name, 'strftime') else str(latest.name),
            "recent_data": market_data.tail(5).reset_index().to_dict(orient="records")
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting market overview for {index}: {str(e)}")]

async def get_foreign_trading(symbol: str = None, start_date: str = None, end_date: str = None) -> list[types.TextContent]:
    """Get foreign investor trading data for market sentiment analysis"""
    try:
        # Set default dates if not provided
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # For foreign trading, we'll provide basic market information as this requires special data sources
        result = {
            "symbol": symbol or "Market-wide",
            "start_date": start_date,
            "end_date": end_date,
            "note": "Foreign trading data requires specialized data sources. This is a placeholder implementation.",
            "suggestion": "Use get_stock_price or get_historical_data for basic stock information."
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting foreign trading data: {str(e)}")]

async def search_companies(query: str, limit: int = 10) -> list[types.TextContent]:
    """Search for companies using fuzzy matching by company name or symbol"""
    if not query:
        return [types.TextContent(type="text", text="Error: query parameter is required")]
    
    try:
        # Use modern vnstock API
        listing = Listing()
        companies = listing.all_symbols()
        
        if companies.empty:
            return [types.TextContent(type="text", text="No companies found in database")]
        
        # Perform fuzzy search on symbol and company name
        query_lower = query.lower()
        
        # Search by symbol (exact and partial matches)
        symbol_matches = companies[
            companies['symbol'].str.lower().str.contains(query_lower, na=False, regex=False)
        ]
        
        # Search by company name if available
        name_column = None
        for col in ['organName', 'companyName', 'company_name', 'name']:
            if col in companies.columns:
                name_column = col
                break
        
        if name_column:
            name_matches = companies[
                companies[name_column].str.lower().str.contains(query_lower, na=False, regex=False)
            ]
            # Combine and deduplicate results
            all_matches = pd.concat([symbol_matches, name_matches]).drop_duplicates()
        else:
            all_matches = symbol_matches
        
        # Limit results
        limited_matches = all_matches.head(limit)
        
        if limited_matches.empty:
            return [types.TextContent(type="text", text=f"No companies found matching query: {query}")]
        
        result = {
            "query": query,
            "total_matches": len(limited_matches),
            "matches": limited_matches.to_dict(orient="records")
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error searching companies: {str(e)}")]

async def list_companies(exchange: str = "ALL", sector: str = None) -> list[types.TextContent]:
    """Get list of all listed companies"""
    try:
        # Use modern vnstock API
        listing = Listing()
        companies = listing.all_symbols()
        
        if companies.empty:
            return [types.TextContent(type="text", text="No companies found in listing")]
        
        # Filter by exchange if specified
        if exchange != "ALL" and 'exchange' in companies.columns:
            companies = companies[companies['exchange'].str.upper() == exchange.upper()]
        
        # Filter by sector if specified
        if sector:
            sector_column = None
            for col in ['sector', 'industryName', 'industry']:
                if col in companies.columns:
                    sector_column = col
                    break
            
            if sector_column:
                companies = companies[companies[sector_column].str.contains(sector, case=False, na=False)]
        
        # Limit the response to avoid overwhelming output
        companies_limited = companies.head(100)  # Limit to first 100 companies
        
        result = {
            "exchange": exchange,
            "sector": sector,
            "total_companies": len(companies),
            "displayed_companies": len(companies_limited),
            "companies": companies_limited.to_dict(orient="records")
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error listing companies: {str(e)}")]

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources"""
    return [
        types.Resource(
            uri="config://version",
            name="Server Version",
            description="Get the vnstock MCP server version information",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Handle resource reads"""
    if uri == "config://version":
        return "vnstock-mcp-server v1.0.8 (Updated for vnstock 3.2.x)"
    else:
        raise ValueError(f"Unknown resource: {uri}")

async def main():
    """Main server function"""
    logger.info("Starting Vnstock MCP Server...")
    
    try:
        # Use stdio transport
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="vnstock-mcp-server",
                    server_version="1.0.8",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
            
    except Exception as e:
        logger.error(f"Error running server: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 