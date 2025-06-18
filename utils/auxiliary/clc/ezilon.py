"""
Módulo CLC para dorking usando motor de busca Ezilon.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Ezilon, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.
"""
from core.basemodule import BaseModule
import httpx
import re
from urllib.parse import quote_plus, unquote
import time
import random
from bs4 import BeautifulSoup
from core.format import Format
from urllib.parse import urljoin, urlparse
import backoff
from requests.exceptions import RequestException

class EzilonDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Ezilon.
    
    Esta classe permite realizar buscas avançadas no Ezilon utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Ezilon.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Ezilon Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Ezilon',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'max_results': 30,  # Número máximo de resultados
            'max_pages': 5,  # Número máximo de páginas para buscar
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:ezilon" -pm',
            'proxy': str(),  # Proxies para requisições (opcional)
        }
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        ]
        
        # Base URL do Ezilon
        self.base_url = "https://find.ezilon.com"
        self.search_path = "/search.php"
        
        # URLs de busca baseadas nos exemplos fornecidos
        self.search_url_templates = [
            "https://find.ezilon.com/search.php?q={DORK}&v={REGION}",
            "https://find.ezilon.com/search.php?q={DORK}&start={START}&t=&v={REGION}&f="

        ]

        # Regiões disponíveis para busca
        self.regions = [
            'usa',
            'asia',
            'eu',
            'in',
            'can',
        ]

    def run(self):
        """
        Executa busca de dorks no Ezilon.
        
        Realiza uma busca no motor de busca Ezilon usando o dork especificado
        e extrai os resultados, apresentando apenas URLs válidas.
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.set_result("⚠️ Dork não fornecido.")
                return

            # Coletando resultados
            results = self._search_ezilon(dork)
            
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
    def _search_ezilon(self, dork: str) -> list:
        """
        Realiza busca no Ezilon usando paginação e extrai resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de URLs válidas encontradas
        """
        results = []
        max_results = self.options.get('max_results', 100)
        max_pages = self.options.get('max_pages', 6)
        
        # Codificar a query
        encoded_dork = quote_plus(dork)
        
        # Headers básicos para simular navegador
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://find.ezilon.com/',
        }

        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }

        
        try:
            with httpx.Client(verify=False, **client_kwargs) as client:
                # Buscar em múltiplas páginas usando o padrão de URL do Ezilon
                for page in range(1, max_pages):
                    try:
                        page_urls = self._search_page(client, headers, encoded_dork, page)
                        results.extend(page_urls)
                        
                        # Limitar número de resultados
                        #if len(results) >= max_results:
                        #    break
                        
                        # Se não encontrou resultados nesta página, parar
                        if not page_urls:
                            break
                        
                        # Delay entre páginas
                        time.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                        
                    except Exception as e:
                        # Continuar para próxima página em caso de erro
                        continue
                
                # Remover duplicatas e filtrar URLs válidas
                unique_results = []
                seen = set()
                
                for url in results:
                    if url and url not in seen and self._is_valid_url(url):
                        seen.add(url)
                        unique_results.append(url)
                        
                        #if len(unique_results) >= max_results:
                        #    break
                
                return unique_results
                
        except RequestException as e:
            self.set_result(f"✗ Erro ao conectar ao Ezilon: {str(e)}")
            return []

    def _search_page(self, client: httpx.Client, headers: dict, encoded_dork: str, page: int) -> list:
        """
        Realiza busca em uma página específica do Ezilon.
        
        Args:
            client (httpx.Client): Cliente HTTP
            headers (dict): Headers da requisição
            encoded_dork (str): Query codificada
            page (int): Número da página
            
        Returns:
            list: Lista de URLs encontradas na página
        """
        try:
            # Calcular parâmetro start baseado na página (padrão observado nos exemplos)
            # Página 1: start não especificado
            # Página 2: start=15
            # Página 3: start=30
            # Página 4: start=45
            # Padrão: start = (page - 1) * 15
            # URLS de exemplo:
            #   https://find.ezilon.com/search.php?q={DORK}&v=usa
            #   https://find.ezilon.com/search.php?q={DORK}&start=15&t=&v=usa&f=
            #   https://find.ezilon.com/search.php?q={DORK}&start=30&t=&v=usa&f=
            #   https://find.ezilon.com/search.php?q={DORK}&start=45&t=&v=usa&f=
            
            if page == 1:
                # Primeira página: usar template simples
                #search_url = f"https://find.ezilon.com/search.php?q={encoded_dork}&v=usa"
                search_url = self.search_url_templates[0].replace("{DORK}", encoded_dork).replace("{REGION}", random.choice(self.regions))
            else:
                # Páginas subsequentes: calcular start
                start = (page - 1) * 15
                #search_url = f"https://find.ezilon.com/search.php?q={encoded_dork}&start={start}&t=&v=usa&f="
                search_url = self.search_url_templates[0].replace("{DORK}", encoded_dork).replace("{START}", str(start)).replace("{REGION}", random.choice(self.regions))
            
            response = client.get(search_url, headers=headers)
            
            if response.status_code == 200:
                return self._extract_urls_from_response(response.text)
            
        except Exception as e:
            pass
        
        return []

    def _extract_urls_from_response(self, html_content: str) -> list:
        """
        Extrai URLs dos resultados de busca do Ezilon.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de URLs encontradas
        """
        urls = []
        
        try:
            # Tentar extrair URLs usando BeautifulSoup primeiro
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar links de resultados com seletores específicos do Ezilon
            selectors = [
                'a[href*="http"]',  # Links gerais HTTP/HTTPS
                '.result a[href^="http"]',  # Links em resultados
                '.search-result a[href^="http"]',  # Links em resultados de busca
                '.listing a[href^="http"]',  # Links em listagens
                'h3 a[href^="http"]',  # Links em títulos h3
                'div a[href^="http"]',  # Links em divs
                'td a[href^="http"]',  # Links em células de tabela
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href', '')
                    if href and self._is_external_url(href):
                        # Decodificar URLs do Ezilon se necessário
                        decoded_url = self._decode_ezilon_url(href)
                        if decoded_url:
                            urls.append(decoded_url)
            
            # Se não encontrar com BeautifulSoup, usar regex
            if not urls:
                # Padrões regex para extrair URLs
                url_patterns = [
                    r'href=["\']([^"\']*https?://[^"\']+)["\']',  # URLs HTTP/HTTPS
                    r'"url":\s*"([^"]*https?://[^"]*)"',  # URLs em JSON
                    r'<a[^>]*href=["\']([^"\']*\.(?:com|org|net|edu|gov|mil)[^"\']*)["\']',  # URLs com domínios específicos
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs diretas
                ]
                
                for pattern in url_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        if self._is_external_url(match):
                            decoded_url = self._decode_ezilon_url(match)
                            if decoded_url:
                                urls.append(decoded_url)
            
        except Exception as e:
            # Fallback para regex em caso de erro
            try:
                pattern = r'href=["\']([^"\']*https?://[^"\']+)["\']'
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if self._is_external_url(match):
                        decoded_url = self._decode_ezilon_url(match)
                        if decoded_url:
                            urls.append(decoded_url)
            except:
                pass
        
        return urls

    def _decode_ezilon_url(self, encoded_url: str) -> str:
        """
        Decodifica URLs do Ezilon que podem estar codificadas ou redirecionadas.
        
        Args:
            encoded_url (str): URL potencialmente codificada
            
        Returns:
            str: URL decodificada ou None se inválida
        """
        if not encoded_url:
            return None
        
        try:
            # Se a URL contém redirecionamento do Ezilon, extrair URL real
            if 'ezilon.com' in encoded_url and ('url=' in encoded_url or 'link=' in encoded_url):
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
        Verifica se uma URL é externa (não do Ezilon).
        
        Args:
            url (str): URL para verificar
            
        Returns:
            bool: True se é URL externa válida
        """
        if not url or not isinstance(url, str):
            return False
        
        # Verificar se não é URL interna do Ezilon
        ezilon_domains = ['ezilon.com', 'find.ezilon.com']
        for domain in ezilon_domains:
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
            'ezilon.com', 'find.ezilon.com',
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
