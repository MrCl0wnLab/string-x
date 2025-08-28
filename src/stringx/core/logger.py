# Biblioteca padrão
import os
import logging
from rich.logging import RichHandler
from rich.console import Console

# Módulos locais
from stringx.config import setting

class Logger:
    """Sistema centralizado de logging para o String-X."""
    
    _instance = None
    _initialized = False
    
    # Mapeamento de níveis de verbosidade
    LEVEL_MAP = {
        1: 'info',
        2: 'warning', 
        3: 'debug',
        4: 'error',
        5: 'exception'
    }
    
    def __new__(cls, name="string-x"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, name="string-x"):
        if self._initialized:
            return
            
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.console = None  # Will be set by set_styled_console()
        self.active_levels = set()  # Níveis ativos para console
        
        # Evitar duplicação de handlers
        if not self.logger.handlers:
            # Configurar saída para console com Rich
            console_handler = RichHandler(rich_tracebacks=True, show_time=False)
            console_handler.setLevel(logging.DEBUG)
            
            # Configurar saída para arquivo - create directory if needed
            os.makedirs(os.path.dirname(setting.LOG_FILE_OUTPUT), exist_ok=True)
            file_handler = logging.FileHandler(setting.LOG_FILE_OUTPUT)
            file_handler.setLevel(logging.DEBUG)
            
            # Configurar arquivo separado para erros
            error_log_path = str(setting.LOG_FILE_OUTPUT).replace('.log', '-errors.log')
            self.error_file_handler = logging.FileHandler(error_log_path)
            self.error_file_handler.setLevel(logging.ERROR)
            
            # Formato para arquivo (com timestamp)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.error_file_handler.setFormatter(file_formatter)
            
            # Formato para console (sem timestamp para saída limpa)
            console_formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)
            
            # Adicionar handlers
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
            # Note: error_file_handler será usado diretamente nos métodos de erro
        
        self._initialized = True
    
    def set_styled_console(self, styled_console):
        """
        Define o console estilizado para usar para saída.
        
        Args:
            styled_console: Instância do console com StyleHighlighter aplicado
        """
        self.console = styled_console
    
    def set_verbose_levels(self, verbose_arg):
        """
        Define os níveis de verbosidade baseado no argumento -v.
        
        Args:
            verbose_arg (str|None): Níveis especificados (ex: "1", "1,2", "all", None)
        """
        if not verbose_arg:
            self.active_levels = set()
            return
            
        if verbose_arg == "all":
            self.active_levels = {'info', 'warning', 'debug', 'error', 'exception'}
            return
            
        # Parse níveis individuais ou combinados (ex: "1,2", "4,3")
        try:
            level_numbers = [int(x.strip()) for x in verbose_arg.split(',')]
            self.active_levels = {self.LEVEL_MAP[num] for num in level_numbers if num in self.LEVEL_MAP}
        except (ValueError, KeyError):
            # Se houver erro no parsing, não ativa nenhum nível
            self.active_levels = set()
    
    def is_level_active(self, level):
        """Verifica se um nível de log está ativo para console"""
        return level in self.active_levels
    
    def debug(self, message, module_name=None):
        """Log debug messages"""
        prefix = f"[{module_name}] " if module_name else ""
        full_message = f"{prefix}{message}"
        
        # Sempre salva no arquivo
        self.logger.debug(full_message)
        
        # Mostra no console apenas se nível 3 (debug) estiver ativo
        if self.is_level_active('debug'):
            self.console.print(f"[dim]DEBUG: {full_message}[/dim]")
    
    def info(self, message, clean_output=False):
        """Log info messages"""
        if clean_output:
            # Para saída limpa (resultados), sempre mostra sem formatação
            self.console.print(message)
            # Ainda salva no arquivo
            self.logger.handlers[1].handle(self.logger.makeRecord(
                self.logger.name, logging.INFO, __file__, 0, message, (), None
            ))
        elif self.is_level_active('info'):
            # Mostra no console E salva no arquivo se nível 1 (info) estiver ativo
            self.logger.info(message)
        else:
            # Apenas salva no arquivo, não mostra no console
            self.logger.handlers[1].handle(self.logger.makeRecord(
                self.logger.name, logging.INFO, __file__, 0, message, (), None
            ))
    
    def warning(self, message):
        """Log warning messages"""
        if self.is_level_active('warning'):
            # Mostra no console E salva no arquivo se nível 2 (warning) estiver ativo
            self.logger.warning(message)
        else:
            # Apenas salva no arquivo, não mostra no console
            self.logger.handlers[1].handle(self.logger.makeRecord(
                self.logger.name, logging.WARNING, __file__, 0, message, (), None
            ))
    
    def error(self, message):
        """Log error messages"""
        # Sempre salva no arquivo de erros separado
        if hasattr(self, 'error_file_handler'):
            error_record = self.logger.makeRecord(
                self.logger.name, logging.ERROR, __file__, 0, message, (), None
            )
            self.error_file_handler.handle(error_record)
        
        # Mostra no console apenas se nível 4 (error) estiver ativo
        if self.is_level_active('error'):
            # Mostra no console sem salvar no arquivo principal
            if self.console:
                self.console.print(f"[red]ERROR: {message}[/red]")
            else:
                print(f"ERROR: {message}")
    
    def exception(self, message):
        """Log exception messages with traceback"""
        # Sempre salva no arquivo de erros separado
        if hasattr(self, 'error_file_handler'):
            error_record = self.logger.makeRecord(
                self.logger.name, logging.ERROR, __file__, 0, message, (), None
            )
            self.error_file_handler.handle(error_record)
        
        # Mostra no console apenas se nível 5 (exception) estiver ativo
        if self.is_level_active('exception'):
            # Mostra no console sem salvar no arquivo principal
            if self.console:
                self.console.print(f"[red]EXCEPTION: {message}[/red]")
            else:
                print(f"EXCEPTION: {message}")
    
    def result(self, message):
        """Print clean results without any formatting or timestamps"""
        if self.console is None:
            # Fallback to plain console if styled console not set
            from rich.console import Console
            console = Console()
            console.print(message)
        else:
            # Use styled console for highlighting
            self.console.print(message)
        # Note: Results are saved to output file via _save_command_log method
        # No need to duplicate in main log file
    
    def verbose(self, message, is_verbose=False):
        """
        Print verbose messages - now respects logging levels instead of boolean flag.
        
        Args:
            message (str): Message to log
            is_verbose (bool): Legacy parameter - ignored, uses level system instead
        """
        # Always save to file
        self.logger.debug(f"VERBOSE: {message}")
        
        # Show on console based on active levels (info level for verbose messages)
        if self.is_level_active('info'):
            self.console.print(f"[dim]{message}[/dim]")
    
    def log_file_info(self):
        """Log information about output and error files"""
        if hasattr(self, 'error_file_handler'):
            output_file = str(setting.LOG_FILE_OUTPUT)
            error_file = str(setting.LOG_FILE_OUTPUT).replace('.log', '-errors.log')
            
            self.info(f"Results will be saved to: {output_file}")
            self.info(f"Errors will be saved to: {error_file}")

# Global logger instance
logger = Logger()