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
# Bibliotecas padrão
import subprocess
from typing import List, Dict, Any, Optional, Union

# Módulos locais
from stringx.core.basemodule import BaseModule

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
        ,
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm'
        }
        
        self.options = {
            'data': str(),  # Nome do host a ser pesquisado
            'records': ['A', 'MX', 'TXT', 'NS'],  # Tipos de registros DNS
            'timeout': 5,  # Timeout para consultas DNS
            'resolver': '8.8.8.8',  # Servidor DNS resolver            
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,             # Número de tentativas de requisição
            'retry_delay': None,       # Atraso entre tentativas de requisição 
        }
    
    def _get_dns_record(self, host: str, record_type: str) -> List[str]:
        """
        Obtém registro DNS específico usando dig.
        
        Este método executa o comando dig para consultar um tipo específico
        de registro DNS para o host fornecido, utilizando o resolver configurado.
        
        Args:
            host: Nome do host para consulta
            record_type: Tipo de registro DNS (A, MX, TXT, NS)
            
        Returns:
            Lista de registros encontrados ou lista vazia
            
        Raises:
            subprocess.TimeoutExpired: Se a consulta exceder o timeout configurado
            subprocess.SubprocessError: Erro na execução do comando dig
        """
        try:
            resolver = self.options.get("resolver", "8.8.8.8")
            timeout = self.options.get("timeout", 5)
            
            self.log_debug(f"[*] Consultando registro {record_type} para {host} usando resolver {resolver}")
            
            cmd = ['dig', f'@{resolver}', '+short', host, record_type]
            self.log_debug(f"[*] Executando comando: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, 
                                  text=True, timeout=timeout)
            
            if result.stdout:
                records = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                self.log_debug(f"[+] Encontrados {len(records)} registros {record_type}")
                return records
            else:
                self.log_debug(f"[!] Nenhum registro {record_type} encontrado para {host}")
                return []
                
        except subprocess.TimeoutExpired as te:
            self.handle_error(te, f"Timeout na consulta DNS para {host} ({record_type})")
            return []
        except subprocess.SubprocessError as se:
            self.handle_error(se, "Erro no comando dig")
            return []
        except Exception as e:
            self.handle_error(e, "Erro na consulta DNS")
            return []
    
    def run(self) -> None:
        """
        Executa coleta de informações DNS.
        
        Este método coordena todo o processo de coleta de registros DNS,
        consultando cada tipo de registro configurado para o host especificado,
        e formatando os resultados em uma saída legível.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
            
        Raises:
            ValueError: Erro na validação do host
            subprocess.SubprocessError: Erro na execução das consultas DNS
        """
        try:
            host = self.options.get("data", "").strip()
            
            if not host:
                self.log_debug("[!] Nenhum host especificado")
                return
            
            # Only clear results if auto_clear is enabled (default behavior)
            if self._auto_clear_results:
                self._result[self._get_cls_name()].clear()
            
            self.log_debug(f"[*] Iniciando coleta de DNS para: {host}")
            
            records_to_check = self.options.get('records', ['A', 'MX', 'TXT', 'NS'])
            self.log_debug(f"[*] Tipos de registros a consultar: {', '.join(records_to_check)}")
            
            dns_info = {
                'host': host,
                'records': {}
            }
        
            # Coletar cada tipo de registro DNS configurado
            for record_type in records_to_check:
                self.log_debug(f"[*] Consultando registros {record_type}...")
                records = self._get_dns_record(host, record_type)
                if records:
                    self.log_debug(f"[+] Registros {record_type}: {', '.join(records)}")
                    dns_info['records'][record_type] = records
            
            # Formatar resultado para saída legível
            if dns_info['records']:
                self.log_debug(f"[+] Coletados {len(dns_info['records'])} tipos de registros")
                result = f"Host: {host}\n"
                for rtype, values in dns_info['records'].items():
                    result += f"  {rtype}: {', '.join(values)}\n"
                
                self.set_result(result)
            else:
                self.log_debug("[!] Nenhum registro DNS encontrado")
                
        except ValueError as ve:
            self.handle_error(ve, "Erro de validação DNS")
        except subprocess.SubprocessError as se:
            self.handle_error(se, "Erro execução dig")
        except Exception as e:
            self.handle_error(e, "Erro DNS")