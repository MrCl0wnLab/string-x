"""
Módulo extrator de endereços IP.

Este módulo implementa funcionalidade para extrair endereços IPv4 e IPv6
de textos usando expressões regulares.
"""
import re
import ipaddress

from stringx.core.basemodule import BaseModule

class IPExtractor(BaseModule):
    """
    Módulo para extração de endereços IP usando regex.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'IP Address Extractor',
            'author': 'MrCl0wn', 
            'version': '1.0',
            'description': 'Extrai endereços IPv4 e IPv6',
            'type': 'extractor'
        ,
            'example': './strx -l logs.txt -st "echo {STRING}" -module "ext:ip" -pm'
        }
        
        self.options = {
            'data': str(),
            'ipv4': True,
            'ipv6': True,
            'private': True,  # Incluir IPs privados            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição 
        }
    
    def run(self):
        """
        Executa o processo de extração de endereços IP.
        
        Utiliza os dados fornecidos e busca por endereços IPv4 e IPv6
        usando padrões regex específicos para cada tipo.
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
            
        self.log_debug("[*] Iniciando extração de endereços IP")
        
        try:
            if not (target_value := self.options.get("data")):
                self.log_debug("[x] Dados não fornecidos")
                return
                
            self.log_debug(f"[*] Processando {len(target_value)} caracteres de dados")
            results = set()
            ipv4_enabled = self.options.get('ipv4', True)
            ipv6_enabled = self.options.get('ipv6', True)
            include_private = self.options.get('private', True)
            
            self.log_debug(f"[*] IPv4: {'[+]' if ipv4_enabled else '[x]'}, IPv6: {'[+]' if ipv6_enabled else '[x]'}, Privados: {'[+]' if include_private else '[x]'}")
            
            if ipv4_enabled:
                # IPv4 pattern
                ipv4_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
                ipv4_matches = re.findall(ipv4_pattern, target_value)
                self.log_debug(f"[+] Encontrados {len(ipv4_matches)} endereços IPv4")
                
                for ip in ipv4_matches:
                    is_private = self._is_private_ipv4(ip)
                    if include_private or not is_private:
                        results.add(f"IPv4: {ip}")
                        self.log_debug(f"[*] {ip} ({'privado' if is_private else 'público'})")
                    else:
                        self.log_debug(f"[x] {ip} (privado - filtrado)")
            
            if ipv6_enabled:
                # IPv6 pattern (simplified)
                ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
                ipv6_matches = re.findall(ipv6_pattern, target_value)
                self.log_debug(f"[+] Encontrados {len(ipv6_matches)} endereços IPv6")
                
                for ip in ipv6_matches:
                    results.add(f"IPv6: {ip}")
                    self.log_debug(f"[*] {ip}")
            
            if results:
                self.log_debug(f"[*] Total de IPs únicos coletados: {len(results)}")
                self.set_result("; ".join(sorted(results)))
            else:
                self.log_debug("[!] Nenhum endereço IP encontrado")
                
        except Exception as e:
            self.handle_error(e, "Erro na extração de IPs")
    
    def _is_private_ipv4(self, ip: str) -> bool:
        """Verifica se é IP privado."""
        try:
            return ipaddress.IPv4Address(ip).is_private
        except Exception as e:
            self.handle_error(e, "Erro ao verificar se IP é privado")
            return False
