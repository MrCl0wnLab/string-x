"""
Módulo de extração de cartões de crédito.

Este módulo implementa funcionalidade para extrair e validar números
de cartão de crédito usando algoritmo de Luhn e padrões conhecidos.
"""
import re
from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class CreditCardExtractor(BaseModule):
    """
    Módulo de extração de cartões de crédito.
    
    Esta classe extrai números de cartão de crédito de texto usando:
    - Padrões regex para diferentes bandeiras
    - Validação via algoritmo de Luhn
    - Identificação da bandeira do cartão
    """
    
    def __init__(self):
        """
        Inicializa o módulo de extração de cartões.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Credit Card Extractor',
             "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Extrai e valida números de cartão de crédito',
            'type': 'extraction',
            'example': './strx -l data.txt -module "ext:credit_card" -pm'
        }
        
        self.options = {
            'data': str(),
            'validate_luhn': True,      # Validar usando algoritmo de Luhn
            'include_invalid': False,   # Incluir cartões inválidos
            'mask_output': True,        # Mascarar números nos logs
            'identify_brand': True,     # Identificar bandeira do cartão
            'min_length': 13,          # Comprimento mínimo
            'max_length': 19,          # Comprimento máximo
            'debug': False
        }
        
        # Padrões de cartões por bandeira
        self.card_patterns = {
            'Visa': re.compile(r'4[0-9]{12}(?:[0-9]{3})?'),
            'MasterCard': re.compile(r'5[1-5][0-9]{14}'),
            'American Express': re.compile(r'3[47][0-9]{13}'),
            'Discover': re.compile(r'6(?:011|5[0-9]{2})[0-9]{12}'),
            'Diners Club': re.compile(r'3[0689][0-9]{11}'),
            'JCB': re.compile(r'35(?:2[89]|[3-8][0-9])[0-9]{12}'),
            'Maestro': re.compile(r'(?:5[0678]\\d\\d|6304|6390|67\\d\\d)\\d{8,15}'),
            'UnionPay': re.compile(r'62[0-9]{14,17}')
        }
    
    def run(self):
        """
        Executa extração de cartões de crédito.
        """
        try:
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            
            target_value = Format.clear_value(self.options.get('data', ''))
            
            if not target_value:
                self.log_debug("[x] Dados não fornecidos")
                return
            
            self.log_debug("[*] Iniciando extração de cartões de crédito")
            self.log_debug(f"[*] Processando {len(target_value)} caracteres de dados")
            
            # Configurações
            validate_luhn = self.options.get('validate_luhn', True)
            include_invalid = self.options.get('include_invalid', False)
            identify_brand = self.options.get('identify_brand', True)
            mask_output = self.options.get('mask_output', True)
            
            self.log_debug(f"[*] Validação Luhn: {'[+]' if validate_luhn else '[x]'}, "
                          f"Incluir inválidos: {'[+]' if include_invalid else '[x]'}")
            
            # Extrair possíveis números de cartão
            potential_cards = self._extract_potential_cards(target_value)
            
            if not potential_cards:
                self.log_debug("[!] Nenhum padrão de cartão encontrado")
                return
            
            self.log_debug(f"[+] Encontrados {len(potential_cards)} possíveis cartões")
            
            # Validar e processar cartões
            valid_cards = []
            invalid_cards = []
            
            for card_number in potential_cards:
                card_info = self._process_card(card_number, validate_luhn, identify_brand)
                
                if card_info['valid']:
                    valid_cards.append(card_info)
                    masked = self._mask_card(card_number) if mask_output else card_number
                    self.log_debug(f"   [+] {masked} ({card_info['brand']})")
                else:
                    invalid_cards.append(card_info)
                    if include_invalid:
                        masked = self._mask_card(card_number) if mask_output else card_number
                        self.log_debug(f"   [x] {masked} (inválido)")
            
            # Preparar resultados
            results = valid_cards
            if include_invalid:
                results.extend(invalid_cards)
            
            if results:
                self.log_debug(f"[+] Total de cartões válidos: {len(valid_cards)}")
                if include_invalid and invalid_cards:
                    self.log_debug(f"[!] Total de cartões inválidos: {len(invalid_cards)}")
                
                self._format_results(results)
            else:
                self.log_debug("[!] Nenhum cartão válido encontrado")
                
        except Exception as e:
            self.handle_error(e, "Erro na extração de cartões de crédito")
    
    def _extract_potential_cards(self, text):
        """
        Extrai possíveis números de cartão do texto.
        """
        # Remover espaços, hífens e outros separadores
        clean_text = re.sub(r'[-\\s]', '', text)
        
        # Buscar sequências numéricas que podem ser cartões
        min_len = self.options.get('min_length', 13)
        max_len = self.options.get('max_length', 19)
        
        pattern = f'\\b\\d{{{min_len},{max_len}}}\\b'
        potential_cards = re.findall(pattern, clean_text)
        
        # Remover duplicatas mantendo ordem
        seen = set()
        unique_cards = []
        for card in potential_cards:
            if card not in seen:
                seen.add(card)
                unique_cards.append(card)
        
        return unique_cards
    
    def _process_card(self, card_number, validate_luhn=True, identify_brand=True):
        """
        Processa e valida um número de cartão.
        """
        card_info = {
            'number': card_number,
            'valid': False,
            'brand': 'Unknown',
            'luhn_valid': False
        }
        
        # Identificar bandeira
        if identify_brand:
            card_info['brand'] = self._identify_brand(card_number)
        
        # Validar usando algoritmo de Luhn
        if validate_luhn:
            card_info['luhn_valid'] = self._luhn_validate(card_number)
            card_info['valid'] = card_info['luhn_valid']
        else:
            # Se não validar Luhn, considerar válido se tem padrão conhecido
            card_info['valid'] = card_info['brand'] != 'Unknown'
        
        return card_info
    
    def _identify_brand(self, card_number):
        """
        Identifica a bandeira do cartão.
        """
        for brand, pattern in self.card_patterns.items():
            if pattern.match(card_number):
                return brand
        return 'Unknown'
    
    def _luhn_validate(self, card_number):
        """
        Valida número usando algoritmo de Luhn.
        """
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        
        try:
            return luhn_checksum(card_number) == 0
        except:
            return False
    
    def _mask_card(self, card_number):
        """
        Mascara número do cartão para logs.
        """
        if len(card_number) < 8:
            return '*' * len(card_number)
        
        return card_number[:4] + '*' * (len(card_number) - 8) + card_number[-4:]
    
    def _format_results(self, cards):
        """
        Formata resultados para saída.
        """
        mask_output = self.options.get('mask_output', True)
        
        results = []
        for card in cards:
            number = self._mask_card(card['number']) if mask_output else card['number']
            status = "✓" if card['valid'] else "✗"
            luhn_status = "✓" if card['luhn_valid'] else "✗"
            
            result = f"{number} | {card['brand']} | Valid: {status} | Luhn: {luhn_status}"
            results.append(result)
        
        final_result = f"Credit Cards Found ({len(cards)} total):\n\n"
        final_result += "\n".join(results)
        
        self.set_result(final_result)
