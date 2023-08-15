import json
import os

from mlp_sdk.hosting.host import host_mlp_cloud
from mlp_sdk.log.setup_logging import get_logger

from action.action import MlpSdService

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info('Starting SD Service...')

    json_config = json.loads(os.environ.get('SERVICE_CONFIG', '{}'))
    host_mlp_cloud(MlpSdService, MlpSdService.get_init_config_schema()(**json_config))
