"""String-X Configuration Settings

This module loads configuration from environment variables and .env file.
It provides centralized configuration management for the entire application.
"""

import os
from pathlib import Path
from typing import List, Optional, Union
from datetime import datetime

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# Get project root directory
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent.resolve()
PROJECT_ROOT = SCRIPT_DIR

# Load .env file from project root
if load_dotenv is not None:
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        # Load from current directory as fallback
        load_dotenv()

# Import banner after loading environment
try:
    from stringx.core.banner.asciiart import AsciiBanner
except ImportError:
    AsciiBanner = None


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable."""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')


def get_env_int(key: str, default: int) -> int:
    """Get integer value from environment variable."""
    try:
        return int(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default


def get_env_float(key: str, default: float) -> float:
    """Get float value from environment variable."""
    try:
        return float(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default


def get_env_list(key: str, default: Optional[List[str]] = None) -> List[str]:
    """Get list value from environment variable (comma-separated)."""
    if default is None:
        default = []
    value = os.getenv(key, '')
    return [item.strip() for item in value.split(',') if item.strip()] or default


def get_env_path(key: str, default: Union[str, Path]) -> Path:
    """Get path value from environment variable."""
    value = os.getenv(key, str(default))
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


# ==========================================
# APPLICATION INFORMATION
# ==========================================
__version__ = os.getenv('STRX_VERSION', '1.0.0')
__author__ = os.getenv('STRX_AUTHOR', 'Cleiton Pinheiro aka MrCl0wn')
__maintainer__ = __author__
__credits__ = [__author__]
__description__ = "String-X: Modern OSINT Automation Tool"
__url__ = os.getenv('STRX_URL', 'https://github.com/MrCl0wnLab/string-x')
__license__ = os.getenv('STRX_LICENSE', 'MIT')
__email__ = os.getenv('STRX_EMAIL', 'mrcl0wnlab@gmail.com')
__twitter__ = os.getenv('STRX_TWITTER', 'https://twitter.com/MrCl0wnLab')
__git__ = [
    'https://github.com/MrCl0wnLab',
    'https://github.com/osintbrazuca'
]

# ==========================================
# LOGGING CONFIGURATION
# ==========================================
LOG_LEVEL = os.getenv('STRX_LOG_LEVEL', 'INFO')
LOG_DIRECTORY = get_env_path('STRX_LOG_DIRECTORY', 'output')
LOG_TIME_FORMAT = os.getenv('STRX_LOG_TIME_FORMAT', '%d-%m-%Y-%H')
LOG_FILE_LAST = os.getenv('STRX_LOG_FILE_LAST', 'output-last-value.log')
ENABLE_FILE_LOGGING = get_env_bool('STRX_ENABLE_FILE_LOGGING', True)
LOG_MAX_FILE_SIZE = get_env_int('STRX_LOG_MAX_FILE_SIZE', 100) * 1024 * 1024  # MB to bytes
LOG_BACKUP_COUNT = get_env_int('STRX_LOG_BACKUP_COUNT', 5)

# Create time-based log filename
TIME = datetime.now().strftime(LOG_TIME_FORMAT)
LOG_FILE_OUTPUT = LOG_DIRECTORY / f'output-{TIME}.log'

# Ensure log directory exists
LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

# ==========================================
# HTTP REQUEST CONFIGURATION
# ==========================================
REQUEST_USER_AGENT = os.getenv('STRX_USER_AGENT', f'String-X/{__version__}')
REQUEST_TIMEOUT = get_env_int('STRX_REQUEST_TIMEOUT', 30)
RETRY_OPERATIONS = get_env_int('STRX_RETRY_OPERATIONS', 3)
RETRY_DELAY = get_env_int('STRX_RETRY_DELAY', 2)
RETRY_MAX_DELAY = get_env_int('STRX_RETRY_MAX_DELAY', 60)
CONNECTION_POOL_SIZE = get_env_int('STRX_CONNECTION_POOL_SIZE', 10)

# ==========================================
# THREADING CONFIGURATION
# ==========================================
THREAD_MAX = get_env_int('STRX_THREAD_MAX', 10)
THREAD_TIMEOUT = get_env_int('STRX_THREAD_TIMEOUT', 300)
THREAD_POOL_MAX_WORKERS = get_env_int('STRX_THREAD_POOL_MAX_WORKERS', 20)

# ==========================================
# BANNER CONFIGURATION
# ==========================================
BANNER_DEFAULT = os.getenv('STRX_BANNER_DEFAULT', 'strx')
BANNER_RANDOM = get_env_bool('STRX_BANNER_RANDOM', True)
BANNER_ENABLED = get_env_bool('STRX_BANNER_ENABLED', True)

# Initialize banner if available
if AsciiBanner and BANNER_ENABLED:
    BANNER = AsciiBanner()
    BANNER_HELP = (
        BANNER.show_random() if BANNER_RANDOM else BANNER.show(BANNER_DEFAULT)
    )
else:
    BANNER = None
    BANNER_HELP = f'String-X {__version__}'

# ==========================================
# OUTPUT CONFIGURATION
# ==========================================
DEFAULT_OUTPUT_FORMAT = os.getenv('STRX_DEFAULT_OUTPUT_FORMAT', 'txt')
OUTPUT_FORMATS = get_env_list('STRX_OUTPUT_FORMATS', ['txt', 'csv', 'json', 'xml'])
OUTPUT_MAX_FILE_SIZE = get_env_int('STRX_OUTPUT_MAX_FILE_SIZE', 500) * 1024 * 1024  # MB
OUTPUT_DIR_PERMISSIONS = int(os.getenv('STRX_OUTPUT_DIR_PERMISSIONS', '755'), 8)

# ==========================================
# SECURITY CONFIGURATION
# ==========================================
MAX_INPUT_SIZE = get_env_int('STRX_MAX_INPUT_SIZE', 1048576)  # 1MB
MAX_THREAD_COUNT = get_env_int('STRX_MAX_THREAD_COUNT', 100)
MAX_TIMEOUT = get_env_int('STRX_MAX_TIMEOUT', 3600)  # 1 hour
MAX_STRING_LIST_SIZE = get_env_int('STRX_MAX_STRING_LIST_SIZE', 10000)
MAX_COMMAND_LENGTH = get_env_int('STRX_MAX_COMMAND_LENGTH', 8192)
SECURITY_VALIDATION = get_env_bool('STRX_SECURITY_VALIDATION', True)
ALLOWED_COMMAND_PATTERNS = get_env_list('STRX_ALLOWED_COMMAND_PATTERNS', 
    [r'^(echo|grep|curl|dig|nslookup|ping|whois|nmap).*'])
BLOCKED_COMMAND_PATTERNS = get_env_list('STRX_BLOCKED_COMMAND_PATTERNS', 
    [r'rm\s+-rf', r'>\s*/dev', r'/etc/passwd', r'/etc/shadow', r'sudo\s+', r'su\s+'])

# ==========================================
# GOOGLE CUSTOM SEARCH ENGINE
# ==========================================
GOOGLE_CSE_ID_FILE = get_env_path('STRX_GOOGLE_CSE_ID_FILE', 
    'src/stringx/config/google_cse_id.txt')
GOOGLE_API_KEY = os.getenv('STRX_GOOGLE_API_KEY', '')
GOOGLE_SEARCH_TIMEOUT = get_env_int('STRX_GOOGLE_SEARCH_TIMEOUT', 10)
GOOGLE_MAX_RESULTS = get_env_int('STRX_GOOGLE_MAX_RESULTS', 100)

# Load Google CSE IDs
try:
    if GOOGLE_CSE_ID_FILE.exists():
        with open(GOOGLE_CSE_ID_FILE, 'r') as f:
            GOOGLE_CSE_ID_LIST = [line.strip() for line in f if line.strip()]
    else:
        GOOGLE_CSE_ID_LIST = []
        # Create directory and empty file if it doesn't exist
        GOOGLE_CSE_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        GOOGLE_CSE_ID_FILE.write_text('')
except Exception:
    GOOGLE_CSE_ID_LIST = []

# ==========================================
# DATABASE CONNECTIONS
# ==========================================
# MySQL
MYSQL_HOST = os.getenv('STRX_MYSQL_HOST', 'localhost')
MYSQL_PORT = get_env_int('STRX_MYSQL_PORT', 3306)
MYSQL_DATABASE = os.getenv('STRX_MYSQL_DATABASE', 'strx_db')
MYSQL_USER = os.getenv('STRX_MYSQL_USER', 'strx_user')
MYSQL_PASSWORD = os.getenv('STRX_MYSQL_PASSWORD', 'Str1ngX_p4ss!')
MYSQL_CHARSET = os.getenv('STRX_MYSQL_CHARSET', 'utf8mb4')
MYSQL_TIMEOUT = get_env_int('STRX_MYSQL_TIMEOUT', 30)

# SQLite
SQLITE_DATABASE = get_env_path('STRX_SQLITE_DATABASE', 'output/strx.db')
SQLITE_TIMEOUT = get_env_int('STRX_SQLITE_TIMEOUT', 30)

# OpenSearch
OPENSEARCH_HOST = os.getenv('STRX_OPENSEARCH_HOST', 'localhost')
OPENSEARCH_PORT = get_env_int('STRX_OPENSEARCH_PORT', 9200)
OPENSEARCH_USERNAME = os.getenv('STRX_OPENSEARCH_USERNAME', 'admin')
OPENSEARCH_PASSWORD = os.getenv('STRX_OPENSEARCH_PASSWORD', 'Str1ngX_p4ss!')
OPENSEARCH_USE_SSL = get_env_bool('STRX_OPENSEARCH_USE_SSL', True)
OPENSEARCH_VERIFY_CERTS = get_env_bool('STRX_OPENSEARCH_VERIFY_CERTS', False)
OPENSEARCH_TIMEOUT = get_env_int('STRX_OPENSEARCH_TIMEOUT', 60)
OPENSEARCH_INDEX = os.getenv('STRX_OPENSEARCH_INDEX', 'strx-data')
OPENSEARCH_RETRY = get_env_int('STRX_OPENSEARCH_RETRY', 3)
OPENSEARCH_RETRY_DELAY = get_env_int('STRX_OPENSEARCH_RETRY_DELAY', 5)

# ==========================================
# AI MODULES CONFIGURATION
# ==========================================
# OpenAI
OPENAI_API_KEY = os.getenv('STRX_OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('STRX_OPENAI_MODEL', 'gpt-3.5-turbo')
OPENAI_TIMEOUT = get_env_int('STRX_OPENAI_TIMEOUT', 30)
OPENAI_MAX_TOKENS = get_env_int('STRX_OPENAI_MAX_TOKENS', 1000)

# Gemini
GEMINI_API_KEY = os.getenv('STRX_GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('STRX_GEMINI_MODEL', 'gemini-pro')
GEMINI_TIMEOUT = get_env_int('STRX_GEMINI_TIMEOUT', 30)

# ==========================================
# THIRD-PARTY SERVICES
# ==========================================
SHODAN_API_KEY = os.getenv('STRX_SHODAN_API_KEY', '')
VIRUSTOTAL_API_KEY = os.getenv('STRX_VIRUSTOTAL_API_KEY', '')
IPINFO_TOKEN = os.getenv('STRX_IPINFO_TOKEN', '')
TELEGRAM_BOT_TOKEN = os.getenv('STRX_TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('STRX_TELEGRAM_CHAT_ID', '')
SLACK_TOKEN = os.getenv('STRX_SLACK_TOKEN', '')
SLACK_CHANNEL = os.getenv('STRX_SLACK_CHANNEL', '')

# FTP
FTP_HOST = os.getenv('STRX_FTP_HOST', 'localhost')
FTP_PORT = get_env_int('STRX_FTP_PORT', 21)
FTP_USERNAME = os.getenv('STRX_FTP_USERNAME', 'anonymous')
FTP_PASSWORD = os.getenv('STRX_FTP_PASSWORD', '')
FTP_TIMEOUT = get_env_int('STRX_FTP_TIMEOUT', 30)

# SSH
SSH_HOST = os.getenv('STRX_SSH_HOST', 'localhost')
SSH_PORT = get_env_int('STRX_SSH_PORT', 22)
SSH_USERNAME = os.getenv('STRX_SSH_USERNAME', '')
SSH_PASSWORD = os.getenv('STRX_SSH_PASSWORD', '')
SSH_TIMEOUT = get_env_int('STRX_SSH_TIMEOUT', 30)

# ==========================================
# PERFORMANCE TUNING
# ==========================================
ENABLE_CACHING = get_env_bool('STRX_ENABLE_CACHING', True)
CACHE_TTL = get_env_int('STRX_CACHE_TTL', 3600)
CACHE_SIZE = get_env_int('STRX_CACHE_SIZE', 1000)
MEMORY_LIMIT = get_env_int('STRX_MEMORY_LIMIT', 512) * 1024 * 1024  # MB to bytes
MIN_DISK_SPACE = get_env_int('STRX_MIN_DISK_SPACE', 100) * 1024 * 1024  # MB

# ==========================================
# DEVELOPMENT/DEBUG OPTIONS
# ==========================================
DEBUG = get_env_bool('STRX_DEBUG', False)
VERBOSE = get_env_bool('STRX_VERBOSE', False)
DEFAULT_VERBOSE_LEVEL = get_env_int('STRX_DEFAULT_VERBOSE_LEVEL', 1)
ENABLE_PROFILING = get_env_bool('STRX_ENABLE_PROFILING', False)
ENABLE_METRICS = get_env_bool('STRX_ENABLE_METRICS', False)

# ==========================================
# BACKWARD COMPATIBILITY
# ==========================================
# Keep old variable names for backward compatibility
user_agent = REQUEST_USER_AGENT  # Legacy
USER_AGENT = REQUEST_USER_AGENT