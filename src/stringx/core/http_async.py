"""
Cliente HTTP assíncrono para o String-X.

Este módulo implementa um cliente HTTP assíncrono utilizando a biblioteca httpx
para realizar requisições paralelas, manipular respostas e processar resultados
de forma eficiente.
"""
# Biblioteca padrão
import asyncio
from typing import Optional, Dict, Any, List, Tuple, Set, Union

# Bibliotecas de terceiros
import httpx
from httpx import Response, HTTPError, ConnectError, TimeoutException, ReadTimeout, ConnectTimeout

# Módulos locais
from stringx.core.format import Format
from stringx.core.style_cli import StyleCli

class HTTPClient:
    """
    Cliente HTTP assíncrono para realizar requisições em paralelo.
    
    Esta classe encapsula funcionalidades para realizar requisições HTTP
    assíncronas utilizando a biblioteca httpx, permitindo execução
    paralela, manipulação de respostas e extração de dados.
    
    Attributes:
        CLIENT_PARAMS (Set[str]): Conjunto de parâmetros válidos para configuração do cliente httpx
        REQUEST_PARAMS (Set[str]): Conjunto de parâmetros válidos para métodos de requisição
    """
    # Parâmetros válidos para configurar o cliente httpx
    CLIENT_PARAMS = {
        'auth', 'params', 'headers', 'cookies', 'verify', 'cert', 
        'http1', 'http2', 'proxies', 'mounts', 'timeout','proxy', 
        'follow_redirects', 'limits', 'event_hooks', 'base_url',
        'transport', 'app', 'trust_env', 'default_encoding'
    }
    
    # Parâmetros válidos para os métodos de requisição (get, post, etc.)
    REQUEST_PARAMS = {
        'params', 'headers', 'cookies', 'auth', 'follow_redirects',
        'timeout', 'extensions', 'content', 'data', 'files', 'json'
    }
    
    def __init__(self, **kwargs):
        """
        Inicializa o cliente HTTP assíncrono.
        
        Args:
            **kwargs: Argumentos de configuração para o cliente HTTP
        """
        self._cli = StyleCli()
        
    @staticmethod
    def _get_title(html: str) -> str:
        """
        Extrai o título de uma página HTML.
        
        Este método utiliza expressões regulares para extrair o conteúdo
        da tag <title> de uma página HTML, limpando e formatando o resultado.
        
        Args:
            html (str): Conteúdo HTML da página
            
        Returns:
            str: Título extraído da página ou string vazia
        """
        if html:
            title = Format.clear_value(Format.regex(html, r'<title[^>]*>([^<]+)</title>')[0])
            title = title.replace("'", "")
            if title:
                return title
        return str()
    
    def _split_params(self, kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Divide os parâmetros em dois grupos: parâmetros do cliente e parâmetros da requisição.
        
        Este método separa os parâmetros recebidos em dois dicionários diferentes,
        um para configuração do cliente httpx e outro para os métodos de requisição,
        de acordo com a documentação da biblioteca.
        
        Args:
            kwargs (Dict[str, Any]): Parâmetros recebidos para configuração
            
        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: Tupla contendo dois dicionários:
                (parâmetros do cliente, parâmetros da requisição)
        """
        client_params = {'verify': False}  # Valor padrão
        request_params = {}
        
        for key, value in kwargs.items():
            if key in self.CLIENT_PARAMS:
                client_params[key] = value
            if key in self.REQUEST_PARAMS:
                request_params[key] = value
                
        return client_params, request_params
    
    async def _get_async(self, url: str, **kwargs) -> Response:
        """
        Realiza uma requisição GET assíncrona.
        
        Args:
            url (str): URL para a requisição GET
            **kwargs: Parâmetros adicionais para a configuração do cliente e requisição
            
        Returns:
            Response: Objeto de resposta da requisição
            
        Raises:
            HTTPError: Erro na comunicação HTTP
        """
        client_params, request_params = self._split_params(kwargs)
            
        async with httpx.AsyncClient(**client_params) as client:
            return await client.get(url, **request_params)
    
    async def _post_async(self, url: str, **kwargs) -> Response:
        """
        Realiza uma requisição POST assíncrona.
        
        Args:
            url (str): URL para a requisição POST
            **kwargs: Parâmetros adicionais para a configuração do cliente e requisição
            
        Returns:
            Response: Objeto de resposta da requisição
            
        Raises:
            HTTPError: Erro na comunicação HTTP
        """
        client_params, request_params = self._split_params(kwargs)
            
        async with httpx.AsyncClient(**client_params) as client:
            return await client.post(url, **request_params)
    
    async def _fetch_all(self, urls: List[str], max_concurrent: int = 10, **kwargs) -> List[Union[Response, Exception]]:
        """
        Faz requisições assíncronas para uma lista de URLs com limite de concorrência.
        
        Este método implementa um mecanismo para realizar múltiplas requisições HTTP
        em paralelo, controlando o número máximo de requisições simultâneas para
        evitar sobrecarga e respeitar limites de recursos.
        
        Args:
            urls (List[str]): Lista de URLs para requisição
            max_concurrent (int): Número máximo de requisições simultâneas
            **kwargs: Argumentos adicionais para a configuração do cliente e requisição
        
        Returns:
            List[Union[Response, Exception]]: Lista de respostas das requisições ou exceções
        """
        # Semáforo para limitar o número de requisições simultâneas
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def _fetch_url(url: str) -> Union[Response, Exception]:
            """Função interna para realizar requisição com controle de semáforo"""
            async with semaphore:
                try:
                    return await self._get_async(url, **kwargs)
                except HTTPError as e:
                    return e
                except ConnectError as e:
                    return e
                except TimeoutException as e:
                    return e
                except Exception as e:
                    return e
        
        # Criar tarefas para cada URL
        tasks = [_fetch_url(url) for url in urls]
        
        # Executar todas as tarefas concorrentemente
        return await asyncio.gather(*tasks)
    
    async def send_request(self, target_list: List[str], **kwargs) -> List[Union[Response, Exception]]:
        """
        Executa requisições assíncronas para uma lista de URLs.
        
        Este é o método principal para realizar requisições HTTP paralelas.
        Recebe uma lista de URLs e parâmetros adicionais, gerencia o processo
        de requisição e retorna os resultados.
        
        Args:
            target_list (List[str]): Lista de URLs para requisição
            **kwargs: Parâmetros adicionais para configuração do cliente e requisição
            
        Returns:
            List[Union[Response, Exception]]: Lista de respostas ou exceções para cada URL
            
        Raises:
            Exception: Erro geral durante o processo de requisição
        """
        try:
            # Capturar o resultado
            results = await self._fetch_all(target_list, **kwargs)
            return results
        except asyncio.CancelledError:
            self._cli.print_error("Requisições canceladas")
            return []
        except Exception as e:
            self._cli.print_error(f"Erro na coleta: {e}")
            return []