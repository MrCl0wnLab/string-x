"""
Módulo CLC para dorking usando motor de busca Sogou.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Sogou, permitindo a extração de resultados usando diferentes
tipos de dorks de busca com paginação dinâmica.

Sogou é um dos principais motores de busca chineses, oferecendo vantagens
significativas para OSINT e reconhecimento digital:
- Indexação extensiva de conteúdo em chinês e asiático em geral
- Acesso a websites e informações focados no mercado chinês
- Resultados diferentes dos obtidos em motores de busca ocidentais
- Cobertura de sites hospedados em infraestrutura chinesa que podem ter
  menor visibilidade em outros buscadores
- Fonte crucial para investigações envolvendo entidades, empresas ou indivíduos
  com presença digital na China

A utilização do Sogou é especialmente importante para investigações que
envolvem o mercado chinês ou operações com conexões à China, fornecendo
uma perspectiva local que complementa as informações de buscadores ocidentais.
"""
import re
import time
import random
import asyncio
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException
from urllib.parse import urljoin, quote_plus, unquote, urlparse, parse_qs

from stringx.core.format import Format
from stringx.core.http_async import HTTPClient
from stringx.core.basemodule import BaseModule
from stringx.core.retry import retry_operation
from stringx.core.user_agent_generator import UserAgentGenerator

class SogouDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Sogou.
    
    Esta classe permite realizar buscas avançadas no Sogou utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Sogou.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Sogou Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Sogou',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:sogou" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'max_results': 50,  # Número máximo de resultados
            'max_pages': 5,  # Número máximo de páginas para buscar            'proxy': str(),  # Proxies para requisições (opcional)
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição   
        }
        
        # Base URL do Sogou
        self.base_url = "http://www.sogou.com"
        self.search_path = "/web"
        
        # URLs de busca baseadas nos exemplos fornecidos
        self.first_page_template = "http://www.sogou.com/web?query={DORK}&cid=&s_from=result_up&page=1&ie=utf8&dr=1"
        self.pagination_template = "http://www.sogou.com/web?query={DORK}&cid=&s_from=result_up&sessiontime={SESSIONTIME}&page={PAGE}&ie=utf8"
        
        # Variável para armazenar sessiontime extraído da primeira página
        self.sessiontime = None

    def run(self):
        """
        Executa busca de dorks no Sogou.
        
        Realiza uma busca no motor de busca Sogou usando o dork especificado
        e extrai os resultados, apresentando apenas URLs válidas.
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.log_debug("Dork não fornecido.")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            # Coletando resultados
            results = self._search_sogou(dork)
            
            if not results:
                self.log_debug(f"Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.handle_error(e, "Erro na busca")

    @retry_operation
    def _search_sogou(self, dork: str) -> list:
        """
        Realiza busca no Sogou usando paginação dinâmica e extrai resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de URLs válidas encontradas
        """
        results = []
        max_results = self.options.get('max_results', 30)
        max_pages = self.options.get('max_pages', 5)
        
        # Codificar a query
        encoded_dork = quote_plus(dork)
        
        # Headers básicos para simular navegador chinês
        headers = {
            'User-Agent': UserAgentGenerator.get_random_lib(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://www.sogou.com/',
        }

        # Configurar parâmetros para HTTPClient
        kwargs = {
            'headers': headers,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
        
        try:
            # Primeira página - usar template específico e extrair sessiontime
            first_page_urls = asyncio.run(self._search_first_page_async(kwargs, encoded_dork))
            results.extend(first_page_urls)
            
            # Se não conseguiu extrair sessiontime ou não há resultados, parar
            if not self.sessiontime or not first_page_urls:
                return self._filter_and_deduplicate(results, max_results)
            
            # Buscar páginas subsequentes usando sessiontime
            for page in range(2, max_pages + 1):
                try:
                    page_urls = asyncio.run(self._search_pagination_page_async(kwargs, encoded_dork, page))
                    results.extend(page_urls)
                    
                    # Limitar número de resultados
                    if len(results) >= max_results:
                        break
                    
                    # Se não encontrou resultados nesta página, parar
                    if not page_urls:
                        break
                    
                    # Delay entre páginas
                    time.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                    
                except Exception:
                    # Continuar para próxima página em caso de erro
                    continue
            
            return self._filter_and_deduplicate(results, max_results)
                
        except Exception as e:
            self.handle_error(e, "Erro ao conectar ao Sogou")
            raise ValueError(e)

    async def _search_first_page_async(self, kwargs: dict, encoded_dork: str) -> list:
        """
        Realiza busca na primeira página do Sogou e extrai sessiontime de forma assíncrona.
        
        Args:
            kwargs (dict): Parâmetros da requisição
            encoded_dork (str): Query codificada
            
        Returns:
            list: Lista de URLs encontradas na primeira página
        """
        try:
            # Construir URL da primeira página
            search_url = self.first_page_template.replace("{DORK}", encoded_dork)
            
            response = await self.request.send_request([search_url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                # Extrair sessiontime do HTML
                self.sessiontime = self._extract_sessiontime(response.text)
                
                # Extrair URLs dos resultados
                return self._extract_urls_from_response(response.text)
            
        except Exception:
            pass
        
        return []

    async def _search_pagination_page_async(self, kwargs: dict, encoded_dork: str, page: int) -> list:
        """
        Realiza busca em uma página de paginação específica do Sogou de forma assíncrona.
        
        Args:
            kwargs (dict): Parâmetros da requisição
            encoded_dork (str): Query codificada
            page (int): Número da página
            
        Returns:
            list: Lista de URLs encontradas na página
        """
        try:
            # Construir URL da página usando sessiontime
            search_url = self.pagination_template.replace("{DORK}", encoded_dork).replace("{SESSIONTIME}", self.sessiontime).replace("{PAGE}", str(page))
            
            response = await self.request.send_request([search_url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                return self._extract_urls_from_response(response.text)
            
        except Exception:
            pass
        
        return []

    def _extract_sessiontime(self, html_content: str) -> str:
        """
        Extrai o sessiontime da div de paginação do Sogou.
        
        Args:
            html_content (str): Conteúdo HTML da página
            
        Returns:
            str: Sessiontime extraído ou None se não encontrado
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar a div de paginação
            pagebar = soup.find('div', {'class': 'p', 'id': 'pagebar_container'})
            
            if pagebar:
                # Buscar links de paginação que contenham sessiontime
                pagination_links = pagebar.find_all('a', href=True)
                
                for link in pagination_links:
                    href = link.get('href', '')
                    if 'sessiontime=' in href:
                        # Extrair sessiontime usando regex
                        sessiontime_match = re.search(r'sessiontime=([^&]+)', href)
                        if sessiontime_match:
                            return sessiontime_match.group(1)
            
            # Método alternativo: buscar em qualquer link que contenha sessiontime
            sessiontime_pattern = r'sessiontime=([^&\'"]+)'
            matches = re.findall(sessiontime_pattern, html_content)
            if matches:
                return matches[0]
            
        except Exception:
            pass
        
        return None

    def _extract_urls_from_response(self, html_content: str) -> list:
        """
        Extrai URLs dos resultados de busca do Sogou.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de URLs encontradas
        """
        urls = []
        
        try:
            # Tentar extrair URLs usando BeautifulSoup primeiro
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar links de resultados com seletores específicos do Sogou
            selectors = [
                'h3 a[href*="http"]',  # Links em títulos h3
                'a.title[href*="http"]',  # Links com classe title
                'a[href*="http"]',  # Links gerais HTTP/HTTPS
                '.result a[href^="http"]',  # Links em resultados
                '.search-result a[href^="http"]',  # Links em resultados de busca
                '.vrTitle a[href^="http"]',  # Links de título vertical
                '.str_info a[href^="http"]',  # Links em informações
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href', '')
                    if href and self._is_external_url(href):
                        # Decodificar URLs do Sogou se necessário
                        decoded_url = self._decode_sogou_url(href)
                        if decoded_url:
                            urls.append(decoded_url)
            
            # Se não encontrar com BeautifulSoup, usar regex
            if not urls:
                # Padrões regex para extrair URLs
                url_patterns = [
                    r'href=["\']([^"\']*https?://[^"\']+)["\']',  # URLs HTTP/HTTPS
                    r'"url":\s*"([^"]*https?://[^"]*)"',  # URLs em JSON
                    r'<a[^>]*href=["\']([^"\']*\.(?:com|org|net|edu|gov|mil|cn|kr|jp)[^"\']*)["\']',  # URLs com domínios específicos
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs diretas
                ]
                
                for pattern in url_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        if self._is_external_url(match):
                            decoded_url = self._decode_sogou_url(match)
                            if decoded_url:
                                urls.append(decoded_url)
            
        except Exception:
            # Fallback para regex em caso de erro
            try:
                pattern = r'href=["\']([^"\']*https?://[^"\']+)["\']'
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if self._is_external_url(match):
                        decoded_url = self._decode_sogou_url(match)
                        if decoded_url:
                            urls.append(decoded_url)
            except:
                pass
        
        return urls

    def _decode_sogou_url(self, encoded_url: str) -> str:
        """
        Decodifica URLs do Sogou que podem estar codificadas ou redirecionadas.
        
        Args:
            encoded_url (str): URL potencialmente codificada
            
        Returns:
            str: URL decodificada ou None se inválida
        """
        if not encoded_url:
            return None
        
        try:
            # Se a URL contém redirecionamento do Sogou, extrair URL real
            if 'sogou.com' in encoded_url and ('url=' in encoded_url or 'link=' in encoded_url):
                # Tentar extrair parâmetro url ou link
                url_match = re.search(r'[?&](?:url|link)=([^&]+)', encoded_url)
                if url_match:
                    decoded_part = unquote(url_match.group(1))
                    if decoded_part.startswith(('http://', 'https://')):
                        return decoded_part
            
            # Se a URL está diretamente codificada
            if encoded_url.startswith('http') and '%' in encoded_url:
                decoded_url = unquote(encoded_url)
                if decoded_url.startswith(('http://', 'https://')):
                    return decoded_url
            
            # Se não tem codificação especial, verificar se é uma URL válida diretamente
            if encoded_url.startswith(('http://', 'https://')):
                return encoded_url
            
            # Se começar com //, adicionar https:
            if encoded_url.startswith('//'):
                return 'https:' + encoded_url
            
        except Exception:
            pass
        
        return None

    def _is_external_url(self, url: str) -> bool:
        """
        Verifica se uma URL é externa (não do Sogou).
        
        Args:
            url (str): URL para verificar
            
        Returns:
            bool: True se é URL externa válida
        """
        if not url or not isinstance(url, str):
            return False
        
        # Verificar se não é URL interna do Sogou
        sogou_domains = ['sogou.com', 'www.sogou.com']
        for domain in sogou_domains:
            if domain in url.lower():
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
            'sogou.com', 'www.sogou.com',
            'wikipedia.org', 'wikimedia.org',
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

    def _filter_and_deduplicate(self, results: list, max_results: int) -> list:
        """
        Remove duplicatas e filtra URLs válidas.
        
        Args:
            results (list): Lista de URLs encontradas
            max_results (int): Número máximo de resultados
            
        Returns:
            list: Lista filtrada e deduplicate
        """
        unique_results = []
        seen = set()
        
        for url in results:
            if url and url not in seen and self._is_valid_url(url):
                seen.add(url)
                unique_results.append(url)
                
                if len(unique_results) >= max_results:
                    break
        
        return unique_results
