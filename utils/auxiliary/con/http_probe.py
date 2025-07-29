"""
Módulo CON para sondagem HTTP.

Este módulo implementa funcionalidade para sondagem HTTP/HTTPS
com análise de headers, redirects e tecnologias.

Permite verificar a disponibilidade de servidores web, coletar
informações sobre as tecnologias utilizadas, analisar headers
de resposta e detectar potenciais vulnerabilidades básicas.
"""
# Bibliotecas padrão
import re
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse

# Bibliotecas de terceiros
import httpx
from httpx import RequestError, ConnectError, TimeoutException

# Módulos locais
from core.basemodule import BaseModule

class HTTPProbe(BaseModule):
    """
    Módulo para sondagem HTTP avançada.
    
    Esta classe implementa funcionalidades para realizar sondagem
    de servidores HTTP/HTTPS, analisando status codes, headers,
    redirecionamentos e tecnologias utilizadas pelo servidor.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'HTTP Probe',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Sondagem HTTP com análise de headers e tecnologias',
            'type': 'connection',
            'example': './strx -l urls.txt -st "echo {STRING}" -module "con:http_probe" -pm'
        }
        
        self.options = {
            'data': str(),  # URL ou host
            'methods': ['GET', 'HEAD'],
            'follow_redirects': True,
            'analyze_tech': True,
            'timeout': 10,
            'user_agent': 'Mozilla/5.0 (compatible; String-X Scanner)',            'proxy': str(),  # Proxies para requisições (opcional)
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição   
        }
    
    def run(self) -> None:
        """
        Executa a sondagem HTTP do host/URL especificado.
        
        Este método coordena todo o processo de sondagem HTTP,
        incluindo a normalização da URL, tentativas em diferentes
        protocolos (HTTPS/HTTP) e análise das respostas obtidas.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
            
        Raises:
            RequestError: Erro na requisição HTTP
            ConnectError: Erro ao conectar ao servidor
            TimeoutException: Timeout durante a conexão
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        target = self.options.get("data", "").strip()
        if not target:
            return
        
        # Normalizar URL
        if not target.startswith(('http://', 'https://')):
            urls = [f"https://{target}", f"http://{target}"]
        else:
            urls = [target]
        
        for url in urls:
            try:
                result = self._probe_url(url)
                if result:
                    self.set_result(result)
                    break  # Para no primeiro sucesso
            except ConnectError as e:
                if self.options.get('debug', False):
                    self.set_result(f"✗ Erro de conexão com {url}: {str(e)}")
                continue
            except TimeoutException as e:
                if self.options.get('debug', False):
                    self.set_result(f"✗ Timeout na conexão com {url}: {str(e)}")
                continue
            except Exception as e:
                if self.options.get('debug', False):
                    self.set_result(f"✗ Erro ao sondar {url}: {str(e)}")
                continue
    
    def _probe_url(self, url: str) -> str:
        """
        Realiza sondagem de uma URL específica.
        
        Este método faz uma requisição HTTP para a URL especificada
        e analisa a resposta, coletando informações sobre headers,
        status code, tecnologias detectadas e título da página.
        
        Args:
            url (str): URL para realizar a sondagem
            
        Returns:
            str: String formatada com as informações coletadas
            
        Raises:
            RequestError: Erro na requisição HTTP
            ConnectError: Erro ao conectar ao servidor
            TimeoutException: Timeout durante a conexão
        """
        headers = {
            'User-Agent': self.options.get('user_agent', 'String-X Scanner')
        }

        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': self.options.get('follow_redirects', True),
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }
        
        try:
            timeout = httpx.Timeout(self.options.get('timeout', 10))
            
            with httpx.Client(
                headers=headers, verify=False, **client_kwargs
            ) as client:
                response = client.get(url)
            
            # Análise básica
            result = f"URL: {url}\n"
            result += f"Status: {response.status_code}\n"
            result += f"Content-Length: {len(response.content)}\n"
            
            # Headers importantes
            important_headers = ['server', 'x-powered-by', 'content-type', 
                               'set-cookie', 'location', 'x-frame-options']
            
            for header in important_headers:
                if header in response.headers:
                    result += f"{header.title()}: {response.headers[header]}\n"
            
            # Análise de tecnologias
            if self.options.get('analyze_tech', True):
                techs = self._detect_technologies(response)
                if techs:
                    result += f"Technologies: {', '.join(techs)}\n"
            
            # Título da página
            title = self._extract_title(response.text)
            if title:
                result += f"Title: {title}\n"
            
            return result
            
        except ConnectError as e:
            raise ConnectError(f"Erro de conexão com {url}: {str(e)}")
        except TimeoutException as e:
            raise TimeoutException(f"Timeout na conexão com {url}: {str(e)}")
        except Exception as e:
            raise RequestError(f"Erro ao sondar {url}: {str(e)}")
    
    def _detect_technologies(self, response) -> List[str]:
        """
        Detecta tecnologias usadas no site.
        
        Este método analisa headers e conteúdo da resposta para
        identificar tecnologias comuns como servidores web,
        linguagens de programação e CMS utilizados.
        
        Args:
            response: Objeto de resposta HTTP do httpx
            
        Returns:
            List[str]: Lista de tecnologias detectadas
        """
        techs = []
        
        # Headers
        server = response.headers.get('server', '').lower()
        if 'apache' in server:
            techs.append('Apache')
        elif 'nginx' in server:
            techs.append('Nginx')
        elif 'iis' in server:
            techs.append('IIS')
        
        powered_by = response.headers.get('x-powered-by', '').lower()
        if 'php' in powered_by:
            techs.append('PHP')
        elif 'asp.net' in powered_by:
            techs.append('ASP.NET')
        
        # Content analysis
        content = response.text.lower()
        if 'wordpress' in content:
            techs.append('WordPress')
        elif 'joomla' in content:
            techs.append('Joomla')
        elif 'drupal' in content:
            techs.append('Drupal')
        
        return techs
    
    def _extract_title(self, html: str) -> str:
        """
        Extrai o título da página HTML.
        
        Este método usa expressões regulares para extrair
        o conteúdo da tag <title> de uma página HTML.
        
        Args:
            html (str): Conteúdo HTML da página
            
        Returns:
            str: Título extraído ou string vazia se não encontrado
        """
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else ''
