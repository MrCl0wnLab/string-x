"""
Módulo CLC para dorking usando motor de busca Google.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Google, com técnicas avançadas para evitar detecção de bots.
"""
from core.basemodule import BaseModule
import httpx
import re
import zlib
import brotli
from urllib.parse import quote_plus, unquote, urlencode
import time
import random
from bs4 import BeautifulSoup
from core.format import Format
import logging
import json
from typing import List, Dict, Optional, Any, Tuple

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
            'data': str(),              # Dork para busca
            'delay': 5,                 # Delay entre requisições (segundos)
            'timeout': 30,              # Timeout para requisições
            'proxies': str(),           # Lista de proxies (opcional, formato: http://ip:porta,http://ip:porta)
            'max_results': 30,          # Número máximo de resultados
            'debug': False,             # Modo debug (salva respostas para análise)
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm'
        }
        
        # Configurações regionais para evitar recaptcha
        self.country_configs = [
            # pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
            {"host": "www.google.co.il", "hl": "pt-BR", "gl": "br", "country": "Brazil"},
            {"host": "www.google.com", "hl": "sv-SE", "gl": "se", "country": "Sweden"},
            {"host": "www.google.fi", "hl": "fi-FI", "gl": "fi", "country": "Finland"},
           
        ]

        '''
            {"host": "www.google.ca", "hl": "en-CA", "gl": "ca", "country": "Canada"},
            {"host": "www.google.co.nz", "hl": "en-NZ", "gl": "nz", "country": "New Zealand"},
            {"host": "www.google.co.uk", "hl": "en-GB", "gl": "uk", "country": "United Kingdom"},
            {"host": "www.google.ie", "hl": "en-IE", "gl": "ie", "country": "Ireland"},
            {"host": "www.google.com.sg", "hl": "en-SG", "gl": "sg", "country": "Singapore"},
            {"host": "www.google.fi", "hl": "fi-FI", "gl": "fi", "country": "Finland"},
            {"host": "www.google.no", "hl": "no-NO", "gl": "no", "country": "Norway"},
            {"host": "www.google.dk", "hl": "da-DK", "gl": "dk", "country": "Denmark"},
            {"host": "www.google.se", "hl": "sv-SE", "gl": "se", "country": "Sweden"}
        '''
        
        # Navegadores modernos simulados
        self.browser_profiles = [
            {
      
                "name": "Chrome Android",
                "user_agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept_language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                "accept_encoding": "gzip, deflate, br, zstd",
                "sec_ch_ua": '"Not A(Brand";v="99", "Google Chrome";v="112", "Chromium";v="112"',
                "sec_ch_ua_mobile": "?1",
                "sec_ch_ua_platform": '"Android"',
            },
            {
                "name": "Safari iOS",
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept_language": "en-US,en;q=0.9",
                "accept_encoding": "gzip, deflate, br",
                "sec_fetch_dest": "document",
                "sec_fetch_mode": "navigate",
                "sec_fetch_site": "none"
            },
            {
                "name": "Firefox Android",
                "user_agent": "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/111.0 Firefox/111.0",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "accept_language": "en-US,en;q=0.5",
                "accept_encoding": "gzip, deflate, br",
                "sec_fetch_dest": "document",
                "sec_fetch_mode": "navigate",
                "sec_fetch_site": "none",
                "sec_fetch_user": "?1"
            },
        ]
        
    def run(self):
        """
        Executa busca de dorks no Google.
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.set_result("⚠️ Dork não fornecido.")
                return

            # Coletando resultados
            results = self._search_google(dork)
            if not results:
                self.set_result(f"⚠️ Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.set_result(f"✗ Erro na busca: {str(e)}")
    
    def _get_useragent(self) -> str:
        """
        Generates a random user agent string mimicking the format of various software versions.

        The user agent string is composed of:
        - Lynx version: Lynx/x.y.z where x is 2-3, y is 8-9, and z is 0-2
        - libwww version: libwww-FM/x.y where x is 2-3 and y is 13-15
        - SSL-MM version: SSL-MM/x.y where x is 1-2 and y is 3-5
        - OpenSSL version: OpenSSL/x.y.z where x is 1-3, y is 0-4, and z is 0-9

        Returns:
            str: A randomly generated user agent string.
        """
        lynx_version = f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
        libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
        ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
        openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
        return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"

    def _search_google(self, dork: str) -> List[str]:
        """
        Realiza busca no Google usando diferentes técnicas.
        """
        results = []
        proxies = self._parse_proxies(self.options.get('proxies', ''))
        debug_mode = self.options.get('debug', True)
        
        # Codificar a query
        encoded_dork = quote_plus(dork)
        
        # Shuffle para aleatorizar a ordem dos hosts e profiles
        random.shuffle(self.country_configs)
        random.shuffle(self.browser_profiles)
        
        # Tentativas com diferentes configurações
        for config in self.country_configs:
  
            # Selecionar um perfil de navegador aleatório
            browser = random.choice(self.browser_profiles)
            
            # Gerar cookies para simular um navegador real
            cookies = self._generate_cookies(config["host"])
            
            # Criar URL com parâmetros específicos para região
            search_url = self._build_search_url(config, encoded_dork)
            
            # Criar headers simulando um navegador real
            headers = self._build_headers(browser, config["host"])
            
            try:
                client_kwargs = {
                    'timeout': self.options.get('timeout', 30),
                    'follow_redirects': True
                }
                
                # Adicionar proxy se disponível
                if proxies and len(proxies) > 0:
                    proxy = random.choice(proxies)
                    client_kwargs['proxies'] = {
                        'http://': proxy,
                        'https://': proxy
                    }
                
                # Fazer a requisição com tratamento especializado
                html_content = self._make_request(
                    search_url, 
                    headers, 
                    cookies, 
                    client_kwargs,
                    config,
                    debug_mode
                )
                
                
                if html_content:
                    # Extrair URLs dos resultados
                    page_results = self._extract_google_urls(html_content)
                    # Adicionar URLs únicas
                    for url in page_results:
                        results.append(url)
                
                # Tempo de espera variável entre tentativas
                delay = self.options.get('delay', 5)
                wait_time = delay + random.uniform(2.0, 7.0)
                time.sleep(wait_time)
                
            except Exception as e:
                if debug_mode:
                    self.set_result(f"⚠️ Erro com {config['host']}: {str(e)}")
                continue
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
            'num': '100',                       # Número de resultados
            'hl': config['hl'],                 # Localização de idioma
            'gl': config['gl'],                 # Localização geográfica
            'pws': '0',                         # Desativa busca personalizada
            'filter': '0',                      # Mostra todos os resultados (sem filtragem)
            'safe': 'off',                      # Desativa SafeSearch
            'start': '0',                       # Resultados a partir do início,
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
        # search_url = f"https://{host}/search?q={encoded_dork}&num=100&btnG=Search&pws=0&hl=pt-BR&filter=0"
                
        query_string = urlencode(params)

        return f"{base_url}?{query_string}"
    
    def _build_headers(self, browser: Dict[str, str], host: str) -> Dict[str, str]:
        """
        Cria headers HTTP simulando um navegador real.
        """
        headers = {
            'User-Agent': browser['user_agent'],
            'Accept': browser['accept'],
            'Accept-Language': browser['accept_language'],
            'Accept-Encoding': browser['accept_encoding'],
            'Referer': f'https://{host}/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # Adicionar headers específicos de cada navegador
        for key, value in browser.items():
            if key.startswith('sec_'):
                # Converter chave de formato snake_case para formato HTTP real
                header_key = key.replace('_', '-')
                headers[header_key] = value
                
        return headers
    
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
    
    def _make_request(self, 
                     url: str, 
                     headers: Dict[str, str], 
                     cookies: Dict[str, str], 
                     client_kwargs: Dict[str, Any],
                     config: Dict[str, str],
                     debug_mode: bool) -> Optional[str]:
        """
        Executa a requisição com tratamento avançado de resposta.
        """
        debug_mode = True
        try:
            with httpx.Client(verify=False, **client_kwargs) as client:
                # Faz a requisição
                response = client.get(url, headers=headers, cookies=cookies,)
                return response.text
        except Exception as e:
            if debug_mode:
                self.set_result(f"⚠️ Erro na requisição para {config['host']}: {str(e)}")
            return None
    
    def _is_bot_detection_page(self, response) -> bool:
        """
        Verifica se a resposta é uma página de detecção de bots.
        """
        return False
        # Verificar o conteúdo da resposta para sinais de detecção de bot
        content = response.text.lower()
        
        # Termos comuns em páginas de detecção de bot do Google
        bot_indicators = [
            'detected unusual traffic', 
            'captcha', 
            'sourcemappingurl', 
            'our systems have detected', 
            'cloginform', 
            'robot',
            'enablejs',
            'noscript',
            'javascriptenabled',
            'automated query',
            'unusual traffic from your computer',
            'we detected that your computer is sending automated queries',
            '<title>google search</title>'
        ]
        
        # Verificar se algum indicador está presente
        for indicator in bot_indicators:
            if indicator in content:
                return True
                
        # Se o tamanho do documento for muito pequeno, provavelmente é uma página de redirecionamento ou erro
        if len(content) < 1000 and ('redirect' in content or 'javascript' in content):
            return True
            
        return False
    
    def _parse_proxies(self, proxies_str: str) -> List[str]:
        """
        Converte string de proxies em lista.
        """
        if not proxies_str:
            return []
        return [p.strip() for p in proxies_str.split(',') if p.strip()]
        
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida.
        """
        
        block_list = [
            'google.com', 'youtube.com', 'gstatic.com', 'google.com.br',
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
        """for block in block_list:
            if block in url:
                return False"""
            
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
        
        decoded = url
        for escaped, char in unicode_map.items():
            decoded = decoded.replace(escaped, char)
            
        return decoded
    
    def _extract_google_urls(self, html_content: str) -> List[str]:
        results = set()
        pattern = r'"(https?:(?:\\u002f|\/){2}[^"]+?)"'
        raw_matches = re.findall(pattern, html_content)
        
        if not raw_matches:
            return []
        
        for url in raw_matches:
            decoded = self._decode_url(url)
            if self._is_valid_url(decoded):
                results.add(decoded)
        
        return list(results)

   