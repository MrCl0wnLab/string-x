"""
Módulo CLC para dorking usando motor de busca Yahoo.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Yahoo, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.
"""
from core.basemodule import BaseModule
from core.user_agent_generator import UserAgentGenerator
import httpx
import re
from urllib.parse import quote_plus
import time
import random
from bs4 import BeautifulSoup
from core.format import Format
from urllib.parse import urljoin, urlparse, unquote
import backoff
from requests.exceptions import RequestException

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
        
        self.meta = {
            'name': 'Yahoo Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Yahoo',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm',
            'proxy': str(),  # Proxies para requisições (opcional)
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
        
        # User-agent aleatório
        headers = {
            'User-Agent': UserAgentGenerator.get_random_lib(),
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://br.search.yahoo.com',
            'DNT': '1'
        }

        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }
        
        try:
            with httpx.Client(verify=False, **client_kwargs) as client:
                # Estratégia 1: URL padrão com paginação

                # Usar os três templates de URL
                for _, template in enumerate(self.search_url_templates):
                    search_url = ""
                    search_url = template.format(DORK=encoded_dork)
                    try:
                        response = client.get(search_url, headers=headers)
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
                        
                    except Exception as e:
                        # Continuar para o próximo formato em caso de erro
                        continue

                return results
                
        except RequestException as e:
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


