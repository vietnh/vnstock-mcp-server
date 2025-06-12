#!/usr/bin/env python3
"""
Vnstock MCP Server - Vietnamese Stock Market Data Integration
Provides MCP interface for accessing Vietnamese stock market data through vnstock library
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta

# MCP Server imports
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.types import (
        CallToolRequest,
        CallToolResult,
        ListToolsRequest,
        ListToolsResult,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
    import mcp.types as types
    MCP_AVAILABLE = True
except ImportError as e:
    MCP_AVAILABLE = False
    print(f"MCP import error: {e}", file=sys.stderr)

# Pandas import
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("pandas library not available", file=sys.stderr)

# Vnstock imports
try:
    import vnstock as vn
    # Test basic import functionality by accessing a known function
    # Instead of importing specific functions, we'll use vn.function_name() format
    test_access = hasattr(vn, 'stock_historical_data') or hasattr(vn, 'listing_companies')
    VNSTOCK_AVAILABLE = True
    logger.info("vnstock library successfully imported")
except ImportError:
    VNSTOCK_AVAILABLE = False
    logging.warning("vnstock library not available. Install with: pip install -U vnstock")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vnstock-mcp-server")

# Add diagnostic output
print(f"Python executable: {sys.executable}", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Python path: {sys.path}", file=sys.stderr)
print(f"Working directory: {os.getcwd()}", file=sys.stderr)

class VnstockMCPServer:
    """MCP Server for Vietnamese Stock Market Data using vnstock"""
    
    def __init__(self):
        self.app = Server("vnstock-mcp-server")
        self.setup_tools()
        
    def setup_tools(self):
        """Setup MCP tools for stock market data access"""
        
        @self.app.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools for Vietnamese stock market data"""
            if not VNSTOCK_AVAILABLE:
                return [Tool(
                    name="vnstock_status",
                    description="Check vnstock library availability status",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )]
            
            return [
                Tool(
                    name="get_stock_price",
                    description="Get current stock price and basic information for a Vietnamese stock symbol",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Stock symbol (e.g., VIC, VCB, MSN)"
                            }
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_historical_data",
                    description="Get historical stock price data for analysis and charting",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Stock symbol (e.g., VIC, VCB, MSN)"
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format (default: 30 days ago)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format (default: today)"
                            },
                            "resolution": {
                                "type": "string",
                                "description": "Data resolution: 1D (daily), 1W (weekly), 1M (monthly)",
                                "enum": ["1D", "1W", "1M"],
                                "default": "1D"
                            }
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_company_overview",
                    description="Get comprehensive company information and fundamental data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Stock symbol (e.g., VIC, VCB, MSN)"
                            }
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_financial_data",
                    description="Get financial statements and ratios for fundamental analysis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Stock symbol (e.g., VIC, VCB, MSN)"
                            },
                            "report_type": {
                                "type": "string",
                                "description": "Financial report type",
                                "enum": ["BalanceSheet", "IncomeStatement", "CashFlow"],
                                "default": "IncomeStatement"
                            },
                            "frequency": {
                                "type": "string",
                                "description": "Report frequency",
                                "enum": ["Quarterly", "Yearly"],
                                "default": "Quarterly"
                            }
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="list_companies",
                    description="Get list of all listed companies on Vietnamese stock exchanges",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "exchange": {
                                "type": "string",
                                "description": "Stock exchange",
                                "enum": ["HOSE", "HNX", "UPCOM", "ALL"],
                                "default": "ALL"
                            },
                            "sector": {
                                "type": "string",
                                "description": "Industry sector filter (optional)"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_market_overview",
                    description="Get Vietnamese stock market overview and indices information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "index": {
                                "type": "string",
                                "description": "Market index",
                                "enum": ["VNINDEX", "HNX30", "UPCOM", "VN30"],
                                "default": "VNINDEX"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_foreign_trading",
                    description="Get foreign investor trading data for market sentiment analysis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Stock symbol or market index (optional)"
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format (default: 30 days ago)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format (default: today)"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="search_stocks",
                    description="Search for stocks by company name or symbol with fuzzy matching",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (company name or symbol)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]

        @self.app.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls for stock market data operations"""
            
            if not VNSTOCK_AVAILABLE and name != "vnstock_status":
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="Error: vnstock library is not available. Please install with: pip install -U vnstock"
                    )]
                )
            
            try:
                if name == "vnstock_status":
                    return await self._handle_vnstock_status()
                elif name == "get_stock_price":
                    return await self._handle_get_stock_price(arguments)
                elif name == "get_historical_data":
                    return await self._handle_get_historical_data(arguments)
                elif name == "get_company_overview":
                    return await self._handle_get_company_overview(arguments)
                elif name == "get_financial_data":
                    return await self._handle_get_financial_data(arguments)
                elif name == "list_companies":
                    return await self._handle_list_companies(arguments)
                elif name == "get_market_overview":
                    return await self._handle_get_market_overview(arguments)
                elif name == "get_foreign_trading":
                    return await self._handle_get_foreign_trading(arguments)
                elif name == "search_stocks":
                    return await self._handle_search_stocks(arguments)
                else:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Unknown tool: {name}"
                        )]
                    )
                    
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Error executing {name}: {str(e)}"
                    )]
                )

    async def _handle_vnstock_status(self) -> CallToolResult:
        """Check vnstock library status"""
        status = {
            "vnstock_available": VNSTOCK_AVAILABLE,
            "server_status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        if VNSTOCK_AVAILABLE:
            try:
                status["vnstock_version"] = vn.__version__
            except:
                status["vnstock_version"] = "unknown"
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps(status, indent=2)
            )]
        )

    async def _handle_get_stock_price(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get current stock price and basic information"""
        symbol = arguments["symbol"].upper()
        
        try:
            # Get current price data using vnstock module functions
            price_data = vn.stock_historical_data(
                symbol=symbol,
                start_date=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                end_date=datetime.now().strftime("%Y-%m-%d"),
                resolution="1D",
                type="stock"
            )
            
            if price_data.empty:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"No data found for symbol: {symbol}"
                    )]
                )
            
            # Get latest price information
            latest = price_data.iloc[-1]
            
            result = {
                "symbol": symbol,
                "date": latest.name.strftime("%Y-%m-%d") if hasattr(latest.name, 'strftime') else str(latest.name),
                "open": float(latest['open']),
                "high": float(latest['high']),
                "low": float(latest['low']),
                "close": float(latest['close']),
                "volume": int(latest['volume']),
                "change": float(latest['close'] - latest['open']),
                "change_percent": float((latest['close'] - latest['open']) / latest['open'] * 100)
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting stock price for {symbol}: {str(e)}"
                )]
            )

    async def _handle_get_historical_data(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get historical stock price data"""
        symbol = arguments["symbol"].upper()
        start_date = arguments.get("start_date", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        end_date = arguments.get("end_date", datetime.now().strftime("%Y-%m-%d"))
        resolution = arguments.get("resolution", "1D")
        
        try:
            data = vn.stock_historical_data(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                resolution=resolution,
                type="stock"
            )
            
            if data.empty:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"No historical data found for {symbol} from {start_date} to {end_date}"
                    )]
                )
            
            # Convert to JSON-serializable format
            result = {
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "resolution": resolution,
                "data_points": len(data),
                "data": data.reset_index().to_dict(orient="records")
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting historical data for {symbol}: {str(e)}"
                )]
            )

    async def _handle_get_company_overview(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get company overview and fundamental information"""
        symbol = arguments["symbol"].upper()
        
        try:
            # Get company overview using vnstock module
            overview = vn.company_overview(symbol)
            
            if overview.empty:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"No company overview found for symbol: {symbol}"
                    )]
                )
            
            # Convert to dictionary format
            result = overview.to_dict(orient="records")[0] if not overview.empty else {}
            result["symbol"] = symbol
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting company overview for {symbol}: {str(e)}"
                )]
            )

    async def _handle_get_financial_data(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get financial statements and ratios"""
        symbol = arguments["symbol"].upper()
        report_type = arguments.get("report_type", "IncomeStatement")
        frequency = arguments.get("frequency", "Quarterly")
        
        try:
            # Get financial data using vnstock module
            financial_data = vn.financial_flow(
                symbol=symbol,
                report_type=report_type,
                frequency=frequency
            )
            
            if financial_data.empty:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"No financial data found for {symbol}"
                    )]
                )
            
            result = {
                "symbol": symbol,
                "report_type": report_type,
                "frequency": frequency,
                "periods": len(financial_data.columns),
                "data": financial_data.reset_index().to_dict(orient="records")
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting financial data for {symbol}: {str(e)}"
                )]
            )

    async def _handle_list_companies(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get list of listed companies"""
        exchange = arguments.get("exchange", "ALL")
        sector = arguments.get("sector")
        
        try:
            # Get company listing using vnstock module
            companies = vn.listing_companies()
            
            if companies.empty:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="No company listings found"
                    )]
                )
            
            # Filter by exchange if specified
            if exchange != "ALL":
                companies = companies[companies['exchange'] == exchange]
            
            # Filter by sector if specified
            if sector:
                companies = companies[companies['icbName'].str.contains(sector, case=False, na=False)]
            
            result = {
                "exchange": exchange,
                "sector": sector,
                "total_companies": len(companies),
                "companies": companies.to_dict(orient="records")
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting company listings: {str(e)}"
                )]
            )

    async def _handle_get_market_overview(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get market overview and indices"""
        index = arguments.get("index", "VNINDEX")
        
        try:
            # Get index data
            index_data = vn.stock_historical_data(
                symbol=index,
                start_date=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                end_date=datetime.now().strftime("%Y-%m-%d"),
                resolution="1D",
                type="index"
            )
            
            if index_data.empty:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"No data found for index: {index}"
                    )]
                )
            
            latest = index_data.iloc[-1]
            
            result = {
                "index": index,
                "date": latest.name.strftime("%Y-%m-%d") if hasattr(latest.name, 'strftime') else str(latest.name),
                "value": float(latest['close']),
                "change": float(latest['close'] - latest['open']),
                "change_percent": float((latest['close'] - latest['open']) / latest['open'] * 100),
                "volume": int(latest['volume']) if 'volume' in latest else 0,
                "weekly_data": index_data.reset_index().to_dict(orient="records")
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting market overview for {index}: {str(e)}"
                )]
            )

    async def _handle_get_foreign_trading(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get foreign investor trading data"""
        symbol = arguments.get("symbol")
        start_date = arguments.get("start_date", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        end_date = arguments.get("end_date", datetime.now().strftime("%Y-%m-%d"))
        
        try:
            # Note: This would require specific vnstock functions for foreign trading data
            # Implementation depends on available vnstock API functions
            result = {
                "message": "Foreign trading data feature requires specific vnstock API implementation",
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "note": "This functionality can be implemented based on available vnstock foreign trading APIs"
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting foreign trading data: {str(e)}"
                )]
            )

    async def _handle_search_stocks(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Search for stocks by name or symbol"""
        query = arguments["query"].lower()
        limit = arguments.get("limit", 10)
        
        try:
            # Search by symbol or company name using vnstock module
            companies = vn.listing_companies()
            
            if companies.empty:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="No companies found in listing"
                    )]
                )
            
            # Search by symbol or company name
            matches = companies[
                companies['symbol'].str.lower().str.contains(query, na=False) |
                companies['companyName'].str.lower().str.contains(query, na=False)
            ].head(limit)
            
            result = {
                "query": query,
                "total_matches": len(matches),
                "limit": limit,
                "matches": matches.to_dict(orient="records")
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, default=str)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error searching stocks: {str(e)}"
                )]
            )

    async def run(self, transport_type: str = "stdio"):
        """Run the MCP server"""
        if not MCP_AVAILABLE:
            print("Error: MCP library not available. Install with: pip install mcp", file=sys.stderr)
            sys.exit(1)
        
        if transport_type == "stdio":
            try:
                from mcp.server.stdio import stdio_server
                
                logger.info("Starting Vnstock MCP Server with stdio transport...")
                print("Vnstock MCP Server starting...", file=sys.stderr)
                
                async with stdio_server() as (read_stream, write_stream):
                    await self.app.run(
                        read_stream,
                        write_stream,
                        InitializationOptions(
                            server_name="vnstock-mcp-server",
                            server_version="1.0.0",
                            capabilities=self.app.get_capabilities(
                                notification_options=NotificationOptions(),
                                experimental_capabilities={},
                            ),
                        ),
                    )
            except Exception as e:
                print(f"Error starting MCP server: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            raise ValueError(f"Unsupported transport type: {transport_type}")

def main():
    """Main entry point for the MCP server"""
    # Check for required dependencies
    if not MCP_AVAILABLE:
        print("Error: MCP library not available. Install with: pip install mcp", file=sys.stderr)
        sys.exit(1)
    
    if not PANDAS_AVAILABLE:
        print("Warning: pandas library not available. Some features may be limited.", file=sys.stderr)
    
    if not VNSTOCK_AVAILABLE:
        print("Warning: vnstock library not available. Install with: pip install -U vnstock", file=sys.stderr)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    try:
        import argparse
        
        parser = argparse.ArgumentParser(description="Vnstock MCP Server for Vietnamese Stock Market Data")
        parser.add_argument("--transport", default="stdio", choices=["stdio"], 
                           help="Transport type (default: stdio)")
        
        args = parser.parse_args()
        
        server = VnstockMCPServer()
        asyncio.run(server.run(args.transport))
    except KeyboardInterrupt:
        print("Server shutdown requested", file=sys.stderr)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
