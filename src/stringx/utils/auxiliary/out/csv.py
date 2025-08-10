"""
Módulo de saída CSV.

Este módulo implementa funcionalidade para salvar resultados em formato CSV
para análise em planilhas.
"""
import os
import csv
from datetime import datetime

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class CSVOutput(BaseModule):
    """
    Módulo de saída para formato CSV.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'CSV Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Salva resultados em formato CSV',
            'type': 'output',
            'example': './strx -l data.txt -st "echo {STRING}" -module "out:csv" -pm'
        }
        
        self.options = {
            'data': str(),
            'file': 'output.csv',
            'columns': ['timestamp', 'data', 'type'],
            'delimiter': ',',            
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,      # Número de tentativas de requisição
            'retry_delay': None,# Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa a gravação dos dados em formato CSV.
        
        Salva os dados fornecidos em um arquivo CSV com colunas
        configuráveis e timestamps.
        """
        data = Format.clear_value(self.options.get("data", "").strip())
        if not data:
            self.log_debug("[!] Nenhum dado fornecido para exportar")
            return
        
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()

        self.log_debug("[*] Iniciando exportação para CSV")
        
        filename = self.options.get('file', 'output.csv')
        # Obter caminho absoluto do diretório output do projeto
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        output_dir = os.path.join(project_root, 'output')
        
        # Garantir que o diretório output existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Construir caminho completo do arquivo
        file_path = os.path.join(output_dir, filename)
        
        columns = self.options.get('columns', ['timestamp', 'data', 'type'])
        delimiter = self.options.get('delimiter', ',')
        
        self.log_debug(f"[*] Arquivo de saída: {file_path}")
        self.log_debug(f"[*] Colunas: {columns}")
        
        try:
            # Verificar se arquivo existe para header
            file_exists = os.path.exists(file_path)
            
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=delimiter)
                
                # Escrever header se arquivo não existe
                if not file_exists:
                    writer.writerow(columns)
                    self.log_debug("[*] Cabeçalhos CSV escritos")
                
                # Preparar dados
                row_data = []
                for col in columns:
                    if col == 'timestamp':
                        row_data.append(datetime.now().isoformat())
                    elif col == 'data':
                        row_data.append(data)
                    elif col == 'type':
                        row_data.append('string-x-result')
                    else:
                        row_data.append('')
                
                writer.writerow(row_data)
            
            self.log_debug(f"[+] Dados salvos em {file_path}")
            self.set_result(f"CSV: Data saved to {file_path}")
            
        except Exception as e:
            self.handle_error(e, "Erro ao salvar dados em CSV")