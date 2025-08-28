"""
Módulo extrator de endereços de email.

Este módulo implementa funcionalidade para extrair endereços de email de textos
usando expressões regulares. Faz parte do sistema de módulos auxiliares do String-X.
"""
import re
from stringx.core.basemodule import BaseModule

class AuxRegexEmail(BaseModule):
    """
    Módulo para extração de endereços de email usando regex.

    Este módulo herda de BaseModule e fornece funcionalidade específica para
    identificar e extrair endereços de email válidos de strings de texto.

    Attributes:
        meta (dict): Metadados do módulo incluindo nome, descrição, autor e tipo
        options (dict): Opções requeridas incluindo dados de entrada e padrão regex

    Methods:
        __init__(): Inicializa o módulo com metadados e configurações
        run(): Executa o processo de extração de emails
    """
    def __init__(self):
        """
        Inicializa o módulo extrator de emails.
        
        Configura os metadados do módulo e define as opções necessárias,
        incluindo o padrão regex para detecção de emails.
        """
        super().__init__()

        # Define informações de meta do módulo
        self.meta.update({
            "name": "Extractor de Emails",
            "description": "Extrai emails do texto fornecido",
            "author": "MrCl0wn",
            "type": "extractor"
        })

        # Define opções requeridas para este módulo
        self.options = {
            "data": str(),
            "regex": "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])",
            "example": "./strx -l documents.txt -st \"{STRING}\" -module \"ext:email\" -pm",
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }

    def run(self):
        """
        Executa o processo de extração de emails.
        
        Utiliza os dados fornecidos e o padrão regex configurado para identificar
        e extrair endereços de email válidos. Os emails encontrados são armazenados
        nos resultados do módulo.
        
        O processo inclui:
        1. Verificação da disponibilidade de dados e padrão regex
        2. Compilação do padrão regex com flag IGNORECASE
        3. Busca por emails no texto
        4. Armazenamento dos resultados únicos encontrados
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
            
        self.log_debug("[*] Iniciando extração de emails")
        result = []
        
        try:
            # Verifica se há dados para processar
            if (target_value := self.options.get("data")) and (regex_data := self.options.get("regex")):
                self.log_debug(f"[*] Processando {len(target_value)} caracteres de dados")
                self.log_debug("[*] Usando padrão regex RFC 5322 para emails")
                
                regex_data = re.compile(regex_data, re.IGNORECASE)
                if regex_result_list := set(re.findall(regex_data, target_value)):
                    self.log_debug(f"[+] Encontrados {len(regex_result_list)} emails únicos")
                    
                    for email in regex_result_list:
                        result.append(email)
                        
                    if result:
                        result = sorted(list(set(result)))
                        self.log_debug(f"[*] Emails após ordenação: {len(result)}")
                        
                        # Log some sample emails for debugging
                        sample_emails = result[:3] if len(result) > 3 else result
                        for i, email in enumerate(sample_emails, 1):
                            self.log_debug(f"   [*] {i}. {email}")
                        if len(result) > 3:
                            self.log_debug(f"   [*] ... e mais {len(result) - 3} emails")
                            
                        return self.set_result("\n".join(result))
                    else:
                        self.log_debug("[!] Lista de emails vazia após processamento")
                else:
                    self.log_debug("[x] Nenhum email encontrado no padrão regex")
            else:
                self.log_debug("[x] Dados ou regex não fornecidos")
                if not self.options.get("data"):
                    self.log_debug("   [ - ] Dados: não fornecidos")
                if not self.options.get("regex"):
                    self.log_debug("   [ - ] Regex: não fornecido")
                    
        except Exception as e:
            self.handle_error(e, "Erro na extração de emails")
