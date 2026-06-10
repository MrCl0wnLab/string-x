# Biblioteca padrão
import os
import re
import logging
from logging.handlers import RotatingFileHandler
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

    # Remove prefixos ad-hoc do início das mensagens (ex.: "[!] ", "[X] ", "[+] ")
    # para o logger aplicar um marcador de nível uniforme.
    _LEADING_TAG = re.compile(r'^\s*\[[!xX+*~-]\]\s*')

    def __new__(cls, name="string-x"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, name="string-x"):
        if self._initialized:
            return
            
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.console = None  # Will be set by set_styled_console() — usado p/ RESULTADOS (stdout)
        # Console dedicado p/ o trace de diagnóstico, sempre em STDERR, para não
        # poluir o stdout (que carrega só os resultados — pipe-friendly).
        self.err_console = Console(stderr=True)
        self.active_levels = set()  # Níveis ativos para console
        
        # Evitar duplicação de handlers
        if not self.logger.handlers:
            # Configurar saída para console com Rich — em STDERR, junto com o
            # restante do trace de diagnóstico (stdout fica só para resultados)
            console_handler = RichHandler(console=self.err_console, rich_tracebacks=True, show_time=False)
            console_handler.setLevel(logging.DEBUG)
            
            # Rotação de arquivo conforme configuração (evita crescimento ilimitado)
            max_bytes = getattr(setting, 'STRX_LOG_MAX_FILE_SIZE', 10 * 1024 * 1024)
            backup_count = getattr(setting, 'STRX_LOG_BACKUP_COUNT', 5)
            enable_file_logging = getattr(setting, 'STRX_ENABLE_FILE_LOGGING', True)

            # Formato para arquivo (com timestamp)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # Formato para console (sem timestamp para saída limpa)
            console_formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)

            # Referências guardadas (None quando o logging em arquivo está desativado)
            self.file_handler = None
            self.error_file_handler = None

            if enable_file_logging:
                # Configurar saída para arquivo - create directory if needed
                os.makedirs(os.path.dirname(setting.LOG_FILE_OUTPUT), exist_ok=True)
                self.file_handler = RotatingFileHandler(
                    setting.LOG_FILE_OUTPUT, maxBytes=max_bytes, backupCount=backup_count
                )
                self.file_handler.setLevel(logging.DEBUG)
                self.file_handler.setFormatter(file_formatter)

                # Configurar arquivo separado para erros
                error_log_path = str(setting.LOG_FILE_OUTPUT).replace('.log', '-errors.log')
                self.error_file_handler = RotatingFileHandler(
                    error_log_path, maxBytes=max_bytes, backupCount=backup_count
                )
                self.error_file_handler.setLevel(logging.ERROR)
                self.error_file_handler.setFormatter(file_formatter)

            # Adicionar handlers
            self.logger.addHandler(console_handler)
            if self.file_handler:
                self.logger.addHandler(self.file_handler)
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
        # Sem nível debug ativo, não há saída nem arquivo: evita construir a
        # mensagem e o I/O de disco no caminho quente (early-exit).
        if not self.is_level_active('debug'):
            return
        prefix = f"[{module_name}] " if module_name else ""
        full_message = f"{prefix}{message}"

        # Salva no arquivo
        self.logger.debug(full_message)

        # Trace de diagnóstico no stderr, com tag uniforme
        clean = self._LEADING_TAG.sub('', str(message))
        mod = f"{module_name}: " if module_name else ""
        self.err_console.print(f"[dim][DEBUG] {mod}{clean}[/dim]")
    
    def info(self, message, clean_output=False):
        """Log info messages"""
        if clean_output:
            # Para saída limpa (resultados), sempre mostra sem formatação
            self.console.print(message)
            # Ainda salva no arquivo
            if self.file_handler:
                self.file_handler.handle(self.logger.makeRecord(
                    self.logger.name, logging.INFO, __file__, 0, message, (), None
                ))
        elif self.is_level_active('info'):
            # Mostra no console E salva no arquivo se nível 1 (info) estiver ativo
            self.logger.info(message)
        else:
            # Apenas salva no arquivo, não mostra no console
            if self.file_handler:
                self.file_handler.handle(self.logger.makeRecord(
                    self.logger.name, logging.INFO, __file__, 0, message, (), None
                ))
    
    def warning(self, message):
        """Log warning messages"""
        if self.is_level_active('warning'):
            # Mostra no console E salva no arquivo se nível 2 (warning) estiver ativo
            self.logger.warning(message)
        else:
            # Apenas salva no arquivo, não mostra no console
            if self.file_handler:
                self.file_handler.handle(self.logger.makeRecord(
                    self.logger.name, logging.WARNING, __file__, 0, message, (), None
                ))
    
    def error(self, message):
        """Log error messages"""
        # Salva no arquivo de erros separado (quando logging em arquivo ativo)
        if getattr(self, 'error_file_handler', None):
            error_record = self.logger.makeRecord(
                self.logger.name, logging.ERROR, __file__, 0, message, (), None
            )
            self.error_file_handler.handle(error_record)
        
        # Mostra no stderr apenas se nível 4 (error) estiver ativo
        if self.is_level_active('error'):
            self.err_console.print(f"[bold red][ERROR][/bold red] {message}")
    
    def exception(self, message):
        """Log exception messages with traceback"""
        # Salva no arquivo de erros separado (quando logging em arquivo ativo)
        if getattr(self, 'error_file_handler', None):
            error_record = self.logger.makeRecord(
                self.logger.name, logging.ERROR, __file__, 0, message, (), None
            )
            self.error_file_handler.handle(error_record)
        
        # Mostra no stderr apenas se nível 5 (exception) estiver ativo
        if self.is_level_active('exception'):
            self.err_console.print(f"[bold red][EXCEPT][/bold red] {message}")
    
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
        # Mensagens verbose só importam quando o nível info está ativo (-v).
        # Sem isso, não construímos a string nem gravamos em disco — corta o
        # I/O síncrono no caminho quente por-string.
        if not self.is_level_active('info'):
            return
        self.logger.debug(f"VERBOSE: {message}")
        clean = self._LEADING_TAG.sub('', str(message))
        self.err_console.print(f"[dim][INFO] {clean}[/dim]")
    
    def log_file_info(self):
        """Log information about output and error files"""
        if getattr(self, 'error_file_handler', None):
            output_file = str(setting.LOG_FILE_OUTPUT)
            error_file = str(setting.LOG_FILE_OUTPUT).replace('.log', '-errors.log')
            
            self.info(f"Results will be saved to: {output_file}")
            self.info(f"Errors will be saved to: {error_file}")

# Global logger instance
logger = Logger()