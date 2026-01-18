#!/usr/bin/env node

/**
 * Display Daily Usage Commands
 * Shows developers what commands to run during daily development
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
log('  🔄 DAILY USAGE COMMANDS', 'bold');
log('  Run these commands during daily development workflow', 'yellow');
log('═'.repeat(70), 'cyan');

console.log('');
log('📊 CHECK STATUS', 'green');
log('─'.repeat(50), 'cyan');
console.log('');
log('   # View OpenAI storage summary (files, vector stores)', 'white');
log('   npm run openai:summary', 'yellow');
console.log('');
log('   # Check if vector DB exists and its status', 'white');
log('   npm run vectordb:status', 'yellow');
console.log('');
log('   # Verify OpenAI API key is still valid', 'white');
log('   npm run check:openai', 'yellow');

console.log('');
log('🔄 REFRESH CONTENT', 'green');
log('─'.repeat(50), 'cyan');
console.log('');
log('   # Re-scrape content (deletes old, fetches fresh)', 'white');
log('   npm run scrape:refresh', 'yellow');
console.log('');
log('   # Update vector DB with new scraped content', 'white');
log('   npm run index:update', 'yellow');

console.log('');
log('🗑️  DELETE SPECIFIC DATA', 'green');
log('─'.repeat(50), 'cyan');
console.log('');
log('   # Delete a specific file from OpenAI storage', 'white');
log('   npm run openai:files:delete -- --filename=<filename.txt>', 'yellow');
console.log('');
log('   # Delete only local scraped files (keep OpenAI data)', 'white');
log('   npm run cleanup:local', 'yellow');
console.log('');
log('   # Delete vector DB from OpenAI (keeps local files)', 'white');
log('   npm run vectordb:delete', 'yellow');
console.log('');
log('   # Delete ALL files from OpenAI storage', 'white');
log('   npm run openai:files:delete-all', 'yellow');
console.log('');
log('   # Delete ALL vector stores from OpenAI', 'white');
log('   npm run openai:stores:delete-all', 'yellow');

console.log('');
log('💥 FULL CLEANUP (when needed)', 'red');
log('─'.repeat(50), 'cyan');
console.log('');
log('   # Delete all OpenAI data (files + vector stores)', 'white');
log('   npm run openai:cleanup-all', 'yellow');
console.log('');
log('   # Delete EVERYTHING (OpenAI + local data) - requires confirmation', 'white');
log('   npm run cleanup:all', 'yellow');

console.log('');
log('═'.repeat(70), 'cyan');
log('  💡 First time? Run "npm run first-time" to see setup commands', 'green');
log('═'.repeat(70), 'cyan');
console.log('');

