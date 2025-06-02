"""
Módulo CON para sondagem HTTP.

Este módulo implementa funcionalidade para sondagem HTTP/HTTPS
com análise de headers, redirects e tecnologias.
"""
from core.basemodule import BaseModule
import httpx
from urllib.parse import urlparse
import re

class HTTPProbe(BaseModule):
    """
    Módulo para sondagem HTTP avançada.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'HTTP Probe',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Sondagem HTTP com análise de headers e tecnologias',
            'type': 'connection'
        }
        
        self.options = {
            'data': str(),  # URL ou host
            'methods': ['GET', 'HEAD'],
            'follow_redirects': True,
            'analyze_tech': True,
            'timeout': 10,
            'user_agent': 'Mozilla/5.0 (compatible; String-X Scanner)',
            'example': './strx -l urls.txt -st "echo {STRING}" -module "con:http_probe" -pm'
        }
    
    def run(self):
        """
        Executa a sondagem HTTP do host/URL especificado.
        
        Tenta conectar via HTTP/HTTPS e analisa headers, tecnologias
        e outras informações relevantes do servidor.
        """
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
            except Exception:
                continue
    
    def _probe_url(self, url: str) -> str:
        """Realiza sondagem de uma URL específica."""
        headers = {
            'User-Agent': self.options.get('user_agent', 'String-X Scanner')
        }
        
        try:
            timeout = httpx.Timeout(self.options.get('timeout', 10))
            
            with httpx.Client(
                headers=headers,
                timeout=timeout,
                follow_redirects=self.options.get('follow_redirects', True),
                verify=False
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
            
        except Exception as e:
            return f"Error probing {url}: {str(e)}"
    
    def _detect_technologies(self, response) -> list:
        """Detecta tecnologias usadas no site."""
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
        """Extrai título da página HTML."""
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else ''
