"""
Módulo CLC para coleta usando Google Custom Search Engine (CSE).

Este módulo implementa funcionalidade para realizar buscas usando múltiplas
Custom Search Engines do Google, coletando automaticamente os tokens necessários
e realizando as consultas de forma sequencial.

O Google Custom Search Engine (CSE) é uma API oficial do Google que oferece
benefícios significativos para coleta de dados:
- Acesso programático e legítimo ao índice do Google
- Contorna muitas das limitações de scraping do Google Search
- Permite maior volume de consultas sem bloqueios (dentro das cotas da API)
- Oferece resultados consistentes e estruturados em formato JSON
- Possibilita a personalização dos parâmetros de busca
- Evita captchas e bloqueios temporários comuns ao scraping direto

Este módulo utiliza múltiplas chaves CSE configuradas para:
- Distribuir consultas entre diferentes CSEs
- Evitar atingir limites de quota individual
- Garantir redundância caso uma das chaves seja limitada
- Oferecer resultados mais abrangentes através de diferentes configurações de CSE
"""
import re
import random
import asyncio
import backoff
import urllib.parse
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException

from config import setting
from core.http_async import HTTPClient
from core.basemodule import BaseModule
from core.retry import retry_operation
from core.user_agent_generator import UserAgentGenerator

class GoogleCSEDorker(BaseModule):
    """
    Módulo para coleta usando Google Custom Search Engine.
    
    Esta classe permite realizar buscas usando múltiplas CSE IDs do Google,
    coletando automaticamente os tokens necessários e realizando as consultas
    para identificar informações específicas usando dorks.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Google CSE.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo - informações sobre versão, autor e descrição
        self.meta = {
            'name': 'Google CSE Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas usando Google Custom Search Engine',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:googlecse" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 3,     # Delay entre requisições (segundos)
            'timeout': 20,  # Timeout para requisições
            'max_pages': 15,  # Número máximo de resultados por CSE            'proxy': str(),  # Proxies para requisições
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': 1,        # Atraso entre tentativas de requisição
            'debug': False,  # Modo de debug para mostrar informações detalhadas
        }
        
        # Lista de CSE IDs do Google - cada ID representa um mecanismo de busca customizado
        # Estes IDs são utilizados para diversificar as buscas e evitar rate limiting
        self.cse_ids = setting.GOOGLE_CSE_ID_LIST
    
    def run(self):
        """
        Executa busca de dorks usando Google CSE.
        Método principal que coordena todo o processo de busca.
        """

        # Obtém o dork da configuração e prepara para uso na URL
        dork = self.options.get('data').strip()
        dork = urllib.parse.quote_plus(dork)  # URL encoding para caracteres especiais

        # Validação de entrada - verifica se o dork foi fornecido
        if not dork:
            self.set_result("⚠️ Dork não fornecido.")
            return

        # Tenta obter informações de configuração de um CSE aleatório
        # Loop através dos CSE IDs até encontrar um que funcione
        for _ in self.cse_ids:
            cse_id = random.choice(self.cse_ids)  # Seleção aleatória para distribuir carga
            if info_js := self._get_info_from_cse(cse_id):
                break
        if not info_js:
            return

        # Executa a busca propriamente dita com o CSE selecionado
        if results := self._search(dork, cse_id, info_js):
            self.set_result("\n".join(results))
   
    def _search(self, dork: str, cse_id: str, info_js: dict) -> list:
        """
        Wrapper síncrono para realizar a busca e retornar os resultados.
        
        Args:
            dork: Query de busca (já codificada para URL)
            cse_id: ID do Custom Search Engine
            info_js: Dicionário com tokens necessários para autenticação
            
        Returns:
            list: Lista de URLs encontradas
        """
        return asyncio.run(self._search_async(dork, cse_id, info_js))
            
    async def _search_async(self, dork: str, cse_id: str, info_js: dict) -> list:
        """
        Versão assíncrona para realizar a busca e retornar os resultados.
        
        Args:
            dork: Query de busca (já codificada para URL)
            cse_id: ID do Custom Search Engine
            info_js: Dicionário com tokens necessários para autenticação
            
        Returns:
            list: Lista de URLs encontradas
        """
        results = []
        max_pages = int(self.options.get('max_pages', 5))

        try:
            # Itera através das páginas de resultados
            for num_page in range(1, max_pages):
                # Constrói URL da API do Google CSE com todos os parâmetros necessários
                # A URL simula uma requisição do frontend do Google CSE
                page_count = num_page * 10  # Converte para contador do Google
                url_request = f"https://cse.google.com/cse/element/v1?rsz=filtered_cse&num={page_count}&hl=en&source=gcsc&start={page_count}&cselibv={info_js['cse_lib_version']}&cx={cse_id}&q={dork}&safe=off&rurl=https://cse.google.com/cse?cx={cse_id}&q={dork}&num=500&hl=en&as_qdr=all&start={num_page}&sa=N&cse_tok={info_js['cse_token']}&exp=cc,apo&callback=google.search.cse.api5630"
                html_content = await self._make_request_async(url_request)
                
                # Processa a resposta se obtida com sucesso
                if html_content:
                    # Extrai URLs dos resultados da busca
                    if url_info_js_result := self._extract_urls_from_html(html_content):
                        results.extend(url_info_js_result)

                # Implementa delay para evitar rate limiting
                await asyncio.sleep(self.options.get('delay', 3))
        
        except Exception as e:
            return []
        return results
    
    def _get_info_from_cse(self, cse_id: str) -> dict:
        """
        Wrapper síncrono para obter informações de configuração do Google CSE.
        
        Args:
            cse_id (str): ID do CSE
            
        Returns:
            dict: Dicionário com tokens de configuração
        """
        return asyncio.run(self._get_info_from_cse_async(cse_id))
    
    async def _get_info_from_cse_async(self, cse_id: str) -> dict:
        """
        Versão assíncrona para obter informações de configuração do Google CSE.
        
        Faz requisição ao arquivo JavaScript de configuração do CSE
        e extrai tokens necessários para autenticação nas buscas.
        
        Args:
            cse_id (str): ID do CSE
            
        Returns:
            dict: Dicionário com tokens de configuração
        """
        # URL do arquivo de configuração JavaScript do CSE
        config_url = f"https://cse.google.com/cse/cse.js?cx={cse_id}"
        response = await self._make_request_async(config_url)

        if not response:
            return {}

        # Usa regex para extrair tokens de configuração do JavaScript
        # cse_token: Token de autenticação necessário para fazer buscas
        tokens = re.findall(r'"cse_token":\s*"([^"]+)"', response)
        # cselibVersion: Versão da biblioteca CSE necessária para compatibilidade
        cse_lib_version = re.findall(r'"cselibVersion":\s*"([^"]+)"', response)
        if not tokens and not cse_lib_version:
            return {}
        
        return {'cse_token': tokens[0],'cse_lib_version': cse_lib_version[0]}
    
    def _extract_urls_from_html(self, html_content: str) -> list:
        """
        Extrai URLs da resposta HTML do Google CSE.
        
        Analisa o conteúdo HTML retornado pela API do CSE e extrai
        URLs válidas dos resultados de busca usando expressões regulares.
        
        Args:
            html_content (str): Conteúdo HTML da resposta
            
        Returns:
            list: Lista de URLs válidas extraídas
        """
        results = []
        try:
            # Padrões regex para capturar URLs em diferentes formatos no JSON/HTML do CSE
            # "url": captura URLs diretas dos resultados
            # "creatorProductor": captura URLs de criadores/produtores de conteúdo
            url_patterns = [
                r'"url":\s*"([^"]+)"',
                r'"creatorProductor":\s*"([^"]+)"'
            ]

            # Aplica cada padrão de regex ao conteúdo
            for pattern in url_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    for url in matches:
                        # Valida cada URL encontrada antes de adicionar aos resultados
                        if self._is_valid_url(url.strip()):
                            results.append(urllib.parse.unquote((url.strip())))
            return list(set(results))  # Remove duplicatas
            
        except Exception:
            return results
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida e não é interna do Google.
        
        Aplica filtros para garantir que apenas URLs úteis sejam retornadas,
        excluindo URLs internas do Google e outros recursos não relevantes.
        
        Args:
            url (str): URL para validar
            
        Returns:
            bool: True se a URL for válida
        """
        # Validações básicas de entrada
        if not url or not isinstance(url, str):
            return False
        
        # Verifica se é uma URL válida (deve começar com http:// ou https://)
        if not re.match(r'^https?://', url):
            return False
        
        # Lista de padrões para filtrar URLs não desejadas
        # Exclui URLs internas do Google, CDNs e recursos não úteis
        excluded_patterns = [
            r'www\.google\.com',        # Google search pages
            r'cse\.google\.com',        # CSE internal pages
            r'accounts\.google\.com',   # Google accounts
            r'support\.google\.com',    # Google support
            r'gstatic\.com',           # Google static content
            r'favicon\.ico$',          # Favicon files
            r'fonts\.googleapis\.com'   # Google fonts
        ]
        
        # Converte URL para lowercase para comparação case-insensitive
        url_lower = url.lower()
        for pattern in excluded_patterns:
            if re.search(pattern, url_lower):
                return False
        
        # Filtrar URLs muito curtas (provavelmente inválidas ou incompletas)
        if len(url) < 15:
            return False
        
        return True
    
    
    def _make_request(self, url: str) -> str:
        """
        Wrapper síncrono para fazer uma requisição HTTP para a URL especificada.
        
        Args:
            url (str): URL para fazer a requisição
            
        Returns:
            str: Conteúdo da resposta ou string vazia em caso de erro
        """
        return asyncio.run(self._make_request_async(url))
    
    @retry_operation
    async def _make_request_async(self, url: str) -> str:
        """
        Versão assíncrona para fazer uma requisição HTTP para a URL especificada.
        
        Utiliza HTTPClient para fazer requisições HTTP com headers apropriados
        para simular um navegador real e evitar bloqueios.
        
        Args:
            url (str): URL para fazer a requisição
            
        Returns:
            str: Conteúdo da resposta ou string vazia em caso de erro
        """

        kwargs = {
            'headers' : {
                    'User-Agent': UserAgentGenerator.get_random_lib(),  # User agent aleatório gerado dinamicamente
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://cse.google.com/cse',  # Referer do Google CSE
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0',
                    'Accept-Encoding': 'gzip, deflate, br, zstd'
                },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),  # Timeout de 10 segundos,
            'follow_redirects': True,
        }


        try:
            # Fazer requisição assíncrona
            response = await self.request.send_request([url], **kwargs)
            
            if not response or isinstance(response[0], Exception):
                self.set_result(f"⚠️ Erro ao acessar {url}: {str(response[0]) if response else 'Sem resposta'}")
                return ""
                
            response = response[0]
            
            if response.status_code == 200:
                return response.text
            else:
                self.set_result(f"⚠️ Erro ao acessar {url}: {response.status_code}")
                return ""
        except Exception as e:
            self.set_result(f"⚠️ Erro de requisição: {e}")
            raise ValueError(e)
