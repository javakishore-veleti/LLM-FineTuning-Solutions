#!/usr/bin/env node

/**
 * Runner script for Python modules
 * Handles virtual environment activation and script execution
 */

const { spawn } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

// Configuration
const VENV_NAME = 'LLM-FineTuning-Solutions';
const VENV_BASE = path.join(os.homedir(), 'runtime_data', 'python_venvs');
const VENV_PATH = path.join(VENV_BASE, VENV_NAME);

// Colors
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function getPythonPath() {
    const isWindows = os.platform() === 'win32';
    if (isWindows) {
        return path.join(VENV_PATH, 'Scripts', 'python.exe');
    }
    return path.join(VENV_PATH, 'bin', 'python');
}

function loadOpenAIKey() {
    const keyFile = path.join(os.homedir(), 'runtime_data', 'keys', 'openai', 'openai_api_key.txt');
    if (fs.existsSync(keyFile)) {
        const key = fs.readFileSync(keyFile, 'utf-8').trim();
        process.env.OPENAI_API_KEY = key;
        return true;
    }
    return false;
}

function runPythonScript(scriptPath, args = []) {
    const pythonPath = getPythonPath();

    // Check if venv exists
    if (!fs.existsSync(pythonPath)) {
        log(`\n❌ Python virtual environment not found at: ${VENV_PATH}`, 'red');
        log(`   Run 'npm run setup:venv' first to create the virtual environment.`, 'yellow');
        process.exit(1);
    }

    // Load OpenAI key if needed
    if (scriptPath.includes('vector_store')) {
        if (!loadOpenAIKey()) {
            log(`\n❌ OpenAI API key not found.`, 'red');
            log(`   Run 'npm run setup:openai' first to configure your API key.`, 'yellow');
            process.exit(1);
        }
    }

    log(`\n🐍 Running Python script: ${path.basename(scriptPath)}`, 'cyan');
    log(`   Using: ${pythonPath}`, 'cyan');
    log('', 'reset');

    const child = spawn(pythonPath, [scriptPath, ...args], {
        cwd: process.cwd(),
        stdio: 'inherit',
        env: {
            ...process.env,
            PYTHONPATH: process.cwd()
        }
    });

    child.on('close', (code) => {
        if (code === 0) {
            log(`\n✅ Script completed successfully`, 'green');
        } else {
            log(`\n❌ Script exited with code ${code}`, 'red');
        }
        process.exit(code);
    });

    child.on('error', (err) => {
        log(`\n❌ Failed to start Python: ${err.message}`, 'red');
        process.exit(1);
    });
}

// Main
const args = process.argv.slice(2);

if (args.length < 1) {
    log('Usage: node run-python.js <script-path> [args...]', 'yellow');
    process.exit(1);
}

const scriptPath = args[0];
const scriptArgs = args.slice(1);

runPythonScript(scriptPath, scriptArgs);

