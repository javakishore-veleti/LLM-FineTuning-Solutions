# LLM-FineTuning-Solutions

A comprehensive toolkit for fine-tuning Large Language Models (LLMs) using AWS Bedrock, OpenAI, and Anthropic Claude APIs.

## 🚀 Features

- **AWS Bedrock Integration** - Fine-tune and deploy models on AWS Bedrock
- **OpenAI LLM Support** - Work with GPT models via OpenAI API
- **Claude LLM Support** - Integrate Anthropic's Claude models
- **Data Processing** - Pandas & NumPy for data manipulation
- **Visualization** - Matplotlib for training metrics visualization
- **SQLite Database** - Local data storage with SQLAlchemy ORM
- **Flask API** - RESTful API for model inference

## 📋 Prerequisites

- Python 3.11+
- PyCharm IDE (with GitHub Copilot plugin)
- AWS CLI installed (`brew install awscli` on macOS)
- AWS Account with appropriate permissions

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/javakishore-veleti/LLM-FineTuning-Solutions.git
cd LLM-FineTuning-Solutions
```

### 2. Setup Python Virtual Environment (Recommended)

This project uses a centralized virtual environment located at:
- **Windows**: `%USERPROFILE%\runtime_data\python_venvs\LLM-FineTuning-Solutions`
- **macOS/Linux**: `~/runtime_data/python_venvs/LLM-FineTuning-Solutions`

#### Option A: Automated Setup (Recommended)

```bash
# Using npm (creates venv + installs dependencies)
npm run setup

# Or run directly with Node.js
node scripts/setup-python-env.js
```

#### Option B: Manual Setup

```bash
# Create the directory structure
mkdir -p ~/runtime_data/python_venvs  # macOS/Linux
# or
mkdir %USERPROFILE%\runtime_data\python_venvs  # Windows

# Create virtual environment
python3.11 -m venv ~/runtime_data/python_venvs/LLM-FineTuning-Solutions  # macOS/Linux
# or
python -m venv %USERPROFILE%\runtime_data\python_venvs\LLM-FineTuning-Solutions  # Windows
```

### 3. Activate Virtual Environment

After running the setup, use the generated helper scripts:

**macOS/Linux:**
```bash
source ./scripts/activate-venv.sh
# or manually:
source ~/runtime_data/python_venvs/LLM-FineTuning-Solutions/bin/activate
```

**Windows (Command Prompt):**
```cmd
call scripts\activate-venv.bat
REM or manually:
%USERPROFILE%\runtime_data\python_venvs\LLM-FineTuning-Solutions\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
. .\scripts\activate-venv.ps1
# or manually:
& $env:USERPROFILE\runtime_data\python_venvs\LLM-FineTuning-Solutions\Scripts\Activate.ps1
```

### 4. Install Dependencies (if not using npm setup)

```bash
pip install -r requirements.txt
```

## 🤖 Setting Up GitHub Copilot in PyCharm

### Step 1: Install GitHub Copilot Plugin

1. Open **PyCharm**
2. Go to **Settings/Preferences** → **Plugins**
3. Search for **"GitHub Copilot"** in the Marketplace
4. Click **Install**
5. Restart PyCharm when prompted
6. Sign in with your GitHub account when prompted

### Step 2: Enable GitHub Copilot Agent Mode

1. After installation, you'll see the **GitHub Copilot** tool window at the bottom of PyCharm
2. Click on the **Copilot Chat** icon (or press `Ctrl+Shift+C` / `Cmd+Shift+C`)
3. In the chat window, click on the **Agent** mode toggle (if available) or type `/agent` to enable agent mode

## ☁️ AWS CLI Profile & IAM User Setup

This project includes automated instructions for setting up AWS CLI with proper IAM user permissions.

### Using GitHub Copilot Agent Mode (Recommended)

1. **Open the Instructions File**
   - In PyCharm, navigate to: `.github/instructions/01-aws-iam-user-setup.instructions.md`
   - Open the file in the editor

2. **Attach the File to Copilot**
   - Open the **GitHub Copilot Chat** window (bottom panel or `Cmd+Shift+C`)
   - Click the **"+"** or **"Attach"** button in the chat input area
   - Select **"File"** and choose `01-aws-iam-user-setup.instructions.md`
   - Or drag and drop the file into the chat window

3. **Run in Agent Mode**
   - Make sure **Agent Mode** is enabled (look for the Agent toggle or icon)
   - Type the following prompt in the chat:
   
   ```
   /run
   ```
   
   Or be more specific:
   
   ```
   Please execute the AWS IAM user setup instructions to create the LLMFineTuningSolutions user with AdministratorAccess and BedrockFullAccess permissions, and configure the local AWS CLI profile.
   ```

4. **Follow the Prompts**
   - The Copilot Agent will execute the setup steps
   - Enter your AWS credentials when prompted
   - The agent will create the IAM user, attach policies, and configure your local AWS CLI

### Manual Setup (Alternative)

If you prefer to run the setup manually:

```bash
# Make the script executable
chmod +x scripts/setup_aws_user.sh

# Run the setup script
./scripts/setup_aws_user.sh
```

### What Gets Configured

After running the setup, you'll have:

| Item | Details |
|------|---------|
| **IAM User** | `LLMFineTuningSolutions` |
| **Policies** | `AdministratorAccess`, `AmazonBedrockFullAccess` |
| **AWS CLI Profile** | `LLMFineTuningSolutions` in `~/.aws/credentials` |
| **Region** | `us-east-1` |
| **Output Format** | `json` |
| **Local Files** | `.env` with credentials (gitignored) |

### Verify Setup

```bash
# Test the new profile
aws sts get-caller-identity --profile LLMFineTuningSolutions

# Or set as default for session
export AWS_PROFILE=LLMFineTuningSolutions
aws sts get-caller-identity
```

## 🔑 OpenAI API Key Setup

This project stores API keys securely outside the project directory.

### Key Storage Location

| OS | Path |
|----|------|
| **macOS/Linux** | `~/runtime_data/keys/openai/` |
| **Windows** | `%USERPROFILE%\runtime_data\keys\openai\` |

### NPM Commands for OpenAI Key Management

| Command | Description |
|---------|-------------|
| `npm run check:openai` | Check if OpenAI key exists (prompts to set up if missing) |
| `npm run setup:openai` | Set up OpenAI API key (prompts for key input) |
| `npm run update:openai` | Update/replace existing OpenAI API key |
| `npm run verify:openai` | Verify the key format is valid |
| `npm run load:openai` | Show command to load key into terminal |

### Setup Steps

1. **Check if key exists** (will prompt you to set up if missing):
   ```bash
   npm run check:openai
   ```

2. **If key is missing**, get your API key from [OpenAI Platform](https://platform.openai.com/api-keys) and run:
   ```bash
   npm run setup:openai
   ```

3. **Enter your API key** when prompted (starts with `sk-`)

4. **Load the key** before running Python scripts:

   **macOS/Linux:**
   ```bash
   source ./scripts/load-openai-key.sh
   ```

   **Windows (CMD):**
   ```cmd
   call scripts\load-openai-key.bat
   ```

   **Windows (PowerShell):**
   ```powershell
   . .\scripts\load-openai-key.ps1
   ```

### Update Your API Key

If you need to update your API key:
```bash
npm run update:openai
```

### Using in Python

```python
from openai import OpenAI

# Automatically uses OPENAI_API_KEY environment variable
client = OpenAI()

# Make a request
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```


For detailed instructions, see: `.github/instructions/02-openai-api-key-setup.instructions.md`

## 📁 Project Structure

```
LLM-FineTuning-Solutions/
├── .github/
│   └── instructions/
│       ├── 01-aws-iam-user-setup.instructions.md  # AWS setup guide
│       └── 02-openai-api-key-setup.instructions.md # OpenAI key setup guide
├── scripts/
│   ├── setup_aws_user.sh                          # AWS IAM setup script
│   ├── setup-python-env.js                        # Python venv setup (cross-platform)
│   ├── setup-openai-key.js                        # OpenAI key setup (cross-platform)
│   ├── activate-venv.sh                           # macOS/Linux venv activation (generated)
│   ├── activate-venv.bat                          # Windows CMD venv activation (generated)
│   ├── activate-venv.ps1                          # Windows PowerShell venv activation (generated)
│   ├── load-openai-key.sh                         # macOS/Linux OpenAI key loader (generated)
│   ├── load-openai-key.bat                        # Windows CMD OpenAI key loader (generated)
│   └── load-openai-key.ps1                        # Windows PowerShell OpenAI key loader (generated)
├── .env                                           # Environment variables (gitignored)
├── .gitignore
├── LICENSE
├── package.json                                   # NPM scripts for setup
├── README.md
└── requirements.txt

# External Directories (not in project):
~/runtime_data/
├── python_venvs/
│   └── LLM-FineTuning-Solutions/                  # Python virtual environment
└── keys/
    └── openai/
        ├── openai_api_key.txt                     # Your API key
        ├── openai_env.sh                          # Bash export script
        ├── openai_env.bat                         # Windows CMD script
        └── openai_env.ps1                         # PowerShell script
```

## 🔒 Security Notes

- **Never commit** `.env` or credential files to version control
- The `.gitignore` is pre-configured to exclude sensitive files
- Store AWS credentials securely
- Consider using AWS IAM roles for production workloads
- Enable MFA for the IAM user for additional security

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | ≥2.0.0 | Data processing |
| numpy | ≥1.24.0 | Numerical operations |
| matplotlib | ≥3.7.0 | Visualization |
| boto3 | ≥1.28.0 | AWS SDK |
| openai | ≥1.0.0 | OpenAI API |
| anthropic | ≥0.18.0 | Claude API |
| sqlalchemy | ≥2.0.0 | Database ORM |
| flask | ≥3.0.0 | Web API |
| flask-restful | ≥0.3.10 | REST API |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
