"""
Módulo de processamento com threads.

Este módulo contém a classe ThreadProcess responsável por gerenciar a execução
de tarefas em paralelo usando threads, permitindo melhor performance no
processamento de listas de dados.
"""
# Biblioteca padrão
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Any, Optional

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
    def __init__(self, max_threads: int = None, sleep_delay: float = 0, timeout: int = None):
        """
        Inicializa a classe ThreadProcess com configurações padrão.
        
        Args:
            max_threads: Número máximo de threads simultâneas
            sleep_delay: Delay entre submissões de tarefas (segundos)
            timeout: Timeout para execução de tarefas (segundos)
        """
        # Configuração via parâmetros ou settings
        try:
            from stringx.config import setting
            self.max_thread = max_threads or getattr(setting, 'STRX_MAX_THREADS', 10)
            self._sleep = sleep_delay or getattr(setting, 'STRX_THREAD_SLEEP', 0)
            self._timeout = timeout or getattr(setting, 'STRX_THREAD_TIMEOUT', 300)
        except ImportError:
            self.max_thread = max_threads or 10
            self._sleep = sleep_delay or 0
            self._timeout = timeout or 300
            
        self._cli = StyleCli()
        self._logger = logging.getLogger(__name__)
        
        # Validate configuration
        if self.max_thread <= 0:
            raise ValueError("max_thread must be positive")
        if self._timeout <= 0:
            raise ValueError("timeout must be positive")

    def exec_thread(self, function_name: Callable, command_str: str, target_list: List[str], argparse: Any) -> List[Any]:
        """
        Executa uma função em múltiplas threads para uma lista de alvos.
        
        Este método usa ThreadPoolExecutor para gerenciar threads de forma mais eficiente,
        processando os alvos em lotes controlados.
        
        Args:
            function_name: Função a ser executada em cada thread
            command_str: String de comando a ser passada para a função
            target_list: Lista de alvos para processamento
            argparse: Argumentos da linha de comando
            
        Returns:
            Lista com os resultados das execuções
        """
        if not all([function_name, command_str, target_list]):
            self._logger.warning("Invalid parameters provided to exec_thread")
            return []
            
        results = []
        failed_targets = []
        
        try:
            with ThreadPoolExecutor(max_workers=self.max_thread) as executor:
                # Submit all tasks first
                futures = {}
                for tgt_str in target_list:
                    if tgt_str:
                        future = executor.submit(function_name, tgt_str, command_str, argparse)
                        futures[future] = tgt_str
                
                # Add sleep delay after all submissions if configured
                if self._sleep > 0:
                    time.sleep(self._sleep)
                
                # Process completed tasks as they finish
                for future in as_completed(futures, timeout=self._timeout):
                    target = futures[future]
                    try:
                        result = future.result(timeout=1)  # Quick timeout per task
                        results.append(result)
                    except Exception as e:
                        failed_targets.append(target)
                        self._logger.error(f"Task failed for target '{target}': {e}")
                        
        except Exception as e:
            self._logger.error(f"Critical error in thread execution: {e}")
            raise
        
        if failed_targets:
            self._logger.warning(f"Failed to process {len(failed_targets)} targets: {failed_targets[:5]}...")
            
        return results

    def main_pool_thread(self, function_name: Callable, target: str, command: str, exploit: list) -> Any:
        """
        Executa uma função usando ThreadPoolExecutor para um único alvo.
        
        Args:
            function_name: Função a ser executada
            target: Alvo único para processamento
            command: Comando a ser executado
            exploit: Lista de exploits ou dados adicionais
            
        Returns:
            Resultado da execução do pool de threads
        """
        return self.setting_main_pool_thread(function_name, [target], [command], [exploit])

    def setting_main_pool_thread(self, function_name: Callable, target: List[str], command: List[str], exploit: List[list]) -> List[Any]:
        """
        Configura e executa um pool de threads com ThreadPoolExecutor.
        
        Args:
            function_name: Função a ser executada em cada worker
            target: Lista de alvos para processamento
            command: Lista de comandos
            exploit: Lista de exploits ou dados adicionais
            
        Returns:
            Lista com os resultados das execuções
        """
        try:
            with ThreadPoolExecutor(max_workers=self.max_thread) as executor:
                results = list(executor.map(function_name, target, command, exploit))
                return results
        except Exception as e:
            self._logger.error(f"Error in thread pool execution: {e}")
            raise
