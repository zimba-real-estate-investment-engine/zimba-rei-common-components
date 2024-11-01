# test_config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load test environment variables
env_path = Path('.') / '.env.test'
load_dotenv(dotenv_path=env_path)

class TestConfig:
    DB_USER = os.getenv('TEST_DB_USER', 'rei_app_rds_user')
    DB_PASSWORD = os.getenv('TEST_DB_PASSWORD', 'thepassword')
    DB_HOST = os.getenv('TEST_DB_HOST', 'zimba-rei-micro.cz2qemaeifj0.us-east-2.rds.amazonaws.com')
    DB_PORT = os.getenv('TEST_DB_PORT', '3306')
    DB_NAME = os.getenv('TEST_DB_NAME', 'zimba_rei_micro_test')
    
    @classmethod
    def get_test_db_url(cls):
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

