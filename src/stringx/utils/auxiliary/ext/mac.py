"""
Módulo extrator de endereços MAC.

Este módulo implementa funcionalidade para extrair endereços MAC (Media Access Control) 
de textos usando expressões regulares. Suporta diferentes formatos de endereços MAC.
Faz parte do sistema de módulos auxiliares do String-X.
"""
import re
from stringx.core.basemodule import BaseModule

class AuxRegexMac(BaseModule):
    """
    Módulo para extração de endereços MAC usando regex.

    Este módulo herda de BaseModule e fornece funcionalidade específica para
    identificar e extrair endereços MAC válidos de strings de texto.

    Suporta os seguintes formatos de endereços MAC:
    - Formato com dois pontos: 00:1B:44:11:3A:B7
    - Formato com hífen: 00-1B-44-11-3A-B7
    - Formato com ponto: 001B.4411.3AB7 (Cisco)
    - Formato sem separadores: 001B44113AB7
    - Formato Linux: 00:1b:44:11:3a:b7 (minúsculas)

    Attributes:
        meta (dict): Metadados do módulo incluindo nome, descrição, autor e tipo
        options (dict): Opções requeridas incluindo dados de entrada e configurações

    Methods:
        __init__(): Inicializa o módulo com metadados e configurações
        run(): Executa o processo de extração de endereços MAC
        _normalize_mac(): Normaliza endereços MAC para formato padrão
        _is_valid_mac(): Valida se um endereço MAC é válido
    """
    
    def __init__(self):
        """
        Inicializa o módulo extrator de endereços MAC.
        
        Configura os metadados do módulo e define as opções necessárias,
        incluindo os padrões regex para detecção de diferentes formatos de MAC.
        """
        super().__init__()

        # Define informações de meta do módulo
        self.meta.update({
            "name": "Extractor de Endereços MAC",
            "description": "Extrai endereços MAC (Media Access Control) em diferentes formatos do texto fornecido",
            "author": "MrCl0wn",
            "type": "extractor"
        })

        # Define opções requeridas para este módulo
        self.options = {
            "data": str(),
            "normalize_format": True,  # Se True, normaliza todos para formato padrão
            "case_sensitive": False,  # Se True, mantém case original
            "example": "./strx -l documents.txt -st \"{STRING}\" -module \"ext:mac\" -pm",
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,  # Número de tentativas de requisição
            'retry_delay': None,  # Atraso entre tentativas de requisição
        }

        # Padrões regex para diferentes formatos de endereços MAC
        self.mac_patterns = [
            # Formato com dois pontos (mais comum): 00:1B:44:11:3A:B7
            r'\b([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b',
            
            # Formato Cisco com pontos: 001B.4411.3AB7
            r'\b[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\b',
            
            # Formato sem separadores: 001B44113AB7
            r'\b[0-9A-Fa-f]{12}\b',
            
            # Formato com espaços: 00 1B 44 11 3A B7
            r'\b([0-9A-Fa-f]{2}\s){5}[0-9A-Fa-f]{2}\b',
        ]

    def run(self):
        """
        Executa o processo de extração de endereços MAC.
        
        Utiliza os dados fornecidos e os padrões regex configurados para identificar
        e extrair endereços MAC válidos. Os endereços encontrados são armazenados
        nos resultados do módulo.
        
        O processo inclui:
        1. Verificação da disponibilidade de dados
        2. Aplicação de diferentes padrões regex
        3. Normalização de formatos (se habilitado)
        4. Armazenamento dos resultados únicos encontrados
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        
        if not (target_value := self.options.get("data")):
            self.log_debug("Nenhum dado fornecido para extração")
            return

        self.log_debug(f"Iniciando extração de endereços MAC em texto de {len(target_value)} caracteres")
        
        results = set()
        normalize_format = self.options.get("normalize_format", True)
        case_sensitive = self.options.get("case_sensitive", False)
        # Debug: mostrar o texto de entrada
        # Aplicar todos os padrões regex
        for pattern in self.mac_patterns:
            flags = 0 if case_sensitive else re.IGNORECASE
            for match in re.finditer(pattern, target_value, flags):
                mac_address = match.group(0)
                if self._is_valid_mac(mac_address):
                    if normalize_format and mac_address:
                        mac_address = self._normalize_mac(mac_address)
                    results.add(mac_address)

        # Armazenar resultados únicos
        if results:
            self.log_debug(f"Encontrados {len(results)} endereços MAC únicos")
            # Como results já é um set(), converter para lista ordenada
            unique_macs = sorted(list(results))
            self.set_result("\n".join(unique_macs))
        else:
            self.log_debug("Nenhum endereço MAC encontrado")

    def _normalize_mac(self, mac_address: str) -> str:
        """
        Normaliza um endereço MAC para o formato padrão (00:1B:44:11:3A:B7).
        
        Args:
            mac_address (str): Endereço MAC em qualquer formato
            
        Returns:
            str: Endereço MAC normalizado no formato padrão
        """
        # Remover todos os separadores e espaços
        clean_mac = re.sub(r'[^0-9A-Fa-f]', '', mac_address).upper()
        
        # Garantir que tem 12 caracteres
        if len(clean_mac) == 12:
            # Dividir em grupos de 2 e juntar com dois pontos
            return ':'.join([clean_mac[i:i+2] for i in range(0, 12, 2)])
        
        return mac_address  # Retornar original se não conseguir normalizar

    def _is_valid_mac(self, mac_address: str) -> bool:
        """
        Valida se um endereço MAC é válido (não é todo zeros, todo F, etc.).
        
        Args:
            mac_address (str): Endereço MAC para validar
            
        Returns:
            bool: True se válido, False caso contrário
        """
        # Remover separadores para análise
        clean_mac = re.sub(r'[^0-9A-Fa-f]', '', mac_address).upper()
        
        # Verificar comprimento
        if len(clean_mac) != 12:
            return False
        
        # Verificar se não é todo zeros
        if clean_mac == "000000000000":
            return False
        
        # Verificar se não é todo F (broadcast)
        if clean_mac == "FFFFFFFFFFFF":
            return False
        
        # Verificar se contém apenas caracteres hexadecimais válidos
        try:
            int(clean_mac, 16)
            return True
        except ValueError:
            return False
