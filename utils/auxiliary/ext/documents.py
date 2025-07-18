"""
Módulo extrator de números de documentos brasileiros.

Este módulo implementa funcionalidade para extrair números de documentos oficiais brasileiros
usando expressões regulares. Suporta CPF, CNPJ, RG, PIS, Título de Eleitor e CNH.
Faz parte do sistema de módulos auxiliares do String-X.
"""
import re
from core.basemodule import BaseModule

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
            'retry_delay': 1,  # Atraso entre tentativas de requisição
        }

        # Padrões regex para documentos brasileiros
        self.document_patterns = {
            'cpf': [
                r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b',  # CPF com ou sem formatação
            ],
            'cnpj': [
                r'\b\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}\b',  # CNPJ com ou sem formatação
            ],
            'rg': [
                r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[0-9X]\b',  # RG formato SP
                r'\b[0-9]{4,9}\b',  # RG formato simples (4-9 dígitos)
            ],
            'pis': [
                r'\b\d{3}\.?\d{5}\.?\d{2}-?\d{1}\b',  # PIS/PASEP
            ],
            'titulo_eleitor': [
                r'\b\d{4}\s?\d{4}\s?\d{4}\b',  # Título de eleitor
            ],
            'cnh': [
                r'\b\d{11}\b',  # CNH (11 dígitos)
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
        3. Validação de dígitos verificadores (quando aplicável)
        4. Armazenamento dos resultados únicos encontrados
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        if not (target_value := self.options.get("data")):
            self.log_debug("Nenhum dado fornecido para extração")
            return

        self.log_debug(f"Iniciando extração de documentos brasileiros em texto de {len(target_value)} caracteres")
        
        results = set()
        validate_checksums = self.options.get("validate_checksums", True)
        
        # Extrair todos os tipos de documentos brasileiros
        document_types = ['cpf', 'cnpj', 'rg', 'pis', 'titulo_eleitor', 'cnh']
        
        for doc_type in document_types:
            extracted = self._extract_by_type(target_value, doc_type, validate_checksums)
            results.update(extracted)
        
        # Armazenar resultados únicos
        if results:
            self.log_debug(f"Encontrados {len(results)} documentos únicos")
            for document in sorted(results):
                self.set_result(document)
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
        
        for pattern in patterns:
            compiled_regex = re.compile(pattern, re.IGNORECASE)
            matches = re.findall(compiled_regex, text)
            
            for match in matches:
                # Limpar e validar o documento
                cleaned_doc = self._clean_document(match)
                
                if validate:
                    if doc_type == 'cpf' and self._validate_cpf(cleaned_doc):
                        results.add(f"CPF, {self._format_cpf(cleaned_doc)}")
                    elif doc_type == 'cnpj' and self._validate_cnpj(cleaned_doc):
                        results.add(f"CNPJ, {self._format_cnpj(cleaned_doc)}")
                    elif doc_type == 'rg' and self._validate_rg(cleaned_doc):
                        results.add(f"RG, {self._format_rg(cleaned_doc)}")
                    elif doc_type in ['pis', 'cnh', 'titulo_eleitor']:
                        # Para outros tipos sem validação específica
                        results.add(f"{doc_type.upper()}, {match}")
                #else:
                    # Adicionar sem validação
                #    results.add(f"{doc_type.upper()}, {match}")
                    
        self.log_debug(f"Extraídos {len(results)} documentos do tipo {doc_type}")
        return results

    def _clean_document(self, document: str) -> str:
        """
        Remove formatação de um documento (pontos, hífens, barras, espaços).
        
        Args:
            document (str): Documento com formatação
            
        Returns:
            str: Documento apenas com números
        """
        return re.sub(r'[^0-9]', '', document)

    def _validate_cpf(self, cpf: str) -> bool:
        """
        Valida um CPF usando o algoritmo de dígitos verificadores.
        
        Args:
            cpf (str): CPF apenas com números
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Calcular primeiro dígito verificador
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Calcular segundo dígito verificador
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return int(cpf[9]) == digit1 and int(cpf[10]) == digit2

    def _validate_cnpj(self, cnpj: str) -> bool:
        """
        Valida um CNPJ usando o algoritmo de dígitos verificadores.
        
        Args:
            cnpj (str): CNPJ apenas com números
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        # Pesos para o cálculo
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # Calcular primeiro dígito verificador
        sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Calcular segundo dígito verificador
        sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2
    
    def _validate_rg(self, rg: str) -> bool:
        """
        Valida um número de RG (Registro Geral) com dígito verificador.

        Args:
            rg (str): O número de RG a ser validado (sem pontos ou traços).

        Returns:
            bool: True se o RG for válido, False caso contrário.
        """
        if len(rg) != 9:
            return False

        try:
            # Calcula o dígito verificador
            soma = 0
            for i in range(8):
                soma += int(rg[i]) * (10 - (i + 1))
            resto = soma % 11
            dv = 11 - resto

            # Trata o caso especial onde dv é 10 (o dígito verificador é 'X')
            if dv == 10 and rg[8] == 'X':
                return True
            elif dv == int(rg[8]):
                return True
            else:
                return False
        except ValueError:
            return False


    def _format_cpf(self, cpf: str) -> str:
        """Formata CPF no padrão XXX.XXX.XXX-XX"""
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def _format_cnpj(self, cnpj: str) -> str:
        """Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX"""
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    
    def _format_rg(self, rg:str):
        """
        Formata um número de RG no formato XX.XXX.XXX-Y.

        Args:
            rg_str: Uma string representando o número do RG (sem formatação).

        Returns:
            Uma string formatada do RG, ou a própria string original se não for possível formatar.
        """
        try:
            # Remove caracteres não numéricos
            rg_str = ''.join(filter(str.isdigit, rg))

            if len(rg_str) == 9:
                return f"{rg_str[:2]}.{rg_str[2:5]}.{rg_str[5:8]}-{rg_str[8]}"
            elif len(rg_str) == 8:
                return f"{rg_str[:2]}.{rg_str[2:5]}.{rg_str[5:8]}-" + self._calc_dig_verif(rg_str)

            elif len(rg_str) < 8:
                return rg_str
            else:
                return rg_str
        except (ValueError, IndexError):
            return rg_str
        
    def _calc_dig_verif(rg_str):
        """
        Calcula o dígito verificador do RG.

        Args:
            rg_str: Uma string com os 8 primeiros dígitos do RG.

        Returns:
            O dígito verificador como uma string.
        """
        if len(rg_str) != 8:
            return "Inválido"

        soma = 0
        multiplicadores = [9, 8, 7, 6, 5, 4, 3, 2]
        for i, num in enumerate(rg_str):
            soma += int(num) * multiplicadores[i]
        resto = soma % 11
        if resto == 10:
            return "X"
        else:
            return str(resto)
