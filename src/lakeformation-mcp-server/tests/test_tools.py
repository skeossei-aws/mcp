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

"""Tests for Lake Formation MCP Server tools."""

import pytest
from awslabs.lakeformation_mcp_server.models import (
    DataLakeSettings,
    PermissionList,
    RegisteredResource,
    RegisteredResourceList,
)
from awslabs.lakeformation_mcp_server.tools.data_lake_settings_tool import get_data_lake_settings
from awslabs.lakeformation_mcp_server.tools.permissions_tool import list_permissions
from awslabs.lakeformation_mcp_server.tools.registered_resources_tool import (
    describe_resource,
    list_resources,
)
from unittest.mock import AsyncMock, Mock, patch


@pytest.fixture
def mock_ctx():
    """Create a mock MCP Context."""
    ctx = Mock()
    ctx.error = AsyncMock()
    return ctx


class TestGetDataLakeSettings:
    """Test get_data_lake_settings tool."""

    @patch(
        'awslabs.lakeformation_mcp_server.tools.data_lake_settings_tool.get_lakeformation_client'
    )
    async def test_basic_call(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.get_data_lake_settings.return_value = {
            'DataLakeSettings': {
                'DataLakeAdmins': [
                    {'DataLakePrincipalIdentifier': 'arn:aws:iam::123456789012:user/admin'}
                ],
                'CreateDatabaseDefaultPermissions': [],
                'CreateTableDefaultPermissions': [],
            }
        }
        mock_get_client.return_value = mock_client

        result = await get_data_lake_settings(ctx=mock_ctx, catalog_id=None, region=None)

        assert isinstance(result, DataLakeSettings)
        assert len(result.data_lake_admins) == 1
        mock_client.get_data_lake_settings.assert_called_once_with()

    @patch(
        'awslabs.lakeformation_mcp_server.tools.data_lake_settings_tool.get_lakeformation_client'
    )
    async def test_with_catalog_id(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.get_data_lake_settings.return_value = {'DataLakeSettings': {}}
        mock_get_client.return_value = mock_client

        await get_data_lake_settings(ctx=mock_ctx, catalog_id='123456789012')

        mock_client.get_data_lake_settings.assert_called_once_with(CatalogId='123456789012')

    @patch(
        'awslabs.lakeformation_mcp_server.tools.data_lake_settings_tool.get_lakeformation_client'
    )
    async def test_error_handling(self, mock_get_client, mock_ctx):
        mock_get_client.side_effect = Exception('Access denied')

        with pytest.raises(Exception, match='Access denied'):
            await get_data_lake_settings(ctx=mock_ctx, catalog_id=None, region=None)


class TestListResources:
    """Test list_resources tool."""

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_basic_call(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_resources.return_value = {
            'ResourceInfoList': [
                {
                    'ResourceArn': 'arn:aws:s3:::my-bucket',
                    'RoleArn': 'arn:aws:iam::123456789012:role/LFRole',
                    'WithFederation': False,
                    'HybridAccessEnabled': False,
                }
            ],
        }
        mock_get_client.return_value = mock_client

        result = await list_resources(ctx=mock_ctx, max_results=None, next_token=None, region=None)

        assert isinstance(result, RegisteredResourceList)
        assert len(result.resources) == 1
        assert result.resources[0].resource_arn == 'arn:aws:s3:::my-bucket'

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_with_pagination(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_resources.return_value = {
            'ResourceInfoList': [],
            'NextToken': 'token123',
        }
        mock_get_client.return_value = mock_client

        result = await list_resources(ctx=mock_ctx, max_results=10, next_token=None, region=None)

        assert result.next_token == 'token123'

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_empty_response(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_resources.return_value = {'ResourceInfoList': []}
        mock_get_client.return_value = mock_client

        result = await list_resources(ctx=mock_ctx, max_results=None, next_token=None, region=None)

        assert result.resources == []
        assert result.next_token is None


class TestDescribeResource:
    """Test describe_resource tool."""

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_basic_call(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.describe_resource.return_value = {
            'ResourceInfo': {
                'ResourceArn': 'arn:aws:s3:::my-bucket',
                'RoleArn': 'arn:aws:iam::123456789012:role/LFRole',
                'WithFederation': True,
                'HybridAccessEnabled': False,
                'VerificationStatus': 'VERIFIED',
            }
        }
        mock_get_client.return_value = mock_client

        result = await describe_resource(ctx=mock_ctx, resource_arn='arn:aws:s3:::my-bucket')

        assert isinstance(result, RegisteredResource)
        assert result.resource_arn == 'arn:aws:s3:::my-bucket'
        assert result.verification_status == 'VERIFIED'
        assert result.with_federation is True

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_error_handling(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.describe_resource.side_effect = Exception('Resource not found')
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match='Resource not found'):
            await describe_resource(ctx=mock_ctx, resource_arn='arn:aws:s3:::nonexistent')


class TestListPermissions:
    """Test list_permissions tool."""

    @patch('awslabs.lakeformation_mcp_server.tools.permissions_tool.get_lakeformation_client')
    async def test_basic_call(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_permissions.return_value = {
            'PrincipalResourcePermissions': [
                {
                    'Principal': {
                        'DataLakePrincipal': {
                            'DataLakePrincipalIdentifier': 'arn:aws:iam::123456789012:role/Analyst'
                        }
                    },
                    'Resource': {'Database': {'Name': 'mydb'}},
                    'Permissions': ['SELECT', 'DESCRIBE'],
                    'PermissionsWithGrantOption': [],
                }
            ],
        }
        mock_get_client.return_value = mock_client

        result = await list_permissions(
            ctx=mock_ctx,
            catalog_id=None,
            principal=None,
            resource_type=None,
            max_results=None,
            next_token=None,
            region=None,
        )

        assert isinstance(result, PermissionList)
        assert len(result.permissions) == 1
        assert result.permissions[0].permissions == ['SELECT', 'DESCRIBE']

    @patch('awslabs.lakeformation_mcp_server.tools.permissions_tool.get_lakeformation_client')
    async def test_with_filters(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_permissions.return_value = {'PrincipalResourcePermissions': []}
        mock_get_client.return_value = mock_client

        await list_permissions(
            ctx=mock_ctx,
            principal='arn:aws:iam::123456789012:role/Analyst',
            resource_type='DATABASE',
        )

        call_args = mock_client.list_permissions.call_args[1]
        assert call_args['Principal'] == {
            'DataLakePrincipal': {
                'DataLakePrincipalIdentifier': 'arn:aws:iam::123456789012:role/Analyst'
            }
        }
        assert call_args['ResourceType'] == 'DATABASE'

    @patch('awslabs.lakeformation_mcp_server.tools.permissions_tool.get_lakeformation_client')
    async def test_with_pagination(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_permissions.return_value = {
            'PrincipalResourcePermissions': [],
            'NextToken': 'page2',
        }
        mock_get_client.return_value = mock_client

        result = await list_permissions(ctx=mock_ctx, max_results=5, next_token='page1')

        assert result.next_token == 'page2'
        call_args = mock_client.list_permissions.call_args[1]
        assert call_args['MaxResults'] == 5
        assert call_args['NextToken'] == 'page1'


class TestServerImport:
    """Test server module can be imported."""

    def test_server_import(self):
        from awslabs.lakeformation_mcp_server import server

        assert server is not None
        assert server.mcp is not None

    def test_main_function(self):
        from awslabs.lakeformation_mcp_server.server import main
        from unittest.mock import patch as mock_patch

        with mock_patch('awslabs.lakeformation_mcp_server.server.mcp') as mock_mcp:
            main()
            mock_mcp.run.assert_called_once()


class TestListResourcesNextToken:
    """Test list_resources with next_token parameter."""

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_with_next_token(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_resources.return_value = {'ResourceInfoList': []}
        mock_get_client.return_value = mock_client

        await list_resources(ctx=mock_ctx, max_results=None, next_token='abc123', region=None)

        mock_client.list_resources.assert_called_once_with(NextToken='abc123')

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_list_resources_api_error(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_resources.side_effect = Exception('ServiceUnavailable')
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match='ServiceUnavailable'):
            await list_resources(ctx=mock_ctx, max_results=None, next_token=None, region=None)


class TestDescribeResourceError:
    """Test describe_resource error path."""

    @patch(
        'awslabs.lakeformation_mcp_server.tools.registered_resources_tool.get_lakeformation_client'
    )
    async def test_describe_resource_api_error(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.describe_resource.side_effect = Exception('InvalidInputException')
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match='InvalidInputException'):
            await describe_resource(
                ctx=mock_ctx, resource_arn='arn:aws:s3:::bad-bucket', region=None
            )


class TestListPermissionsError:
    """Test list_permissions error path."""

    @patch('awslabs.lakeformation_mcp_server.tools.permissions_tool.get_lakeformation_client')
    async def test_list_permissions_api_error(self, mock_get_client, mock_ctx):
        mock_client = Mock()
        mock_client.list_permissions.side_effect = Exception('AccessDeniedException')
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match='AccessDeniedException'):
            await list_permissions(
                ctx=mock_ctx,
                catalog_id=None,
                principal=None,
                resource_type=None,
                max_results=None,
                next_token=None,
                region=None,
            )
