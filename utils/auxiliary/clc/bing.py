"""
Módulo CLC para dorking usando motor de busca Bing.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Bing, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.
"""
from core.basemodule import BaseModule
import httpx
import re
from urllib.parse import quote_plus
import time
import random
from bs4 import BeautifulSoup
from core.format import Format
from urllib.parse import urljoin, urlparse

class BingDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Bing.
    
    Esta classe permite realizar buscas avançadas no Bing utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Bing.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Bing Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Bing',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm'
        }
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        ]
        
        self.search_url_templates = [
            "https://www.bing.com/search?q={DORK}&form=DEEPSH&shm=cr&shajax=2",
            "https://www.bing.com/search?q={DORK}&shm=cr&form=DEEPSH&shajax=1",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=1&FORM=PERE",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=11&FORM=PERE",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=21&FORM=PERE",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=31&FORM=PERE",

        ]
    
    def run(self):
        """
        Executa busca de dorks no Bing.
        
        Realiza uma busca no motor de busca Bing usando o dork especificado
        e extrai os resultados, apresentando apenas URLs por padrão ou detalhes completos.
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.set_result("⚠️ Dork não fornecido.")
                return

            # Coletando resultados
            results = self._search_bing(dork)
            
            if not results:
                self.set_result(f"⚠️ Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except Exception as e:
            self.set_result(f"✗ Erro na busca: {str(e)}")
    
    def _search_bing(self, dork: str) -> list:
        """
        Realiza busca no Bing usando diferentes URLs e extrai resultados.
        
        Args:
            dork (str): Query de busca (dork)
            
        Returns:
            list: Lista de dicionários com os resultados (título, URL, descrição)
        """
   
        # Lista para armazenar resultados
        results = []
        
        # Codificar a query
        encoded_dork = quote_plus(dork)
        
        # User-agent aleatório
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.bing.com/',
            'DNT': '1'
        }
        
        try:
            with httpx.Client(timeout=self.options.get('timeout', 15)) as client:
                # Estratégia 1: URL padrão com paginação

                # Usar os três templates de URL
                for _, template in enumerate(self.search_url_templates):
                    search_url = ""
                    search_url = template.format(DORK=encoded_dork)
                    try:
                        response = client.get(search_url, headers=headers)
                        if response.status_code != 200:
                            continue
                        
                        # Extrair resultados
                        page_results = set(self._parse_bing_results(response.text))
                        
                        # Filtrar duplicidades
                        for url in page_results:
                            if url:
                                results.append(url)
                        
                        # Respeitar delay entre requisições
                        time.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                        
                    except Exception as e:
                        # Continuar para o próximo formato em caso de erro
                        continue

                return results
                
        except Exception as e:
            self.set_result(f"✗ Erro ao conectar ao Bing: {str(e)}")
            return []
        
    def _is_valid_url(self,url):
        """Verifica se uma URL é válida"""
        block_list = [
            'bing.com', 'microsoft.com', 'msn.com', 'live.com', 'outlook.com',
            'hotmail.com', 'office.com', 'skype.com', 'xbox.com', 'windows.com',
            'microsoftonline.com', 'azurewebsites.net', 'uol.com.br','play.google.com'
        ]

        if not url:
            return False

        for block in block_list:
            if block in url:
                return False
        
        if url.startswith(('http://', 'https://', 'www.')):
            return True
        return False

    def _normalize_url(self, url, base_url=None):
        """Normaliza a URL e converte relativas para absolutas se houver base_url"""
        url = url.strip()

        if ' › ' in url:
            # Remover partes desnecessárias da URL
            url = url.replace(' › ','/')
        if ('...' in url ) or ('…' in url):
            url = url.replace('...','').replace('…','')

        # Remover aspas do início e fim se existirem
        if (url.startswith('"') and url.endswith('"')) or (url.startswith("'") and url.endswith("'")):
            url = url[1:-1]
        
        # Converter URL relativa para absoluta se houver base_url
        if base_url and not bool(urlparse(url).netloc):
            return urljoin(base_url, url)
        
        return url
    
    def _extract_urls_from_html(self, html_content, base_url=None):
        """Extrai URLs de um conteúdo HTML"""
        urls = set()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Extrair URLs de elementos com atributos comuns de URL
        url_attributes = {
            'a': 'href',
            'script': 'src',
            'link': 'href',
            'iframe': 'src',
            'source': 'src',
            'video': 'src',
            'audio': 'src',
            'embed': 'src',
            'form': 'action',
        }

        # 2. Extrair URLs de qualquer elemento com atributos que podem conter URLs
        potential_url_attrs = [
            'href', 'src', 'data-src', 'data-href', 'data-url', 'poster', 
            'background', 'data-original', 'content', 'data-sbihi-src', 
            'data-bm', 'data-orighref', 'hover-url'
        ]

        for tag_name, attrs in url_attributes.items():
            if isinstance(attrs, str):
                attrs = [attrs]
            for attr in attrs:
                for tag in soup.find_all(tag_name, attrs={attr: True}):
                    url = tag[attr]
                    if self._is_valid_url(url):
                        urls.add(self._normalize_url(url, base_url))

        for attr in potential_url_attrs:
            for tag in soup.find_all(attrs={attr: True}):
                url = tag[attr]
                if self._is_valid_url(url):
                    urls.add(self._normalize_url(url, base_url))
        
        # 7. Extrair URLs de texto comum
        for text in soup.stripped_strings:
            url_matches = re.findall(r'http[s]?://[^\s\'"<>()]+', text)
            for url in url_matches:
                if self._is_valid_url(url):
                    urls.add(self._normalize_url(url, base_url))
        
        # 8. Extrair URLs de tags <cite>
        for cite_tag in soup.find_all('cite'):
            if cite_tag.string:
                url_text = cite_tag.get_text(strip=True)
                # Verificar se o texto parece uma URL
                if self._is_valid_url(url_text):
                    urls.add(self._normalize_url(url_text, base_url))
                        
        # Extrair URLs de hover-url=
        cite_urls = re.findall(r'hover-url="([^"]*)"', html_content)
        for url in cite_urls:
            if self._is_valid_url(url):
                urls.add(self._normalize_url(url, base_url))
    
        return urls

    def _parse_bing_results(self, html_content: str) -> list:
        """
        Extrai resultados da página de busca do Bing usando expressões regulares.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de dicionários com título, URL e descrição
        """
        html_content = html_content.replace('<strong>', '').replace('</strong>', '')
        html_content = re.sub(r'<strong>|</strong>',"",html_content)
       
        results = []
        
        try:
            # Definir uma URL base para converter URLs relativas em absolutas
            base_url = "https://www.bing.com"
            # Coletar URLs do HTML
            results = self._extract_urls_from_html(html_content, base_url)
            return results
                
        except Exception as e:
            self.set_result(f"✗ Erro ao analisar resultados: {str(e)}")
            return []