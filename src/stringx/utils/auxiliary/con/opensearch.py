from datetime import datetime
import json
import uuid
import time
import sys
from typing import Dict, Any, Optional
import socket
import httpx
import warnings
import urllib3

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class OpenSearchOutput(BaseModule):
    """
    Módulo de saída para OpenSearch.
    
    Esta classe permite salvar dados processados no OpenSearch,
    fornecendo persistência, indexação e capacidade de busca para os resultados.
    
    Suporta as seguintes opções de configuração:
    - host: Host do OpenSearch (padrão: localhost)
    - port: Porta do OpenSearch (padrão: 9200)
    - index: Nome do índice para armazenar os dados (padrão: strx-data)
    - username: Nome de usuário para autenticação (opcional)
    - password: Senha para autenticação (opcional)
    - use_ssl: Usar conexão SSL (padrão: False)
    - verify_certs: Verificar certificados SSL (padrão: False)
    - client_type: Tipo de cliente a ser usado ('low' ou 'high') (padrão: 'high')
    - data: Dados a serem enviados (obrigatório)
    - suppress_warnings: Suprimir avisos de SSL inseguro (padrão: True)
    """
    
    def __init__(self):
        """
        Inicializa o módulo de saída OpenSearch.
        """
        super().__init__()
        
        self.meta = {
            'name': 'OpenSearch Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Salva dados no OpenSearch para indexação e busca',
            'type': 'output',
            'example': './strx -l domains.txt -st "echo {STRING}" -module "con:opensearch" -pm'
        }
        
        self.options = {
            'host': self.setting.STRX_OPENSEARCH_HOST,
            'port': self.setting.STRX_OPENSEARCH_PORT,
            'index': self.setting.STRX_OPENSEARCH_INDEX,
            'username': self.setting.STRX_OPENSEARCH_USERNAME,
            'password': self.setting.STRX_OPENSEARCH_PASS,
            'use_ssl': self.setting.STRX_OPENSEARCH_USE_SSL,
            'verify_certs': self.setting.STRX_OPENSEARCH_VERIFY_CERTS,
            'timeout': self.setting.STRX_OPENSEARCH_TIMEOUT,
            'retry': self.setting.STRX_OPENSEARCH_RETRY,
            'retry_delay': self.setting.STRX_OPENSEARCH_RETRY_DELAY,
            'suppress_warnings': True,  # Opção para suprimir avisos de SSL
            'data': str(),
            'debug': False,
            'client_type': 'high',  # 'low' para cliente de baixo nível, 'high' para cliente de alto nível

        }
    
    def check_server_availability(self, host, port, timeout=30):
        """
        Verifica se o servidor está disponível antes de tentar conectar
        """
        try:
            # Primeiro tenta um socket simples para verificar se o servidor está online
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result != 0:
                return False, f"Não foi possível conectar ao servidor {host}:{port}. O servidor está rodando?"
            
            # Se o socket conectou, tenta uma solicitação HTTP básica
            protocol = "https" if self.options.get('use_ssl') else "http"
            url = f"{protocol}://{host}:{port}"
            
            auth = None
            if self.options.get('username') and self.options.get('password'):
                auth = (self.options.get('username'), self.options.get('password'))
            
            # Suprimir avisos apenas durante esta solicitação
            with warnings.catch_warnings():
                if self.options.get('suppress_warnings', True):
                    warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)
                
                # Criando cliente httpx com configurações específicas
                client = httpx.Client(verify=self.options.get('verify_certs', False), timeout=timeout)
                response = client.get(
                    url, 
                    auth=auth
                )
            
            if response.status_code >= 200 and response.status_code < 300:
                if self.options.get('debug', False):
                    self.set_result(f"OpenSearch está rodando: {response.text}")
                # Verificar se é realmente um servidor OpenSearch/Elasticsearch
                try:
                    resp_data = response.json()
                    if not (resp_data.get("version") and resp_data.get("name")):
                        self.set_result(f"Aviso: O servidor em {url} pode não ser um OpenSearch/Elasticsearch válido")
                except:
                    pass
                    
                return True, "Servidor disponível"
            else:
                error_detail = ""
                try:
                    error_detail = f" - {response.text}"
                except:
                    pass
                return False, f"Servidor respondeu com código de status {response.status_code}{error_detail}"
                
        except httpx.SSLError:
            return False, "Erro de SSL. Tente configurar use_ssl=True e verify_certs=False"
        except httpx.ConnectError:
            return False, f"Não foi possível estabelecer conexão com {host}:{port}"
        except httpx.TimeoutException:
            return False, f"Timeout ao conectar a {host}:{port}"
        except Exception as e:
            self.handle_error(e, "Erro ao verificar disponibilidade do OpenSearch")
            return False, f"Erro ao verificar disponibilidade: {str(e)}"
    
    def run(self):
        """
        Executa o salvamento no OpenSearch.
        """
        try:
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()
            # Suprimir avisos se configurado para isso
            if self.options.get('suppress_warnings', True):
                # Suprimir avisos de SSL inseguro do urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                # Suprimir avisos do OpenSearch
                warnings.filterwarnings('ignore', message='Connecting to .* using SSL with verify_certs=False is insecure')
            
            data = Format.clear_value(self.options.get('data', ''))
            if not data:
                self.log_debug("[x] Erro: Nenhum dado fornecido para enviar ao OpenSearch")
                return
            
            # Verifica se as bibliotecas necessárias estão instaladas
            try:
                from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
                from opensearchpy.helpers import bulk
                from opensearchpy.exceptions import ConnectionError as OSConnectionError
                from opensearchpy.exceptions import AuthenticationException, AuthorizationException
                
                # Verificar se httpx está instalado
                if 'httpx' not in sys.modules:
                    import httpx
            except ImportError as e:
                if "httpx" in str(e):
                    self.log_debug("[x] Erro: Biblioteca 'httpx' não está instalada. "
                                    "Instale com: pip install httpx")
                else:
                    self.log_debug("[x] Erro: Biblioteca 'opensearch-py' não está instalada. "
                                    "Instale com: pip install opensearch-py")
                return
            
            # Parâmetros de conexão
            host = self.options.get('host', 'localhost')
            port = int(self.options.get('port', 9200))
            index = self.options.get('index', 'strx-data')
            username = self.options.get('username')
            password = self.options.get('password')
            use_ssl = self.options.get('use_ssl', False)
            verify_certs = self.options.get('verify_certs', False)
            client_type = self.options.get('client_type', 'high')
            timeout = self.options.get('timeout', 60)
            retry = self.options.get('retry', 3)
            retry_delay = self.options.get('retry_delay', 5)
            
            # Verificar disponibilidade do servidor antes de tentar conectar
            """
            available, message = self.check_server_availability(host, port)
            if not available:
                self.set_result(f"Erro OpenSearch: {message}")
                return
            """
            
            # Configuração de autenticação
            auth = None
            if username and password:
                auth = (username, password)
            
            # Criação de configuração do cliente
            client_config = {
                'hosts': [{'host': host, 'port': port}],
                'use_ssl': use_ssl,
                'verify_certs': verify_certs,
                'connection_class': RequestsHttpConnection,
                'timeout': timeout,
                'retry_on_timeout': True,
                'max_retries': retry,
                # Silenciar avisos do OpenSearch
                'ssl_show_warn': not self.options.get('suppress_warnings', True)
            }
            
            if auth:
                client_config['http_auth'] = auth
            
            if self.options.get('debug', False):
                self.set_result(f"Configuração OpenSearch: {client_config}")
            
            # Inicializar o cliente OpenSearch
            client = OpenSearch(**client_config)
            
            # Preparar documento para indexação
            timestamp = datetime.now().isoformat()
            doc_id = str(uuid.uuid4())
            
            # Tentar analisar como JSON se possível
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                # Se não for JSON válido, tratar como texto
                json_data = {"content": data}
            
            # Adicionar metadados
            document = {
                "timestamp": timestamp,
                "source": "string-x",
                "module_type": "output",
                "processed_at": timestamp,
                "data": json_data
            }
            
            # Loop de tentativas para verificar se o índice existe
            index_exists = False
            for attempt in range(retry + 1):
                try:
                    index_exists = client.indices.exists(index=index)
                    break
                except Exception as e:
                    self.handle_error(e, "Erro ao verificar índice OpenSearch")
                    if attempt < retry:
                        self.log_debug(f"[!] Tentativa {attempt+1} falhou ao verificar índice: {str(e)}")
                        time.sleep(retry_delay)
                    else:
                        raise e
            
            # Verificar se o índice existe, senão criar
            if not index_exists:
                # Configuração básica do índice
                index_settings = {
                    "settings": {
                        "index": {
                            "number_of_shards": 1,
                            "number_of_replicas": 1
                        }
                    },
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "source": {"type": "keyword"},
                            "module_type": {"type": "keyword"},
                            "processed_at": {"type": "date"},
                            "data": {"type": "object", "dynamic": True}
                        }
                    }
                }
                
                # Tentar verificar novamente se o índice já existe (pode ter sido criado por outro processo)
                try:
                    double_check = client.indices.exists(index=index)
                    if double_check:
                        self.log_debug(f"[+] Índice {index} já existe (verificação secundária)")
                        index_exists = True
                except Exception as e:
                    self.handle_error(e, "Erro na verificação secundária do índice")
                    pass
                    
                # Se ainda não existe, tentar criar
                if not index_exists:
                    try:
                        create_response = client.indices.create(index=index, body=index_settings)
                        self.log_debug(f"[+] Índice {index} criado com sucesso: {create_response}")
                    except Exception as e:
                        self.handle_error(e, "Erro ao criar índice no OpenSearch")
                        error_message = str(e)
                        
                        # Se o índice já existe, não é um erro real
                        if "resource_already_exists_exception" in error_message or "already exists" in error_message:
                            self.log_debug(f"[+] Índice {index} já existe")
                        else:
                            self.log_debug(f"[x] Erro ao criar índice: {error_message}")
                            if self.options.get('debug', False):
                                # Tentar obter mais detalhes do erro
                                try:
                                    # Verificar se há detalhes adicionais de erro
                                    if hasattr(e, 'info') and isinstance(e.info, dict):
                                        self.log_debug(f"[*] Detalhes do erro: {e.info}")
                                except:
                                    pass
                            # Apenas log do erro, mas continuar tentando indexar no índice
            
            # Indexar documento com base no tipo de cliente
            if client_type.lower() == 'low':
                # Usando o cliente de baixo nível com retries
                for attempt in range(retry + 1):
                    try:
                        response = client.index(
                            index=index,
                            body=document,
                            id=doc_id,
                            refresh=True
                        )
                        
                        if self.options.get('debug', False):
                            self.set_result(f"OpenSearch resposta (baixo nível): {response}")
                            
                        if response['result'] == 'created':
                            self.set_result(f"{doc_id}, {data}")
                        else:
                            self.set_result(f"Erro na indexação: {response}")
                        break
                    except Exception as e:
                        self.handle_error(e, "Erro ao indexar documento no OpenSearch")
                        if attempt < retry:
                            time.sleep(retry_delay)
                        else:
                            raise e
                
            else:  # client_type == 'high'
                # Usando o cliente de alto nível (bulk API) com retries
                bulk_data = [
                    {
                        "_index": index,
                        "_id": doc_id,
                        "_source": document
                    }
                ]
                
                for attempt in range(retry + 1):
                    try:
                        success, failed = bulk(client, bulk_data, refresh=True)
                        
                        if self.options.get('debug', False):
                            self.log_debug(f"[+] OpenSearch bulk resposta: {success} sucessos, {len(failed)} falhas")
                        
                        if success and not failed:
                            self.log_debug(f"[*] {doc_id}, {data}")
                        else:
                            self.log_debug(f"[x] Erro na indexação: {failed}")
                        break
                    except Exception as e:
                        self.handle_error(e, "Erro ao indexar em bulk no OpenSearch")
                        if attempt < retry:
                            time.sleep(retry_delay)
                        else:
                            raise e
        
        except AuthenticationException:
            self.handle_error(AuthenticationException("Falha de autenticação"), "Erro OpenSearch de autenticação")
        except AuthorizationException:
            self.handle_error(AuthorizationException("Falha de autorização"), "Erro OpenSearch de autorização")
        except OSConnectionError as e:
            self.handle_error(e, "Erro OpenSearch de conexão")
        except Exception as e:
            self.handle_error(e, "Erro geral do OpenSearch")