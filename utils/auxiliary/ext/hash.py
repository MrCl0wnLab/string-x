"""
Módulo extrator de hashes.

Este módulo implementa funcionalidade para extrair diferentes tipos de hashes
de textos usando expressões regulares.
"""
import re
from core.basemodule import BaseModule

class HashExtractor(BaseModule):
    """
    Módulo para extração de hashes usando regex.
    
    Suporta MD5, SHA1, SHA256, SHA512 e outros formatos comuns.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'Hash Extractor',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Extrai hashes MD5, SHA1, SHA256, SHA512',
            'type': 'extractor'
        ,
            'example': './strx -l password_dump.txt -st "echo {STRING}" -module "ext:hash" -pm'
        }
        
        self.options = {
            'data': str(),
            'hash_types': ['md5', 'sha1', 'sha256', 'sha512', 'all'],            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa o processo de extração de hashes.
        
        Utiliza os dados fornecidos e busca por diferentes tipos de hashes
        usando padrões regex específicos para cada tipo.
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        
        if not (target_value := self.options.get("data")):
            return
            
        patterns = {
            'md5': r'\b[a-fA-F0-9]{32}\b',
            'sha1': r'\b[a-fA-F0-9]{40}\b', 
            'sha256': r'\b[a-fA-F0-9]{64}\b',
            'sha512': r'\b[a-fA-F0-9]{128}\b'
        }
        
        hash_types = self.options.get('hash_types', ['all'])
        
        if 'all' in hash_types:
            hash_types = list(patterns.keys())
            
        for hash_type in hash_types:
            if hash_type in patterns:
                regex = re.compile(patterns[hash_type], re.IGNORECASE)
                matches = set(re.findall(regex, target_value))
                for match in matches:
                    self.set_result(f"{hash_type.upper()}, {match}")
