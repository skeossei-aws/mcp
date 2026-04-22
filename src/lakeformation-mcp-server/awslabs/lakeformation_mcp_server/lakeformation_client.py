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

"""AWS client utilities for the Lake Formation MCP Server."""

import boto3
import os
from awslabs.lakeformation_mcp_server import __version__
from botocore.config import Config
from loguru import logger
from typing import Any, Optional


def get_lakeformation_client(region: Optional[str] = None) -> Any:
    """Create a LakeFormation Client.

    Args:
        region: AWS region override. Defaults to AWS_REGION env var or us-east-1

    Returns:
        Configured boto3 LakeFormation client.
    """
    region = region or os.environ.get('AWS_REGION', 'us-east-1')
    config = Config(user_agent_extra=f'md/awslabs#mcp#lakeformation-mcp-server#{__version__}')

    try:
        if aws_profile := os.environ.get('AWS_PROFILE'):
            session = boto3.Session(profile_name=aws_profile, region_name=region)
        else:
            session = boto3.Session(region_name=region)
        return session.client('lakeformation', config=config)
    except Exception as e:
        logger.error(f'Error creating LakeFormation client: {e}')
        raise Exception(f'Error creating LakeFormation client: {e}')
