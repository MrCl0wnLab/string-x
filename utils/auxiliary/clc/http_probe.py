"""
Módulo CLC para verificação de servidores HTTP/HTTPS.

Este módulo implementa um coletor que verifica a disponibilidade de servidores web
e coleta informações básicas como status HTTP, título da página, servidores, redirecionamentos
e cabeçalhos de segurança.

É útil para:
- Verificar se um host está ativo e respondendo em portas HTTP/HTTPS
- Coletar cabeçalhos de resposta para análise
- Identificar tecnologias utilizadas pelo servidor
- Verificar redirecionamentos e configurações de segurança
- Mapear a superfície de ataque de aplicações web
"""
# Bibliotecas padrão
import re
import ssl
import socket

# Bibliotecas de terceiros
import httpx
import asyncio
from bs4 import BeautifulSoup

from typing import Dict, List, Any, Optional, Union
from urllib.parse import urlparse, urljoin

# Módulos locais
from core.basemodule import BaseModule
from core.retry import retry_operation

class HttpProbe(BaseModule):
    """
    Coletor para verificação e análise de servidores HTTP/HTTPS.
    
    Esta classe verifica a disponibilidade de servidores web, coleta informações
    sobre status HTTP, títulos, tecnologias e configurações de segurança.
    
    Herda de BaseModule fornecendo interface padrão para módulos auxiliares.
    """
    
    def __init__(self):
        """
        Inicializa o verificador HTTP com configurações padrão.
        """
        super().__init__()
        
        self.meta = {
            'name': 'HTTP Server Probe',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Verifica disponibilidade e coleta informações de servidores HTTP/HTTPS',
            'type': 'collector',
            'example': './strx -l urls.txt -st "echo {STRING}" -module "clc:http_probe" -pm'
        }
        
        self.options = {
            'data': str(),          # URL ou domínio a ser verificado
            'timeout': 10,           # Timeout para requisições HTTP em segundos
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'follow_redirects': True,  # Seguir redirecionamentos
            'max_redirects': 5,       # Máximo de redirecionamentos a seguir
            'verify_ssl': False,      # Verificar certificados SSL
            'ports': [80, 443, 8080, 8443],  # Portas padrão a verificar
            'collect_headers': True,  # Coletar cabeçalhos importantes
            'collect_title': True,    # Extrair título da página
            'debug': False,           # Modo de debug
            'proxy': None,            # Proxy para requisições
            'retry': 3,               # Número de tentativas
            'retry_delay': None,         # Atraso entre tentativas (segundos)
        }
        
        # Cabeçalhos de segurança importantes para verificação
        self.security_headers = [
            'Content-Security-Policy',
            'Strict-Transport-Security',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy',
        ]
    
    def _normalize_url(self, url: str) -> List[str]:
        """
        Normaliza e formata URLs para verificação.
        
        Converte domínios em URLs completas (HTTP e HTTPS) e
        valida formatos de URL.
        
        Args:
            url: URL ou domínio a ser normalizado
            
        Returns:
            Lista de URLs normalizadas para testar
        """
        url = url.strip()
        urls_to_check = []
        
        # Se não tiver um esquema, tente ambos HTTP e HTTPS
        if not url.startswith(('http://', 'https://')):
            # Verifica se parece um IP ou domínio
            if re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}$', url) or \
               re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', url):
                ports = self.options.get('ports', [80, 443, 8080, 8443])
                
                # Adiciona HTTP para portas 80 e 8080
                if 80 in ports:
                    urls_to_check.append(f"http://{url}")
                if 8080 in ports:
                    urls_to_check.append(f"http://{url}:8080")
                
                # Adiciona HTTPS para portas 443 e 8443
                if 443 in ports:
                    urls_to_check.append(f"https://{url}")
                if 8443 in ports:
                    urls_to_check.append(f"https://{url}:8443")
            else:
                # Se não parece um domínio ou IP válido, tenta como está
                urls_to_check.append(url)
        else:
            # Já tem esquema, usar como está
            urls_to_check.append(url)
            
        return urls_to_check
    
    def _extract_title(self, content: str) -> str:
        """
        Extrai o título de uma página HTML.
        
        Args:
            content: Conteúdo HTML da página
            
        Returns:
            Título extraído ou string vazia se não encontrado
        """
        try:
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.title.string if soup.title else ""
            return title.strip() if title else ""
        except Exception as e:
            self.handle_error(e, "Erro ao extrair título da página")
            return ""
    
    @retry_operation
    async def _probe_url(self, url: str, client: httpx.AsyncClient) -> Dict[str, Any]:
        """
        Verifica uma URL e coleta informações.
        
        Args:
            url: URL a ser verificada
            client: Cliente HTTP assíncrono
            
        Returns:
            Dicionário com informações coletadas
        """
        result = {
            'url': url,
            'status': None,
            'title': None,
            'server': None,
            'redirect_url': None,
            'security_headers': {},
            'error': None,
            'ip': None,
        }
        
        try:
            # Resolver IP do host
            parsed = urlparse(url)
            try:
                result['ip'] = socket.gethostbyname(parsed.netloc.split(':')[0])
            except socket.gaierror:
                result['ip'] = None
            
            # Fazer requisição HTTP
            response = await client.get(url)
            result['status'] = response.status_code
            
            # Verificar redirecionamento
            if response.is_redirect:
                redirect_url = response.headers.get('Location', '')
                if not redirect_url.startswith(('http://', 'https://')):
                    # Resolver URLs relativas
                    redirect_url = urljoin(url, redirect_url)
                result['redirect_url'] = redirect_url
            
            # Coletar cabeçalhos
            result['server'] = response.headers.get('Server', '')
            
            # Coletar cabeçalhos de segurança
            if self.options.get('collect_headers', True):
                for header in self.security_headers:
                    if header in response.headers:
                        result['security_headers'][header] = response.headers[header]
            
            # Extrair título se configurado e se for HTML
            if self.options.get('collect_title', True) and 'text/html' in response.headers.get('Content-Type', ''):
                result['title'] = self._extract_title(response.text)
            
            return result
        except httpx.HTTPError as e:
            result['error'] = f"Erro HTTP: {str(e)}"
            return result
        except Exception as e:
            result['error'] = f"Erro: {str(e)}"
            return result
    
    async def _probe_all_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Verifica várias URLs de forma assíncrona.
        
        Args:
            urls: Lista de URLs a verificar
            
        Returns:
            Lista de resultados para cada URL
        """
        timeout = self.options.get('timeout', 10)
        user_agent = self.options.get('user_agent', 'Mozilla/5.0')
        verify_ssl = self.options.get('verify_ssl', False)
        max_redirects = self.options.get('max_redirects', 5) if self.options.get('follow_redirects', True) else 0
        proxy = self.options.get('proxy')
        
        # Configurações de limites para clientes
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=25)
        
        headers = {'User-Agent': user_agent}
        
        # Construir configuração de cliente HTTP
        client_params = {
            'timeout': timeout,
            'follow_redirects': self.options.get('follow_redirects', True),
            'headers': headers,
            'limits': limits,
            'verify': verify_ssl,
        }
        
        # Adicionar proxy se configurado
        if proxy:
            client_params['proxies'] = proxy
        
        # Verificar URLs de forma assíncrona
        async with httpx.AsyncClient(**client_params) as client:
            tasks = [self._probe_url(url, client) for url in urls]
            results = []
            
            for task in tasks:
                try:
                    result = await task
                    results.append(result)
                except Exception as e:
                    self.handle_error(e, "Erro ao verificar URL")
        
        return results
        
    def _format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Formata os resultados das verificações para saída.
        
        Args:
            results: Lista de resultados de verificações
            
        Returns:
            String formatada com os resultados
        """
        output = []
        
        for result in results:
            status_str = f"{result['status']}" if result['status'] else "Error"
            
            # Determinar cor/símbolo com base no status
            if result.get('error'):
                status_indicator = "❌"
            elif result['status'] and 200 <= result['status'] < 300:
                status_indicator = "✅"
            elif result['status'] and 300 <= result['status'] < 400:
                status_indicator = "↪️"
            elif result['status'] and 400 <= result['status'] < 500:
                status_indicator = "⚠️"
            elif result['status'] and 500 <= result['status'] < 600:
                status_indicator = "🔥"
            else:
                status_indicator = "❓"
            
            # Formatar linha principal
            line = f"{status_indicator} {result['url']} ({status_str})"
            if result['ip']:
                line += f" - IP: {result['ip']}"
            output.append(line)
            
            # Adicionar detalhes
            if result['title']:
                output.append(f"   📄 Título: {result['title']}")
            
            if result['server']:
                output.append(f"   🖥️ Servidor: {result['server']}")
            
            if result['redirect_url']:
                output.append(f"   Redireciona para: {result['redirect_url']}")
            
            if result['security_headers']:
                headers_str = ", ".join([f"{k}: {v}" for k, v in result['security_headers'].items()])
                output.append(f"   🔒 Headers de Segurança: {headers_str}")
            
            if result['error']:
                output.append(f"   Erro: {result['error']}")
            
            # Linha em branco entre resultados
            output.append("")
        
        return "\n".join(output).strip()
    
    async def _async_run(self) -> None:
        """
        Implementação assíncrona do método run.
        """
        try:
            target = self.options.get("data", "").strip()
            
            if not target:
                self.log_debug("Nenhum alvo especificado")
                return
            
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            
            self.log_debug(f"Verificando URL/host: {target}")
            
            # Normalizar URL(s)
            urls_to_check = self._normalize_url(target)
            if not urls_to_check:
                self.log_debug(f"Erro: URL inválida: {target}")
                return
            
            self.log_debug(f"URLs a verificar: {', '.join(urls_to_check)}")
            
            # Verificar todas as URLs
            results = await self._probe_all_urls(urls_to_check)
            
            # Formatar e definir resultados
            if results:
                output = self._format_results(results)
                self.set_result(output)
            else:
                self.log_debug(f"❓ Sem resposta de {target}")
            
        except Exception as e:
            self.handle_error(e, "Erro HTTPProbe")
    
    def run(self) -> None:
        """
        Executa a verificação de servidor HTTP/HTTPS.
        
        Este método coordena todo o processo de verificação de URLs,
        incluindo normalização, requisições assíncronas e formatação
        dos resultados.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
        """
        
        
        # Obter loop de evento ou criar um novo
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Executar o método assíncrono
        loop.run_until_complete(self._async_run())
