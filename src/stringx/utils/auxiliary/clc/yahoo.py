"""
Módulo CLC para dorking usando motor de busca Yahoo.

Este módulo implementa funcionalidade para realizar buscas avançadas (dorking)
no motor de busca Yahoo, permitindo a extração de resultados usando diferentes
tipos de dorks de busca.

O Yahoo Search, embora tenha perdido participação de mercado para o Google,
ainda oferece vantagens significativas para OSINT:
- Algoritmo de indexação e classificação diferente dos concorrentes
- Menor probabilidade de bloqueio para ferramentas de scraping
- Indexação de conteúdos que podem estar ausentes em outros buscadores
- Operadores de busca avançada com comportamentos distintos
- Resultados potencialmente diferentes para as mesmas consultas
- Menor implementação de filtros de personalização

A diversificação de fontes de busca é fundamental para investigações OSINT
abrangentes, e o Yahoo pode revelar informações que não seriam encontradas
utilizando apenas um motor de busca principal como o Google.
"""
# Bibliotecas padrão
import re
import time
import random
import asyncio
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urljoin, urlparse, unquote, quote_plus

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

class YahooDorker(BaseModule):
    """
    Módulo para dorking usando motor de busca Yahoo.
    
    Esta classe permite realizar buscas avançadas no Yahoo utilizando dorks
    para identificar informações específicas, como arquivos sensíveis,
    diretórios expostos e vulnerabilidades potenciais.
    """
    
    def __init__(self) -> None:
        """
        Inicializa o módulo de dorking Yahoo.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Yahoo Dorking Tool',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Realiza buscas avançadas com dorks no Yahoo',
            'type': 'collector'
        ,
            'example': './strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Dork para busca
            'delay': 2,     # Delay entre requisições (segundos)
            'timeout': 15,  # Timeout para requisições
            'proxy': str(),  # Proxies para requisições (opcional)
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 3,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição   
        }
        
        self.search_url_templates = [
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=1&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=8&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=15&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://search.yahoo.com/search?fr2=piv-web&p={DORK}&b=22&pz=7&bct=0&xargs=0&ei=UTF-8",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}fr=goodsearch-yhsif&b=1&pz=10&bct=0&xargs=0",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}&fr=goodsearch-yhsif&b=11&pz=10&bct=0&xargs=0",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}&fr=goodsearch-yhsif&b=21&pz=10&bct=0&xargs=0",
            "https://us.yhs4.search.yahoo.com/yhs/search?p={DORK}&fr=goodsearch-yhsif&b=31&pz=10&bct=0&xargs=0",
        ]
    

    
    def run(self) -> None:
        """
        Executa busca de dorks no Yahoo.
        
        Esta função realiza uma busca no motor de busca Yahoo usando o dork 
        especificado e extrai os resultados, apresentando as URLs encontradas.
        
        Returns:
            None: Os resultados são armazenados através do método set_result
            
        Raises:
            ValueError: Se o dork for inválido ou a busca falhar
            RequestException: Se ocorrer erro na comunicação HTTP
            ConnectionError: Se não for possível estabelecer conexão
            Timeout: Se a requisição exceder o tempo limite
        """
        try:
            dork = Format.clear_value(self.options.get('data', '').strip())
            
            # Validar o dork
            if not dork:
                self.log_debug("Dork não fornecido")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            
            self.log_debug(f"Iniciando busca para dork: {dork}")
            
            # Coletando resultados
            results = self._search(dork)
            
            if not results:
                self.log_debug("Nenhum resultado encontrado")
                return

            self.log_debug(f"Encontrados {len(results)} resultados")
            self.set_result("\n".join(results))
            
        except ValueError as e:
            self.handle_error(e, "Erro validação Yahoo")
        except RequestException as e:
            self.handle_error(e, "Erro requisição Yahoo")
        except ConnectError as e:
            self.handle_error(e, "Erro conexão Yahoo")
        except (ReadTimeout, ConnectTimeout, TimeoutException) as e:
            self.handle_error(e, "Timeout Yahoo")
        except Exception as e:
            self.handle_error(e, "Erro Yahoo")
    
    @retry_operation
    def _search(self, dork: str) -> List[str]:
        """
        Realiza busca no Yahoo usando diferentes URLs e extrai resultados.
        
        Args:
            dork: Query de busca (dork)
            
        Returns:
            Lista de URLs encontradas nos resultados
            
        Raises:
            ValueError: Se o dork for inválido ou a busca falhar
            RequestException: Se ocorrer erro na comunicação HTTP
            ConnectError: Se não for possível estabelecer conexão
            ReadTimeout, ConnectTimeout, TimeoutException: Se a requisição exceder o tempo limite
        """
   
        # Lista para armazenar resultados
        results = []
        
        # Codificar a query
        encoded_dork = quote_plus(dork)
        self.log_debug(f"Dork codificado: {encoded_dork}")
        
        # Configurar parâmetros para HTTPClient
        proxy = self.options.get('proxy') if self.options.get('proxy') else None
        kwargs = {
            'headers': {
                'User-Agent': UserAgentGenerator.get_random_lib(),
                'Accept': 'text/html,application/xhtml+xml,application/xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://br.search.yahoo.com',
                'DNT': '1'
            },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
        
        try:
            # Usar o método assíncrono do HTTPClient
            for idx, template in enumerate(self.search_url_templates):
                search_url = template.format(DORK=encoded_dork)
                self.log_debug(f"Consultando URL #{idx+1}: {search_url}")
                
                try:
                    # Executar requisição assíncrona
                    async def make_request():
                        return await self.request.send_request([search_url], **kwargs)
                    response = asyncio.run(make_request())[0]
                    
                    if response.status_code != 200:
                        self.log_debug(f"Status não-OK: {response.status_code}")
                        continue
                    
                    # Extrair resultados
                    page_results = set(self._extract_urls(response.text))
                    self.log_debug(f"Extraídos {len(page_results)} URLs desta página")
                    
                    # Filtrar duplicidades
                    for url in page_results:
                        if url and url not in results:
                            results.append(url)
                    
                    # Respeitar delay entre requisições
                    delay = self.options.get('delay', 2) + random.uniform(0.5, 1.5)
                    self.log_debug(f"Aguardando {delay:.2f}s antes da próxima requisição")
                    time.sleep(delay)
                    
                except RequestException as e:
                    self.log_debug(f"Erro de requisição na URL #{idx+1}: {str(e)}")
                    continue
                except Exception as e:
                    self.log_debug(f"Erro ao processar URL #{idx+1}: {str(e)}")
                    continue
            
            return sorted(list(set(results)))  # Garantir que não haja duplicatas
                
        except ConnectError as e:
            self.log_debug(f"Erro de conexão: {str(e)}")
            raise
        except (ReadTimeout, ConnectTimeout, TimeoutException) as e:
            self.log_debug(f"Timeout: {str(e)}")
            raise
        except Exception as e:
            self.log_debug(f"Erro inesperado: {type(e).__name__}: {str(e)}")
            raise ValueError(f"Falha ao realizar busca: {str(e)}")
        
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica se uma URL é válida e não pertence à lista de bloqueio.
        
        Args:
            url: URL a ser validada
            
        Returns:
            True se a URL for válida e não bloqueada, False caso contrário
        """
        block_list = [
            'bing.com', 'microsoft.com', 'msn.com', 'live.com', 'outlook.com',
            'hotmail.com', 'office.com', 'skype.com', 'xbox.com', 'windows.com',
            'microsoftonline.com', 'azurewebsites.net', 'uol.com.br', 'play.google.com',
            'yahoo.com'
        ]

        if not url:
            return False

        for block in block_list:
            if block in url:
                return False
            
        if url.startswith('http'):
            return True
        return False

    def _extract_urls(self, html_content: str) -> List[str]:
        """
        Extrai URLs dos resultados de busca do Yahoo usando regex.
        
        Args:
            html_content: Conteúdo HTML da página de resultados
            
        Returns:
            Lista de URLs extraídas e decodificadas
        """
        results = []
        # Regex para capturar URLs entre R*= e /R*=
        pattern = r'\/R[A-Za-z0-9]+=([http][^\/]+)\/R[A-Za-z0-9]+='
        
        # Encontrar todas as correspondências
        matches = re.findall(pattern, html_content)
        self.log_debug(f"Encontradas {len(matches)} URLs no padrão")
        
        # Decodificar as URLs encontradas (converter %3a para :, %2f para /, etc)
        for url in matches:
            if self._is_valid_url(url):
                decoded_url = unquote(url)
                results.append(decoded_url)
                
        return results


