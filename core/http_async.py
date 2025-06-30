# core/http_client.py
import httpx
from typing import Optional
import asyncio
from core.format import Format
from core.style_cli import StyleCli


class HTTPClient:
    def __init__(self):
        self._cli = StyleCli()
        self._client = httpx.Client(
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            timeout=httpx.Timeout(30.0)
        )

        
        

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
    
    async def _get_async(self, url: str, **kwargs):
        async with httpx.AsyncClient(verify=False) as client:
            return await client.get(url, **kwargs)
    
    async def _post_async(self, url: str, **kwargs):
        async with httpx.AsyncClient(verify=False) as client:
            return await client.post(url, **kwargs)
    
    def _get(self, url: str, **kwargs):
        return self._client.get(url, **kwargs)
    
    def _post(self, url: str, **kwargs):
        return self._client.post(url, **kwargs)

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