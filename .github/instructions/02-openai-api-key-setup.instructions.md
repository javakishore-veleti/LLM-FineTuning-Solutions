# OpenAI API Key Setup Instructions

This guide helps you set up and manage your OpenAI API key for the LLM-FineTuning-Solutions project.

## ⚠️ Important Note

**OpenAI API keys cannot be created via command line.** You must generate them manually through the OpenAI web dashboard.

## Prerequisites

- An OpenAI account (https://platform.openai.com)
- A valid payment method added to your OpenAI account (for API usage)

## Step 1: Generate Your OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in with your OpenAI account
3. Click **"Create new secret key"**
4. Give your key a name (e.g., `LLM-FineTuning-Solutions`)
5. Click **"Create secret key"**
6. **IMPORTANT**: Copy the key immediately - you won't be able to see it again!

## Step 2: Key Storage Location

This project stores API keys in a centralized location outside the project directory:

| OS | Key Storage Path |
|----|------------------|
| **macOS/Linux** | `~/runtime_data/keys/openai/` |
| **Windows** | `%USERPROFILE%\runtime_data\keys\openai\` |

### Files Created:
- `openai_api_key.txt` - Contains your API key (plain text, for scripts)
- `openai_env.sh` - Shell script to export the key (macOS/Linux)
- `openai_env.bat` - Batch script to set the key (Windows CMD)
- `openai_env.ps1` - PowerShell script to set the key (Windows PowerShell)

## Step 3: Setup Using Scripts

### Option A: Automated Setup (Recommended)

Run the setup command which will prompt you to enter your API key:

```bash
# Using npm
npm run setup:openai

# Or run directly
node scripts/setup-openai-key.js
```

### Option B: Manual Setup

#### macOS/Linux:
```bash
# Create directory
mkdir -p ~/runtime_data/keys/openai

# Create the key file (replace with your actual key)
echo "sk-your-openai-api-key-here" > ~/runtime_data/keys/openai/openai_api_key.txt

# Set proper permissions (readable only by you)
chmod 600 ~/runtime_data/keys/openai/openai_api_key.txt

# Create the environment script
cat > ~/runtime_data/keys/openai/openai_env.sh << 'EOF'
#!/bin/bash
# OpenAI API Key Environment Setup
# Source this file to set OPENAI_API_KEY in your shell

OPENAI_KEY_FILE="$HOME/runtime_data/keys/openai/openai_api_key.txt"

if [ -f "$OPENAI_KEY_FILE" ]; then
    export OPENAI_API_KEY=$(cat "$OPENAI_KEY_FILE")
    echo "✅ OPENAI_API_KEY loaded successfully"
else
    echo "❌ OpenAI API key file not found at: $OPENAI_KEY_FILE"
    echo "   Run 'npm run setup:openai' to set up your key"
fi
EOF

chmod +x ~/runtime_data/keys/openai/openai_env.sh
```

#### Windows (Command Prompt):
```cmd
REM Create directory
mkdir %USERPROFILE%\runtime_data\keys\openai

REM Create the key file (replace with your actual key)
echo sk-your-openai-api-key-here > %USERPROFILE%\runtime_data\keys\openai\openai_api_key.txt
```

#### Windows (PowerShell):
```powershell
# Create directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\runtime_data\keys\openai"

# Create the key file (replace with your actual key)
"sk-your-openai-api-key-here" | Out-File -FilePath "$env:USERPROFILE\runtime_data\keys\openai\openai_api_key.txt" -NoNewline
```

## Step 4: Loading the API Key

### Before Running Python Scripts

#### macOS/Linux:
```bash
# Source the environment script
source ~/runtime_data/keys/openai/openai_env.sh

# Or use the project helper
source ./scripts/load-openai-key.sh

# Verify it's set
echo $OPENAI_API_KEY
```

#### Windows (Command Prompt):
```cmd
REM Run the environment script
call %USERPROFILE%\runtime_data\keys\openai\openai_env.bat

REM Or use the project helper
call scripts\load-openai-key.bat

REM Verify it's set
echo %OPENAI_API_KEY%
```

#### Windows (PowerShell):
```powershell
# Run the environment script
. $env:USERPROFILE\runtime_data\keys\openai\openai_env.ps1

# Or use the project helper
. .\scripts\load-openai-key.ps1

# Verify it's set
echo $env:OPENAI_API_KEY
```

### In Python Code

```python
import os
from openai import OpenAI

# Option 1: Use environment variable (recommended)
client = OpenAI()  # Automatically uses OPENAI_API_KEY env var

# Option 2: Load from file directly
def load_openai_key():
    key_path = os.path.expanduser("~/runtime_data/keys/openai/openai_api_key.txt")
    if os.path.exists(key_path):
        with open(key_path, 'r') as f:
            return f.read().strip()
    raise FileNotFoundError(f"OpenAI API key not found at {key_path}")

client = OpenAI(api_key=load_openai_key())

# Option 3: Use python-dotenv with .env file
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
```

## Step 5: Using with npm Scripts

The `package.json` includes scripts that automatically load the API key:

```bash
# Run any Python script with OpenAI key loaded
npm run python -- your_script.py

# Or load the key and start a shell
npm run shell:openai
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Set restrictive file permissions**: `chmod 600` on macOS/Linux
3. **Use environment variables** rather than hardcoding keys
4. **Rotate keys periodically** through the OpenAI dashboard
5. **Set usage limits** in your OpenAI account to prevent unexpected charges
6. **Use separate keys** for development and production

## Troubleshooting

### Key Not Found
```
❌ OpenAI API key file not found
```
**Solution**: Run `npm run setup:openai` to set up your key.

### Invalid API Key
```
openai.AuthenticationError: Invalid API key
```
**Solution**: 
1. Verify your key at https://platform.openai.com/api-keys
2. Run `npm run setup:openai` to update your key

### Permission Denied
```
Permission denied: ~/runtime_data/keys/openai/openai_api_key.txt
```
**Solution**: Fix permissions with `chmod 600 ~/runtime_data/keys/openai/openai_api_key.txt`

## Quick Reference

| Command | Description |
|---------|-------------|
| `npm run setup:openai` | Set up or update OpenAI API key |
| `npm run load:openai` | Load API key into current shell |
| `npm run verify:openai` | Verify API key is valid |

## File Locations Summary

```
~/runtime_data/keys/openai/
├── openai_api_key.txt    # Your API key (plain text)
├── openai_env.sh         # Bash/Zsh export script
├── openai_env.bat        # Windows CMD script
└── openai_env.ps1        # Windows PowerShell script

Project Directory (scripts/ folder):
├── scripts/load-openai-key.sh    # Helper to source the key (macOS/Linux)
├── scripts/load-openai-key.bat   # Helper to load the key (Windows CMD)
└── scripts/load-openai-key.ps1   # Helper to load the key (Windows PowerShell)
```

