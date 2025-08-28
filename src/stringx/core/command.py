"""
Módulo responsável pela execução de comandos e manipulação de templates.

Este módulo contém a classe Command que é responsável por processar templates de comandos,
executar os comandos no sistema operacional e gerenciar a saída dos resultados.
"""

# Biblioteca padrão
import re
import os
import time
import hashlib
import shlex
import argparse
import subprocess
import logging.config

# Módulos locais
from stringx.config import setting
from stringx.core.format import Format
from stringx.core.func_format import FuncFormat
from stringx.core.style_cli import StyleCli
from stringx.core.filelocal import FileLocal
from stringx.core.auto_module import AutoModulo
from stringx.core.output_formatter import OutputFormatter
from stringx.core.logger import logger
from stringx.core.notify import notification_manager

class Command:
    """
    Classe responsável pela execução de comandos e processamento de templates.
    
    Esta classe gerencia a execução de comandos baseados em templates, processamento
    de funções customizadas, módulos automáticos e gerenciamento de logs.
    
    Attributes:
        _file (FileLocal): Instância para manipulação de arquivos
        _format_func (FuncFormat): Instância para formatação de funções
        _cli (StyleCli): Instância para interface CLI estilizada
        _print_func (bool): Flag para imprimir resultados de funções
        _output_func (bool): Flag para salvar resultados de funções
        _print_result_module (bool): Flag para imprimir apenas resultados de módulos
        _filter (str): Filtro para strings de entrada
        _sleep (int): Tempo de delay entre execuções
        file_output (str): Caminho do arquivo de saída
        file_last_output (str): Caminho do arquivo do último valor
        last_value (str): Último valor processado
        verbose (bool): Flag para modo verboso
        _type_module (str): Tipo de módulo a ser executado
    """
    def __init__(self,):
        """
        Inicializa a classe Command com configurações padrão.
        
        Configura todas as variáveis necessárias e inicializa o sistema de logging.
        """
        self._file = FileLocal()
        self._format_func = FuncFormat()
        self._cli = StyleCli()
        self._current_module: str = str()
        self._current_function: str = str()
        self._print_func: bool = False
        self._output_func: bool = False
        self._print_result_module: bool = False
        self._print_module_chain: bool = False  # Flag para imprimir resultados de cada módulo na cadeia
        self._filter: str = str()
        self._filter_function: str = str()  # iff filter
        self._filter_module: str = str()    # ifm filter
        self._sleep: int = int()
        self.file_output: str = str()
        self.file_last_output: str = str()
        self.last_value: str = str()
        self.verbose: bool = False
        self._type_module: str = str()
        self._proxy : str = str()
        self.output_format: str = "txt"
        self._retry: int = int()
        self._retry_delay: int = int()
        self._no_shell: bool = False  # Flag for no-shell mode

        # Command execution cache to avoid duplicates
        self._command_cache: set = set()
        
        # Error tracking to avoid spam
        self._error_count: dict = {}
        self._max_same_errors: int = 5

        self._logging_config = {
            "version": 1,
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "http",
                    "stream": "ext://sys.stderr"
                }
            },
            "formatters": {
                "http": {
                    "format": "%(levelname)s [%(asctime)s] %(name)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M",
                }
            },
            'loggers': {
                'httpx': {
                    'handlers': ['default'],
                    'level': 'CRITICAL',
                },
                'httpcore': {
                    'handlers': ['default'],
                    'level': 'CRITICAL',
                },
            }
        }
        self._set_logging()

    def _set_logging(self) -> None:
        """
        Configura o sistema de logging da aplicação.
        
        Estabelece as configurações de logging para a aplicação e bibliotecas externas,
        definindo níveis críticos para httpx e httpcore para reduzir verbosidade.
        """
        logging.basicConfig(
            format='%(message)s',
        )
        logging.config.dictConfig(self._logging_config)
        logging.getLogger()

    def _save_command_log(self, value: str) -> None:
        """
        Salva o resultado de um comando no arquivo de log.
        
        Args:
            value (str): Valor a ser salvo no arquivo de log
        """
        if not value:
            return 
        
        if value:
            try:
                # Formatar a saída de acordo com o formato especificado
                formatted_output = OutputFormatter.format(
                    self.output_format, 
                    value, 
                    module=self._current_module,
                    function=self._current_function
                )
                
                # Verificar se o file_output está configurado
                if not self.file_output:
                    logger.error("Caminho de saída não definido!")
                    return

                # Garantir que o nome do arquivo tenha um diretório válido
                output_dir = os.path.dirname(self.file_output)
                
                # Se o diretório for vazio (arquivo no diretório atual), não precisa criar
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

                # Criar diretório de logs se não existir
                # os.makedirs(os.path.dirname(self.file_output), exist_ok=True)
                
                # Abrir arquivo e escrever saída formatada
                self._file.save_value(f"{formatted_output}\n", self.file_output)
                '''with open(self.file_output, 'a+') as file_a:
                    file_a.write(f"{formatted_output}\n")'''
                
                # Salvar último valor processado
                self._save_last_target(formatted_output)
                '''with open(self.file_last_output, 'w+') as file_w:
                    file_w.write(str(value))'''
            except Exception as e:
                logger.error(f"Erro ao salvar arquivo: {str(e)}")

    def _save_last_target(self, value: str) -> None:
        """
        Salva o último valor processado em arquivo específico.
        
        Args:
            value (str): Último valor processado
        """
        if value:
            self.last_value = value
            self._file.save_last_value(f"{value}\n", file=self.file_last_output)

    @staticmethod
    def _shlex(command: str) -> list[str]:
        """
        Converte uma string de comando em lista usando shlex.
        
        Args:
            command (str): Comando a ser convertido
            
        Returns:
            list[str]: Lista com os argumentos do comando
        """
        if command:
            return shlex.split(f"{command}")

    def _filter_module_results(self, results: list, module_name: str) -> list:
        """
        Aplica filtro aos resultados dos módulos baseado no parâmetro -ifm.
        
        Args:
            results (list): Lista de resultados do módulo
            module_name (str): Nome do módulo para logs
            
        Returns:
            list: Lista filtrada de resultados
        """
        if not self._filter_module or not results:
            return results
            
        filtered_results = []
        for result in results:
            if result and self._filter_module in result:
                logger.verbose(f"[!] MODULE FILTER MATCH [{module_name}]: {result}")
                filtered_results.append(result)
            elif result:
                logger.verbose(f"[X] MODULE FILTER [{module_name}]: {result}")
                
        return filtered_results

    def _exec_module(self, _type_module: str, data: str) -> AutoModulo | None:
        """
        Executa um ou mais módulos automáticos com os dados fornecidos.
        
        Suporta encadeamento de módulos utilizando o caractere pipe (|).
        Exemplo: 'ext:url|ext:domain|clc:dns'
        
        Args:
            _type_module (str): Tipo do(s) módulo(s) no formato 'tipo1:nome1|tipo2:nome2|...'
            data (str): Dados iniciais a serem processados pelos módulos
            
        Returns:
            AutoModulo | None: Instância do último módulo executado ou None se houver erro
        """
        if not _type_module or ":" not in _type_module or data is None:
            return None
            
        # Verifica se há múltiplos módulos encadeados
        if "|" in _type_module:
            modules = _type_module.split("|")
            current_data = data
            last_module = None
            
            # Executa cada módulo na cadeia
            for i, module_spec in enumerate(modules):
                module_spec = module_spec.strip()  # Remove espaços em branco
                if not module_spec or ":" not in module_spec:
                    continue
                    
                logger.verbose(f"[+] Executando módulo {i+1}/{len(modules)}: {module_spec}")
                auto_load = AutoModulo(module_spec)
                if obj_module := auto_load.load_module():
                    # Update current module name
                    self._current_module = module_spec
                    # Track module usage for notifications
                    if notification_manager.enabled:
                        notification_manager.add_module_used(module_spec)
                    
                    # Se estiver usando -pmc, cada módulo processa os dados originais
                    # Caso contrário, usa comportamento em cadeia (passando resultados entre módulos)
                    input_data = data if self._print_module_chain else current_data
                    
                    # Check if this is a collector module that needs individual processing
                    module_type = obj_module.meta.get('type', '')
                    is_collector = module_type == 'collector'
                    
                    if is_collector and '\n' in input_data and not self._print_module_chain:
                        # For collector modules in chain mode, process each line individually
                        lines = [line.strip() for line in input_data.split('\n') if line.strip()]
                        logger.verbose(f"[+] Processando {len(lines)} itens individualmente para módulo coletor {module_spec}")
                        
                        # Clear previous results and disable auto-clear for accumulation
                        obj_module._result[obj_module._get_cls_name()].clear()
                        obj_module.set_auto_clear(False)  # Disable auto-clear to accumulate results
                        
                        for line in lines:
                            logger.verbose(f"[+] Processando item: {line}")
                            obj_module.options.update({
                                'data': line, 
                                'proxy': self._proxy, 
                                'retry': self._retry,
                                'retry_delay': self._retry_delay
                            })
                            obj_module.run()
                    else:
                        # Normal processing for non-collector modules or single items
                        obj_module.options.update({
                            'data': input_data, 
                            'proxy': self._proxy, 
                            'retry': self._retry,
                            'retry_delay': self._retry_delay
                        })
                        obj_module.run()
                    
                    # Obter resultados do módulo
                    if results := obj_module.get_result():
                        # Apply module filter if specified
                        filtered_results = self._filter_module_results(results, module_spec)
                        
                        # Se a flag de impressão de módulos encadeados estiver ativa,
                        # imprime os resultados deste módulo separadamente
                        if self._print_module_chain:
                            self._print_module_result(filtered_results, module_spec, i+1, len(modules))
                            # No modo -pmc, não alteramos current_data, cada módulo usa os dados originais
                        else:
                            # No modo normal (sem -pmc), preparamos os dados para o próximo módulo
                            if filtered_results:  # Only proceed if we have filtered results
                                current_data = "\n".join(filtered_results)
                            else:
                                logger.verbose(f"[!] Módulo {module_spec} não retornou resultados após filtragem. Encadeamento interrompido.")
                                break  # Stop chain if no results after filtering
                    else:
                        # Se não houver resultados, interrompe a cadeia no modo normal
                        # No modo -pmc, continua para o próximo módulo com os dados originais
                        if not self._print_module_chain:
                            logger.verbose(f"[!] Módulo {module_spec} não retornou resultados. Encadeamento interrompido.")
                            #return None
                        
                    last_module = obj_module
                else:
                    logger.verbose(f"[!] Falha ao carregar módulo: {module_spec}")
                    #return None
            
            # Retorna o último módulo processado
            return last_module
        else:
            # Comportamento original para um único módulo
            auto_load = AutoModulo(_type_module)
            if obj_module := auto_load.load_module():
                # Update current module name
                self._current_module = _type_module
                # Track module usage for notifications
                if notification_manager.enabled:
                    notification_manager.add_module_used(_type_module)
                obj_module.options.update({
                        'data': data, 
                        'proxy': self._proxy, 
                        'retry': self._retry,
                        'retry_delay': self._retry_delay
                    })
                obj_module.run()
                return obj_module
            return None

    def _exec_direct_processing(self, target: str, command: str) -> None:
        """
        Executa processamento direto de entrada através de módulos/funções sem shell.
        
        Este método implementa a funcionalidade da flag -no-shell, permitindo que
        os dados sejam processados diretamente pelos módulos e funções, sem
        passar por comandos shell intermediários.
        
        Args:
            target (str): Valor alvo original para processamento
            command (str): Template com funções e/ou {STRING} placeholder
        """
        if not command:
            return
        
        logger.verbose("[!] NO-SHELL MODE: Processing directly without shell execution")
        
        # Step 1: Handle template substitution
        processed_command = re.sub(r'\{[sS][tT][rR][iI][nN][gG]\}', target, command)
        logger.verbose(f"[!] TEMPLATE SUBSTITUTION: {command} -> {processed_command}")
        
        # Step 2: Check for functions and process them
        function_result = self._format_function(processed_command)
        if function_result:
            logger.verbose(f"[!] FUNCTION RESULT: {function_result}")
            # If function processing was successful, use the result
            processed_data = function_result
        else:
            # If no functions or function processing failed, use the substituted command
            processed_data = processed_command
        
        # Step 3: If modules are specified, process through modules
        if self._type_module:
            logger.verbose(f"[!] ROUTING TO MODULE: {self._type_module}")
            if object_module := self._exec_module(self._type_module, processed_data):
                if result_module := object_module.get_result():
                    # Apply module filter
                    filtered_results = self._filter_module_results(result_module, self._type_module)
                    if filtered_results:
                        # Handle module chain printing vs normal module output
                        if not self._print_module_chain:
                            result_output = "\n".join(filtered_results)
                            is_chain = "|" in self._type_module
                            if is_chain:
                                modules = self._type_module.split("|")
                                logger.verbose(f"[Chain: {' → '.join(modules)}]")
                            self._print_line_std(result_output, is_module_result=True)
                        # Note: _print_module_chain case is handled inside _exec_module
        else:
            # No modules specified, just output the processed data if functions were involved
            # or if we're in function-only mode
            if function_result and (self._print_func or not self._type_module):
                logger.verbose("[!] NO MODULE: Outputting function result directly")
                self._print_line_std(function_result, is_module_result=False)
            elif not function_result and processed_data != command:
                # Template was substituted but no functions, output if appropriate
                logger.verbose("[!] NO MODULE/FUNCTION: Outputting template substitution")
                self._print_line_std(processed_data, is_module_result=False)

    def _exec_command(self, command: str, pipe_command: str) -> None:
        """
        Executa um comando no sistema operacional com suporte a pipes.
        
        Args:
            command (str): Comando principal a ser executado
            pipe_command (str): Comando de pipe opcional
        """
        if not command:
            return
            
        # Sanitizar e validar comando principal
        command = self._sanitize_command(command)
        if not self._is_valid_command(command):
            logger.verbose(f"[X] Comando inválido ou vazio ignorado: '{command}'")
            return
            
        # Check cache to avoid duplicate executions
        if not self._should_execute_command(command):
            return
            
        # Sanitizar comando de pipe se existir
        if pipe_command:
            pipe_command = self._sanitize_command(pipe_command)
            if not self._is_valid_command(pipe_command):
                logger.verbose(f"[X] Comando de pipe inválido ignorado: '{pipe_command}'")
                pipe_command = None

        # When modules are specified, prioritize sending processed template results
        # directly to modules instead of executing as shell commands
        if self._type_module and command:
                # Check if this looks like a processed template result (contains functions output)
                # by looking for patterns like domain; hash or similar structured data
                has_semicolon = ';' in command
                has_hash_pattern = bool(re.search(r'[a-fA-F0-9]{32,128}', command))
                has_function_result = has_semicolon or has_hash_pattern
                
                if has_function_result:
                    logger.verbose(f"[!] Sending processed template to module: {command}")
                    if object_module := self._exec_module(self._type_module, command):
                        if result_module := object_module.get_result():
                            # Apply module filter for single module execution too
                            filtered_results = self._filter_module_results(result_module, self._type_module)
                            if filtered_results:  # Only proceed if we have filtered results
                                if not self._print_module_chain:
                                    result_module = "\n".join(filtered_results)
                                    is_chain = "|" in self._type_module
                                    if is_chain:
                                        modules = self._type_module.split("|")
                                        logger.verbose(f"[Chain: {' → '.join(modules)}]")
                                    self._print_line_std(result_module, is_module_result=True)
                    return  # Exit early, don't execute as shell command
        
        first_process = None
        result_command = None
        try:
            # Create initial process
            # Use shell=True for commands with shell operators like ; | & < > 
            shell_operators = [';', '|', '&', '<', '>', '&&', '||', '$(', '`']
            use_shell = any(op in command for op in shell_operators)
            
            try:
                if use_shell:
                    first_process = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding='utf-8'
                    )
                else:
                    first_process = subprocess.Popen(
                        self._shlex(command),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding='utf-8'
                    )
                result_command = first_process
                
                if pipe_command:
                    try:
                        # Create piped process
                        use_shell_pipe = any(op in pipe_command for op in shell_operators)
                        if use_shell_pipe:
                            result_command = subprocess.Popen(
                                pipe_command,
                                shell=True,
                                stdin=first_process.stdout,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8'
                            )
                        else:
                            result_command = subprocess.Popen(
                                self._shlex(pipe_command),
                                stdin=first_process.stdout,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8'
                            )
                        # Close the first process stdout so it can terminate
                        if first_process.stdout:
                            first_process.stdout.close()
                    except FileNotFoundError as e:
                        if not self._print_func:
                            logger.error(f"Comando não encontrado: {e}")
                        return
                    except ValueError:
                        return

                # Use communicate() with timeout to prevent hanging
                try:
                    # Use configurable timeout from settings instead of hard-coded value
                    command_timeout = getattr(setting, 'STRX_THREAD_TIMEOUT', 300)
                    stdout_data, stderr_data = result_command.communicate(timeout=command_timeout)
                    
                    if stdout_data:
                        # Process each line of output
                        for line_std in stdout_data.splitlines():
                            if line_std:
                                if not self._print_result_module:
                                    line_std = Format.clear_value(line_std)
                                    self._print_line_std(line_std)
                                if object_module := self._exec_module(self._type_module, line_std):
                                    if result_module := object_module.get_result():
                                        # Apply module filter for shell-based module execution too
                                        filtered_results = self._filter_module_results(result_module, self._type_module)
                                        if filtered_results:  # Only proceed if we have filtered results
                                            # Quando -pmc está ativado, não precisamos imprimir o resultado final aqui
                                            # pois cada módulo já imprime seu próprio resultado
                                            if not self._print_module_chain:
                                                # Formatar o resultado do módulo como texto
                                                result_module = "\n".join(filtered_results)
                                                
                                                # Determinar se o módulo é o último em uma cadeia
                                                is_chain = "|" in self._type_module
                                                if is_chain:
                                                    # No caso de cadeia de módulos, adiciona o nome dos módulos
                                                    modules = self._type_module.split("|")
                                                    logger.verbose(f"[Chain: {' → '.join(modules)}]")  
                        
                                                # Imprimir o resultado final
                                                self._print_line_std(result_module, is_module_result=True)
                    
                    # Melhor tratamento de stderr com filtros para evitar spam
                    if stderr_data and not self._print_func:
                        stderr_lines = stderr_data.strip().split('\n')
                        for stderr_line in stderr_lines:
                            stderr_line = stderr_line.strip()
                            if stderr_line:
                                # Filtrar erros conhecidos que não são críticos
                                if self._should_ignore_stderr(stderr_line):
                                    logger.verbose(f"[!] Stderr ignorado: {stderr_line}")
                                else:
                                    error_msg = f"Command stderr: {stderr_line}"
                                    if self._should_log_error(error_msg):
                                        logger.error(error_msg)
                        
                except subprocess.TimeoutExpired:
                    error_msg = f"Command timed out: {command}"
                    if self._should_log_error(error_msg):
                        logger.error(error_msg)
                    # Kill the process if it times out
                    if result_command:
                        result_command.kill()
                        result_command.wait()
                    if first_process and first_process != result_command:
                        first_process.kill()
                        first_process.wait()
                    
            except FileNotFoundError as e:
                if not self._print_func:
                    error_msg = f"Comando não encontrado: {e}"
                    if self._should_log_error(error_msg):
                        logger.error(error_msg)
            except ValueError as e:
                if not self._print_func:
                    error_msg = f"Erro de valor no comando: {e}"
                    if self._should_log_error(error_msg):
                        logger.error(error_msg)
            except Exception as e:
                error_msg = f"Erro na execução do comando: {e}"
                if self._should_log_error(error_msg):
                    logger.error(error_msg)
        except Exception as e:
            error_msg = f"Erro geral no comando: {e}"
            if self._should_log_error(error_msg):
                logger.error(error_msg)
        finally:
                # Ensure processes are cleaned up
                if result_command:
                    try:
                        result_command.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        result_command.kill()
                        result_command.wait()
                    except:
                        pass
                        
                if first_process and first_process != result_command:
                    try:
                        first_process.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        first_process.kill()
                        first_process.wait()
                    except:
                        pass

    def _print_line_std(self, line_std, is_module_result=False) -> None:
        """
        Imprime uma linha de saída padrão e salva no log.
        
        Args:
            line_std: Linha a ser impressa e salva
            is_module_result: Se True, aplica formatação baseada no output_format
        """
        if line_std:
            # Track result for notifications
            if notification_manager.enabled:
                # Count the number of lines as results
                result_lines = line_std.strip().split('\n') if isinstance(line_std, str) else [str(line_std)]
                notification_manager.add_result(len(result_lines))
            output_to_print = line_std
            
            # Se for resultado de módulo e formato não for txt, aplicar formatação
            if is_module_result and self.output_format != "txt":
                output_to_print = OutputFormatter.format(
                    self.output_format, 
                    line_std, 
                    module=self._current_module
                )
            
            if self.verbose:
                logger.verbose('RESULT')
                logger.result(output_to_print)
            else:
                logger.result(output_to_print)
            
            # Para logs, salvar apenas o resultado original (não formatado)
            # A formatação de arquivo é feita separadamente no _save_command_log
            self._save_command_log(line_std)
            
    def _print_module_result(self, results: list, module_name: str, module_index: int = 0, total_modules: int = 0) -> None:
        """
        Imprime os resultados de um módulo formatados adequadamente.
        
        Esta função é usada pelo parâmetro -pmc para imprimir resultados de cada módulo na cadeia,
        garantindo que cada item seja exibido em sua própria linha. É capaz de processar vários
        tipos de valores, incluindo URLs, listas separadas por delimitadores e valores simples.
        
        Args:
            results (list): Lista de resultados do módulo
            module_name (str): Nome do módulo para exibição
            module_index (int): Índice do módulo na cadeia (se aplicável)
            total_modules (int): Total de módulos na cadeia (se aplicável)
        """

        if not results:
            return

        # Exibe cabeçalho do módulo
        if module_index > 0 and total_modules > 0:
            header = f"[bold cyan][Módulo {module_index}/{total_modules}: {module_name}][/bold cyan]"
        else:
            header = f"[bold cyan][Módulo: {module_name}][/bold cyan]"
            
        logger.verbose(header)
        
        # Processa e exibe cada resultado individualmente
        if self.output_format != "txt":
            # Para formatos não-texto, formatar todos os resultados juntos
            formatted_output = OutputFormatter.format(
                self.output_format, 
                results, 
                module=module_name
            )
            logger.result(formatted_output)
        else:
            # Para formato texto, exibir cada resultado em linha separada
            for result in results:
                if result and result.strip():
                    logger.result(result)
        
        if results:
            # Salva todos os resultados no log (sempre formatado se não for txt)
            if self.output_format != "txt":
                formatted_output = OutputFormatter.format(
                    self.output_format, 
                    results, 
                    module=module_name
                )
                self._save_command_log(formatted_output)
            else:
                result_output = "\n".join(results)
                self._save_command_log(result_output)

    def _format_function(self, command: str) -> str:
        """
        Aplica formatação de funções customizadas em um comando.
        
        Args:
            command (str): Comando a ser formatado
            
        Returns:
            str: Comando formatado com funções processadas
        """
        command_func: str = str()
        try:
            if command:
                # Get the function name if available using regex
                func_match = re.search(r'([a-zA-Z0-9_]+)\(', command)
                if func_match:
                    self._current_function = func_match.group(1)
                    # Track function usage for notifications
                    if notification_manager.enabled:
                        notification_manager.add_function_used(self._current_function)

                command_func = self._format_func.func_format(command)
                
                # Apply function filter if specified
                should_save_function = True  # Track if function result should be saved
                if self._filter_function and command_func:
                    if self._filter_function not in command_func:
                        logger.verbose(f"[X] FUNCTION FILTER: {command_func}")
                        should_save_function = False  # Don't save filtered out results
                        return str()  # Return empty string if filter doesn't match
                    else:
                        logger.verbose(f"[!] FUNCTION FILTER MATCH: {command_func}")
                
                if self._print_func and not (self._type_module and self._print_result_module):
                    if self.verbose:
                        if command_func: 
                            self._cli.console.log(command_func)
                    else:
                        if command_func:
                            if self.output_format != "txt":
                                # Formatar a saída de função
                                formatted = OutputFormatter.format(self.output_format, command_func)
                                self._cli.console.print(formatted)
                            else:
                                self._cli.console.print(command_func)
                
                # Only save function results that pass the filter and are actually displayed to the user
                # Don't save function results when modules are active and printing module results (-pm)
                should_show_function = self._print_func and not (self._type_module and self._print_result_module)
                if (self._output_func or should_show_function) and command_func and should_save_function:
                    self._save_command_log(command_func)
            return command_func
        except Exception:
            pass

    def _sanitize_command(self, command: str) -> str:
        """
        Sanitiza e valida um comando antes da execução.
        
        Args:
            command (str): Comando a ser sanitizado
            
        Returns:
            str: Comando sanitizado ou string vazia se inválido
        """
        if not command or not command.strip():
            return ""
            
        # Remove caracteres de controle e quebras de linha problemáticas
        sanitized = command.strip()
        
        # Remove múltiplas quebras de linha consecutivas
        sanitized = re.sub(r'\n+', ' ', sanitized)
        
        # Remove caracteres de controle ASCII
        sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', sanitized)
        
        # Verifica se o comando não é apenas espaços em branco
        if not sanitized or not sanitized.strip():
            return ""
            
        # Verifica se o comando não contém apenas caracteres especiais que causam erro
        if re.match(r'^[^a-zA-Z0-9/._-]*$', sanitized):
            return ""
            
        return sanitized

    def _is_valid_command(self, command: str) -> bool:
        """
        Verifica se um comando é válido para execução.
        
        Args:
            command (str): Comando a ser validado
            
        Returns:
            bool: True se o comando for válido
        """
        if not command or not command.strip():
            return False
            
        # Lista de padrões que indicam comandos potencialmente problemáticos
        invalid_patterns = [
            r'^\s*$',  # Apenas espaços em branco
            r'^\s*\n+\s*$',  # Apenas quebras de linha
            r'^\s*[;&|]+\s*$',  # Apenas operadores shell
            r'^\s*[<>]+\s*$',  # Apenas redirecionamentos
        ]
        
        for pattern in invalid_patterns:
            if re.match(pattern, command):
                return False
                
        return True

    def _should_execute_command(self, command: str) -> bool:
        """
        Verifica se um comando deve ser executado baseado no cache.
        
        Args:
            command (str): Comando a ser verificado
            
        Returns:
            bool: True se o comando deve ser executado
        """
        # Generate a simple hash for the command to use as cache key
        command_hash = hashlib.md5(command.encode()).hexdigest()
        
        if command_hash in self._command_cache:
            logger.verbose(f"[!] Comando já executado (cache): {command}")
            return False
            
        # Add to cache
        self._command_cache.add(command_hash)
        return True

    def _should_log_error(self, error_msg: str) -> bool:
        """
        Verifica se um erro deve ser logado baseado na frequência.
        
        Args:
            error_msg (str): Mensagem de erro
            
        Returns:
            bool: True se o erro deve ser logado
        """
        # Generate a simple hash for the error message
        error_hash = hashlib.md5(error_msg.encode()).hexdigest()
        
        # Track error count
        self._error_count[error_hash] = self._error_count.get(error_hash, 0) + 1
        
        # Only log if we haven't exceeded the limit
        if self._error_count[error_hash] <= self._max_same_errors:
            return True
        elif self._error_count[error_hash] == self._max_same_errors + 1:
            # Log one final message about suppression
            logger.error(f"Suprimindo erros similares (máximo {self._max_same_errors} atingido)")
            return False
            
        return False

    def _should_ignore_stderr(self, stderr_line: str) -> bool:
        """
        Determina se uma linha de stderr deve ser ignorada para reduzir spam.
        
        Args:
            stderr_line (str): Linha de stderr a ser analisada
            
        Returns:
            bool: True se a linha deve ser ignorada
        """
        # Lista de padrões de erro que são comuns e não críticos
        ignore_patterns = [
            r'erro de sintaxe próximo ao token inesperado.*newline',  # Syntax error with newline
            r'syntax error near unexpected token.*newline',
            r'linha\s+\d+:\s*$',  # Empty line error
            r'^\s*$',  # Empty lines
            r'warning.*deprecated',  # Deprecation warnings
            r'warning.*insecure',  # Insecure warnings
            r'% Total.*% Received.*% Xferd.*Average Speed',  # curl progress header
            r'Dload\s+Upload\s+Total\s+Spent\s+Left\s+Speed',  # curl progress header
            r'^\s*\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+.*--:--:--.*--:--:--.*--:--:--\s*\d*$',  # curl progress line
            r'^\s*\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+--:--:--.*$',  # curl progress numbers
        ]
        
        for pattern in ignore_patterns:
            if re.search(pattern, stderr_line, re.IGNORECASE):
                return True
                
        return False

    def _command_prepare(self, target: str, command: str) -> str:
        """
        Prepara um comando substituindo placeholders e aplicando formatações.
        
        Args:
            target (str): Valor alvo a ser substituído no placeholder {STRING}
            command (str): Template do comando
            
        Returns:
            str: Comando preparado para execução
        """
        try:
            if not target or not command:
                return str()
                
            # Clean target value to avoid injection
            target = Format.clear_value(target)
            if not target or not target.strip():
                return str()
                
            # Replace both {STRING} and {string} with the target value
            command_target = re.sub(r'\{[sS][tT][rR][iI][nN][gG]\}', target, command)
            command_target = self._format_function(command_target)
            
            if command_target and command_target.strip():
                # Validar se o comando preparado não está vazio ou malformado
                sanitized = self._sanitize_command(command_target)
                if self._is_valid_command(sanitized):
                    return sanitized
                else:
                    logger.verbose(f"[X] Comando preparado inválido: '{command_target}' -> ignorado")
                    
            return str()
        except Exception as e:
            logger.verbose(f"[X] Erro ao preparar comando: {e}")
            return str()

    def command_template(self, target: str, command: str, args: argparse.Namespace):
        """
        Processa um template de comando com um valor alvo específico.
        
        Este é o método principal que coordena todo o processamento de um comando,
        incluindo filtros, delays, verbose mode e execução de pipes.
        
        Args:
            target (str): Valor alvo para substituição no template
            command (str): Template do comando a ser executado
            args (argparse.Namespace): Argumentos da linha de comando
        """
        if target and command:
            target = Format.clear_value(target)
            self._save_last_target(target)

            self._print_func = args.pf
            self._output_func = args.of
            self._filter = args.filter
            self._filter_function = args.iff
            self._filter_module = args.ifm
            self._sleep = args.sleep
            self._type_module = args.module
            self._print_result_module = args.pm
            self._print_module_chain = args.pmc
            self._proxy = args.proxy
            self._retry = int(args.retry)
            self._retry_delay = int(args.retry_delay)
            self._no_shell = getattr(args, 'no_shell', False)  # Handle no-shell flag
            
            # Set output format
            if hasattr(args, 'format') and args.format:
                self.output_format = args.format
            
            # Reset module and function information
            self._current_module = str()
            self._current_function = str()

            if self._sleep: time.sleep(int(self._sleep))

            if self._filter:
                if self._filter not in target:
                    return logger.verbose(f"[X] IF VALUE: {target}")
                elif self._filter in target:
                    logger.verbose(f"[!] IF VALUE: {target}")

            try:
                # Check if no-shell mode is active and route accordingly
                if self._no_shell:
                    logger.verbose(f"[!] TEMPLATE: {command}")
                    logger.verbose("[!] NO-SHELL MODE ACTIVATED")
                    return self._exec_direct_processing(target, command)
                else:
                    # Traditional shell-based processing
                    command_target = self._command_prepare(target, command)
                    command_pipe = self._command_prepare(target, args.pipe)
                    if command: logger.verbose(f"[!] TEMPLATE: {command}")
                    if command_target: logger.verbose(f"[!] COMMAND: {command_target}")
                    if command_pipe: logger.verbose(f"[!] PIPE: {command_pipe}")
                    return self._exec_command(command_target, command_pipe)
            except Exception:
                pass
