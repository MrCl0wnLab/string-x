"""
Módulo de saída XML.

Este módulo implementa funcionalidade para salvar resultados em formato XML
estruturado para integração com sistemas que necessitam deste formato.
"""
import os
from datetime import datetime
import xml.etree.ElementTree as ET

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class XMLOutput(BaseModule):
    """
    Módulo de saída para formato XML.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'XML Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Salva resultados em formato XML estruturado',
            'type': 'output'
        ,
            'example': './strx -l data.txt -st "echo {STRING}" -module "out:xml" -pm'
        }
        
        self.options = {
            'data': str(),
            'file': 'output.xml',
            'root_element': 'stringx_results',
            'item_element': 'result',            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa a gravação dos dados em formato XML.
        
        Salva os dados fornecidos em um arquivo XML com estrutura
        hierárquica e metadados.
        """
        data = Format.clear_value(self.options.get("data", "").strip())
        if not data:
            return
        
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()

        file_path = self.options.get('file', 'output.xml')
        root_name = self.options.get('root_element', 'stringx_results')
        item_name = self.options.get('item_element', 'result')
        
        try:
            # Carregar XML existente ou criar novo
            if os.path.exists(file_path):
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                except:
                    root = ET.Element(root_name)
                    tree = ET.ElementTree(root)
            else:
                root = ET.Element(root_name)
                tree = ET.ElementTree(root)
            
            # Criar novo elemento resultado
            result_elem = ET.SubElement(root, item_name)
            
            # Adicionar timestamp
            timestamp_elem = ET.SubElement(result_elem, 'timestamp')
            timestamp_elem.text = datetime.now().isoformat()
            
            # Adicionar dados
            data_elem = ET.SubElement(result_elem, 'data')
            data_elem.text = data
            
            # Adicionar fonte
            source_elem = ET.SubElement(result_elem, 'source')
            source_elem.text = 'string-x'
            
            # Salvar arquivo
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            
            self.log_debug(f"[+] Data saved to {file_path}")
            
        except Exception as e:
            self.handle_error(e, "Erro ao salvar dados em XML")
