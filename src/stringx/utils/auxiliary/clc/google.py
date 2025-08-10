"""
Módulo CLC para dorking usando motor de busca Google.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Google, com técnicas avançadas para evitar detecção de bots.

O Google é o maior motor de busca do mundo e oferece operadores avançados
de busca (dorks) que podem ser utilizados para:
- Encontrar informações específicas usando operadores como site:, filetype:, intitle:
- Identificar arquivos sensíveis expostos publicamente
- Descobrir configurações incorretas em servidores e aplicações web
- Localizar páginas de login, painéis administrativos e interfaces de gestão
- Encontrar dados sensíveis que foram indexados acidentalmente
- Mapear a superfície de ataque de um alvo específico

Este módulo implementa diversas técnicas anti-detecção para evitar bloqueios
e captchas durante as pesquisas, como rotação de user agents, delays aleatórios
e múltiplas estratégias de requisição.
"""
# Bibliotecas padrão
import re
import time
import random
import asyncio
from typing import List, Dict, Optional, Any, Tuple
from urllib.parse import quote_plus, unquote, urlencode

# Bibliotecas de terceiros
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException

# Módulos locais
from stringx.core.format import Format
from stringx.core.http_async import HTTPClient
from stringx.core.basemodule import BaseModule
from stringx.core.retry import retry_operation
from stringx.core.user_agent_generator import UserAgentGenerator

class GoogleDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Google.
    
    Esta classe permite realizar buscas avançadas no Google utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    
    Implementa técnicas anti-detecção como rotação de user-agents, cookies
    personalizados, headers variados e configurações regionais aleatórias
    para evitar o bloqueio por captcha durante as buscas intensivas.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Google.
        
        Configura opções padrão, metadados do módulo, cliente HTTP assíncrono
        e estruturas de dados para armazenamento de resultados e paginação.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request  = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Google Dorking Tool',
            'author': 'MrCl0wn',
            'version': '2.0',
            'description': 'Realiza buscas avançadas com dorks no Google',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),                                                                  # Dork para busca
            'delay': 5,                                                                     # Delay entre requisições (segundos)
            'timeout': 30,                                                                  # Timeout para requisições                                                     # Número máximo de resultados
            'debug': False,                                                                 # Modo debug (salva respostas para análise)
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm',  # Exemplo de uso do módulo
            'proxy': str(),
            'retry': None,             # Número de tentativas de requisição
            'retry_delay': None,       # Atraso entre tentativas de requisição
        }

        self.pagination = []  # Contador de páginas para navegação
        self.search_url = str()

        # Configurações regionais para evitar recaptcha
        self.country_configs = [
            # pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
            {"host": "www.google.com.br", "hl": "pt-BR", "gl": "br", "country": "Brazil"},
            {"host": "www.google.com", "hl": "sv-SE", "gl": "se", "country": "Sweden"},
            {"host": "www.google.fi", "hl": "fi-FI", "gl": "fi", "country": "Finland"},
            {"host": "www.google.ca", "hl": "en-CA", "gl": "ca", "country": "Canada"},
            {"host": "www.google.co.nz", "hl": "en-NZ", "gl": "nz", "country": "New Zealand"},
            {"host": "www.google.co.uk", "hl": "en-GB", "gl": "uk", "country": "United Kingdom"},
            {"host": "www.google.ie", "hl": "en-IE", "gl": "ie", "country": "Ireland"},
            {"host": "www.google.com.sg", "hl": "en-SG", "gl": "sg", "country": "Singapore"},
            {"host": "www.google.fi", "hl": "fi-FI", "gl": "fi", "country": "Finland"},
            {"host": "www.google.no", "hl": "no-NO", "gl": "no", "country": "Norway"},
            {"host": "www.google.dk", "hl": "da-DK", "gl": "dk", "country": "Denmark"},
            {"host": "www.google.se", "hl": "sv-SE", "gl": "se", "country": "Sweden"}
         ]
        
        
    def run(self):
        """
        Executa busca de dorks usando Google.
        
        Este método coordena todo o processo de busca, incluindo a 
        verificação da dork fornecida, realização da busca inicial
        e processamento de páginas de resultado adicionais.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
        try:
            dork = Format.clear_value(self.options.get('data').strip())
            
            if not dork:
                self.log_debug("[X] Dork não fornecido.")
                return

            # Coletando resultados
            results = self._first_search_google(dork)
            if self.pagination:
                for page in self.pagination:
                    if page.startswith("https://"):
                        self.search_url = page
                        results.extend(self._first_search_google(dork))
                        
            if not results:
                self.log_debug(f"[!] Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except RequestException as e:
            self.handle_error(e, "Erro requisição Google")
        except ValueError as e:
            self.handle_error(e, "Erro valor Google")
        except Exception as e:
            self.handle_error(e, "Erro Google")
    
    def _first_search_google(self, dork: str) -> List[str]:
        """
        Realiza busca no Google usando diferentes técnicas.
        
        Este método executa a busca principal no Google, utilizando técnicas de 
        rotação de configurações regionais para evitar bloqueios. Processa a
        resposta para extrair URLs e links de paginação.
        
        Args:
            dork (str): Termo de busca (dork) a ser pesquisado
            
        Returns:
            List[str]: Lista de URLs encontrados nos resultados da busca
            
        Raises:
            RequestException: Erro na requisição HTTP
            ValueError: Erro no processamento de valores
        """
        results = []
        debug_mode = self.options.get('debug')

        # Shuffle para aleatorizar a ordem dos hosts e profiles
        random.shuffle(self.country_configs)
        config = self.country_configs[0]
        # Codificar a query
        encoded_dork = quote_plus(dork)

        if self.pagination:
            search_url = self.search_url
        # Criar URL com parâmetros específicos para região
        else:
            search_url = self._build_search_url(config, encoded_dork)

        try:
            # Fazer a requisição com tratamento especializado
            html_content = self._make_request(
                search_url, 
                config,
                debug_mode
            )

            if html_content:
                # Extrair URLs dos resultados
                if len(self.pagination) == 0:
                    self.pagination = self._get_pagination(html_content, config["host"])
                page_results = self._extract_google_urls(html_content)
                # Adicionar URLs únicas
                for url in page_results:
                    results.append(url)
                return results
            return None
        except RequestException as e:
            if debug_mode:
                self.log_debug(f"Erro de requisição com {config['host']}: {str(e)}")
        except ValueError as e:
            if debug_mode:
                self.log_debug(f"Erro de processamento com {config['host']}: {str(e)}")
        except Exception as e:
            if debug_mode:
                self.log_debug(f"Erro com {config['host']}: {str(e)}")
        return None
        
    
    def _generate_sei_value(self) -> str:
        """
        Gera um valor aleatório para o parâmetro 'sei' da URL.
        
        Este método cria um valor para o parâmetro 'sei' seguindo o padrão
        observado nas requisições do Google, ajudando a simular requisições
        legítimas de um navegador para evitar detecção.
        
        Returns:
            str: String aleatória formatada de acordo com o padrão do Google
        """
        # Primeira parte: caracteres aleatórios (geralmente letras maiúsculas e números)
        first_part = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        # Segunda parte: geralmente tem formato fixo (ex: CqaQ)
        middle_parts = ['CqaQ', 'DsRt', 'EpLk', 'FmNs', 'GbVc']
        second_part = random.choice(middle_parts)
        # Terceira parte: geralmente números/letras indicando uma sequência
        num_sequence = random.randint(1, 9)
        # Quarta parte: sequência de letras minúsculas geralmente relacionadas a palavras
        word_parts = ['sQP', 'tRP', 'qAP', 'xZP', 'lMP']
        fourth_part = random.choice(word_parts)
        # Quinta parte: palavras curtas aleatórias
        word_endings = ['xqqFqQc', 'rttGhYu', 'pllJkLm', 'wnnBvCx', 'zmmNbVc']
        fifth_part = random.choice(word_endings)
        
        return f"{first_part}{second_part}{num_sequence}{fourth_part}{fifth_part}"

    def _build_search_url(self, config: Dict[str, str], encoded_dork: str) -> str:
        """
        Cria URL de busca com parâmetros adequados.
        
        Este método constrói uma URL de pesquisa do Google com parâmetros 
        específicos para a região selecionada, incluindo configurações para
        maximizar resultados e minimizar filtros. Também adiciona parâmetros
        aleatórios para variar a assinatura das requisições.
        
        Args:
            config (Dict[str, str]): Configuração regional com host, hl e gl
            encoded_dork (str): Termo de busca já codificado para URL
            
        Returns:
            str: URL completa para realizar a busca
        """
        
        # Parâmetros da URL    
        params = {
            'q': encoded_dork,                  # A consulta de busca
            'num': '1500',                      # Número de resultados
            'hl': config['hl'],                 # Localização de idioma
            'gl': config['gl'],                 # Localização geográfica
            'pws': '1',                         # Desativa busca personalizada
            'filter': '0',                      # Mostra todos os resultados (sem filtragem)
            'safe': 'off',                      # Desativa SafeSearch
            'start': 100,                       # Resultados a partir do início,
            'btnG': 'Search',                   # Botão de busca
            'sei': self._generate_sei_value()   # Valor aleatório para 'sei'
        }
        
        # Adicionar parâmetros adicionais aleatórios para variar assinatura
        if random.choice([True, False]):
            params['ie'] = 'utf-8'
            params['oe'] = 'utf-8'
            
        if random.choice([True, False]):
            params['sourceid'] = 'chrome'
            
        # Construir URL completa
        base_url = f"https://{config['host']}/search"
        # base_url = f"https://www.google.com.br/search?q={encoded_dork}&num=100&btnG=Search&pws=0&hl=pt-BR&filter=0"
                
        query_string = urlencode(params)

        return f"{base_url}?{query_string}"
    
    def _generate_cookies(self, host: str) -> Dict[str, str]:
        """
        Gera cookies para simular navegação legítima.
        
        Este método cria um conjunto de cookies com valores semelhantes aos
        gerados por navegadores reais durante sessões de navegação no Google,
        ajudando a evitar a detecção como bot.
        
        Args:
            host (str): Nome do host para o qual os cookies serão gerados
            
        Returns:
            Dict[str, str]: Dicionário com os cookies necessários para a requisição
        """
        timestamp = int(time.time())
        rand_id = ''.join(random.choices('0123456789abcdef', k=16))
        
        cookies = {
            #'CONSENT': f'YES+cb.{timestamp-random.randint(500,1000)}-04-p0.{timestamp-random.randint(1,400)}',
            'CONSENT': 'PENDING+987', # Bypasses the consent page
            'SOCS': 'CAESHAgBEhIaAB',
            '1P_JAR': time.strftime('%Y-%m-%d', time.localtime()),
            'NID': f'511=eXGAsIsSBk-FJvOUTpiBqxP9uh_JMvazXkVZgfgbcC5CyHrTL{rand_id}mBJcZN9232hH1aQ7bN1mhqudSKmNZi{rand_id}wkzR',
            'AEC': f'AUEFqZc{rand_id}{random.choice(["a", "b", "c", "d"])}{random.randint(10000, 99999)}c',
            'SIDCC': f"AFvIBn{random.randint(10000, 99999)}XsQdVFDb{random.randint(100, 999)}KgPxRCD{random.randint(1000, 9999)}"
        }

        return cookies
    
    @retry_operation
    def _make_request(self, 
                     url: str, 
                     config: Dict[str, str],
                     debug_mode: bool) -> Optional[str]:
        """
        Executa a requisição HTTP com tratamento avançado de resposta.
        
        Este método realiza uma requisição HTTP assíncrona utilizando headers
        e cookies personalizados para simular um navegador real. Implementa
        tratamento de erros e suporte a proxies.
        
        Args:
            url (str): URL completa para fazer a requisição
            config (Dict[str, str]): Configuração regional com host
            debug_mode (bool): Indica se o modo de debug está ativado
            
        Returns:
            Optional[str]: Conteúdo HTML da página ou None em caso de erro
            
        Raises:
            RequestException: Erro relacionado à requisição HTTP
            ValueError: Erro no processamento da resposta
        """
        # Gerar cookies para simular um navegador real
        cookies = self._generate_cookies(config["host"])

        kwargs = {
            'headers' : {
                'User-Agent': UserAgentGenerator.get_random_lib(),
                'Accept':  "*/*",
                'Referer': f'https://{config["host"]}/',
                },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'cookies': cookies
        }

        try:
            async def make_request():
                return await self.request.send_request([url], **kwargs)
            response = asyncio.run(make_request())[0]
            return response.text
        except RequestException as e:
            if debug_mode:
                self.log_debug(f"Erro na requisição para {config['host']}: {str(e)}")
            raise
        except Exception as e:
            if debug_mode:
                self.log_debug(f"Erro inesperado na requisição para {config['host']}: {str(e)}")
            raise ValueError(f"Erro no processamento da requisição: {str(e)}")
        
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida e não pertence à lista de bloqueio.
        
        Este método filtra URLs para remover resultados indesejados como
        páginas do próprio Google, mídias sociais ou sites de busca. 
        Também faz limpeza básica nas URLs recebidas.
        
        Args:
            url (str): URL a ser verificada
            
        Returns:
            bool: True se a URL for válida e não estiver bloqueada, False caso contrário
        """
        
        block_list = [
            'google.com', 'youtube.com', 'gstatic.com', 'www.google.',
            'googleusercontent.com', 'googlesyndication.com', 'googleapis.com',
            'bing.com', 'microsoft.com', 'msn.com', 'yahoo.com', 'ask.com',
            'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com'
        ]

        if not url:
            return False
        
        # Remover aspas do início e fim se existirem
        if (url.startswith('"') and url.endswith('"')) or (url.startswith("'") and url.endswith("'")):
            url = url[1:-1]

        # Verificar se a URL contém domínios bloqueados
        for block in block_list:
            if block in url:
                return False
            
        # Verificar se a URL começa com http e não termina com extensões comuns de arquivos
        if url.startswith('http') and not re.search(r'\.(jpg|jpeg|png|gif|css|js)$', url.lower()):
            return True
            
        return False
    
    def _decode_url(self, url: str) -> str:
        """
        Decodifica sequências de escape Unicode em URLs.
        
        Este método processa a URL para substituir sequências de escape 
        Unicode por seus caracteres correspondentes e também remove
        parâmetros de rastreamento como 'srsltid'.
        
        Args:
            url (str): URL para decodificar
            
        Returns:
            str: URL decodificada sem parâmetros de rastreamento
        """
        unicode_map = {
            r'\u003d': '=', r'\u0026': '&', r'\u002f': '/', 
            r'\u003a': ':', r'\u003f': '?', r'\u003b': ';',
            r'\u002b': '+', r'\u0023': '#', r'\u0025': '%',
            r'\u002c': ',', r'\u003c': '<', r'\u003e': '>'
        }

        if '?srsltid=' in url:
            url = url.split('?srsltid=')[0]  # Remove o parâmetro srsltid

        decoded = url
        for escaped, char in unicode_map.items():
            decoded = decoded.replace(escaped, char)
            decoded = unquote(decoded)
            
        return decoded
    
    def _extract_google_urls(self, html_content: str) -> List[str]:
        """
        Extrai URLs dos resultados de busca do Google.
        
        Este método analisa o HTML da página de resultados do Google para
        extrair os links das páginas nos resultados da busca, removendo
        links internos do Google e decodificando as URLs.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            List[str]: Lista de URLs únicas encontradas nos resultados
        """
        results = []
        if html_content:
            soup = BeautifulSoup(html_content, "html.parser")
            for link_tag in soup.find_all('a', href=True):
                if link := unquote(link_tag["href"].split("&")[0].replace("/url?q=", "")):
                    if link.startswith("http") and self._is_valid_url(link):
                        results.append(self._decode_url(link))
        
        return list(set(results))
    
    def _get_pagination(self, html_content: str, config: Dict[str, str]) -> List[str]:
        """
        Extrai links de navegação da página HTML do Google.
        
        Este método analisa o HTML dos resultados do Google para encontrar
        links de paginação que permitem navegar para as próximas páginas 
        de resultados.
        
        Args:
            html_content (str): Conteúdo HTML da página do Google
            config (Dict[str, str]): Configuração com informações do host
            
        Returns:
            List[str]: Lista de URLs de navegação encontradas
        """
        # Verifica se o conteúdo HTML foi fornecido
        if not html_content:
            return []
        
        results = []
        
        # Analisa o HTML com BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Encontra todos os links de navegação (tags anchor dentro de elementos de navegação)
        navigation = soup.find('div', role='navigation')
        if navigation:
            links = navigation.find_all('a', href=True)
            for url in links:
                if url["href"]:
                    results.append(f"https://{config['host']}/{url['href']}")
        return results

   