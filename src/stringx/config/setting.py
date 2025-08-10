"""String-X Configuration Settings

This module automatically loads all variables from default.json file.
Variables are automatically imported as module attributes.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from stringx.core.banner.asciiart import AsciiBanner
except ImportError:
    AsciiBanner = None

# Get project root directory
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent.resolve()
PROJECT_ROOT = SCRIPT_DIR

# Application information (hardcoded, not from default.json)
__version__ = "1.0.0"
__author__ = "Cleiton Pinheiro aka MrCl0wn"
__maintainer__ = __author__
__credits__ = [__author__]
__description__ = "String-X: Modern OSINT Automation Tool"
__url__ = "https://github.com/MrCl0wnLab/string-x"
__license__ = "MIT"
__email__ = "mrcl0wnlab@gmail.com"
__twitter__ = "https://twitter.com/MrCl0wnLab"
__git__ = [
    'https://github.com/MrCl0wnLab',
    'https://github.com/osintbrazuca'
]

def _convert_value(key, value):
    """Convert string values to appropriate types based on variable name patterns."""
    if not isinstance(value, str):
        return value
    
    # Boolean conversion
    bool_patterns = ['DEBUG', 'VERBOSE', 'ENABLED', 'RANDOM', 'USE_SSL', 'VERIFY_CERTS', 'VALIDATION']
    if any(pattern in key for pattern in bool_patterns):
        return value.lower() in ('true', '1', 'yes', 'on')
    
    # Integer conversion
    int_patterns = ['PORT', 'TIMEOUT', 'MAX', 'COUNT', 'SIZE', 'LIMIT', 'DELAY', 'RETRY', 'LEVEL']
    if any(pattern in key for pattern in int_patterns):
        try:
            val = int(value)
            # Convert MB to bytes for memory/size variables
            if any(size_key in key for size_key in ['MEMORY_LIMIT', 'MIN_DISK_SPACE', 'FILE_SIZE']):
                return val * 1024 * 1024
            return val
        except (ValueError, TypeError):
            pass
    
    # Path conversion (exclude simple filename configs)
    path_patterns = ['DIRECTORY', 'DATABASE', 'PATH']
    file_patterns = ['_FILE']
    if any(pattern in key for pattern in path_patterns):
        path = Path(value)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path
    elif any(pattern in key for pattern in file_patterns):
        # Only convert files that contain directory separators to Path
        if '/' in value or '\\' in value:
            path = Path(value)
            if not path.is_absolute():
                path = PROJECT_ROOT / path
            return path
        # Otherwise keep as string (simple filenames)
        return value
    
    # List conversion (comma-separated)
    if 'FORMATS' in key or 'PATTERNS' in key:
        return [item.strip() for item in value.split(',') if item.strip()]
    
    return value

# AUTO-IMPORT ALL default.json VARIABLES
config_path = Path(__file__).parent / 'default.json'
if config_path.exists():
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_vars = json.load(f)
        
        current_module = sys.modules[__name__]
        for k, v in config_vars.items():
            if v is not None:  # Skip None values
                converted_value = _convert_value(k, v)
                setattr(current_module, k, converted_value)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load default.json: {e}", file=sys.stderr)

# Create computed variables and initialize components
def _initialize_computed_vars():
    """Initialize computed variables and components after default.json loading."""
    current_module = sys.modules[__name__]
    
    # Time-based variables
    if hasattr(current_module, 'STRX_LOG_TIME_FORMAT'):
        TIME = datetime.now().strftime(current_module.STRX_LOG_TIME_FORMAT)
        setattr(current_module, 'TIME', TIME)
        
        if hasattr(current_module, 'STRX_LOG_DIRECTORY'):
            log_file = current_module.STRX_LOG_DIRECTORY / f'output-{TIME}.log'
            setattr(current_module, 'LOG_FILE_OUTPUT', log_file)
            
            # Create computed path for last log file
            if hasattr(current_module, 'STRX_LOG_FILE_LAST'):
                log_file_last = current_module.STRX_LOG_DIRECTORY / current_module.STRX_LOG_FILE_LAST
                setattr(current_module, 'LOG_FILE_LAST_PATH', log_file_last)
            
            # Ensure log directory exists
            current_module.STRX_LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    
    # Banner initialization
    if AsciiBanner and getattr(current_module, 'STRX_BANNER_ENABLED', True):
        banner = AsciiBanner()
        setattr(current_module, 'BANNER', banner)
        
        banner_default = getattr(current_module, 'STRX_BANNER_DEFAULT', 'strx')
        banner_random = getattr(current_module, 'STRX_BANNER_RANDOM', True)
        banner_help = banner.show_random() if banner_random else banner.show(banner_default)
        setattr(current_module, 'BANNER_HELP', banner_help)
    else:
        setattr(current_module, 'BANNER', None)
        setattr(current_module, 'BANNER_HELP', f'String-X {__version__}')
    
    # Google CSE IDs
    if hasattr(current_module, 'STRX_GOOGLE_CSE_ID_FILE'):
        try:
            google_cse_file = current_module.STRX_GOOGLE_CSE_ID_FILE
            if isinstance(google_cse_file, str):
                google_cse_file = PROJECT_ROOT / google_cse_file
            
            if google_cse_file.exists():
                with open(google_cse_file, 'r') as f:
                    cse_ids = [line.strip() for line in f if line.strip()]
            else:
                cse_ids = []
                # Create directory and empty file if it doesn't exist
                google_cse_file.parent.mkdir(parents=True, exist_ok=True)
                google_cse_file.write_text('')
            
            setattr(current_module, 'GOOGLE_CSE_ID_LIST', cse_ids)
        except Exception:
            setattr(current_module, 'GOOGLE_CSE_ID_LIST', [])

# Initialize computed variables
_initialize_computed_vars()
