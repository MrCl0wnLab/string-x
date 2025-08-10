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
            "regex": r'https?://[^\s<>"\']+',
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
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
            
        self.log_debug("[*] Iniciando extração de URLs")
        result = []
        
        try:
            # Verifica se há dados para processar
            if (target_value := self.options.get("data")) and (regex_data := self.options.get("regex")):
                self.log_debug(f"[*] Processando {len(target_value)} caracteres de dados")
                self.log_debug(f"[*] Padrão regex: {regex_data}")
                
                regex_data = re.compile(regex_data, re.IGNORECASE)
                if regex_result_list := re.findall(regex_data, target_value):
                    self.log_debug(f"[+] Encontradas {len(regex_result_list)} URLs (com duplicatas)")
                    
                    for url in regex_result_list:
                        url = url.strip()
                        url = url[:url.rfind(';')] if ';' in url else url  # Remove fragmentos
                        result.append(url)
                        
                    if result:
                        result = sorted(list(set(result)))  # Remove duplicatas
                        self.log_debug(f"[*] URLs únicas após deduplicação: {len(result)}")
                        
                        # Log some sample URLs for debugging
                        sample_urls = result[:3] if len(result) > 3 else result
                        for i, url in enumerate(sample_urls, 1):
                            self.log_debug(f"   {i}. {url}")
                        if len(result) > 3:
                            self.log_debug(f"   ... e mais {len(result) - 3} URLs")
                            
                        self.set_result("\n".join(result))
                    else:
                        self.log_debug("[!] Lista de URLs vazia após processamento")
                else:
                    self.log_debug("[X] Nenhuma URL encontrada no padrão regex")
            else:
                self.log_debug("[X] Dados ou regex não fornecidos")
                if not self.options.get("data"):
                    self.log_debug("   - Dados: não fornecidos")
                if not self.options.get("regex"):
                    self.log_debug("   - Regex: não fornecido")
                    
        except Exception as e:
            self.handle_error(e, "Erro na extração de URLs")

