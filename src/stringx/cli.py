#!/usr/bin/python
"""
String-X (STRX) - Main CLI Entry Point

This module is the main entry point for the String-X tool, a fast and customizable
automation tool developed to assist analysts in various tasks related to string
manipulation in command line.

Author: Cleiton Pinheiro aka MrCl0wn
Email: mrcl0wnlab[@]gmail.com
License: MIT
Version: 1.0.0
"""

import os
import sys
import signal
from typing import List, Optional
from pathlib import Path

# Import modules using new src layout
from stringx.config import setting
from stringx.core.command import Command
from stringx.core.filelocal import FileLocal
from stringx.core.thread_process import ThreadProcess
from stringx.core.style_cli import StyleCli, RichArgumentParser, RawDescriptionHelpFormatter
from stringx.core.help_modules import *
from stringx.core.upgrade_manager import UpgradeManager
from stringx.core.security_validator import SecurityValidator
from stringx.core.notify import notification_manager


def quit_process(signal, frame) -> None:
    """
    Manipula a interrupção do processo por sinal SIGINT (Ctrl+C).
    
    Esta função é chamada quando o usuário pressiona Ctrl+C, permitindo
    uma saída limpa do programa com informações sobre o último arquivo
    de saída e o último valor processado.
    
    Args:
        signal: O sinal recebido
        frame: O frame atual de execução
        
    Returns:
        None
    """
    import os
    import sys
    
    print("\n")
    try:
        CLI.console.log(f" [!] Interrompido pelo usuário (Ctrl+C)")
        CLI.console.log(f" [!] Saindo...")
        CLI.console.log(f" [!] File output: {setting.LOG_FILE_OUTPUT}")
        CLI.console.log(f" [!] Last value: {CMD.last_value}")
    except:
        print(" [!] Processo interrompido pelo usuário")
    
    # Immediate exit without complex cleanup to avoid futures scheduling issues
    os._exit(0)


def stdin_get_list() -> List[str]:
    """
    Lê lista de strings do stdin com suporte a múltiplas codificações.
    Esta função tenta ler dados da entrada padrão (stdin) e processar as linhas
    como uma lista de strings. Ela tenta automaticamente detectar a codificação
    correta tentando, em sequência: utf-8, latin-1, cp1252 e iso-8859-1.
    Se nenhuma codificação for bem-sucedida, usa utf-8 com errors='ignore'.
    Linhas vazias são removidas do resultado final.
    Returns:
        list: Lista de strings não vazias lidas do stdin, com espaços em branco
             no início e fim de cada linha removidos.
        None: Se stdin for um terminal ou se ocorrer um erro (KeyboardInterrupt,
              NameError ou IOError).
    Raises:
        As exceções capturadas internamente são: KeyboardInterrupt, NameError e IOError.
        Outras exceções não tratadas podem ser propagadas.
    """
    
    if not sys.stdin.isatty():
        try:
            # Primeiro, tenta ler os bytes brutos
            stdin_bytes = sys.stdin.buffer.read()
            
            # Tenta decodificar com diferentes codificações
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    stdin_text = stdin_bytes.decode(encoding)
                    stdin_lines = stdin_text.splitlines()
                    return [line.strip() for line in stdin_lines if line.strip()]
                except UnicodeDecodeError:
                    continue
            
            # Se nenhuma codificação funcionar, usa UTF-8 com ignore
            stdin_text = stdin_bytes.decode('utf-8', errors='ignore')
            stdin_lines = stdin_text.splitlines()
            return [line.strip() for line in stdin_lines if line.strip()]
            
        except KeyboardInterrupt:
            CLI.console.print_exception(max_frames=3)
        except NameError:
            CLI.console.print_exception(max_frames=3)
        except IOError:
            CLI.console.print_exception(max_frames=3)
    return None


def open_file(filename: str) -> List[str]:
    """
    Abre um arquivo e retorna seu conteúdo como lista de strings.
    
    Args:
        filename (str): Caminho para o arquivo a ser aberto
        
    Returns:
        list[str]: Lista com as linhas do arquivo ou None se houver erro
    """
    if filename:
        try:
            txt_line, _ = FILE.open_file(filename, 'r')
            if txt_line:
                return txt_line
        except FileNotFoundError:
            CLI.console.log(f"[!] Arquivo não encontrado: {filename}")
        except PermissionError:
            CLI.console.log(f"[!] Permissão negada ao ler: {filename}")
        except UnicodeDecodeError:
            CLI.console.log(f"[!] Erro de decodificação no arquivo: {filename}")


def main(target_str_list: list, template_str: str) -> None:
    """
    Função principal que executa o processamento das strings de entrada.
    
    Esta função recebe uma lista de strings de entrada e um template de comando,
    e executa o processamento usando threads para melhor performance.
    
    Args:
        target_str_list (list): Lista de strings para processar
        template_str (str): Template de comando para executar
        
    Returns:
        None
        
    Raises:
        BrokenPipeError: Quando há erro de pipe quebrado
    """
    # Start execution tracking for notifications
    if notification_manager.enabled:
        notification_manager.start_execution(template_str)
    
    if target_str_list and template_str:
        try:
            if list is type(target_str_list):
                try:
                    THREAD.exec_thread(
                        function_name=CMD.command_template,
                        command_str=template_str,
                        target_list=target_str_list,
                        argparse=ARGS,
                    )
                except MemoryError as e:
                    print(f"[!] ERRO DE MEMÓRIA: {str(e)}")
                    print(f"[!] Reduza o número de threads (-t) ou o tamanho do input")
                    exit(1)
                except Exception as e:
                    try:
                        CLI.console.print_exception(max_frames=3)
                    except Exception:
                        # Fallback if Rich fails to print exception
                        print(f"[!] ERRO: {type(e).__name__}: {str(e)}")
                        exit(1)
        except BrokenPipeError:
            CLI.console.print_exception(max_frames=3)
    
    # End execution tracking and send notification
    if notification_manager.enabled:
        notification_manager.end_execution()


def main_cli():
    """
    Main CLI entry point function for setuptools console_scripts.
    
    This function serves as the main entry point when the package is installed
    and called via the 'strx' command. It contains all the initialization logic
    and argument parsing.
    """
    global CLI, FILE, THREAD, CMD, ARGS
    
    signal.signal(signal.SIGINT, quit_process)
    CLI = StyleCli()
    FILE = FileLocal()
    THREAD = ThreadProcess()
    CMD = Command()

    # Set security resource limits
    SecurityValidator.set_resource_limits()
    
    try:
        parser = RichArgumentParser(
            prog="strx",
            formatter_class=lambda prog: RawDescriptionHelpFormatter(
                prog, max_help_position=60,
                indent_increment=13),
            description=setting.BANNER_HELP
        )
                
        parser.add_argument('-types', help="Lista tipos de módulos", action='store_true')
        parser.add_argument('-examples', help="Lista módulos e exemplos de uso", action='store_true')
        parser.add_argument('-functions', '-funcs', help="Lista funções", action='store_true')
        parser.add_argument('-list', '-l', metavar="file", help="Arquivo com strings para execução", default=None)
        parser.add_argument('-s', metavar="string", help="String única para execução", default=None)
        parser.add_argument('-str', '-st', metavar="cmd", help="String template de comando", default=None)
        parser.add_argument('-out', '-o', metavar="file", help="Arquivo output de valores da execução shell", default=setting.LOG_FILE_OUTPUT)
        parser.add_argument('-pipe', '-p', dest='pipe', metavar="cmd", help="Comando que será executado depois de um pipe |", default=None)
        parser.add_argument('-verbose', '-v', metavar="<levels>", help="Níveis de verbosidade: 1=info, 2=warning, 3=debug, 4=error, 5=exception, all=todos. Ex: -v 1 ou -v 1,2 ou -v all", default=None, required=False)
        parser.add_argument('-thread', '-t', metavar=f"<{setting.STRX_THREAD_MAX}>", help="Quantidade de threads", default=setting.STRX_THREAD_MAX)
        parser.add_argument('-pf', dest='pf', help="Mostrar resultados da execução de função, ignora shell", action='store_true', default=False)
        parser.add_argument('-of', dest='of', help="Habilitar output de valores da execução de função", action='store_true', default=False)
        parser.add_argument('-filter', '-f', dest='filter', metavar="value", help="Valor para filtrar strings para execução", default=None, required=False)
        parser.add_argument('-iff', dest='iff', metavar="value", help="Filtrar resultados de função: retorna apenas resultados que contenham o valor especificado", default=None, required=False)
        parser.add_argument('-ifm', dest='ifm', metavar="value", help="Filtrar resultados de módulo: retorna apenas resultados que contenham o valor especificado", default=None, required=False)
        parser.add_argument('-sleep', metavar="<5>", help="Segundos de delay entre threads", default=None, required=False)
        parser.add_argument('-module', metavar="<type:module>", help="Selecionar o tipo e module, possível usar encadeamento type1:module1|type:module2", default=str(), required=False)
        parser.add_argument('-printmodule', '-pm', dest='pm', help="Mostrar somente resultados de execução do module", action='store_true', default=False)
        parser.add_argument('-pmc', help="Mostrar resultados de cada módulo no encadeamento separadamente (para coletores, preserva o input original)", action='store_true', default=False)
        parser.add_argument('-proxy', help="Setar um proxy para request", default=str(), required=False)
        parser.add_argument('-disable-security',  '-ds', dest='disable_security', help="Disable security validations (use with caution)", action='store_true', default=False)
        parser.add_argument('-no-shell', '-ns', dest='no_shell', help="Process input directly through modules/functions without shell command execution", action='store_true', default=False)
        parser.add_argument('-format', metavar="<format>", help=f"Formato de saída ({', '.join(setting.STRX_OUTPUT_FORMATS)})", default=setting.STRX_DEFAULT_OUTPUT_FORMAT, choices=setting.STRX_OUTPUT_FORMATS)
        parser.add_argument('-upgrade', help="Atualizar String-X via Git", action='store_true')
        parser.add_argument('-retry', '-r', metavar=f"<{setting.STRX_RETRY_OPERATIONS}>", help="Quantidade de tentativas", default=setting.STRX_RETRY_OPERATIONS, required=False)
        parser.add_argument('-retry-delay', '-rd', metavar=f"<{setting.STRX_RETRY_DELAY}>", help="Delay entre tentativas", default=setting.STRX_RETRY_DELAY, required=False)
        parser.add_argument('-notify', help="Enviar notificação desktop ao finalizar a execução", action='store_true', default=False)
        parser.add_argument('-version', action='version', version=f"%(prog)s {setting.__version__}")
        ARGS = parser.parse_args() 

        # Upgrade do String-X
        if ARGS.upgrade:
            CLI.console.print(f"{setting.BANNER_HELP}\n")
            upgrade_manager = UpgradeManager()
            upgrade_manager.upgrade()
            exit(0)

        # Exibe as categorias de módulos disponíveis
        if ARGS.types:
            CLI.console.print(f"{setting.BANNER_HELP}\n")
            exit(show_module_categories())
        
        # Exibe exemplos de uso dos módulos
        if ARGS.examples:
            CLI.console.print(f"{setting.BANNER_HELP}\n")
            exit(show_module_examples())
            
        # Exibe as funções auxiliares disponíveis
        if ARGS.functions:
            CLI.console.print(f"{setting.BANNER_HELP}\n")
            exit(show_helper_functions())
        
        # Define o formato de saída a ser utilizado
        if ARGS.format:
            CMD.output_format = ARGS.format

        # Verifica se o argumento -str foi fornecido quando não estamos em modo de ajuda
        if ARGS.str:
            # Show warning if security is disabled
            if ARGS.disable_security:
                CLI.console.log("[!] Security validations disabled - use with caution!")
            else:
                # Validate command template security only if not disabled
                is_safe, reason = SecurityValidator.validate_command_safety(ARGS.str)
                if not is_safe:
                    CLI.console.log(f"[!] Command template rejected for security: {reason}")
                    CLI.console.log(f"[!] Use -ds to disable security validations if this is a trusted command")
                    exit(1)
            
            # stdin will be handled later in the input processing section
        else:
            parser.error("o argumento -str/-st é obrigatório quando não estiver usando -types, -examples ou -functions")
            
        # Define o número máximo de threads a serem utilizadas
        if ARGS.thread:
            thread_count = int(ARGS.thread)
            
            # Hard limit for memory protection
            if thread_count > 50:
                CLI.console.log(f"[!] ERRO: Número de threads muito alto ({thread_count})")
                CLI.console.log(f"[!] Máximo recomendado: 20 threads para evitar problemas de memória")
                exit(1)
                
            if not ARGS.disable_security and not SecurityValidator.validate_thread_limits(thread_count):
                CLI.console.log(f"[!] Thread count {thread_count} exceeds security limits (max {SecurityValidator.MAX_THREAD_COUNT})")
                CLI.console.log(f"[!] Use -ds to disable security validations if you need more threads")
                exit(1)
            THREAD.max_thread = thread_count

        # Carrega a lista de strings alvo de um arquivo, da entrada direta ou de uma string única
        if ARGS.list:
            target_list = open_file(ARGS.list) if os.path.isfile(str(ARGS.list)) else ARGS.list
        elif ARGS.s:
            # Usa o parâmetro -s para string única, colocando em uma lista
            target_list = [ARGS.s.strip()]
            CLI.console.log(f"[+] Usando string única: {ARGS.s}")
        else:
            # Tenta ler do stdin se não houver lista ou string única
            target_list = stdin_get_list()
            if not target_list:
                # Se não conseguir ler do stdin, exibe a ajuda e sai
                CLI.console.print(f"{setting.BANNER_HELP}\n")
                CLI.console.log("[!] Nenhuma entrada fornecida. Use -l para arquivo, -s para string única ou pipe stdin.")
                exit(1)
            else:
                pass  # stdin was successfully read

        if ARGS.out:
            if setting.LOG_FILE_OUTPUT != ARGS.out:
                CMD.file_output = f'{setting.STRX_LOG_DIRECTORY}/{ARGS.out}'
            else:
                CMD.file_output = ARGS.out
            CMD.file_last_output = setting.LOG_FILE_LAST_PATH

        CMD.verbose = ARGS.verbose
        
        # Configurar níveis de logging baseado no parâmetro -v
        from stringx.core.logger import logger
        logger.set_verbose_levels(ARGS.verbose)
        
        # Configurar o logger para usar o console estilizado
        logger.set_styled_console(CLI.console)

        # Enable notifications if requested
        if ARGS.notify:
            if notification_manager.enable():
                CLI.console.log("[+] Notificações desktop habilitadas")
            else:
                CLI.console.log("[!] Não foi possível habilitar notificações (notify_py não disponível)")

        # Verifica se a lista de alvos não está vazia antes de chamar main
        if target_list:
            # Validate input size for security (only if security not disabled)
            if not ARGS.disable_security:
                if not SecurityValidator.validate_input_size(target_list):
                    CLI.console.log(f"[!] Input data exceeds security limits")
                    CLI.console.log(f"[!] Use -ds to disable security validations if you need to process large datasets")
                    exit(1)
            main(
                target_str_list=target_list,
                template_str=ARGS.str
            )
        else:
            CLI.console.log("[!] Nenhuma string para processar. Use -l para um arquivo ou -s para string única.")
            exit(1)
    except KeyboardInterrupt:
        # Direct exit to avoid complex shutdown procedures
        print("\n [!] Processo interrompido pelo usuário")
        import os
        os._exit(1)
    except SystemError:
        CLI.console.print_exception(max_frames=3)
    except ModuleNotFoundError:
        CLI.console.print_exception(max_frames=3)


if __name__ == '__main__':
    main_cli()