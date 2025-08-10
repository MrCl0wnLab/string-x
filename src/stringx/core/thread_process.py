"""
Módulo de processamento com threads.

Este módulo contém a classe ThreadProcess responsável por gerenciar a execução
de tarefas em paralelo usando threads, permitindo melhor performance no
processamento de listas de dados.
"""
# Biblioteca padrão
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Módulos locais
from stringx.core.style_cli import StyleCli


class ThreadProcess:
    """
    Classe responsável pelo gerenciamento de processamento com threads.
    
    Esta classe fornece métodos para executar funções em paralelo usando
    threading tradicional ou ThreadPoolExecutor, permitindo processamento
    eficiente de grandes volumes de dados.
    
    Attributes:
        max_thread (int): Número máximo de threads simultâneas
        _sleep (int): Tempo de delay entre execuções
        _cli (StyleCli): Instância para interface CLI estilizada
    """
    def __init__(self):
        """
        Inicializa a classe ThreadProcess com configurações padrão.
        """
        self.max_thread = 10
        self._sleep = 0
        self._cli = StyleCli()

    def exec_thread(self, function_name, command_str, target_list, argparse):
        """
        Executa uma função em múltiplas threads para uma lista de alvos.
        
        Este método usa ThreadPoolExecutor para gerenciar threads de forma mais eficiente,
        processando os alvos em lotes controlados.
        
        Args:
            function_name: Função a ser executada em cada thread
            command_str: String de comando a ser passada para a função
            target_list: Lista de alvos para processamento
            argparse: Argumentos da linha de comando
        """
        if function_name and command_str and target_list:
            try:
                # Use ThreadPoolExecutor for better thread management
                with ThreadPoolExecutor(max_workers=self.max_thread) as executor:
                    # Create futures for each target
                    futures = []
                    for tgt_str in target_list:
                        if tgt_str:
                            future = executor.submit(function_name, tgt_str, command_str, argparse)
                            futures.append(future)
                            
                            # Add sleep if configured
                            if self._sleep:
                                time.sleep(int(self._sleep))
                    
                    # Wait for all tasks to complete
                    for future in futures:
                        try:
                            # Use configurable timeout from settings
                            from stringx.config import setting
                            task_timeout = getattr(setting, 'STRX_THREAD_TIMEOUT', 300)
                            future.result(timeout=task_timeout)
                        except Exception as e:
                            # Log error but continue processing other tasks
                            pass
                            
            except Exception:
                pass

    def main_pool_thread(self, function_name, target, command, exploit: list):
        """
        Executa uma função usando ThreadPoolExecutor para um único alvo.
        
        Args:
            function_name: Função a ser executada
            target: Alvo único para processamento
            command: Comando a ser executado
            exploit (list): Lista de exploits ou dados adicionais
            
        Returns:
            Resultado da execução do pool de threads
        """
        return self.setting_main_pool_thread(function_name, [target], [command], [exploit])

    def setting_main_pool_thread(self, function_name, target, command, exploit: list):
        """
        Configura e executa um pool de threads com ThreadPoolExecutor.
        
        Args:
            function_name: Função a ser executada em cada worker
            target: Lista de alvos para processamento
            command: Lista de comandos
            exploit (list): Lista de exploits ou dados adicionais
        """
        try:
            executor = ThreadPoolExecutor(max_workers=self.max_thread)
            executor.map(function_name, target, command, exploit)
            executor.shutdown(wait=True)
            executor.shutdown()
        except Exception:
            pass
