"""
Módulo CLC Spider para coleta recursiva de URLs.

Este módulo implementa um web spider (crawler) que coleta URLs de forma recursiva,
visitando páginas web e extraindo links para exploração adicional baseada em
profundidade configurável.

O spider oferece:
- Coleta recursiva de URLs com controle de profundidade
- Requisições HTTP/HTTPS assíncronas para performance
- Suporte a proxy e configurações de timeout
- Filtragem e deduplicação automática de URLs
- Extração de URLs usando expressões regulares otimizadas
- Tratamento robusto de erros HTTP/SSL
- Controle de rate limiting para evitar sobrecarga
"""
import re
import asyncio
import time
from typing import Dict, List, Set, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse, urlunparse
from collections import defaultdict

# Bibliotecas de terceiros
import httpx
from bs4 import BeautifulSoup

# Módulos locais
from stringx.core.basemodule import BaseModule
from stringx.core.format import Format

class WebSpider(BaseModule):
    """
    Spider para coleta recursiva de URLs.
    
    Esta classe implementa um web crawler que explora páginas web de forma
    recursiva, extraindo URLs e visitando-as baseado no nível de profundidade
    configurado.
    
    Herda de BaseModule fornecendo interface padrão para módulos auxiliares.
    """
    
    def __init__(self):
        """
        Inicializa o spider com configurações padrão.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Web Spider URL Collector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Coleta URLs de forma recursiva com controle de profundidade',
            'type': 'collector',
            'example': './strx -s "https://example.com" -st "echo {STRING}" -module "clc:spider" -pm'
        }
        
        self.options = {
            'data': str(),                    # URL inicial para começar o spider
            'depth': 5,                       # Profundidade máxima de exploração
            'max_urls': 10000,                  # Número máximo de URLs a coletar
            'timeout': 10,                    # Timeout para requisições HTTP
            'delay': 1.0,                     # Delay entre requisições (rate limiting)
            'user_agent': self.setting.STRX_USER_AGENT,  # User-Agent para requisições HTTP
            'verify_ssl': False,              # Verificar certificados SSL
            'follow_redirects': True,         # Seguir redirecionamentos
            'max_redirects': 5,               # Máximo de redirecionamentos
            'include_external': True,        # Incluir URLs externas ao domínio inicial
            'file_extensions': 'html,htm,php,asp,aspx,jsp,cfm,py,rb,pl',  # Extensões de arquivo a incluir
            'exclude_extensions': 'jpg,jpeg,png,gif,bmp,svg,ico,css,js,pdf,zip,rar,tar,gz,mp3,mp4,avi,mov,wmv,flv,swf,exe,msi,dmg,deb,rpm',  # Extensões a excluir
            'include_patterns': str(),        # Padrões regex para incluir URLs
            'exclude_patterns': str(),        # Padrões regex para excluir URLs
            'concurrent_requests': 5,         # Número de requisições simultâneas
            'extract_from_js': True,         # Extrair URLs de arquivos JavaScript
            'extract_from_css': False,        # Extrair URLs de arquivos CSS
            'respect_robots': False,          # Respeitar robots.txt (básico)
            'debug': False,                   # Modo de debug
            'proxy': None,                    # Proxy para requisições
            'retry': 2,                       # Número de tentativas por URL
            'retry_delay': None,              # Atraso entre tentativas
        }
        
        # Regex patterns para extração de URLs
        self.url_patterns = [
            # URLs padrão HTTP/HTTPS
            re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-\w%/.#?&=]*)*', re.IGNORECASE),
            # URLs em atributos href
            re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE),
            # URLs em atributos src
            re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE),
            # URLs em atributos action
            re.compile(r'action=["\']([^"\']+)["\']', re.IGNORECASE),
            # URLs em JavaScript
            re.compile(r'(?:window\.location|location\.href)\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE),
            # URLs em meta refresh
            re.compile(r'content=["\'][^"\']*url=([^"\']+)["\']', re.IGNORECASE),
        ]
        
        # Conjunto para controlar URLs já visitadas
        self.visited_urls: Set[str] = set()
        self.collected_urls: Set[str] = set()
        self.base_domain: str = ""
        
    def _normalize_url(self, url: str, base_url: str = "") -> str:
        """
        Normaliza uma URL para formato padrão.
        
        Args:
            url: URL a ser normalizada
            base_url: URL base para resolver URLs relativas
            
        Returns:
            URL normalizada
        """
        if not url:
            return ""
        
        # Remove espaços e caracteres de controle
        url = url.strip()
        
        # Resolver URLs relativas
        if base_url and not url.startswith(('http://', 'https://', '//', 'mailto:', 'tel:', 'javascript:')):
            url = urljoin(base_url, url)
        
        # Normalizar esquema para lowercase
        if url.startswith(('HTTP://', 'HTTPS://')):
            url = url.lower()
        
        # Remover fragmentos (#) se não essenciais
        if '#' in url and not self.options.get('include_fragments', False):
            url = url.split('#')[0]
        
        # Remover parâmetros de tracking comuns se configurado
        if self.options.get('remove_tracking', True):
            tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid']
            parsed = urlparse(url)
            if parsed.query:
                query_params = [param for param in parsed.query.split('&') 
                              if not any(param.startswith(track + '=') for track in tracking_params)]
                query = '&'.join(query_params)
                url = urlunparse(parsed._replace(query=query))
        
        return url
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida para coleta.
        
        Args:
            url: URL a ser verificada
            
        Returns:
            True se a URL for válida
        """
        if not url or not url.startswith(('http://', 'https://')):
            return False
        
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False
        except Exception:
            return False
        
        # Verificar se é domínio externo
        if not self.options.get('include_external', False):
            parsed = urlparse(url)
            if self.base_domain and parsed.netloc.lower() != self.base_domain.lower():
                return False
        
        # Verificar extensões excluídas
        exclude_ext = self.options.get('exclude_extensions', '').split(',')
        if exclude_ext:
            path = parsed.path.lower()
            if any(path.endswith('.' + ext.strip()) for ext in exclude_ext if ext.strip()):
                return False
        
        # Verificar extensões incluídas
        include_ext = self.options.get('file_extensions', '').split(',')
        if include_ext and include_ext != ['']:
            path = parsed.path.lower()
            has_extension = '.' in path.split('/')[-1]
            if has_extension and not any(path.endswith('.' + ext.strip()) for ext in include_ext if ext.strip()):
                return False
        
        # Verificar padrões de exclusão
        exclude_patterns = self.options.get('exclude_patterns', '')
        if exclude_patterns:
            try:
                if re.search(exclude_patterns, url, re.IGNORECASE):
                    return False
            except re.error:
                pass
        
        # Verificar padrões de inclusão
        include_patterns = self.options.get('include_patterns', '')
        if include_patterns:
            try:
                if not re.search(include_patterns, url, re.IGNORECASE):
                    return False
            except re.error:
                pass
        
        return True
    
    def _extract_urls_from_content(self, content: str, base_url: str) -> List[str]:
        """
        Extrai URLs do conteúdo HTML.
        
        Args:
            content: Conteúdo HTML da página
            base_url: URL base para resolver URLs relativas
            
        Returns:
            Lista de URLs encontradas
        """
        urls = set()
        
        try:
            # Usar BeautifulSoup para parsing HTML mais robusto
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extrair de tags <a href="">
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href:
                    normalized = self._normalize_url(href, base_url)
                    if self._is_valid_url(normalized):
                        urls.add(normalized)
            
            # Extrair de tags com src (se configurado)
            if self.options.get('extract_from_js', False) or self.options.get('extract_from_css', False):
                for tag in soup.find_all(['script', 'link', 'img'], src=True):
                    src = tag.get('src', '')
                    if src:
                        normalized = self._normalize_url(src, base_url)
                        if self._is_valid_url(normalized):
                            urls.add(normalized)
                            
                for tag in soup.find_all('link', href=True):
                    href = tag.get('href', '')
                    if href:
                        normalized = self._normalize_url(href, base_url)
                        if self._is_valid_url(normalized):
                            urls.add(normalized)
            
            # Fallback: usar regex patterns no conteúdo bruto
            for pattern in self.url_patterns:
                matches = pattern.findall(content)
                for match in matches:
                    # match pode ser uma tupla ou string dependendo do padrão
                    if isinstance(match, tuple):
                        match = match[0] if match else ""
                    
                    if match:
                        normalized = self._normalize_url(match, base_url)
                        if self._is_valid_url(normalized):
                            urls.add(normalized)
        
        except Exception as e:
            if self.options.get('debug'):
                self.log_debug(f"Erro ao extrair URLs: {e}")
            
            # Fallback para regex simples se BeautifulSoup falhar
            for pattern in self.url_patterns:
                try:
                    matches = pattern.findall(content)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0] if match else ""
                        
                        if match:
                            normalized = self._normalize_url(match, base_url)
                            if self._is_valid_url(normalized):
                                urls.add(normalized)
                except Exception:
                    continue
        
        return list(urls)
    
    async def _fetch_url(self, session: httpx.AsyncClient, url: str) -> Tuple[str, str, bool]:
        """
        Faz requisição HTTP para uma URL.
        
        Args:
            session: Cliente HTTP assíncrono
            url: URL a ser requisitada
            
        Returns:
            Tupla (url, content, success)
        """
        try:
            if self.options.get('debug'):
                self.log_debug(f"Fazendo requisição para: {url}")
            
            response = await session.get(url)
            
            # Verificar se é conteúdo HTML/texto
            content_type = response.headers.get('content-type', '').lower()
            if not any(ct in content_type for ct in ['text/html', 'text/plain', 'application/xhtml']):
                if self.options.get('debug'):
                    self.log_debug(f"Tipo de conteúdo ignorado: {content_type}")
                return url, "", False
            
            # Verificar tamanho do conteúdo
            if len(response.content) > 5 * 1024 * 1024:  # 5MB
                if self.options.get('debug'):
                    self.log_debug(f"Conteúdo muito grande, ignorando: {len(response.content)} bytes")
                return url, "", False
            
            content = response.text
            return url, content, True
            
        except httpx.TimeoutException:
            if self.options.get('debug'):
                self.log_debug(f"Timeout na requisição: {url}")
            return url, "", False
        except httpx.RequestError as e:
            if self.options.get('debug'):
                self.log_debug(f"Erro de requisição para {url}: {e}")
            return url, "", False
        except Exception as e:
            if self.options.get('debug'):
                self.log_debug(f"Erro inesperado para {url}: {e}")
            return url, "", False
    
    async def _crawl_level(self, session: httpx.AsyncClient, urls: List[str], current_depth: int) -> List[str]:
        """
        Faz crawling de um nível de URLs.
        
        Args:
            session: Cliente HTTP assíncrono
            urls: Lista de URLs para processar
            current_depth: Profundidade atual
            
        Returns:
            Lista de novas URLs encontradas
        """
        if not urls or current_depth <= 0:
            return []
        
        new_urls = []
        semaphore = asyncio.Semaphore(self.options.get('concurrent_requests', 5))
        
        async def process_url(url: str):
            async with semaphore:
                if url in self.visited_urls:
                    return
                
                if len(self.collected_urls) >= self.options.get('max_urls', 100):
                    return
                
                self.visited_urls.add(url)
                self.collected_urls.add(url)
                
                # Rate limiting
                delay = self.options.get('delay', 1.0)
                if delay > 0:
                    await asyncio.sleep(delay)
                
                url_result, content, success = await self._fetch_url(session, url)
                
                if success and content:
                    # Extrair URLs do conteúdo
                    found_urls = self._extract_urls_from_content(content, url)
                    
                    for found_url in found_urls:
                        if (found_url not in self.visited_urls and 
                            found_url not in self.collected_urls and 
                            len(self.collected_urls) < self.options.get('max_urls', 100)):
                            new_urls.append(found_url)
                            self.collected_urls.add(found_url)
        
        # Processar URLs em paralelo
        tasks = [process_url(url) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return new_urls
    
    async def _run_spider_async(self, start_url: str) -> List[str]:
        """
        Executa o spider de forma assíncrona.
        
        Args:
            start_url: URL inicial
            
        Returns:
            Lista de URLs coletadas
        """
        # Configurar domínio base
        parsed = urlparse(start_url)
        self.base_domain = parsed.netloc
        
        # Configurar cliente HTTP
        timeout = httpx.Timeout(
            timeout=self.options.get('timeout', 10),
            connect=self.options.get('timeout', 10),
            read=self.options.get('timeout', 10)
        )
        
        limits = httpx.Limits(
            max_connections=self.options.get('concurrent_requests', 5),
            max_keepalive_connections=self.options.get('concurrent_requests', 5)
        )
        
        headers = {
            'User-Agent': self.options.get('user_agent', 'String-X-Spider/1.0'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        client_params = {
            'timeout': timeout,
            'follow_redirects': self.options.get('follow_redirects', True),
            'headers': headers,
            'limits': limits,
            'verify': self.options.get('verify_ssl', False),
        }
        
        # Adicionar proxy se configurado
        proxy = self.options.get('proxy')
        if proxy:
            client_params['proxies'] = proxy
        
        # Inicializar com URL inicial
        current_urls = [start_url]
        max_depth = self.options.get('depth', 2)
        
        async with httpx.AsyncClient(**client_params) as session:
            for depth in range(max_depth):
                if not current_urls or len(self.collected_urls) >= self.options.get('max_urls', 100):
                    break
                
                if self.options.get('debug'):
                    self.log_debug(f"Processando nível {depth + 1}/{max_depth} com {len(current_urls)} URLs")
                
                new_urls = await self._crawl_level(session, current_urls, max_depth - depth)
                current_urls = new_urls[:self.options.get('max_urls', 100) - len(self.collected_urls)]
        
        return sorted(list(self.collected_urls))
    
    def run(self):
        """
        Executa o spider principal.
        """
        try:
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            self.visited_urls.clear()
            self.collected_urls.clear()
            
            start_url = Format.clear_value(self.options.get('data', ''))
            if not start_url:
                self.log_debug("Nenhuma URL inicial fornecida")
                return
            
            # Normalizar URL inicial
            start_url = self._normalize_url(start_url)
            if not self._is_valid_url(start_url):
                self.set_result(f"URL inicial inválida: {start_url}")
                return
            
            if self.options.get('debug'):
                self.log_debug(f"Iniciando spider em: {start_url}")
                self.log_debug(f"Profundidade máxima: {self.options.get('depth', 2)}")
                self.log_debug(f"URLs máximas: {self.options.get('max_urls', 100)}")
            
            # Executar spider
            start_time = time.time()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                collected_urls = loop.run_until_complete(self._run_spider_async(start_url))
            finally:
                loop.close()
            
            end_time = time.time()
            
            if collected_urls:
                # Formatar resultados
                result_lines = []
                
                if self.options.get('debug'):
                    result_lines.append(f"# Spider concluído em {end_time - start_time:.2f}s")
                    result_lines.append(f"# URLs coletadas: {len(collected_urls)}")
                    result_lines.append(f"# URLs visitadas: {len(self.visited_urls)}")
                    result_lines.append("")
                
                result_lines.extend(collected_urls)
                
                self.set_result("\n".join(result_lines))
                
                if self.options.get('debug'):
                    self.log_debug(f"Spider coletou {len(collected_urls)} URLs")
            else:
                self.set_result(f"Nenhuma URL coletada de: {start_url}")
                
        except Exception as e:
            self.handle_error(e, "Erro durante execução do spider")
