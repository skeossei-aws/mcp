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

"""get_data_lake_settings tool for Lake Formation MCP Server."""

from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client
from awslabs.lakeformation_mcp_server.models import DataLakeSettings
from loguru import logger
from mcp.server.fastmcp import Context
from pydantic import Field
from typing import Optional


async def get_data_lake_settings(
    ctx: Context,
    catalog_id: Optional[str] = Field(
        default=None,
        min_length=12,
        max_length=12,
        pattern=r'^\d{12}$',
        description='AWS account ID of the data lake (12-digit number). Defaults to the caller account.',
    ),
    region: Optional[str] = Field(
        default=None,
        min_length=1,
        description='AWS region. Defaults to AWS_REGION env var or us-east-1.',
    ),
) -> DataLakeSettings:
    """Retrieve AWS Lake Formation data lake settings.

    Use this tool to inspect the configuration of a Lake Formation data lake,
    including who the administrators are and what default permissions are applied
    to newly created databases and tables.

    ## When to use:
    - To find out who the data lake administrators are
    - To check default permission settings for new databases and tables
    - To verify external data filtering and EMR access configuration
    - To audit read-only admin assignments

    ## Output:
    Returns data lake admins, default permissions, trusted resource
    owners, external filtering settings, and configuration parameters.
    """
    try:
        client = get_lakeformation_client(region)
        params = {}
        if catalog_id:
            params['CatalogId'] = catalog_id

        response = client.get_data_lake_settings(**params)
        settings = response.get('DataLakeSettings', {})

        return DataLakeSettings(**settings)
    except Exception as e:
        logger.error(f'Error getting data lake settings: {e}')
        await ctx.error(f'Error getting data lake settings: {e}')
        raise
