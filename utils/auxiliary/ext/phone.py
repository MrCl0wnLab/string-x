"""
Módulo extrator de números de telefone.

Este módulo implementa funcionalidade para extrair números de telefone brasileiros
de textos usando expressões regulares. Faz parte do sistema de módulos auxiliares
do String-X.
"""
import re
from core.basemodule import BaseModule

class Phone(BaseModule):
    """
    Módulo para extração de números de telefone usando regex.

    Este módulo herda de BaseModule e fornece funcionalidade específica para
    identificar e extrair números de telefone brasileiros de strings de texto.

    Attributes:
        meta (dict): Metadados do módulo incluindo nome, descrição, autor e tipo
        options (dict): Opções requeridas incluindo dados de entrada e padrão regex
    """
    
    def __init__(self):
        """
        Inicializa o módulo extrator de telefones.
        
        Configura os metadados do módulo e define as opções necessárias,
        incluindo o padrão regex para detecção de números de telefone brasileiros.
        """
        super().__init__()
        
        # Definir metadados do módulo
        self.meta = {
            'name': 'Phone Extractor',
            "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Extrai números de telefone brasileiros',
            'type': 'extractor'
        ,
            'example': './strx -l contacts.txt -st "echo {STRING}" -module "ext:phone" -pm'
        }
        
        # Definir opções configuráveis
        self.options = {
            'data': str(),
            'regex': r'(?:\+55\s?)?(?:\([1-9]{2}\)\s?|[1-9]{2}\s?)?(?:9\s?)?[0-9]{4}-?[0-9]{4}',            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa o processo de extração de telefones.
        
        Utiliza os dados fornecidos e o padrão regex configurado para identificar
        e extrair números de telefone brasileiros válidos. Os números encontrados
        são armazenados nos resultados do módulo.
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        
        # Verifica se há dados para processar
        if (target_value := self.options.get("data")) and (regex_data := self.options.get("regex")): 
            regex_data = re.compile(regex_data, re.IGNORECASE)
            if regex_result_list := set(re.findall(regex_data, target_value)):
                for value_regex in regex_result_list:
                    self.set_result(value_regex)


