"""
Módulo extrator de hashes.

Este módulo implementa funcionalidade para extrair diferentes tipos de hashes
de textos usando expressões regulares.
"""
import re
from stringx.core.basemodule import BaseModule

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
            'hash_types': ['md5', 'sha1', 'sha256', 'sha512', 'all'],            
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa o processo de extração de hashes.
        
        Utiliza os dados fornecidos e busca por diferentes tipos de hashes
        usando padrões regex específicos para cada tipo.
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
            
        self.log_debug("[*] Iniciando extração de hashes")
        
        try:
            if not (target_value := self.options.get("data")):
                self.log_debug("[X] Dados não fornecidos")
                return
                
            self.log_debug(f"[*] Processando {len(target_value)} caracteres de dados")
               
            patterns = {
                'md5': r'\b[a-fA-F0-9]{32}\b',
                'sha1': r'\b[a-fA-F0-9]{40}\b', 
                'sha256': r'\b[a-fA-F0-9]{64}\b',
                'sha512': r'\b[a-fA-F0-9]{128}\b'
            }
            
            hash_types = self.options.get('hash_types', ['all'])
            
            if 'all' in hash_types:
                hash_types = list(patterns.keys())
            
            self.log_debug(f"[*] Tipos de hash procurados: {', '.join(hash_types)}")
            
            results = []    
            for hash_type in hash_types:
                if hash_type in patterns:
                    regex = re.compile(patterns[hash_type], re.IGNORECASE)
                    matches = list(set(re.findall(regex, target_value)))
                    self.log_debug(f"[+] {hash_type.upper()}: {len(matches)} hashes encontrados")
                    
                    for match in matches:
                        results.append({
                            'type': hash_type.upper(),
                            'value': match
                        })
                        self.log_debug(f"   [*] {hash_type.upper()}: {match}")
            
            if results:
                self.log_debug(f"[*] Total de hashes coletados: {len(results)}")
                # Usar novo método estruturado
                self.set_result_structured(results)
            else:
                self.log_debug("[!] Nenhum hash encontrado")
                
        except Exception as e:
            self.handle_error(e, "Erro na extração de hashes")
