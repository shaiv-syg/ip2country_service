from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()
CONFIG_FILE_PATH = BASE_DIR / 'app' / 'config' / 'config.yaml'

# ip country db for testing and development
DATA_FILE_PATH = BASE_DIR / 'data' / 'ip_data.csv'