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

"""Common models for the Lake Formation MCP Server."""

from pydantic import BaseModel, ConfigDict, Field


class DataLakePrincipal(BaseModel):
    """An AWS Lake Formation principal."""

    model_config = ConfigDict(populate_by_name=True)

    data_lake_principal_identifier: str = Field(
        default=...,
        alias='DataLakePrincipalIdentifier',
        description='An identifier for the Lake Formation principal (IAM user ARN, IAM role ARN, or group identifier).',
    )
