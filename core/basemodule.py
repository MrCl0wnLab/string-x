"""
Módulo base para criação de módulos auxiliares.

Este módulo contém a classe BaseModule que serve como classe base para todos
os módulos auxiliares do sistema String-X. Define a interface comum e estrutura
básica que todos os módulos devem seguir.
"""
# Bibliotecas padrão
import traceback
from typing import Optional, Any, List, Dict, Type

# Bibliotecas de terceiros
try:
    from requests.exceptions import RequestException
except ImportError:
    RequestException = Exception

try:
    from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException
except ImportError:
    ConnectError = TimeoutException = ReadTimeout = ConnectTimeout = Exception

# Módulos locais
from core.output_formatter import OutputFormatter

class BaseModule:
    """
    Classe base para criação de módulos com funcionalidades específicas.
    
    Cada módulo deve herdar desta classe e implementar o método `run`.
    Fornece estrutura comum para armazenamento de resultados, opções
    e metadados do módulo.
    
    Attributes:
        _result (dict): Dicionário para armazenar resultados, inicializado 
                       com o nome da classe como chave
        options (dict): Dicionário para definir opções específicas do módulo
        meta (dict): Dicionário para armazenar meta-informações sobre o módulo
    
    Methods:
        set_result(value: str): Adiciona um resultado ao dicionário _result
        get_result(): Retorna a lista de resultados armazenados
        _get_cls_name(): Retorna o nome da classe
        run(**kwargs): Método abstrato que deve ser implementado pelas subclasses
        handle_error(e, user_message, raise_error): Trata e registra erros de forma padronizada
    """
    
    def __init__(self):
        """
        Inicializa a classe BaseModule.
        
        Configura estruturas básicas para resultados, opções e metadados
        que serão utilizadas pelos módulos filhos.
        """

        self._result = {f"{self._get_cls_name()}": []}
        self._auto_clear_results = True  # Habilita limpeza automática por padrão


        # Cada módulo deverá definir suas opções (chave: dict com required, description, value)
        self.options = {
            "data": None,
            "proxy": None,
            "debug": None,
            "retry":None,
            'retry_delay': None,
        }

        # Meta-informações do módulo
        self.meta = {
            "name": None, 
            "description": None, 
            "author": None,
            "version": None,
            "type": None
        }
    def _clear_results(self):
        """Limpa todos os resultados armazenados."""
        self._result[self._get_cls_name()].clear()
    
    def set_auto_clear(self, value: bool):
        """
        Define se os resultados devem ser limpos automaticamente.
        
        Args:
            value (bool): True para limpar automaticamente, False caso contrário
        """
        self._auto_clear_results = value

    def set_result(self, value: str):
        """
        Adiciona um resultado à lista de resultados do módulo.
        
        Args:
            value (str): Valor a ser adicionado aos resultados
        """
         # Se auto_clear estiver habilitado e for o primeiro resultado, limpar antes
        if self._auto_clear_results and not self._result.get(self._get_cls_name()):
            self._clear_results()
            
        if value:
            self._result.get(self._get_cls_name()).append(value)


    def get_result(self, plain=False):
        """
        Retorna a lista de resultados armazenados no módulo.
        
        Returns:
            list: Lista contendo todos os resultados encontrados pelo módulo
        """
        if plain:
           # Retorna resultados sem formatação, ícones ou cores
           return list(OutputFormatter._strip_formatting(r) for r in self._results)
        return list(self._result.values())[0]

    def log_debug(self, message):
        """
        Registra uma mensagem de debug se o modo de debug estiver ativado.
        
        Args:
            message (str): Mensagem de log
        """
        if self.options.get('debug'):
            print(f"[{self._get_cls_name()}] {message}")

    def _get_cls_name(self):
        """
        Retorna o nome da classe atual.
        
        Returns:
            str: Nome da classe que herda de BaseModule
        """
        return self.__class__.__name__
    
       
    def run(self, **kwargs):
        """
        Método abstrato que define o comportamento do módulo.
        
        Este método deve ser implementado por todas as subclasses para
        definir a funcionalidade específica do módulo.
        
        Args:
            **kwargs: Argumentos específicos do módulo
            
        Raises:
            NotImplementedError: Se a subclasse não implementar este método
        """
        raise NotImplementedError("Subclasses devem implementar o método run()")
    
    def handle_error(self, e: Exception, user_message: Optional[str] = None, raise_error: bool = False) -> None:
        """
        Método auxiliar para tratar erros de forma padronizada.
        
        Este método centraliza o tratamento de erros para todos os módulos,
        registrando informações técnicas no log de debug e fornecendo
        mensagens mais amigáveis para o usuário final.
        
        Args:
            e: Exceção capturada
            user_message: Mensagem personalizada para o usuário (opcional)
            raise_error: Se True, re-lança a exceção após o registro
            
        Raises:
            Exception: Re-lança a exceção original se raise_error for True
        """
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Mensagem para log (mais técnica)
        log_message = f"{error_type}: {error_msg}"
        self.log_debug(log_message)
        
        # Mensagem para o usuário (mais amigável)
        if user_message:
            user_error_msg = f"{user_message}: {error_msg}"
        else:
            user_error_msg = f"Erro ({error_type}): {error_msg}"
            
        self.log_debug(user_error_msg)
        
        # Registra traceback para erros não esperados
        if not isinstance(e, (ValueError, RequestException, ConnectError, 
                              ReadTimeout, ConnectTimeout, TimeoutException)):
            self.log_debug(traceback.format_exc())
            
        # Re-lança a exceção se necessário
        if raise_error:
            raise