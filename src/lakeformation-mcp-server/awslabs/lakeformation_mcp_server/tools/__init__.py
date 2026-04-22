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

"""Lake Formation MCP Server tools."""

import textwrap

from mcp.types import ToolAnnotations


READONLY_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)


def _desc(text: str) -> str:
    """Clean up a multi-line description string."""
    return textwrap.dedent(text).strip()


def register_tools(mcp):
    """Register all Lake Formation tools with the MCP server."""
    from awslabs.lakeformation_mcp_server.tools.data_lake_settings_tool import (
        get_data_lake_settings,
    )
    from awslabs.lakeformation_mcp_server.tools.permissions_tool import list_permissions
    from awslabs.lakeformation_mcp_server.tools.registered_resources_tool import (
        describe_resource,
        list_resources,
    )

    mcp.tool(
        name='get_data_lake_settings',
        description=_desc("""
            Retrieves the list of the data lake administrators of a Lake Formation-managed
            data lake, along with default permissions for newly created databases and tables,
            and EMR data filtering configuration.

            Use when you need to inspect who manages the data lake, audit admin assignments,
            or check how new resources are configured by default.
        """),
        annotations=READONLY_ANNOTATIONS,
    )(get_data_lake_settings)

    mcp.tool(
        name='list_resources',
        description=_desc("""
            Lists the resources (S3 locations) registered to be managed by the Data Catalog.

            Use when you need to discover which data locations are under Lake Formation control,
            check their IAM roles, or verify federation and hybrid access settings.
            Results may be paginated.
        """),
        annotations=READONLY_ANNOTATIONS,
    )(list_resources)

    mcp.tool(
        name='describe_resource',
        description=_desc("""
            Retrieves the current data access role and configuration for a given resource
            registered in Lake Formation. Requires the resource ARN.

            Use when you need details about a specific registered S3 location, including its
            IAM role, verification status, and federation settings.
            Use list_resources first if you need to find the ARN.
        """),
        annotations=READONLY_ANNOTATIONS,
    )(describe_resource)

    mcp.tool(
        name='list_permissions',
        description=_desc("""
            Returns a list of the principal permissions on Lake Formation resources,
            filtered by the permissions of the caller.

            Use when you need to audit who has access to specific databases, tables, or
            S3 locations, check what permissions a specific IAM user or role has been granted,
            or troubleshoot access denied errors.
            Filter by principal (IAM ARN) or resource_type (DATABASE, TABLE, etc.) to narrow results.
        """),
        annotations=READONLY_ANNOTATIONS,
    )(list_permissions)
