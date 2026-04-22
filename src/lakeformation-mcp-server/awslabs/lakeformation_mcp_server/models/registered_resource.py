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

"""Pydantic models for Lake Formation Registered Resources."""

from pydantic import BaseModel, Field
from typing import List, Optional


class RegisteredResource(BaseModel):
    """A registered Lake Formation resource."""

    resource_arn: str = Field(
        default=..., description='The Amazon Resource Name (ARN) of the resource.'
    )
    role_arn: Optional[str] = Field(
        default=None, description='The IAM role that registered a resource.'
    )
    last_modified: Optional[str] = Field(
        default=None, description='The date and time the resource was last modified.'
    )
    with_federation: bool = Field(
        default=False, description='Whether or not the resource is a federated resource.'
    )
    hybrid_access_enabled: bool = Field(
        default=False,
        description='Whether the data access of tables pointing to the location can be managed by both Lake Formation permissions as well as Amazon S3 bucket policies.',
    )
    with_privileged_access: bool = Field(
        default=False,
        description='Grants the calling principal the permissions to perform all supported Lake Formation operations on the registered data location.',
    )
    verification_status: Optional[str] = Field(
        default=None,
        description='Whether the registered role has sufficient permissions to access the registered S3 location. Values: VERIFIED, NOT_VERIFIED, VERIFICATION_FAILED.',
    )
    expected_resource_owner_account: Optional[str] = Field(
        default=None,
        description='The AWS account that owns the Glue tables associated with specific Amazon S3 locations.',
    )


class RegisteredResourceList(BaseModel):
    """List of registered resources."""

    resources: List[RegisteredResource] = Field(
        default_factory=list, description='List of registered Lake Formation resources.'
    )
    next_token: Optional[str] = Field(
        default=None, description='A continuation token if the results are paginated.'
    )
