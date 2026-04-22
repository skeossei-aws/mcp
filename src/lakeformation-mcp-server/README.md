# AWS Labs Lake Formation MCP Server

This AWS Labs Model Context Protocol (MCP) server for Lake Formation enables your AI agents to inspect AWS Lake Formation configuration. It provides read-only access to data lake settings, registered resources, and permissions, allowing agents to audit data lake access, verify resource registration, and troubleshoot permission issues.

## Features

**Data Lake Settings** - Retrieve data lake administrators, default permissions for new databases and tables, EMR data filtering configuration, and other data lake settings.

**Resource Management** - List and describe resources (S3 locations, Redshift, CloudTrail, Glue connections) registered with Lake Formation, including their IAM roles, federation settings, and verification status.

**Permission Auditing** - List permissions granted on data lake resources, filtered by principal (IAM user/role) or resource type (DATABASE, TABLE, etc.) for access auditing and troubleshooting.

## Prerequisites

1. An AWS account with [Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html) configured.
2. This MCP server can only be run locally on the same host as your LLM client.
3. Set up AWS credentials with access to AWS services:
   - You need an AWS account with appropriate permissions (see required permissions below)
   - Configure AWS credentials with `aws configure` or environment variables

## Available Tools

- `get_data_lake_settings` - Retrieve data lake administrators, default permissions, and configuration settings
- `list_resources` - List all S3 locations and other resources registered with Lake Formation
- `describe_resource` - Get details about a specific registered resource by ARN
- `list_permissions` - List permissions granted on data lake resources, with optional filtering

### Required IAM Permissions

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lakeformation:GetDataLakeSettings",
                "lakeformation:ListResources",
                "lakeformation:DescribeResource",
                "lakeformation:ListPermissions"
            ],
            "Resource": "*"
        }
    ]
}
```

## Installation

### Prerequisites

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/)
2. Install Python using `uv python install 3.10`

### MCP Config (Kiro, Cline)

```json
{
    "mcpServers": {
        "awslabs.lakeformation-mcp-server": {
            "command": "uvx",
            "args": ["awslabs.lakeformation-mcp-server@latest"],
            "env": {
                "AWS_PROFILE": "your-aws-profile",
                "AWS_REGION": "us-east-1",
                "FASTMCP_LOG_LEVEL": "ERROR"
            }
        }
    }
}
```

### Cursor Config

```json
{
    "command": "uvx",
    "args": ["awslabs.lakeformation-mcp-server@latest"],
    "env": {
        "AWS_PROFILE": "your-aws-profile",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
    }
}
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `AWS_PROFILE` | AWS profile name for credentials | Default credential chain |
| `AWS_REGION` | AWS region for API calls | `us-east-1` |
| `FASTMCP_LOG_LEVEL` | Log level (DEBUG, INFO, WARNING, ERROR) | `WARNING` |

## Development

```bash
cd src/lakeformation-mcp-server
uv sync
uv run pytest --cov --cov-branch -v
```

### Running the Inspector

```bash
uv run mcp dev awslabs/lakeformation_mcp_server/server.py
```
