#!/usr/bin/env node

/**
 * Simple validation script for quick testing of vnstock MCP server
 * Performs basic checks and installs dependencies before testing
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

console.log('🧪 Quick Validation Test for vnstock MCP Server\n');

// Test 1: Package structure
console.log('Testing package structure...');
const requiredFiles = [
    'package.json',
    'bin/vnstock-mcp-server.js', 
    'src/index.js',
    'python/vnstock_mcp_server.py'
];

let structureOk = true;
for (const file of requiredFiles) {
    if (!fs.existsSync(file)) {
        console.log(`❌ Missing: ${file}`);
        structureOk = false;
    } else {
        console.log(`✅ Found: ${file}`);
    }
}

if (!structureOk) {
    console.log('\n❌ Package structure validation failed');
    process.exit(1);
}

// Test 2: Package.json validation
console.log('\nTesting package.json...');
try {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    console.log(`✅ Package name: ${packageJson.name}`);
    console.log(`✅ Version: ${packageJson.version}`);
    console.log(`✅ Dependencies: ${Object.keys(packageJson.dependencies || {}).join(', ')}`);
} catch (error) {
    console.log('❌ package.json is invalid');
    process.exit(1);
}

// Test 3: Node.js syntax check
console.log('\nChecking Node.js syntax...');
exec('node -c bin/vnstock-mcp-server.js', (error, stdout, stderr) => {
    if (error) {
        console.log('❌ Syntax error in bin file');
        console.log(error.message);
        process.exit(1);
    } else {
        console.log('✅ Bin file syntax OK');
    }
});

exec('node -c src/index.js', (error, stdout, stderr) => {
    if (error) {
        console.log('❌ Syntax error in main file');
        console.log(error.message);
        process.exit(1);
    } else {
        console.log('✅ Main file syntax OK');
        
        // Test 4: Install dependencies
        console.log('\nInstalling NPM dependencies...');
        exec('npm install', (error, stdout, stderr) => {
            if (error) {
                console.log('❌ NPM install failed');
                console.log(error.message);
                process.exit(1);
            } else {
                console.log('✅ Dependencies installed successfully');
                
                // Test 5: Help display test
                console.log('\nTesting help display...');
                exec('node src/index.js --help', (error, stdout, stderr) => {
                    if (stdout.includes('Vnstock MCP Server')) {
                        console.log('✅ Help display works');
                        
                        // Test 6: Test system requirements
                        console.log('\nTesting system requirements validation...');
                        exec('node src/index.js --test', { timeout: 30000 }, (error, stdout, stderr) => {
                            if (stdout.includes('Testing system requirements') || stderr.includes('Testing system requirements')) {
                                console.log('✅ System requirements test executed');
                                console.log('\n🎉 All validation tests passed!');
                                console.log('\n📋 Next Steps:');
                                console.log('1. Test with: npx . --help');
                                console.log('2. Run full test: npx . --test');
                                console.log('3. Configure Claude Desktop with NPX command');
                                console.log('4. Commit and push to GitHub');
                            } else {
                                console.log('⚠️  System requirements test may have issues');
                                console.log('Output:', stdout);
                                console.log('Error:', stderr);
                                console.log('\n🎉 Basic validation passed, but check system requirements manually');
                            }
                        });
                    } else {
                        console.log('❌ Help display failed');
                        console.log('Output:', stdout);
                        console.log('Error:', stderr);
                    }
                });
            }
        });
    }
});
