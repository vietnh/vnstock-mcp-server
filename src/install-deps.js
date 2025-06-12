/**
 * Python dependency installer for vnstock MCP server
 * Handles automatic installation of required Python packages
 */

const { exec } = require('child_process');
const which = require('which');
const chalk = require('chalk');

class DependencyInstaller {
    constructor() {
        this.pythonPath = null;
        this.requiredPackages = [
            { name: 'vnstock', version: '>=3.2.0' },
            { name: 'mcp', version: '>=0.1.0' },
            { name: 'pandas', version: '>=1.5.0' },
            { name: 'asyncio-compat', version: '>=0.2.0' }
        ];
    }

    /**
     * Main installation process
     */
    async install() {
        console.log(chalk.blue('🔧 Installing Python dependencies for vnstock MCP server...'));

        try {
            await this.locatePython();
            await this.upgradePackageManager();
            await this.installRequiredPackages();
            await this.verifyInstallation();
            
            console.log(chalk.green('✅ All dependencies installed successfully!'));
            return true;
        } catch (error) {
            console.error(chalk.red('❌ Dependency installation failed:'), error.message);
            return false;
        }
    }

    /**
     * Locate Python executable
     */
    async locatePython() {
        const pythonCommands = ['python3', 'python'];
        
        for (const command of pythonCommands) {
            try {
                this.pythonPath = await which(command);
                console.log(chalk.green(`✅ Found Python: ${this.pythonPath}`));
                return;
            } catch (error) {
                continue;
            }
        }
        
        throw new Error('Python installation not found. Please install Python 3.8+ and ensure it is in your PATH.');
    }

    /**
     * Upgrade pip package manager
     */
    async upgradePackageManager() {
        console.log(chalk.blue('📦 Upgrading package manager...'));
        
        return new Promise((resolve, reject) => {
            exec(`${this.pythonPath} -m pip install --upgrade pip`, (error, stdout, stderr) => {
                if (error) {
                    console.log(chalk.yellow('⚠️  Package manager upgrade failed, continuing...'));
                    resolve(); // Continue even if upgrade fails
                } else {
                    console.log(chalk.green('✅ Package manager upgraded'));
                    resolve();
                }
            });
        });
    }

    /**
     * Install required Python packages
     */
    async installRequiredPackages() {
        console.log(chalk.blue('📚 Installing required packages...'));

        for (const pkg of this.requiredPackages) {
            await this.installPackage(pkg);
        }
    }

    /**
     * Install individual Python package
     */
    async installPackage(packageInfo) {
        const packageSpec = packageInfo.version ? 
            `${packageInfo.name}${packageInfo.version}` : 
            packageInfo.name;

        console.log(chalk.blue(`📦 Installing ${packageSpec}...`));

        return new Promise((resolve, reject) => {
            const command = `${this.pythonPath} -m pip install "${packageSpec}"`;
            
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    console.error(chalk.red(`❌ Failed to install ${packageInfo.name}:`), stderr);
                    reject(error);
                } else {
                    console.log(chalk.green(`✅ Installed ${packageInfo.name}`));
                    resolve();
                }
            });
        });
    }

    /**
     * Verify installation by importing packages
     */
    async verifyInstallation() {
        console.log(chalk.blue('🔍 Verifying installation...'));

        for (const pkg of this.requiredPackages) {
            await this.verifyPackage(pkg.name);
        }
    }

    /**
     * Verify individual package installation
     */
    async verifyPackage(packageName) {
        return new Promise((resolve, reject) => {
            // Special handling for package names that differ from import names
            const importName = packageName === 'asyncio-compat' ? 'asyncio' : packageName;
            
            exec(`${this.pythonPath} -c "import ${importName}; print('${packageName} OK')"`, (error, stdout, stderr) => {
                if (error) {
                    console.error(chalk.red(`❌ Package verification failed for ${packageName}`));
                    reject(error);
                } else {
                    console.log(chalk.green(`✅ Verified ${packageName}`));
                    resolve();
                }
            });
        });
    }

    /**
     * Display installation summary
     */
    displaySummary() {
        console.log(chalk.blue(`
📋 Installation Summary:

Required Python packages for vnstock MCP server:
${this.requiredPackages.map(pkg => `  • ${pkg.name} ${pkg.version || ''}`).join('\n')}

System Requirements:
  • Python 3.8 or higher
  • Internet connection for market data access
  • Sufficient disk space for package dependencies

Next Steps:
  1. Test the installation: npx vnstock-mcp-server --test
  2. Configure Claude Desktop with the vnstock MCP server
  3. Start using Vietnamese stock market data analysis

For configuration instructions, visit:
https://github.com/vietnh/vnstock-mcp-server
        `));
    }
}

/**
 * Main execution for standalone usage
 */
async function main() {
    const installer = new DependencyInstaller();
    
    console.log(chalk.blue('🎯 vnstock MCP Server - Dependency Installation\n'));
    
    const success = await installer.install();
    
    if (success) {
        installer.displaySummary();
        process.exit(0);
    } else {
        console.log(chalk.red('\n❌ Installation failed. Please check the error messages above.'));
        process.exit(1);
    }
}

// Execute if this file is run directly
if (require.main === module) {
    main().catch((error) => {
        console.error(chalk.red('❌ Unexpected error:'), error.message);
        process.exit(1);
    });
}

module.exports = DependencyInstaller;
