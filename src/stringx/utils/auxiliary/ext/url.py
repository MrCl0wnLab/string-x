"""
Módulo extrator de URLs.

Este módulo implementa funcionalidade para extrair URLs de textos usando
expressões regulares. Faz parte do sistema de módulos auxiliares do String-X.
"""
import re
import time
import random
from stringx.core.basemodule import BaseModule

class AuxRegexURL(BaseModule):
    """
    Módulo para extração de URLs usando regex.

    Este módulo herda de BaseModule e fornece funcionalidade específica para
    identificar e extrair URLs válidas de strings de texto.

    Attributes:
        meta (dict): Metadados do módulo incluindo nome, descrição, autor e tipo
        options (dict): Opções requeridas incluindo dados de entrada e padrão regex
    """
    
    def __init__(self):
        """
        Inicializa o módulo extrator de URLs.
        
        Configura os metadados do módulo e define as opções necessárias,
        incluindo o padrão regex para detecção de URLs HTTP/HTTPS.
        """
        super().__init__()
        self.meta = {
            "name": "Extractor de URLs",
            "description": "Extrai URLs de strings",
            "author": "MrCl0wn",
            "type": "extractor"
        }
        self.options = {
            "data": str(),
            "regex": r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-\w%/.]*)*(?:\?[-\w%&=.]*)?',
            "example": "./strx -l webpages.txt -st \"{STRING}\" -module \"ext:url\" -pm",
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 1,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa o processo de extração de URLs.
        
        Utiliza os dados fornecidos e o padrão regex configurado para identificar
        e extrair URLs válidas de strings de texto. As URLs encontradas
        são armazenadas nos resultados do módulo.
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        result = []
        # Verifica se há dados para processar
        if (target_value := self.options.get("data")) and (regex_data := self.options.get("regex")): 
            regex_data = re.compile(regex_data, re.IGNORECASE)
            if regex_result_list := re.findall(regex_data, target_value):
                for url in regex_result_list:
                    result.append(url)
                if result:
                    result = sorted(list(set(result)))  # Remove duplicatas
                    return self.set_result("\n".join(result))

