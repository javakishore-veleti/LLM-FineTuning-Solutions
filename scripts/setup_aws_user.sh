#!/bin/bash
set -e

# ============================================
# AWS IAM User Setup Script
# User: LLMFineTuningSolutions
# ============================================

# Configuration
AWS_USER_NAME="LLMFineTuningSolutions"
AWS_CLI_PROFILE="default"
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
    CREDS_FILE="${AWS_USER_NAME}_credentials.json"
    aws iam create-access-key \
        --user-name "$AWS_USER_NAME" \
        --profile "$AWS_CLI_PROFILE" \
        --output json > "$CREDS_FILE"

    echo -e "${GREEN}✅ Access keys created and saved to $CREDS_FILE${NC}"
    echo -e "${RED}⚠️  IMPORTANT: Store these credentials securely and delete the file!${NC}"

    # Extract credentials from JSON
    ACCESS_KEY=$(jq -r '.AccessKey.AccessKeyId' "$CREDS_FILE")
    SECRET_KEY=$(jq -r '.AccessKey.SecretAccessKey' "$CREDS_FILE")

    # Check if local profile exists before configuring
    echo -e "\n${YELLOW}Step 4.1: Configuring local AWS CLI profile...${NC}"
    if check_local_profile_exists "$AWS_USER_NAME"; then
        echo -e "${YELLOW}⚠️  Profile '$AWS_USER_NAME' already exists locally in ~/.aws/credentials${NC}"
        echo "Current configuration:"
        aws configure list --profile "$AWS_USER_NAME"
        echo "Overwriting with new credentials..."
    else
        echo "Creating new profile '$AWS_USER_NAME' in ~/.aws/credentials..."
    fi

    # Configure the profile
    aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$AWS_USER_NAME"
    aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$AWS_USER_NAME"
    aws configure set region "$AWS_REGION" --profile "$AWS_USER_NAME"
    aws configure set output json --profile "$AWS_USER_NAME"
    echo -e "${GREEN}✅ Profile '$AWS_USER_NAME' configured successfully with output format: json${NC}"

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

