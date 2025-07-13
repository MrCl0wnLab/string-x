import os
import sys

__author__ = "Cleiton Pinheiro aka MrCl0wn"
__maintainer__ = "Cleiton Pinheiro aka MrCl0wn"
__credits__ = ["Cleiton Pinheiro"]
__description__ = "String-X: Tool for automating commands"
__url__ = "https://github.com/MrCl0wnLab/string-x"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "mrcl0wnlab[@]gmail.com"
__twitter__ = "https://twitter.com/MrCl0wnLab"
__git__ = [
    "https://github.com/MrCl0wnLab",
    "https://github.com/osintbrazuca"
]

# Obter diretório do projeto
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from core.banner.asciiart import AsciiBanner

# LOGS - Use absolute paths
TIME = datetime.now().strftime("%d-%m-%Y-%H")
LOG_DIRECTORY = os.path.join(SCRIPT_DIR, 'output')  # Absolute path for output directory
LOG_FILE_LAST = 'output-last-value.log'
LOG_FILE_OUTPUT = f'{LOG_DIRECTORY}/output-{TIME}.log'

# REQUEST
REQUEST_USER_AGENT = 'String-X/1.0'

# BANNERS
BANNER = AsciiBanner()
BANNER_DEFAULT = 'strx'
BANNER_RANDOM = True
BANNER_HELP = (
    BANNER.show_random() if BANNER_RANDOM is True else BANNER.show(BANNER_DEFAULT)
)

# THREADS
THREAD_MAX = 10

# OUTPUT FORMAT
DEFAULT_OUTPUT_FORMAT = 'txt'
OUTPUT_FORMATS = ['txt', 'csv', 'json']

# Remove duplicate SCRIPT_DIR definition
PROJECT_ROOT = SCRIPT_DIR  # No need to redefine, already defined above

# Usar caminho absoluto
GOOGLE_CSE_ID_FILE = os.path.join(SCRIPT_DIR, 'config', 'google_cse_id.txt')
try:
    with open(GOOGLE_CSE_ID_FILE, 'r') as f:
        GOOGLE_CSE_ID_LIST = f.read().splitlines()
except FileNotFoundError:
    # Criar arquivo vazio se não existir
    GOOGLE_CSE_ID_LIST = []
    os.makedirs(os.path.dirname(GOOGLE_CSE_ID_FILE), exist_ok=True)
    with open(GOOGLE_CSE_ID_FILE, 'w') as f:
        f.write('')