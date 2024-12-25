import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
TEMP_DIR = BASE_DIR / "temp"

# Create necessary directories
for directory in [LOG_DIR, DATA_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'agency.log',
            'formatter': 'standard'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': True
        }
    }
}

# Azure OpenAI configuration
AZURE_CONFIG = {
    'api_version': os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
    'timeout': 30.0,
    'max_retries': 3,
    'retry_delay': 1,
}

# Agent configuration
AGENT_CONFIG = {
    'max_prompt_tokens': 25000,
    'temperature': 0.7,
    'timeout': 300,
}

# Database configuration
DATABASE_CONFIG = {
    'path': DATA_DIR / 'agency.db',
    'timeout': 30,
} 