"""
Módulo CLC para dorking usando motor de busca Lycos.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Lycos, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.

Lycos é um dos motores de busca mais antigos ainda em operação, oferecendo
vantagens específicas para OSINT:
- Algoritmo de indexação e classificação diferente dos grandes buscadores
- Menor uso de filtros de personalização e bolhas de informação
- Menor probabilidade de limitação de consultas e bloqueio de bots
- Potencial para encontrar conteúdos mais antigos ou históricos
- Indexação de sites que podem não aparecer em buscadores principais

A diversificação de fontes de busca é uma estratégia importante para OSINT,
e o Lycos pode revelar informações que não são facilmente descobertas
através dos motores de busca mainstream como Google ou Bing.
"""
import re
import random
import asyncio
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException
from urllib.parse import urljoin, urlparse, quote_plus, unquote

from stringx.core.format import Format
from stringx.core.http_async import HTTPClient
from stringx.core.basemodule import BaseModule
from stringx.core.retry import retry_operation
from stringx.core.user_agent_generator import UserAgentGenerator

class LycosDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Lycos.
    
    Esta classe permite realizar buscas avançadas no Lycos utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Lycos.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request  = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Lycos Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Lycos',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:lycos" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'max_results': 30,  # Número máximo de resultados
            'max_pages': 5,  # Número máximo de páginas para buscar (usando paginação automática)            'proxy': str(),   # Proxies para requisições
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição   
        }
        
        # Base URL do Lycos
        self.base_url = "https://search.lycos.com"
        self.search_path = "/web/"
        
        # Variável para armazenar o keyvol
        self.keyvol = None

    def run(self):
        """
        Executa busca de dorks no Lycos.
        
        Realiza uma busca no motor de busca Lycos usando o dork especificado
        e extrai os resultados, apresentando apenas URLs válidas.
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.log_debug("[!] Dork não fornecido.")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()
            
            # Coletando resultados
            results = self._search_lycos(dork)
            
            if not results:
                self.log_debug(f"[!] Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.handle_error(e, "Erro na busca")
    
    async def _get_keyvol_async(self, headers: dict) -> bool:
        """
        Versão assíncrona para obter o valor keyvol necessário para as buscas no Lycos.
        
        Args:
            headers (dict): Headers da requisição
            
        Returns:
            bool: True se conseguiu obter o keyvol, False caso contrário
        """
        try:
            # Fazer requisição inicial para obter o keyvol
            response = await self.request.send_request([self.base_url + self.search_path], 
                                                         headers=headers, 
                                                         follow_redirects=True)
            
            if not response or isinstance(response[0], Exception):
                return False
                
            response = response[0]
            
            if response.status_code == 200:
                html = response.text
                
                # Extrair keyvol usando regex baseado no código PHP fornecido
                # Padrão: name="keyvol".*value=".*"
                pattern = r'name="keyvol"[^>]*value="([^"]*)"'
                match = re.search(pattern, html, re.IGNORECASE)
               
                if match:
                    self.keyvol = match.group(1)
                    return True
                
                # Tentar padrão alternativo
                pattern_alt = r'<input[^>]*name=["\']keyvol["\'][^>]*value=["\']([^"\']*)["\']'
                match_alt = re.search(pattern_alt, html, re.IGNORECASE)
                if match_alt:
                    self.keyvol = match_alt.group(1)
                    return True
                
            return False
            
        except Exception as e:
            return False

    def _get_keyvol(self, headers: dict) -> bool:
        """
        Wrapper síncrono para obter o valor keyvol necessário para as buscas no Lycos.
        
        Args:
            headers (dict): Headers da requisição
            
        Returns:
            bool: True se conseguiu obter o keyvol, False caso contrário
        """
        return asyncio.run(self._get_keyvol_async(headers))

    async def _search_lycos_async(self, dork: str) -> list:
        """
        Versão assíncrona para realizar busca no Lycos usando paginação automática e extrair resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de URLs válidas encontradas
        """
        results = []
        max_results = self.options.get('max_results', 40)
        max_pages = self.options.get('max_pages', 3)
        
        # Codificar a query
        encoded_dork = quote_plus(dork)
        
        # Headers básicos para simular navegador
        headers = {
            'User-Agent': UserAgentGenerator.get_random_lib(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://search.lycos.com/',
        }

        # Configurar parâmetros para o HTTPClient
        kwargs = {
            'headers': headers,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }

        try:
            # Primeiro, obter o keyvol fazendo uma requisição inicial
            if not await self._get_keyvol_async(headers):
                self.handle_error(ValueError("Não foi possível obter keyvol"), "Erro ao obter keyvol do Lycos")
                return []
                
            # Iniciar com a primeira página
            next_page_url = f"{self.base_url}{self.search_path}?q={encoded_dork}&keyvol={self.keyvol}&pageInfo=Keywords={encoded_dork}&pn=1"
            page_count = 0
                
            # Buscar páginas usando paginação automática
            while next_page_url and page_count < max_pages:
                try:
                    response = await self.request.send_request([next_page_url], **kwargs)
                    
                    if not response or isinstance(response[0], Exception):
                        break
                        
                    response = response[0]
                    
                    if response.status_code == 200:
                        # Extrair URLs da página atual
                        page_urls = self._extract_urls_from_response(response.text)
                        results.extend(page_urls)
                        
                        # Limitar número de resultados
                        if len(results) >= max_results:
                            break
                        
                        # Se não encontrou resultados nesta página, parar
                        if not page_urls:
                            break
                        
                        # Buscar próxima página usando link de paginação
                        next_page_url = self._get_next_page_url(response.text)
                        page_count += 1
                        
                        # Delay entre páginas
                        if next_page_url:
                            await asyncio.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                    else:
                        break
                    
                except Exception as e:
                    # Parar em caso de erro
                    break
            
            # Remover duplicatas e filtrar URLs válidas
            unique_results = []
            seen = set()
            
            for url in results:
                if url and url not in seen and self._is_valid_url(url):
                    seen.add(url)
                    unique_results.append(url)
                    
                    if len(unique_results) >= max_results:
                        break
            
            return unique_results
                
        except Exception as e:
            self.handle_error(e, "Erro ao conectar ao Lycos")
            return []
    
    
    def _search_lycos(self, dork: str) -> list:
        """
        Wrapper síncrono para realizar busca no Lycos usando paginação automática e extrair resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de URLs válidas encontradas
        """
        return asyncio.run(self._search_lycos_async(dork))

    @retry_operation
    def _get_next_page_url(self, html_content: str) -> str:
        """
        Extrai a URL da próxima página da seção de paginação.
        
        Args:
            html_content (str): Conteúdo HTML da página
            
        Returns:
            str: URL da próxima página ou None se não encontrar
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar pela seção de paginação
            pagination = soup.find('ul', class_='pagination')
            
            if pagination:
                # Buscar pelo link "Next"
                next_links = pagination.find_all('a', title='Next')
                
                if next_links:
                    next_href = next_links[0].get('href')
                    if next_href:
                        # Se o href for relativo, adicionar o base URL
                        if next_href.startswith('/'):
                            return self.base_url + next_href
                        elif next_href.startswith('http'):
                            return next_href
                        else:
                            return self.base_url + '/' + next_href
            
            return None
            
        except Exception as e:
            raise ValueError(e)

    def _extract_urls_from_response(self, html_content: str) -> list:
        """
        Extrai URLs dos resultados de busca do Lycos.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de URLs encontradas
        """
        urls = []
        
        try:
            # Tentar extrair URLs usando BeautifulSoup primeiro
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar links de resultados com seletores específicos do Lycos
            selectors = [
                'span.result-url',  # Títulos de resultado
                'a.result-title',  # Links de título de resultado
                'h3.result-title a',  # Títulos de resultado
                'a[href*="http"]',  # Links gerais HTTP
                '.result a[href^="http"]',  # Links em resultados
                '.search-result a[href^="http"]',  # Links em resultados de busca
                '.search-result a[href^="http"]',  # Links em resultados de busca
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    if link:
                        if 'result-url' in str(link):
                            # Extrair link de span result-url
                            url_span = str(link).replace('<span class="result-url">', '')
                            url_span = url_span.replace('</span>', '')
                            url_span = "https://" + url_span
                            if url_span and self._is_external_url(url_span):
                                urls.append(url_span)
                        if 'href' in link.attrs:
                            # Extrair href diretamente
                            url_href = link.get('href')
                            if url_href and  url_href.startswith(('http://', 'https://')):
                                if url_href and self._is_external_url(url_href):
                                    urls.append(url_href)
            # Se não encontrar com BeautifulSoup, usar regex
            if not urls:
                # Padrões regex para extrair URLs
                url_patterns = [
                    r'href=["\']([^"\']*https?://[^"\']+)["\']',  # URLs HTTP/HTTPS
                    r'<a[^>]*href=["\']([^"\']*https?://[^"\']+)["\']',  # URLs gerais em tags de âncora
                ]
                
                for pattern in url_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        if self._is_external_url(match):
                            urls.append(match)
            
        except Exception as e:
            # Fallback para regex em caso de erro
            try:
                pattern = r'href=["\']([^"\']*https?://[^"\']+)["\']'
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if self._is_external_url(match):
                        urls.append(match)
            except:
                pass
        
        return urls

    def _is_external_url(self, url: str) -> bool:
        """
        Verifica se uma URL é externa (não do Lycos).
        
        Args:
            url (str): URL para verificar
            
        Returns:
            bool: True se é URL externa válida
        """
        if not url or not isinstance(url, str):
            return False
        
        # Verificar se não é URL interna do Lycos
        if 'lycos.com' in url.lower():
            return False
        
        # Verificar se é URL válida
        return url.startswith(('http://', 'https://'))

    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida e não está na lista de bloqueio.
        
        Args:
            url (str): URL para validar
            
        Returns:
            bool: True se a URL é válida, False caso contrário
        """
        if not url or not isinstance(url, str):
            return False
        
        # Lista de domínios a serem filtrados
        blocked_domains = [
            'lycos.com', 'wikipedia.org', 'wikimedia.org',
            'facebook.com', 'twitter.com', 'instagram.com', 'youtube.com',
            'linkedin.com', 'reddit.com', 'pinterest.com'
        ]
        
        # Verificar se a URL está em formato válido
        if not url.startswith(('http://', 'https://')):
            return False
        
        # Verificar se não está na lista de domínios bloqueados
        for blocked_domain in blocked_domains:
            if blocked_domain in url.lower():
                return False
        
        # Verificar se não é um arquivo de mídia comum
        media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', 
                          '.mp4', '.avi', '.mov', '.mp3', '.wav']
        
        url_lower = url.lower()
        for ext in media_extensions:
            if url_lower.endswith(ext):
                return False
        
        # Verificar se a URL tem um domínio válido
        try:
            parsed = urlparse(url)
            if not parsed.netloc or len(parsed.netloc) < 4:
                return False
        except:
            return False
        
        return True
