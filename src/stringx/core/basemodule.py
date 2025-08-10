"""
Módulo base para criação de módulos auxiliares.

Este módulo contém a classe BaseModule que serve como classe base para todos
os módulos auxiliares do sistema String-X. Define a interface comum e estrutura
básica que todos os módulos devem seguir.
"""
# Bibliotecas padrão
import traceback
from typing import Optional, Any, List, Dict, Type, Union

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
from stringx.core.output_formatter import OutputFormatter
from stringx.core.logger import logger
from stringx.config import setting

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
        self.setting = setting
        self._result = {f"{self._get_cls_name()}": []}
        self._auto_clear_results = True  # Habilita limpeza automática por padrão


        # Cada módulo deverá definir suas opções (chave: dict com required, description, value)
        self.options = {
            "data": None,
            "proxy": None,
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

    def set_result(self, value: Union[str, List[str], Dict[str, Any]]):
        """
        Adiciona um resultado à lista de resultados do módulo.
        
        Args:
            value: Valor a ser adicionado aos resultados (string, lista ou dicionário)
        """
         # Se auto_clear estiver habilitado e for o primeiro resultado, limpar antes
        if self._auto_clear_results and not self._result.get(self._get_cls_name()):
            self._clear_results()
            
        if value:
            if isinstance(value, list):
                # Adicionar cada item da lista separadamente
                for item in value:
                    if item:  # Só adiciona se não for vazio
                        self._result.get(self._get_cls_name()).append(str(item))
            else:
                self._result.get(self._get_cls_name()).append(str(value))

    def set_result_list(self, values: List[Union[str, Dict[str, Any]]]):
        """
        Adiciona múltiplos resultados estruturados à lista.
        
        Args:
            values (List): Lista de valores a serem adicionados
        """
        if self._auto_clear_results and not self._result.get(self._get_cls_name()):
            self._clear_results()
            
        for value in values:
            if value:
                if isinstance(value, dict):
                    # Se for dicionário com 'type' e 'value', formatar apropriadamente
                    if 'type' in value and 'value' in value:
                        formatted = f"{value['type']}: {value['value']}"
                        self._result.get(self._get_cls_name()).append(formatted)
                    else:
                        self._result.get(self._get_cls_name()).append(str(value))
                else:
                    self._result.get(self._get_cls_name()).append(str(value))

    def set_result_structured(self, results: List[Dict[str, Any]]):
        """
        Adiciona resultados em formato estruturado.
        
        Args:
            results: Lista de dicionários com estrutura {'type': str, 'value': str}
        """
        if self._auto_clear_results and not self._result.get(self._get_cls_name()):
            self._clear_results()
            
        for result in results:
            if isinstance(result, dict) and 'type' in result and 'value' in result:
                formatted = f"{result['type']}: {result['value']}"
                self._result.get(self._get_cls_name()).append(formatted)
            else:
                self._result.get(self._get_cls_name()).append(str(result))


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
        Registra uma mensagem de debug.
        
        Args:
            message (str): Mensagem de log
        """
        logger.debug(message, module_name=self._get_cls_name())

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
        logger.debug(log_message, module_name=self._get_cls_name())
        
        # Mensagem para o usuário (mais amigável)
        if user_message:
            user_error_msg = f"{user_message}: {error_msg}"
            logger.error(user_error_msg)
        else:
            user_error_msg = f"Erro ({error_type}): {error_msg}"
            logger.error(user_error_msg)
        
        # Registra traceback para erros não esperados
        if not isinstance(e, (ValueError, RequestException, ConnectError, 
                              ReadTimeout, ConnectTimeout, TimeoutException)):
            logger.exception(f"Traceback completo para {error_type}")
            logger.debug(traceback.format_exc(), module_name=self._get_cls_name())
            
        # Re-lança a exceção se necessário
        if raise_error:
            raise

    def __getstate__(self):
        """
        Customiza o processo de serialização (pickle) removendo referências de módulos.
        
        Returns:
            dict: Estado do objeto sem referências de módulos que não podem ser serializadas
        """
        state = self.__dict__.copy()
        # Remove a referência ao módulo setting para evitar erros de pickle
        if 'setting' in state:
            del state['setting']
        return state
    
    def __setstate__(self, state):
        """
        Customiza o processo de desserialização (unpickle) restaurando referências de módulos.
        
        Args:
            state (dict): Estado do objeto desserializado
        """
        self.__dict__.update(state)
        # Restaura a referência ao módulo setting
        from stringx.config import setting
        self.setting = setting