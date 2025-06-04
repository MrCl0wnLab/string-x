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
            'extract_urls_only': True,  # True para extrair apenas URLs, False para incluir títulos e descrições
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
                return
            
            
            extract_urls_only = self.options.get('extract_urls_only', True)
            
            # Coletando resultados
            results = self._search_bing(dork)
            
            if not results:
                self.set_result(f"⚠️ Nenhum resultado encontrado para: {dork}")
                return
            
            # Formatando resultados
            if extract_urls_only:
                # Mais eficiente: unir todas as URLs em um único resultado
                urls = [result['url'] for result in results]
                self.set_result("\n".join(urls))
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
        results = []
        unique_urls = set()  # Para evitar duplicidades
        
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
                for idx, template in enumerate(self.search_url_templates):
                    search_url = ""
                    search_url = template.format(DORK=encoded_dork)
                    try:
                        response = client.get(search_url, headers=headers)
                        if response.status_code != 200:
                            continue
                        
                        # Extrair resultados
                        page_results = self._parse_bing_results(response.text)
                        
                        # Filtrar duplicidades
                        for result in page_results:
                            if result['url'] not in unique_urls:
                                unique_urls.add(result['url'])
                                results.append(result)
                        
                        # Respeitar delay entre requisições
                        time.sleep(self.options.get('delay', 2) + random.uniform(0.5, 1.5))
                        
                    except Exception as e:
                        # Continuar para o próximo formato em caso de erro
                        continue

                return results
                
        except Exception as e:
            self.set_result(f"✗ Erro ao conectar ao Bing: {str(e)}")
            return []
    
    def _parse_bing_results(self, html_content: str) -> list:
        """
        Extrai resultados da página de busca do Bing.
        
        Args:
            html_content (str): Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de dicionários com título, URL e descrição
        """
        results = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscando por elementos de resultado do Bing
            search_results = soup.select("li.b_algo")
            
            if not search_results:  # Formato alternativo
                search_results = soup.select("div.b_title, div.b_caption")
            
            for result in search_results:
                try:
                    # Extrair título e URL do link
                    title_element = result.select_one("h2 a") or result.select_one("a")
                    if not title_element:
                        continue
                        
                    title = title_element.get_text(strip=True)
                    url = title_element.get('href', '')
                    
                    # Filtrar URLs inválidas e internas do Bing
                    if not url or url.startswith('/') or 'bing.com' in url:
                        continue
                        
                    # Extrair descrição
                    description_element = result.select_one("p") or result.select_one("div.b_caption p")
                    description = ""
                    if description_element:
                        description = description_element.get_text(strip=True)
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'description': description
                    })
                except Exception:
                    continue
            
            # Método alternativo se não encontrou resultados
            if not results:
                # Buscar links diretamente
                for link in soup.select("a[href^='http']"):
                    url = link.get('href', '')
                    
                    # Filtrar URLs internas do Bing
                    if 'bing.com' in url or 'microsoft.com' in url or not url:
                        continue
                        
                    title = link.get_text(strip=True) or url
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'description': ""
                    })
            
            return results
            
        except Exception as e:
            self.set_result(f"✗ Erro ao analisar resultados: {str(e)}")
            return []