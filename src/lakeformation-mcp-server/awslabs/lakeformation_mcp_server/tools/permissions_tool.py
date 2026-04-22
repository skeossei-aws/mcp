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

"""Permissions tool for Lake Formation MCP Server."""

from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client
from awslabs.lakeformation_mcp_server.models import Permission, PermissionList
from loguru import logger
from mcp.server.fastmcp import Context
from pydantic import Field
from typing import Optional


async def list_permissions(
    ctx: Context,
    catalog_id: Optional[str] = Field(
        default=None,
        min_length=12,
        max_length=12,
        pattern=r'^\d{12}$',
        description='AWS account ID of the data lake (12-digit number). Defaults to the caller account.',
    ),
    principal: Optional[str] = Field(
        default=None,
        min_length=1,
        description='IAM ARN of the principal to filter permissions for.',
    ),
    resource_type: Optional[str] = Field(
        default=None,
        min_length=1,
        description=(
            'Resource type to filter by: CATALOG, DATABASE, TABLE, '
            'DATA_LOCATION, LF_TAG, LF_TAG_POLICY, LF_TAG_POLICY_DATABASE, '
            'or LF_TAG_POLICY_TABLE.'
        ),
    ),
    max_results: Optional[int] = Field(
        default=None,
        ge=1,
        le=1000,
        description='Maximum number of results to return (1-1000).',
    ),
    next_token: Optional[str] = Field(
        default=None,
        min_length=1,
        description='Pagination token from a previous response.',
    ),
    region: Optional[str] = Field(
        default=None,
        min_length=1,
        description='AWS region. Defaults to AWS_REGION env var or us-east-1.',
    ),
) -> PermissionList:
    """List Lake Formation permissions on data lake resources.

    Use this tool to inspect who has access to what in your data lake. Returns
    permissions granted to principals (IAM users/roles) on Lake Formation resources.

    ## When to use:
    - To audit who has access to specific databases, tables, or S3 locations
    - To check what permissions a specific IAM user or role has been granted
    - To list all permissions of a certain resource type (e.g., all TABLE permissions)
    - To troubleshoot access denied errors by checking granted permissions

    ## Usage Tips:
    - Filter by principal to see all permissions for a specific user/role
    - Filter by resource_type to narrow results to a specific resource category
    - Results may be paginated — use next_token to retrieve more
    - Combine filters for targeted queries (e.g., principal + resource_type)

    ## Output:
    Returns a list of permission entries, each containing the
    principal, resource, granted permissions, and grantable permissions.
    """
    try:
        client = get_lakeformation_client(region)
        params = {}
        if catalog_id:
            params['CatalogId'] = catalog_id
        if principal:
            params['Principal'] = {'DataLakePrincipal': {'DataLakePrincipalIdentifier': principal}}
        if resource_type:
            params['ResourceType'] = resource_type
        if max_results:
            params['MaxResults'] = max_results
        if next_token:
            params['NextToken'] = next_token

        response = client.list_permissions(**params)
        permissions = []
        for p in response.get('PrincipalResourcePermissions', []):
            permissions.append(
                Permission(
                    principal=p.get('Principal', {}).get('DataLakePrincipal'),
                    resource=p.get('Resource', {}),
                    permissions=p.get('Permissions', []),
                    permissions_with_grant_option=p.get('PermissionsWithGrantOption', []),
                )
            )
        return PermissionList(
            permissions=permissions,
            next_token=response.get('NextToken'),
        )
    except Exception as e:
        logger.error(f'Error listing permissions: {e}')
        await ctx.error(f'Error listing permissions: {e}')
        raise
