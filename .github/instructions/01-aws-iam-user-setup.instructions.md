# AWS IAM User Setup Instructions

This guide helps you create an AWS IAM user with CLI access, AdministratorAccess, and BedrockAgentCoreFullAccess permissions using AWS CLI.

## Prerequisites

- AWS CLI installed (`brew install awscli` on macOS)
- An existing AWS profile with IAM permissions to create users

## Configuration Variables

```bash
# User Configuration
AWS_USER_NAME="LLMFineTuningSolutions"
AWS_CLI_PROFILE="MY_AWS_CLI_PROFILE"
AWS_REGION="us-east-1"

# Note: IAM users don't have first name, last name, or email fields.
# These are only available in AWS IAM Identity Center (SSO).
# For tagging purposes, we can add metadata as tags:
USER_DISPLAY_NAME="LLM Fine Tuning Solutions"
USER_EMAIL="dumm@example.com"
```

## Step 1: Check if AWS CLI Profile Exists

```bash
# Check if the profile exists
check_profile_exists() {
    if aws configure list --profile "$AWS_CLI_PROFILE" &>/dev/null; then
        echo "✅ Profile '$AWS_CLI_PROFILE' exists."
        return 0
    else
        echo "❌ Profile '$AWS_CLI_PROFILE' does not exist."
        return 1
    fi
}

# Run the check
if ! check_profile_exists; then
    echo "Setting up AWS CLI profile..."
    
    # Configure the profile (you'll be prompted for credentials)
    aws configure --profile "$AWS_CLI_PROFILE"
    
    # Or set values directly (replace with your actual values):
    # aws configure set aws_access_key_id YOUR_ACCESS_KEY --profile "$AWS_CLI_PROFILE"
    # aws configure set aws_secret_access_key YOUR_SECRET_KEY --profile "$AWS_CLI_PROFILE"
    # aws configure set region "$AWS_REGION" --profile "$AWS_CLI_PROFILE"
    # aws configure set output json --profile "$AWS_CLI_PROFILE"
fi
```

## Step 2: Create IAM User

```bash
# Create the IAM user with tags for metadata
aws iam create-user \
    --user-name "$AWS_USER_NAME" \
    --tags \
        Key=DisplayName,Value="$USER_DISPLAY_NAME" \
        Key=Email,Value="$USER_EMAIL" \
        Key=Project,Value="LLM-FineTuning-Solutions" \
    --profile "$AWS_CLI_PROFILE"
```

## Step 3: Attach Required Policies

```bash
# Attach AdministratorAccess policy (full admin access)
aws iam attach-user-policy \
    --user-name "$AWS_USER_NAME" \
    --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess" \
    --profile "$AWS_CLI_PROFILE"

# Attach AmazonBedrockFullAccess policy (Bedrock access)
# Note: BedrockAgentCoreFullAccess may be a custom policy or newer AWS managed policy
# Using AmazonBedrockFullAccess as the standard Bedrock policy
aws iam attach-user-policy \
    --user-name "$AWS_USER_NAME" \
    --policy-arn "arn:aws:iam::aws:policy/AmazonBedrockFullAccess" \
    --profile "$AWS_CLI_PROFILE"

# If BedrockAgentCoreFullAccess exists as a managed policy, attach it:
# aws iam attach-user-policy \
#     --user-name "$AWS_USER_NAME" \
#     --policy-arn "arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess" \
#     --profile "$AWS_CLI_PROFILE"
```

## Step 4: Create Programmatic Access (CLI Access Keys)

```bash
# Create access keys for CLI/programmatic access
aws iam create-access-key \
    --user-name "$AWS_USER_NAME" \
    --profile "$AWS_CLI_PROFILE" \
    --output json > "${AWS_USER_NAME}_credentials.json"

# IMPORTANT: Save these credentials securely!
echo "⚠️  Access keys saved to ${AWS_USER_NAME}_credentials.json"
echo "⚠️  Store these credentials securely and delete the file after saving them!"

# Display the credentials (be careful with this in production)
cat "${AWS_USER_NAME}_credentials.json"
```

**Output Example:**
```json
{
    "AccessKey": {
        "UserName": "LLMFineTuningSolutions",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "Status": "Active",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "CreateDate": "2026-01-18T12:00:00+00:00"
    }
}
```

## Step 5: Configure AWS CLI Profile with Access Keys

```bash
# Extract credentials from the JSON file
ACCESS_KEY=$(jq -r '.AccessKey.AccessKeyId' "${AWS_USER_NAME}_credentials.json")
SECRET_KEY=$(jq -r '.AccessKey.SecretAccessKey' "${AWS_USER_NAME}_credentials.json")

# Function to check if local profile exists
check_local_profile_exists() {
    local profile_name="$1"
    if aws configure list --profile "$profile_name" 2>/dev/null | grep -q "access_key"; then
        # Check if access_key is actually set (not just profile exists)
        local access_key_check=$(aws configure get aws_access_key_id --profile "$profile_name" 2>/dev/null)
        if [ -n "$access_key_check" ]; then
            return 0  # Profile exists with credentials
        fi
    fi
    return 1  # Profile doesn't exist or has no credentials
}

# Configure the profile only if it doesn't already exist locally
if check_local_profile_exists "$AWS_USER_NAME"; then
    echo "⚠️  Profile '$AWS_USER_NAME' already exists locally in ~/.aws/credentials"
    echo "Current configuration:"
    aws configure list --profile "$AWS_USER_NAME"
    
    read -p "Do you want to overwrite the existing profile? (y/N): " overwrite
    if [[ "$overwrite" =~ ^[Yy]$ ]]; then
        echo "Updating profile '$AWS_USER_NAME'..."
        aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$AWS_USER_NAME"
        aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$AWS_USER_NAME"
        aws configure set region "$AWS_REGION" --profile "$AWS_USER_NAME"
        aws configure set output json --profile "$AWS_USER_NAME"
        echo "✅ Profile '$AWS_USER_NAME' updated successfully!"
    else
        echo "⏭️  Skipping profile configuration. Existing profile retained."
    fi
else
    echo "Creating new profile '$AWS_USER_NAME' in ~/.aws/credentials..."
    aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$AWS_USER_NAME"
    aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$AWS_USER_NAME"
    aws configure set region "$AWS_REGION" --profile "$AWS_USER_NAME"
    aws configure set output json --profile "$AWS_USER_NAME"
    echo "✅ Profile '$AWS_USER_NAME' configured successfully!"
fi

# Display the configured profile location
echo ""
echo "📁 AWS CLI Configuration Files:"
echo "   Credentials: ~/.aws/credentials"
echo "   Config: ~/.aws/config"
echo ""
echo "📋 Profile configured with output format: json"
```

## Step 6: Verify Access Keys Configuration

```bash
# Verify the profile is configured correctly
aws configure list --profile "$AWS_USER_NAME"

# Test the credentials by getting caller identity
aws sts get-caller-identity --profile "$AWS_USER_NAME"

# Expected output:
# {
#     "UserId": "AIDAEXAMPLEUSERID",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/LLMFineTuningSolutions"
# }
```

## Step 7: Store Access Keys Securely

```bash
# Option 1: Use AWS credentials file (default location: ~/.aws/credentials)
# The credentials are already stored when using 'aws configure set'

# Option 2: Export as environment variables (for current session)
export AWS_ACCESS_KEY_ID="$ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$SECRET_KEY"
export AWS_DEFAULT_REGION="$AWS_REGION"

# Option 3: Create a .env file for your project (DO NOT commit to git!)
cat > .env << EOF
AWS_ACCESS_KEY_ID=$ACCESS_KEY
AWS_SECRET_ACCESS_KEY=$SECRET_KEY
AWS_DEFAULT_REGION=$AWS_REGION
AWS_PROFILE=$AWS_USER_NAME
EOF

# Make sure .env is in .gitignore
echo ".env" >> .gitignore
echo "${AWS_USER_NAME}_credentials.json" >> .gitignore

# Delete the credentials JSON file after storing securely
rm -f "${AWS_USER_NAME}_credentials.json"
echo "✅ Credentials file deleted for security."
```

## Complete Setup Script

```bash
#!/bin/bash
set -e

# ============================================
# AWS IAM User Setup Script
# User: LLMFineTuningSolutions
# ============================================

# Configuration
AWS_USER_NAME="LLMFineTuningSolutions"
AWS_CLI_PROFILE="MY_AWS_CLI_PROFILE"
AWS_REGION="us-east-1"
USER_DISPLAY_NAME="LLM Fine Tuning Solutions"
USER_EMAIL="dumm@example.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting AWS IAM User Setup...${NC}"

# Step 1: Check if profile exists
echo -e "\n${YELLOW}Step 1: Checking AWS CLI profile...${NC}"
if aws configure list --profile "$AWS_CLI_PROFILE" &>/dev/null; then
    echo -e "${GREEN}✅ Profile '$AWS_CLI_PROFILE' exists.${NC}"
else
    echo -e "${RED}❌ Profile '$AWS_CLI_PROFILE' does not exist.${NC}"
    echo "Please configure the profile first:"
    echo "  aws configure --profile $AWS_CLI_PROFILE"
    exit 1
fi

# Step 2: Check if user already exists
echo -e "\n${YELLOW}Step 2: Checking if user exists...${NC}"
if aws iam get-user --user-name "$AWS_USER_NAME" --profile "$AWS_CLI_PROFILE" &>/dev/null; then
    echo -e "${YELLOW}⚠️  User '$AWS_USER_NAME' already exists. Skipping user creation.${NC}"
else
    echo "Creating IAM user..."
    aws iam create-user \
        --user-name "$AWS_USER_NAME" \
        --tags \
            Key=DisplayName,Value="$USER_DISPLAY_NAME" \
            Key=Email,Value="$USER_EMAIL" \
            Key=Project,Value="LLM-FineTuning-Solutions" \
        --profile "$AWS_CLI_PROFILE"
    echo -e "${GREEN}✅ User '$AWS_USER_NAME' created.${NC}"
fi

# Step 3: Attach policies
echo -e "\n${YELLOW}Step 3: Attaching policies...${NC}"

# AdministratorAccess
echo "Attaching AdministratorAccess..."
aws iam attach-user-policy \
    --user-name "$AWS_USER_NAME" \
    --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess" \
    --profile "$AWS_CLI_PROFILE" 2>/dev/null || true
echo -e "${GREEN}✅ AdministratorAccess attached.${NC}"

# AmazonBedrockFullAccess
echo "Attaching AmazonBedrockFullAccess..."
aws iam attach-user-policy \
    --user-name "$AWS_USER_NAME" \
    --policy-arn "arn:aws:iam::aws:policy/AmazonBedrockFullAccess" \
    --profile "$AWS_CLI_PROFILE" 2>/dev/null || true
echo -e "${GREEN}✅ AmazonBedrockFullAccess attached.${NC}"

# Step 4: Create access keys (if none exist)
echo -e "\n${YELLOW}Step 4: Creating programmatic access keys...${NC}"
EXISTING_KEYS=$(aws iam list-access-keys --user-name "$AWS_USER_NAME" --profile "$AWS_CLI_PROFILE" --query 'AccessKeyMetadata[*].AccessKeyId' --output text)

# Function to check if local profile exists with credentials
check_local_profile_exists() {
    local profile_name="$1"
    local access_key_check=$(aws configure get aws_access_key_id --profile "$profile_name" 2>/dev/null)
    if [ -n "$access_key_check" ]; then
        return 0  # Profile exists with credentials
    fi
    return 1  # Profile doesn't exist or has no credentials
}

if [ -z "$EXISTING_KEYS" ]; then
    aws iam create-access-key \
        --user-name "$AWS_USER_NAME" \
        --profile "$AWS_CLI_PROFILE" \
        --output json > "${AWS_USER_NAME}_credentials.json"
    
    echo -e "${GREEN}✅ Access keys created and saved to ${AWS_USER_NAME}_credentials.json${NC}"
    echo -e "${RED}⚠️  IMPORTANT: Store these credentials securely and delete the file!${NC}"
    
    # Extract credentials from JSON
    ACCESS_KEY=$(jq -r '.AccessKey.AccessKeyId' "${AWS_USER_NAME}_credentials.json")
    SECRET_KEY=$(jq -r '.AccessKey.SecretAccessKey' "${AWS_USER_NAME}_credentials.json")
    
    # Check if local profile exists before configuring
    echo -e "\n${YELLOW}Step 4.1: Configuring local AWS CLI profile...${NC}"
    if check_local_profile_exists "$AWS_USER_NAME"; then
        echo -e "${YELLOW}⚠️  Profile '$AWS_USER_NAME' already exists locally in ~/.aws/credentials${NC}"
        echo "Current configuration:"
        aws configure list --profile "$AWS_USER_NAME"
        
        read -p "Do you want to overwrite the existing profile? (y/N): " overwrite
        if [[ "$overwrite" =~ ^[Yy]$ ]]; then
            echo "Updating profile '$AWS_USER_NAME'..."
            aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$AWS_USER_NAME"
            aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$AWS_USER_NAME"
            aws configure set region "$AWS_REGION" --profile "$AWS_USER_NAME"
            aws configure set output json --profile "$AWS_USER_NAME"
            echo -e "${GREEN}✅ Profile '$AWS_USER_NAME' updated successfully with output format: json${NC}"
        else
            echo -e "${YELLOW}⏭️  Skipping profile configuration. Existing profile retained.${NC}"
        fi
    else
        echo "Creating new profile '$AWS_USER_NAME' in ~/.aws/credentials..."
        aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$AWS_USER_NAME"
        aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$AWS_USER_NAME"
        aws configure set region "$AWS_REGION" --profile "$AWS_USER_NAME"
        aws configure set output json --profile "$AWS_USER_NAME"
        echo -e "${GREEN}✅ Profile '$AWS_USER_NAME' configured successfully with output format: json${NC}"
    fi
    
    # Display configuration file locations
    echo ""
    echo -e "${GREEN}📁 AWS CLI Configuration Files:${NC}"
    echo "   Credentials: ~/.aws/credentials"
    echo "   Config: ~/.aws/config"
    
    # Display the access keys for reference
    echo -e "\n${YELLOW}📋 Access Key Details:${NC}"
    echo "Access Key ID: $ACCESS_KEY"
    echo "Secret Access Key: $SECRET_KEY"
    echo -e "${RED}⚠️  Save these credentials NOW - the secret key cannot be retrieved again!${NC}"
    
    # Create .env file for project use
    cat > .env << EOF
# AWS Credentials for LLMFineTuningSolutions
# DO NOT COMMIT THIS FILE TO VERSION CONTROL
AWS_ACCESS_KEY_ID=$ACCESS_KEY
AWS_SECRET_ACCESS_KEY=$SECRET_KEY
AWS_DEFAULT_REGION=$AWS_REGION
AWS_PROFILE=$AWS_USER_NAME
EOF
    echo -e "${GREEN}✅ .env file created with credentials.${NC}"
    
    # Ensure .env is in .gitignore
    if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
        echo ".env" >> .gitignore
        echo "${AWS_USER_NAME}_credentials.json" >> .gitignore
        echo -e "${GREEN}✅ Added .env to .gitignore${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  User '$AWS_USER_NAME' already has access keys. Skipping key creation.${NC}"
    echo "Existing keys:"
    echo "$EXISTING_KEYS"
fi

# Step 5: Verify access keys work
echo -e "\n${YELLOW}Step 5: Verifying access keys...${NC}"
if aws sts get-caller-identity --profile "$AWS_USER_NAME" &>/dev/null; then
    echo -e "${GREEN}✅ Access keys verified successfully!${NC}"
    aws sts get-caller-identity --profile "$AWS_USER_NAME"
else
    echo -e "${RED}❌ Could not verify access keys. Profile '$AWS_USER_NAME' may not be configured.${NC}"
fi

# Step 6: Verify setup
echo -e "\n${YELLOW}Step 6: Verifying setup...${NC}"
echo "Listing attached policies for user '$AWS_USER_NAME':"
aws iam list-attached-user-policies --user-name "$AWS_USER_NAME" --profile "$AWS_CLI_PROFILE"

echo -e "\n${GREEN}🎉 AWS IAM User setup complete!${NC}"
echo -e "${GREEN}📁 AWS CLI Configuration Files:${NC}"
echo "   Credentials: ~/.aws/credentials"
echo "   Config: ~/.aws/config"
echo ""
echo -e "${GREEN}To use the new profile, run:${NC}"
echo "   export AWS_PROFILE=$AWS_USER_NAME"
echo "   # or use --profile $AWS_USER_NAME with AWS CLI commands"
```

## Cleanup Script (Optional)

If you need to delete the user and start over:

```bash
#!/bin/bash
# Cleanup script - USE WITH CAUTION

AWS_USER_NAME="LLMFineTuningSolutions"
AWS_CLI_PROFILE="MY_AWS_CLI_PROFILE"

echo "⚠️  This will delete user '$AWS_USER_NAME' and all associated resources."
read -p "Are you sure? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# 1. Delete access keys
echo "Deleting access keys..."
aws iam list-access-keys --user-name "$AWS_USER_NAME" --profile "$AWS_CLI_PROFILE" \
    --query 'AccessKeyMetadata[*].AccessKeyId' --output text | \
    xargs -I {} aws iam delete-access-key --user-name "$AWS_USER_NAME" --access-key-id {} --profile "$AWS_CLI_PROFILE"

# 2. Detach policies
echo "Detaching policies..."
aws iam detach-user-policy --user-name "$AWS_USER_NAME" \
    --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess" --profile "$AWS_CLI_PROFILE" 2>/dev/null || true
aws iam detach-user-policy --user-name "$AWS_USER_NAME" \
    --policy-arn "arn:aws:iam::aws:policy/AmazonBedrockFullAccess" --profile "$AWS_CLI_PROFILE" 2>/dev/null || true

# 3. Delete the user
echo "Deleting user..."
aws iam delete-user --user-name "$AWS_USER_NAME" --profile "$AWS_CLI_PROFILE"

echo "✅ User '$AWS_USER_NAME' deleted successfully."
```

## Important Notes

1. **Security Best Practice**: AdministratorAccess provides full access. Consider using more restrictive policies for production.

2. **IAM vs IAM Identity Center**: IAM users don't have first name, last name, or email fields. If you need those fields, consider using AWS IAM Identity Center (SSO).

3. **Credential Storage**: Never commit AWS credentials to version control. Use environment variables or AWS credentials file.

4. **MFA**: Consider enabling MFA for the user for additional security:
   ```bash
   aws iam create-virtual-mfa-device --virtual-mfa-device-name "$AWS_USER_NAME-mfa" --profile "$AWS_CLI_PROFILE"
   ```

5. **BedrockAgentCoreFullAccess**: This might be a custom policy or a newer AWS managed policy. Check AWS documentation for the exact policy ARN.

