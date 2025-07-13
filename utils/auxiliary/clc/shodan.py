"""
Módulo collector para Shodan API.

Este módulo implementa funcionalidade para consultar a API do Shodan
e obter informações detalhadas sobre hosts, incluindo serviços expostos,
vulnerabilidades e dados de geolocalização.

Shodan é uma ferramenta especializada que realiza varreduras constantes da Internet,
indexando serviços e dispositivos conectados, fornecendo informações valiosas para:
- Descoberta de dispositivos IoT, sistemas industriais e servidores expostos
- Identificação de serviços vulneráveis e versões desatualizadas
- Reconhecimento de infraestrutura e superfície de ataque
- Análise de configurações incorretas e serviços expostos inadvertidamente
- Monitoramento da própria infraestrutura para detecção de exposições acidentais
- Identificação de tecnologias específicas através de banners e fingerprints
- Avaliação de risco externo com base em dados objetivos

Este módulo implementa acesso à API do Shodan para integrar seus recursos
de descoberta de dispositivos e reconhecimento com o fluxo de trabalho do String-X.
"""
import json
import asyncio
import ipaddress
import urllib.parse

from core.http_async import HTTPClient
from core.basemodule import BaseModule

class ShodanCollector(BaseModule):
    """
    Módulo coletor para API do Shodan.
    
    Esta classe permite consultar a API do Shodan para obter informações
    detalhadas sobre hosts, incluindo serviços, portas, vulnerabilidades
    e dados de geolocalização.
    """
    
    def __init__(self):
        """
        Inicializa o módulo coletor Shodan.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Shodan Collector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Coleta informações via API Shodan',
            'type': 'collector'
        ,
            'example': './strx -l ips.txt -st "echo {STRING}" -module "clc:shodan" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # IP ou hostname
            'api_key': str(),  # API key do Shodan
            'query_type': 'host',  # host, search, count
            'facets': str(),  # Para query type 'search'
            'limit': 100,            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'proxy': str(),  # Proxies para requisições (opcional)
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': 1,        # Atraso entre tentativas de requisição  
        }
    
    def run(self):
        """
        Executa consulta na API do Shodan.
        """
        try:
            data = self.options.get('data', '').strip()
            api_key = self.options.get('api_key', '')
            query_type = self.options.get('query_type', 'host')
            
            if not data:
                return
            
            if not api_key:
                self.set_result("✗ Erro: API key do Shodan é obrigatória")
                return
            
            if query_type == 'host':
                result = self._query_host(data, api_key)
            elif query_type == 'search':
                result = self._query_search(data, api_key)
            elif query_type == 'count':
                result = self._query_count(data, api_key)
            else:
                self.set_result("✗ Erro: query_type inválido (host, search, count)")
                return
            
            if result:
                self.set_result(result)
                
        except Exception as e:
            self.set_result(f"✗ Erro Shodan: {str(e)}")
    
    async def _query_host_async(self, ip: str, api_key: str) -> str:
        """Consulta informações de um host específico."""
        try:
            # Validar se é um IP válido
            ipaddress.ip_address(ip)
            
            url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
            
            kwargs = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': 15,
            }
            
            response = await self.request.send_request([url], **kwargs)
            response = response[0]  # Obtém o primeiro resultado da lista
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                result = f"📍 Host: {data.get('ip_str', ip)}\n"
                result += f"🌍 País: {data.get('country_name', 'N/A')}\n"
                result += f"🏢 Org: {data.get('org', 'N/A')}\n"
                result += f"🔌 Portas: {', '.join([str(p['port']) for p in data.get('data', [])])}\n"
                
                # Serviços detectados
                services = []
                for service in data.get('data', []):
                    port = service.get('port')
                    product = service.get('product', 'unknown')
                    version = service.get('version', '')
                    services.append(f"{port}/{product} {version}".strip())
                
                if services:
                    result += f"🔧 Serviços: {'; '.join(services[:5])}\n"
                
                # Vulnerabilidades
                vulns = data.get('vulns', [])
                if vulns:
                    result += f"⚠️ CVEs: {', '.join(list(vulns)[:3])}\n"
                
                return result
                
        except ValueError:
            return "✗ Erro: IP inválido"
        except Exception as e:
            if hasattr(e, 'status_code') and e.status_code == 404:
                return f"ℹ️ Host {ip}: Nenhuma informação disponível"
            return f"✗ Erro na consulta: {str(e)}"
    
    def _query_host(self, ip: str, api_key: str) -> str:
        """Consulta informações de um host específico (wrapper para método assíncrono)."""
        return asyncio.run(self._query_host_async(ip, api_key))
    
    async def _query_search_async(self, query: str, api_key: str) -> str:
        """Realiza busca por query no Shodan."""
        try:
            limit = self.options.get('limit', 100)
            encoded_query = urllib.parse.quote(query)
            
            url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={encoded_query}&limit={limit}"
            
            kwargs = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': 20,
            }
            
            response = await self.request.send_request([url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                total = data.get('total', 0)
                matches = data.get('matches', [])
                
                result = f"🔍 Query: {query}\n"
                result += f"📊 Total: {total} resultados\n"
                result += f"📋 Mostrando: {len(matches)} hosts\n\n"
                
                for i, match in enumerate(matches[:10], 1):
                    ip = match.get('ip_str', 'N/A')
                    port = match.get('port', 'N/A')
                    org = match.get('org', 'N/A')
                    country = match.get('location', {}).get('country_name', 'N/A')
                    
                    result += f"{i}. {ip}:{port} | {org} | {country}\n"
                
                return result
                
        except Exception as e:
            return f"✗ Erro na busca: {str(e)}"
            
    def _query_search(self, query: str, api_key: str) -> str:
        """Realiza busca por query no Shodan (wrapper para método assíncrono)."""
        return asyncio.run(self._query_search_async(query, api_key))
    
    async def _query_count_async(self, query: str, api_key: str) -> str:
        """Conta resultados para uma query."""
        try:
            encoded_query = urllib.parse.quote(query)
            facets = self.options.get('facets', '')
            
            url = f"https://api.shodan.io/shodan/host/count?key={api_key}&query={encoded_query}"
            if facets:
                url += f"&facets={urllib.parse.quote(facets)}"
            
            kwargs = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': 15,
            }
            
            response = await self.request.send_request([url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                total = data.get('total', 0)
                result = f"🔍 Query: {query}\n"
                result += f"📊 Total de resultados: {total}\n"
                
                # Facets (estatísticas)
                facets_data = data.get('facets', {})
                for facet_name, facet_values in facets_data.items():
                    result += f"\n📈 {facet_name.title()}:\n"
                    for item in facet_values[:5]:
                        result += f"  • {item['value']}: {item['count']}\n"
                
                return result
                
        except Exception as e:
            return f"✗ Erro na contagem: {str(e)}"
            
    def _query_count(self, query: str, api_key: str) -> str:
        """Conta resultados para uma query (wrapper para método assíncrono)."""
        return asyncio.run(self._query_count_async(query, api_key))