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

"""Tests for Lake Formation MCP Server client."""

import pytest
from unittest.mock import Mock, patch


class TestGetLakeFormationClient:
    """Test get_lakeformation_client function."""

    @patch('boto3.Session')
    def test_default_region(self, mock_session):
        from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client

        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client

        with patch.dict('os.environ', {}, clear=True):
            result = get_lakeformation_client()

        assert result == mock_client
        mock_session.assert_called_once_with(region_name='us-east-1')

    @patch('boto3.Session')
    def test_custom_region(self, mock_session):
        from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client

        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client

        result = get_lakeformation_client(region='eu-west-1')

        assert result == mock_client
        mock_session.assert_called_once_with(region_name='eu-west-1')

    @patch('boto3.Session')
    def test_region_from_env(self, mock_session):
        from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client

        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client

        with patch.dict('os.environ', {'AWS_REGION': 'ap-southeast-1'}):
            result = get_lakeformation_client()

        assert result == mock_client
        mock_session.assert_called_once_with(region_name='ap-southeast-1')

    @patch('boto3.Session')
    def test_with_aws_profile(self, mock_session):
        from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client

        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client

        with patch.dict('os.environ', {'AWS_PROFILE': 'test-profile'}):
            result = get_lakeformation_client(region='eu-west-1')

        assert result == mock_client
        mock_session.assert_called_once_with(profile_name='test-profile', region_name='eu-west-1')

    @patch('boto3.Session')
    def test_user_agent_is_set(self, mock_session):
        from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client

        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client

        get_lakeformation_client()

        call_args = mock_session.return_value.client.call_args
        assert call_args[0][0] == 'lakeformation'
        config = call_args[1]['config']
        assert 'awslabs#mcp#lakeformation-mcp-server' in config.user_agent_extra

    @patch('boto3.Session')
    def test_error_handling(self, mock_session):
        from awslabs.lakeformation_mcp_server.lakeformation_client import get_lakeformation_client

        mock_session.side_effect = Exception('Credentials error')

        with pytest.raises(Exception, match='Credentials error'):
            get_lakeformation_client()
