"""
Módulo de saída para OpenSearch.

Este módulo implementa funcionalidade para salvar resultados processados
no OpenSearch, permitindo indexação e busca de dados extraídos pelo String-X.
Suporta tanto o cliente de baixo nível quanto o de alto nível da API OpenSearch.
"""
from datetime import datetime
import json
import uuid
from typing import Dict, Any, Optional

from core.format import Format
from core.basemodule import BaseModule

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
            'example': './strx -l domains.txt -st "echo {STRING}" -module "out:opensearch" -pm'
        }
        
        self.options = {
            'host': 'localhost',
            'port': 9200,
            'index': 'strx-data',
            'username': None,
            'password': None,
            'use_ssl': False,
            'verify_certs': False,
            'client_type': 'high',  # 'low' para cliente de baixo nível, 'high' para cliente de alto nível
            'data': str(),
            'debug': False,
            'timeout': 30,
            'retry': 0,
            'retry_delay': 2,
        }
    
    def run(self):
        """
        Executa o salvamento no OpenSearch.
        """
        try:
            data = Format.clear_value(self.options.get('data', ''))
            if not data:
                self.set_result("✗ Erro: Nenhum dado fornecido para enviar ao OpenSearch")
                return
            
            # Verifica se opensearch-py está instalado
            try:
                from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
                from opensearchpy.helpers import bulk
            except ImportError:
                self.set_result("✗ Erro: Biblioteca 'opensearch-py' não está instalada. "
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
                'timeout': self.options.get('timeout', 30)
            }
            
            if auth:
                client_config['http_auth'] = auth
            
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
            
            # Verificar se o índice existe, senão criar
            if not client.indices.exists(index=index):
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
                
                client.indices.create(index=index, body=index_settings)
            
            # Indexar documento com base no tipo de cliente
            if client_type.lower() == 'low':
                # Usando o cliente de baixo nível
                response = client.index(
                    index=index,
                    body=document,
                    id=doc_id,
                    refresh=True
                )
                
                if self.options.get('debug', False):
                    self.set_result(f"OpenSearch resposta (baixo nível): {response}")
                    
                if response['result'] == 'created':
                    self.set_result(f"{data} ✓ Dados indexados com sucesso em OpenSearch (id: {doc_id})")
                else:
                    self.set_result(f"✗ Erro na indexação: {response}")
                
            else:  # client_type == 'high'
                # Usando o cliente de alto nível (bulk API)
                bulk_data = [
                    {
                        "_index": index,
                        "_id": doc_id,
                        "_source": document
                    }
                ]
                
                success, failed = bulk(client, bulk_data, refresh=True)
                
                if self.options.get('debug', False):
                    self.set_result(f"OpenSearch bulk resposta: {success} sucessos, {len(failed)} falhas")
                
                if success and not failed:
                    self.set_result(f"{data} ✓ Dados indexados com sucesso em OpenSearch (id: {doc_id})")
                else:
                    self.set_result(f"✗ Erro na indexação: {failed}")
        
        except Exception as e:
            self.set_result(f"✗ Erro OpenSearch: {str(e)}")