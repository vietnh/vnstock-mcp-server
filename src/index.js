 /**
 * Main Node.js wrapper for vnstock MCP server
 * Manages Python environment and process execution
 */

const { spawn, exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const which = require('which');
const chalk = require('chalk');

class VnstockMCPWrapper {
    constructor() {
        this.pythonPath = null;
        this.serverProcess = null;
        this.packageDir = path.join(__dirname, '..');
        this.pythonServerPath = path.join(this.packageDir, 'python', 'vnstock_mcp_server.py');
    }

    /**
     * Initialize the wrapper and verify system requirements
     */
    async initialize() {
        console.error(chalk.blue('Initializing vnstock MCP server...'));
        
        try {
            await this.checkPythonInstallation();
            await this.verifyPythonDependencies();
            console.error(chalk.green('System requirements verified'));
            return true;
        } catch (error) {
            console.error(chalk.red('Initialization failed:'), error.message);
            return false;
        }
    }

    /**
     * Check for Python installation and locate executable
     */
    async checkPythonInstallation() {
        const pythonCommands = ['python3', 'python'];
        
        for (const command of pythonCommands) {
            try {
                this.pythonPath = await which(command);
                console.error(chalk.green(`Found Python: ${this.pythonPath}`));
                
                // Verify Python version
                const version = await this.getPythonVersion();
                if (this.isValidPythonVersion(version)) {
                    console.error(chalk.green(`Python version ${version} is compatible`));
                    return;
                } else {
                    console.error(chalk.yellow(`Python ${version} found, but version 3.8+ recommended`));
                }
            } catch (error) {
                // Continue to next command
            }
        }
        
        throw new Error('Python 3.8+ is required but not found. Please install Python and ensure it is in your PATH.');
    }

    /**
     * Get Python version information
     */
    getPythonVersion() {
        return new Promise((resolve, reject) => {
            exec(`${this.pythonPath} --version`, (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                    return;
                }
                
                const output = stdout || stderr;
                const versionMatch = output.match(/Python (\d+\.\d+\.\d+)/);
                if (versionMatch) {
                    resolve(versionMatch[1]);
                } else {
                    reject(new Error('Could not determine Python version'));
                }
            });
        });
    }

    /**
     * Verify Python version compatibility
     */
    isValidPythonVersion(version) {
        const [major, minor] = version.split('.').map(Number);
        return major === 3 && minor >= 8;
    }

    /**
     * Verify required Python dependencies are installed
     */
    async verifyPythonDependencies() {
        const requiredPackages = ['vnstock', 'mcp', 'pandas'];
        console.error(chalk.blue('Checking Python dependencies...'));

        for (const packageName of requiredPackages) {
            try {
                await this.checkPythonPackage(packageName);
                console.error(chalk.green(`${packageName} is installed`));
            } catch (error) {
                console.error(chalk.yellow(`${packageName} not found, attempting installation...`));
                await this.installPythonPackage(packageName);
            }
        }
    }

    /**
     * Check if a Python package is installed
     */
    checkPythonPackage(packageName) {
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
     * Install a Python package using pip
     */
    installPythonPackage(packageName) {
        return new Promise((resolve, reject) => {
            console.error(chalk.blue(`Installing ${packageName}...`));
            
            let installCommand = `${this.pythonPath} -m pip install ${packageName}`;
            if (packageName === 'vnstock') {
                // Install latest vnstock with upgrade flag
                installCommand = `${this.pythonPath} -m pip install -U vnstock>=3.2.0`;
            }
            
            exec(installCommand, (error, stdout, stderr) => {
                if (error) {
                    console.error(chalk.red(`Failed to install ${packageName}:`), stderr);
                    reject(error);
                } else {
                    console.error(chalk.green(`Successfully installed ${packageName}`));
                    resolve();
                }
            });
        });
    }

    /**
     * Start the Python MCP server process
     */
    async startServer() {
        if (!fs.existsSync(this.pythonServerPath)) {
            throw new Error(`Python server file not found: ${this.pythonServerPath}`);
        }

        console.error(chalk.blue('Starting vnstock MCP server...'));

        // Validate Python executable before starting
        if (!this.pythonPath) {
            throw new Error('Python executable path not set');
        }

        this.serverProcess = spawn(this.pythonPath, [this.pythonServerPath], {
            stdio: ['pipe', 'pipe', 'pipe'],
            cwd: this.packageDir,
            env: { ...process.env, PYTHONPATH: this.packageDir }
        });

        // Handle server output
        this.serverProcess.stdout.on('data', (data) => {
            process.stdout.write(data);
        });

        this.serverProcess.stderr.on('data', (data) => {
            process.stderr.write(data);
        });

        // Handle server process events
        this.serverProcess.on('error', (error) => {
            console.error(chalk.red('Server process error:'), error.message);
            process.exit(1);
        });

        this.serverProcess.on('close', (code) => {
            if (code !== 0) {
                console.error(chalk.red(`Server process exited with code ${code}`));
                process.exit(code);
            }
        });

        // Setup signal handlers for graceful shutdown
        this.setupSignalHandlers();

        console.error(chalk.green('vnstock MCP server is running'));
        
        // Keep the process alive
        process.stdin.resume();
    }

    /**
     * Setup signal handlers for graceful shutdown
     */
    setupSignalHandlers() {
        const shutdown = (signal) => {
            console.error(chalk.yellow(`\nReceived ${signal}, shutting down gracefully...`));
            
            if (this.serverProcess) {
                this.serverProcess.kill(signal);
                setTimeout(() => {
                    if (!this.serverProcess.killed) {
                        console.error(chalk.red('Force killing server process...'));
                        this.serverProcess.kill('SIGKILL');
                    }
                }, 5000);
            }
            
            process.exit(0);
        };

        process.on('SIGINT', () => shutdown('SIGINT'));
        process.on('SIGTERM', () => shutdown('SIGTERM'));
    }

    /**
     * Display help information
     */
    displayHelp() {
        console.error(chalk.blue(`Vnstock MCP Server - Vietnamese Stock Market Data

Usage:
  npx vnstock-mcp-server              Start the MCP server
  npx vnstock-mcp-server --help       Show this help message
  npx vnstock-mcp-server --test       Test system requirements
  npx vnstock-mcp-server --install-deps Install Python dependencies
  npx vnstock-mcp-server --version    Show version information

Configuration:
  Add to Claude Desktop config file:
  {
    "mcpServers": {
      "vnstock": {
        "command": "npx",
        "args": ["vnstock-mcp-server"]
      }
    }
  }

For more information, visit:
https://github.com/vietnh/vnstock-mcp-server
        `));
    }

    /**
     * Test system requirements and connection
     */
    async testConnection() {
        console.error(chalk.blue('Testing system requirements...'));
        
        try {
            const success = await this.initialize();
            if (success) {
                console.error(chalk.green('All tests passed! System is ready for vnstock MCP server.'));
            } else {
                console.error(chalk.red('System requirements test failed.'));
                process.exit(1);
            }
        } catch (error) {
            console.error(chalk.red('Test failed:'), error.message);
            process.exit(1);
        }
    }
}

/**
 * Main execution logic
 */
async function main() {
    const args = process.argv.slice(2);
    const wrapper = new VnstockMCPWrapper();

    // Handle command line arguments
    if (args.includes('--help') || args.includes('-h')) {
        wrapper.displayHelp();
        return;
    }

    if (args.includes('--test')) {
        await wrapper.testConnection();
        return;
    }

    if (args.includes('--install-deps')) {
        const DependencyInstaller = require('./install-deps');
        const installer = new DependencyInstaller();
        const success = await installer.install();
        process.exit(success ? 0 : 1);
    }

    if (args.includes('--version')) {
        console.error(chalk.blue('vnstock-mcp-server version 1.0.0'));
        return;
    }

    // Initialize and start the server
    try {
        const success = await wrapper.initialize();
        if (success) {
            await wrapper.startServer();
        } else {
            process.exit(1);
        }
    } catch (error) {
        console.error(chalk.red('Failed to start server:'), error.message);
        process.exit(1);
    }
}

// Execute if this file is run directly
if (require.main === module) {
    main().catch((error) => {
        console.error(chalk.red('Unexpected error:'), error.message);
        process.exit(1);
    });
}

module.exports = VnstockMCPWrapper;
