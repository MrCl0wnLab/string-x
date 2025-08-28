"""
Módulo de saída para MySQL.

Este módulo implementa funcionalidade para salvar resultados processados
em banco de dados MySQL, permitindo armazenamento estruturado e consultas
avançadas dos dados extraídos pelo String-X.
"""
from datetime import datetime

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class MySqlOutput(BaseModule):
    """
    Módulo de saída para banco de dados MySQL.
    
    Esta classe permite salvar dados processados em banco MySQL,
    oferecendo escalabilidade e capacidades avançadas de consulta.
    
    TODO: Implementar funcionalidade de conexão e inserção de dados.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de saída MySQL.
        """
        super().__init__()
        
        self.meta = {
            'name': 'MySQL Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Salva dados em banco MySQL',
            'type': 'output'
        ,
            'example': './strx -l data.txt -st "echo {STRING}" -module "con:mysql" -pm'
        }
        
        self.options = {
            'host': self.setting.STRX_MYSQL_HOST,
            'port': self.setting.STRX_MYSQL_PORT,
            'database': self.setting.STRX_MYSQL_DATABASE,
            'username': self.setting.STRX_MYSQL_USER,
            'password': self.setting.STRX_MYSQL_PASS,
            'table': 'results',
            'source': "string-x",  # Origem dos dados (opcional)
            'metadata': str(),     # Metadados em formato JSON (opcional)
            'debug': False,        # Modo de debug para mostrar informações detalhadas
            'retry': 0,            # Número de tentativas de requisição
            'retry_delay': None,   # Atraso entre tentativas de requisição
            'data': str(),
        }
    
    def run(self):
        """
        Executa salvamento no MySQL.
        """
        try:
            import mysql.connector
            
            data = Format.clear_value(self.options.get('data', ''))
            if not data:
                self.log_debug("[x] Nenhum dado fornecido para salvar no MySQL.")
                return
            
            # Only clear results if auto_clear is enabled (default behavior)
            if self._auto_clear_results:
                self._result[self._get_cls_name()].clear()

            # Configurações de conexão
            config = {
                'host': self.options.get('host', 'localhost'),
                'port': self.options.get('port', 3306),
                'database': self.options.get('database', 'strx_db'),
                'user': self.options.get('username', 'strx_user'),
                'password': self.options.get('password', '')
            }
            
            if not config['password']:
                self.set_result("Erro: Senha MySQL não fornecida")
                return
            
            table_name = self.options.get('table', 'results')
            
            # Conectar ao MySQL
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    module_type VARCHAR(50) DEFAULT 'unknown',
                    processed_at DATETIME,
                    source VARCHAR(255),
                    metadata TEXT
                )
            ''')
            
            # Inserir dados
            timestamp = datetime.now()
            source = self.options.get('source', '')
            metadata = self.options.get('metadata', '')
            
            # Inserir com campos adicionais se fornecidos
            if source or metadata:
                cursor.execute(f'''
                    INSERT INTO {table_name} (data, processed_at, module_type, source, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (data, timestamp, self.meta.get('type', 'output'), source, metadata))
            else:
                cursor.execute(f'''
                    INSERT INTO {table_name} (data, processed_at, module_type)
                    VALUES (%s, %s, %s)
                ''', (data, timestamp, self.meta.get('type', 'output')))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            self.set_result(f"✓ Dados salvos em MySQL: {config['database']}.{table_name}")
            
        except ImportError:
            self.handle_error(ImportError("mysql-connector-python não instalado"), "Erro de importação MySQL")
        except Exception as e:
            self.handle_error(e, "Erro ao salvar dados no MySQL")