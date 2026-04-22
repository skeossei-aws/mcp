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

"""Pydantic models for Lake Formation Data Lake Settings."""

from awslabs.lakeformation_mcp_server.models.common import DataLakePrincipal
from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, List, Optional


class PrincipalPermissions(BaseModel):
    """Permissions granted to a principal."""

    model_config = ConfigDict(populate_by_name=True)

    principal: Optional[DataLakePrincipal] = Field(
        default=None, alias='Principal', description='The principal who is granted permissions.'
    )
    permissions: List[str] = Field(
        default_factory=list,
        alias='Permissions',
        description='The permissions that are granted to the principal.',
    )


class DataLakeSettings(BaseModel):
    """Data Lake Settings Model."""

    model_config = ConfigDict(populate_by_name=True)

    data_lake_admins: List[DataLakePrincipal] = Field(
        default_factory=list,
        alias='DataLakeAdmins',
        description='A list of Lake Formation principals (IAM users or roles) designated as data lake administrators.',
    )
    read_only_admins: List[DataLakePrincipal] = Field(
        default_factory=list,
        alias='ReadOnlyAdmins',
        description='A list of Lake Formation principals with only view access to the resources, without the ability to make changes.',
    )
    create_database_default_permissions: List[PrincipalPermissions] = Field(
        default_factory=list,
        alias='CreateDatabaseDefaultPermissions',
        description='Specifies whether access control on newly created database is managed by Lake Formation permissions or exclusively by IAM permissions.',
    )
    create_table_default_permissions: List[PrincipalPermissions] = Field(
        default_factory=list,
        alias='CreateTableDefaultPermissions',
        description='Specifies whether access control on newly created table is managed by Lake Formation permissions or exclusively by IAM permissions.',
    )
    trusted_resource_owners: List[str] = Field(
        default_factory=list,
        alias='TrustedResourceOwners',
        description='A list of the resource-owning account IDs that the caller account can use to share their user access details.',
    )
    allow_external_data_filtering: bool = Field(
        default=False,
        alias='AllowExternalDataFiltering',
        description='Whether to allow Amazon EMR clusters to access data managed by Lake Formation.',
    )
    allow_full_table_external_data_access: bool = Field(
        default=False,
        alias='AllowFullTableExternalDataAccess',
        description='Whether to allow a third-party query engine to get data access credentials without session tags when a caller has full data access permissions.',
    )
    external_data_filtering_allow_list: List[DataLakePrincipal] = Field(
        default_factory=list,
        alias='ExternalDataFilteringAllowList',
        description='A list of the account IDs of AWS accounts with Amazon EMR clusters that are to perform data filtering.',
    )
    authorized_session_tag_value_list: List[str] = Field(
        default_factory=list,
        alias='AuthorizedSessionTagValueList',
        description='Lake Formation session tag values authorized for the third party integrator to tag the temporary security credentials.',
    )
    parameters: Dict[str, str] = Field(
        default_factory=dict,
        alias='Parameters',
        description='A key-value map that provides additional configuration on your data lake, such as CROSS_ACCOUNT_VERSION.',
    )
