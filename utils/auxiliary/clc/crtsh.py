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
# Bibliotecas padrão
import re
import json
import asyncio
import warnings
import traceback
import urllib.parse
from typing import List, Dict, Any, Optional

# Bibliotecas de terceiros
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException

# Módulos locais
from core.http_async import HTTPClient
from core.basemodule import BaseModule
from core.retry import retry_operation
from core.user_agent_generator import UserAgentGenerator

# Suprimir avisos relacionados a verificação de certificados
warnings.filterwarnings("ignore", category=Warning)

class CrtshCollector(BaseModule):
    """
    Coletor de informações de certificados SSL/TLS usando crt.sh.
    
    Esta classe permite coletar informações sobre certificados SSL/TLS e 
    subdomínios associados a um domínio através do serviço crt.sh,
    que armazena dados dos logs de Certificate Transparency.
    """
    
    def __init__(self) -> None:
        """
        Inicializa o módulo de coleta crt.sh.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Certificate Transparency Collector',
            "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Coleta certificados SSL/TLS e subdomínios usando crt.sh',
            'type': 'collector'
        ,
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:crtsh" -pm'
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
            'debug': False,  # Modo de debug para mostrar informações detalhadas            'retry': 0,             # Número de tentativas de requisição
            'retry_delay': 1,       # Atraso entre tentativas de requisição 
        }

    def run(self) -> None:
        """
        Executa a coleta de certificados e subdomínios do crt.sh.
        
        Esta função realiza a consulta ao serviço crt.sh, processa os dados 
        retornados e extrai os subdomínios associados ao domínio alvo.
        
        Returns:
            None: Os resultados são armazenados através do método set_result
            
        Raises:
            ValueError: Se ocorrer erro na validação ou processamento dos dados
            RequestException: Se ocorrer erro na comunicação com o serviço crt.sh
            ConnectionError: Se não for possível estabelecer conexão com o serviço
            Timeout: Se a requisição exceder o tempo limite configurado
        """
        # Obtém o domínio alvo da entrada
        domain = self.options.get('data')
        if not domain:
            self.log_debug("Nenhum domínio fornecido")
            return
        
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        
        self.log_debug(f"Iniciando coleta de certificados para domínio: {domain}")
        
        # Realiza consulta ao crt.sh
        try:
            # Mensagem de debug para o usuário
            self.set_result(f"🔍 Consultando certificados para: {domain}")
            
            self.log_debug("Iniciando consulta ao serviço crt.sh")
            
            # Verificar configurações
            use_wildcard = self.options.get('wildcard', True)
            if use_wildcard:
                self.log_debug("Usando busca com wildcard (%.domain)")
            
            timeout = self.options.get('timeout', 30)
            self.log_debug(f"Timeout configurado: {timeout} segundos")
            
            proxy = self.options.get('proxy')
            if proxy:
                self.log_debug(f"Usando proxy: {proxy}")
            
            # Executar consulta
            crt_data = self._query_crtsh(domain)
            
            total_results = len(crt_data) if crt_data else 0
            self.log_debug(f"Consulta retornou {total_results} certificados")
            
            if not crt_data:
                # Nenhum resultado encontrado
                self.log_debug("Nenhum certificado encontrado para o domínio")
                self.set_result("")
                return
                
            # Extrai os subdomínios
            exclude_wildcards = self.options.get('exclude_wildcards', True)
            if exclude_wildcards:
                self.log_debug("Configurado para excluir subdomínios wildcard (*)")
                
            sort_unique = self.options.get('sort_unique', True)
            if sort_unique:
                self.log_debug("Configurado para ordenar e remover duplicados")
                
            self.log_debug("Extraindo subdomínios dos certificados")
            subdomains = self._extract_subdomains(crt_data, domain)
            self.log_debug(f"Total de subdomínios extraídos: {len(subdomains)}")
            
            # Define o resultado conforme o formato de saída
            if not subdomains:
                self.log_debug("Nenhum subdomínio extraído após processamento")
                self.set_result("")
            else:
                # Converte para string com uma entrada por linha para compatibilidade com StringX
                result_str = "\n".join(subdomains)
                self.log_debug(f"Retornando {len(subdomains)} subdomínios únicos")
                self.set_result(result_str)
                
        except ValueError as e:
            self.handle_error(e, "Erro de validação")
        except RequestException as e:
            self.handle_error(e, "Erro de comunicação com crt.sh")
        except ConnectError as e:
            self.handle_error(e, "Falha ao conectar com crt.sh")
        except (ReadTimeout, ConnectTimeout, TimeoutException) as e:
            self.handle_error(e, "Timeout na consulta ao crt.sh")
        except Exception as e:
            self.handle_error(e, "Erro inesperado")
            
    @retry_operation
    def _query_crtsh(self, domain: str) -> List[Dict[str, Any]]:
        """
        Realiza consulta ao crt.sh e retorna os resultados.
        
        Args:
            domain: Domínio para pesquisa
            
        Returns:
            Lista de resultados da consulta ao crt.sh
            
        Raises:
            ValueError: Se o domínio for inválido ou a consulta falhar
            RequestException: Se ocorrer erro na comunicação HTTP
            ConnectionError: Se não for possível estabelecer conexão
            Timeout: Se a requisição exceder o tempo limite
        """
        # Sanitiza o domínio de entrada (remove espaços e caracteres não imprimíveis)
        domain = re.sub(r'[^\x20-\x7E]', '', domain).strip()
        self.log_debug(f"Domínio sanitizado: {domain}")
        
        # Prepara o domínio para consulta (adiciona wildcard se configurado)
        query_domain = f"%.{domain}" if self.options.get('wildcard', True) else domain
        self.log_debug(f"Query de domínio preparada: {query_domain}")
        
        encoded_domain = urllib.parse.quote(query_domain)
        self.log_debug(f"Domínio codificado: {encoded_domain}")
        
        # Constrói a URL final com parâmetros codificados adequadamente
        url = f"https://crt.sh/?q={encoded_domain}&output=json"
        self.log_debug(f"URL de consulta: {url}")
        

        kwargs = {
            'headers' : {
                'User-Agent': UserAgentGenerator.get_desktop_user_agent(),
                'Accept': 'application/json',
                },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }

        self.log_debug("Configurações da requisição preparadas")
        
        try:
            # Realiza a requisição
            async def make_request():
                self.log_debug("Iniciando requisição assíncrona")
                return await self.request.send_request([url], **kwargs)
            
            self.log_debug("Enviando requisição HTTP ao crt.sh")
            response = asyncio.run(make_request())[0]
            self.log_debug(f"Resposta recebida com status code: {response.status_code}")
                
            if response.status_code == 200:
                try:
                    data = response.json()
                    record_count = len(data)
                    self.log_debug(f"Resposta JSON válida recebida com {record_count} registros")
                    
                    if record_count > 0:
                        self.log_debug(f"Primeiros certificados: {data[:2]}")
                    
                    return data
                except json.JSONDecodeError as e:
                    error_msg = f"Resposta recebida não é um JSON válido: {str(e)}"
                    self.log_debug(error_msg)
                    self.log_debug(f"Primeiros 200 caracteres da resposta: {response.text[:200]}...")
                    raise ValueError(error_msg)
            else:
                error_msg = f"Erro na requisição: Status {response.status_code}"
                self.log_debug(error_msg)
                self.log_debug(f"Primeiros 200 caracteres da resposta: {response.text[:200]}...")
                raise RequestException(error_msg)
                
        except (ConnectError, ReadTimeout, ConnectTimeout, TimeoutException) as e:
            self.handle_error(e, "Erro de conexão ou timeout", raise_error=True)
        except Exception as e:
            self.handle_error(e, "Erro ao consultar crt.sh")
            raise ValueError(f"Erro ao consultar crt.sh: {str(e)}")
    
    def _extract_subdomains(self, crt_data: List[Dict[str, Any]], domain: str) -> List[str]:
        """
        Extrai e processa subdomínios dos dados de certificados.
        
        Args:
            crt_data: Dados de certificados do crt.sh
            domain: Domínio base para filtragem
            
        Returns:
            Lista de subdomínios únicos, opcionalmente ordenados
            
        Raises:
            ValueError: Se ocorrer erro no processamento dos dados
        """
        result_domains = []
        self.log_debug(f"Iniciando extração de subdomínios de {len(crt_data)} certificados")
        
        try:
            excluded_wildcards = 0
            total_names = 0
            
            # Configurações para processamento
            exclude_wildcards = self.options.get('exclude_wildcards', True)
            
            for entry in crt_data:
                name_value = entry.get('name_value', '')
                
                if not name_value:
                    continue
                    
                # Processar nomes que podem estar separados por quebras de linha
                if '\n' in name_value:
                    names = name_value.split('\n')
                    self.log_debug(f"Certificado contém {len(names)} nomes alternativos")
                else:
                    names = [name_value]
                
                total_names += len(names)
                
                for domain_name in names:
                    domain_name = domain_name.strip().lower()
                    
                    # Verificar e processar wildcards
                    if '*.' in domain_name:
                        if exclude_wildcards:
                            excluded_wildcards += 1
                            continue
                        else:
                            domain_name = domain_name.replace('*.', '')
                    
                    result_domains.append(domain_name)
            
            self.log_debug(f"Processados {total_names} nomes de domínio")
            if exclude_wildcards:
                self.log_debug(f"Excluídos {excluded_wildcards} subdomínios wildcard")
            
            # Remover duplicados e opcionalmente ordenar
            unique_domains = list(set(result_domains))
            self.log_debug(f"Encontrados {len(unique_domains)} subdomínios únicos")
            
            if self.options.get('sort_unique', True):
                self.log_debug("Ordenando subdomínios alfabeticamente")
                return sorted(unique_domains)
            
            return unique_domains
            
        except Exception as e:
            self.handle_error(e, "Erro ao extrair subdomínios")
            raise ValueError(f"Erro ao extrair subdomínios: {str(e)}")



