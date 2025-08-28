"""
Módulo CLC para dorking usando motor de busca Ezilon.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Ezilon, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.

Ezilon é um motor de busca e diretório web menos conhecido que pode ser útil para:
- Descobrir resultados que não aparecem em motores de busca mainstream
- Obter informações alternativas quando outros motores limitam resultados
- Contornar limitações de rate impostas por buscadores mais populares
- Encontrar sites e conteúdos indexados apenas em diretórios específicos
- Diversificar fontes de informação em investigações OSINT

O uso de motores de busca alternativos como o Ezilon permite uma cobertura
mais abrangente durante a coleta de informações e pode revelar conteúdos
que não foram indexados ou são difíceis de encontrar em outros buscadores.
"""
import re
import random
import backoff
import asyncio
from bs4 import BeautifulSoup
from stringx.core.format import Format
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException
from urllib.parse import urljoin, urlparse, quote_plus, unquote

from stringx.core.http_async import HTTPClient
from stringx.core.basemodule import BaseModule
from stringx.core.retry import retry_operation
from stringx.core.user_agent_generator import UserAgentGenerator

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
        # Instância do cliente HTTP assíncrono
        self.request  = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Ezilon Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Ezilon',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:ezilon" -pm'
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
                self.log_debug("Dork não fornecido.")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            # Coletando resultados
            results = self._search_ezilon(dork)
            
            if not results:
                self.log_debug(f"Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.handle_error(e, "Erro na busca")
    
    
    def _search_ezilon(self, dork: str) -> list:
        """
        Wrapper síncrono para busca no Ezilon usando paginação e extrair resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de URLs válidas encontradas
        """
        return asyncio.run(self._search_ezilon_async(dork))
    
    @retry_operation
    async def _search_ezilon_async(self, dork: str) -> list:
        """
        Versão assíncrona para busca no Ezilon usando paginação e extrair resultados.
        
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
            'User-Agent': UserAgentGenerator.get_random_lib(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://find.ezilon.com/',
        }

        # Configurar parâmetros para o HTTPClient
        kwargs = {
            'headers': headers,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
        
        
        try:
            # Buscar em múltiplas páginas usando o padrão de URL do Ezilon
            for page in range(1, max_pages):
                try:
                    page_urls = await self._search_page_async(headers, encoded_dork, page, kwargs)
                    results.extend(page_urls)
                    
                    # Se não encontrou resultados nesta página, parar
                    if not page_urls:
                        break
                    
                    # Delay entre páginas
                    await asyncio.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                    
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
                    
                    if len(unique_results) >= max_results:
                        break
            
            return unique_results
            
        except Exception as e:
            self.handle_error(e, "Erro ao conectar ao Ezilon")
            raise ValueError(e)

    async def _search_page_async(self, headers: dict, encoded_dork: str, page: int, kwargs: dict) -> list:
        """
        Versão assíncrona para realizar busca em uma página específica do Ezilon.
        
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
            # Página 1: start não especificado
            # Página 2: start=15
            # Página 3: start=30
            # Página 4: start=45
            # Padrão: start = (page - 1) * 15
            start = 0 if page == 1 else (page - 1) * 15
            
            # Escolher uma região aleatória para variar as buscas
            region = random.choice(self.regions)
            
            # Montar URL de busca com base no template adequado
            if page == 1:
                search_url = self.search_url_templates[0].format(DORK=encoded_dork, REGION=region)
            else:
                search_url = self.search_url_templates[1].format(DORK=encoded_dork, START=start, REGION=region)
            
            # Fazer requisição HTTP
            response = await self.request.send_request([search_url], **kwargs)
            
            if not response or isinstance(response[0], Exception):
                return []
                
            response = response[0]
            
            if response.status_code == 200:
                # Extrair URLs do HTML de resposta
                return self._extract_urls_from_response(response.text)
            else:
                return []
            
        except Exception as e:
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
            
            # Buscar elementos específicos da estrutura do Ezilon
            # Padrão de resultado do Ezilon: <div class="web_result">...</div>
            result_containers = soup.select('.web_result, .result_container, .result, .search_result')
            
            for container in result_containers:
                # Tentar extrair URL do título do resultado
                title_link = container.select_one('a.title, a.result_title, h3 a')
                if title_link and 'href' in title_link.attrs:
                    href = title_link.get('href')
                    if href and self._is_external_url(href):
                        urls.append(href)
                
                # Também buscar outros links no container
                other_links = container.select('a[href^="http"]')
                for link in other_links:
                    href = link.get('href')
                    if href and self._is_external_url(href):
                        urls.append(href)
            
            # Se não encontrar com seletores específicos, buscar links gerais
            if not urls:
                general_links = soup.select('a[href^="http"]')
                for link in general_links:
                    href = link.get('href')
                    if href and self._is_external_url(href):
                        urls.append(href)
                        
            # Se ainda não encontrou, usar regex
            if not urls:
                # Padrões regex para capturar URLs
                url_patterns = [
                    r'href=["\']([^"\']*https?://[^"\']+)["\']',
                    r'<a[^>]*href=["\']([^"\']*https?://[^"\']+)["\']'
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
        
        # Remover URLs duplicadas preservando a ordem
        unique_urls = []
        seen = set()
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        return unique_urls

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
        ezilon_domains = ['ezilon.com', 'findezilon.com', 'find.ezilon.com']
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
            'ezilon.com', 'findezilon.com', 'find.ezilon.com',
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
