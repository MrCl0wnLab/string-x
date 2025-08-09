"""
Módulo de banners ASCII.

Este módulo contém a classe AsciiBanner responsável por carregar e exibir
banners ASCII armazenados em arquivos, incluindo seleção aleatória de banners.
"""
import os
import random
from stringx.config import setting
from stringx.core.filelocal import FileLocal
from stringx.core.style_cli import StyleCli


class AsciiBanner:
    """
    Classe para gerenciamento de banners ASCII.
    
    Esta classe permite carregar banners ASCII de arquivos e exibi-los
    no terminal, incluindo funcionalidade de seleção aleatória.
    
    Attributes:
        _file (FileLocal): Instância para manipulação de arquivos
        _cli (StyleCli): Instância para interface CLI estilizada
        _files_path (str): Caminho para diretório dos banners
    """
    def __init__(self):
        """
        Inicializa AsciiBanner com configurações padrão.
        """
        self._file = FileLocal()
        self._cli = StyleCli()
        # Usar caminho absoluto para o diretório de banners
        SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self._files_path = os.path.join(SCRIPT_DIR, 'core', 'banner', 'asciiart')

    def _get_banner_file(self, banner_name: str):
        """
        Busca arquivo de banner por nome.
        
        Args:
            banner_name (str): Nome do banner a ser buscado
            
        Returns:
            list: Lista de arquivos que correspondem ao nome
        """
        banner_list = self._get_banner_list()
        if not banner_list or 'files' not in banner_list:
            return []
        banners = banner_list.get('files')
        return [name for name in banners if banner_name in str(name)]

    def _get_banner_list(self):
        """
        Obtém lista de arquivos de banner disponíveis.
        
        Returns:
            dict: Dicionário com lista de arquivos de banner
        """
        try:
            return self._file.list_file_dir(self._files_path)
        except Exception:
            self._cli.console.print_exception(max_frames=3)
            return {'files': []}

    def show(self, banner_name: str):
        """
        Exibe um banner específico.
        
        Args:
            banner_name (str): Nome do banner a ser exibido
            
        Returns:
            str: Conteúdo do banner ou string vazia se não encontrado
        """
        if banner_name:
            try:
                banner_files = self._get_banner_file(banner_name)
                if not banner_files:  # Verificar se a lista está vazia
                    return ""
                
                file_name = str(banner_files[0])
                txt_line, data_return = self._file.open_file(file_name, 'r')
                if txt_line:
                    txt_line = ''.join(txt_line).replace(
                            '[DESCRIPTION]',setting.__description__ 
                        ).replace(
                            '[VERSION]', setting.__version__
                        )
                    return ''.join(txt_line)
            except (IndexError, FileNotFoundError):
                # Silenciar exceção e retornar string vazia
                return ""
        return ""

    def show_random(self):
        """
        Exibe um banner selecionado aleatoriamente.
        
        Returns:
            str: Conteúdo do banner aleatório
        """
        try:
            banner_list = self._get_banner_list()
            if not banner_list or not banner_list.get('files'):
                return ""
                
            files = banner_list.get('files')
            random.shuffle(files)
            if not files:
                return ""
                
            banner_file_name = files[0].stem
            return self.show(banner_file_name)
        except Exception:
            return ""

