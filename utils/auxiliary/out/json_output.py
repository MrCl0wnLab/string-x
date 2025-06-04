"""
Módulo de saída JSON.

Este módulo implementa funcionalidade para salvar resultados em formato JSON
estruturado, útil para integração com outras ferramentas.
"""
from core.basemodule import BaseModule
import json
import os
from datetime import datetime
from core.format import Format

class JSONOutput(BaseModule):
    """
    Módulo de saída para formato JSON.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'JSON Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Salva resultados em formato JSON estruturado',
            'type': 'output'
        }
        
        self.options = {
            'data': str(),
            'file': 'output.json',
            'append': True,
            'pretty': True,
            'example': './strx -l data.txt -st "echo {STRING}" -module "out:json_output" -pm'
        }
    
    def run(self):
        """
        Executa a gravação dos dados em formato JSON.
        
        Salva os dados fornecidos em um arquivo JSON com timestamp
        e metadados adicionais.
        """
        data = Format.clear_value(self.options.get("data", "").strip())
        if not data:
            return
        
        file_path = self.options.get('file', 'output.json')
        append = self.options.get('append', True)
        pretty = self.options.get('pretty', True)
        
        # Estrutura do resultado
        result_entry = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'source': 'string-x'
        }
        
        try:
            # Carregar dados existentes se append=True
            if append and os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                        if not isinstance(existing_data, list):
                            existing_data = [existing_data]
                except:
                    existing_data = []
            else:
                existing_data = []
            
            # Adicionar novo resultado
            existing_data.append(result_entry)
            
            # Salvar arquivo
            with open(file_path, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(existing_data, f, ensure_ascii=False)
            
            self.set_result(f"Data saved to {file_path}")
            
        except Exception as e:
            self.set_result(f"Error saving to JSON: {str(e)}")
