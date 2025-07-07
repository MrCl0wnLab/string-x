"""
Módulo CLC para coleta de informações DNS.

Este módulo implementa um coletor de informações DNS que consulta diferentes
tipos de registros DNS (A, MX, TXT, NS) para hosts especificados, utilizando
dig como ferramenta subjacente.

O sistema DNS (Domain Name System) é a infraestrutura fundamental da Internet
que traduz nomes de domínios em endereços IP e fornece outros tipos de informações.
Este coletor permite obter vários tipos de registros DNS, o que é útil para:
- Mapeamento da infraestrutura de rede de um domínio
- Identificação de servidores de e-mail (registros MX)
- Verificação de políticas de segurança (registros TXT)
- Enumeração de servidores de nomes autoritativos (registros NS)
- Descoberta de relacionamentos entre domínios
"""
from core.basemodule import BaseModule
import subprocess


class DnsInfo(BaseModule):
    """
    Coletor de informações DNS.
    
    Esta classe coleta registros DNS de hosts especificados, suportando
    múltiplos tipos de registros (A, MX, TXT, NS) e permitindo configuração
    de servidor DNS resolver e timeout.
    
    Herda de BaseModule fornecendo interface padrão para módulos auxiliares.
    """
    
    def __init__(self):
        """
        Inicializa o coletor DNS com configurações padrão.
        """
        super().__init__()
        
        self.meta = {
            'name': 'DNS Information Collector',
            "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Coleta registros DNS de hosts usando dig',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # Nome do host a ser pesquisado
            'records': ['A', 'MX', 'TXT', 'NS'],  # Tipos de registros DNS
            'timeout': 5,  # Timeout para consultas DNS
            'resolver': '8.8.8.8',  # Servidor DNS resolver
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm'
        }
    
    def _get_dns_record(self, host: str, record_type: str) -> list:
        """
        Obtém registro DNS específico usando dig.
        
        Args:
            host (str): Nome do host para consulta
            record_type (str): Tipo de registro DNS (A, MX, TXT, NS)
            
        Returns:
            list: Lista de registros encontrados ou lista vazia
        """
        try:
            cmd = ['dig', f'@{self.options["resolver"]}', 
                   '+short', host, record_type]
            result = subprocess.run(cmd, capture_output=True, 
                                  text=True, timeout=self.options['timeout'])
            if result.stdout:
                records = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                return records
                
        except Exception:
            pass
        return []
    
    def run(self):
        """
        Executa coleta de informações DNS.
        
        Consulta todos os tipos de registros DNS configurados para o host
        especificado e formata o resultado em string legível.
        """
        host = self.options.get("data", "").strip()
        
        if not host:
            return
        
        dns_info = {
            'host': host,
            'records': {}
        }
        
        # Coletar cada tipo de registro DNS configurado
        for record_type in self.options['records']:
            records = self._get_dns_record(host, record_type)
            if records:
                dns_info['records'][record_type] = records
        
        # Formatar resultado para saída legível
        if dns_info['records']:
            result = f"Host: {host}\n"
            for rtype, values in dns_info['records'].items():
                result += f"  {rtype}: {', '.join(values)}\n"
            
            self.set_result(result)