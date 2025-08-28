"""
Módulo collector para geolocalização de IPs.

Este módulo implementa funcionalidade para obter informações de
geolocalização de endereços IP usando APIs públicas gratuitas.

A geolocalização de endereços IP fornece informações valiosas para:
- Identificar a localização aproximada (país, cidade) da origem do tráfego
- Detectar potenciais ameaças com base na região de origem
- Analisar logs de acesso e tentativas de intrusão
- Verificar a legitimidade de conexões e requisições
- Mapear a distribuição geográfica de visitantes ou atacantes
- Identificar o provedor de serviços associado ao endereço IP

Este módulo utiliza múltiplas fontes de informação para obter dados
de geolocalização com maior precisão e confiabilidade, alternando
entre diferentes APIs quando necessário.
"""
import json
import asyncio
import ipaddress

from stringx.core.basemodule import BaseModule
from stringx.core.http_async import HTTPClient

class GeoIPCollector(BaseModule):
    """
    Módulo coletor para geolocalização de IPs.
    
    Esta classe permite obter informações detalhadas de geolocalização
    de endereços IP através de múltiplas APIs públicas.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de geolocalização IP.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'GeoIP Collector',
            'author': 'MrCl0wn',
            'version': '1.1',
            'description': 'Geolocalização de endereços IP',
            'type': 'collector'
        ,
            'example': './strx -l ips.txt -st "echo {STRING}" -module "clc:geoip" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # IP address
            'api_provider': 'auto',  # auto, ipapi, ipinfo, freegeoip
            'include_isp': True,
            'timeout': 10,            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição   
        }
        
        
    
    def run(self):
        """
        Executa consulta de geolocalização.
        """
        try:
            ip = self.options.get('data', '').strip()
            
            if not ip:
                self.log_debug("[!] Nenhum IP fornecido.")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            # Validar IP
            if not self._is_valid_ip(ip):
                self.set_result(f"{ip}: IP inválido")
                return
            
            # Verificar se é IP privado
            if self._is_private_ip(ip):
                self.set_result(f"{ip}: IP privado/local")
                return
            
            provider = self.options.get('api_provider', 'auto')
            
            # Tentar diferentes APIs em ordem de preferência
            apis = ['ipapi', 'ipinfo', 'freegeoip'] if provider == 'auto' else [provider]
            
            for api in apis:
                try:
                    result = asyncio.run(self._query_api(ip, api))
                    if result:
                        self.set_result(result)
                        return
                except Exception:
                    continue
            
            self.set_result(f"{ip}: Não foi possível obter geolocalização")
            
        except Exception as e:
            self.handle_error(e, "Erro GeoIP")
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Valida se é um IP válido."""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def _is_private_ip(self, ip: str) -> bool:
        """Verifica se é um IP privado."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
        except ValueError:
            return False
    
    async def _query_api(self, ip: str, api: str) -> str:
        """Consulta API específica."""
        if api == 'ipapi':
            return await self._query_ipapi(ip)
        elif api == 'ipinfo':
            return await self._query_ipinfo(ip)
        elif api == 'freegeoip':
            return await self._query_freegeoip(ip)
        else:
            raise ValueError(f"API não suportada: {api}")
    
    async def _query_ipapi(self, ip: str) -> str:
        """Consulta API ip-api.com (gratuita)."""
        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
            
            kwargs = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': self.options.get('timeout', 10),
            }
            
            response = await self.request.send_request([url], **kwargs)
            response = response[0]  # Obtém o primeiro resultado da lista
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                if data.get('status') == 'success':
                    result = f"🌍 IP: {data.get('query', ip)}\n"
                    result += f"🗺️ Localização:\n"
                    result += f"  • País: {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})\n"
                    result += f"  • Estado: {data.get('regionName', 'N/A')}\n"
                    result += f"  • Cidade: {data.get('city', 'N/A')}\n"
                    result += f"  • CEP: {data.get('zip', 'N/A')}\n"
                    result += f"📍 Coordenadas: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}\n"
                    result += f"⏰ Timezone: {data.get('timezone', 'N/A')}\n"
                    
                    if self.options.get('include_isp', True):
                        result += f"🏢 ISP: {data.get('isp', 'N/A')}\n"
                        result += f"🏭 Org: {data.get('org', 'N/A')}\n"
                        result += f"🔢 AS: {data.get('as', 'N/A')}\n"
                    
                    result += f"📊 Fonte: ip-api.com"
                    return result
            
            return None
                    
        except Exception:
            return None
    
    async def _query_ipinfo(self, ip: str) -> str:
        """Consulta API ipinfo.io (gratuita com limite)."""
        try:
            url = f"https://ipinfo.io/{ip}/json"
            
            kwargs = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': self.options.get('timeout', 10),
            }
            
            response = await self.http_client.send_request([url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                if 'ip' in data and 'bogon' not in data:
                    result = f"🌍 IP: {data.get('ip', ip)}\n"
                    result += f"🗺️ Localização:\n"
                    
                    # Parse location
                    location = data.get('loc', '').split(',')
                    if len(location) == 2:
                        lat, lon = location
                        result += f"📍 Coordenadas: {lat}, {lon}\n"
                    
                    result += f"  • Cidade: {data.get('city', 'N/A')}\n"
                    result += f"  • Estado: {data.get('region', 'N/A')}\n"
                    result += f"  • País: {data.get('country', 'N/A')}\n"
                    result += f"  • CEP: {data.get('postal', 'N/A')}\n"
                    result += f"⏰ Timezone: {data.get('timezone', 'N/A')}\n"
                    
                    if self.options.get('include_isp', True):
                        result += f"🏢 Org: {data.get('org', 'N/A')}\n"
                    
                    result += f"📊 Fonte: ipinfo.io"
                    return result
            
            return None
                    
        except Exception:
            return None
    
    async def _query_freegeoip(self, ip: str) -> str:
        """Consulta API freegeoip.app (gratuita)."""
        try:
            url = f"https://freegeoip.app/json/{ip}"
            
            kwargs = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': self.options.get('timeout', 10),
            }
            
            response = await self.http_client.send_request([url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                if data.get('ip') == ip:
                    result = f"🌍 IP: {data.get('ip', ip)}\n"
                    result += f"🗺️ Localização:\n"
                    result += f"  • País: {data.get('country_name', 'N/A')} ({data.get('country_code', 'N/A')})\n"
                    result += f"  • Estado: {data.get('region_name', 'N/A')}\n"
                    result += f"  • Cidade: {data.get('city', 'N/A')}\n"
                    result += f"  • CEP: {data.get('zip_code', 'N/A')}\n"
                    result += f"📍 Coordenadas: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}\n"
                    result += f"⏰ Timezone: {data.get('time_zone', 'N/A')}\n"
                    result += f"📊 Fonte: freegeoip.app"
                    return result
            
            return None
                    
        except Exception:
            return None