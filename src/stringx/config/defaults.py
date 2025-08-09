"""String-X Default Configuration Values

This module contains all the default configuration values for String-X.
These are the project's fixed strings, integers, and booleans that define
the application's behavior when no environment variables are set.

Environment variables in .env will override these defaults.
"""

from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()

# ==========================================
# APPLICATION INFORMATION
# ==========================================
DEFAULT_VERSION = '1.0.0'
DEFAULT_AUTHOR = 'Cleiton Pinheiro aka MrCl0wn'
DEFAULT_URL = 'https://github.com/MrCl0wnLab/string-x'
DEFAULT_EMAIL = 'mrcl0wnlab@gmail.com'
DEFAULT_TWITTER = 'https://twitter.com/MrCl0wnLab'
DEFAULT_LICENSE = 'MIT'

# ==========================================
# LOGGING CONFIGURATION
# ==========================================
DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_LOG_DIRECTORY = 'output'
DEFAULT_LOG_TIME_FORMAT = '%d-%m-%Y-%H'
DEFAULT_LOG_FILE_LAST = 'output-last-value.log'
DEFAULT_ENABLE_FILE_LOGGING = True
DEFAULT_LOG_MAX_FILE_SIZE = 100  # MB
DEFAULT_LOG_BACKUP_COUNT = 5

# ==========================================
# THREADING CONFIGURATION
# ==========================================
DEFAULT_THREAD_MAX = 10
DEFAULT_THREAD_TIMEOUT = 300  # seconds
DEFAULT_THREAD_POOL_MAX_WORKERS = 20

# ==========================================
# HTTP REQUEST CONFIGURATION
# ==========================================
DEFAULT_USER_AGENT = f'String-X/{DEFAULT_VERSION}'
DEFAULT_REQUEST_TIMEOUT = 30  # seconds
DEFAULT_RETRY_OPERATIONS = 3
DEFAULT_RETRY_DELAY = 2  # seconds
DEFAULT_RETRY_MAX_DELAY = 60  # seconds
DEFAULT_CONNECTION_POOL_SIZE = 10

# ==========================================
# SECURITY CONFIGURATION
# ==========================================
DEFAULT_MAX_INPUT_SIZE = 1048576  # 1MB
DEFAULT_MAX_THREAD_COUNT = 100
DEFAULT_MAX_TIMEOUT = 3600  # 1 hour
DEFAULT_MAX_STRING_LIST_SIZE = 10000
DEFAULT_MAX_COMMAND_LENGTH = 8192
DEFAULT_SECURITY_VALIDATION = True

# Default allowed and blocked command patterns
DEFAULT_ALLOWED_COMMAND_PATTERNS = [
    r'^(echo|grep|curl|dig|nslookup|ping|whois|nmap).*'
]
DEFAULT_BLOCKED_COMMAND_PATTERNS = [
    r'rm\s+-rf', r'>\s*/dev', r'/etc/passwd', r'/etc/shadow', 
    r'sudo\s+', r'su\s+'
]

# ==========================================
# OUTPUT CONFIGURATION
# ==========================================
DEFAULT_OUTPUT_FORMAT = 'txt'
DEFAULT_OUTPUT_FORMATS = ['txt', 'csv', 'json', 'xml']
DEFAULT_OUTPUT_MAX_FILE_SIZE = 500  # MB
DEFAULT_OUTPUT_DIR_PERMISSIONS = 0o755

# ==========================================
# BANNER CONFIGURATION
# ==========================================
DEFAULT_BANNER_DEFAULT = 'strx'
DEFAULT_BANNER_RANDOM = True
DEFAULT_BANNER_ENABLED = True

# ==========================================
# NOTIFICATION CONFIGURATION
# ==========================================
DEFAULT_NOTIFICATIONS_ENABLED = False
DEFAULT_NOTIFICATION_ICON_PATH = ''  # Will be auto-resolved if empty
DEFAULT_NOTIFICATION_APP_NAME = 'String-X'

# ==========================================
# DATABASE CONNECTION DEFAULTS
# ==========================================
# MySQL defaults
DEFAULT_MYSQL_HOST = 'localhost'
DEFAULT_MYSQL_PORT = 3306
DEFAULT_MYSQL_DATABASE = 'strx_db'
DEFAULT_MYSQL_USER = 'strx_user'
DEFAULT_MYSQL_PASSWORD = 'Str1ngX_p4ss!'  # Default only - override in .env
DEFAULT_MYSQL_CHARSET = 'utf8mb4'
DEFAULT_MYSQL_TIMEOUT = 30

# SQLite defaults
DEFAULT_SQLITE_DATABASE = 'output/strx.db'
DEFAULT_SQLITE_TIMEOUT = 30

# OpenSearch defaults
DEFAULT_OPENSEARCH_HOST = 'localhost'
DEFAULT_OPENSEARCH_PORT = 9200
DEFAULT_OPENSEARCH_USERNAME = 'admin'
DEFAULT_OPENSEARCH_PASSWORD = 'Str1ngX_p4ss!'  # Default only - override in .env
DEFAULT_OPENSEARCH_USE_SSL = True
DEFAULT_OPENSEARCH_VERIFY_CERTS = False
DEFAULT_OPENSEARCH_TIMEOUT = 60
DEFAULT_OPENSEARCH_INDEX = 'strx-data'
DEFAULT_OPENSEARCH_RETRY = 3
DEFAULT_OPENSEARCH_RETRY_DELAY = 5

# ==========================================
# GOOGLE CUSTOM SEARCH CONFIGURATION
# ==========================================
DEFAULT_GOOGLE_CSE_ID_FILE = 'src/stringx/config/google_cse_id.txt'
DEFAULT_GOOGLE_SEARCH_TIMEOUT = 10
DEFAULT_GOOGLE_MAX_RESULTS = 100

# ==========================================
# FTP CONNECTION DEFAULTS
# ==========================================
DEFAULT_FTP_HOST = 'localhost'
DEFAULT_FTP_PORT = 21
DEFAULT_FTP_USERNAME = 'anonymous'
DEFAULT_FTP_PASSWORD = ''
DEFAULT_FTP_TIMEOUT = 30

# ==========================================
# SSH CONNECTION DEFAULTS
# ==========================================
DEFAULT_SSH_HOST = 'localhost'
DEFAULT_SSH_PORT = 22
DEFAULT_SSH_USERNAME = ''
DEFAULT_SSH_PASSWORD = ''
DEFAULT_SSH_TIMEOUT = 30

# ==========================================
# AI MODULES CONFIGURATION
# ==========================================
# OpenAI defaults
DEFAULT_OPENAI_MODEL = 'gpt-3.5-turbo'
DEFAULT_OPENAI_TIMEOUT = 30
DEFAULT_OPENAI_MAX_TOKENS = 1000

# Gemini defaults
DEFAULT_GEMINI_MODEL = 'gemini-pro'
DEFAULT_GEMINI_TIMEOUT = 30

# ==========================================
# PERFORMANCE TUNING
# ==========================================
DEFAULT_ENABLE_CACHING = True
DEFAULT_CACHE_TTL = 3600  # seconds
DEFAULT_CACHE_SIZE = 1000  # items
DEFAULT_MEMORY_LIMIT = 512  # MB
DEFAULT_MIN_DISK_SPACE = 100  # MB

# ==========================================
# DEVELOPMENT/DEBUG OPTIONS
# ==========================================
DEFAULT_DEBUG = False
DEFAULT_VERBOSE = False
DEFAULT_DEFAULT_VERBOSE_LEVEL = 1
DEFAULT_ENABLE_PROFILING = False
DEFAULT_ENABLE_METRICS = False