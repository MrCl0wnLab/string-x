"""
Módulo extrator de domínios.

Este módulo implementa funcionalidade para extrair domínios válidos de textos
usando expressões regulares com validação de TLDs. Faz parte do sistema de
módulos auxiliares do String-X.
"""
import re
from stringx.core.basemodule import BaseModule

class AuxRegexDomain(BaseModule):
    """
    Módulo para extração de domínios usando regex com validação de TLD.

    Este módulo herda de BaseModule e fornece funcionalidade específica para
    identificar e extrair domínios válidos de strings de texto, validando
    contra uma lista extensa de TLDs conhecidos.

    Attributes:
        meta (dict): Metadados do módulo incluindo nome, descrição, autor e tipo
        options (dict): Opções requeridas incluindo dados de entrada e padrão regex
    """
    
    def __init__(self):
        """
        Inicializa o módulo extrator de domínios.
        
        Configura os metadados do módulo e define as opções necessárias,
        incluindo uma lista extensa de TLDs válidos e o padrão regex
        correspondente para detecção de domínios.
        """
        super().__init__()
        self.meta = {
            "name": "Extractor de Domínios",
            "description": "Extrai domínios de strings fornecidas",
            "author": "MrCl0wn",
            "version": "1.0",
            "type": "extractor"
        }
        
        # Lista de TLDs válidos mais comuns
        tlds = ['com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'co', 'io', 'ai', 'app', 'dev',
            'br', 'us', 'uk', 'ca', 'de', 'fr', 'it', 'es', 'au', 'jp', 'cn', 'in', 'ru',
            'com.br', 'gov.br', 'org.br', 'net.br', 'edu.br', 'mil.br',
            # Novos TLDs genéricos
            'info', 'biz', 'name', 'pro', 'aero', 'asia', 'cat', 'coop', 'jobs', 'mobi', 
            'museum', 'tel', 'travel', 'xxx', 'xyz', 'online', 'site', 'tech', 'store',
            'web', 'blog', 'shop', 'cloud', 'host', 'space', 'media', 'news', 'live',
            # Mais ccTLDs (country code)
            'eu', 'nl', 'be', 'ch', 'at', 'se', 'no', 'dk', 'fi', 'pl', 'cz', 'sk',
            'hu', 'ro', 'bg', 'gr', 'pt', 'ie', 'is', 'lt', 'lv', 'ee', 'si', 'hr',
            'mx', 'ar', 'cl', 'pe', 'co', 've', 'ec', 'uy', 'py', 'bo', 'cr', 'pa',
            'za', 'eg', 'ma', 'ng', 'ke', 'tn', 'ae', 'sa', 'il', 'tr', 'ua', 'kz',
            'sg', 'my', 'th', 'vn', 'id', 'ph', 'kr', 'tw', 'hk', 'mo', 'nz', 'au']
        
        # Regex com validação de TLD
        tld_pattern = '|'.join(re.escape(tld) for tld in tlds)
        
        self.options = {
            "data": str(),
            "regex": rf'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{{0,61}}[a-zA-Z0-9])?\.)+(?:{tld_pattern})\b',
            "example": './strx -l documents.txt -st "{STRING}" -module "ext:domain" -pm -f ".com"',
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 1,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
        
    def run(self):
        """
        Executa o processo de extração de domínios.
        
        Utiliza os dados fornecidos e o padrão regex configurado para identificar
        e extrair domínios válidos com TLDs reconhecidos. Os domínios encontrados
        são armazenados nos resultados do módulo.
        
        O processo inclui:
        1. Verificação da disponibilidade de dados e padrão regex
        2. Compilação do padrão regex com flag IGNORECASE
        3. Busca por domínios no texto com validação de TLD
        4. Armazenamento dos resultados únicos encontrados
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
            
        self.log_debug("[*] Iniciando extração de domínios")
        result = []
        
        try:
            # Verifica se há dados para processar
            if (target_value := self.options.get("data")) and (regex_data := self.options.get("regex")):
                self.log_debug(f"[*] Processando {len(target_value)} caracteres de dados")
                self.log_debug(f"[*] Padrão regex configurado para TLDs válidos")
                
                regex_data = re.compile(regex_data, re.IGNORECASE)
                if regex_result_list := re.findall(regex_data, target_value):
                    self.log_debug(f"[+] Encontrados {len(regex_result_list)} domínios (com duplicatas)")
                    
                    for domain in regex_result_list:
                        result.append(domain)
                        
                    if result:
                        result = sorted(list(set(result)))  # Remove duplicatas
                        self.log_debug(f"[*] Domínios únicos após deduplicação: {len(result)}")
                        
                        # Log some sample domains for debugging
                        sample_domains = result[:3] if len(result) > 3 else result
                        for i, domain in enumerate(sample_domains, 1):
                            self.log_debug(f"   {i}. {domain}")
                        if len(result) > 3:
                            self.log_debug(f"   ... e mais {len(result) - 3} domínios")
                            
                        return self.set_result("\n".join(result))
                    else:
                        self.log_debug("[!] Lista de domínios vazia após processamento")
                else:
                    self.log_debug("[X] Nenhum domínio encontrado no padrão regex")
            else:
                self.log_debug("[X] Dados ou regex não fornecidos")
                if not self.options.get("data"):
                    self.log_debug("   - Dados: não fornecidos")
                if not self.options.get("regex"):
                    self.log_debug("   - Regex: não fornecido")
                    
        except Exception as e:
            self.handle_error(e, "Erro na extração de domínios")

            