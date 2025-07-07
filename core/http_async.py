# core/http_client.py
import httpx
from typing import Optional, Dict, Any
import asyncio
from core.format import Format
from core.style_cli import StyleCli


class HTTPClient:
    # Parâmetros válidos para configurar o cliente httpx
    CLIENT_PARAMS = {
        'auth', 'params', 'headers', 'cookies', 'verify', 'cert', 
        'http1', 'http2', 'proxies', 'mounts', 'timeout', 
        'follow_redirects', 'limits', 'event_hooks', 'base_url',
        'transport', 'app', 'trust_env', 'default_encoding'
    }
    
    # Parâmetros válidos para os métodos de requisição (get, post, etc.)
    REQUEST_PARAMS = {
        'params', 'headers', 'cookies', 'auth', 'follow_redirects',
        'timeout', 'extensions', 'content', 'data', 'files', 'json'
    }
    
    def __init__(self, **kwargs):
        self._cli = StyleCli()
        
    @staticmethod
    def _get_title(html: str) -> str:
        """
        Extrai o título de uma página HTML.
        
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
    
    def _split_params(self, kwargs: Dict[str, Any]) -> tuple:
        """
        Divide os parâmetros em dois grupos: parâmetros do cliente e parâmetros da requisição.
        
        Args:
            kwargs: Parâmetros recebidos
            
        Returns:
            tuple: (parâmetros do cliente, parâmetros da requisição)
        """
        client_params = {'verify': False}  # Valor padrão
        request_params = {}
        
        for key, value in kwargs.items():
            if key in self.CLIENT_PARAMS:
                client_params[key] = value
            if key in self.REQUEST_PARAMS:
                request_params[key] = value
                
        return client_params, request_params
    
    async def _get_async(self, url: str, **kwargs):
        client_params, request_params = self._split_params(kwargs)
            
        async with httpx.AsyncClient(**client_params) as client:
            return await client.get(url, **request_params)
    
    async def _post_async(self, url: str, **kwargs):
        client_params, request_params = self._split_params(kwargs)
            
        async with httpx.AsyncClient(**client_params) as client:
            return await client.post(url, **request_params)
    
    async def _fetch_all(self, urls: list[str], max_concurrent: int = 10, **kwargs) -> list:
        """
        Faz requisições assíncronas para uma lista de URLs com limite de concorrência.
        
        Args:
            urls (list[str]): Lista de URLs para requisição
            max_concurrent (int): Número máximo de requisições simultâneas
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            list: Lista de respostas das requisições ou exceções
        """
        # Semáforo para limitar o número de requisições simultâneas
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def _fetch_url(url):
            async with semaphore:
                try:
                    return await self._get_async(url, **kwargs)
                except Exception as e:
                    return e
        
        # Criar tarefas para cada URL
        tasks = [_fetch_url(url) for url in urls]
        
        # Executar todas as tarefas concorrentemente
        return await asyncio.gather(*tasks)
    
    # Função assíncrona para executar a coleta
    async def send_request(self, target_list: list[str], **kwargs) -> list:
        try:
            # Capture the result
            results = await self._fetch_all(target_list, **kwargs)
            return results
        except Exception as e:
            print(f"Erro na coleta: {e}")
            return []