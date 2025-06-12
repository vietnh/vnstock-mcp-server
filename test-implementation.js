#!/usr/bin/env node

/**
 * Test script for vnstock MCP server implementation
 * Validates package structure, dependencies, and basic functionality
 */

const fs = require('fs');
const path = require('path');
const { spawn, exec } = require('child_process');

class ImplementationTester {
    constructor() {
        this.packageDir = path.join(__dirname);
        this.testResults = [];
        this.totalTests = 0;
        this.passedTests = 0;
    }

    /**
     * Run all implementation tests
     */
    async runAllTests() {
        console.log('🧪 Running implementation tests for vnstock MCP server...\n');

        const tests = [
            { name: 'Package Structure Validation', test: () => this.testPackageStructure() },
            { name: 'Package.json Validation', test: () => this.testPackageJson() },
            { name: 'Node.js Syntax Validation', test: () => this.testNodeSyntax() },
            { name: 'Python Syntax Validation', test: () => this.testPythonSyntax() },
            { name: 'Dependencies Installation Test', test: () => this.testDependenciesInstall() },
            { name: 'Basic Execution Test', test: () => this.testBasicExecution() }
        ];

        for (const test of tests) {
            await this.runTest(test.name, test.test);
        }

        this.displayResults();
        return this.passedTests === this.totalTests;
    }

    /**
     * Execute individual test with error handling
     */
    async runTest(testName, testFunction) {
        this.totalTests++;
        try {
            await testFunction();
            this.testResults.push({ name: testName, status: 'PASS', message: 'Test completed successfully' });
            this.passedTests++;
            console.log(`✅ ${testName}: PASSED`);
        } catch (error) {
            this.testResults.push({ name: testName, status: 'FAIL', message: error.message });
            console.log(`❌ ${testName}: FAILED - ${error.message}`);
        }
    }

    /**
     * Test package structure and file existence
     */
    async testPackageStructure() {
        const requiredFiles = [
            'package.json',
            'bin/vnstock-mcp-server.js',
            'src/index.js',
            'src/install-deps.js',
            'src/test-connection.js',
            'python/vnstock_mcp_server.py',
            'README.md',
            'LICENSE'
        ];

        const requiredDirs = [
            'bin',
            'src',
            'python',
            'config',
            'docs'
        ];

        // Check required files
        for (const file of requiredFiles) {
            const filePath = path.join(this.packageDir, file);
            if (!fs.existsSync(filePath)) {
                throw new Error(`Required file missing: ${file}`);
            }
        }

        // Check required directories
        for (const dir of requiredDirs) {
            const dirPath = path.join(this.packageDir, dir);
            if (!fs.existsSync(dirPath) || !fs.statSync(dirPath).isDirectory()) {
                throw new Error(`Required directory missing: ${dir}`);
            }
        }
    }

    /**
     * Test package.json validity and content
     */
    async testPackageJson() {
        const packageJsonPath = path.join(this.packageDir, 'package.json');
        
        try {
            const packageContent = fs.readFileSync(packageJsonPath, 'utf8');
            const packageJson = JSON.parse(packageContent);

            // Validate required fields
            const requiredFields = ['name', 'version', 'description', 'main', 'bin', 'dependencies'];
            for (const field of requiredFields) {
                if (!packageJson[field]) {
                    throw new Error(`Missing required field in package.json: ${field}`);
                }
            }

            // Validate bin configuration
            if (!packageJson.bin['vnstock-mcp-server']) {
                throw new Error('Missing bin configuration for vnstock-mcp-server');
            }

            // Check if bin file exists
            const binFile = packageJson.bin['vnstock-mcp-server'];
            const binPath = path.join(this.packageDir, binFile);
            if (!fs.existsSync(binPath)) {
                throw new Error(`Bin file does not exist: ${binFile}`);
            }

            // Validate dependencies
            const dependencies = packageJson.dependencies || {};
            const requiredDeps = ['which', 'chalk'];
            for (const dep of requiredDeps) {
                if (!dependencies[dep]) {
                    throw new Error(`Missing required dependency: ${dep}`);
                }
            }

        } catch (error) {
            if (error instanceof SyntaxError) {
                throw new Error('Invalid JSON in package.json');
            }
            throw error;
        }
    }

    /**
     * Test Node.js files for syntax errors
     */
    async testNodeSyntax() {
        const nodeFiles = [
            'bin/vnstock-mcp-server.js',
            'src/index.js',
            'src/install-deps.js',
            'src/test-connection.js'
        ];

        for (const file of nodeFiles) {
            const filePath = path.join(this.packageDir, file);
            
            try {
                // Use Node.js to check syntax
                await new Promise((resolve, reject) => {
                    exec(`node -c "${filePath}"`, (error, stdout, stderr) => {
                        if (error) {
                            reject(new Error(`Syntax error in ${file}: ${error.message}`));
                        } else {
                            resolve();
                        }
                    });
                });
            } catch (error) {
                throw error;
            }
        }
    }

    /**
     * Test Python file for syntax errors
     */
    async testPythonSyntax() {
        const pythonFile = path.join(this.packageDir, 'python', 'vnstock_mcp_server.py');
        
        return new Promise((resolve, reject) => {
            exec(`python -m py_compile "${pythonFile}"`, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(`Python syntax error: ${error.message}`));
                } else {
                    resolve();
                }
            });
        });
    }

    /**
     * Test NPM dependencies installation
     */
    async testDependenciesInstall() {
        return new Promise((resolve, reject) => {
            console.log('   Installing NPM dependencies...');
            exec('npm install', { cwd: this.packageDir }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(`NPM install failed: ${error.message}`));
                } else {
                    resolve();
                }
            });
        });
    }

    /**
     * Test basic execution with help flag
     */
    async testBasicExecution() {
        const binFile = path.join(this.packageDir, 'bin', 'vnstock-mcp-server.js');
        
        return new Promise((resolve, reject) => {
            const child = spawn('node', [binFile, '--help'], {
                stdio: ['pipe', 'pipe', 'pipe'],
                cwd: this.packageDir
            });

            let output = '';
            let errorOutput = '';

            child.stdout.on('data', (data) => {
                output += data.toString();
            });

            child.stderr.on('data', (data) => {
                errorOutput += data.toString();
            });

            child.on('close', (code) => {
                if (code === 0 && (output.includes('Vnstock MCP Server') || errorOutput.includes('Starting vnstock MCP server'))) {
                    resolve();
                } else {
                    reject(new Error(`Basic execution failed with code ${code}. Output: ${output}, Error: ${errorOutput}`));
                }
            });

            child.on('error', (error) => {
                reject(new Error(`Execution error: ${error.message}`));
            });

            // Set a timeout for the test
            setTimeout(() => {
                child.kill();
                reject(new Error('Basic execution test timed out'));
            }, 10000);
        });
    }

    /**
     * Display comprehensive test results
     */
    displayResults() {
        console.log('\n📊 Implementation Test Results:\n');

        this.testResults.forEach((result) => {
            const statusColor = result.status === 'PASS' ? '\x1b[32m' : '\x1b[31m';
            const statusIcon = result.status === 'PASS' ? '✅' : '❌';
            const reset = '\x1b[0m';
            
            console.log(`${statusColor}${statusIcon} ${result.name}: ${result.status}${reset}`);
            if (result.status === 'FAIL') {
                console.log(`   └─ ${result.message}`);
            }
        });

        console.log(`\n📈 Overall Result: ${this.passedTests}/${this.totalTests} tests passed`);

        if (this.passedTests === this.totalTests) {
            console.log('\n🎉 All tests passed! Implementation is ready for deployment.');
            this.displayDeploymentInstructions();
        } else {
            console.log('\n🔧 Some tests failed. Please fix the issues before deployment.');
            this.displayFixingGuidance();
        }
    }

    /**
     * Display deployment instructions for successful tests
     */
    displayDeploymentInstructions() {
        console.log(`
🚀 Deployment Instructions:

1. Commit and push to GitHub:
   git add .
   git commit -m "Fix Node.js wrapper implementation issues"
   git push origin main

2. Test NPX execution:
   npx vnstock-mcp-server --test

3. Configure Claude Desktop:
   {
     "mcpServers": {
       "vnstock": {
         "command": "npx",
         "args": ["vnstock-mcp-server"]
       }
     }
   }

4. Optional: Publish to NPM:
   npm login
   npm publish

Implementation is ready for production use!
        `);
    }

    /**
     * Display guidance for fixing issues
     */
    displayFixingGuidance() {
        console.log(`
🔧 Fixing Guidance:

Common Issues and Solutions:

• Package Structure Issues:
  Ensure all required files and directories exist
  Check file permissions on executable files

• Syntax Errors:
  Review JavaScript and Python files for syntax errors
  Use proper async/await patterns in Node.js code

• Dependency Issues:
  Verify package.json dependencies are correct
  Remove unnecessary or invalid dependencies

• Execution Issues:
  Test individual components separately
  Check Node.js and Python executable paths

Run the test again after making fixes.
        `);
    }
}

/**
 * Main execution for testing
 */
async function main() {
    const tester = new ImplementationTester();
    const success = await tester.runAllTests();
    process.exit(success ? 0 : 1);
}

// Execute if this file is run directly
if (require.main === module) {
    main().catch((error) => {
        console.error('❌ Test execution failed:', error.message);
        process.exit(1);
    });
}

module.exports = ImplementationTester;
