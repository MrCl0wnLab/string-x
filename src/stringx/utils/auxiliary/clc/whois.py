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
# Bibliotecas padrão
from typing import Optional, Dict, Any

# Bibliotecas de terceiros
import whois

# Módulos locais
from stringx.core.basemodule import BaseModule

class WhoisInfo(BaseModule):
    """
    Coletor de informações WHOIS.
    
    Esta classe coleta dados WHOIS de domínios especificados,
    oferecendo informações completas sobre registros de domínios.
    """
    
    def __init__(self) -> None:
        """
        Inicializa o módulo coletor de informações WHOIS.
        """
        super().__init__()
        self.meta = {
            'name': 'WHOIS Information Collector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Coleta informações WHOIS de domínios',
            'type': 'collector'
        ,
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:whois" -pm'
        }
        self.options = {
            'data': str(),            # Domínio alvo para consulta WHOIS            'debug': False,           # Modo de debug para mostrar informações detalhadas
            'retry': 0,               # Número de tentativas de requisição
            'retry_delay': None,         # Atraso entre tentativas de requisição    
        }
    
    def run(self) -> None:
        """
        Executa a consulta WHOIS para o domínio especificado.
        
        Esta função realiza uma consulta WHOIS para o domínio fornecido
        e retorna as informações de registro disponíveis.
        
        Returns:
            None: Os resultados são armazenados através do método set_result
            
        Raises:
            ValueError: Se o domínio for inválido
            WhoisCommandFailed: Se o comando WHOIS falhar
            FailedParsingWhoisOutput: Se não for possível interpretar a saída WHOIS
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
            
        self.log_debug("[*] Iniciando coleta WHOIS")
        
        domain = self.options.get("data", "").strip()
        if not domain:
            self.log_debug("[X] Nenhum domínio fornecido")
            return
        
        self.log_debug(f"[*] Processando domínio: {domain}")
        
        try:
            self.log_debug(f"[*] Consultando WHOIS para: {domain}")
            
            whois_info = whois.whois(domain)
            
            if whois_info:
                self.log_debug("[+] Informações WHOIS obtidas com sucesso")
                
                # Log de informações importantes encontradas
                if hasattr(whois_info, 'domain_name') and whois_info.domain_name:
                    domain_name = whois_info.domain_name
                    if isinstance(domain_name, list):
                        domain_name = domain_name[0]
                    self.log_debug(f"   [*] Nome de domínio: {domain_name}")
                
                if hasattr(whois_info, 'registrar') and whois_info.registrar:
                    self.log_debug(f"   [*] Registrar: {whois_info.registrar}")
                
                if hasattr(whois_info, 'creation_date') and whois_info.creation_date:
                    creation = whois_info.creation_date
                    if isinstance(creation, list):
                        creation = creation[0]
                    self.log_debug(f"   [*] Data de criação: {creation}")
                
                if hasattr(whois_info, 'expiration_date') and whois_info.expiration_date:
                    expiration = whois_info.expiration_date
                    if isinstance(expiration, list):
                        expiration = expiration[0]
                    self.log_debug(f"   [*] Data de expiração: {expiration}")
                    
                if hasattr(whois_info, 'name_servers') and whois_info.name_servers:
                    if isinstance(whois_info.name_servers, list):
                        ns_list = whois_info.name_servers[:3]
                        self.log_debug(f"   [*] Servidores de nome: {', '.join(ns_list)}")
                        if len(whois_info.name_servers) > 3:
                            self.log_debug(f"        ... e mais {len(whois_info.name_servers) - 3} servidores")
                    else:
                        self.log_debug(f"   [*] Servidores de nome: {whois_info.name_servers}")
                
                if hasattr(whois_info, 'status') and whois_info.status:
                    status = whois_info.status
                    if isinstance(status, list):
                        status = ', '.join(status[:2])  # Show first 2 statuses
                    self.log_debug(f"   [*] Status: {status}")
                
                self.log_debug("[*] Dados WHOIS coletados e formatados")
                self.set_result(str(whois_info))
            else:
                self.log_debug("[!] Nenhuma informação WHOIS encontrada")
                self.set_result("Nenhuma informação WHOIS disponível para este domínio")
                
        except Exception as e:
            self.handle_error(e, "Erro WHOIS")