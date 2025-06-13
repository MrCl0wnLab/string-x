"""
Módulo CLC para enumeração de subdomínios.

Este módulo implementa um coletor de subdomínios usando múltiplas técnicas
incluindo certificate transparency e bruteforce DNS.
"""
from core.basemodule import BaseModule
import httpx
import json

class SubdomainEnum(BaseModule):
    """
    Coletor de subdomínios usando múltiplas fontes.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'Subdomain Enumerator',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Enumera subdomínios usando CT logs e bruteforce',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # Domínio alvo
            'methods': ['crtsh', 'certspotter', 'hackertarget'],
            'timeout': 10,
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:subdomain" -pm',
            'proxy': str(),  # Proxies para requisições (opcional)
        }
    
    def run(self):
        """
        Executa a enumeração de subdomínios.
        
        Utiliza múltiplas fontes para encontrar subdomínios do domínio especificado.
        """
        domain = self.options.get("data", "").strip()
        if not domain:
            return
            
        subdomains = set()
        methods = self.options.get('methods', ['crtsh'])
        
        for method in methods:
            try:
                if method == 'crtsh':
                    subs = self._crtsh_search(domain)
                elif method == 'certspotter':
                    subs = self._certspotter_search(domain)
                elif method == 'hackertarget':
                    subs = self._hackertarget_search(domain)
                else:
                    continue
                    
                subdomains.update(subs)
            except Exception:
                continue
        
        for subdomain in sorted(subdomains):
            self.set_result(subdomain)
    
    def _crtsh_search(self, domain: str) -> set:
        """Busca subdomínios no crt.sh"""
        url = f"https://crt.sh/?q=%25.{domain}&output=json"


        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }

        with httpx.Client(verify=False, **client_kwargs) as client:
            response = client.get(url)
        
        subdomains = set()
        if response.status_code == 200:
            try:
                data = response.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    if '\n' in name:
                        subdomains.update(name.split('\n'))
                    else:
                        subdomains.add(name)
            except:
                pass
        
        return {sub.strip() for sub in subdomains if sub.strip() and domain in sub}
    
    def _certspotter_search(self, domain: str) -> set:
        """Busca subdomínios no CertSpotter"""
        url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"

        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }


        with httpx.Client(verify=False, **client_kwargs) as client:
            response = client.get(url)
        
        subdomains = set()
        if response.status_code == 200:
            try:
                data = response.json()
                for entry in data:
                    dns_names = entry.get('dns_names', [])
                    subdomains.update(dns_names)
            except:
                pass
        
        return {sub for sub in subdomains if domain in sub}
    
    def _hackertarget_search(self, domain: str) -> set:
        """Busca subdomínios no HackerTarget"""
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"

        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }
        
        with httpx.Client(verify=False, **client_kwargs) as client:
            response = client.get(url)
        
        subdomains = set()
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            for line in lines:
                if ',' in line:
                    subdomain = line.split(',')[0].strip()
                    subdomains.add(subdomain)
        
        return subdomains
