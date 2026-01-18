#!/usr/bin/env node

/**
 * OpenAI API Key Setup Script
 *
 * Sets up OpenAI API key storage in:
 * - Windows: %USERPROFILE%\runtime_data\keys\openai\
 * - macOS/Linux: ~/runtime_data/keys/openai/
 *
 * Creates environment loading scripts for all platforms.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

// Configuration
const KEY_DIR_NAME = 'openai';
const KEY_FILE_NAME = 'openai_api_key.txt';

// Colors for console output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    magenta: '\x1b[35m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function logStep(step, message) {
    log(`\n[Step ${step}] ${message}`, 'cyan');
}

function logSuccess(message) {
    log(`✅ ${message}`, 'green');
}

function logWarning(message) {
    log(`⚠️  ${message}`, 'yellow');
}

function logError(message) {
    log(`❌ ${message}`, 'red');
}

/**
 * Detect the current operating system
 */
function detectOS() {
    const platform = os.platform();
    switch (platform) {
        case 'win32':
            return 'windows';
        case 'darwin':
            return 'macos';
        case 'linux':
            return 'linux';
        default:
            return 'unknown';
    }
}

/**
 * Get the home directory path
 */
function getHomeDir() {
    return os.homedir();
}

/**
 * Get the keys base path
 */
function getKeysBasePath() {
    const homeDir = getHomeDir();
    return path.join(homeDir, 'runtime_data', 'keys');
}

/**
 * Get the OpenAI keys directory path
 */
function getOpenAIKeyDir() {
    return path.join(getKeysBasePath(), KEY_DIR_NAME);
}

/**
 * Get the OpenAI key file path
 */
function getOpenAIKeyFilePath() {
    return path.join(getOpenAIKeyDir(), KEY_FILE_NAME);
}

/**
 * Create directory if it doesn't exist
 */
function ensureDirectory(dirPath) {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        logSuccess(`Created directory: ${dirPath}`);
    } else {
        log(`Directory already exists: ${dirPath}`, 'blue');
    }
}

/**
 * Check if API key file exists
 */
function keyFileExists() {
    return fs.existsSync(getOpenAIKeyFilePath());
}

/**
 * Read existing API key
 */
function readExistingKey() {
    const keyPath = getOpenAIKeyFilePath();
    if (fs.existsSync(keyPath)) {
        return fs.readFileSync(keyPath, 'utf-8').trim();
    }
    return null;
}

/**
 * Validate OpenAI API key format
 */
function validateKeyFormat(key) {
    // OpenAI keys typically start with 'sk-' and are 40+ characters
    if (!key || key.length < 20) {
        return { valid: false, message: 'Key is too short' };
    }
    if (!key.startsWith('sk-')) {
        return { valid: false, message: 'Key should start with "sk-"' };
    }
    return { valid: true };
}

/**
 * Mask API key for display
 */
function maskKey(key) {
    if (!key || key.length < 10) return '***';
    return key.substring(0, 7) + '...' + key.substring(key.length - 4);
}

/**
 * Save API key to file
 */
function saveApiKey(key, osType) {
    const keyPath = getOpenAIKeyFilePath();
    fs.writeFileSync(keyPath, key, 'utf-8');

    // Set restrictive permissions on Unix-like systems
    if (osType !== 'windows') {
        try {
            fs.chmodSync(keyPath, 0o600);
            log(`Set file permissions to 600 (owner read/write only)`, 'blue');
        } catch (e) {
            logWarning(`Could not set file permissions: ${e.message}`);
        }
    }

    logSuccess(`API key saved to: ${keyPath}`);
}

/**
 * Create shell environment script (Bash/Zsh)
 */
function createBashEnvScript(keyDir) {
    const scriptPath = path.join(keyDir, 'openai_env.sh');
    const keyFilePath = getOpenAIKeyFilePath();

    const content = `#!/bin/bash
# OpenAI API Key Environment Setup
# Source this file to set OPENAI_API_KEY in your shell
# Usage: source ${scriptPath}

OPENAI_KEY_FILE="${keyFilePath}"

if [ -f "$OPENAI_KEY_FILE" ]; then
    export OPENAI_API_KEY=$(cat "$OPENAI_KEY_FILE")
    echo "✅ OPENAI_API_KEY loaded successfully"
else
    echo "❌ OpenAI API key file not found at: $OPENAI_KEY_FILE"
    echo "   Run 'npm run setup:openai' to set up your key"
    return 1
fi
`;

    fs.writeFileSync(scriptPath, content, 'utf-8');
    fs.chmodSync(scriptPath, 0o755);
    logSuccess(`Created: ${scriptPath}`);
}

/**
 * Create Windows CMD batch script
 */
function createBatEnvScript(keyDir) {
    const scriptPath = path.join(keyDir, 'openai_env.bat');
    const keyFilePath = getOpenAIKeyFilePath();

    const content = `@echo off
REM OpenAI API Key Environment Setup
REM Run this file to set OPENAI_API_KEY in your CMD session
REM Usage: call ${scriptPath}

set "OPENAI_KEY_FILE=${keyFilePath}"

if exist "%OPENAI_KEY_FILE%" (
    set /p OPENAI_API_KEY=<"%OPENAI_KEY_FILE%"
    echo [32m✅ OPENAI_API_KEY loaded successfully[0m
) else (
    echo [31m❌ OpenAI API key file not found at: %OPENAI_KEY_FILE%[0m
    echo    Run 'npm run setup:openai' to set up your key
    exit /b 1
)
`;

    fs.writeFileSync(scriptPath, content, 'utf-8');
    logSuccess(`Created: ${scriptPath}`);
}

/**
 * Create Windows PowerShell script
 */
function createPowerShellEnvScript(keyDir) {
    const scriptPath = path.join(keyDir, 'openai_env.ps1');
    const keyFilePath = getOpenAIKeyFilePath();

    const content = `# OpenAI API Key Environment Setup
# Dot-source this file to set OPENAI_API_KEY in your PowerShell session
# Usage: . ${scriptPath}

$OpenAIKeyFile = "${keyFilePath}"

if (Test-Path $OpenAIKeyFile) {
    $env:OPENAI_API_KEY = (Get-Content $OpenAIKeyFile -Raw).Trim()
    Write-Host "✅ OPENAI_API_KEY loaded successfully" -ForegroundColor Green
} else {
    Write-Host "❌ OpenAI API key file not found at: $OpenAIKeyFile" -ForegroundColor Red
    Write-Host "   Run 'npm run setup:openai' to set up your key" -ForegroundColor Yellow
}
`;

    fs.writeFileSync(scriptPath, content, 'utf-8');
    logSuccess(`Created: ${scriptPath}`);
}

/**
 * Create project-local helper scripts in scripts/ folder
 */
function createProjectHelperScripts(projectPath, osType) {
    const keyDir = getOpenAIKeyDir();
    const scriptsDir = path.join(projectPath, 'scripts');

    // Ensure scripts directory exists
    ensureDirectory(scriptsDir);

    // Bash/Zsh helper
    const shContent = `#!/bin/bash
# Load OpenAI API Key
# Usage: source ./scripts/load-openai-key.sh

source "${path.join(keyDir, 'openai_env.sh')}"
`;
    const shPath = path.join(scriptsDir, 'load-openai-key.sh');
    fs.writeFileSync(shPath, shContent, 'utf-8');
    if (osType !== 'windows') {
        fs.chmodSync(shPath, 0o755);
    }
    logSuccess(`Created: ${shPath}`);

    // Windows CMD helper
    const batContent = `@echo off
REM Load OpenAI API Key
REM Usage: call scripts\\load-openai-key.bat

call "${path.join(keyDir, 'openai_env.bat')}"
`;
    const batPath = path.join(scriptsDir, 'load-openai-key.bat');
    fs.writeFileSync(batPath, batContent, 'utf-8');
    logSuccess(`Created: ${batPath}`);

    // PowerShell helper
    const ps1Content = `# Load OpenAI API Key
# Usage: . .\\scripts\\load-openai-key.ps1

. "${path.join(keyDir, 'openai_env.ps1')}"
`;
    const ps1Path = path.join(scriptsDir, 'load-openai-key.ps1');
    fs.writeFileSync(ps1Path, ps1Content, 'utf-8');
    logSuccess(`Created: ${ps1Path}`);
}

/**
 * Prompt user for input
 */
function prompt(question) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    return new Promise((resolve) => {
        rl.question(question, (answer) => {
            rl.close();
            resolve(answer);
        });
    });
}

/**
 * Main setup function
 */
async function main() {
    const args = process.argv.slice(2);
    const verifyOnly = args.includes('--verify');
    const loadOnly = args.includes('--load');
    const checkOnly = args.includes('--check');
    const updateKey = args.includes('--update');

    const osType = detectOS();
    const keyDir = getOpenAIKeyDir();
    const keyFilePath = getOpenAIKeyFilePath();
    const projectPath = process.cwd();

    // --check mode: Check if key exists, if not prompt user to run setup
    if (checkOnly) {
        log('\n🔍 Checking OpenAI API Key...', 'cyan');

        if (keyFileExists()) {
            const key = readExistingKey();
            const validation = validateKeyFormat(key);
            if (validation.valid) {
                logSuccess(`OpenAI API key is configured: ${maskKey(key)}`);
                log(`   Location: ${keyFilePath}`, 'blue');
                process.exit(0);
            } else {
                logError(`OpenAI API key exists but format is invalid: ${validation.message}`);
                log('\n📋 To fix this, run:', 'yellow');
                log('   npm run update:openai', 'blue');
                process.exit(1);
            }
        } else {
            logError('OpenAI API key is NOT configured!');
            log('\n' + '='.repeat(60), 'yellow');
            log('📋 To set up your OpenAI API key:', 'yellow');
            log('='.repeat(60), 'yellow');
            log('\n   1. Get your API key from: https://platform.openai.com/api-keys', 'blue');
            log('   2. Run the following command:', 'blue');
            log('\n      npm run setup:openai', 'green');
            log('\n   3. Paste your API key when prompted', 'blue');
            log('\n' + '='.repeat(60), 'yellow');
            process.exit(1);
        }
    }

    // --update mode: Force update the key
    if (updateKey) {
        log('\n🔄 Update OpenAI API Key', 'green');
        log('='.repeat(60), 'cyan');

        if (keyFileExists()) {
            const existingKey = readExistingKey();
            log(`\nCurrent key: ${maskKey(existingKey)}`, 'blue');
            log(`Location: ${keyFilePath}`, 'blue');
        }

        log('\n📋 To get a new OpenAI API key:', 'yellow');
        log('   1. Go to https://platform.openai.com/api-keys', 'blue');
        log('   2. Sign in to your account', 'blue');
        log('   3. Click "Create new secret key"', 'blue');
        log('   4. Copy the key (starts with "sk-")\n', 'blue');

        const newKey = await prompt('Enter your new OpenAI API key: ');
        const trimmedKey = newKey.trim();

        const validation = validateKeyFormat(trimmedKey);
        if (!validation.valid) {
            logError(`Invalid API key: ${validation.message}`);
            process.exit(1);
        }

        // Ensure directory exists
        ensureDirectory(keyDir);

        // Save the new key
        saveApiKey(trimmedKey, osType);

        // Recreate environment scripts
        createBashEnvScript(keyDir);
        createBatEnvScript(keyDir);
        createPowerShellEnvScript(keyDir);

        log('\n' + '='.repeat(60), 'cyan');
        logSuccess('OpenAI API key updated successfully!');
        log('='.repeat(60), 'cyan');
        log('\n📋 Remember to reload the key in your terminal:', 'yellow');
        if (osType === 'windows') {
            log('   call scripts\\load-openai-key.bat', 'blue');
        } else {
            log('   source ./scripts/load-openai-key.sh', 'blue');
        }
        process.exit(0);
    }

    log('\n🔑 OpenAI API Key Setup', 'green');
    log('='.repeat(60), 'cyan');

    // Step 1: Detect OS
    logStep(1, 'Detecting operating system...');
    logSuccess(`Detected OS: ${osType}`);


    log(`\n📁 Paths:`, 'blue');
    log(`   Home Directory: ${getHomeDir()}`);
    log(`   Key Directory: ${keyDir}`);
    log(`   Key File: ${keyFilePath}`);
    log(`   Project Path: ${projectPath}`);

    // If verify only
    if (verifyOnly) {
        logStep(2, 'Verifying API key...');
        if (keyFileExists()) {
            const key = readExistingKey();
            const validation = validateKeyFormat(key);
            if (validation.valid) {
                logSuccess(`API key found and format is valid: ${maskKey(key)}`);
                process.exit(0);
            } else {
                logError(`API key format invalid: ${validation.message}`);
                process.exit(1);
            }
        } else {
            logError(`API key file not found at: ${keyFilePath}`);
            process.exit(1);
        }
    }

    // If load only - just print the source command
    if (loadOnly) {
        if (keyFileExists()) {
            if (osType === 'windows') {
                log(`\nRun this command to load the key:`, 'yellow');
                log(`  call "${path.join(keyDir, 'openai_env.bat')}"`, 'blue');
            } else {
                log(`\nRun this command to load the key:`, 'yellow');
                log(`  source "${path.join(keyDir, 'openai_env.sh')}"`, 'blue');
            }
        } else {
            logError(`API key not set up yet. Run 'npm run setup:openai' first.`);
            process.exit(1);
        }
        return;
    }

    // Step 2: Create directory structure
    logStep(2, 'Creating directory structure...');
    ensureDirectory(keyDir);

    // Step 3: Check for existing key
    logStep(3, 'Checking for existing API key...');
    let apiKey = null;

    if (keyFileExists()) {
        const existingKey = readExistingKey();
        logWarning(`Existing API key found: ${maskKey(existingKey)}`);

        const answer = await prompt('\nDo you want to replace it? (y/N): ');
        if (answer.toLowerCase() !== 'y') {
            log('Keeping existing key.', 'blue');
            apiKey = existingKey;
        }
    }

    // Step 4: Get API key from user
    if (!apiKey) {
        logStep(4, 'Setting up API key...');

        log('\n📋 To get your OpenAI API key:', 'yellow');
        log('   1. Go to https://platform.openai.com/api-keys', 'blue');
        log('   2. Sign in to your account', 'blue');
        log('   3. Click "Create new secret key"', 'blue');
        log('   4. Copy the key (starts with "sk-")\n', 'blue');

        apiKey = await prompt('Enter your OpenAI API key: ');
        apiKey = apiKey.trim();

        // Validate
        const validation = validateKeyFormat(apiKey);
        if (!validation.valid) {
            logError(`Invalid API key: ${validation.message}`);
            log('Please try again with a valid OpenAI API key.', 'yellow');
            process.exit(1);
        }

        // Save the key
        saveApiKey(apiKey, osType);
    }

    // Step 5: Create environment scripts
    logStep(5, 'Creating environment scripts...');
    createBashEnvScript(keyDir);
    createBatEnvScript(keyDir);
    createPowerShellEnvScript(keyDir);

    // Step 6: Create project helper scripts
    logStep(6, 'Creating project helper scripts...');
    createProjectHelperScripts(projectPath, osType);

    // Print final instructions
    log('\n' + '='.repeat(60), 'cyan');
    log('✨ Setup Complete!', 'green');
    log('='.repeat(60), 'cyan');

    log('\n📋 Your API key is stored at:', 'yellow');
    log(`   ${keyFilePath}`, 'blue');

    log('\n📋 To load the API key in your terminal:', 'yellow');
    switch (osType) {
        case 'windows':
            log('\n   Command Prompt:', 'magenta');
            log(`   call scripts\\load-openai-key.bat`, 'blue');
            log('\n   PowerShell:', 'magenta');
            log(`   . .\\scripts\\load-openai-key.ps1`, 'blue');
            break;
        case 'macos':
        case 'linux':
            log(`   source ./scripts/load-openai-key.sh`, 'blue');
            break;
    }

    log('\n📋 To verify the key is loaded:', 'yellow');
    if (osType === 'windows') {
        log('   echo %OPENAI_API_KEY%', 'blue');
    } else {
        log('   echo $OPENAI_API_KEY', 'blue');
    }

    log('\n📋 In Python code:', 'yellow');
    log('   from openai import OpenAI', 'blue');
    log('   client = OpenAI()  # Uses OPENAI_API_KEY env var', 'blue');

    log('\n', 'reset');
}

// Run main function
main().catch(error => {
    logError(`Setup failed: ${error.message}`);
    process.exit(1);
});

