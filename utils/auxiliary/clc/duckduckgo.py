"""
Módulo CLC para dorking usando motor de busca DuckDuckGo.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca DuckDuckGo, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.
"""
from core.basemodule import BaseModule
from core.user_agent_generator import UserAgentGenerator
import httpx
import re
from urllib.parse import quote_plus, unquote
import time
import random
from bs4 import BeautifulSoup
from core.format import Format
from urllib.parse import urljoin, urlparse
import json
import backoff
from requests.exceptions import RequestException

class DuckDuckGoDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca DuckDuckGo.
    
    Esta classe permite realizar buscas avançadas no DuckDuckGo utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking DuckDuckGo.
        """
        super().__init__()
        
        self.meta = {
            'name': 'DuckDuckGo Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no DuckDuckGo',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'max_results': 30,  # Número máximo de resultados
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:duckduckgo" -pm',
            'proxy': str(),  # Proxies para requisições (opcional)
        }
        
        # URLs de busca do DuckDuckGo com diferentes estratégias
        self.search_url_templates = [
            "https://duckduckgo.com/?q={DORK}&t=h_&ia=web",
            "https://duckduckgo.com/html/?q={DORK}&kl=wt-wt",
            "https://lite.duckduckgo.com/lite/?q={DORK}&kl=wt-wt",
        ]
        
        # Padrões para extrair URLs dos resultados
        self.url_patterns = [
            r'href=["\']([^"\']*uddg[^"\']*)["\']',  # URLs com parâmetro uddg
            r'data-testid="result-title-a"[^>]*href=["\']([^"\']+)["\']',  # Links de título
            r'class="result__a"[^>]*href=["\']([^"\']+)["\']',  # Links de resultado
            r'<a[^>]*href=["\']([^"\']*\.(?:com|org|net|edu|gov|mil|br|uk|de|fr|it|es|pt|ru)[^"\']*)["\']',  # URLs gerais
        ]

    def run(self):
        """
        Executa busca de dorks no DuckDuckGo.
        
        Realiza uma busca no motor de busca DuckDuckGo usando o dork especificado
        e extrai os resultados, apresentando apenas URLs válidas.
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.set_result("⚠️ Dork não fornecido.")
                return

            # Coletando resultados
            results = self._search_duckduckgo(dork)
            
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
    def _search_duckduckgo(self, dork: str) -> list:
        """
        Realiza busca no DuckDuckGo usando diferentes URLs e extrai resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de URLs válidas encontradas
        """
        results = []
        max_results = self.options.get('max_results', 30)
        
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
        }

        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }
        
        try:
            with httpx.Client(verify=False, **client_kwargs) as client:
                # Tentar diferentes templates de URL
                for template in self.search_url_templates:
                    search_url = template.format(DORK=encoded_dork)
                    
                    try:
                        # Adicionar referer específico para cada tipo de busca
                        if 'lite.duckduckgo.com' in search_url:
                            headers['Referer'] = 'https://lite.duckduckgo.com/'
                        elif 'html' in search_url:
                            headers['Referer'] = 'https://duckduckgo.com/html/'
                        else:
                            headers['Referer'] = 'https://duckduckgo.com/'
                        
                        response = client.get(search_url, headers=headers)
                        
                        if response.status_code == 200:
                            page_urls = self._extract_urls_from_response(response.text)
                            results.extend(page_urls)
                            
                            # Limitar número de resultados
                            if len(results) >= max_results:
                                break
                        
                        # Delay entre requisições
                        time.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                        
                    except Exception as e:
                        # Continuar para o próximo template em caso de erro
                        continue
                
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
                
        except RequestException as e:
            self.set_result(f"✗ Erro ao conectar ao DuckDuckGo: {str(e)}")
            return []

    def _extract_urls_from_response(self, html_content: str) -> list:
        """
        Extrai URLs dos resultados de busca do DuckDuckGo.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de URLs encontradas
        """
        urls = []
        
        try:
            # Tentar extrair URLs usando BeautifulSoup primeiro
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar links de resultados com seletores específicos do DuckDuckGo
            selectors = [
                'a[data-testid="result-title-a"]',  # Novo layout
                'a.result__a',  # Layout clássico
                'h2.result__title a',  # Variação do layout
                'a[href*="uddg"]',  # URLs com parâmetro uddg
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href', '')
                    if href:
                        # Decodificar URLs do DuckDuckGo
                        decoded_url = self._decode_duckduckgo_url(href)
                        if decoded_url:
                            urls.append(decoded_url)
            
            # Se não encontrar com BeautifulSoup, usar regex
            if not urls:
                for pattern in self.url_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        decoded_url = self._decode_duckduckgo_url(match)
                        if decoded_url:
                            urls.append(decoded_url)
            
        except Exception as e:
            # Fallback para regex em caso de erro
            for pattern in self.url_patterns:
                try:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        decoded_url = self._decode_duckduckgo_url(match)
                        if decoded_url:
                            urls.append(decoded_url)
                except:
                    continue
        
        return urls

    def _decode_duckduckgo_url(self, encoded_url: str) -> str:
        """
        Decodifica URLs do DuckDuckGo que podem estar com parâmetros uddg.
        
        Args:
            encoded_url (str): URL potencialmente codificada
            
        Returns:
            str: URL decodificada ou None se inválida
        """
        if not encoded_url:
            return None
        
        try:
            # Se a URL contém o parâmetro uddg, extrair a URL real
            if 'uddg=' in encoded_url:
                # Extrair o valor do parâmetro uddg
                match = re.search(r'uddg=([^&]+)', encoded_url)
                if match:
                    encoded_part = match.group(1)
                    # Decodificar URL
                    decoded_url = unquote(encoded_part)
                    return decoded_url
            
            # Se não tem uddg, verificar se é uma URL válida diretamente
            if encoded_url.startswith(('http://', 'https://')):
                return encoded_url
            
            # Se começar com //, adicionar https:
            if encoded_url.startswith('//'):
                return 'https:' + encoded_url
            
        except Exception:
            pass
        
        return None

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
            'duckduckgo.com', 'duck.com', 'wikipedia.org', 'wikimedia.org',
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

    def _normalize_url(self, url: str) -> str:
        """
        Normaliza uma URL removendo parâmetros desnecessários.
        
        Args:
            url (str): URL para normalizar
            
        Returns:
            str: URL normalizada
        """
        if not url:
            return url
        
        # Remover parâmetros de tracking comuns
        tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 
                          'utm_term', 'fbclid', 'gclid', 'ref', 'source']
        
        try:
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            # Filtrar parâmetros de tracking
            filtered_params = {k: v for k, v in query_params.items() 
                             if k not in tracking_params}
            
            # Reconstruir query string
            new_query = urlencode(filtered_params, doseq=True)
            
            # Reconstruir URL
            new_parsed = parsed._replace(query=new_query)
            return urlunparse(new_parsed)
            
        except Exception:
            # Se falhar a normalização, retornar URL original
            return url
