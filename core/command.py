"""
Módulo responsável pela execução de comandos e manipulação de templates.

Este módulo contém a classe Command que é responsável por processar templates de comandos,
executar os comandos no sistema operacional e gerenciar a saída dos resultados.
"""

# Biblioteca padrão
import re
import os
import time
import shlex
import argparse
import subprocess
import logging.config

# Módulos locais
from config import setting
from core.format import Format
from core.func_format import FuncFormat
from core.style_cli import StyleCli
from core.filelocal import FileLocal
from core.auto_module import AutoModulo
from core.output_formatter import OutputFormatter
from core.logger import logger

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
                    
                    # Se estiver usando -pmc, cada módulo processa os dados originais
                    # Caso contrário, usa comportamento em cadeia (passando resultados entre módulos)
                    input_data = data if self._print_module_chain else current_data
                    
                    obj_module.options.update({
                        'data': input_data, 
                        'proxy': self._proxy, 
                        'retry': self._retry,
                        'retry_delay': self._retry_delay
                    })
                    obj_module.run()
                    
                    # Obter resultados do módulo
                    if results := obj_module.get_result():
                        # Se a flag de impressão de módulos encadeados estiver ativa,
                        # imprime os resultados deste módulo separadamente
                        if self._print_module_chain:
                            self._print_module_result(results, module_spec, i+1, len(modules))
                            # No modo -pmc, não alteramos current_data, cada módulo usa os dados originais
                        else:
                            # No modo normal (sem -pmc), preparamos os dados para o próximo módulo
                            current_data = "\n".join(results)
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
                obj_module.options.update({
                        'data': data, 
                        'proxy': self._proxy, 
                        'retry': self._retry,
                        'retry_delay': self._retry_delay
                    })
                obj_module.run()
                return obj_module
            return None

    def _exec_command(self, command: str, pipe_command: str) -> None:
        """
        Executa um comando no sistema operacional com suporte a pipes.
        
        Args:
            command (str): Comando principal a ser executado
            pipe_command (str): Comando de pipe opcional
        """
        if command:
            try:
                result_command = subprocess.Popen(
                    self._shlex(command),
                    stdout=subprocess.PIPE,
                    encoding='utf-8'
                )
                if pipe_command:
                    try:
                        result_command = subprocess.Popen(
                            self._shlex(pipe_command),
                            stdin=result_command.stdout,
                            stdout=subprocess.PIPE,
                            encoding='utf-8'
                        )
                    except FileNotFoundError as e:
                        if not self._print_func:
                            logger.error(f"Comando não encontrado: {e}")
                    except ValueError:
                        pass

                if result_command.stdout:
                    for line_std in result_command.stdout:
                        if line_std:
                            if not self._print_result_module:
                                line_std = Format.clear_value(line_std)
                                self._print_line_std(line_std)
                            if object_module := self._exec_module(self._type_module, line_std):
                                if result_module := object_module.get_result():
                                    # Quando -pmc está ativado, não precisamos imprimir o resultado final aqui
                                    # pois cada módulo já imprime seu próprio resultado
                                    if not self._print_module_chain:
                                        # Formatar o resultado do módulo como texto
                                        result_module = "\n".join(result_module)
                                        
                                        # Determinar se o módulo é o último em uma cadeia
                                        is_chain = "|" in self._type_module
                                        if is_chain:
                                            # No caso de cadeia de módulos, adiciona o nome dos módulos
                                            modules = self._type_module.split("|")
                                            logger.verbose(f"[Chain: {' → '.join(modules)}]")  
            
                                        
                                        # Imprimir o resultado final
                                        self._print_line_std(result_module)

            except FileNotFoundError as e:
                if not self._print_func:
                    logger.error(f"Comando não encontrado: {e}")
                pass
            except ValueError:
                pass

    def _print_line_std(self, line_std) -> None:
        """
        Imprime uma linha de saída padrão e salva no log.
        
        Args:
            line_std: Linha a ser impressa e salva
        """
        if line_std:
            if self.verbose:
                logger.verbose('RESULT')
                logger.result(line_std)
            else:
                logger.result(line_std)
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
        for result in results:
            if result and result.strip():
                logger.result(result)
        if results:
            # Salva todos os resultados no log
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

                command_func = self._format_func.func_format(command)
                if self._print_func:
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
                if self._output_func and command_func:
                    self._save_command_log(command_func)
            return command_func
        except Exception:
            pass

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
            if target and command:
                # Replace both {STRING} and {string} with the target value
                command_target = re.sub(r'\{[sS][tT][rR][iI][nN][gG]\}', target, command)
                command_target = self._format_function(command_target)
                if command_target:
                    return command_target
            return str()
        except Exception:
            pass

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
            self._sleep = args.sleep
            self._type_module = args.module
            self._print_result_module = args.pm
            self._print_module_chain = args.pmc
            self._proxy = args.proxy
            self._retry = int(args.retry)
            self._retry_delay = int(args.retry_delay)
            
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
                command_target = self._command_prepare(target, command)
                command_pipe = self._command_prepare(target, args.pipe)
                if command: logger.verbose(f"[!] TEMPLATE: {command}")
                if command_target: logger.verbose(f"[!] COMMAND: {command_target}")
                if command_pipe: logger.verbose(f"[!] PIPE: {command_pipe}")
                return self._exec_command(command_target, command_pipe)
            except Exception:
                pass
