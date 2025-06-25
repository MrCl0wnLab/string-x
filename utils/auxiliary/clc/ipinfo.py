"""
Módulo collector para informações detalhadas de endereços IP.

Este módulo implementa funcionalidade para obter informações detalhadas sobre 
endereços IP utilizando a API do ipinfo.io, incluindo localização geográfica,
ASN, organização, entre outros dados.
"""
from core.basemodule import BaseModule
from core.user_agent_generator import UserAgentGenerator
import httpx
import json
import socket
import os
import time
from datetime import datetime, timedelta


class IPInfo(BaseModule):
    """
    Coletor de informações detalhadas sobre endereços IP.
    
    Esta classe coleta informações completas sobre endereços IP usando a API
    do ipinfo.io, com opção de utilização de token de API para acesso a 
    recursos adicionais e maior limite de requisições.
    
    Herda de BaseModule fornecendo interface padrão para módulos auxiliares.
    """
 
    def __init__(self):
        """
        Inicializa o coletor de informações IP com configurações padrão.
        
        Este módulo utiliza a API ipinfo.io para obter detalhes como:
        - Hostname e ASN
        - Localização geográfica (cidade, região, país)
        - Coordenadas (latitude, longitude)
        - Organização e ASN
        - Timezone e código postal
        - Informações sobre privacidade e abuso
        
        Nota: O uso gratuito da API tem limite de 50.000 requisições por mês.
        Para acesso a recursos premium, defina um token de API.
        """
        super().__init__()
        
        self.meta = {
            'name': 'IP Information Collector',
            'author': 'MrCl0wn',
            'version': '1.1',
            'description': 'Coleta informações detalhadas sobre endereços IP usando ipinfo.io',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),          # Endereço IP a ser consultado (pode ser múltiplos IPs separados por nova linha)
            'api_token': str(),     # Token de API do ipinfo.io (opcional, pode usar env IPINFO_TOKEN)
            'timeout': 10,          # Timeout para requisições
            'user-agent': 'STRX/1.0 (https://github.com/MrCl0wnLab/string-x)', # User-Agent para requisições
            'example': './strx -l ips.txt -st "echo {STRING}" -module "clc:ipinfo" -pm' # Exemplo de uso
        }
    
    def _is_valid_ip(self, ip: str) -> bool:
        """
        Verifica se o endereço IP fornecido é válido.
        
        Args:
            ip (str): Endereço IP a ser validado
            
        Returns:
            bool: True se o IP for válido, False caso contrário
        """
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            # Pode ser um hostname, tenta resolver
            try:
                socket.gethostbyname(ip)
                return True
            except socket.error:
                return False
    
    def _is_private_ip(self, ip: str) -> bool:
        """
        Verifica se o endereço IP é privado/local.
        
        Args:
            ip (str): Endereço IP a ser verificado
            
        Returns:
            bool: True se for IP privado, False caso contrário
        """
        try:
            # Verifica se é um IP local/privado
            if ip.startswith(('10.', '172.16.', '172.17.', '172.18.', 
                             '172.19.', '172.20.', '172.21.', '172.22.',
                             '172.23.', '172.24.', '172.25.', '172.26.',
                             '172.27.', '172.28.', '172.29.', '172.30.',
                             '172.31.', '192.168.', '127.', '169.254.')):
                return True
            return False
        except Exception:
            return False
    

    def _query_ipinfo(self, ip: str) -> dict:
        """
        Consulta a API do ipinfo.io para obter informações do IP.
        
        Args:
            ip (str): Endereço IP para consulta
            
        Returns:
            dict: Dicionário com informações do IP ou None em caso de erro
        """
     
        
        try:

            base_url = f"https://ipinfo.io/{ip}/json"
            headers = {
                'Accept': 'application/json',
                'User-Agent': UserAgentGenerator.get_random_lib()
            }
            
            # Adiciona token de API se disponível (prioriza opção, depois variável de ambiente)
            token = self.options.get('api_token') or os.environ.get('IPINFO_TOKEN')
            if token:
                headers['Authorization'] = f"Bearer {token}"
            
            response = httpx.get(
                url=base_url, 
                headers=headers,
                timeout=self.options.get('timeout', 10),
                follow_redirects=True
            )
            
            if response.status_code == 200:
                data = response.json()
                # Armazenar no cache com timestamp atual
                return data
            elif response.status_code == 429:  # Too Many Requests
                self.set_result(f"⚠️ {ip}: Limite de requisições excedido. Tente novamente mais tarde ou use um token de API.")
                return None
            else:
                self.set_result(f"⚠️ {ip}: API retornou código {response.status_code}")
                return None
            
        except httpx.RequestError as e:
            self.set_result(f"✗ {ip}: Erro de conexão: {str(e)}")
            return None
        except Exception as e:
            self.set_result(f"✗ {ip}: Erro ao consultar API: {str(e)}")
            return None
    

    def run(self, **kwargs):
        """
        Executa consulta de informações do IP.
        
        Obtém e formata informações detalhadas do IP especificado utilizando
        a API ipinfo.io e registra o resultado. Suporta processamento em lote
        para múltiplos IPs.
        
        Args:
            **kwargs: Argumentos adicionais a serem mesclados com self.options
        """

        ip = self.options.get("data", "").strip()
        if not ip or not self._is_valid_ip(ip) or self._is_private_ip(ip):
            return
        

        if data := self._query_ipinfo(ip):
            '''
            {
                "ip": "8.8.8.8",
                "hostname": "dns.google",
                "city": "Mountain View",
                "region": "California",
                "country": "US",
                "loc": "37.4056,-122.0775",
                "org": "AS15169 Google LLC",
                "postal": "94043",
                "timezone": "America/Los_Angeles",
                "readme": "https://ipinfo.io/missingauth",
                "anycast": true
            }
            '''
            result = {
                "IP": data.get("ip", "N/A"),
                "Hostname": data.get("hostname", "N/A"),
                "City": data.get("city", "N/A"),
                "Region": data.get("region", "N/A"),
                "Country": data.get("country", "N/A"),
                "Location": data.get("loc", "N/A"),
                "Organization": data.get("org", "N/A"),
                "Postal Code": data.get("postal", "N/A"),
                "Timezone": data.get("timezone", "N/A"),
                "Anycast": data.get("anycast", False)
            }
            self.set_result(json.dumps(result))
        return str()