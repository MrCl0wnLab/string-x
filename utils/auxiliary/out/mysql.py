"""
Módulo de saída para MySQL.

Este módulo implementa funcionalidade para salvar resultados processados
em banco de dados MySQL, permitindo armazenamento estruturado e consultas
avançadas dos dados extraídos pelo String-X.
"""
from datetime import datetime

from core.format import Format
from core.basemodule import BaseModule

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
            'example': './strx -l data.txt -st "echo {STRING}" -module "out:mysql" -pm'
        }
        
        self.options = {
            'host': 'localhost',
            'port': 3306,
            'database': 'strx_results',
            'username': str(),
            'password': str(),
            'table': 'results',
            'data': str(),            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': 1,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa salvamento no MySQL.
        """
        try:
            import mysql.connector
            
            data = Format.clear_value(self.options.get('data', ''))
            if not data:
                return
            
            # Configurações de conexão
            config = {
                'host': self.options.get('host', 'localhost'),
                'port': self.options.get('port', 3306),
                'database': self.options.get('database', 'strx_results'),
                'user': self.options.get('username', ''),
                'password': self.options.get('password', '')
            }
            
            if not config['user']:
                self.set_result("✗ Erro: Username MySQL não fornecido")
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
                    processed_at DATETIME
                )
            ''')
            
            # Inserir dados
            timestamp = datetime.now()
            cursor.execute(f'''
                INSERT INTO {table_name} (data, processed_at, module_type)
                VALUES (%s, %s, %s)
            ''', (data, timestamp, self.meta.get('type', 'output')))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            self.set_result(f"✓ Dados salvos em MySQL: {config['database']}.{table_name}")
            
        except ImportError:
            self.set_result("✗ Erro: mysql-connector-python não instalado (pip install mysql-connector-python)")
        except Exception as e:
            self.set_result(f"✗ Erro MySQL: {str(e)}")