"""
Módulo extrator de credenciais.

Este módulo implementa funcionalidade para extrair padrões de credenciais
como senhas, tokens API, chaves SSH, etc. Possui suporte aprimorado para arquivos .env.
"""
import re
import os
from stringx.core.basemodule import BaseModule

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
            'description': 'Extrai credenciais, tokens API, chaves com suporte especial para arquivos .env',
            'type': 'extractor',
            'example': './strx -l config_files.txt -st "echo {STRING}" -module "ext:credential" -pm'
        }
        
        self.options = {
            'data': str(),
            'types': ['all'],  # aws, github, slack, password, ssh, env
            'prioritize_env': True,  # Prioriza detecção de formato .env
            'redact_values': False,  # Se True, oculta valores de credenciais sensíveis
            'min_password_length': 6, # Tamanho mínimo para detectar senhas
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,      # Número de tentativas de requisição
            'retry_delay': None,  # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa o processo de extração de credenciais.
        
        Utiliza os dados fornecidos e busca por diferentes tipos de credenciais
        e tokens usando padrões regex específicos. Possui suporte aprimorado
        para arquivos .env e outros formatos de configuração.
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
        
        if not (target_value := self.options.get("data")):
            self.log_debug("[X] Nenhum dado fornecido para extração")
            return
        
        self.log_debug(f"[*] Iniciando extração de credenciais em texto de {len(target_value)} caracteres")
        
        # Configurações
        prioritize_env = self.options.get('prioritize_env', True)
        redact_values = self.options.get('redact_values', False)
        min_password_length = self.options.get('min_password_length', 6)
        
        # Padrões de credenciais por tipo
        patterns = {
            'aws_access_key': r'(?:AKIA|ASIA|AROA|AIDA)[A-Z0-9]{16}',
            'aws_secret_key': r'[0-9a-zA-Z/+]{40}',
            'github_token': r'gh[ps]_[0-9a-zA-Z]{36,40}',
            'slack_token': r'xox[baprs]-[0-9a-zA-Z-]{10,48}',
            'jwt_token': r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
            'ssh_private': r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
            'password_pattern': r'(?i)(password|pwd|pass|senha)\s*[:=]\s*[\'"]?([^\s\'"]{' + str(min_password_length) + r',})',
            'api_key': r'(?i)(api[_-]?key|apikey|app_key|token)\s*[:=]\s*[\'"]?([a-zA-Z0-9_\-.=+/]{16,})',
            'mail_credentials': r'(?i)(mail_password|smtp_password|email_pwd)\s*[:=]\s*[\'"]?([^\s\'"]+)',
            'firebase_key': r'AIza[0-9A-Za-z\\-_]{35}',
            'database_url': r'(?i)(jdbc:|mongodb:|mysql://|postgres://|sqlserver://)[^\s\'\"<>]{10,}'
        }
        
        # Padrões específicos para arquivos .env
        env_patterns = r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*([^\s].*?)(?:\s*#.*)?$'
        
        results = []
        types = self.options.get('types', ['all'])
        if 'all' in types:
            types = list(patterns.keys()) + ['env']
        
        # Realizar extração prioritária de formato .env se ativado
        if prioritize_env and ('env' in types or 'all' in types):
            self.log_debug("[*] Buscando por credenciais em formato .env")
            env_credentials = self._extract_env_credentials(target_value, redact_values)
            if env_credentials:
                results.extend(env_credentials)
        
        # Extrair outros padrões de credenciais
        for pattern_type in types:
            if pattern_type != 'env' and pattern_type in patterns:
                self.log_debug(f"[*] Buscando por credenciais do tipo {pattern_type}")
                regex = re.compile(patterns[pattern_type], re.IGNORECASE | re.MULTILINE)
                matches = regex.findall(target_value)
                
                for match in matches:
                    if isinstance(match, tuple):
                        # Para padrões que contêm grupos de captura (como password_pattern)
                        key = match[0]
                        value = match[1] if len(match) > 1 else match[0]
                        
                        # Ocultar valor se for sensível e redact_values estiver ativo
                        if redact_values:
                            value = self._redact_sensitive_value(value)
                            
                        results.append(f"{key.upper()}: {value}")
                    else:
                        # Para padrões que retornam apenas o valor
                        value = match
                        if redact_values:
                            value = self._redact_sensitive_value(value)
                            
                        results.append(f"{pattern_type.upper()}: {value}")
        
        # Armazenar resultados únicos
        if results:
            unique_results = sorted(list(set(results)))
            self.log_debug(f"[+] Encontradas {len(unique_results)} credenciais únicas")
            self.set_result("\n".join(unique_results))
        else:
            self.log_debug("[!] Nenhuma credencial encontrada")
    
    def _extract_env_credentials(self, text: str, redact: bool = False) -> list:
        """
        Extrai credenciais de um formato de arquivo .env
        
        Args:
            text (str): Texto a ser analisado
            redact (bool): Se True, oculta valores sensíveis
            
        Returns:
            list: Lista de credenciais encontradas
        """
        results = []
        env_pattern = r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*([^\s].*?)(?:\s*#.*)?$'
        
        # Palavras-chave de alto valor para destacar (sensíveis)
        sensitive_keywords = [
            'password', 'pwd', 'secret', 'key', 'token', 'apikey', 'host',
            'credential', 'auth', 'senha', 'private', 'access', 'user'
        ]
        
        # Processar linha por linha para melhor precisão com arquivos .env
        for line in text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            match = re.match(env_pattern, line, re.IGNORECASE)
            if match:
                key, value = match.groups()
                
                # Remover aspas no início e final do valor, se presentes
                value = value.strip('\'"')
                
                # Verificar se é uma credencial de alto valor (sensível)
                is_sensitive = any(keyword.lower() in key.lower() for keyword in sensitive_keywords)
                
                # Ocultar valor se for sensível e redact estiver ativo
                if redact and is_sensitive and len(value) > 0:
                    value = self._redact_sensitive_value(value)
                
                # Adicionar ao resultado se tiver valor
                if value and not (value.startswith('$') and value.endswith('}')):
                    results.append(f"{key}: {value}")
        
        return results
    
    def _redact_sensitive_value(self, value: str) -> str:
        """
        Oculta valores sensíveis mantendo apenas partes seguras para visualização.
        
        Args:
            value (str): Valor a ser ocultado
            
        Returns:
            str: Valor parcialmente ocultado
        """
        if not value or len(value) <= 4:
            return '****'
        
        # Mostrar apenas os primeiros e últimos caracteres para referência
        visible_chars = min(3, len(value) // 4)
        return value[:visible_chars] + '*' * (len(value) - visible_chars * 2) + value[-visible_chars:]
