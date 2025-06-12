#!/usr/bin/env node

/**
 * NPX executable for vnstock-mcp-server
 * Enables remote execution via: npx vnstock-mcp-server
 */

const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

// Get the package directory
const packageDir = path.join(__dirname, '..');
const srcPath = path.join(packageDir, 'src', 'index.js');

// Check if we're running from a global install or NPX
const isGlobalInstall = __dirname.includes('node_modules');

if (isGlobalInstall) {
    console.log('🚀 Starting vnstock MCP server...');
} else {
    console.log('📦 Running vnstock MCP server via NPX...');
}

// Execute the main Node.js entry point
const child = spawn('node', [srcPath], {
    stdio: 'inherit',
    cwd: packageDir
});

child.on('error', (error) => {
    console.error('❌ Failed to start vnstock MCP server:', error.message);
    process.exit(1);
});

child.on('close', (code) => {
    if (code !== 0) {
        console.error(`❌ vnstock MCP server exited with code ${code}`);
        process.exit(code);
    }
});

// Handle termination signals
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down vnstock MCP server...');
    child.kill('SIGINT');
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Terminating vnstock MCP server...');
    child.kill('SIGTERM');
});
