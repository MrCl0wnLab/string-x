"""
Módulo extrator de endereços de criptomoedas.

Este módulo implementa funcionalidade para extrair endereços de criptomoedas de
textos usando expressões regulares. Suporta Bitcoin, Ethereum, Litecoin,
Dogecoin e outras moedas. Faz parte do sistema de módulos auxiliares do
String-X.
"""
import re
from stringx.core.basemodule import BaseModule


class AuxRegexCryptocurrency(BaseModule):
    """
    Módulo para extração de endereços de criptomoedas usando regex.

    Este módulo herda de BaseModule e fornece funcionalidade específica para
    identificar e extrair endereços válidos de várias criptomoedas de strings
    de texto.

    Suporta as seguintes criptomoedas:
    - Bitcoin (BTC): Endereços Legacy, SegWit e Bech32
    - Ethereum (ETH): Endereços padrão
    - Litecoin (LTC): Endereços Legacy e SegWit
    - Dogecoin (DOGE): Endereços padrão
    - Bitcoin Cash (BCH): Endereços Legacy
    - Ripple (XRP): Endereços padrão
    - Monero (XMR): Endereços padrão

    Attributes:
        meta (dict): Metadados do módulo incluindo nome, descrição, autor e
            tipo
        options (dict): Opções requeridas incluindo dados de entrada e
            configurações

    Methods:
        __init__(): Inicializa o módulo com metadados e configurações
        run(): Executa o processo de extração de endereços de criptomoedas
        _extract_bitcoin(): Extrai endereços Bitcoin
        _extract_ethereum(): Extrai endereços Ethereum
        _extract_litecoin(): Extrai endereços Litecoin
        _extract_other_cryptos(): Extrai endereços de outras criptomoedas
    """

    def __init__(self):
        """
        Inicializa o módulo extrator de endereços de criptomoedas.

        Configura os metadados do módulo e define as opções necessárias,
        incluindo os padrões regex para detecção de diferentes tipos de
        endereços.
        """
        super().__init__()

        # Define informações de meta do módulo
        self.meta.update({
            "name": "Extractor de Criptomoedas",
            "description": ("Extrai endereços de criptomoedas (Bitcoin, "
                            "Ethereum, Litecoin, etc.) do texto fornecido"),
            "author": "MrCl0wn",
            "type": "extractor"
        })

        # Define opções requeridas para este módulo
        self.options = {
            "data": str(),
            "bitcoin_only": False,  # Se True, extrai apenas endereços Bitcoin
            "ethereum_only": False,  # Se True, extrai apenas endereços
            # Ethereum
            "include_private_keys": False,  # Se True, inclui chaves privadas
            "example": ("./strx -l documents.txt -st \"{STRING}\" "
                        "-module \"ext:cryptocurrency\" -pm"),
            'debug': False,  # Modo de debug para mostrar informações
                             # detalhadas
            'retry': 0,  # Número de tentativas de requisição
            'retry_delay': None,  # Atraso entre tentativas de requisição
        }

        # Padrões regex para diferentes criptomoedas
        self.crypto_patterns = {
            # Bitcoin addresses (Legacy P2PKH: 1..., P2SH: 3..., Bech32:
            # bc1...)
            'bitcoin': [
                r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',  # Legacy addresses
                r'\bbc1[a-z0-9]{39,59}\b',  # Bech32 addresses
            ],

            # Ethereum addresses (0x followed by 40 hex characters)
            'ethereum': [
                r'\b0x[a-fA-F0-9]{40}\b',
            ],

            # Litecoin addresses (L..., M..., ltc1...)
            'litecoin': [
                r'\b[LM][a-km-zA-HJ-NP-Z1-9]{26,33}\b',  # Legacy addresses
                r'\bltc1[a-z0-9]{39,59}\b',  # Bech32 addresses
            ],

            # Dogecoin addresses (D...)
            'dogecoin': [
                r'\bD[a-km-zA-HJ-NP-Z1-9]{33}\b',
            ],

            # Bitcoin Cash addresses (same as Bitcoin Legacy)
            'bitcoin_cash': [
                r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
                r'\bq[a-z0-9]{41}\b',  # CashAddr format
            ],

            # Ripple/XRP addresses (r...)
            'ripple': [
                r'\br[a-zA-Z0-9]{24,34}\b',
            ],

            # Monero addresses (4... or 8...)
            'monero': [
                r'\b[48][a-zA-Z0-9]{94}\b',
            ],

            # Cardano addresses (addr1...)
            'cardano': [
                r'\baddr1[a-z0-9]{58}\b',
            ],

            # Private keys (WIF format, 51-52 characters starting with 5, K, or
            # L)
            'private_keys': [
                r'\b[5KL][1-9A-HJ-NP-Za-km-z]{50,51}\b',
            ],

            # Mnemonic seed phrases (12, 15, 18, 21, or 24 words)
            'seed_phrases': [
                r'\b(?:[a-z]+\s+){11}[a-z]+\b',  # 12 words
                r'\b(?:[a-z]+\s+){14}[a-z]+\b',  # 15 words
                r'\b(?:[a-z]+\s+){17}[a-z]+\b',  # 18 words
                r'\b(?:[a-z]+\s+){20}[a-z]+\b',  # 21 words
                r'\b(?:[a-z]+\s+){23}[a-z]+\b',  # 24 words
            ]
        }

    def run(self):
        """
        Executa o processo de extração de endereços de criptomoedas.

        Utiliza os dados fornecidos e os padrões regex configurados para
        identificar e extrair endereços válidos de criptomoedas. Os endereços
        encontrados são armazenados nos resultados do módulo.

        O processo inclui:
        1. Verificação da disponibilidade de dados
        2. Extração baseada nas opções configuradas
        3. Validação e filtragem de resultados duplicados
        4. Armazenamento dos resultados únicos encontrados
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()

        if not (target_value := self.options.get("data")):
            self.log_debug("Nenhum dado fornecido para extração")
            return

        self.log_debug(
            f"Iniciando extração de criptomoedas em texto de {
                len(target_value)} caracteres")

        results = set()
        results_and_type = []
        # Verificar opções de filtragem
        bitcoin_only = self.options.get("bitcoin_only", False)
        ethereum_only = self.options.get("ethereum_only", False)
        include_private_keys = self.options.get("include_private_keys", False)

        if bitcoin_only:
            self.log_debug("Modo Bitcoin apenas ativado")
            results.update(self._extract_by_type(target_value, 'bitcoin'))
        elif ethereum_only:
            self.log_debug("Modo Ethereum apenas ativado")
            results.update(self._extract_by_type(target_value, 'ethereum'))
        else:
            # Extrair todos os tipos de endereços
            self.log_debug("Extraindo todos os tipos de criptomoedas")
            for crypto_type in ['bitcoin', 'ethereum', 'litecoin', 'dogecoin',
                                'bitcoin_cash', 'ripple', 'monero', 'cardano']:
                results.update(
                    self._extract_by_type(
                        target_value, crypto_type))

        # Incluir chaves privadas se solicitado
        if include_private_keys:
            self.log_debug("Incluindo chaves privadas na extração")
            results.update(self._extract_by_type(target_value, 'private_keys'))
            results.update(self._extract_by_type(target_value, 'seed_phrases'))

        # Armazenar resultados únicos
        if results:
            self.log_debug(
                f"Encontrados {
                    len(results)} endereços únicos de criptomoedas")
            for crypto_address in sorted(results):
                crypto_type = self._identify_crypto_type(crypto_address)
                results_and_type.append(f"{crypto_type}, {crypto_address}")
            if results_and_type:
                results_and_type = sorted(
                    list(set(results_and_type)))  # Remove duplicatas
                return self.set_result("\n".join(results_and_type))
        else:
            self.log_debug("Nenhum endereço de criptomoeda encontrado")

    def _extract_by_type(self, text: str, crypto_type: str) -> set:
        """
        Extrai endereços de um tipo específico de criptomoeda.

        Args:
            text (str): Texto onde buscar endereços
            crypto_type (str): Tipo de criptomoeda para extrair

        Returns:
            set: Conjunto de endereços encontrados
        """
        results = set()
        patterns = self.crypto_patterns.get(crypto_type, [])

        for pattern in patterns:
            compiled_regex = re.compile(pattern, re.IGNORECASE)
            matches = re.findall(compiled_regex, text)
            results.update(matches)

        self.log_debug(
            f"Extraídos {
                len(results)} endereços do tipo {crypto_type}")
        return results

    def _identify_crypto_type(self, address: str) -> str:
        """
        Identifica o tipo de criptomoeda com base no formato do endereço.

        Args:
            address (str): Endereço a ser identificado

        Returns:
            str: Tipo de criptomoeda identificado
        """
        # Bitcoin
        if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
            return "BTC"
        elif re.match(r'^bc1[a-z0-9]{39,59}$', address):
            return "BTC"

        # Ethereum
        elif re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return "ETH"

        # Litecoin
        elif re.match(r'^[LM][a-km-zA-HJ-NP-Z1-9]{26,33}$',
                      address, re.IGNORECASE):
            return "LTC"
        elif re.match(r'^ltc[a-z0-9]{39,59}$', address, re.IGNORECASE):
            return "LTC"
        elif re.fullmatch(r'^ltc1[ac-hj-np-z02-9]{39,59}$',
                          address, re.IGNORECASE):
            return "LTC"

        # Dogecoin
        elif re.match(r'^D[a-km-zA-HJ-NP-Z1-9]{33}$', address):
            return "DOGE"

        # Bitcoin Cash
        elif re.match(r'^q[a-z0-9]{41}$', address):
            return "BCH"

        # Ripple/XRP
        elif re.match(r'^r[a-zA-Z0-9]{24,34}$', address):
            return "XRP"

        # Monero
        elif re.match(r'^[48][a-zA-Z0-9]{94}$', address):
            return "XMR"

        # Cardano
        elif re.match(r'^addr1[a-z0-9]{58}$', address):
            return "ADA"

        # Private Keys
        elif re.match(r'^[5KL][1-9A-HJ-NP-Za-km-z]{50,51}$', address):
            return "PRIVATE_KEY"

        # Seed phrases
        elif len(address.split()) in [12, 15, 18, 21, 24]:
            return "SEED_PHRASE"

        return "UNKNOWN"
