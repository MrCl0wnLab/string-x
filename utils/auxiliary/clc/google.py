"""
Módulo CLC para dorking usando motor de busca Google.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Google, com técnicas avançadas para evitar detecção de bots.
"""
from core.basemodule import BaseModule
from core.user_agent_generator import UserAgentGenerator
import httpx
import re
from urllib.parse import quote_plus, unquote, urlencode
import time
import random
from bs4 import BeautifulSoup
from core.format import Format
from typing import List, Dict, Optional, Any, Tuple
import backoff
from requests.exceptions import RequestException

class GoogleDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Google.
    
    Esta classe permite realizar buscas avançadas no Google utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Google.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Google Dorking Tool',
            'author': 'MrCl0wn',
            'version': '2.0',
            'description': 'Realiza buscas avançadas com dorks no Google',
            'type': 'collector'
        }

        self.options = {
            'data': str(),                                                                  # Dork para busca
            'delay': 5,                                                                     # Delay entre requisições (segundos)
            'timeout': 30,                                                                  # Timeout para requisições                                                     # Número máximo de resultados
            'debug': False,                                                                 # Modo debug (salva respostas para análise)
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm',  # Exemplo de uso do módulo
            'proxy': str(),                                                                # Proxies para requisições
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
        Executa busca de dorks no Google.
        """
        try:
            dork = Format.clear_value(self.options.get('data').strip())
            
            if not dork:
                self.set_result("⚠️ Dork não fornecido.")
                return

            # Coletando resultados
            results = self._first_search_google(dork)
            if self.pagination:
                for page in self.pagination:
                    if page.startswith("https://"):
                        self.search_url = page
                        results.extend(self._first_search_google(dork))
                        
            if not results:
                self.set_result(f"⚠️ Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.set_result(f"✗ Erro na busca: {str(e)}")
    
    def _first_search_google(self, dork: str) -> List[str]:
        """
        Realiza busca no Google usando diferentes técnicas.
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

        except Exception as e:
            if debug_mode:
                self.set_result(f"⚠️ Erro com {config['host']}: {str(e)}")
        return results
    
    # Gerar um valor aleatório para 'sei' seguindo o padrão observado
    def _generate_sei_value(self) -> str:
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
    
    @backoff.on_exception(
        backoff.expo,
        RequestException,
        max_tries=3,
        max_time=30
    ) 
    def _make_request(self, 
                     url: str, 
                     config: Dict[str, str],
                     debug_mode: bool) -> Optional[str]:
        """
        Executa a requisição com tratamento avançado de resposta.
        """

        debug_mode = True

        # Gerar cookies para simular um navegador real
        cookies = self._generate_cookies(config["host"])

        # Criar headers simulando um navegador real
        headers = {
            'User-Agent': UserAgentGenerator.get_random_lib(),
            'Accept':  "*/*",
            'Referer': f'https://{config["host"]}/',
        }

        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }

        try:
            with httpx.Client(verify=False, **client_kwargs) as client:
                # Faz a requisição
                response = client.get(url, headers=headers, cookies=cookies,)
                return response.text
        except RequestException as e:
            if debug_mode:
                self.set_result(f"⚠️ Erro na requisição para {config['host']}: {str(e)}")
            return None
        
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida.
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
    
    def _decode_url(self, url):
        # Função para decodificar sequências de escape Unicode em URLs
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
        results = []
        if html_content:
            soup = BeautifulSoup(html_content, "html.parser")
            for link_tag in soup.find_all('a', href=True):
                if link := unquote(link_tag["href"].split("&")[0].replace("/url?q=", "")):
                    if link.startswith("http") and self._is_valid_url(link):
                        results.append(self._decode_url(link))
        
        return list(set(results))
    
    def _get_pagination(self, html_content: str, config: dict) -> List[str]:
        """
        Extrai links de navegação da página HTML do Google.
        Args:
            html_content (str): Conteúdo HTML da página do Google.
        Returns:
            List[str]: Lista de URLs de navegação encontradas.
        """
        # Verifica se o conteúdo HTML foi fornecido
        if not html_content:
            return []
        
        results = []
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find all navigation links (anchor tags within navigation elements)
        navigation = soup.find('div', role='navigation')
        if navigation:
            links = navigation.find_all('a', href=True)
            for url in links:
                if url["href"]:
                    results.append(f"https://{config["host"]}/{url["href"]}")
        return results

   