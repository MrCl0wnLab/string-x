"""
Módulo de conexão MongoDB.

Este módulo implementa funcionalidade para armazenar e recuperar dados
do MongoDB, facilitando persistência de dados do String-X.
"""
import json
from datetime import datetime
from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class MongoDBConnection(BaseModule):
    """
    Módulo de conexão MongoDB.
    
    Esta classe permite armazenar dados processados no MongoDB
    com suporte a coleções customizadas e indexação.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de conexão MongoDB.
        """
        super().__init__()
        
        self.meta = {
            'name': 'MongoDB Connection',
             "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Armazena dados no MongoDB',
            'type': 'database',
            'example': './strx -l results.txt -module "con:mongodb" -pm'
        }
        
        self.options = {
            'host': self.setting.STRX_MONGODB_HOST,
            'port': self.setting.STRX_MONGODB_PORT,
            'database': self.setting.STRX_MONGODB_DATABASE,
            'username': self.setting.STRX_MONGODB_USER,
            'password': self.setting.STRX_MONGODB_PASS,
            'collection': 'results',
            'data': str(),
            'operation': 'insert',      # insert, find, update, delete
            'query': '{}',             # Query JSON para operações
            'upsert': False,           # Upsert para updates
            'create_index': True,      # Criar índices automaticamente
            'debug': False
        }
    
    def run(self):
        """
        Executa operação MongoDB.
        """
        try:
            # Verificar se pymongo está disponível
            try:
                import pymongo
                from pymongo import MongoClient
            except ImportError:
                self.log_debug("[x] Erro: Biblioteca 'pymongo' não está instalada")
                self.log_debug("       Execute: pip install pymongo")
                return
            
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            
            data = Format.clear_value(self.options.get('data', ''))
            operation = self.options.get('operation', 'insert')
            
            self.log_debug("[*] Iniciando operação MongoDB")
            
            # Conectar ao MongoDB
            client = self._connect_mongodb()
            if not client:
                return
            
            # Selecionar database e collection
            db_name = self.options.get('database', 'stringx')
            collection_name = self.options.get('collection', 'results')
            
            db = client[db_name]
            collection = db[collection_name]
            
            self.log_debug(f"[*] Conectado: {db_name}.{collection_name}")
            
            # Criar índices se solicitado
            if self.options.get('create_index', True):
                self._create_indexes(collection)
            
            # Executar operação
            if operation == 'insert':
                self._insert_data(collection, data)
            elif operation == 'find':
                self._find_data(collection)
            elif operation == 'update':
                self._update_data(collection, data)
            elif operation == 'delete':
                self._delete_data(collection)
            else:
                self.log_debug(f"[x] Operação desconhecida: {operation}")
            
            # Fechar conexão
            client.close()
            self.log_debug("[*] Conexão MongoDB fechada")
            
        except Exception as e:
            self.handle_error(e, "Erro na operação MongoDB")
    
    def _connect_mongodb(self):
        """
        Estabelece conexão com MongoDB.
        """
        try:
            from pymongo import MongoClient
            
            host = self.options.get('host', 'localhost')
            port = int(self.options.get('port', 27017))
            username = self.options.get('username', '')
            password = self.options.get('password', '')
            
            self.log_debug(f"[*] Conectando ao MongoDB: {host}:{port}")
            
            # Construir URI de conexão
            if username and password:
                uri = f"mongodb://{username}:{password}@{host}:{port}/"
                self.log_debug("[*] Usando autenticação")
            else:
                uri = f"mongodb://{host}:{port}/"
                self.log_debug("[*] Sem autenticação")
            
            # Conectar
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            
            # Testar conexão
            client.admin.command('ping')
            self.log_debug("[+] Conexão MongoDB estabelecida")
            
            return client
            
        except Exception as e:
            self.log_debug(f"[x] Erro na conexão MongoDB: {e}")
            return None
    
    def _create_indexes(self, collection):
        """
        Cria índices úteis na coleção.
        """
        try:
            # Índice por timestamp
            collection.create_index("timestamp")
            # Índice por tipo de dados
            collection.create_index("data_type")
            # Índice composto
            collection.create_index([("timestamp", -1), ("data_type", 1)])
            
            self.log_debug("[+] Índices criados")
            
        except Exception as e:
            self.log_debug(f"[!] Erro ao criar índices: {e}")
    
    def _insert_data(self, collection, data):
        """
        Insere dados na coleção.
        """
        if not data:
            self.log_debug("[!] Nenhum dado fornecido para inserção")
            return
        
        try:
            # Preparar documento
            document = {
                "data": data,
                "timestamp": datetime.utcnow(),
                "data_type": "string-x-result",
                "source": "string-x",
                "length": len(data)
            }
            
            # Inserir documento
            result = collection.insert_one(document)
            
            if result.inserted_id:
                self.log_debug(f"[+] Documento inserido: {result.inserted_id}")
                
                response = f"MongoDB Insert Success\\n"
                response += f"Document ID: {result.inserted_id}\\n"
                response += f"Data length: {len(data)} characters"
                
                self.set_result(response)
            else:
                self.log_debug("[x] Falha na inserção")
                
        except Exception as e:
            self.log_debug(f"[x] Erro na inserção: {e}")
    
    def _find_data(self, collection):
        """
        Busca dados na coleção.
        """
        try:
            query_str = self.options.get('query', '{}')
            
            # Parsear query JSON
            try:
                query = json.loads(query_str)
            except json.JSONDecodeError:
                self.log_debug(f"[x] Query JSON inválida: {query_str}")
                return
            
            self.log_debug(f"[*] Executando query: {query}")
            
            # Executar busca
            cursor = collection.find(query).limit(100)  # Limitar resultados
            documents = list(cursor)
            
            if documents:
                self.log_debug(f"[+] Encontrados {len(documents)} documentos")
                
                results = []
                for doc in documents:
                    # Remover _id se presente (não é JSON serializable)
                    if '_id' in doc:
                        doc['_id'] = str(doc['_id'])
                    
                    results.append(doc)
                
                # Formatear resultado
                response = f"MongoDB Find Results ({len(results)} documents)\\n\\n"
                response += json.dumps(results, indent=2, default=str)
                
                self.set_result(response)
            else:
                self.log_debug("[!] Nenhum documento encontrado")
                self.set_result("MongoDB Find: No documents found")
                
        except Exception as e:
            self.log_debug(f"[x] Erro na busca: {e}")
    
    def _update_data(self, collection, data):
        """
        Atualiza dados na coleção.
        """
        try:
            query_str = self.options.get('query', '{}')
            upsert = self.options.get('upsert', False)
            
            # Parsear query JSON
            try:
                query = json.loads(query_str)
            except json.JSONDecodeError:
                self.log_debug(f"[x] Query JSON inválida: {query_str}")
                return
            
            # Preparar update
            update_doc = {
                "$set": {
                    "data": data,
                    "updated_at": datetime.utcnow(),
                    "length": len(data)
                }
            }
            
            # Executar update
            result = collection.update_many(query, update_doc, upsert=upsert)
            
            self.log_debug(f"[+] Documentos atualizados: {result.modified_count}")
            
            if upsert and result.upserted_id:
                self.log_debug(f"[+] Documento criado via upsert: {result.upserted_id}")
            
            response = f"MongoDB Update Success\\n"
            response += f"Modified: {result.modified_count} documents\\n"
            if upsert and result.upserted_id:
                response += f"Upserted: {result.upserted_id}"
            
            self.set_result(response)
            
        except Exception as e:
            self.log_debug(f"[x] Erro no update: {e}")
    
    def _delete_data(self, collection):
        """
        Remove dados da coleção.
        """
        try:
            query_str = self.options.get('query', '{}')
            
            # Parsear query JSON
            try:
                query = json.loads(query_str)
            except json.JSONDecodeError:
                self.log_debug(f"[x] Query JSON inválida: {query_str}")
                return
            
            # Confirmar se query não está vazia (segurança)
            if not query:
                self.log_debug("[x] Query vazia - operação cancelada por segurança")
                return
            
            # Executar delete
            result = collection.delete_many(query)
            
            self.log_debug(f"[+] Documentos removidos: {result.deleted_count}")
            
            response = f"MongoDB Delete Success\\n"
            response += f"Deleted: {result.deleted_count} documents"
            
            self.set_result(response)
            
        except Exception as e:
            self.log_debug(f"[x] Erro na remoção: {e}")
