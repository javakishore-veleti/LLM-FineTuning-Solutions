#!/usr/bin/env node

/**
 * Display First-Time Setup Commands
 * Shows developers what commands to run for initial setup
 */

const colors = {
    reset: '\x1b[0m',
    bold: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    magenta: '\x1b[35m',
    white: '\x1b[37m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

console.log('');
log('═'.repeat(70), 'cyan');
log('  🔧 FIRST-TIME SETUP COMMANDS', 'bold');
log('  Run these commands ONCE when setting up the project for the first time', 'yellow');
log('═'.repeat(70), 'cyan');

console.log('');
log('📦 STEP 1: Environment Setup', 'green');
log('─'.repeat(50), 'cyan');
console.log('');
log('   # Create Python virtual environment and install dependencies', 'white');
log('   npm run setup', 'yellow');
console.log('');
log('   # Configure OpenAI API key (you will be prompted to enter it)', 'white');
log('   npm run setup:openai', 'yellow');
console.log('');
log('   # Verify OpenAI key is configured', 'white');
log('   npm run check:openai', 'yellow');

console.log('');
log('📥 STEP 2: Initial Data Setup', 'green');
log('─'.repeat(50), 'cyan');
console.log('');
log('   # Scrape AWS re:Invent 2025 content', 'white');
log('   npm run scrape', 'yellow');
console.log('');
log('   # Create vector database from scraped content', 'white');
log('   npm run index', 'yellow');
console.log('');
log('   # Verify vector DB was created', 'white');
log('   npm run vectordb:status', 'yellow');

console.log('');
log('🗑️  STEP 3: Cleanup Options (if needed)', 'green');
log('─'.repeat(50), 'cyan');
console.log('');
log('   # Delete a specific file from OpenAI storage', 'white');
log('   npm run openai:files:delete -- --filename=<filename.txt>', 'yellow');
console.log('');
log('   # Delete all vector stores from OpenAI', 'white');
log('   npm run openai:stores:delete-all', 'yellow');
console.log('');
log('   # Delete only local scraped data', 'white');
log('   npm run cleanup:local', 'yellow');
console.log('');
log('   # Delete EVERYTHING and start fresh (OpenAI + local)', 'white');
log('   npm run cleanup:all', 'yellow');

console.log('');
log('═'.repeat(70), 'cyan');
log('  ✅ After completing these steps, use "npm run daily" for daily commands', 'green');
log('═'.repeat(70), 'cyan');
console.log('');

