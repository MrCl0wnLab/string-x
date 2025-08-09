"""
Módulo CLC para dorking usando motor de busca Bing.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Bing, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.

O Bing é um motor de busca da Microsoft que permite o uso de operadores especiais
para refinar as buscas, permitindo encontrar:
- Informações específicas em domínios particulares usando site:
- Documentos de certos tipos usando filetype:
- Páginas com termos específicos em seus títulos usando intitle:
- Conteúdo em diferentes idiomas e regiões
"""
# Bibliotecas padrão
import re
import time
import random
import asyncio
from typing import List, Dict, Any, Optional, Union, Set, Tuple
from urllib.parse import urljoin, urlparse, quote_plus

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

class BingDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Bing.
    
    Esta classe permite realizar buscas avançadas no Bing utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    
    Implementa métodos para contornar limitações do Bing, como detecção de bots,
    através de rotação de headers, simulação de navegação e múltiplas estratégias
    de requisição.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de dorking Bing.
        
        Configura opções padrão, metadados do módulo, cliente HTTP assíncrono
        e templates de URLs para pesquisas no motor Bing.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Bing Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Bing',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),          # Dork para busca
            'delay': 2,             # Delay entre requisições (segundos)
            'timeout': 15,          # Timeout para requisições
            'proxy': str(),         # Proxies para requisições (opcional)
            'debug': False,         # Modo de debug para mostrar informações detalhadas
            'retry': 3,             # Número de tentativas de requisição
            'retry_delay': None,       # Atraso entre tentativas de requisição
        }
        
        self.search_url_templates = [
            "https://www.bing.com/search?q={DORK}&form=DEEPSH&shm=cr&shajax=2",
            "https://www.bing.com/search?q={DORK}&shm=cr&form=DEEPSH&shajax=1",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=1&FORM=PERE",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=11&FORM=PERE",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=21&FORM=PERE",
            "https://www.bing.com/search?q={DORK}&filt=rf&first=31&FORM=PERE",

        ]
    
    def run(self) -> None:
        """
        Executa busca de dorks no Bing.
        
        Este método coordena todo o processo de busca no Bing, incluindo
        a validação da dork fornecida, execução da busca e processamento
        dos resultados obtidos.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
            
        Raises:
            RequestException: Erro na requisição HTTP
            ValueError: Erro na validação dos parâmetros
            ConnectionError: Erro de conexão durante a busca
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            if not dork:
                self.log_debug("Dork não fornecido.")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()
                

            # Coletando resultados
            results = self._search_bing(dork)
            
            if not results:
                self.log_debug(f"Nenhum resultado encontrado para: {dork}")
                return

            self.set_result("\n".join(results))
        except RequestException as e:
            self.handle_error(e, "Erro requisição Bing")
        except ConnectError as e:
            self.handle_error(e, "Erro conexão Bing")
        except (ReadTimeout, ConnectTimeout, TimeoutException) as e:
            self.handle_error(e, "Timeout Bing")
        except ValueError as e:
            self.handle_error(e, "Erro validação Bing")
        except Exception as e:
            self.handle_error(e, "Erro Bing")


    @retry_operation
    def _search_bing(self, dork: str) -> List[str]:
        """
        Realiza busca no Bing usando diferentes URLs e extrai resultados.
        
        Este método executa a busca principal no Bing, utilizando diferentes
        templates de URL para maximizar a coleta de resultados. Processa as
        respostas HTML para extrair URLs relevantes.
        
        Args:
            dork (str): Query de busca (dork) a ser pesquisada
            
        Returns:
            List[str]: Lista de URLs encontrados nos resultados da busca
            
        Raises:
            RequestException: Erro na requisição HTTP
            ConnectionError: Erro de conexão durante a busca
            ValueError: Erro no processamento da resposta
        """
   
        # Lista para armazenar resultados
        results = []
        # Codificar a query
        encoded_dork = quote_plus(dork)
        
        kwargs = {
            'headers' : {
                'User-Agent': UserAgentGenerator.get_desktop_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.bing.com/',
                'DNT': '1'
                },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),  # Timeout de 10 segundos,
        }

        
        
        try:
            # Usar os três templates de URL
            for _, template in enumerate(self.search_url_templates):
                url = ""
                url = template.format(DORK=encoded_dork)
                try:
                    async def make_request():
                        return await self.request .send_request([url], **kwargs)
                    response = asyncio.run(make_request())[0]
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
                    self.handle_error(e, "Erro ao processar resultados do Bing")
                    # Continuar para o próximo formato em caso de erro
                    continue
            return results
                
        except RequestException as e:
            self.log_debug(f"Erro ao conectar ao Bing: {str(e)}")
            raise # Re-raise the original exception
        
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida e não pertence à lista de bloqueio.
        
        Este método filtra URLs para remover resultados indesejados como
        páginas do próprio Bing, da Microsoft ou outros sites não relevantes.
        
        Args:
            url (str): URL a ser verificada
            
        Returns:
            bool: True se a URL for válida e não estiver bloqueada, False caso contrário
        """
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

    def _normalize_url(self, url: str, base_url: Optional[str] = None) -> str:
        """
        Normaliza a URL e converte relativas para absolutas se houver base_url.
        
        Este método limpa e padroniza URLs, removendo caracteres especiais, 
        convertendo URLs relativas para absolutas quando uma base é fornecida,
        e tratando formatos específicos dos resultados do Bing.
        
        Args:
            url (str): URL a ser normalizada
            base_url (Optional[str]): URL base para converter URLs relativas em absolutas
            
        Returns:
            str: URL normalizada
        """
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
    
    def _extract_urls_from_html(self, html_content: str, base_url: Optional[str] = None) -> List[str]:
        """
        Extrai URLs de um conteúdo HTML.
        
        Este método utiliza o BeautifulSoup para analisar o HTML e extrair URLs
        de diferentes elementos como links, scripts, iframes, etc. Também processa
        elementos específicos do formato de resultados do Bing.
        
        Args:
            html_content (str): Conteúdo HTML para análise
            base_url (Optional[str]): URL base para normalizar URLs relativas
            
        Returns:
            List[str]: Lista de URLs extraídas do HTML
        """
        urls = []
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
                        urls.append(self._normalize_url(url, base_url))

        for attr in potential_url_attrs:
            for tag in soup.find_all(attrs={attr: True}):
                url = tag[attr]
                if self._is_valid_url(url):
                    urls.append(self._normalize_url(url, base_url))
        
        # 7. Extrair URLs de texto comum
        for text in soup.stripped_strings:
            url_matches = re.findall(r'http[s]?://[^\s\'"<>()]+', text)
            for url in url_matches:
                if self._is_valid_url(url):
                    urls.append(self._normalize_url(url, base_url))
        
        # 8. Extrair URLs de tags <cite>
        for cite_tag in soup.find_all('cite'):
            if cite_tag.string:
                url_text = cite_tag.get_text(strip=True)
                # Verificar se o texto parece uma URL
                if self._is_valid_url(url_text):
                    urls.append(self._normalize_url(url_text, base_url))
                        
        # Extrair URLs de hover-url=
        cite_urls = re.findall(r'hover-url="([^"]*)"', html_content)
        for url in cite_urls:
            if self._is_valid_url(url):
                urls.append(self._normalize_url(url, base_url))
    
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
            self.handle_error(e, "Erro ao analisar resultados do Bing")
            return []