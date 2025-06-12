# Usage Guide

This comprehensive guide demonstrates how to effectively utilize the vnstock MCP server for Vietnamese stock market analysis through Claude Desktop integration.

## Getting Started

Once the vnstock MCP server is properly installed and configured, Claude Desktop provides natural language access to comprehensive Vietnamese market data. The server exposes eight specialized tools that enable sophisticated financial analysis and research capabilities.

The integration allows you to request market information using conversational language, with Claude automatically selecting the appropriate tools and formatting responses for optimal readability and analysis.

## Stock Price Analysis

The stock price retrieval functionality provides current market data with comprehensive trading metrics. You can request current prices for any Vietnamese stock using the stock symbol or company name.

Example queries for price information include requesting current trading data for major Vietnamese companies, asking for specific price metrics such as opening prices or daily ranges, and obtaining volume information for liquidity analysis.

When requesting stock prices, the system returns opening, high, low, and closing prices along with trading volume and calculated change metrics. This information supports both quick market checks and detailed technical analysis workflows.

## Historical Data Retrieval

Historical data analysis capabilities enable comprehensive technical analysis and trend identification across multiple timeframes. The system supports daily, weekly, and monthly data resolution for different analytical approaches.

You can specify custom date ranges for historical analysis, allowing focused examination of specific market periods or events. The historical data includes all standard OHLC metrics with volume information for complete market context.

Example requests include retrieving six months of daily data for trend analysis, requesting weekly data for medium-term pattern recognition, and obtaining monthly data for long-term investment research.

## Company Fundamental Analysis

Company overview functionality provides comprehensive fundamental information including business descriptions, financial metrics, and market positioning data. This information supports investment research and due diligence processes.

The system delivers detailed company profiles that include industry classification, business descriptions, and key financial ratios. This information enables comparative analysis across companies and sectors within the Vietnamese market.

Financial statement access provides balance sheet, income statement, and cash flow data with both quarterly and annual reporting options. This comprehensive financial information supports detailed fundamental analysis and valuation modeling.

## Market Index Monitoring

Market overview capabilities provide real-time information about major Vietnamese indices including VNINDEX, HNX30, VN30, and UPCOM. This information enables broad market sentiment analysis and portfolio benchmarking.

Index data includes current values, daily changes, and recent performance metrics that support market timing decisions and overall portfolio management strategies.

## Company Discovery and Screening

Company listing functionality enables comprehensive market screening across all Vietnamese exchanges. You can filter companies by exchange, sector, or industry classification to identify investment opportunities.

The search capabilities support fuzzy matching for company names and symbols, making it easy to locate specific companies or explore related businesses within particular sectors.

Example screening queries include identifying all banking companies listed on HOSE, finding technology companies across all exchanges, and discovering companies in specific industries such as real estate or manufacturing.

## Foreign Investment Analysis

Foreign trading data provides insights into international investor sentiment and capital flows within Vietnamese markets. This information supports market sentiment analysis and identification of institutional investment trends.

While this functionality requires ongoing development based on available vnstock APIs, the framework supports comprehensive foreign investment tracking once data sources are fully integrated.

## Advanced Query Techniques

The natural language interface supports complex multi-part queries that combine different data types and analysis requirements. You can request comparative analysis between companies, trend analysis across time periods, and sector-wide performance reviews.

Example advanced queries include comparing financial performance between multiple companies, analyzing sector trends during specific market periods, and identifying companies with particular financial characteristics or performance metrics.

## Data Export and Integration

All data returned by the vnstock MCP server uses standard JSON formatting that integrates seamlessly with external analysis tools and workflows. The structured data format enables easy export to spreadsheets, databases, or analytical software.

The pandas DataFrame compatibility ensures that data can be immediately utilized in Python-based analysis workflows, supporting advanced statistical analysis, machine learning applications, and custom visualization development.

## Best Practices

For optimal performance and accuracy, structure queries with specific requirements and timeframes. Clear, detailed requests enable the system to select appropriate tools and return the most relevant information for your analysis needs.

Consider the market data limitations and update frequencies when designing analysis workflows. Vietnamese market data may experience varying latency during high-traffic periods, and historical data requests for extended periods may require additional processing time.

## Error Handling and Troubleshooting

The system provides comprehensive error messages when data is unavailable or when query parameters are invalid. Common issues include requesting data for non-existent stock symbols, specifying invalid date ranges, or requesting data during market closure periods.

If queries return unexpected results or error messages, verify stock symbols are correct and formatted properly, ensure date ranges fall within available data periods, and confirm that requested companies are listed on Vietnamese exchanges.

## Support and Further Development

The vnstock MCP server continues to evolve with enhanced functionality and improved data access capabilities. Community contributions and feedback help identify areas for improvement and new feature development.

For advanced use cases or custom functionality requirements, the open-source nature of the project enables modifications and extensions to meet specific analytical needs and integration requirements.
