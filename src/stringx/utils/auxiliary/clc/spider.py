"""
Módulo CLC Spider para coleta recursiva de URLs com códigos HTTP.

Este módulo implementa um web spider (crawler) que coleta URLs de forma recursiva,
visitando páginas web e extraindo links para exploração adicional baseada em
profundidade configurável. Cada URL é acompanhada do seu código de status HTTP.

O spider oferece:
- Coleta recursiva de URLs com controle de profundidade
- Requisições HTTP/HTTPS assíncronas para performance
- Captura e exibição de códigos de status HTTP para cada URL
- Suporte a proxy e configurações de timeout
- Filtragem e deduplicação automática de URLs
- Extração de URLs usando expressões regulares otimizadas
- Tratamento robusto de erros HTTP/SSL
- Controle de rate limiting para evitar sobrecarga
- Formato de saída: {URL}; {HTTP_CODE}
"""
import re
import asyncio
import signal
import time
from typing import List, Set, Tuple
from urllib.parse import urljoin, urlparse, urlunparse
from collections import deque

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
            'example': './strx -s "https://example.com" -st "echo {STRING}" -module "clc:spider" -pm',
            'output_format': '{URL}; {HTTP_CODE}'
        }
        
        # Get user agent value to avoid pickle issues with module references
        try:
            user_agent_value = getattr(self.setting, 'STRX_USER_AGENT', 'String-X-Spider/1.0')
        except AttributeError:
            user_agent_value = 'String-X-Spider/1.0'
        
        self.options = {
            'data': str(),                    # URL inicial para começar o spider
            'depth': 3,                       # Profundidade máxima de exploração (reduzida para performance)
            'max_urls': 14000,                 # Número máximo de URLs a coletar (reduzida para evitar memory issues)
            'max_url_length': 5096,           # Tamanho máximo de URL para evitar memory issues
            'max_content_size': 5242880,      # Tamanho máximo de conteúdo (5MB)
            'max_total_memory': 104857600,    # Limite de memória total (100MB)
            'timeout': 30,                     # Timeout para requisições HTTP (reduzido)
            'delay': 5.0,                     # Delay entre requisições (reduzido para velocidade)
            'user_agent': user_agent_value,   # User-Agent para requisições HTTP (valor direto, não referência ao módulo)
            'verify_ssl': False,              # Verificar certificados SSL
            'follow_redirects': False,        # Seguir redirecionamentos
            'max_redirects': 3,               # Máximo de redirecionamentos (reduzido)
            'include_external': True,         # Incluir URLs externas ao domínio inicial
            'file_extensions': 'html,htm,php,asp,aspx,jsp',  # Extensões principais (reduzidas)
            'exclude_extensions': 'jpg,jpeg,png,gif,bmp,svg,ico,css,js,pdf,zip,rar,tar,gz,mp3,mp4,avi,mov,wmv,flv,swf,exe,msi,dmg,deb,rpm,woff,woff2,ttf,eot',  # Extensões a excluir (expandidas)
            'include_patterns': str(),        # Padrões regex para incluir URLs
            'exclude_patterns': str(),        # Padrões regex para excluir URLs
            'concurrent_requests': 3,         # Número de requisições simultâneas (reduzido para memory safety)
            'extract_from_js': True,          # Extrair URLs de arquivos JavaScript
            'extract_from_css': False,        # Extrair URLs de arquivos CSS
            'respect_robots': False,          # Respeitar robots.txt (básico)
            'debug': False,                   # Modo de debug
            'proxy': None,                    # Proxy para requisições
            'retry': 1,                       # Número de tentativas por URL (reduzido)
            'retry_delay': None,              # Atraso entre tentativas
        }
        
        # Regex patterns para extração de URLs otimizadas
        self.url_patterns = [
            # URLs padrão HTTP/HTTPS - mais rápido
            re.compile(r'https?://[^\s<>"\']+', re.IGNORECASE),
            # URLs em atributos - compilado uma vez para múltiplos atributos
            re.compile(r'(?:href|src|action)=["\']([^"\']+)["\']', re.IGNORECASE),
            # URLs em JavaScript - otimizado
            re.compile(r'(?:window\.location|location\.href)\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE),
            # URLs em meta refresh
            re.compile(r'content=["\'][^"\']*url=([^"\']+)["\']', re.IGNORECASE),
        ]
        
        # Cache compilado para padrões de validação
        self._exclude_ext_pattern = None
        self._include_ext_pattern = None
        self._exclude_pattern = None
        self._include_pattern = None
        
        # Conjunto para controlar URLs já visitadas - usando deque para performance
        self.visited_urls: Set[str] = set()
        self.collected_urls: Set[str] = set()
        self.url_status: dict = {}  # Store URL -> HTTP status code mapping
        self.url_queue: deque = deque()
        self.base_domain: str = ""
        
        # Cache de rate limiting
        self._last_request_time = 0
        self._request_timestamps = deque(maxlen=100)
        
        # Memory protection
        self._total_content_size = 0
        self._processed_urls = 0
        
        # Interrupt handling
        self._interrupted = False
        self._shutdown_event = None
    
    def __getstate__(self):
        """Custom pickle state to handle module references."""
        state = self.__dict__.copy()
        # Remove the unpicklable entries (module reference)
        if 'setting' in state:
            del state['setting']
        return state
    
    def __setstate__(self, state):
        """Custom pickle restoration to rebuild module references."""
        self.__dict__.update(state)
        # Restore the setting module
        from stringx.config import setting
        self.setting = setting
        
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
        url = url.replace('echo ', '')
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
    
    def _compile_validation_patterns(self):
        """Compila padrões de validação uma vez para reutilização."""
        if self._exclude_ext_pattern is None:
            exclude_ext = self.options.get('exclude_extensions', '').split(',')
            if exclude_ext and exclude_ext != ['']:
                pattern = r'\.(?:' + '|'.join(re.escape(ext.strip()) for ext in exclude_ext if ext.strip()) + ')$'
                self._exclude_ext_pattern = re.compile(pattern, re.IGNORECASE)
        
        if self._include_ext_pattern is None:
            include_ext = self.options.get('file_extensions', '').split(',')
            if include_ext and include_ext != ['']:
                pattern = r'\.(?:' + '|'.join(re.escape(ext.strip()) for ext in include_ext if ext.strip()) + ')$'
                self._include_ext_pattern = re.compile(pattern, re.IGNORECASE)
        
        if self._exclude_pattern is None:
            exclude_patterns = self.options.get('exclude_patterns', '')
            if exclude_patterns:
                try:
                    self._exclude_pattern = re.compile(exclude_patterns, re.IGNORECASE)
                except re.error:
                    self._exclude_pattern = False
        
        if self._include_pattern is None:
            include_patterns = self.options.get('include_patterns', '')
            if include_patterns:
                try:
                    self._include_pattern = re.compile(include_patterns, re.IGNORECASE)
                except re.error:
                    self._include_pattern = False

    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida para coleta (versão otimizada com validação de tamanho).
        
        Args:
            url: URL a ser verificada
            
        Returns:
            True se a URL for válida
        """
        if not url or not url.startswith(('http://', 'https://')):
            return False
        
        # Validar tamanho da URL para evitar memory issues
        max_url_length = self.options.get('max_url_length', 2048)
        if len(url) > max_url_length:
            if self.options.get('debug'):
                self.log_debug(f"[!] URL muito longa ({len(url)} chars): {url[:100]}...")
            return False
        
        # Parse uma vez e reutiliza
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False
        except Exception:
            return False
        
        # Verificar se é domínio externo
        if not self.options.get('include_external', False):
            if self.base_domain and parsed.netloc.lower() != self.base_domain.lower():
                return False
        
        # Compilar padrões se necessário
        self._compile_validation_patterns()
        
        path_lower = parsed.path.lower()
        
        # Verificar extensões excluídas (usando regex compilada)
        if self._exclude_ext_pattern and self._exclude_ext_pattern.search(path_lower):
            return False
        
        # Verificar extensões incluídas (usando regex compilada)
        if self._include_ext_pattern:
            has_extension = '.' in path_lower.split('/')[-1]
            if has_extension and not self._include_ext_pattern.search(path_lower):
                return False
        
        # Verificar padrões de exclusão (usando regex compilada)
        if self._exclude_pattern and self._exclude_pattern.search(url):
            return False
        
        # Verificar padrões de inclusão (usando regex compilada)
        if self._include_pattern and not self._include_pattern.search(url):
            return False
        
        return True
    
    def _extract_urls_from_content(self, content: str, base_url: str) -> List[str]:
        """
        Extrai URLs do conteúdo HTML (versão otimizada).
        
        Args:
            content: Conteúdo HTML da página
            base_url: URL base para resolver URLs relativas
            
        Returns:
            Lista de URLs encontradas
        """
        urls = set()
        
        # Usar regex primeiro (mais rápido) e depois BeautifulSoup se necessário
        try:
            # Extração rápida com regex patterns otimizadas
            for pattern in self.url_patterns:
                matches = pattern.findall(content)
                for match in matches:
                    # match pode ser uma tupla ou string dependendo do padrão
                    if isinstance(match, tuple):
                        match = match[0] if match else ""
                    
                    if match and len(match) > 3:  # Skip muito curtas
                        normalized = self._normalize_url(match, base_url)
                        if normalized and self._is_valid_url(normalized):
                            urls.add(normalized)
            
            # Se não encontrou muitas URLs com regex, tenta BeautifulSoup
            if len(urls) < 5:
                try:
                    # Usar parser mais rápido do BeautifulSoup
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Batch processing de links
                    for link in soup.find_all('a', href=True, limit=500):  # Limitar busca
                        href = link.get('href', '')
                        if href and len(href) > 3:
                            normalized = self._normalize_url(href, base_url)
                            if normalized and self._is_valid_url(normalized):
                                urls.add(normalized)
                    
                    # Extrair de tags com src (se configurado) - mais seletivo
                    if self.options.get('extract_from_js', False):
                        for tag in soup.find_all(['script', 'link'], src=True, limit=100):
                            src = tag.get('src', '')
                            if src and len(src) > 3:
                                normalized = self._normalize_url(src, base_url)
                                if normalized and self._is_valid_url(normalized):
                                    urls.add(normalized)
                                    
                        for tag in soup.find_all('link', href=True, limit=100):
                            href = tag.get('href', '')
                            if href and len(href) > 3:
                                normalized = self._normalize_url(href, base_url)
                                if normalized and self._is_valid_url(normalized):
                                    urls.add(normalized)
                
                except Exception as e:
                    if self.options.get('debug'):
                        self.log_debug(f"[x] BeautifulSoup parsing falhou: {e}")
        
        except Exception as e:
            if self.options.get('debug'):
                self.log_debug(f"[x] Erro ao extrair URLs: {e}")
        
        return list(urls)
    
    async def _fetch_url(self, session: httpx.AsyncClient, url: str) -> Tuple[str, str, bool, int]:
        """
        Faz requisição HTTP para uma URL.
        
        Args:
            session: Cliente HTTP assíncrono
            url: URL a ser requisitada
            
        Returns:
            Tupla (url, content, success, status_code)
        """
        try:
            if self.options.get('debug'):
                self.log_debug(f"[*] Fazendo requisição para: {url}")
            
            response = await session.get(url)
            status_code = response.status_code
            
            # Store the status code for this URL
            self.url_status[url] = status_code
            
            # Verificar se é conteúdo HTML/texto
            content_type = response.headers.get('content-type', '').lower()
            if not any(ct in content_type for ct in ['text/html', 'text/plain', 'application/xhtml']):
                if self.options.get('debug'):
                    self.log_debug(f"[!] Tipo de conteúdo ignorado: {content_type}")
                return url, "", False, status_code
            
            # Verificar tamanho do conteúdo usando configuração
            max_content_size = self.options.get('max_content_size', 5242880)  # 5MB default
            if len(response.content) > max_content_size:
                if self.options.get('debug'):
                    self.log_debug(f"[!] Conteúdo muito grande, ignorando: {len(response.content)} bytes")
                return url, "", False, status_code
            
            content = response.text
            return url, content, True, status_code
            
        except httpx.TimeoutException:
            if self.options.get('debug'):
                self.log_debug(f"[!] Timeout na requisição: {url}")
            self.url_status[url] = 408  # Request Timeout
            return url, "", False, 408
        except httpx.RequestError as e:
            if self.options.get('debug'):
                self.log_debug(f"[x] Erro de requisição para {url}: {e}")
            self.url_status[url] = 0  # Connection error
            return url, "", False, 0
        except Exception as e:
            if self.options.get('debug'):
                self.log_debug(f"[x] Erro inesperado para {url}: {e}")
            self.url_status[url] = -1  # Unknown error
            return url, "", False, -1
    
    def _setup_signal_handlers(self):
        """
        Configura manipuladores de sinal para interrupção graciosa.
        """
        try:
            def signal_handler(signum, frame):
                self._interrupted = True
                if self.options.get('debug'):
                    self.log_debug("Recebido sinal de interrupção, parando spider...")
                    
            # Configure signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        except ValueError:
            # signal only works in main thread, use alternative approach
            if self.options.get('debug'):
                self.log_debug("Signal handlers não disponíveis (não é thread principal)")
    
    async def _crawl_level(self, session: httpx.AsyncClient, urls: List[str], current_depth: int) -> List[str]:
        """
        Faz crawling de um nível de URLs (versão otimizada).
        
        Args:
            session: Cliente HTTP assíncrono
            urls: Lista de URLs para processar
            current_depth: Profundidade atual
            
        Returns:
            Lista de novas URLs encontradas
        """
        if not urls or current_depth <= 0 or self._interrupted:
            return []
        
        new_urls = []
        semaphore = asyncio.Semaphore(self.options.get('concurrent_requests', 5))
        batch_new_urls = asyncio.Queue(maxsize=1000)
        
        async def process_url(url: str):
            # Check for interruption before processing
            if self._interrupted:
                return
                
            async with semaphore:
                if url in self.visited_urls or len(self.collected_urls) >= self.options.get('max_urls', 100) or self._interrupted:
                    return
                
                # Memory protection check
                #max_memory = self.options.get('max_total_memory', 104857600)  # 100MB
                #if self._total_content_size > max_memory:
                #    if self.options.get('debug'):
                #        self.log_debug(f"[!] Memory limit reached: {self._total_content_size} bytes")
                #    return
                
                self.visited_urls.add(url)
                self.collected_urls.add(url)
                self._processed_urls += 1
                
                # Rate limiting otimizado - não bloquear todo o semaphore
                delay = self.options.get('delay', 1.0)
                if delay > 0:
                    current_time = time.time()
                    if current_time - self._last_request_time < delay:
                        await asyncio.sleep(delay - (current_time - self._last_request_time))
                    self._last_request_time = current_time
                
                _, content, success, status_code = await self._fetch_url(session, url)
                
                if success and content:
                    # Track content size for memory protection
                    self._total_content_size += len(content)
                    
                    # Extrair URLs do conteúdo
                    found_urls = self._extract_urls_from_content(content, url)
                    
                    # Batch add para evitar locks frequentes
                    valid_new_urls = []
                    for found_url in found_urls:
                        if (found_url not in self.visited_urls and 
                            found_url not in self.collected_urls and 
                            len(self.collected_urls) < self.options.get('max_urls', 100)):
                            valid_new_urls.append(found_url)
                            self.collected_urls.add(found_url)
                    
                    # Adicionar em batch para reduzir contention
                    for valid_url in valid_new_urls[:50]:  # Limitar para evitar memory bloat
                        try:
                            await batch_new_urls.put(valid_url, timeout=0.1)
                        except asyncio.QueueFull:
                            break
        
        # Processar URLs em paralelo com chunks menores para evitar memory spike
        chunk_size = min(10, len(urls))  # Reduzir chunk size para memory safety
        for i in range(0, len(urls), chunk_size):
            # Check for interruption
            if self._interrupted:
                if self.options.get('debug'):
                    self.log_debug("[!] Spider interrupted, stopping processing")
                break
                
            # Check memory limit before processing next chunk
            max_memory = self.options.get('max_total_memory', 104857600)
            if self._total_content_size > max_memory:
                if self.options.get('debug'):
                    self.log_debug(f"[!] Memory limit reached, stopping processing")
                break
                
            chunk = urls[i:i + chunk_size]
            tasks = [process_url(url) for url in chunk]
            
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except asyncio.CancelledError:
                if self.options.get('debug'):
                    self.log_debug("[!] Tasks cancelled due to interruption")
                break
            
            # Small delay between chunks to allow garbage collection and check for interruption
            try:
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
        
        # Coletar URLs encontradas
        while not batch_new_urls.empty():
            try:
                url = batch_new_urls.get_nowait()
                new_urls.append(url)
            except asyncio.QueueEmpty:
                break
        
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
        
        try:
            async with httpx.AsyncClient(**client_params) as session:
                for depth in range(max_depth):
                    # Check for interruption at each depth level
                    if self._interrupted:
                        if self.options.get('debug'):
                            self.log_debug("[!] Spider interrupted at depth level")
                        break
                        
                    if not current_urls or len(self.collected_urls) >= self.options.get('max_urls', 100):
                        break
                    
                    if self.options.get('debug'):
                        self.log_debug(f"[*] Processando nível {depth + 1}/{max_depth} com {len(current_urls)} URLs")
                    
                    try:
                        new_urls = await self._crawl_level(session, current_urls, max_depth - depth)
                        current_urls = new_urls[:self.options.get('max_urls', 100) - len(self.collected_urls)]
                    except asyncio.CancelledError:
                        if self.options.get('debug'):
                            self.log_debug("[!] Crawl level cancelled")
                        break
            
            return sorted(list(self.collected_urls))
        except asyncio.CancelledError:
            if self.options.get('debug'):
                self.log_debug("[!] Spider async cancelled")
            return sorted(list(self.collected_urls))
        except Exception as e:
            if self.options.get('debug'):
                self.log_debug(f"[x] Erro no spider async: {e}")
            return sorted(list(self.collected_urls))
    
    def run(self):
        """
        Executa o spider principal.
        """
        try:
            # Limpar resultados anteriores e reinicializar contadores
            self._result[self._get_cls_name()].clear()
            self.visited_urls.clear()
            self.collected_urls.clear()
            self.url_status.clear()
            self._total_content_size = 0
            self._processed_urls = 0
            
            start_url = Format.clear_value(self.options.get('data', ''))
            if not start_url:
                self.log_debug("Nenhuma URL inicial fornecida")
                return
            
            # Normalizar URL inicial
            start_url = self._normalize_url(start_url)
            if not self._is_valid_url(start_url):
                self.log_debug(f"URL inicial inválida: {start_url}")
                return
            
            if self.options.get('debug'):
                self.log_debug(f"Iniciando spider em: {start_url}")
                self.log_debug(f"Profundidade máxima: {self.options.get('depth', 2)}")
                self.log_debug(f"URLs máximas: {self.options.get('max_urls', 100)}")
            
            # Executar spider - com manejo adequado do event loop
            start_time = time.time()
            collected_urls = []
            
            try:
                # Setup signal handling for graceful shutdown
                self._setup_signal_handlers()
                
                # Use asyncio.run with proper KeyboardInterrupt handling
                try:
                    collected_urls = asyncio.run(self._run_spider_async(start_url))
                except KeyboardInterrupt:
                    self._interrupted = True
                    if self.options.get('debug'):
                        self.log_debug("Spider interrompido por KeyboardInterrupt")
                    collected_urls = list(self.collected_urls)
                    
            except KeyboardInterrupt:
                if self.options.get('debug'):
                    self.log_debug("Spider interrompido pelo usuário (Ctrl+C)")
                self._interrupted = True
                collected_urls = list(self.collected_urls)  # Return what we have so far
            except Exception as e:
                if self.options.get('debug'):
                    self.log_debug(f"Erro durante execução do spider: {e}")
                collected_urls = []
            finally:
                # Ensure any pending async operations are cleaned up
                try:
                    # Close any remaining event loops cleanly
                    loop = asyncio.get_event_loop()
                    if not loop.is_closed():
                        pending = asyncio.all_tasks(loop)
                        if pending:
                            for task in pending:
                                task.cancel()
                except RuntimeError:
                    # No event loop running, which is fine
                    pass
            
            end_time = time.time()
            
            if collected_urls:
                # Formatar resultados
                result_lines = []
                
                if self.options.get('debug'):
                    status = "interrompido" if self._interrupted else "concluído"
                    result_lines.append(f"# Spider {status} em {end_time - start_time:.2f}s")
                    result_lines.append(f"# URLs coletadas: {len(collected_urls)}")
                    result_lines.append(f"# URLs visitadas: {len(self.visited_urls)}")
                    result_lines.append("")
                
                # Format URLs with HTTP status codes
                for url in collected_urls:
                    status_code = self.url_status.get(url, 'N/A')
                    result_lines.append(f"{url}; {status_code}")
                
                self.set_result("\n".join(result_lines))
                
                if self.options.get('debug'):
                    self.log_debug(f"Spider coletou {len(collected_urls)} URLs")
            else:
                # Even if no URLs collected, show the start URL with its status
                start_status = self.url_status.get(start_url, 'N/A')
                self.set_result(f"{start_url}; {start_status}")
                self.log_debug(f"Nenhuma URL coletada de: {start_url}")
                
        except Exception as e:
            self.handle_error(e, "Erro durante execução do spider")
