"""
Módulo CLC URL Check para verificação de status HTTP.

Este módulo implementa um verificador de URLs que realiza requisições HTTP
assíncronas para verificar o status de múltiplas URLs simultaneamente,
retornando apenas URLs que respondem com algum código HTTP.

O módulo oferece:
- Verificação assíncrona de status HTTP com httpx
- Rate limiting inteligente com aiometer (se disponível)
- Controle de concorrência para múltiplas requisições
- Tratamento robusto de erros de conexão e timeout
- Suporte a proxy e configurações de timeout
- Filtragem automática de URLs inacessíveis
- Fallback automático quando aiometer não está disponível
- Formato de saída: {URL}; {HTTP_CODE}
"""
import asyncio
import signal
from typing import List, Dict, Set, Tuple
from urllib.parse import urlparse
import re

# Bibliotecas de terceiros
import httpx
try:
    import aiometer
except ImportError:
    aiometer = None

# Módulos locais
from stringx.core.basemodule import BaseModule
from stringx.core.format import Format


class UrlChecker(BaseModule):
    """
    Verificador assíncrono de status HTTP para URLs.
    
    Esta classe implementa um verificador que testa múltiplas URLs de forma
    assíncrona, verificando seus códigos de status HTTP e retornando apenas
    aquelas que respondem com códigos válidos.
    
    Herda de BaseModule fornecendo interface padrão para módulos auxiliares.
    """
    
    def __init__(self):
        """
        Inicializa o verificador com configurações padrão.
        """
        super().__init__()
        
        self.meta = {
            'name': 'URL Status Checker',
            'author': 'MrCl0wn',
            'version': '1.2',
            'description': 'Verifica status HTTP de URLs de forma assíncrona com aiometer (otimizado para velocidade)',
            'type': 'collector',
            'example': './strx -s "https://example.com" -st "echo {STRING}" -module "clc:url_check" -pm',
            'output_format': '{ORIGINAL_URL} -> {FINAL_URL}; {HTTP_CODE}',
            'speed_modes': {
                'fast': 'Máxima velocidade (100+ concurrent, 200+ req/s)',
                'balanced': 'Balanço velocidade/compatibilidade (50 concurrent, 100 req/s)',
                'conservative': 'Modo conservador (10 concurrent, 20 req/s)'
            },
            'output_options': {
                'include_errors': 'Inclui URLs com qualquer tipo de erro (códigos 0, -1)',
                'include_unreachable': 'Inclui apenas URLs que não retornaram código HTTP',
                'show_all_attempts': 'Mostra todas as URLs testadas, independente do resultado',
                'show_final_url': 'Mostra URL final após redirecionamentos na saída'
            }
        }
        
        # Get user agent value to avoid pickle issues
        try:
            user_agent_value = getattr(self.setting, 'STRX_USER_AGENT', 'String-X-UrlChecker/1.0')
        except AttributeError:
            user_agent_value = 'String-X-UrlChecker/1.0'
        
        self.options = {
            'data': str(),                    # URLs para verificar (uma por linha ou separadas por vírgula)
            'timeout': 5,                     # Timeout para requisições HTTP (reduzido para velocidade)
            'max_concurrent': 50,             # Número máximo de requisições simultâneas (aumentado)
            'delay': 1,                       # Delay entre requisições (removido para velocidade)
            'max_per_second': 100,            # Rate limit (requests per second) - aumentado para velocidade
            'user_agent': user_agent_value,   # User-Agent para requisições HTTP
            'verify_ssl': False,              # Verificar certificados SSL
            'follow_redirects': True,        # Seguir redirecionamentos (False para velocidade)
            'max_redirects': 3,               # Máximo de redirecionamentos
            'methods': 'HEAD',                # Método HTTP para teste (HEAD é mais rápido que GET)
            'include_errors': False,          # Incluir URLs com erro (código 0, -1)
            'include_unreachable': False,     # Incluir URLs que não retornaram nenhum código HTTP
            'show_all_attempts': False,       # Mostrar todas as URLs testadas, independente do resultado
            'show_final_url': True,           # Mostrar URL final após redirecionamentos
            'status_filter': str(),           # Filtrar por códigos de status (ex: "200,404,500")
            'exclude_status': str(),          # Excluir códigos de status específicos
            'retry_attempts': 1,              # Tentativas por URL (sem retry para velocidade)
            'retry_delay': 0.5,               # Delay entre tentativas (reduzido)
            'debug': False,                   # Modo debug
            'proxy': None,                    # Proxy para requisições
            'speed_mode': 'fast',         # Modo de velocidade: 'fast', 'balanced', 'conservative'
        }
        
        # Apply speed mode presets
        self._apply_speed_mode()
        
        # Control structures
        self.url_results: Dict[str, Tuple[int, str]] = {}
        self.failed_urls: Set[str] = set()
        self.processed_count = 0
        self.interrupted = False
        
        # URL validation regex
        self.url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Valida se uma URL está bem formada.
        
        Args:
            url: URL para validar
            
        Returns:
            True se a URL for válida
        """
        if not url or not isinstance(url, str):
            return False
        
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            return False
        
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and self.url_pattern.match(url)
        except Exception:
            return False
    
    def _parse_urls_from_input(self, data: str) -> List[str]:
        """
        Extrai URLs válidas da entrada de dados.
        
        Args:
            data: String contendo URLs (separadas por linha ou vírgula)
            
        Returns:
            Lista de URLs válidas
        """
        urls = []
        
        if not data:
            return urls
        
        # Split by newlines and process each line
        lines = data.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try regex first to find URLs in the line
            import re
            url_matches = re.findall(r'https?://[^\s,;]+', line, re.IGNORECASE)
            
            if url_matches:
                # Found URLs with regex
                for url in url_matches:
                    url = url.strip().rstrip('.,;')
                    if self._is_valid_url(url):
                        urls.append(url)
                    elif self.options.get('debug'):
                        self.log_debug(f"URL inválida ignorada: {url}")
            else:
                # Try splitting by comma
                if ',' in line:
                    url_candidates = [u.strip() for u in line.split(',')]
                else:
                    url_candidates = [line]
                
                for url_candidate in url_candidates:
                    url_candidate = url_candidate.strip()
                    if self._is_valid_url(url_candidate):
                        urls.append(url_candidate)
                    elif self.options.get('debug'):
                        self.log_debug(f"URL inválida ignorada: {url_candidate}")
        
        return list(set(urls))  # Remove duplicates
    
    def _should_include_status(self, status_code: int) -> bool:
        """
        Verifica se o código de status deve ser incluído nos resultados.
        
        Args:
            status_code: Código de status HTTP
            
        Returns:
            True se deve incluir o status
        """
        # Show all attempts option overrides everything
        if self.options.get('show_all_attempts', False):
            return True
        
        # Check for unreachable URLs (status codes 0, -1)
        if status_code <= 0:
            # include_unreachable specifically for URLs that didn't return any HTTP code
            if self.options.get('include_unreachable', False):
                return True
            # include_errors is the broader option for any error condition
            if self.options.get('include_errors', False):
                return True
            # Otherwise exclude error codes
            return False
        
        # For valid HTTP status codes (> 0), apply filtering
        
        # Check status filter
        status_filter = self.options.get('status_filter', '').strip()
        if status_filter:
            allowed_statuses = []
            for status in status_filter.split(','):
                try:
                    allowed_statuses.append(int(status.strip()))
                except ValueError:
                    continue
            if allowed_statuses and status_code not in allowed_statuses:
                return False
        
        # Check exclude status
        exclude_status = self.options.get('exclude_status', '').strip()
        if exclude_status:
            excluded_statuses = []
            for status in exclude_status.split(','):
                try:
                    excluded_statuses.append(int(status.strip()))
                except ValueError:
                    continue
            if status_code in excluded_statuses:
                return False
        
        return True
    
    def _apply_speed_mode(self):
        """
        Aplica presets de configuração baseados no modo de velocidade.
        """
        speed_mode = self.options.get('speed_mode', 'balanced')
        
        if speed_mode == 'fast':
            # Máxima velocidade - pode sobrecarregar alguns servidores
            self.options.update({
                'timeout': 3,
                'max_concurrent': 100,
                'max_per_second': 200,
                'delay': 0,
                'retry_attempts': 1,
                'retry_delay': 0.2,
                'methods': 'HEAD'
            })
            
        elif speed_mode == 'balanced':
            # Balanço entre velocidade e compatibilidade (padrão atual)
            self.options.update({
                'timeout': 5,
                'max_concurrent': 50,
                'max_per_second': 100,
                'delay': 0,
                'retry_attempts': 1,
                'retry_delay': 0.5,
                'methods': 'HEAD'
            })
            
        elif speed_mode == 'conservative':
            # Modo conservador - amigável com todos os servidores
            self.options.update({
                'timeout': 10,
                'max_concurrent': 10,
                'max_per_second': 20,
                'delay': 0.2,
                'retry_attempts': 2,
                'retry_delay': 1.0,
                'methods': 'HEAD,GET'
            })
            
        if self.options.get('debug'):
            self.log_debug(f"Aplicando modo de velocidade: {speed_mode}")
    
    async def _check_url_status(self, session: httpx.AsyncClient, url: str, method: str = 'GET') -> Tuple[str, int, str]:
        """
        Verifica o status HTTP de uma URL.
        
        Args:
            session: Cliente HTTP assíncrono
            url: URL para verificar
            method: Método HTTP (GET, HEAD, etc)
            
        Returns:
            Tupla (original_url, status_code, final_url)
        """
        if self.interrupted:
            return url, -1, url
        
        retry_attempts = max(1, self.options.get('retry_attempts', 1))
        retry_delay = self.options.get('retry_delay', 1.0)
        
        for attempt in range(retry_attempts):
            if self.interrupted:
                return url, -1, url, url
            
            try:
                if self.options.get('debug'):
                    self.log_debug(f"Verificando {url} (tentativa {attempt + 1}/{retry_attempts})")
                
                # Check for interruption before making request
                if self.interrupted:
                    return url, -1, url
                
                response = await session.request(method, url)
                status_code = response.status_code
                final_url = str(response.url)
                
                if self.options.get('debug'):
                    if final_url != url:
                        self.log_debug(f"{url} -> {final_url} ({status_code})")
                    else:
                        self.log_debug(f"{url} -> {status_code}")
                
                return url, status_code, final_url
                
            except asyncio.CancelledError:
                # Task was cancelled, likely due to interruption
                self.interrupted = True
                return url, -1, url, url
                
            except httpx.TimeoutException:
                if self.options.get('debug'):
                    self.log_debug(f"Timeout: {url}")
                if attempt < retry_attempts - 1 and not self.interrupted:
                    try:
                        await asyncio.sleep(retry_delay)
                    except asyncio.CancelledError:
                        self.interrupted = True
                        return url, -1, url, url
                    continue
                return url, 408, url  # Request Timeout
                
            except httpx.ConnectError:
                if self.options.get('debug'):
                    self.log_debug(f"Erro de conexão: {url}")
                if attempt < retry_attempts - 1 and not self.interrupted:
                    try:
                        await asyncio.sleep(retry_delay)
                    except asyncio.CancelledError:
                        self.interrupted = True
                        return url, -1, url, url
                    continue
                return url, 0, url  # Connection failed
                
            except httpx.RequestError as e:
                if self.options.get('debug'):
                    self.log_debug(f"Erro de requisição para {url}: {e}")
                if attempt < retry_attempts - 1 and not self.interrupted:
                    try:
                        await asyncio.sleep(retry_delay)
                    except asyncio.CancelledError:
                        self.interrupted = True
                        return url, -1, url, url
                    continue
                return url, -1, url, url  # Request error
                
            except Exception as e:
                if self.options.get('debug'):
                    self.log_debug(f"Erro inesperado para {url}: {e}")
                if attempt < retry_attempts - 1 and not self.interrupted:
                    try:
                        await asyncio.sleep(retry_delay)
                    except asyncio.CancelledError:
                        self.interrupted = True
                        return url, -1, url, url
                    continue
                return url, -1, url, url  # Unknown error
        
        return url, -1, url  # All attempts failed
    
    async def _manual_url_processing(self, session: httpx.AsyncClient, urls: List[str], methods: List[str], results: Dict[str, Tuple[int, str]]) -> Dict[str, Tuple[int, str]]:
        """
        Fallback manual URL processing when aiometer is not available.
        
        Args:
            session: HTTP client session
            urls: List of URLs to process
            methods: HTTP methods to try
            results: Existing results dictionary
            
        Returns:
            Updated results dictionary with {url: (status_code, final_url)}
        """
        # Control concurrency with semaphore
        semaphore = asyncio.Semaphore(self.options.get('max_concurrent', 20))
        delay = self.options.get('delay', 0.1)
        
        async def check_url_with_methods_and_delay(url: str) -> Tuple[str, int, str]:
            """Check URL with methods and apply delay."""
            if self.interrupted:
                return url, -1, url, url
            
            async with semaphore:
                # Try each method until we get a valid response
                for method in methods:
                    if self.interrupted:
                        return url, -1, url
                    
                    url_result, status_code, final_url = await self._check_url_status(session, url, method)
                    
                    # If we get a successful response, return it
                    if status_code > 0:
                        if delay > 0:
                            try:
                                await asyncio.sleep(delay)
                            except asyncio.CancelledError:
                                self.interrupted = True
                                return url, -1, url
                        return url_result, status_code, final_url
                
                # If all methods failed, return the last result
                if delay > 0:
                    try:
                        await asyncio.sleep(delay)
                    except asyncio.CancelledError:
                        self.interrupted = True
                        return url, -1, url, url
                return url, status_code, final_url
        
        # Process URLs in chunks to avoid overwhelming the server
        # Optimize chunk size based on concurrency for better performance\n        
        max_concurrent = self.options.get('max_concurrent', 50)
        chunk_size = min(max_concurrent * 2, len(urls))
        for i in range(0, len(urls), chunk_size):
            if self.interrupted:
                if self.options.get('debug'):
                    self.log_debug("[!] URL checking interrupted during manual processing")
                break
            
            chunk = urls[i:i + chunk_size]
            
            if self.options.get('debug'):
                self.log_debug(f"Processando chunk {i//chunk_size + 1}/{(len(urls)-1)//chunk_size + 1} ({len(chunk)} URLs)")
            
            # Create tasks for this chunk
            tasks = [check_url_with_methods_and_delay(url) for url in chunk]
            
            try:
                # Process chunk with proper cancellation handling
                chunk_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in chunk_results:
                    if self.interrupted:
                        break
                        
                    if isinstance(result, Exception):
                        if self.options.get('debug'):
                            self.log_debug(f"Task exception: {result}")
                        continue
                    
                    url, status_code, final_url = result
                    if self._should_include_status(status_code):
                        results[url] = (status_code, final_url)
                    
                    self.processed_count += 1
            
            except asyncio.CancelledError:
                if self.options.get('debug'):
                    self.log_debug("[!] Tasks cancelled during manual processing")
                self.interrupted = True
                break
            except Exception as e:
                if self.options.get('debug'):
                    self.log_debug(f"[!] Chunk processing error: {e}")
                continue
            
            # Small delay between chunks only if delay is configured
            delay = self.options.get('delay', 0)
            if delay > 0 and not self.interrupted and i + chunk_size < len(urls):
                try:
                    await asyncio.sleep(min(delay, 0.1))  # Cap delay to prevent slowdown
                except asyncio.CancelledError:
                    self.interrupted = True
                    break
        
        return results
    
    async def _check_urls_async(self, urls: List[str]) -> Dict[str, Tuple[int, str]]:
        """
        Verifica múltiplas URLs de forma assíncrona.
        
        Args:
            urls: Lista de URLs para verificar
            
        Returns:
            Dicionário com {url: (status_code, final_url)}
        """
        if not urls:
            return {}
        
        results = {}
        
        # Setup HTTP client with performance optimizations
        timeout_value = self.options.get('timeout', 5)
        concurrent = self.options.get('max_concurrent', 50)
        
        timeout = httpx.Timeout(
            timeout=timeout_value,
            connect=min(timeout_value, 3),  # Faster connection timeout
            read=timeout_value,
            pool=0.5  # Quick pool timeout
        )
        
        # Increase connection limits for better performance
        limits = httpx.Limits(
            max_connections=concurrent * 2,        # Double the connections
            max_keepalive_connections=concurrent,  # Keep connections alive
            keepalive_expiry=30                    # Keep connections for 30s
        )
        
        # Minimal headers for faster requests
        headers = {
            'User-Agent': self.options.get('user_agent', 'String-X-UrlChecker/1.0'),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip',  # Enable compression
        }
        
        client_params = {
            'timeout': timeout,
            'follow_redirects': self.options.get('follow_redirects', True),
            'headers': headers,
            'limits': limits,
            'verify': self.options.get('verify_ssl', False),
        }
        
        # Add proxy if configured
        proxy = self.options.get('proxy')
        if proxy:
            client_params['proxies'] = proxy
        
        # Get HTTP methods to try
        methods = [m.strip().upper() for m in self.options.get('methods', 'GET').split(',')]
        if not methods:
            methods = ['GET']
        
        try:
            async with httpx.AsyncClient(**client_params) as session:
                
                async def check_url_with_methods(url: str) -> Tuple[str, int, str]:
                    """Check URL with multiple methods if needed."""
                    if self.interrupted:
                        return url, -1, url
                    
                    # Try each method until we get a valid response
                    for method in methods:
                        if self.interrupted:
                            return url, -1, url
                        
                        url_result, status_code, final_url = await self._check_url_status(session, url, method)
                        
                        # If we get a successful response, return it
                        if status_code > 0:
                            return url_result, status_code, final_url
                    
                    # If all methods failed, return the last result
                    return url, status_code, final_url
                
                # Use aiometer.amap if available, otherwise fall back to manual processing
                if aiometer is not None:
                    # Configure aiometer rate limiting
                    max_per_second = self.options.get('max_per_second', 10)
                    max_concurrent = self.options.get('max_concurrent', 20)
                    
                    if self.options.get('debug'):
                        self.log_debug(f"Using aiometer with {max_per_second} req/s, {max_concurrent} concurrent")
                    
                    try:
                        # Use aiometer.amap for rate-limited concurrent execution
                        async with aiometer.amap(
                            check_url_with_methods,
                            urls,
                            max_per_second=max_per_second,
                            max_at_once=max_concurrent
                        ) as url_results_async:
                            # Process results as they come
                            async for result in url_results_async:
                                if self.interrupted:
                                    break
                                
                                url, status_code, final_url = result
                                if self._should_include_status(status_code):
                                    results[url] = (status_code, final_url)
                                
                                self.processed_count += 1
                            
                    except asyncio.CancelledError:
                        if self.options.get('debug'):
                            self.log_debug("[!] Aiometer execution cancelled")
                        self.interrupted = True
                    except Exception as e:
                        if self.options.get('debug'):
                            self.log_debug(f"[!] Aiometer execution error: {e}")
                        # Fall back to manual processing
                        results = await self._manual_url_processing(session, urls, methods, results)
                else:
                    # Fall back to manual processing when aiometer is not available
                    if self.options.get('debug'):
                        self.log_debug("Aiometer not available, using manual processing")
                    results = await self._manual_url_processing(session, urls, methods, results)
        
        except asyncio.CancelledError:
            if self.options.get('debug'):
                self.log_debug("[!] URL checking async cancelled")
            self.interrupted = True
        except Exception as e:
            if self.options.get('debug'):
                self.log_debug(f"Erro na verificação assíncrona: {e}")
        
        return results
    
    def _setup_signal_handlers(self):
        """
        Configura manipuladores de sinal para interrupção graciosa.
        """
        try:
            def signal_handler(signum, frame):
                self.interrupted = True
                if self.options.get('debug'):
                    self.log_debug("Verificação interrompida pelo usuário")
                # Raise KeyboardInterrupt to properly handle the signal
                raise KeyboardInterrupt("URL checking interrupted by user")
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        except ValueError:
            # Signal handlers not available (not main thread)
            if self.options.get('debug'):
                self.log_debug("Signal handlers não disponíveis (não é thread principal)")
    
    def run(self):
        """
        Executa a verificação de URLs.
        """
        try:
            # Clear previous results
            self._result[self._get_cls_name()].clear()
            self.url_results.clear()
            self.failed_urls.clear()
            self.processed_count = 0
            self.interrupted = False
            
            # Get input data
            # Don't use Format.clear_value as it removes newlines which we need
            data = self.options.get('data', '')
            if isinstance(data, str):
                data = data.strip()
            if not data:
                self.log_debug("Nenhuma URL fornecida para verificação")
                return
            
            # Parse URLs from input
            urls = self._parse_urls_from_input(data)
            if not urls:
                self.log_debug("Nenhuma URL válida encontrada na entrada")
                return
            
            if self.options.get('debug'):
                self.log_debug(f"Verificando {len(urls)} URLs...")
            
            # Setup signal handling
            self._setup_signal_handlers()
            
            # Run async URL checking with proper interrupt handling
            try:
                # Use asyncio.run with proper KeyboardInterrupt handling
                try:
                    results = asyncio.run(self._check_urls_async(urls))
                except KeyboardInterrupt:
                    self.interrupted = True
                    if self.options.get('debug'):
                        self.log_debug("URL checking interrompida por KeyboardInterrupt")
                    results = self.url_results
            except KeyboardInterrupt:
                self.interrupted = True
                results = self.url_results
                if self.options.get('debug'):
                    self.log_debug("Verificação interrompida pelo usuário")
            except Exception as e:
                if self.options.get('debug'):
                    self.log_debug(f"Erro durante verificação: {e}")
                results = self.url_results
            
            # Format results
            if results:
                result_lines = []
                
                # Sort by URL for consistent output
                for url in sorted(results.keys()):
                    status_code, final_url = results[url]
                    
                    # Format output based on show_final_url option
                    if self.options.get('show_final_url', True) and final_url != url:
                        result_lines.append(f"{url} -> {final_url}; {status_code}")
                    else:
                        result_lines.append(f"{url}; {status_code}")
                
                self.set_result("\n".join(result_lines))
                
                if self.options.get('debug'):
                    status = "interrompida" if self.interrupted else "concluída"
                    self.log_debug(f"Verificação {status}: {len(results)} URLs com status válido de {len(urls)} testadas")
            else:
                self.log_debug("Nenhuma URL retornou status válido")
        
        except Exception as e:
            self.handle_error(e, "Erro durante verificação de URLs")