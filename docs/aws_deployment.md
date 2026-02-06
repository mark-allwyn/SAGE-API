# SAGE API - AWS Deployment Guide

Deploy the SAGE API to AWS App Runner with pay-per-request pricing. You only pay when the API receives traffic - no idle compute costs.

## Cost breakdown

| Resource | Cost |
|---|---|
| App Runner (pay-per-request) | $0 idle, ~$0.064/vCPU-hour when processing |
| ECR (image storage) | ~$0.10/month for one image |
| Secrets Manager (2 secrets) | ~$0.80/month |
| **Total when idle** | **~$1/month** |

App Runner's pay-per-request mode keeps a provisioned instance warm for routing but only charges for compute during actual requests. Cold starts are typically 2-5 seconds on first request after idle.

## Prerequisites

- AWS CLI v2 installed and configured (`aws configure`)
- Docker installed locally
- Your AWS account ID (run `aws sts get-caller-identity --query Account --output text`)

Set these variables in your terminal for the commands below:

```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export AWS_REGION=eu-central-1
```

---

## Step 1: Create ECR repository

```bash
aws ecr create-repository \
  --repository-name sage-api \
  --region $AWS_REGION \
  --image-scanning-configuration scanOnPush=true
```

## Step 2: Build and push the Docker image

```bash
# Authenticate Docker with ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push
docker build -t sage-api .
docker tag sage-api:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sage-api:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sage-api:latest
```

## Step 3: Store secrets in Secrets Manager

Store your API keys as secrets. App Runner will inject these as environment variables at runtime.

```bash
# OpenAI API key (skip if you only use Bedrock)
aws secretsmanager create-secret \
  --name sage/openai-api-key \
  --secret-string "sk-proj-your-openai-key-here" \
  --region $AWS_REGION

# SAGE API authentication keys (JSON map of key -> client name)
aws secretsmanager create-secret \
  --name sage/api-keys \
  --secret-string '{"sk-sage-your-key-here": "my-client"}' \
  --region $AWS_REGION
```

To update a secret later:

```bash
aws secretsmanager put-secret-value \
  --secret-id sage/api-keys \
  --secret-string '{"sk-sage-key1": "client-a", "sk-sage-key2": "client-b"}' \
  --region $AWS_REGION
```

## Step 4: Create IAM roles

App Runner needs two roles:

1. **Access role** - lets App Runner pull images from ECR
2. **Instance role** - lets the running container call Bedrock and read secrets

### 4a: ECR access role

```bash
# Create the trust policy
cat > /tmp/apprunner-trust.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "build.apprunner.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create role and attach ECR policy
aws iam create-role \
  --role-name sage-apprunner-ecr-access \
  --assume-role-policy-document file:///tmp/apprunner-trust.json

aws iam attach-role-policy \
  --role-name sage-apprunner-ecr-access \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
```

### 4b: Instance role (Bedrock + Secrets Manager)

```bash
# Create the trust policy
cat > /tmp/instance-trust.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "tasks.apprunner.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the permissions policy
cat > /tmp/sage-instance-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvoke",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    },
    {
      "Sid": "SecretsRead",
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:*:*:secret:sage/*"
    }
  ]
}
EOF

# Create role and attach policy
aws iam create-role \
  --role-name sage-apprunner-instance \
  --assume-role-policy-document file:///tmp/instance-trust.json

aws iam put-role-policy \
  --role-name sage-apprunner-instance \
  --policy-name sage-bedrock-secrets \
  --policy-document file:///tmp/sage-instance-policy.json
```

Wait about 10 seconds for IAM to propagate before creating the App Runner service.

## Step 5: Create the App Runner service

```bash
# Get the role ARNs
export ECR_ROLE_ARN=$(aws iam get-role --role-name sage-apprunner-ecr-access --query 'Role.Arn' --output text)
export INSTANCE_ROLE_ARN=$(aws iam get-role --role-name sage-apprunner-instance --query 'Role.Arn' --output text)

# Create the service configuration
cat > /tmp/sage-apprunner.json << EOF
{
  "ServiceName": "sage-api",
  "SourceConfiguration": {
    "AuthenticationConfiguration": {
      "AccessRoleArn": "$ECR_ROLE_ARN"
    },
    "AutoDeploymentsEnabled": false,
    "ImageRepository": {
      "ImageIdentifier": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sage-api:latest",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "AWS_REGION": "$AWS_REGION",
          "DEFAULT_GENERATION_PROVIDER": "bedrock",
          "DEFAULT_GENERATION_MODEL": "eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
          "DEFAULT_EMBEDDING_PROVIDER": "bedrock",
          "DEFAULT_EMBEDDING_MODEL": "amazon.titan-embed-text-v2:0",
          "DEFAULT_VISION_PROVIDER": "bedrock",
          "DEFAULT_VISION_MODEL": "eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
          "DEFAULT_VIDEO_PROVIDER": "bedrock",
          "DEFAULT_VIDEO_MODEL": "eu.twelvelabs.pegasus-1-2-v1:0",
          "DEFAULT_TEMPERATURE": "0.7",
          "BATCH_SIZE": "10",
          "CONCURRENCY_LIMIT": "20"
        },
        "RuntimeEnvironmentSecrets": {
          "OPENAI_API_KEY": "arn:aws:secretsmanager:$AWS_REGION:$AWS_ACCOUNT_ID:secret:sage/openai-api-key",
          "SAGE_API_KEYS": "arn:aws:secretsmanager:$AWS_REGION:$AWS_ACCOUNT_ID:secret:sage/api-keys"
        }
      }
    }
  },
  "InstanceConfiguration": {
    "Cpu": "0.25 vCPU",
    "Memory": "0.5 GB",
    "InstanceRoleArn": "$INSTANCE_ROLE_ARN"
  },
  "HealthCheckConfiguration": {
    "Protocol": "HTTP",
    "Path": "/health",
    "Interval": 20,
    "Timeout": 5,
    "HealthyThreshold": 1,
    "UnhealthyThreshold": 5
  }
}
EOF

# Create the service
aws apprunner create-service \
  --cli-input-json file:///tmp/sage-apprunner.json \
  --region $AWS_REGION
```

This takes 2-5 minutes. Check the status:

```bash
aws apprunner list-services --region $AWS_REGION \
  --query 'ServiceSummaryList[?ServiceName==`sage-api`].{Status:Status,Url:ServiceUrl}' \
  --output table
```

Wait until Status shows `RUNNING`.

> **Note on secrets ARNs:** Secrets Manager appends a random 6-character suffix to secret ARNs.
> If the create-service command fails with an error about secret ARNs, list your actual ARNs:
> ```bash
> aws secretsmanager list-secrets --region $AWS_REGION \
>   --query 'SecretList[?starts_with(Name,`sage/`)].ARN' --output text
> ```
> Then update the `RuntimeEnvironmentSecrets` values in the JSON with the full ARNs.

## Step 6: Verify the deployment

```bash
# Get the service URL
export SAGE_URL=$(aws apprunner list-services --region $AWS_REGION \
  --query 'ServiceSummaryList[?ServiceName==`sage-api`].ServiceUrl' \
  --output text)

# Health check (no auth required)
curl https://$SAGE_URL/health

# API info (requires auth if SAGE_API_KEYS is set)
curl https://$SAGE_URL/api/v1/info \
  -H "Authorization: Bearer sk-sage-your-key-here"

# List models
curl https://$SAGE_URL/api/v1/models \
  -H "Authorization: Bearer sk-sage-your-key-here"
```

---

## Deploying updates

After making code changes, build and push a new image, then trigger a deployment:

```bash
# Build and push
docker build -t sage-api .
docker tag sage-api:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sage-api:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sage-api:latest

# Get the service ARN
export SERVICE_ARN=$(aws apprunner list-services --region $AWS_REGION \
  --query 'ServiceSummaryList[?ServiceName==`sage-api`].ServiceArn' \
  --output text)

# Trigger redeployment
aws apprunner start-deployment --service-arn $SERVICE_ARN --region $AWS_REGION
```

## Scaling up if needed

The default 0.25 vCPU / 0.5 GB is fine for light usage. If you hit timeouts on large requests (many personas, video processing), scale up:

```bash
aws apprunner update-service \
  --service-arn $SERVICE_ARN \
  --instance-configuration '{"Cpu": "1 vCPU", "Memory": "2 GB"}' \
  --region $AWS_REGION
```

## Tearing it all down

```bash
# Delete App Runner service
aws apprunner delete-service --service-arn $SERVICE_ARN --region $AWS_REGION

# Delete secrets
aws secretsmanager delete-secret --secret-id sage/openai-api-key --force-delete-without-recovery --region $AWS_REGION
aws secretsmanager delete-secret --secret-id sage/api-keys --force-delete-without-recovery --region $AWS_REGION

# Delete ECR repository
aws ecr delete-repository --repository-name sage-api --force --region $AWS_REGION

# Delete IAM roles
aws iam delete-role-policy --role-name sage-apprunner-instance --policy-name sage-bedrock-secrets
aws iam detach-role-policy --role-name sage-apprunner-ecr-access --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
aws iam delete-role --role-name sage-apprunner-instance
aws iam delete-role --role-name sage-apprunner-ecr-access
```
