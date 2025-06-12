/**
 * Connection testing utility for vnstock MCP server
 * Validates system requirements and network connectivity
 */

const { exec } = require('child_process');
const which = require('which');
const chalk = require('chalk');
const path = require('path');

class ConnectionTester {
    constructor() {
        this.pythonPath = null;
        this.testResults = [];
        this.packageDir = path.join(__dirname, '..');
    }

    /**
     * Execute comprehensive system testing
     */
    async runTests() {
        console.log(chalk.blue('🧪 vnstock MCP Server - System Requirements Test\n'));

        const tests = [
            { name: 'Python Installation', test: () => this.testPythonInstallation() },
            { name: 'Python Version Compatibility', test: () => this.testPythonVersion() },
            { name: 'Required Package Availability', test: () => this.testPackageAvailability() },
            { name: 'Network Connectivity', test: () => this.testNetworkConnectivity() },
            { name: 'Market Data Access', test: () => this.testMarketDataAccess() },
            { name: 'MCP Server File Integrity', test: () => this.testServerFiles() }
        ];

        console.log(chalk.blue('Running system diagnostics...\n'));

        for (const test of tests) {
            await this.executeTest(test.name, test.test);
        }

        this.displayResults();
        return this.allTestsPassed();
    }

    /**
     * Execute individual test with error handling
     */
    async executeTest(testName, testFunction) {
        try {
            await testFunction();
            this.testResults.push({ name: testName, status: 'PASS', message: 'Test completed successfully' });
            console.log(chalk.green(`✅ ${testName}: PASSED`));
        } catch (error) {
            this.testResults.push({ name: testName, status: 'FAIL', message: error.message });
            console.log(chalk.red(`❌ ${testName}: FAILED - ${error.message}`));
        }
    }

    /**
     * Test Python installation and locate executable
     */
    async testPythonInstallation() {
        const pythonCommands = ['python3', 'python'];
        
        for (const command of pythonCommands) {
            try {
                this.pythonPath = await which(command);
                return; // Success
            } catch (error) {
                continue;
            }
        }
        
        throw new Error('Python executable not found in system PATH');
    }

    /**
     * Test Python version compatibility
     */
    async testPythonVersion() {
        if (!this.pythonPath) {
            throw new Error('Python path not available for version check');
        }

        return new Promise((resolve, reject) => {
            exec(`${this.pythonPath} --version`, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error('Could not determine Python version'));
                    return;
                }
                
                const output = stdout || stderr;
                const versionMatch = output.match(/Python (\d+\.\d+\.\d+)/);
                
                if (!versionMatch) {
                    reject(new Error('Invalid Python version format'));
                    return;
                }
                
                const version = versionMatch[1];
                const [major, minor] = version.split('.').map(Number);
                
                if (major !== 3 || minor < 8) {
                    reject(new Error(`Python ${version} found, but version 3.8+ required`));
                } else {
                    resolve();
                }
            });
        });
    }

    /**
     * Test required Python package availability
     */
    async testPackageAvailability() {
        const requiredPackages = ['vnstock', 'mcp', 'pandas'];
        const missingPackages = [];

        for (const packageName of requiredPackages) {
            try {
                await this.checkPackageImport(packageName);
            } catch (error) {
                missingPackages.push(packageName);
            }
        }

        if (missingPackages.length > 0) {
            throw new Error(`Missing required packages: ${missingPackages.join(', ')}`);
        }
    }

    /**
     * Check if Python package can be imported
     */
    checkPackageImport(packageName) {
        return new Promise((resolve, reject) => {
            exec(`${this.pythonPath} -c "import ${packageName}"`, (error) => {
                if (error) {
                    reject(error);
                } else {
                    resolve();
                }
            });
        });
    }

    /**
     * Test basic network connectivity
     */
    async testNetworkConnectivity() {
        return new Promise((resolve, reject) => {
            exec('ping -c 1 8.8.8.8 2>/dev/null || ping -n 1 8.8.8.8', (error) => {
                if (error) {
                    reject(new Error('Network connectivity test failed'));
                } else {
                    resolve();
                }
            });
        });
    }

    /**
     * Test Vietnamese market data access through vnstock
     */
    async testMarketDataAccess() {
        const testScript = `
try:
    import vnstock as vn
    # Quick test of vnstock functionality
    companies = vn.listing_companies()
    if len(companies) > 0:
        print("Market data access successful")
    else:
        raise Exception("No company data retrieved")
except Exception as e:
    raise Exception(f"Market data access failed: {str(e)}")
        `;

        return new Promise((resolve, reject) => {
            exec(`${this.pythonPath} -c "${testScript}"`, (error, stdout, stderr) => {
                if (error || stderr.includes('Exception')) {
                    reject(new Error('Unable to access Vietnamese market data'));
                } else {
                    resolve();
                }
            });
        });
    }

    /**
     * Test MCP server file integrity
     */
    async testServerFiles() {
        const fs = require('fs');
        const serverFile = path.join(this.packageDir, 'python', 'vnstock_mcp_server.py');
        
        if (!fs.existsSync(serverFile)) {
            throw new Error('MCP server Python file not found');
        }

        const content = fs.readFileSync(serverFile, 'utf8');
        
        // Basic integrity checks
        if (!content.includes('VnstockMCPServer')) {
            throw new Error('MCP server file appears corrupted');
        }

        if (!content.includes('def main()')) {
            throw new Error('MCP server entry point not found');
        }
    }

    /**
     * Display comprehensive test results
     */
    displayResults() {
        console.log(chalk.blue('\n📊 Test Results Summary:\n'));

        this.testResults.forEach((result, index) => {
            const statusColor = result.status === 'PASS' ? 'green' : 'red';
            const statusIcon = result.status === 'PASS' ? '✅' : '❌';
            
            console.log(chalk[statusColor](`${statusIcon} ${result.name}: ${result.status}`));
            if (result.status === 'FAIL') {
                console.log(chalk.gray(`   └─ ${result.message}`));
            }
        });

        const passCount = this.testResults.filter(r => r.status === 'PASS').length;
        const totalCount = this.testResults.length;

        console.log(chalk.blue(`\n📈 Overall Result: ${passCount}/${totalCount} tests passed`));

        if (this.allTestsPassed()) {
            console.log(chalk.green('\n🎉 System is ready for vnstock MCP server operation!'));
            this.displayNextSteps();
        } else {
            console.log(chalk.red('\n🔧 System requires attention before vnstock MCP server can operate.'));
            this.displayTroubleshootingGuidance();
        }
    }

    /**
     * Check if all tests passed
     */
    allTestsPassed() {
        return this.testResults.every(result => result.status === 'PASS');
    }

    /**
     * Display next steps for successful setup
     */
    displayNextSteps() {
        console.log(chalk.blue(`
🚀 Next Steps:

1. Configure Claude Desktop:
   Add vnstock MCP server to your Claude Desktop configuration:
   
   {
     "mcpServers": {
       "vnstock": {
         "command": "npx",
         "args": ["vnstock-mcp-server"]
       }
     }
   }

2. Restart Claude Desktop to activate the MCP server

3. Start analyzing Vietnamese stock market data:
   • Ask about current stock prices: "What is VIC's current price?"
   • Request historical data: "Show me VCB's price history"
   • Research companies: "Give me information about Techcombank"

For detailed documentation, visit:
https://github.com/vietnh/vnstock-mcp-server
        `));
    }

    /**
     * Display troubleshooting guidance for failed tests
     */
    displayTroubleshootingGuidance() {
        console.log(chalk.yellow(`
🔧 Troubleshooting Guidance:

Common Issues and Solutions:

• Python Installation Issues:
  Install Python 3.8+ from python.org and ensure it's in your PATH

• Missing Package Dependencies:
  Run: npx vnstock-mcp-server --install-deps
  Or manually: pip install vnstock mcp pandas

• Network Connectivity Problems:
  Check internet connection and firewall settings
  Ensure access to Vietnamese market data sources

• File Integrity Issues:
  Reinstall the package: npm uninstall -g vnstock-mcp-server
  Then: npx vnstock-mcp-server (fresh installation)

For additional support, create an issue at:
https://github.com/vietnh/vnstock-mcp-server/issues
        `));
    }
}

/**
 * Main execution for standalone testing
 */
async function main() {
    const tester = new ConnectionTester();
    const success = await tester.runTests();
    process.exit(success ? 0 : 1);
}

// Execute if this file is run directly
if (require.main === module) {
    main().catch((error) => {
        console.error(chalk.red('❌ Test execution failed:'), error.message);
        process.exit(1);
    });
}

module.exports = ConnectionTester;
