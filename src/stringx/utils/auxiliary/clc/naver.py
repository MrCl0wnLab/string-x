"""
Módulo CLC para dorking usando motor de busca Naver.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Naver, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.

Naver é o maior motor de busca da Coreia do Sul, oferecendo vantagens específicas
para OSINT e reconhecimento digital:
- Cobertura extensa de conteúdo asiático, particularmente coreano
- Indexação de sites e conteúdos que não aparecem em buscadores ocidentais
- Algoritmo de busca diferente que pode revelar resultados exclusivos
- Menor probabilidade de implementação de medidas anti-scraping para ferramentas ocidentais
- Fonte valiosa para investigações relacionadas à região asiática

A utilização de motores de busca regionais como Naver é especialmente importante
para investigações que envolvam alvos ou operações na Ásia Oriental, permitindo
acessar dados que podem estar ausentes ou menos visíveis em motores de busca ocidentais.
"""

import re
import random
import asyncio
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException
from urllib.parse import quote_plus, unquote,  urljoin, urlparse

from stringx.core.format import Format
from stringx.core.http_async import HTTPClient
from stringx.core.basemodule import BaseModule
from stringx.core.retry import retry_operation
from stringx.core.user_agent_generator import UserAgentGenerator

class NaverDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Naver.
    
    Esta classe permite realizar buscas avançadas no Naver utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Naver.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Naver Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Naver',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:naver" -pm'
        }
        # Opções configuráveis do módulo        
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'max_results': 30,  # Número máximo de resultados
            'max_pages': 5,  # Número máximo de páginas para buscar            'proxy': str(),  # Proxies para requisições (opcional)
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição   
        }
        
        # Base URL do Naver
        self.base_url = "https://search.naver.com"
        self.search_path = "/search.naver"
        
        # URLs de busca baseadas nos exemplos fornecidos (AINDA Não usado)
        self.search_url_templates = [
            "https://search.naver.com/search.naver?nso=&query={DORK}&sm=tab_pge&where=nexearch",
            "https://search.naver.com/search.naver?nso=&query={DORK}&sm=tab_pge&where=web"
        ]

    def run(self):
        """
        Executa busca de dorks no Naver.
        
        Realiza uma busca no motor de busca Naver usando o dork especificado
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
            results = self._search_naver(dork)
            
            if not results:
                self.log_debug(f"Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.handle_error(e, "Erro na busca")
    
    
    def _search_naver(self, dork: str) -> list:
        """
        Wrapper síncrono para realizar busca no Naver usando paginação e extrair resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de URLs válidas encontradas
        """
        return asyncio.run(self._search_naver_async(dork))
    
    @retry_operation
    async def _search_naver_async(self, dork: str) -> list:
        """
        Versão assíncrona para realizar busca no Naver usando paginação e extrair resultados.
        
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
        
        # Headers básicos para simular navegador
        headers = {
            'User-Agent': UserAgentGenerator.get_random_lib(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://search.naver.com/',
        }

        # Configurar parâmetros para o HTTPClient
        kwargs = {
            'headers': headers,
            'proxy' : self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
    
        
        try:
            # Buscar em múltiplas páginas usando o padrão de URL do Naver
            for page in range(1, max_pages + 1):
                try:
                    page_urls = await self._search_page_async(headers, encoded_dork, page, kwargs)
                    results.extend(page_urls)
                    
                    # Limitar número de resultados
                    if len(results) >= max_results:
                        break
                    
                    # Se não encontrou resultados nesta página, parar
                    if not page_urls:
                        break
                    
                    # Delay entre páginas
                    await asyncio.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    self.handle_error(e, "Erro ao processar página do Naver")
                    # Continuar para próxima página em caso de erro
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
                
        except Exception as e:
            self.handle_error(e, "Erro ao conectar ao Naver")
            raise ValueError(e)

    async def _search_page_async(self, headers: dict, encoded_dork: str, page: int, kwargs: dict) -> list:
        """
        Versão assíncrona para realizar busca em uma página específica do Naver.
        
        Args:
            headers (dict): Headers da requisição
            encoded_dork (str): Query codificada
            page (int): Número da página
            kwargs (dict): Argumentos adicionais para a requisição
            
        Returns:
            list: Lista de URLs encontradas na página
        """
        try:
            # Calcular parâmetro start baseado na página (padrão observado nos exemplos)
            # Página 1: start não especificado ou 1
            # Página 2: start=1
            # Página 3: start=16
            # Página 4: start=31
            # Padrão aproximado: start = (page - 1) * 15 + 1 para page > 1
            # URLS de exemplo:
            #   https://search.naver.com/search.naver?nso=&query={DORK}&sm=tab_pge&where=nexearch
            #   https://search.naver.com/search.naver?nso=&page=2&query={DORK}&sm=tab_pge&start=1&where=web
            #   https://search.naver.com/search.naver?nso=&page=3&query={DORK}&sm=tab_pge&start=16&where=web
            #   https://search.naver.com/search.naver?nso=&page=4&query={DORK}&sm=tab_pge&start=31&where=web
            
            if page == 1:
                # Primeira página: usar template simples
                search_url = f"https://search.naver.com/search.naver?nso=&query={encoded_dork}&sm=tab_pge&where=web"
            else:
                # Páginas subsequentes: calcular start
                start = (page - 1) * 15 + 1 if page > 2 else 1
                search_url = f"https://search.naver.com/search.naver?nso=&page={page}&query={encoded_dork}&sm=tab_pge&start={start}&where=web"
            
            response = await self.request.send_request([search_url], **kwargs)
            
            if not response or isinstance(response[0], Exception):
                return []
                
            response = response[0]
            
            if response.status_code == 200:
                return self._extract_urls_from_response(response.text)
            
        except Exception as e:
            self.handle_error(e,"Erro ao buscar página")
        
        return []

    def _extract_urls_from_response(self, html_content: str) -> list:
        """
        Extrai URLs dos resultados de busca do Naver.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de URLs encontradas
        """
        urls = []
        
        try:
            # Tentar extrair URLs usando BeautifulSoup primeiro
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar links de resultados com seletores específicos do Naver
            selectors = [
                'a.link_tit',  # Links de título de resultado
                'a.total_tit',  # Títulos totais
                'a[href*="http"]',  # Links gerais HTTP
                '.result_item a[href^="http"]',  # Links em itens de resultado
                '.search_result a[href^="http"]',  # Links em resultados de busca
                '.total_wrap a[href^="http"]',  # Links no wrapper total
                '.api_subject_bx a[href^="http"]',  # Links de assunto API
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href', '')
                    if href and self._is_external_url(href):
                        # Decodificar URLs do Naver se necessário
                        decoded_url = self._decode_naver_url(href)
                        if decoded_url:
                            urls.append(decoded_url)
            
            # Se não encontrar com BeautifulSoup, usar regex
            if not urls:
                # Padrões regex para extrair URLs
                url_patterns = [
                    r'href=["\']([^"\']*https?://[^"\']+)["\']',  # URLs HTTP/HTTPS
                    r'"url":\s*"([^"]*https?://[^"]*)"',  # URLs em JSON
                    r'<a[^>]*href=["\']([^"\']*\.(?:com|org|net|edu|gov|mil|kr|jp|cn)[^"\']*)["\']',  # URLs com domínios específicos
                ]
                
                for pattern in url_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        if self._is_external_url(match):
                            decoded_url = self._decode_naver_url(match)
                            if decoded_url:
                                urls.append(decoded_url)
            
        except Exception as e:
            self.handle_error(e, "Erro ao extrair URLs da resposta do Naver")
            # Fallback para regex em caso de erro
            try:
                pattern = r'href=["\']([^"\']*https?://[^"\']+)["\']'
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if self._is_external_url(match):
                        decoded_url = self._decode_naver_url(match)
                        if decoded_url:
                            urls.append(match)
            except:
                pass
        
        return urls

    def _decode_naver_url(self, encoded_url: str) -> str:
        """
        Decodifica URLs do Naver que podem estar codificadas ou redirecionadas.
        
        Args:
            encoded_url (str): URL potencialmente codificada
            
        Returns:
            str: URL decodificada ou None se inválida
        """
        if not encoded_url:
            return None
        
        try:
            # Se a URL contém redirecionamento do Naver, extrair URL real
            if 'search.naver.com' in encoded_url and ('url=' in encoded_url or 'link=' in encoded_url):
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
            
        except Exception as e:
            self.handle_error(e, "Erro ao decodificar URL do Naver")
            pass
        
        return None

    def _is_external_url(self, url: str) -> bool:
        """
        Verifica se uma URL é externa (não do Naver).
        
        Args:
            url (str): URL para verificar
            
        Returns:
            bool: True se é URL externa válida
        """
        if not url or not isinstance(url, str):
            return False
        
        # Verificar se não é URL interna do Naver
        naver_domains = ['naver.com', 'naver.net', 'navercorp.com']
        for domain in naver_domains:
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
            'naver.com', 'naver.net', 'navercorp.com',
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
