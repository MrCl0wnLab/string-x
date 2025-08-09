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
        domain = self.options.get("data", "").strip()
        if not domain:
            self.log_debug("Nenhum domínio fornecido")
            return
        
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        
        try:
            self.log_debug(f"Iniciando consulta WHOIS para: {domain}")
            
            whois_info = whois.whois(domain)
            
            if whois_info:
                self.log_debug("Informações WHOIS obtidas com sucesso")
                
                # Log de informações importantes encontradas
                if hasattr(whois_info, 'domain_name') and whois_info.domain_name:
                    self.log_debug(f"Nome de domínio: {whois_info.domain_name}")
                
                if hasattr(whois_info, 'registrar') and whois_info.registrar:
                    self.log_debug(f"Registrar: {whois_info.registrar}")
                
                if hasattr(whois_info, 'creation_date') and whois_info.creation_date:
                    self.log_debug(f"Data de criação: {whois_info.creation_date}")
                
                if hasattr(whois_info, 'expiration_date') and whois_info.expiration_date:
                    self.log_debug(f"Data de expiração: {whois_info.expiration_date}")
                    
                if hasattr(whois_info, 'name_servers') and whois_info.name_servers:
                    if isinstance(whois_info.name_servers, list):
                        self.log_debug(f"Servidores de nome: {', '.join(whois_info.name_servers[:3])}")
                    else:
                        self.log_debug(f"Servidores de nome: {whois_info.name_servers}")
                
                self.set_result(str(whois_info))
            else:
                self.log_debug("Nenhuma informação WHOIS encontrada")
                self.set_result("Nenhuma informação WHOIS disponível para este domínio")
                
        except Exception as e:
            self.handle_error(e, "Erro WHOIS")