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

"""Tests for Lake Formation MCP Server models."""

import pytest
from awslabs.lakeformation_mcp_server.models import (
    DataLakePrincipal,
    DataLakeSettings,
    Permission,
    PermissionList,
    PrincipalPermissions,
    RegisteredResource,
    RegisteredResourceList,
)


class TestDataLakePrincipal:
    """Test DataLakePrincipal model."""

    def test_valid_principal(self):
        p = DataLakePrincipal(
            data_lake_principal_identifier='arn:aws:iam::123456789012:role/Admin'
        )
        assert p.data_lake_principal_identifier == 'arn:aws:iam::123456789012:role/Admin'

    def test_missing_identifier_raises(self):
        with pytest.raises(Exception):
            DataLakePrincipal()


class TestPrincipalPermissions:
    """Test PrincipalPermissions model."""

    def test_with_principal_and_permissions(self):
        pp = PrincipalPermissions(
            principal=DataLakePrincipal(data_lake_principal_identifier='IAM_ALLOWED_PRINCIPALS'),
            permissions=['ALL'],
        )
        assert pp.principal.data_lake_principal_identifier == 'IAM_ALLOWED_PRINCIPALS'
        assert pp.permissions == ['ALL']

    def test_defaults(self):
        pp = PrincipalPermissions()
        assert pp.principal is None
        assert pp.permissions == []


class TestDataLakeSettings:
    """Test DataLakeSettings model."""

    def test_defaults(self):
        settings = DataLakeSettings()
        assert settings.data_lake_admins == []
        assert settings.read_only_admins == []
        assert settings.create_database_default_permissions == []
        assert settings.create_table_default_permissions == []
        assert settings.trusted_resource_owners == []
        assert settings.allow_external_data_filtering is False
        assert settings.allow_full_table_external_data_access is False
        assert settings.external_data_filtering_allow_list == []
        assert settings.authorized_session_tag_value_list == []
        assert settings.parameters == {}

    def test_with_admins(self):
        settings = DataLakeSettings(
            data_lake_admins=[
                DataLakePrincipal(
                    data_lake_principal_identifier='arn:aws:iam::123456789012:user/admin'
                )
            ],
        )
        assert len(settings.data_lake_admins) == 1
        assert (
            settings.data_lake_admins[0].data_lake_principal_identifier
            == 'arn:aws:iam::123456789012:user/admin'
        )

    def test_json_serialization(self):
        settings = DataLakeSettings(
            data_lake_admins=[
                DataLakePrincipal(
                    data_lake_principal_identifier='arn:aws:iam::123456789012:user/admin'
                )
            ],
            allow_external_data_filtering=True,
            parameters={'CROSS_ACCOUNT_VERSION': '3'},
        )
        json_data = settings.model_dump(mode='json')
        assert json_data['allow_external_data_filtering'] is True
        assert json_data['parameters']['CROSS_ACCOUNT_VERSION'] == '3'
        assert len(json_data['data_lake_admins']) == 1


class TestRegisteredResource:
    """Test RegisteredResource model."""

    def test_minimal(self):
        r = RegisteredResource(resource_arn='arn:aws:s3:::my-bucket')
        assert r.resource_arn == 'arn:aws:s3:::my-bucket'
        assert r.role_arn is None
        assert r.last_modified is None
        assert r.with_federation is False
        assert r.hybrid_access_enabled is False
        assert r.with_privileged_access is False
        assert r.verification_status is None
        assert r.expected_resource_owner_account is None

    def test_full(self):
        r = RegisteredResource(
            resource_arn='arn:aws:s3:::my-bucket',
            role_arn='arn:aws:iam::123456789012:role/LFRole',
            last_modified='2024-01-01T00:00:00',
            with_federation=True,
            hybrid_access_enabled=True,
            with_privileged_access=False,
            verification_status='VERIFIED',
            expected_resource_owner_account='123456789012',
        )
        assert r.verification_status == 'VERIFIED'
        assert r.with_federation is True

    def test_missing_arn_raises(self):
        with pytest.raises(Exception):
            RegisteredResource()


class TestRegisteredResourceList:
    """Test RegisteredResourceList model."""

    def test_empty(self):
        rl = RegisteredResourceList()
        assert rl.resources == []
        assert rl.next_token is None

    def test_with_resources(self):
        rl = RegisteredResourceList(
            resources=[RegisteredResource(resource_arn='arn:aws:s3:::bucket1')],
            next_token='token123',
        )
        assert len(rl.resources) == 1
        assert rl.next_token == 'token123'


class TestPermission:
    """Test Permission model."""

    def test_defaults(self):
        p = Permission()
        assert p.principal is None
        assert p.resource == {}
        assert p.permissions == []
        assert p.permissions_with_grant_option == []

    def test_with_data(self):
        p = Permission(
            principal=DataLakePrincipal(
                data_lake_principal_identifier='arn:aws:iam::123456789012:role/Analyst'
            ),
            resource={'Database': {'Name': 'mydb'}},
            permissions=['SELECT', 'DESCRIBE'],
            permissions_with_grant_option=['SELECT'],
        )
        assert p.permissions == ['SELECT', 'DESCRIBE']
        assert p.permissions_with_grant_option == ['SELECT']


class TestPermissionList:
    """Test PermissionList model."""

    def test_empty(self):
        pl = PermissionList()
        assert pl.permissions == []
        assert pl.next_token is None

    def test_with_permissions(self):
        pl = PermissionList(
            permissions=[Permission(permissions=['ALL'])],
            next_token='next',
        )
        assert len(pl.permissions) == 1
        assert pl.next_token == 'next'
