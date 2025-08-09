"""
Módulo extrator de números de documentos brasileiros.

Este módulo implementa funcionalidade para extrair números de documentos oficiais brasileiros
usando expressões regulares. Suporta CPF, CNPJ, RG, PIS, Título de Eleitor e CNH.
Faz parte do sistema de módulos auxiliares do String-X.
"""
import re
from stringx.core.basemodule import BaseModule
from stringx.core.validators import Validator

class AuxRegexDocuments(BaseModule):
    """
    Módulo para extração de números de documentos brasileiros usando regex.

    Este módulo herda de BaseModule e fornece funcionalidade específica para
    identificar e extrair números de documentos oficiais brasileiros válidos de strings de texto.

    Suporta os seguintes tipos de documentos brasileiros:
    - CPF (Cadastro de Pessoas Físicas)
    - CNPJ (Cadastro Nacional da Pessoa Jurídica)
    - RG (Registro Geral) - formato básico
    - PIS/PASEP (Programa de Integração Social)
    - Título de Eleitor
    - CNH (Carteira Nacional de Habilitação)

    Attributes:
        meta (dict): Metadados do módulo incluindo nome, descrição, autor e tipo
        options (dict): Opções requeridas incluindo dados de entrada e configurações

    Methods:
        __init__(): Inicializa o módulo com metadados e configurações
        run(): Executa o processo de extração de números de documentos
        _validate_cpf(): Valida dígitos verificadores do CPF
        _validate_cnpj(): Valida dígitos verificadores do CNPJ
    """
    
    def __init__(self):
        """
        Inicializa o módulo extrator de números de documentos.
        
        Configura os metadados do módulo e define as opções necessárias,
        incluindo os padrões regex para detecção de diferentes tipos de documentos.
        """
        super().__init__()

        # Define informações de meta do módulo
        self.meta.update({
            "name": "Extractor de Documentos Brasileiros",
            "description": "Extrai números de documentos oficiais brasileiros (CPF, CNPJ, RG, PIS, Título de Eleitor, CNH) do texto fornecido",
            "author": "MrCl0wn",
            "type": "extractor"
        })

        # Define opções requeridas para este módulo
        self.options = {
            "data": str(),
            "validate_checksums": True,  # Se True, valida dígitos verificadores quando possível
            "example": "./strx -l documents.txt -st \"{STRING}\" -module \"ext:documents\" -pm",
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,  # Número de tentativas de requisição
            'retry_delay': None,  # Atraso entre tentativas de requisição
        }

        # Padrões regex para documentos brasileiros - melhorados para extração de diversos formatos
        self.document_patterns = {
            'cpf': [
                # CPF com formatação padrão: 123.456.789-09
                r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b',
                
                # CPF em dumps e outros formatos não padronizados
                r'(?:CPF|cpf|Cpf)[\s:]*(\d{3}\.?\d{3}\.?\d{3}-?\d{2})',
                r'(?:nr_cpf|numcpf|num_cpf|cpf_num|cpf_value)[\s:=\"\']*(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{11})',
                
                # CPF sem formatação em meio a texto ou valores
                r'(?<!\d)(\d{11})(?!\d)',
            ],
            'cnpj': [
                # CNPJ formatação padrão: 12.345.678/0001-90
                r'\b\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}\b',
                
                # CNPJ em dumps e outros formatos não padronizados
                r'(?:CNPJ|cnpj|Cnpj)[\s:]*(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2})',
                r'(?:nr_cnpj|numcnpj|num_cnpj|cnpj_num|cnpj_value)[\s:=\"\']*(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}|\d{14})',
                
                # CNPJ sem formatação em meio a texto ou valores
                r'(?<!\d)(\d{14})(?!\d)',
            ],
            'rg': [
                # RG formato SP: 12.345.678-9
                r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[0-9X]\b',
                
                # RG em dumps e outros formatos não padronizados
                r'(?:RG|rg|Rg|registro\s*geral)[\s:]*([0-9]{1,2}\.?[0-9]{3}\.?[0-9]{3}-?[0-9X])',
                r'(?:nr_rg|numrg|num_rg|rg_num|rg_value)[\s:=\"\']*([0-9]{1,2}\.?[0-9]{3}\.?[0-9]{3}-?[0-9X]|[0-9]{7,9}[0-9X]?)',
                
                # RG formato simples (4-9 dígitos)
                r'\b(?<![\w\.])([0-9]{4,9})(?![\w\.])\b',
            ],
            'pis': [
                # PIS/PASEP formatação padrão: 123.45678.90-1
                r'\b\d{3}\.?\d{5}\.?\d{2}-?\d{1}\b',
                
                # PIS/PASEP em dumps e outros formatos não padronizados
                r'(?:PIS|pis|Pis|PASEP|pasep|Pasep)[\s:]*(\d{3}\.?\d{5}\.?\d{2}-?\d{1})',
                r'(?:nr_pis|numpis|num_pis|pis_num|pis_value)[\s:=\"\']*(\d{3}\.?\d{5}\.?\d{2}-?\d{1}|\d{11})',
                
                # PIS/PASEP sem formatação
                r'(?<!\d)(\d{11})(?!\d)',
            ],
            'titulo_eleitor': [
                # Título de eleitor formatação padrão: 1234 5678 9012
                r'\b\d{4}\s?\d{4}\s?\d{4}\b',
                
                # Título de eleitor em dumps e outros formatos não padronizados
                r'(?:titulo\s*eleitoral|titulo\s*de\s*eleitor|te)[\s:]*(\d{4}\s?\d{4}\s?\d{4}|\d{12})',
                r'(?:nr_titulo|numtitulo|num_titulo|titulo_num|titulo_value)[\s:=\"\']*(\d{4}\s?\d{4}\s?\d{4}|\d{12})',
                
                # Título de eleitor sem formatação
                r'(?<!\d)(\d{12})(?!\d)',
            ],
            'cnh': [
                # CNH (11 dígitos)
                r'\b\d{11}\b',
                
                # CNH em dumps e outros formatos não padronizados
                r'(?:CNH|cnh|Cnh|habilitacao|carteira\s*nacional\s*de\s*habilitacao)[\s:]*(\d{11})',
                r'(?:nr_cnh|numcnh|num_cnh|cnh_num|cnh_value)[\s:=\"\']*(\d{11})',
                
                # CNH sem formatação específica para CNH
                r'(?<!\d)(\d{11})(?!\d)',
            ],
        }

    def run(self):
        """
        Executa o processo de extração de números de documentos brasileiros.
        
        Utiliza os dados fornecidos e os padrões regex configurados para identificar
        e extrair números de documentos brasileiros válidos. Os documentos encontrados são 
        armazenados nos resultados do módulo.
        
        O processo inclui:
        1. Verificação da disponibilidade de dados
        2. Extração de todos os tipos de documentos brasileiros
        3. Validação de dígitos verificadores usando a classe Validator
        4. Armazenamento dos resultados únicos encontrados
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        if not (target_value := self.options.get("data")):
            self.log_debug("Nenhum dado fornecido para extração")
            return

        self.log_debug(f"Iniciando extração de documentos brasileiros em texto de {len(target_value)} caracteres")
        
        validate_checksums = self.options.get("validate_checksums", True)
        
        # Extrair todos os tipos de documentos brasileiros
        document_types = ['cpf', 'cnpj', 'rg', 'pis', 'titulo_eleitor', 'cnh']
        
        # Estrutura para armazenar todos os documentos encontrados
        all_extracted = set()
        
        # Processar texto como está e também normalizar para melhorar detecção
        processed_text = self._normalize_text(target_value)
        
        for doc_type in document_types:
            docs = self._extract_by_type(processed_text, doc_type, validate_checksums)
            all_extracted.update(docs)
        
        # Armazenar resultados únicos
        if all_extracted:
            self.log_debug(f"Encontrados {len(all_extracted)} documentos únicos")
            self.set_result("\n".join(sorted(all_extracted)))
        else:
            self.log_debug("Nenhum documento brasileiro encontrado")

    def _extract_by_type(self, text: str, doc_type: str, validate: bool = True) -> set:
        """
        Extrai documentos brasileiros de um tipo específico.
        
        Args:
            text (str): Texto onde buscar documentos
            doc_type (str): Tipo de documento brasileiro para extrair
            validate (bool): Se deve validar checksums
            
        Returns:
            set: Conjunto de documentos encontrados
        """
        results = set()
        patterns = self.document_patterns.get(doc_type, [])
        
        # Mapear tipos de documento para métodos de validação do Validator
        validator_methods = {
            'cpf': Validator.validate_cpf if hasattr(Validator, 'validate_cpf') else None,
            'cnpj': Validator.validate_cnpj if hasattr(Validator, 'validate_cnpj') else None,
            'rg': None,  # RG não tem validador padrão no Validator
            'pis': None,  # PIS não tem validador padrão no Validator
            'titulo_eleitor': Validator.validate_titulo_eleitor if hasattr(Validator, 'validate_titulo_eleitor') else None,
            'cnh': Validator.validate_cnh if hasattr(Validator, 'validate_cnh') else None
        }
        
        # Mapear tipos de documento para rótulos
        doc_type_labels = {
            'cpf': 'CPF',
            'cnpj': 'CNPJ',
            'rg': 'RG',
            'pis': 'PIS/PASEP',
            'titulo_eleitor': 'TÍTULO DE ELEITOR',
            'cnh': 'CNH'
        }
        
        # Verificar comprimentos mínimos para diferentes tipos de documentos
        min_lengths = {'cpf': 11, 'cnpj': 14, 'rg': 7, 'pis': 11, 
                     'titulo_eleitor': 12, 'cnh': 11}
        
        for pattern in patterns:
            compiled_regex = re.compile(pattern, re.IGNORECASE|re.MULTILINE|re.DOTALL)
            matches = re.findall(compiled_regex, text)
            
            for match in matches:
                # Processar o match que pode ser string ou tupla
                if isinstance(match, tuple):
                    doc_match = next((m for m in match if m), "")
                else:
                    doc_match = match
                
                if not doc_match:
                    continue
                
                # Limpar o documento de caracteres não numéricos (exceto X para RG)
                cleaned_doc = self._clean_document(doc_match)
                
                # Verificar comprimento mínimo
                if len(cleaned_doc) < min_lengths.get(doc_type, 4):
                    continue
                
                # Se validação está ativada e existe um método validador para o tipo de documento
                if validate and validator_methods[doc_type]:
                    # Validar usando a classe Validator
                    if validator_methods[doc_type](cleaned_doc):
                        results.add(f"{doc_type_labels[doc_type]}, {cleaned_doc}")
                else:
                    # Sem validação ou sem método validador disponível
                    results.add(f"{doc_type_labels[doc_type]}, {cleaned_doc}")
        
        self.log_debug(f"Extraídos {len(results)} documentos do tipo {doc_type}")
        return results

    def _clean_document(self, document: str) -> str:
        """
        Remove formatação de um documento (pontos, hífens, barras, espaços).
        
        Args:
            document (str): Documento com formatação
            
        Returns:
            str: Documento apenas com números (e 'X' para RG)
        """
        # Preserva X para RGs que usam X como dígito verificador
        if 'X' in document.upper():
            # Substitui todos os caracteres não numéricos exceto X
            cleaned = ''.join(c for c in document.upper() if c.isdigit() or c == 'X')
            return cleaned
            
        # Para outros documentos, remove tudo que não for dígito
        return re.sub(r'[^0-9]', '', document)
    
    def _normalize_text(self, text: str) -> str:
        """
        Normaliza o texto para melhorar a extração de documentos.
        
        Prepara o texto para melhor extração de documentos de diferentes fontes como:
        - SQL dumps
        - HTML
        - Logs
        - Arquivos de texto diversos
        
        Args:
            text (str): Texto original a ser normalizado
            
        Returns:
            str: Texto normalizado para melhor extração de documentos
        """
        if not text:
            return ""
        
        # Processar em etapas para melhor desempenho
        result = text
        
        # 1. Substituir caracteres de escape e HTML entities mais comuns
        escape_mappings = {
            "\\n": " ", "\\r": " ", "\\t": " ", "\\\\": "\\", 
            '\\"': '"', "\\'": "'", "&#039;": "'", "&quot;": '"', 
            "&amp;": "&", "&lt;": "<", "&gt;": ">"
        }
        
        for esc, repl in escape_mappings.items():
            result = result.replace(esc, repl)
        
        # 2. Processamento regex em uma única passagem
        result = re.sub(
            r'<[^>]+>|'              # Remove tags HTML
            r'\s+|'                  # Normaliza espaços
            r'0x[0-9a-fA-F]+|'       # Remove valores hexadecimais
            r'[;:,\[\]\{\}\(\)\|\\_/]',  # Remove caracteres de formatação
            ' ', 
            result
        )
        
        # 3. Adicionar espaço entre números e letras para ajudar na separação
        result = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', result)
        result = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', result)
        
        # 4. Normalizar espaços finais
        result = ' '.join(result.split())
        
        return result
