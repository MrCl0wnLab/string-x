# Biblioteca padrão
import logging
from rich.logging import RichHandler

# Módulos locais
from config import setting

class Logger:
    """Sistema centralizado de logging para o String-X."""
    
    def __init__(self, name="string-x"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Configurar saída para console com Rich
        console_handler = RichHandler(rich_tracebacks=True)
        console_handler.setLevel(logging.INFO)
        
        # Configurar saída para arquivo
        file_handler = logging.FileHandler(setting.LOG_FILE_OUTPUT)
        file_handler.setLevel(logging.DEBUG)
        
        # Formato
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Adicionar handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def exception(self, message):
        self.logger.exception(message)