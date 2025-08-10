"""
Módulo de saída para SQLite.

Este módulo implementa funcionalidade para salvar resultados processados
em banco de dados SQLite, permitindo armazenamento estruturado de dados
extraídos pelo String-X.
"""
import sqlite3
from datetime import datetime

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class SqliteOutput(BaseModule):
    """
    Módulo de saída para banco de dados SQLite.
    
    Esta classe permite salvar dados processados em banco SQLite,
    fornecendo persistência e capacidade de consulta para os resultados.
    
    TODO: Implementar funcionalidade de conexão e inserção de dados.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de saída SQLite.
        """
        super().__init__()
        
        self.meta = {
            'name': 'SQLite Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Salva dados em banco SQLite',
            'type': 'output'
        ,
            'example': './strx -l domains.txt -st "echo {STRING}" -module "con:sqlite" -pm'
        }
        
        self.options = {
            'database': self.setting.STRX_SQLITE_DATABASE,
            'table': 'results',
            'data': str(),
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'timeout': self.setting.STRX_SQLITE_TIMEOUT,  # Tempo limite para operações de banco de dados
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa salvamento no SQLite.
        """
        try:
            data = Format.clear_value(self.options.get('data', ''))
            if not data:
                self.log_debug("[!] Nenhum dado fornecido para salvar no SQLite")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            database_path = self.options.get('database', 'strx_results.db')
            table_name = self.options.get('table', 'results')
            
            # Conectar ao banco SQLite
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    module_type TEXT DEFAULT 'unknown',
                    processed_at TEXT
                )
            ''')
            
            # Inserir dados
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f'''
                INSERT INTO {table_name} (data, processed_at, module_type)
                VALUES (?, ?, ?)
            ''', (data, timestamp, self.meta.get('type', 'output')))
            
            conn.commit()
            conn.close()
            
            self.set_result(f"{data} ✓ Dados salvos em SQLite: {database_path}")
            
        except ImportError:
            self.handle_error(ImportError("sqlite3 não disponível"), "Erro de importação SQLite")
        except Exception as e:
            self.handle_error(e, "Erro ao salvar dados no SQLite")