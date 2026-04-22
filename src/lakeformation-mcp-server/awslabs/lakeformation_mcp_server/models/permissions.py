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

"""Pydantic models for Lake Formation Permissions."""

from awslabs.lakeformation_mcp_server.models.common import DataLakePrincipal
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class Permission(BaseModel):
    """A Lake Formation permission entry."""

    principal: Optional[DataLakePrincipal] = Field(
        default=None,
        description='The Data Lake principal granted permissions.',
    )
    # Note: In the future, we can make this stricter typed instead of using `Any`
    resource: Dict[str, Any] = Field(
        default_factory=dict,
        description='The resource where permissions apply. Can be Catalog, Database, Table, DataLocation, LFTag, or LFTagPolicy.',
    )
    permissions: List[str] = Field(
        default_factory=list,
        description='The permissions granted on the resource.',
    )
    permissions_with_grant_option: List[str] = Field(
        default_factory=list,
        description='Permissions that can be granted to others.',
    )


class PermissionList(BaseModel):
    """List of permissions."""

    permissions: List[Permission] = Field(
        default_factory=list, description='List of principal-resource permission entries.'
    )
    next_token: Optional[str] = Field(
        default=None, description='A continuation token if the results are paginated.'
    )
