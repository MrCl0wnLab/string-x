"""
Módulo de funções auxiliares.

Este módulo contém a classe Funcs com métodos estáticos que implementam
diversas funções auxiliares para formatação, codificação, rede e manipulação
de dados. Essas funções são utilizadas pelo sistema de templates dinâmicos.
"""
import os
import re
import json
import base64
import socket
import hashlib
import random
import asyncio
import datetime
import ipaddress
import subprocess
from urllib.parse import urlparse

from stringx.core.format import Format
from stringx.core.randomvalue import RandomValue
from stringx.core.http_async import HTTPClient


class Funcs:
    """
    Classe com funções auxiliares estáticas.

    Esta classe fornece um conjunto de métodos estáticos para diversas
    operações como codificação/decodificação, hash, geração de valores
    aleatórios, resolução DNS e manipulação de URLs.
    """

    def __init__(self):
        ...

    @staticmethod
    def clear(value: str) -> str:
        """
        Limpa e formata uma string removendo caracteres especiais.

        Args:
            value (str): String a ser limpa

        Returns:
            str: String limpa ou string vazia
        """
        if not value:
            return str()

        try:
            # Remove caracteres de controle e espaços extras
            cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            return Format.clear_value(cleaned)
        except Exception:
            return str()

    @staticmethod
    def debase64(value: str) -> str:
        """
        Decodifica string de Base64.

        Args:
            value (str): String codificada em Base64

        Returns:
            str: String decodificada ou string vazia
        """
        if value:
            return Format.decode64(value)
        return str()

    @staticmethod
    def base64(value: str) -> str:
        """
        Codifica string em Base64.

        Args:
            value (str): String a ser codificada

        Returns:
            str: String codificada em Base64 ou string vazia
        """
        if value:
            return Format.encode64(value)
        return str()

    @staticmethod
    def sha1(value: str) -> str:
        """
        Gera hash SHA1 de uma string.

        Args:
            value (str): String para gerar hash

        Returns:
            str: Hash SHA1 ou string vazia
        """
        if value:
            return Format.sha1(value)
        return str()

    @staticmethod
    def sha256(value: str) -> str:
        """
        Gera hash SHA256 de uma string.

        Args:
            value (str): String para gerar hash

        Returns:
            str: Hash SHA256 ou string vazia
        """
        if value:
            return Format.sha256(value)
        return str()

    @staticmethod
    def hex(value: str) -> str:
        """
        Codifica string em hexadecimal.

        Args:
            value (str): String a ser codificada

        Returns:
            str: String codificada em hex ou string vazia
        """
        if value:
            return Format.encodehex(value)
        return str()

    @staticmethod
    def dehex(value: str) -> str:
        """
        Decodifica string hexadecimal.

        Args:
            value (str): String em hexadecimal

        Returns:
            str: String decodificada ou string vazia
        """
        if value:
            return Format.decodehex(value)
        return str()

    @staticmethod
    def md5(value: str) -> str:
        """
        Gera hash MD5 de uma string.

        Args:
            value (str): String para gerar hash

        Returns:
            str: Hash MD5 ou string vazia
        """
        if value:
            return Format.md5(value)
        return str()

    @staticmethod
    def str_rand(value: str) -> str:
        """
        Gera string aleatória de caracteres alfanuméricos.

        Args:
            value (str): Comprimento da string

        Returns:
            str: String aleatória ou string vazia
        """
        if value:
            return RandomValue.get_str_rand(value)
        return str()

    @staticmethod
    def int_rand(value: str) -> str:
        """
        Gera string de números aleatórios.

        Args:
            value (str): Quantidade de números

        Returns:
            str: String de números aleatórios ou string vazia
        """
        if value:
            return str(RandomValue.get_int_rand(value))
        return str()

    @staticmethod
    def ip(value: str) -> str:
        """
        Resolve hostname para endereço IP.

        Args:
            value (str): Hostname ou domínio

        Returns:
            str: Endereço IP ou string vazia se falhar
        """
        if value:
            try:
                return socket.gethostbyname(value)
            except socket.gaierror:
                return str()
        return str()

    @staticmethod
    def replace(value: str) -> str:
        """
        Substitui substring em uma string.

        Args:
            value (str): String no formato "old,new,texto"

        Returns:
            str: String com substituição aplicada ou string vazia
        """
        if value:
            old, new, cmd = value.split(',')
            if old and new and cmd:
                return cmd.replace(old, new)
        return str()

    @staticmethod
    def get(value: str) -> str:
        """
        Faz requisição HTTP GET para uma URL.

        Args:
            value (str): URL para requisição

        Returns:
            str: Resposta da requisição ou string vazia
        """
        if value.startswith('http'):
            try:
                request = HTTPClient()
                results = asyncio.run(request.send_request([value]))[0]
                success_error_redirect = (
                    results.is_success or results.is_error
                    or results.is_redirect)
                if success_error_redirect:
                    return (f"{results.status_code}; "
                            f"{Funcs.title_html(results.text)}")
                elif results.is_exception:
                    return f"exception; {str(results.exception)}"
            except Exception:
                pass
        return str()

    @staticmethod
    def title_html(html: str) -> str:
        """
        Extrai o título de uma página HTML.

        Args:
            html (str): Conteúdo HTML da página

        Returns:
            str: Título extraído da página ou string vazia
        """
        if html:
            title = Format.clear_value(Format.regex(
                html, r'<title[^>]*>([^<]+)</title>')[0])
            title = title.replace("'", "")
            if title:
                return title
        return str()

    @staticmethod
    def urlencode(value: str) -> str:
        """
        Codifica URL.

        Args:
            value (str): URL a ser codificada

        Returns:
            str: URL codificada ou string vazia
        """
        if value:
            encode = Format.parse_urlencode(value)
            if encode:
                return encode
        return str()

    @staticmethod
    def rev(value: str) -> str:
        """
        Inverte uma string.

        Args:
            value (str): String a ser invertida

        Returns:
            str: String invertida ou string vazia
        """
        if value:
            value_rev = value[::-1]
            if value_rev:
                return value_rev
        return str()

    @staticmethod
    def timestamp(value: str) -> str:
        """
        Retorna timestamp atual formatado.

        Args:
            value (str): Formato da data/hora (não utilizado)

        Returns:
            str: Timestamp formatado ou string vazia
        """
        if not value:
            return str()

        try:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return str()

    @staticmethod
    def extract_domain(value: str) -> str:
        """
        Extrai domínio de uma URL.

        Args:
            value (str): URL completa

        Returns:
            str: Domínio extraído ou string vazia
        """
        if not value:
            return str()

        try:
            parsed = urlparse(value)
            return parsed.netloc or parsed.path.split('/')[0]
        except BaseException:
            return str()

    @staticmethod
    def jwt_decode(value: str) -> str:
        """
        Decodifica JWT token (apenas payload, sem verificação de assinatura).

        Args:
            value (str): JWT token

        Returns:
            str: Payload decodificado em JSON ou string vazia
        """
        if not value:
            return str()

        try:
            parts = value.split('.')
            if len(parts) != 3:
                return str()

            # Adiciona padding se necessário
            payload = parts[1]
            missing_padding = len(payload) % 4
            if missing_padding:
                payload += '=' * (4 - missing_padding)

            decoded = base64.urlsafe_b64decode(payload)
            return json.dumps(json.loads(decoded), indent=2)
        except Exception:
            return str()

    @staticmethod
    def whois_lookup(value: str) -> str:
        """
        Realiza consulta whois para um domínio.

        Args:
            value (str): Domínio para consulta

        Returns:
            str: Resultado do whois ou string vazia
        """
        if not value:
            return str()

        try:
            result = subprocess.run(['whois', value],
                                    capture_output=True, text=True, timeout=10)
            return result.stdout if result.returncode == 0 else str()
        except Exception:
            return str()

    @staticmethod
    def cert_info(value: str) -> str:
        """
        Obtém informações do certificado SSL de um host.

        Args:
            value (str): Host:porta (ex: example.com:443)

        Returns:
            str: Informações do certificado ou string vazia
        """
        if not value:
            return str()

        try:
            if ':' not in value:
                value += ':443'

            cmd = f"echo | openssl s_client -connect {value} -servername {
                value.split(':')[0]} 2>/dev/null | openssl x509 -noout -text"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10)
            return result.stdout if result.returncode == 0 else str()
        except Exception:
            return str()

    @staticmethod
    def user_agent(value: str) -> str:
        """
        Gera User-Agent aleatório para requisições.

        Returns:
            str: User-Agent aleatório
        """
        agents = [
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
            ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
             "Safari/537.36"),
            ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) "
             "Gecko/20100101 Firefox/121.0"),
        ]

        return random.choice(agents)

    @staticmethod
    def cidr_expand(value: str) -> str:
        """
        Expande notação CIDR em lista de IPs.

        Args:
            value (str): Notação CIDR (ex: 192.168.1.0/24)

        Returns:
            str: Lista de IPs separados por vírgula
        """
        if not value or '/' not in value:
            return str()

        try:
            network = ipaddress.IPv4Network(value, strict=False)
            return ','.join(str(ip) for ip in network.hosts())
        except Exception:
            return str()

    @staticmethod
    def subdomain_gen(value: str) -> str:
        """
        Gera subdomínios comuns para um domínio.

        Args:
            value (str): Domínio base

        Returns:
            str: Lista de subdomínios separados por vírgula
        """
        if not value:
            return str()

        common_subs = [
            'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
            'blog', 'shop', 'app', 'mobile', 'secure', 'portal', 'vpn'
        ]

        return ','.join(f"{sub}.{value}" for sub in common_subs)

    @staticmethod
    def email_validator(value: str) -> str:
        """
        Valida formato de email.

        Args:
            value (str): Email para validar

        Returns:
            str: "valid" ou "invalid"
        """
        if not value:
            return "invalid"

        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return "valid" if re.match(pattern, value) else "invalid"

    @staticmethod
    def hash_file(value: str) -> str:
        """
        Calcula hashes MD5, SHA1 e SHA256 de um arquivo.

        Args:
            value (str): Caminho para o arquivo

        Returns:
            str: Hashes separados por vírgula
        """
        if not value or not os.path.exists(value):
            return "file_not_found"
        try:

            file_size = os.path.getsize(value)
            if file_size > 100 * 1024 * 1024:
                return "file_too_large"

            md5_hash = hashlib.md5()
            sha1_hash = hashlib.sha1()
            sha256_hash = hashlib.sha256()

            with open(value, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
                    sha1_hash.update(chunk)
                    sha256_hash.update(chunk)

            return (f"MD5:{md5_hash.hexdigest()},"
                    f"SHA1:{sha1_hash.hexdigest()},"
                    f"SHA256:{sha256_hash.hexdigest()}")
        except Exception as e:
            return f"error:{str(e)[:50]}"

    @staticmethod
    def encode_url_all(value: str) -> str:
        """
        Codifica URL com diferentes métodos.

        Args:
            value (str): URL para codificar

        Returns:
            str: URL codificada
        """
        try:
            import urllib.parse
            encoded = urllib.parse.quote(value, safe='')
            return encoded
        except Exception:
            return str()

    @staticmethod
    def phone_format(value: str) -> str:
        """
        Formata número de telefone brasileiro.

        Args:
            value (str): Número de telefone

        Returns:
            str: Telefone formatado
        """
        try:
            import re
            # Remove tudo exceto números
            numbers = re.sub(r'\D', '', value)

            # Formato brasileiro
            if len(numbers) == 11:  # Celular com DDD
                return (f"({numbers[:2]}) {numbers[2]} "
                        f"{numbers[3:7]}-{numbers[7:]}")
            elif len(numbers) == 10:  # Fixo com DDD
                return f"({numbers[:2]}) {numbers[2:6]}-{numbers[6:]}"
            else:
                return value
        except Exception:
            return value

    @staticmethod
    def password_strength(value: str) -> str:
        """
        Avalia força de senha.

        Args:
            value (str): Senha para avaliar

        Returns:
            str: Nível de força (weak, medium, strong)
        """
        try:
            import re

            if len(value) < 6:
                return "weak"

            score = 0

            # Comprimento
            if len(value) >= 8:
                score += 1
            if len(value) >= 12:
                score += 1

            # Caracteres
            if re.search(r'[a-z]', value):
                score += 1
            if re.search(r'[A-Z]', value):
                score += 1
            if re.search(r'\d', value):
                score += 1
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                score += 1

            if score <= 2:
                return "weak"
            elif score <= 4:
                return "medium"
            else:
                return "strong"
        except Exception:
            return "unknown"

    @staticmethod
    def social_media_extract(value: str) -> str:
        """
        Extrai handles de redes sociais do texto.

        Args:
            value (str): Texto para análise

        Returns:
            str: Handles encontrados separados por vírgula
        """
        try:
            patterns = {
                'twitter': r'@[A-Za-z0-9_]+',
                'instagram': r'@[A-Za-z0-9_.]+',
                'telegram': r'@[A-Za-z0-9_]+',
                'linkedin': r'linkedin\.com/in/[A-Za-z0-9-]+',
                'github': r'github\.com/[A-Za-z0-9_-]+',
                'facebook': r'facebook\.com/[A-Za-z0-9.]+',
                'youtube': r'youtube\.com/(?:c/|channel/|user/)[A-Za-z0-9_-]+'
            }

            found = []
            for platform, pattern in patterns.items():
                matches = re.findall(pattern, value)
                for match in matches:
                    found.append(f"{platform}:{match}")

            return ','.join(found) if found else str()
        except Exception:
            return str()

    @staticmethod
    def leak_check_format(value: str) -> str:
        """
        Formata email para busca em bases de vazamentos.

        Args:
            value (str): Email para formatar

        Returns:
            str: Email formatado ou string vazia
        """
        try:
            if not value or '@' not in value:
                return str()

            # Normaliza email para lowercase
            email = value.lower().strip()

            # Verifica formato básico
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                return str()

            return email
        except Exception:
            return str()

    @staticmethod
    def cpf_validate(value: str) -> str:
        """
        Valida CPF brasileiro.

        Args:
            value (str): Número do CPF

        Returns:
            str: "valid" ou "invalid"
        """
        try:
            # Remove caracteres não numéricos
            cpf = re.sub(r'\D', '', value)

            # Verifica se tem 11 dígitos
            if len(cpf) != 11:
                return "invalid"

            # Verifica se todos os dígitos são iguais
            if cpf == cpf[0] * 11:
                return "invalid"

            # Calcula primeiro dígito verificador
            soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
            resto = soma % 11
            dv1 = 0 if resto < 2 else 11 - resto

            # Calcula segundo dígito verificador
            soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
            resto = soma % 11
            dv2 = 0 if resto < 2 else 11 - resto

            # Verifica se os dígitos calculados conferem
            if int(cpf[9]) == dv1 and int(cpf[10]) == dv2:
                return "valid"
            else:
                return "invalid"

        except Exception:
            return "invalid"
