"""
Módulo extrator de credenciais.

Este módulo implementa funcionalidade para extrair padrões de credenciais
como senhas, tokens API, chaves SSH, etc.
"""
from core.basemodule import BaseModule
import re

class CredentialExtractor(BaseModule):
    """
    Módulo para extração de credenciais e tokens sensíveis.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'Credential Extractor',
            'author': 'MrCl0wn',
            'version': '1.0', 
            'description': 'Extrai credenciais, tokens API, chaves',
            'type': 'extractor'
        }
        
        self.options = {
            'data': str(),
            'types': ['all'],  # aws, github, slack, password, ssh
            'example': './strx -l config_files.txt -st "echo {STRING}" -module "ext:credential" -pm',
            'debug': False  # Modo de debug para mostrar informações detalhadas
        }
    
    def run(self):
        """
        Executa o processo de extração de credenciais.
        
        Utiliza os dados fornecidos e busca por diferentes tipos de credenciais
        e tokens usando padrões regex específicos.
        """
        if not (target_value := self.options.get("data")):
            return
            
        patterns = {
            'aws_access_key': r'AKIA[0-9A-Z]{16}',
            'aws_secret_key': r'[0-9a-zA-Z/+]{40}',
            'github_token': r'ghp_[0-9a-zA-Z]{36}',
            'slack_token': r'xox[baprs]-[0-9a-zA-Z-]{10,48}',
            'jwt_token': r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
            'ssh_private': r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
            'password_pattern': r'(?i)(password|pwd|pass|senha)\s*[:=]\s*[\'"]?([^\s\'"]+)',
            'api_key': r'(?i)(api[_-]?key|apikey)\s*[:=]\s*[\'"]?([a-zA-Z0-9_-]{20,})'
        }
        
        types = self.options.get('types', ['all'])
        if 'all' in types:
            types = list(patterns.keys())
            
        for pattern_type in types:
            if pattern_type in patterns:
                regex = re.compile(patterns[pattern_type], re.IGNORECASE | re.MULTILINE)
                matches = regex.findall(target_value)
                
                for match in matches:
                    if isinstance(match, tuple):
                        result = f"{pattern_type.upper()}: {match[1] if len(match) > 1 else match[0]}"
                    else:
                        result = f"{pattern_type.upper()}: {match}"
                    self.set_result(result)
