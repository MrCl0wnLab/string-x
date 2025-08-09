"""
Módulo extrator de hashes de arquivos.

Este módulo implementa funcionalidade para extrair diferentes tipos de hashes
de arquivos usando algoritmos criptográficos padrão.
"""
import os
import hashlib
from pathlib import Path
from stringx.core.basemodule import BaseModule

class FileHashExtractor(BaseModule):
    """
    Módulo para extração de hashes de arquivos.
    
    Calcula simultaneamente MD5, SHA-1, SHA256 e SHA512 de arquivos
    de forma eficiente, lendo o arquivo apenas uma vez.
    """
    
    def __init__(self):
        """
        Inicializa o módulo extrator de hashes de arquivos.
        """
        super().__init__()
        
        self.meta = {
            'name': 'File Hash Extractor',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Extrai hashes MD5, SHA-1, SHA256, SHA512 de arquivos',
            'type': 'extractor',
            'example': './strx -l arquivos.txt -st "echo {STRING}" -module "ext:file_hash" -pm'
        }
        
        self.options = {
            'data': str(),              # Caminho do arquivo
            'hash_types': ['md5', 'sha1', 'sha256', 'sha512'],  # Tipos de hash a calcular
            'file_size_limit': 500,     # Limite em MB para processamento (0 = sem limite)
            'buffer_size': 65536,       # Tamanho do buffer para leitura (64KB)
            'debug': False,             # Modo de debug
            'retry': 0,                 # Número de tentativas
            'retry_delay': None,        # Atraso entre tentativas
        }
    
    def run(self):
        """
        Executa o processo de extração de hashes do arquivo.
        
        Lê o arquivo uma única vez e calcula todos os hashes simultaneamente
        para maior eficiência.
        """
        # Limpar resultados anteriores
        self._result[self._get_cls_name()].clear()
        
        file_path = self.options.get("data", "").strip()
        if not file_path:
            if self.options.get('debug', False):
                self.log_debug("Nenhum caminho de arquivo especificado")
            return

        try:
            # Verificar se o arquivo existe
            if not os.path.exists(file_path):
                if self.options.get('debug', False):
                    self.log_debug(f"Arquivo não encontrado: {file_path}")
                return

            # Verificar se é um arquivo (não diretório)
            if not os.path.isfile(file_path):
                if self.options.get('debug', False):
                    self.log_debug(f"Caminho não é um arquivo: {file_path}")
                return

            # Verificar limite de tamanho
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            size_limit = self.options.get("file_size_limit", 500)
            
            if size_limit > 0 and file_size_mb > size_limit:
                if self.options.get('debug', False):
                    self.log_debug(f"Arquivo muito grande ({file_size_mb:.2f}MB > {size_limit}MB): {file_path}")
                return

            # Calcular hashes
            hashes = self._calculate_file_hashes(file_path)
            result = []
            if hashes:
                # Formatar e definir resultados individuais sem quebras de linha
                filename = Path(file_path).name
                self.set_result(f"Arquivo: {filename}")
                
                # Ordem específica solicitada
                hash_order = ['md5', 'sha1', 'sha256', 'sha512']
                hash_labels = {
                    'md5': 'MD5',
                    'sha1': 'SHA-1', 
                    'sha256': 'SHA256',
                    'sha512': 'SHA512'
                }
                
                for hash_type in hash_order:
                    if hash_type in hashes:
                        label = hash_labels[hash_type]
                        result.append(f"{label}: {hashes[hash_type]}")
                if result:
                    result.append("")
                    self.set_result("\n".join(result))
                
                if self.options.get('debug', False):
                    self.log_debug(f"Hashes calculados com sucesso para: {file_path}")
                        
        except Exception as e:
            self.handle_error(e, f"Erro ao calcular hashes de {file_path}")

    def _calculate_file_hashes(self, file_path: str) -> dict:
        """
        Calcula todos os hashes do arquivo simultaneamente.
        
        Args:
            file_path: Caminho para o arquivo
            
        Returns:
            Dicionário com os hashes calculados
        """
        hash_types = self.options.get('hash_types', ['md5', 'sha1', 'sha256', 'sha512'])
        buffer_size = self.options.get('buffer_size', 65536)
        
        # Inicializar objetos de hash
        hash_objects = {}
        for hash_type in hash_types:
            if hash_type.lower() == 'md5':
                hash_objects['md5'] = hashlib.md5()
            elif hash_type.lower() == 'sha1':
                hash_objects['sha1'] = hashlib.sha1()
            elif hash_type.lower() == 'sha256':
                hash_objects['sha256'] = hashlib.sha256()
            elif hash_type.lower() == 'sha512':
                hash_objects['sha512'] = hashlib.sha512()
        
        try:
            # Ler arquivo uma única vez e atualizar todos os hashes
            with open(file_path, 'rb') as file:
                while chunk := file.read(buffer_size):
                    for hash_obj in hash_objects.values():
                        hash_obj.update(chunk)
            
            # Obter hashes finais
            result_hashes = {}
            for hash_type, hash_obj in hash_objects.items():
                result_hashes[hash_type] = hash_obj.hexdigest()
            
            return result_hashes
            
        except Exception as e:
            self.handle_error(e, f"Erro ao ler arquivo {file_path}")
            return {}
