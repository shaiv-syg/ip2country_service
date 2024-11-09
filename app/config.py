import yaml
import os
from .constants import CONFIG_FILE_PATH

class Setting:
    def __init__(self, default, yml_path, env_var=None, value_type=str):
        self.default = default
        self.yml_path = yml_path
        self.env_var = env_var
        self.value_type = value_type
        self._value = default

    def load_from_yaml(self, yaml_data):
        keys = self.yml_path.split('.')
        value = yaml_data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                value = None
            if value is None:
                break
        if value is not None:
            self._value = value

    def load_from_env(self):
        if self.env_var:
            env_value = os.getenv(self.env_var)
            if env_value is not None:
                if self.value_type == int:
                    self._value = int(env_value)
                else:
                    self._value = env_value

    def get(self):
        return self._value

# Load YAML configuration
with open(CONFIG_FILE_PATH, 'r') as f:
    yaml_config = yaml.safe_load(f)

def create_setting(default, yml_path, env_var=None, value_type=str):
    setting = Setting(default, yml_path, env_var, value_type)
    setting.load_from_yaml(yaml_config)
    setting.load_from_env()
    return setting.get()

# Define settings with their final values
IP_COUNTRY_DB = create_setting(
    default='csv',
    yml_path='rate_limiter_service.ip_country_db',
    env_var='IP_COUNTRY_DB'
)

RATE_LIMIT = create_setting(
    default=5,
    yml_path='rate_limiter_service.rate_limit',
    env_var='RATE_LIMIT',
    value_type=int
)

REDIS_HOST = create_setting(
    default='redis',
    yml_path='rate_limiter_service.redis_host',
    env_var='REDIS_HOST'
)

REDIS_PORT = create_setting(
    default=6379,
    yml_path='rate_limiter_service.redis_port',
    env_var='REDIS_PORT',
    value_type=int
)