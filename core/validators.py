import re
import base64
import ipaddress
from typing import List, Tuple, Optional
from urllib.parse import urlparse

class Validator:
    """Input validator for String-X.
    
    This class provides static methods to validate various types of input data,
    including Brazilian documents, international identifiers, and general formats.
    All methods are stateless and return boolean values indicating validity.
    """
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validates a URL format and basic structure.
        
        Args:
            url (str): The URL to validate.
            
        Returns:
            bool: True if the URL is valid and uses http/https protocol, False otherwise.
            
        Example:
            >>> validate_url("https://example.com")
            >>> validate_url("http://sub.domain.com/path")
        """
        if not url:
            return False
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False
            if result.scheme not in ['http', 'https']:
                return False
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """
        Validates an IP address (IPv4 or IPv6).
        
        Args:
            ip (str): The IP address to validate.
            
        Returns:
            bool: True if the IP address is valid, False otherwise.
            
        Example:
            >>> validate_ip("192.168.1.1")
            >>> validate_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        """
        if not ip:
            return False
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_domain(domain: str) -> bool:
        """
        Validates a domain name format.
        
        Args:
            domain (str): The domain name to validate.
            
        Returns:
            bool: True if the domain format is valid, False otherwise.
            
        Example:
            >>> validate_domain("example.com")
            >>> validate_domain("sub.domain.co.uk")
        """
        if not domain:
            return False
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        if re.match(pattern, domain):
            return True
        return False
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validates an email address format.
        
        Args:
            email (str): The email address to validate.
            
        Returns:
            bool: True if the email format is valid, False otherwise.
            
        Example:
            >>> validate_email("user@example.com")
            >>> validate_email("name.surname+tag@domain.co.uk")
        """
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        return False
    
    @staticmethod
    def validate_mac(mac: str) -> bool:
        """
        Validates a MAC address format.
        
        Args:
            mac (str): The MAC address to validate.
            
        Returns:
            bool: True if the MAC address format is valid, False otherwise.
            
        Example:
            >>> validate_mac("00:11:22:33:44:55")
            >>> validate_mac("00-11-22-33-44-55")
        """
        if not mac:
            return False
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if re.match(pattern, mac):
            return True
        return False
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validates a phone number format.
        Supports Brazilian phone numbers with or without country code.
        
        Args:
            phone (str): The phone number to validate.
            
        Returns:
            bool: True if the phone number format is valid, False otherwise.
            
        Example:
            >>> validate_phone("+5511999999999")
            >>> validate_phone("11999999999")
            >>> validate_phone("1155554444")
        """
        if not phone:
            return False
        # Remove common separators and spaces to normalize the input
        if phone := ''.join(filter(str.isdigit, phone)).strip():
            # Regular expression for landline and mobile numbers
            regx = r"^(?:[14689][0-9]|2[12478]|3([1-5]|[7-8])|5([13-5])|7[193-7])9?[0-9]{8}$"
            match = re.match(regx, phone)
            return bool(match)
        return False
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """
        Valida um CNPJ.

        Args:
            cnpj (str): O CNPJ a ser validado (com ou sem máscara).

        Returns:
            bool: True se o CNPJ for válido, False caso contrário.
        """
     
        if not cnpj:
            return False
        
        # Remove caracteres não numéricos
        if cnpj := ''.join(filter(str.isdigit, cnpj)).strip():

            if len(cnpj) != 14:
                return False
            
            # Verifica se todos os dígitos são iguais
            if len(set(cnpj)) == 1:
                return False
            try:
                # Validação dos dígitos verificadores
                def calcula_digito(cnpj_base):
                    # Pesos para cálculo do primeiro dígito: 5,4,3,2,9,8,7,6,5,4,3,2
                    # Pesos para cálculo do segundo dígito: 6,5,4,3,2,9,8,7,6,5,4,3,2
                    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
                    soma = 0
                    
                    # Ajusta os pesos com base no tamanho do CNPJ base (12 ou 13 dígitos)
                    peso_inicial = len(pesos) - len(cnpj_base)
                    
                    for i, digito in enumerate(cnpj_base):
                        soma += int(digito) * pesos[peso_inicial + i]
                        
                    resto = soma % 11
                    return '0' if resto < 2 else str(11 - resto)

                # Primeiro dígito verificador
                cnpj_base = cnpj[:12]
                primeiro_dv = calcula_digito(cnpj_base)
                if primeiro_dv != cnpj[12]:
                    return False

                # Segundo dígito verificador
                cnpj_base = cnpj[:12] + primeiro_dv
                segundo_dv = calcula_digito(cnpj_base)
                if segundo_dv != cnpj[13]:
                    return False

                return True
            except Exception as e:
                print(f"Erro ao validar CNPJ: {e}")
                return False
                               
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """
        Valida um CPF usando o algoritmo de dígitos verificadores.
        
        Args:
            cpf (str): CPF apenas com números
            
        Returns:
            bool: True se válido, False caso contrário
            
        Example:
            >>> validate_cpf("12345678909")
            >>> validate_cpf("123.456.789-09")
        """
        # Remove caracteres não numéricos
        cpf_clean = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf_clean) != 11 or cpf_clean == cpf_clean[0] * 11:
            return False
        
        # Calcular primeiro dígito verificador
        sum1 = sum(int(cpf_clean[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Calcular segundo dígito verificador
        sum2 = sum(int(cpf_clean[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return int(cpf_clean[9]) == digit1 and int(cpf_clean[10]) == digit2
        
    @staticmethod
    def validate_hash(hash_value: str, hash_type: str = "auto") -> bool:
        """
        Validates cryptographic hash formats.
        
        Args:
            hash_value (str): The hash string to validate.
            hash_type (str, optional): The type of hash to validate ('md5', 'sha1', 'sha256', 'sha512', or 'auto').
                                     When 'auto', the type is inferred from the length. Defaults to "auto".
            
        Returns:
            bool: True if the hash format is valid for the specified type, False otherwise.
            
        Example:
            >>> validate_hash("5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "sha256")
            >>> validate_hash("d41d8cd98f00b204e9800998ecf8427e")  # auto-detects MD5
        """
        if not hash_value:
            return False
        
        hash_patterns = {
            'md5': r'^[a-fA-F0-9]{32}$',
            'sha1': r'^[a-fA-F0-9]{40}$', 
            'sha256': r'^[a-fA-F0-9]{64}$',
            'sha512': r'^[a-fA-F0-9]{128}$'
        }
        
        if hash_type == "auto":
            # Auto-detect based on length
            length = len(hash_value)
            type_map = {32: 'md5', 40: 'sha1', 64: 'sha256', 128: 'sha512'}
            hash_type = type_map.get(length, '')
        
        pattern = hash_patterns.get(hash_type.lower())
        if pattern and re.match(pattern, hash_value):
            return True
        return False
    
    @staticmethod
    def validate_jwt_token(token: str) -> bool:
        """
        Validates the basic format of a JWT token.
        Does not verify the signature, only checks the structure.
        
        Args:
            token (str): The JWT token to validate.
            
        Returns:
            bool: True if the token has valid JWT format, False otherwise.
            
        Example:
            >>> validate_jwt_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U")
        """
        if not token:
            return False
        
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        # Verify each part is valid base64
        try:
            for part in parts:
                # Add padding if necessary
                padded = part + '=' * (4 - len(part) % 4)
                base64.urlsafe_b64decode(padded)
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_uuid(uuid_string: str, version: int = None) -> bool:
        """
        Validates a UUID string format.
        
        Args:
            uuid_string (str): The UUID string to validate.
            version (int, optional): The UUID version to validate against (1-5).
                                   If None, any version is accepted. Defaults to None.
            
        Returns:
            bool: True if the UUID format is valid and matches the specified version (if any), False otherwise.
            
        Example:
            >>> validate_uuid("123e4567-e89b-12d3-a456-426614174000")
            >>> validate_uuid("123e4567-e89b-12d3-a456-426614174000", version=1)
        """
        if not uuid_string:
            return False
        
        uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        
        if not re.match(uuid_pattern, uuid_string):
            return False
        
        if version:
            version_char = uuid_string[14]  # Version digit position
            if version_char != str(version):
                return False
        
        return True
    
    @staticmethod
    def validate_base64(encoded_string: str) -> bool:
        """
        Validates if a string is valid base64 encoded.
        
        Args:
            encoded_string (str): The string to validate as base64.
            
        Returns:
            bool: True if the string is valid base64, False otherwise.
            
        Example:
            >>> validate_base64("SGVsbG8gV29ybGQ=")
        """
        if not encoded_string:
            return False
        
        try:
            if isinstance(encoded_string, str):
                encoded_string = encoded_string.encode('ascii')
            decoded = base64.b64decode(encoded_string, validate=True)
            return base64.b64encode(decoded).decode('ascii') == encoded_string.decode('ascii')
        except Exception:
            return False


    @staticmethod
    def validate_hex_color(color: str) -> bool:
        """
        Valida cor hexadecimal (#RRGGBB ou #RGB)

        Args:
            color (str): A cor hexadecimal a ser validada (com ou sem '#').

        Returns:
            bool: True se a cor for válida, False caso contrário.
        """
        if not color:
            return False
        
        patterns = [
            r'^#[0-9a-fA-F]{6}$',  # #RRGGBB
            r'^#[0-9a-fA-F]{3}$'   # #RGB
        ]
        
        return any(re.match(pattern, color) for pattern in patterns)
 
    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """
        Validates ISBN-10 and ISBN-13 numbers.
        
        Args:
            isbn (str): The ISBN number to validate, with or without formatting.
            
        Returns:
            bool: True if the ISBN is valid, False otherwise.
            
        Example:
            >>> validate_isbn("0-7475-3269-9")  # ISBN-10
            >>> validate_isbn("978-0-7475-3269-9")  # ISBN-13
        """
        if not isbn:
            return False
        
        # Remove non-alphanumeric characters
        isbn_clean = re.sub(r'[^0-9X]', '', isbn.upper())
        
        if len(isbn_clean) == 10:
            # ISBN-10
            try:
                total = 0
                for i in range(9):
                    total += int(isbn_clean[i]) * (10 - i)
                
                check_digit = isbn_clean[9]
                remainder = total % 11
                
                if remainder == 0:
                    return check_digit == '0'
                elif remainder == 1:
                    return check_digit == 'X'
                else:
                    return check_digit == str(11 - remainder)
            except ValueError:
                return False
                
        elif len(isbn_clean) == 13:
            # ISBN-13
            try:
                total = 0
                for i in range(12):
                    weight = 1 if i % 2 == 0 else 3
                    total += int(isbn_clean[i]) * weight
                
                check_digit = int(isbn_clean[12])
                remainder = total % 10
                expected = 0 if remainder == 0 else 10 - remainder
                
                return check_digit == expected
            except ValueError:
                return False
        
        return False

    @staticmethod
    def validate_iban(iban: str) -> bool:
        """
        Valida IBAN (International Bank Account Number)

        Args:  
            iban (str): O IBAN a ser validado (com ou sem espaços).

        Returns:
            bool: True se o IBAN for válido, False caso contrário.
        """
        if not iban:
            return False
        
        # Remove espaços e converte para maiúscula
        iban_clean = re.sub(r'\s', '', iban.upper())
        
        # Verifica comprimento (15-34 caracteres)
        if len(iban_clean) < 15 or len(iban_clean) > 34:
            return False
        
        # Verifica formato básico (2 letras + 2 dígitos + alfanumérico)
        if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z0-9]+$', iban_clean):
            return False
        
        # Algoritmo de validação mod-97
        try:
            # Move os primeiros 4 caracteres para o final
            rearranged = iban_clean[4:] + iban_clean[:4]
            
            # Substitui letras por números (A=10, B=11, ..., Z=35)
            numeric_string = ''
            for char in rearranged:
                if char.isalpha():
                    numeric_string += str(ord(char) - ord('A') + 10)
                else:
                    numeric_string += char
            
            # Verifica se o resto da divisão por 97 é 1
            return int(numeric_string) % 97 == 1
        except ValueError:
            return False
        

    @staticmethod
    def validate_rg(rg: str) -> bool:
        """
        Valida RG brasileiro (formato SP com dígito verificador)

        Args:
            rg (str): O RG a ser validado (com ou sem máscara).

        Returns:
            bool: True se o RG for válido, False caso contrário.
        """
        if not rg:
            return False
        
        # Remove caracteres não numéricos e X
        rg_clean = re.sub(r'[^0-9X]', '', rg.upper())
        
        if len(rg_clean) != 9:
            return False
        
        try:
            # Calcula o dígito verificador
            soma = 0
            for i in range(8):
                soma += int(rg_clean[i]) * (9 - i)
            
            resto = soma % 11
            if resto < 2:
                dv = 0
            else:
                dv = 11 - resto
            
            # Verifica dígito verificador
            if dv == 10:
                return rg_clean[8] == 'X'
            else:
                return int(rg_clean[8]) == dv
        except (ValueError, IndexError):
            return False

    @staticmethod
    def validate_pis(pis: str) -> bool:
        """
        Valida um número de PIS/PASEP.
        
        Args:
            pis (str): PIS apenas com números
            
        Returns:
            bool: True se válido, False caso contrário
            
        Example:
            >>> validate_pis("12345678909")
            >>> validate_pis("123.45678.90-9")
        """
        # Remove caracteres não numéricos
        pis_clean = re.sub(r'[^0-9]', '', pis)
        
        if len(pis_clean) != 11:
            return False
            
        if pis_clean == pis_clean[0] * 11:
            return False
            
        # Pesos para o cálculo
        weights = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # Calcular dígito verificador
        soma = sum(int(pis_clean[i]) * weights[i] for i in range(10))
        resto = soma % 11
        dv = 11 - resto if resto != 0 and resto != 1 else 0
        
        return int(pis_clean[10]) == dv

    @staticmethod
    def validate_litecoin_address(address: str) -> bool:
        """
        Valida endereços Litecoin (Legacy e Bech32)

        Args:
            address (str): O endereço Litecoin a ser validado.
        
        Returns:
            bool: True se o endereço for válido, False caso contrário.
        """
        if not address:
            return False
        
        patterns = [
            r'^[LM][a-km-zA-HJ-NP-Z1-9]{26,33}$',  # Legacy addresses
            r'^ltc1[a-z0-9]{39,59}$',  # Bech32 addresses
        ]
        
        return any(re.match(pattern, address) for pattern in patterns)

    @staticmethod
    def validate_monero_address(address: str) -> bool:
        """
        Valida endereços Monero

        Args:
            address (str): O endereço Monero a ser validado.
        
        Returns:
            bool: True se o endereço for válido, False caso contrário.
        """
        if not address:
            return False
        
        # Endereços Monero começam com 4 ou 8 e têm 95 caracteres
        pattern = r'^[48][a-zA-Z0-9]{94}$'
        return bool(re.match(pattern, address))

    @staticmethod
    def validate_cnh(cnh: str) -> bool:
        """
        Valida Carteira Nacional de Habilitação (CNH)

        Args:
            cnh (str): A CNH a ser validada (com ou sem máscara).
        
        Returns:
            bool: True se a CNH for válida, False caso contrário.
        """
        if not cnh:
            return False
        
        # Remove caracteres não numéricos
        cnh_clean = re.sub(r'\D', '', cnh)
        
        if len(cnh_clean) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if len(set(cnh_clean)) == 1:
            return False
        
        try:
            # Calcula primeiro dígito verificador
            soma1 = 0
            sequencia = list(range(9, 0, -1))
            
            for i in range(9):
                soma1 += int(cnh_clean[i]) * sequencia[i]
            
            resto1 = soma1 % 11
            dv1 = 0 if resto1 < 2 else 11 - resto1
            
            # Calcula segundo dígito verificador
            soma2 = 0
            sequencia2 = list(range(1, 10))
            
            for i in range(9):
                soma2 += int(cnh_clean[i]) * sequencia2[i]
            
            soma2 += dv1 * 2
            resto2 = soma2 % 11
            dv2 = 0 if resto2 < 2 else 11 - resto2
            
            return int(cnh_clean[9]) == dv1 and int(cnh_clean[10]) == dv2
        except (ValueError, IndexError):
            return False

    @staticmethod
    def validate_cep(cep: str) -> bool:
        """
        Valida CEP brasileiro (XXXXX-XXX)
        
        Args:
            cep (str): O CEP a ser validado (com ou sem máscara).
        
        Returns:
            bool: True se o CEP for válido, False caso contrário.
        """
        if not cep:
            return False
        
        # Remove caracteres não numéricos
        cep_clean = re.sub(r'\D', '', cep)
        
        # Verifica se tem 8 dígitos
        if len(cep_clean) != 8:
            return False
        
        # Verifica se não é sequência inválida (00000000, 11111111, etc.)
        if len(set(cep_clean)) == 1:
            return False
        
        return True

    @staticmethod
    def validate_renavam(renavam: str) -> bool:
        """
        Validates Brazilian Vehicle Registration (RENAVAM).
        
        Args:
            renavam (str): The RENAVAM number to validate, with or without formatting.
            
        Returns:
            bool: True if the RENAVAM is valid, False otherwise.
            
        Example:
            >>> validate_renavam("00123456789")
            >>> validate_renavam("123.456.789-0")
        """
        if not renavam:
            return False
        
        # Remove caracteres não numéricos
        renavam_clean = re.sub(r'\D', '', renavam)
        
        if len(renavam_clean) != 11:
            return False
        
        try:
            # Sequência de multiplicadores para cálculo
            sequencia = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            
            # Calcula soma ponderada dos 10 primeiros dígitos
            soma = sum(int(renavam_clean[i]) * sequencia[i] for i in range(10))
            
            # Calcula dígito verificador
            resto = soma % 11
            dv = 0 if resto in [0, 1] else 11 - resto
            
            return int(renavam_clean[10]) == dv
        except (ValueError, IndexError):
            return False

    @staticmethod
    def validate_placa_veiculo(placa: str) -> bool:
        """
        Validates Brazilian vehicle license plates (old format and Mercosul format).
        
        Args:
            placa (str): The license plate to validate, with or without formatting.
            
        Returns:
            bool: True if the license plate format is valid, False otherwise.
            
        Example:
            >>> validate_placa_veiculo("ABC1234")  # Old format
            >>> validate_placa_veiculo("ABC1D23")  # Mercosul format
            >>> validate_placa_veiculo("ABC-1234") # Old format with hyphen
        """
        if not placa:
            return False
        
        placa_clean = placa.upper().strip()
        
        # Formato antigo: AAA-9999
        formato_antigo = r'^[A-Z]{3}-?\d{4}$'
        
        # Formato Mercosul: AAA9A99
        formato_mercosul = r'^[A-Z]{3}\d[A-J]\d{2}$'
        
        return bool(re.match(formato_antigo, placa_clean) or 
                   re.match(formato_mercosul, placa_clean))

    @staticmethod
    def validate_passaporte_brasileiro(passaporte: str) -> bool:
        """
        Validates Brazilian passport numbers.
        
        Args:
            passaporte (str): The passport number to validate.
            
        Returns:
            bool: True if the passport number format is valid, False otherwise.
            
        Example:
            >>> validate_passaporte_brasileiro("AA123456")
            >>> validate_passaporte_brasileiro("FD789456")
        """
        if not passaporte:
            return False
        
        passaporte_clean = passaporte.upper().strip()
        pattern = r'^[A-Z]{2}\d{6}$'
        
        return bool(re.match(pattern, passaporte_clean))

    @staticmethod
    def validate_rne(rne: str) -> bool:
        """
        Validates Brazilian Foreign National Registration (RNE).
        
        Args:
            rne (str): The RNE number to validate, with or without formatting.
            
        Returns:
            bool: True if the RNE format is valid, False otherwise.
            
        Example:
            >>> validate_rne("RNEW123456X")
            >>> validate_rne("RNE123456-7")
        """
        if not rne:
            return False
        
        rne_clean = rne.upper().replace(' ', '').replace('-', '').replace('.', '')
        pattern = r'^RNE[A-Z\d]\d{6}[A-Z\d]$'
        
        return bool(re.match(pattern, rne_clean))

    @staticmethod
    def validate_crm(crm: str) -> bool:
        """
        Validates Brazilian Medical License (CRM).
        
        Args:
            crm (str): The CRM number to validate, with or without formatting.
            
        Returns:
            bool: True if the CRM format is valid, False otherwise.
            
        Example:
            >>> validate_crm("123456SP")
            >>> validate_crm("12345-SP")
            >>> validate_crm("12.345 SP")
        """
        if not crm:
            return False
        
        # Formato: números seguidos de sigla do estado (ex: 12345SP)
        pattern = r'^[0-9\-\/]{4,11}[A-Z]{2}$'
        crm_clean = crm.upper().replace(' ', '')
        
        return bool(re.match(pattern, crm_clean))

    @staticmethod
    def validate_processo_cnj(processo: str) -> bool:
        """
        Validates Brazilian Legal Process Number (CNJ format).
        
        Args:
            processo (str): The process number to validate, with or without formatting.
            
        Returns:
            bool: True if the process number format is valid, False otherwise.
            
        Example:
            >>> validate_processo_cnj("0123456-78.2019.8.26.0100")
            >>> validate_processo_cnj("01234567820198260100")
        
        Note:
            Format: NNNNNNN-DD.AAAA.J.TR.OOOO where:
            - NNNNNNN: Sequential number
            - DD: Check digits
            - AAAA: Year
            - J: Court segment (4-8)
            - TR: Court identifier
            - OOOO: Court unit
        """
        if not processo:
            return False
        
        # Remove caracteres de formatação
        processo_clean = re.sub(r'[^\d]', '', processo)
        
        if len(processo_clean) != 20:
            return False
        
        # Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
        pattern = r'^\d{7}-?\d{2}\.?\d{4}\.?[4-8]\.?\d{2}\.?\d{4}$'
        
        # Verifica com formatação original
        return bool(re.match(pattern, processo))

    @staticmethod
    def validate_pix_key(key: str) -> bool:
        """
        Validates Brazilian PIX payment system keys.
        
        Args:
            key (str): The PIX key to validate (CPF, CNPJ, email, phone, or random key).
            
        Returns:
            bool: True if the PIX key format is valid, False otherwise.
            
        Example:
            >>> validate_pix_key("12345678901")  # CPF
            >>> validate_pix_key("email@domain.com")  # Email
            >>> validate_pix_key("+5511999999999")  # Phone
            >>> validate_pix_key("123e4567-e89b-12d3-a456-426655440000")  # Random
        """
        if not key:
            return False
        
        pattern = r'([0-9]{14,20})([bB][rR]\.[gG][oO][vV]\.[bB][cC][bB]\.[pP][iI][xX]).*(6304)([0-9a-zA-Z]{4})'
        key_clean = key.lower().strip()
        return bool(re.match(pattern, key_clean))

    @staticmethod
    def validate_chave_pix_aleatoria(chave: str) -> bool:
        """Valida chave PIX aleatória (formato UUID)"""
        if not chave:
            return False
        
        pattern = r'^[a-z\d]{8}-[a-z\d]{4}-[a-z\d]{4}-[a-z\d]{4}-[a-z\d]{12}$'
        chave_clean = chave.lower().strip()
        
        return bool(re.match(pattern, chave_clean))

    @staticmethod
    def validate_boleto_bancario(boleto: str) -> bool:
        """
        Validates Brazilian bank slip numbers (boleto bancário).
        
        Args:
            boleto (str): The bank slip number to validate, with or without formatting.
            
        Returns:
            bool: True if the bank slip number format is valid, False otherwise.
            
        Example:
            >>> validate_boleto_bancario("23790.12345 67890.123456 78901.234567 8 12345678901234")
            >>> validate_boleto_bancario("23790123456789012345678901234567890123456789012345")
        
        Note:
            Accepts three formats:
            - 47 digits
            - 48 digits
            - 4 groups of 12 digits
        """
        if not boleto:
            return False
        
        # Remove espaços e pontos
        boleto_clean = re.sub(r'[\s\.]', '', boleto)
        
        # Três formatos possíveis
        patterns = [
            r'^\d{47}$',  # 47 dígitos
            r'^\d{48}$',  # 48 dígitos
            r'^\d{12}\d{12}\d{12}\d{12}$'  # 4 grupos de 12 dígitos
        ]
        
        return any(re.match(pattern, boleto_clean) for pattern in patterns)

    @staticmethod
    def validate_correios_tracking(codigo: str) -> bool:
        """
        Validates Brazilian Postal Service (Correios) tracking codes.
        
        Args:
            codigo (str): The tracking code to validate.
            
        Returns:
            bool: True if the tracking code format is valid, False otherwise.
            
        Example:
            >>> validate_correios_tracking("AA123456789BR")
            >>> validate_correios_tracking("LB987654321BR")
            
        Note:
            Format: Two letters + 9 digits + BR
        """
        if not codigo:
            return False
        
        codigo_clean = codigo.upper().strip()
        pattern = r'^[A-Z]{2}\d{9}BR$'
        
        return bool(re.match(pattern, codigo_clean))


    @staticmethod
    def validate_inscricao_estadual_sp(ie: str) -> bool:
        """
        Validates São Paulo State Tax ID (Inscrição Estadual).
        
        Args:
            ie (str): The state tax ID to validate, with or without formatting.
            
        Returns:
            bool: True if the state tax ID is valid, False otherwise.
            
        Example:
            >>> validate_inscricao_estadual_sp("110.042.490.114")
            >>> validate_inscricao_estadual_sp("110042490114")
        
        Note:
            Format: 12 digits with two check digits (positions 9 and 12)
        """
        if not ie:
            return False
        
        # Remove caracteres não numéricos
        ie_clean = re.sub(r'\D', '', ie)
        
        if len(ie_clean) != 12:
            return False
        
        try:
            # Calcula primeiro dígito verificador
            soma1 = 0
            pesos1 = [1, 3, 4, 5, 6, 7, 8, 10]
            
            for i in range(8):
                soma1 += int(ie_clean[i]) * pesos1[i]
            
            resto1 = soma1 % 11
            dv1 = 11 - resto1 if resto1 > 1 else 0
            
            # Calcula segundo dígito verificador
            soma2 = 0
            pesos2 = [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2]
            
            for i in range(11):
                if i == 8:
                    soma2 += dv1 * pesos2[i]
                else:
                    soma2 += int(ie_clean[i]) * pesos2[i]
            
            resto2 = soma2 % 11
            dv2 = 11 - resto2 if resto2 > 1 else 0
            
            return (int(ie_clean[8]) == dv1 and 
                   int(ie_clean[11]) == dv2)
        except (ValueError, IndexError):
            return False


    @staticmethod
    def validate_uf_sigla(uf: str) -> bool:
        """Valida sigla de Unidade Federativa brasileira"""
        if not uf:
            return False
        
        ufs_validas = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', 'BR'
        }
        
        return uf.upper().strip() in ufs_validas

    @staticmethod
    def validate_cartao_sus(cns: str) -> bool:
        """Valida Cartão Nacional de Saúde (CNS)"""
        if not cns:
            return False
        
        # Remove caracteres não numéricos
        cns_clean = re.sub(r'\D', '', cns)
        
        if len(cns_clean) != 15:
            return False
        
        # Verifica se começa com 1 ou 2 (cartão definitivo) ou 7, 8 ou 9 (provisório)
        if not cns_clean[0] in '12789':
            return False
            
        try:
            soma = 0
            for i in range(0, 15):
                soma += int(cns_clean[i]) * (15 - i)
            
            return (soma % 11) == 0
        except (ValueError, IndexError):
            return False

    @staticmethod
    def validate_titulo_eleitor(titulo: str) -> bool:
        """Valida Título de Eleitor"""
        if not titulo:
            return False
        
        # Remove caracteres não numéricos
        titulo_clean = re.sub(r'\D', '', titulo)
        
        if len(titulo_clean) != 12:
            return False
            
        try:
            # Validação do primeiro dígito verificador
            soma1 = 0
            for i in range(8):
                soma1 += int(titulo_clean[i]) * (9 - i)
            
            resto1 = soma1 % 11
            if resto1 == 10:
                resto1 = 0
            if int(titulo_clean[10]) != resto1:
                return False
            
            # Validação do segundo dígito verificador
            soma2 = 0
            for i in range(8, 11):
                soma2 += int(titulo_clean[i]) * (4 - (i - 8))
            
            resto2 = soma2 % 11
            if resto2 == 10:
                resto2 = 0
            
            return int(titulo_clean[11]) == resto2
        except (ValueError, IndexError):
            return False

    @staticmethod
    def validate_crea(crea: str) -> bool:
        """Valida número de registro CREA"""
        if not crea:
            return False
        
        # Formato: número + UF (ex: 123456SP)
        pattern = r'^\d{6,8}[A-Z]{2}$'
        crea_clean = crea.upper().replace(' ', '').replace('-', '').replace('.', '')
        
        if not re.match(pattern, crea_clean):
            return False
            
        # Verifica se a UF é válida
        uf = crea_clean[-2:]
        ufs_validas = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        }
        
        return uf in ufs_validas

    @staticmethod
    def validate_oab(oab: str) -> bool:
        """Valida número de registro OAB"""
        if not oab:
            return False
        
        # Formato: número + UF (ex: 123456SP)
        pattern = r'^\d{3,6}[A-Z]{2}$'
        oab_clean = oab.upper().replace(' ', '').replace('-', '').replace('.', '')
        
        if not re.match(pattern, oab_clean):
            return False
            
        # Verifica se a UF é válida
        uf = oab_clean[-2:]
        ufs_validas = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        }
        
        return uf in ufs_validas

    @staticmethod
    def validate_ipv4_range(ip_range: str) -> bool:
        """
        Validates an IPv4 CIDR range format.
        
        Args:
            ip_range (str): The IP range to validate in CIDR notation.
            
        Returns:
            bool: True if the IP range format is valid, False otherwise.
            
        Example:
            >>> validate_ipv4_range("192.168.0.0/24")
            >>> validate_ipv4_range("10.0.0.0/8")
        """
        if not ip_range:
            return False
        
        try:
            network = ipaddress.IPv4Network(ip_range, strict=False)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_domain_br(domain: str) -> bool:
        """
        Validates Brazilian domain names (.br TLDs).
        
        Args:
            domain (str): The domain name to validate.
            
        Returns:
            bool: True if the domain ends with a valid Brazilian TLD, False otherwise.
            
        Example:
            >>> validate_domain_br("example.com.br")
            >>> validate_domain_br("site.gov.br")
        """
        if not domain:
            return False
        
        # Lista de TLDs brasileiros comuns
        br_tlds = [
            'com.br', 'net.br', 'org.br', 'gov.br', 'edu.br', 
            'mil.br', 'esp.br', 'leg.br', 'jus.br', 'mp.br',
            'wiki.br', 'blog.br', 'adm.br', 'adv.br', 'arq.br',
            'ato.br', 'bio.br', 'bmd.br', 'cim.br', 'cng.br',
            'cnt.br', 'ecn.br', 'eng.br', 'eti.br', 'far.br',
            'fnd.br', 'fot.br', 'fst.br', 'ggf.br', 'jor.br',
            'lel.br', 'mat.br', 'med.br', 'mus.br', 'not.br',
            'ntr.br', 'odo.br', 'ppg.br', 'pro.br', 'psc.br',
            'qsl.br', 'radio.br', 'slg.br', 'trd.br', 'vet.br',
            'zlg.br', 'nom.br', 'agr.br', 'art.br', 'can.br',
            'coop.br', 'def.br', 'emp.br', 'flog.br', 'imb.br',
            'ind.br', 'inf.br', 'rec.br', 'srv.br', 'tmp.br',
            'tur.br', 'tv.br', 'vlog.br'
        ]
        
        domain = domain.lower().strip()
        return any(domain.endswith('.' + tld) for tld in br_tlds)
    
    @staticmethod
    def validate_phone_br_type(phone: str) -> tuple[bool, str]:
        """
        Validates Brazilian phone numbers and identifies their type.
        
        Args:
            phone (str): The phone number to validate.
            
        Returns:
            tuple[bool, str]: A tuple containing:
                - bool: True if the phone number is valid, False otherwise
                - str: The type of phone number ('celular', 'fixo', 'especial', or 'inválido')
            
        Example:
            >>> validate_phone_br_type("11999999999")  # ('True', 'celular')
            >>> validate_phone_br_type("1155554444")   # ('True', 'fixo')
        """
        if not phone:
            return False, 'inválido'
        
        # Remove caracteres não numéricos
        phone_clean = re.sub(r'\D', '', phone)
        
        # Verifica DDD válido
        ddds_validos = {
            '11', '12', '13', '14', '15', '16', '17', '18', '19',  # SP
            '21', '22', '24', '27', '28',  # RJ, ES
            '31', '32', '33', '34', '35', '37', '38',  # MG
            '41', '42', '43', '44', '45', '46', '47', '48', '49',  # PR, SC
            '51', '53', '54', '55',  # RS
            '61', '62', '63', '64', '65', '66', '67', '68', '69',  # Centro-Oeste e Norte
            '71', '73', '74', '75', '77', '79',  # BA, SE
            '81', '82', '83', '84', '85', '86', '87', '88', '89',  # Nordeste
            '91', '92', '93', '94', '95', '96', '97', '98', '99'  # Norte
        }
        
        if len(phone_clean) < 10 or phone_clean[:2] not in ddds_validos:
            return False, 'inválido'
        
        # Números especiais
        if len(phone_clean) == 10 and phone_clean[2] in '0':
            return True, 'especial'
        
        # Celular (começa com 9)
        if len(phone_clean) == 11 and phone_clean[2] == '9':
            return True, 'celular'
        
        # Fixo
        if len(phone_clean) == 10 and phone_clean[2] in '2345':
            return True, 'fixo'
        
        return False, 'inválido'

    @staticmethod
    def validate_cbo(cbo: str) -> bool:
        """
        Validates a Brazilian Occupation Code (CBO).
        
        Args:
            cbo (str): The CBO number to validate.
            
        Returns:
            bool: True if the CBO format is valid, False otherwise.
            
        Example:
            >>> validate_cbo("252205")  # Engenheiro de Software
            >>> validate_cbo("251205")  # Analista de Sistemas
        """
        if not cbo:
            return False
        
        # Remove caracteres não numéricos
        cbo_clean = re.sub(r'\D', '', cbo)
        
        # CBO tem 6 dígitos
        if len(cbo_clean) != 6:
            return False
        
        # Primeiro dígito deve ser entre 0 e 9
        if not '0' <= cbo_clean[0] <= '9':
            return False
        
        return True

    @staticmethod
    def validate_brazilian_cpf(cpf: str) -> bool:
        """
        Validates a Brazilian CPF (Individual Taxpayer Registration).
        
        Args:
            cpf (str): The CPF number to validate, with or without formatting.
            
        Returns:
            bool: True if the CPF is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_cpf("123.456.789-09")
            >>> validate_brazilian_cpf("12345678909")
        """
        if not cpf:
            return False
        
        # Remove non-numeric characters
        if cpf := ''.join(filter(str.isdigit, cpf)).strip():
            if len(cpf) != 11:
                return False
            
            # Check if all digits are the same
            if len(set(cpf)) == 1:
                return False
                
            # Calculate first verification digit
            soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
            resto = (soma * 10) % 11
            if resto == 10:
                resto = 0
            if resto != int(cpf[9]):
                return False
                
            # Calculate second verification digit
            soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
            resto = (soma * 10) % 11
            if resto == 10:
                resto = 0
            if resto != int(cpf[10]):
                return False
                
            return True
        return False

    
    @staticmethod
    def validate_brazilian_cnpj(cnpj: str) -> bool:
        """
        Validates a Brazilian CNPJ (National Registry of Legal Entities).
        
        Args:
            cnpj (str): The CNPJ number to validate, with or without formatting.
            
        Returns:
            bool: True if the CNPJ is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_cnpj("12.345.678/0001-90")
            >>> validate_brazilian_cnpj("12345678000190")
        """
        if not cnpj:
            return False
            
        # Remove non-numeric characters
        if cnpj := ''.join(filter(str.isdigit, cnpj)).strip():
            if len(cnpj) != 14:
                return False
                
            # Check if all digits are the same
            if len(set(cnpj)) == 1:
                return False
                
            # Calculate first verification digit
            weights = [5,4,3,2,9,8,7,6,5,4,3,2]
            soma = sum(int(cnpj[i]) * weights[i] for i in range(12))
            resto = soma % 11
            if resto < 2:
                resto = 0
            else:
                resto = 11 - resto
            if resto != int(cnpj[12]):
                return False
                
            # Calculate second verification digit
            weights = [6,5,4,3,2,9,8,7,6,5,4,3,2]
            soma = sum(int(cnpj[i]) * weights[i] for i in range(13))
            resto = soma % 11
            if resto < 2:
                resto = 0
            else:
                resto = 11 - resto
            if resto != int(cnpj[13]):
                return False
                
            return True
        return False


    @staticmethod
    def validate_brazilian_drivers_license(cnh: str) -> bool:
        """
        Validates a Brazilian Driver's License (CNH).
        
        Args:
            cnh (str): The CNH number to validate, with or without formatting.
            
        Returns:
            bool: True if the CNH is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_drivers_license("12345678901")
        """
        if not cnh:
            return False
            
        # Remove non-numeric characters
        if cnh := ''.join(filter(str.isdigit, cnh)).strip():
            if len(cnh) != 11:
                return False
                
            # Check if all digits are the same
            if len(set(cnh)) == 1:
                return False
                
            # Calculate first verification digit
            soma = 0
            for i in range(9):
                soma += int(cnh[i]) * (i + 2)
            resto = soma % 11
            if resto <= 1:
                dv1 = 0
            else:
                dv1 = 11 - resto
            if dv1 != int(cnh[9]):
                return False
                
            # Calculate second verification digit
            soma = 0
            for i in range(9):
                soma += int(cnh[i]) * (9 - i)
            soma += dv1 * 2
            resto = soma % 11
            if resto <= 1:
                dv2 = 0
            else:
                dv2 = 11 - resto
            if dv2 != int(cnh[10]):
                return False
                
            return True
        return False

    @staticmethod
    def validate_brazilian_postal_code(cep: str) -> bool:
        """
        Validates a Brazilian Postal Code (CEP).
        
        Args:
            cep (str): The CEP number to validate, with or without formatting.
            
        Returns:
            bool: True if the CEP format is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_postal_code("12345-678")
            >>> validate_brazilian_postal_code("12345678")
        """
        if not cep:
            return False
            
        # Remove non-numeric characters
        cep = ''.join(filter(str.isdigit, cep)).strip()
        return bool(cep and len(cep) == 8 and cep.isdigit())

    @staticmethod
    def validate_brazilian_license_plate(plate: str) -> bool:
        """
        Validates a Brazilian vehicle license plate.
        Supports both Mercosul and old formats.
        
        Args:
            plate (str): The license plate to validate, with or without formatting.
            
        Returns:
            bool: True if the plate format is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_license_plate("ABC1234")  # Old format
            >>> validate_brazilian_license_plate("ABC1D23")  # Mercosul format
        """
        if not plate:
            return False
            
        # Remove espaços e hífens
        plate = plate.replace(' ', '').replace('-', '').upper()
        
        # Formato antigo (ABC1234)
        old_format = bool(re.match(r'^[A-Z]{3}[0-9]{4}$', plate))
        
        # Mercosul format (ABC1D23)
        mercosul_format = bool(re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', plate))
        
        return old_format or mercosul_format

    @staticmethod
    def validate_brazilian_legal_process(process: str) -> bool:
        """
        Validates a Brazilian Legal Process Number (CNJ format).
        
        Args:
            process (str): The process number to validate, with or without formatting.
            
        Returns:
            bool: True if the process number is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_legal_process("0123456-78.2019.8.26.0100")
        """
        if not process:
            return False
            
        # Remove non-alphanumeric characters
        process = ''.join(filter(str.isalnum, process)).strip()
        
        if len(process) != 20:
            return False
            
        try:
            # Extract components
            nnnnnnn = process[:7]      # Número sequencial
            dd = process[7:9]          # Dígito verificador
            aaaa = process[9:13]       # Ano do ajuizamento
            j = process[13]            # Órgão ou segmento do Poder Judiciário
            tr = process[14:16]        # Tribunal
            oooo = process[16:]        # Unidade de origem
            
            # Basic validations
            if not (nnnnnnn + dd + aaaa + j + tr + oooo).isdigit():
                return False
                
            # Calculate verification digits
            numero = f"{nnnnnnn}{aaaa}{j}{tr}{oooo}"
            soma = sum(int(numero[i]) * (i + 1) for i in range(len(numero)))
            resto = soma % 97
            dv = 98 - resto
            
            return dv == int(dd)
            
        except (ValueError, IndexError):
            return False
            

    
    @staticmethod
    def validate_brazilian_voter_id(title: str) -> bool:
        """
        Validates a Brazilian Voter ID (Título de Eleitor).
        
        Args:
            title (str): The voter ID number to validate, with or without formatting.
            
        Returns:
            bool: True if the voter ID is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_voter_id("123456789012")
        """
        if not title:
            return False
            
        # Remove non-numeric characters
        if title := ''.join(filter(str.isdigit, title)).strip():
            if len(title) != 12:
                return False
                
            # Extract components
            inscricao = title[:8]
            zona = title[8:10]
            secao = title[10:]
            
            # Check if values are in valid ranges
            if not (0 <= int(zona) <= 99 and 0 <= int(secao) <= 99):
                return False
                
            # Calculate verification digits for registration number
            soma = 0
            peso = 2
            for i in range(7, -1, -1):
                soma += int(inscricao[i]) * peso
                peso += 1
                if peso > 9:
                    peso = 2
                    
            resto = soma % 11
            if resto == 0:
                dv1 = 1
            elif resto == 1:
                dv1 = 0
            else:
                dv1 = 11 - resto
                
            # Calculate second verification digit
            soma = dv1 * 9
            peso = 8
            for i in range(7, -1, -1):
                soma += int(inscricao[i]) * peso
                peso -= 1
                
            resto = soma % 11
            if resto == 0:
                dv2 = 1
            elif resto == 1:
                dv2 = 0
            else:
                dv2 = 11 - resto
                
            return dv1 == int(title[8]) and dv2 == int(title[9])
            
        return False



    @staticmethod
    def validate_brazilian_health_card(sus: str) -> bool:
        """
        Validates a Brazilian Health Card Number (Cartão SUS).
        
        Args:
            sus (str): The SUS card number to validate, with or without formatting.
            
        Returns:
            bool: True if the SUS number is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_health_card("123456789012345")
        """
        if not sus:
            return False
            
        # Remove non-numeric characters
        if sus := ''.join(filter(str.isdigit, sus)).strip():
            if len(sus) != 15:
                return False
                
            # Calculate verification digit (PIS algorithm)
            soma = 0
            peso = 15
            for i in range(14):
                soma += int(sus[i]) * peso
                peso -= 1
                
            resto = soma % 11
            if resto == 0:
                dv = 0
            else:
                dv = 11 - resto
                
            return dv == int(sus[14])
            
        return False

    
    @staticmethod
    def validate_brazilian_state_code(uf: str) -> bool:
        """
        Validates a Brazilian State Code (UF).
        
        Args:
            uf (str): The two-letter state code to validate.
            
        Returns:
            bool: True if the state code is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_state_code("SP")
            >>> validate_brazilian_state_code("RJ")
        """
        if not uf:
            return False
            
        valid_ufs = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        }
        
        return uf.upper() in valid_ufs


    
    @staticmethod
    def validate_brazilian_postal_tracking(code: str) -> bool:
        """
        Validates a Brazilian Postal Tracking Code (Código de Rastreio Correios).
        
        Args:
            code (str): The tracking code to validate, with or without formatting.
            
        Returns:
            bool: True if the tracking code format is valid, False otherwise.
            
        Example:
            >>> validate_brazilian_postal_tracking("AA123456789BR")
        """
        if not code:
            return False
            
        # Remove spaces and convert to uppercase
        code = code.replace(' ', '').upper()
        
        # Validate format: 2 letters + 9 numbers + 2 letters
        return bool(re.match(r'^[A-Z]{2}[0-9]{9}[A-Z]{2}$', code))




