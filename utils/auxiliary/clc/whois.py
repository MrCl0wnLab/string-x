"""
Módulo CLC para coleta de informações WHOIS.

Este módulo implementa um coletor de informações WHOIS que consulta
dados de registro de domínios.
"""
from core.basemodule import BaseModule
import whois

class WhoisInfo(BaseModule):
    """
    Coletor de informações WHOIS.
    
    Esta classe coleta dados WHOIS de domínios especificados.
    """
    
    def __init__(self):
        super().__init__()
        self.meta = {
            'name': 'WHOIS Information Collector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Coleta informações WHOIS de domínios',
            'type': 'collector'
        }
        self.options = {
            'data': str(),
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:whois" -pm'
        }
    
    def run(self):
        domain = self.options.get("data", "").strip()
        if not domain:
            return None
        
        whois_info = whois.whois(domain)
        self.set_result(str(whois_info))