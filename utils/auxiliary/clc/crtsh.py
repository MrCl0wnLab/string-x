"""
Módulo CLC para coleta de certificados SSL/TLS de crt.sh.

Este módulo implementa um coletor de informações de certificados SSL/TLS
utilizando o Certificate Transparency Search (crt.sh), permitindo enumerar
certificados e subdomínios associados a um domínio.

O Certificate Transparency (CT) é um sistema que monitora e registra certificados
SSL/TLS à medida que são emitidos em tempo real. O serviço crt.sh permite consultar
esses logs, o que é útil para:
- Enumeração de subdomínios de um determinado domínio
- Descoberta de certificados emitidos historicamente
- Identificação de certificados potencialmente maliciosos
- Monitoramento de emissão de certificados para um domínio
"""
from core.basemodule import BaseModule
from core.user_agent_generator import UserAgentGenerator
import httpx
import json
import re
import urllib.parse
import backoff
from requests.exceptions import RequestException
import warnings

import asyncio
from core.http_async import HTTPClient

# Suprimir avisos relacionados a verificação de certificados
warnings.filterwarnings("ignore", category=Warning)

class CrtshCollector(BaseModule):
    """
    Coletor de informações de certificados SSL/TLS usando crt.sh.
    
    Esta classe permite coletar informações sobre certificados SSL/TLS e 
    subdomínios associados a um domínio através do serviço crt.sh,
    que armazena dados dos logs de Certificate Transparency.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de coleta crt.sh.
        """
        super().__init__()
        
        # Metadados do módulo
        self.meta = {
            'name': 'Certificate Transparency Collector',
            "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Coleta certificados SSL/TLS e subdomínios usando crt.sh',
            'type': 'collector'
        }
        
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Domínio alvo
            'timeout': 30,  # Timeout para requisições
            'wildcard': True,  # Usar wildcard na busca (%.domain)
            'include_expired': False,  # Incluir certificados expirados
            'exclude_wildcards': True,  # Excluir resultados com wildcard (*.) nos nomes
            'sort_unique': True,  # Ordenar e remover duplicados
            'proxy': str(),  # Proxies para requisições
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:crtsh" -pm',
        }
        
    def log_debug(self, message):
        """
        Registra uma mensagem de debug se o modo de debug estiver ativado.
        
        Args:
            message (str): Mensagem de log
        """
        if self.options.get('debug'):
            print(f"[CRTSH-DEBUG] {message}")
    

    def run(self):
        """
        Executa a coleta de certificados e subdomínios do crt.sh.
        
        Returns:
            Resultados da busca de subdomínios para o domínio alvo.
        """
        # Obtém o domínio alvo da entrada
        domain = self.options.get('data')
        if not domain:
            self.log_debug("Nenhum domínio fornecido")
            return
        
        self.log_debug(f"Domínio alvo: {domain}")
        
        # Realiza consulta ao crt.sh
        try:
            self.log_debug("Iniciando consulta ao crt.sh")
            crt_data = self._query_crtsh(domain)
            
            self.log_debug(f"Resultados obtidos: {len(crt_data) if crt_data else 0}")
            
            if not crt_data:
                # Nenhum resultado encontrado
                self.log_debug("Nenhum resultado encontrado")
                self.set_result("")
                return
                
            # Extrai os subdomínios
            subdomains = self._extract_subdomains(crt_data, domain)
            self.log_debug(f"Subdomínios extraídos: {len(subdomains)}")
            
            # Define o resultado conforme o formato de saída
            if not subdomains:
                self.log_debug("Nenhum subdomínio extraído")
                self.set_result("")
            else:
                # Converte para string com uma entrada por linha para compatibilidade com StringX
                result_str = "\n".join(subdomains)
                self.log_debug(f"Retornando {len(subdomains)} subdomínios")
                self.set_result(result_str)
                
        except Exception as e:
            error_msg = f"Erro na coleta de dados do crt.sh: {str(e)}"
            self.log_error(error_msg)
            self.log_debug(f"Exceção: {type(e).__name__}: {str(e)}")
            import traceback
            self.log_debug(traceback.format_exc())
            self.set_result("")
            return
            
    @backoff.on_exception(
        backoff.expo,
        (httpx.HTTPError, httpx.TimeoutException, RequestException),
        max_tries=3,
        max_time=30
    )
    def _query_crtsh(self, domain: str) -> list:
        """
        Realiza consulta ao crt.sh e retorna os resultados.
        
        Args:
            domain (str): Domínio para pesquisa
            
        Returns:
            list: Lista de resultados da consulta ao crt.sh
        """
        # Sanitiza o domínio de entrada (remove espaços e caracteres não imprimíveis)
        domain = re.sub(r'[^\x20-\x7E]', '', domain).strip()
        # Prepara o domínio para consulta (adiciona wildcard se configurado)
        query_domain = f"%.{domain}"  # Wildcard para crt.sh
        encoded_domain = urllib.parse.quote(query_domain) # Encode properly
        # Constrói a URL final com parâmetros codificados adequadamente
        url = f"https://crt.sh/?q={encoded_domain}&output=json"
        proxy = self.options.get('proxy') if self.options.get('proxy') else None


        kwargs = {
            'headers' : {
                'User-Agent': UserAgentGenerator.get_desktop_user_agent(),
                'Accept': 'application/json',
                },
            'proxies': {
                'http://': proxy,
                'https://': proxy
                },
            'timeout': self.options.get('timeout', 30),  # Timeout de 10 segundos,
            'follow_redirects': True,
        }

        self.log_debug(f"URL de consulta: {url}")
        self.log_debug(f"Parâmetros cliente: {kwargs}")
        request = HTTPClient()
        try:
            # Realiza a requisição
            async def make_request():
                return await request.send_request([url], **kwargs)
            
            self.log_debug("Enviando requisição...")     
            response = asyncio.run(make_request())[0]
            self.log_debug(f"Status code: {response.status_code}")
                
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.log_debug(f"Dados JSON recebidos: {len(data)} registros")
                    return data
                except json.JSONDecodeError:
                    error_msg = "Resposta recebida não é um JSON válido"
                    print(error_msg)
                    self.log_debug(f"Resposta: {response.text[:200]}...")
                    return []
            else:
                error_msg = f"Erro na requisição: Status {response.status_code}"
                self.log_error(error_msg)
                self.log_debug(f"Resposta: {response.text[:200]}...")
                return []
                
        except Exception as e:
            error_msg = f"Erro ao consultar crt.sh: {e}"
            print(error_msg)
            self.log_debug(f"Exceção detalhada: {type(e).__name__}: {str(e)}")
            import traceback
            self.log_debug(traceback.format_exc())
            return []
    
    def _extract_subdomains(self, crt_data: list, domain: str) -> list:
        """
        Extrai e processa subdomínios dos dados de certificados.
        
        Args:
            crt_data (list): Dados de certificados do crt.sh
            domain (str): Domínio base para filtragem
            
        Returns:
            list: Lista de subdomínios únicos, opcionalmente ordenados
        """
        result_domains = []
        try:
            for entry in crt_data:
                name = entry.get('name_value', '')
                if '\n' in name:
                    names = name.split('\n')
                else:
                    names = [name]
                
                for domain in names:
                    domain = domain.strip().lower().replace('*.', '')  # Remove wildcard prefix if exists
                    result_domains.append(domain)
            
            return list(set(result_domains))  # Remove duplicados
        except Exception as e:
            error_msg = f"Erro ao extrair subdomínios: {str(e)}"
            self.log_debug(error_msg)
            import traceback
            self.log_debug(traceback.format_exc())
            return []
        
   