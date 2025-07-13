"""
Módulo CLC para coleta de informações WHOIS.

Este módulo implementa um coletor de informações WHOIS que consulta
dados de registro de domínios.

O WHOIS é um protocolo que fornece informações de registro de domínios e
endereços IP, revelando dados importantes para investigações OSINT:
- Informações sobre proprietários de domínios (quando não protegidas por privacy)
- Datas de criação, atualização e expiração do domínio
- Servidores de nomes autoritativos (nameservers)
- Registrar responsável pelo domínio
- Informações de contato administrativas e técnicas
- Status do domínio (ativo, bloqueado, transferência pendente)

Estas informações são valiosas para:
- Verificar a legitimidade de um site
- Identificar relacionamentos entre diferentes domínios
- Estabelecer cronologia e idade de um domínio
- Correlacionar domínios pertencentes à mesma entidade
- Identificar informações de contato para investigações adicionais
"""
import whois

from core.basemodule import BaseModule

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
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:whois" -pm',
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': 1,        # Atraso entre tentativas de requisição    
        }
    
    def run(self):
        domain = self.options.get("data", "").strip()
        if not domain:
            return None
        
        whois_info = whois.whois(domain)
        self.set_result(str(whois_info))