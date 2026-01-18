#!/usr/bin/env node

/**
 * Python Virtual Environment Setup Script
 *
 * Creates a Python virtual environment named "LLM-FineTuning-Solutions" in:
 * - Windows: %USERPROFILE%\runtime_data\python_venvs\
 * - macOS/Linux: ~/runtime_data/python_venvs/
 *
 * Supports: Windows, macOS, Ubuntu/Linux
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const VENV_NAME = 'LLM-FineTuning-Solutions';

// Colors for console output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m'
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
 * Get the virtual environment base path
 */
function getVenvBasePath() {
    const homeDir = getHomeDir();
    return path.join(homeDir, 'runtime_data', 'python_venvs');
}

/**
 * Get the full virtual environment path
 */
function getVenvPath() {
    return path.join(getVenvBasePath(), VENV_NAME);
}

/**
 * Get the Python executable path based on OS
 */
function getPythonExecutable(osType) {
    const pythonCommands = ['python3.11', 'python3', 'python'];

    for (const cmd of pythonCommands) {
        try {
            const version = execSync(`${cmd} --version 2>&1`, { encoding: 'utf-8' });
            if (version.includes('3.11') || version.includes('3.')) {
                log(`Found Python: ${version.trim()}`, 'blue');
                return cmd;
            }
        } catch (e) {
            // Try next command
        }
    }

    // On Windows, try py launcher
    if (osType === 'windows') {
        try {
            const version = execSync('py -3.11 --version 2>&1', { encoding: 'utf-8' });
            log(`Found Python: ${version.trim()}`, 'blue');
            return 'py -3.11';
        } catch (e) {
            try {
                const version = execSync('py -3 --version 2>&1', { encoding: 'utf-8' });
                log(`Found Python: ${version.trim()}`, 'blue');
                return 'py -3';
            } catch (e2) {
                // Continue
            }
        }
    }

    return null;
}

/**
 * Get the pip executable path within the venv
 */
function getVenvPip(osType, venvPath) {
    if (osType === 'windows') {
        return path.join(venvPath, 'Scripts', 'pip.exe');
    }
    return path.join(venvPath, 'bin', 'pip');
}

/**
 * Get the Python executable path within the venv
 */
function getVenvPython(osType, venvPath) {
    if (osType === 'windows') {
        return path.join(venvPath, 'Scripts', 'python.exe');
    }
    return path.join(venvPath, 'bin', 'python');
}

/**
 * Get the activation script path based on OS
 */
function getActivationScript(osType, venvPath) {
    switch (osType) {
        case 'windows':
            return {
                cmd: path.join(venvPath, 'Scripts', 'activate.bat'),
                powershell: path.join(venvPath, 'Scripts', 'Activate.ps1'),
                command: `${path.join(venvPath, 'Scripts', 'activate.bat')}`
            };
        case 'macos':
        case 'linux':
            return {
                bash: path.join(venvPath, 'bin', 'activate'),
                command: `source ${path.join(venvPath, 'bin', 'activate')}`
            };
        default:
            return null;
    }
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
 * Check if virtual environment already exists
 */
function venvExists(venvPath) {
    const osType = detectOS();
    const pythonPath = getVenvPython(osType, venvPath);
    return fs.existsSync(pythonPath);
}

/**
 * Create the virtual environment
 */
function createVenv(pythonCmd, venvPath) {
    log(`Creating virtual environment at: ${venvPath}`, 'blue');

    try {
        // Handle 'py -3.11' style commands
        if (pythonCmd.includes(' ')) {
            const [cmd, ...args] = pythonCmd.split(' ');
            execSync(`${cmd} ${args.join(' ')} -m venv "${venvPath}"`, {
                stdio: 'inherit',
                shell: true
            });
        } else {
            execSync(`${pythonCmd} -m venv "${venvPath}"`, {
                stdio: 'inherit',
                shell: true
            });
        }
        logSuccess(`Virtual environment created successfully!`);
        return true;
    } catch (error) {
        logError(`Failed to create virtual environment: ${error.message}`);
        return false;
    }
}

/**
 * Install requirements from requirements.txt
 */
function installRequirements(osType, venvPath, projectPath) {
    const pipPath = getVenvPip(osType, venvPath);
    const requirementsPath = path.join(projectPath, 'requirements.txt');

    if (!fs.existsSync(requirementsPath)) {
        logWarning(`requirements.txt not found at: ${requirementsPath}`);
        return false;
    }

    log(`Installing dependencies from requirements.txt...`, 'blue');

    try {
        // Upgrade pip first
        log(`Upgrading pip...`, 'blue');
        execSync(`"${pipPath}" install --upgrade pip`, {
            stdio: 'inherit',
            shell: true
        });

        // Install requirements
        execSync(`"${pipPath}" install -r "${requirementsPath}"`, {
            stdio: 'inherit',
            shell: true
        });

        logSuccess(`Dependencies installed successfully!`);
        return true;
    } catch (error) {
        logError(`Failed to install dependencies: ${error.message}`);
        return false;
    }
}

/**
 * Print activation instructions
 */
function printActivationInstructions(osType, venvPath) {
    const activation = getActivationScript(osType, venvPath);

    log('\n' + '='.repeat(60), 'cyan');
    log('📋 ACTIVATION INSTRUCTIONS', 'green');
    log('='.repeat(60), 'cyan');

    switch (osType) {
        case 'windows':
            log('\nFor Command Prompt:', 'yellow');
            log(`  ${activation.cmd}`, 'blue');
            log('\nFor PowerShell:', 'yellow');
            log(`  ${activation.powershell}`, 'blue');
            break;
        case 'macos':
        case 'linux':
            log('\nFor Bash/Zsh:', 'yellow');
            log(`  source ${activation.bash}`, 'blue');
            break;
    }

    log('\nTo deactivate:', 'yellow');
    log('  deactivate', 'blue');

    log('\n' + '='.repeat(60), 'cyan');
}

/**
 * Create a convenience activation script in the project
 */
function createActivationHelper(osType, venvPath, projectPath) {
    const activation = getActivationScript(osType, venvPath);

    if (osType === 'windows') {
        // Create batch file for Windows
        const batContent = `@echo off
echo Activating LLM-FineTuning-Solutions virtual environment...
call "${activation.cmd}"
echo Virtual environment activated!
`;
        fs.writeFileSync(path.join(projectPath, 'activate-venv.bat'), batContent);

        // Create PowerShell script
        const ps1Content = `# Activate LLM-FineTuning-Solutions virtual environment
Write-Host "Activating LLM-FineTuning-Solutions virtual environment..." -ForegroundColor Cyan
& "${activation.powershell}"
Write-Host "Virtual environment activated!" -ForegroundColor Green
`;
        fs.writeFileSync(path.join(projectPath, 'activate-venv.ps1'), ps1Content);

        logSuccess('Created activate-venv.bat and activate-venv.ps1');
    } else {
        // Create shell script for macOS/Linux
        const shContent = `#!/bin/bash
# Activate LLM-FineTuning-Solutions virtual environment
echo "Activating LLM-FineTuning-Solutions virtual environment..."
source "${activation.bash}"
echo "Virtual environment activated!"
`;
        const scriptPath = path.join(projectPath, 'activate-venv.sh');
        fs.writeFileSync(scriptPath, shContent);
        fs.chmodSync(scriptPath, '755');

        logSuccess('Created activate-venv.sh');
    }
}

/**
 * Main setup function
 */
async function main() {
    const args = process.argv.slice(2);
    const activateInfoOnly = args.includes('--activate-info');

    log('\n🚀 LLM-FineTuning-Solutions Python Environment Setup', 'green');
    log('='.repeat(60), 'cyan');

    // Step 1: Detect OS
    logStep(1, 'Detecting operating system...');
    const osType = detectOS();
    logSuccess(`Detected OS: ${osType}`);

    // Get paths
    const venvBasePath = getVenvBasePath();
    const venvPath = getVenvPath();
    const projectPath = process.cwd();

    log(`\n📁 Paths:`, 'blue');
    log(`   Home Directory: ${getHomeDir()}`);
    log(`   Venv Base Path: ${venvBasePath}`);
    log(`   Venv Full Path: ${venvPath}`);
    log(`   Project Path: ${projectPath}`);

    // If only showing activation info
    if (activateInfoOnly) {
        if (venvExists(venvPath)) {
            printActivationInstructions(osType, venvPath);
        } else {
            logError(`Virtual environment does not exist at: ${venvPath}`);
            log('Run "npm run setup" to create it first.', 'yellow');
        }
        return;
    }

    // Step 2: Find Python
    logStep(2, 'Finding Python installation...');
    const pythonCmd = getPythonExecutable(osType);

    if (!pythonCmd) {
        logError('Python 3.x not found! Please install Python 3.11 or later.');
        log('\nInstallation instructions:', 'yellow');
        switch (osType) {
            case 'windows':
                log('  Download from: https://www.python.org/downloads/', 'blue');
                log('  Or use: winget install Python.Python.3.11', 'blue');
                break;
            case 'macos':
                log('  brew install python@3.11', 'blue');
                break;
            case 'linux':
                log('  sudo apt update && sudo apt install python3.11 python3.11-venv', 'blue');
                break;
        }
        process.exit(1);
    }
    logSuccess(`Using Python: ${pythonCmd}`);

    // Step 3: Create base directory
    logStep(3, 'Creating virtual environment directory...');
    ensureDirectory(venvBasePath);

    // Step 4: Check if venv exists or create it
    logStep(4, 'Setting up virtual environment...');

    if (venvExists(venvPath)) {
        logWarning(`Virtual environment already exists at: ${venvPath}`);
        log('Skipping creation, will install/update dependencies.', 'blue');
    } else {
        if (!createVenv(pythonCmd, venvPath)) {
            process.exit(1);
        }
    }

    // Step 5: Install requirements
    logStep(5, 'Installing dependencies...');
    installRequirements(osType, venvPath, projectPath);

    // Step 6: Create activation helper scripts
    logStep(6, 'Creating activation helper scripts...');
    createActivationHelper(osType, venvPath, projectPath);

    // Print final instructions
    printActivationInstructions(osType, venvPath);

    log('\n✨ Setup complete!', 'green');
    log('\nNext steps:', 'yellow');
    log('1. Activate the virtual environment using the commands above', 'blue');
    log('2. Run your Python scripts with the activated environment', 'blue');
    log('\nOr use the helper script:', 'yellow');
    if (osType === 'windows') {
        log('  .\\activate-venv.bat  (Command Prompt)', 'blue');
        log('  .\\activate-venv.ps1  (PowerShell)', 'blue');
    } else {
        log('  source ./activate-venv.sh', 'blue');
    }
}

// Run main function
main().catch(error => {
    logError(`Setup failed: ${error.message}`);
    process.exit(1);
});

