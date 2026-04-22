# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""awslabs Lake Formation MCP Server implementation."""

from awslabs.lakeformation_mcp_server.tools import register_tools
from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    'awslabs.lakeformation-mcp-server',
    instructions="""
# AWS Lake Formation MCP Server

This MCP server provides read-only tools for inspecting AWS Lake Formation data lake configuration.

## Available Tools

### get_data_lake_settings
Retrieve data lake administrators, default permissions for new databases and tables,
EMR data filtering configuration, and other data lake settings.
Use when you need to inspect who manages the data lake or audit admin assignments.

### list_resources
List all resources (S3 locations, Redshift, CloudTrail, Glue connections) registered
with Lake Formation. Returns IAM roles, federation settings, and verification status.
Supports pagination via next_token.

### describe_resource
Get details about a specific registered resource by ARN.
Use after list_resources to inspect a particular resource's configuration.

### list_permissions
List permissions granted on data lake resources. Filter by principal (IAM ARN)
or resource_type (DATABASE, TABLE, CATALOG, DATA_LOCATION, LF_TAG, LF_TAG_POLICY).
Use when auditing access or troubleshooting permission denied errors.
Supports pagination via next_token.

## Usage Tips
- All tools are read-only and will not modify any resources.
- Use list_resources first to discover ARNs, then describe_resource for details.
- Use list_permissions with a principal filter to check a specific user or role's access.
- Results may be paginated — check for next_token in responses.
""",
    dependencies=['boto3', 'botocore', 'pydantic', 'loguru'],
)

register_tools(mcp)


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == '__main__':
    main()
