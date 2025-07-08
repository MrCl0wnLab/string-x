"""
Módulo CLC para dorking usando motor de busca Yahoo.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Yahoo, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.

O Yahoo Search, embora tenha perdido participação de mercado para o Google,
ainda oferece vantagens significativas para OSINT:
- Algoritmo de indexação e classificação diferente dos concorrentes
- Menor probabilidade de bloqueio para ferramentas de scraping
- Indexação de conteúdos que podem estar ausentes em outros buscadores
- Operadores de busca avançada com comportamentos distintos
- Resultados potencialmente diferentes para as mesmas consultas
- Menor implementação de filtros de personalização

A diversificação de fontes de busca é fundamental para investigações OSINT
abrangentes, e o Yahoo pode revelar informações que não seriam encontradas
utilizando apenas um motor de busca principal como o Google.
"""
from core.basemodule import BaseModule
from core.user_agent_generator import UserAgentGenerator
import re
from urllib.parse import quote_plus
import time
import random
from bs4 import BeautifulSoup
from core.format import Format
from urllib.parse import urljoin, urlparse, unquote
import asyncio
from core.http_async import HTTPClient
import backoff
from requests.exceptions import RequestException
import asyncio
from core.http_async import HTTPClient

class YahooDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Yahoo.
    
    Esta classe permite realizar buscas avançadas no Yahoo utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Yahoo.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Yahoo Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Yahoo',
            'type': 'collector'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm',
            'proxy': str(),  # Proxies para requisições (opcional)
            'debug': False,  # Modo de debug para mostrar informações detalhadas    
        }
        
        self.search_url_templates = [
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=1&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=8&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=15&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=22&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}fr=goodsearch-yhsif&b=1&pz=10&bct=0&xargs=0",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}&fr=goodsearch-yhsif&b=11&pz=10&bct=0&xargs=0",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}&fr=goodsearch-yhsif&b=21&pz=10&bct=0&xargs=0",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}&fr=goodsearch-yhsif&b=31&pz=10&bct=0&xargs=0",
        ]
    
    def run(self):
        """
        Executa busca de dorks no Yahoo.
        
        Realiza uma busca no motor de busca Yahoo usando o dork especificado
        e extrai os resultados, apresentando apenas URLs por padrão ou detalhes completos.
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.set_result("⚠️ Dork não fornecido.")
                return

            # Coletando resultados
            results = self._search(dork)
            
            if not results:
                self.set_result(f"⚠️ Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.set_result(f"✗ Erro na busca: {str(e)}")
    
    @backoff.on_exception(
        backoff.expo,
        RequestException,
        max_tries=3,
        max_time=30
    ) 
    def _search(self, dork: str) -> list:
        """
        Realiza busca no Yahoo usando diferentes URLs e extrai resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de dicionários com os resultados (título, URL, descrição)
        """
   
        # Lista para armazenar resultados
        results = []
        
        # Codificar a query
        encoded_dork = quote_plus(dork)
        # Definir proxy se fornecido
        proxy = self.options.get('proxy') if self.options.get('proxy') else None
        # Configurar parâmetros para HTTPClient
        kwargs = {
            'headers': {
                'User-Agent': UserAgentGenerator.get_random_lib(),
                'Accept': 'text/html,application/xhtml+xml,application/xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://br.search.yahoo.com',
                'DNT': '1'
            },
            'proxies': {
                'http://': proxy,
                'https://': proxy
            },
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
        
        try:
            # Usar o método assíncrono do HTTPClient
            for _, template in enumerate(self.search_url_templates):
                search_url = template.format(DORK=encoded_dork)
                try:
                    # Executar requisição assíncrona
                    async def make_request():
                        return await self.request.send_request([search_url], **kwargs)
                    response = asyncio.run(make_request())[0]
                    
                    if response.status_code != 200:
                        continue
                    
                    # Extrair resultados
                    page_results = set(self._extract_urls(response.text))
                    
                    # Filtrar duplicidades
                    for url in page_results:
                        if url:
                            results.append(url)
                    # Respeitar delay entre requisições
                    time.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                    
                except Exception:
                    # Continuar para o próximo formato em caso de erro
                    continue
            
            return results
                
        except Exception as e:
            self.set_result(f"✗ Erro ao conectar ao Yahoo: {str(e)}")
            return []
        
    def _is_valid_url(self,url):
        """Verifica se uma URL é válida"""
        block_list = [
            'bing.com', 'microsoft.com', 'msn.com', 'live.com', 'outlook.com',
            'hotmail.com', 'office.com', 'skype.com', 'xbox.com', 'windows.com',
            'microsoftonline.com', 'azurewebsites.net', 'uol.com.br','play.google.com',
            'yahoo.com'
        ]

        if not url:
            return False

        for block in block_list:
            if block in url:
                return False
            
        if url.startswith('http'):
            return True
        return False


    def _extract_urls(self, html_content):
        results = []
        # Regex para capturar URLs entre R*= e /R*=
        pattern = r'\/R[A-Za-z0-9]+=([http][^\/]+)\/R[A-Za-z0-9]+='
        # Encontrar todas as correspondências
        matches = re.findall(pattern, html_content)
        # Decodificar as URLs encontradas (converter %3a para :, %2f para /, etc)
        for url in matches:
            if self._is_valid_url(url):
                results.append(unquote(url))
        return results


