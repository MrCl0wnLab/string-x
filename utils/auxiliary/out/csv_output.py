"""
Módulo de saída CSV.

Este módulo implementa funcionalidade para salvar resultados em formato CSV
para análise em planilhas.
"""
from core.basemodule import BaseModule
import csv
import os
from datetime import datetime

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
            'type': 'output'
        }
        
        self.options = {
            'data': str(),
            'file': 'output.csv',
            'columns': ['timestamp', 'data', 'type'],
            'delimiter': ',',
            'example': './strx -l data.txt -st "echo {STRING}" -module "out:csv_output" -pm'
        }
    
    def run(self):
        """
        Executa a gravação dos dados em formato CSV.
        
        Salva os dados fornecidos em um arquivo CSV com colunas
        configuráveis e timestamps.
        """
        data = self.options.get("data", "").strip()
        if not data:
            return
        
        file_path = self.options.get('file', 'output.csv')
        columns = self.options.get('columns', ['timestamp', 'data', 'type'])
        delimiter = self.options.get('delimiter', ',')
        
        try:
            # Verificar se arquivo existe para header
            file_exists = os.path.exists(file_path)
            
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=delimiter)
                
                # Escrever header se arquivo não existe
                if not file_exists:
                    writer.writerow(columns)
                
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
            
            self.set_result(f"Data saved to {file_path}")
            
        except Exception as e:
            self.set_result(f"Error saving to CSV: {str(e)}")
