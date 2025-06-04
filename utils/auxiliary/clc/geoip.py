"""
Módulo collector para geolocalização de IPs.

Este módulo implementa funcionalidade para obter informações de
geolocalização de endereços IP usando APIs públicas gratuitas.
"""
from core.basemodule import BaseModule
import ipaddress

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
        
        self.meta = {
            'name': 'GeoIP Collector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Geolocalização de endereços IP',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # IP address
            'api_provider': 'auto',  # auto, ipapi, ipinfo, freegeoip
            'include_isp': True,
            'timeout': 10,
            'example': './strx -l ips.txt -st "echo {STRING}" -module "clc:geoip" -pm'
        }
    
    def run(self):
        """
        Executa consulta de geolocalização.
        """
        try:
            ip = self.options.get('data', '').strip()
            
            if not ip:
                return
            
            # Validar IP
            if not self._is_valid_ip(ip):
                self.set_result(f"✗ {ip}: IP inválido")
                return
            
            # Verificar se é IP privado
            if self._is_private_ip(ip):
                self.set_result(f"ℹ️ {ip}: IP privado/local")
                return
            
            provider = self.options.get('api_provider', 'auto')
            
            # Tentar diferentes APIs em ordem de preferência
            apis = ['ipapi', 'ipinfo', 'freegeoip'] if provider == 'auto' else [provider]
            
            for api in apis:
                try:
                    result = self._query_api(ip, api)
                    if result:
                        self.set_result(result)
                        return
                except Exception:
                    continue
            
            self.set_result(f"✗ {ip}: Não foi possível obter geolocalização")
            
        except Exception as e:
            self.set_result(f"✗ Erro na geolocalização: {str(e)}")
    
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
    
    def _query_api(self, ip: str, api: str) -> str:
        """Consulta API específica."""
        if api == 'ipapi':
            return self._query_ipapi(ip)
        elif api == 'ipinfo':
            return self._query_ipinfo(ip)
        elif api == 'freegeoip':
            return self._query_freegeoip(ip)
        else:
            raise ValueError(f"API não suportada: {api}")
    
    def _query_ipapi(self, ip: str) -> str:
        """Consulta API ip-api.com (gratuita)."""
        try:
            import json
            import urllib.request
            
            url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
            
            with urllib.request.urlopen(url, timeout=self.options.get('timeout', 10)) as response:
                data = json.loads(response.read().decode('utf-8'))
                
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
                else:
                    return None
                    
        except Exception:
            return None
    
    def _query_ipinfo(self, ip: str) -> str:
        """Consulta API ipinfo.io (gratuita com limite)."""
        try:
            import json
            import urllib.request
            
            url = f"https://ipinfo.io/{ip}/json"
            
            with urllib.request.urlopen(url, timeout=self.options.get('timeout', 10)) as response:
                data = json.loads(response.read().decode('utf-8'))
                
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
                else:
                    return None
                    
        except Exception:
            return None
    
    def _query_freegeoip(self, ip: str) -> str:
        """Consulta API freegeoip.app (gratuita)."""
        try:
            import json
            import urllib.request
            
            url = f"https://freegeoip.app/json/{ip}"
            
            with urllib.request.urlopen(url, timeout=self.options.get('timeout', 10)) as response:
                data = json.loads(response.read().decode('utf-8'))
                
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
                else:
                    return None
                    
        except Exception:
            return None
