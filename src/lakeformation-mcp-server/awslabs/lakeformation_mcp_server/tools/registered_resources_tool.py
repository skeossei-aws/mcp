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

"""Resource tools for Lake Formation MCP Server."""

from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client
from awslabs.lakeformation_mcp_server.models import RegisteredResource, RegisteredResourceList
from loguru import logger
from mcp.server.fastmcp import Context
from pydantic import Field
from typing import Optional


async def list_resources(
    ctx: Context,
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
) -> RegisteredResourceList:
    """List all resources (S3 locations) registered with Lake Formation.

    Use this tool to discover which S3 locations are managed by Lake Formation
    and what IAM roles are used to access them.

    ## When to use:
    - To see all S3 locations registered with Lake Formation
    - To find the IAM role associated with a registered location
    - To check federation and hybrid access settings across resources
    - To verify resource registration status

    ## Output:
    Returns a list of registered resources, each containing the
    resource ARN, role ARN, federation settings, and verification status.
    Results may be paginated — use next_token to retrieve more.
    """
    try:
        client = get_lakeformation_client(region)
        params = {}
        if max_results:
            params['MaxResults'] = max_results
        if next_token:
            params['NextToken'] = next_token

        response = client.list_resources(**params)
        resources = []
        for r in response.get('ResourceInfoList', []):
            resources.append(
                RegisteredResource(
                    resource_arn=r.get('ResourceArn', ''),
                    role_arn=r.get('RoleArn'),
                    last_modified=str(r['LastModified']) if r.get('LastModified') else None,
                    with_federation=r.get('WithFederation', False),
                    hybrid_access_enabled=r.get('HybridAccessEnabled', False),
                    with_privileged_access=r.get('WithPrivilegedAccess', False),
                    verification_status=r.get('VerificationStatus'),
                    expected_resource_owner_account=r.get('ExpectedResourceOwnerAccount'),
                )
            )

        return RegisteredResourceList(resources=resources, next_token=response.get('NextToken'))
    except Exception as e:
        logger.error(f'Error listing resources: {e}')
        await ctx.error(f'Error listing resources: {e}')
        raise


async def describe_resource(
    ctx: Context,
    resource_arn: str = Field(
        default=...,
        min_length=1,
        pattern=r'^arn:(aws|aws-cn|aws-us-gov):(s3|redshift|cloudtrail|glue|s3tables):.+',
        description='The ARN of the resource to describe. Supported types: S3, Redshift, CloudTrail, Glue Connection, S3 Table Bucket.',
    ),
    region: Optional[str] = Field(
        default=None,
        min_length=1,
        description='AWS region. Defaults to AWS_REGION env var or us-east-1.',
    ),
) -> RegisteredResource:
    """Get details about a specific resource registered with Lake Formation.

    Use this tool to inspect a single registered resource by its ARN, such as
    an S3 location, to see its IAM role, federation, and verification status.

    ## When to use:
    - To check the IAM role associated with a specific S3 location
    - To verify whether a resource's role has sufficient permissions (verification status)
    - To check federation or hybrid access settings on a specific resource
    - After list_resources, to get full details on a specific resource

    ## Output:
    Returns the resource ARN, role ARN, last modified time,
    federation settings, hybrid access, verification status, and owner account.
    """
    try:
        client = get_lakeformation_client(region)
        response = client.describe_resource(ResourceArn=resource_arn)
        r = response.get('ResourceInfo', {})
        return RegisteredResource(
            resource_arn=r.get('ResourceArn', ''),
            role_arn=r.get('RoleArn'),
            last_modified=str(r['LastModified']) if r.get('LastModified') else None,
            with_federation=r.get('WithFederation', False),
            hybrid_access_enabled=r.get('HybridAccessEnabled', False),
            with_privileged_access=r.get('WithPrivilegedAccess', False),
            verification_status=r.get('VerificationStatus'),
            expected_resource_owner_account=r.get('ExpectedResourceOwnerAccount'),
        )
    except Exception as e:
        logger.error(f'Error describing resource: {e}')
        await ctx.error(f'Error describing resource: {e}')
        raise
