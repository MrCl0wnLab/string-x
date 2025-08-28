# Criação de Funções para String-X

Este guia explica como criar e adicionar novas funções ao sistema de templates dinâmicos do String-X no arquivo `utils/helper/functions.py`.

## Visão Geral das Funções

As funções do String-X são métodos estáticos da classe `Funcs` que podem ser chamados dentro de templates usando a sintaxe `nome_funcao({STRING})`. Elas permitem transformações dinâmicas de dados durante o processamento.

### Localização das Funções

**Arquivo**: `src/stringx/utils/helper/functions.py`
**Classe**: `Funcs`
**Tipo**: Métodos estáticos (`@staticmethod`)

## Estrutura Base de uma Função

Todas as funções devem seguir este padrão:

```python
@staticmethod
def nome_funcao(value: str, *args, **kwargs) -> str:
    """
    Descrição clara da função.
    
    Explicação detalhada do que a função faz, incluindo exemplos de uso
    e comportamentos especiais ou limitações.
    
    Args:
        value (str): Valor de entrada (geralmente {STRING})
        *args: Argumentos posicionais adicionais (opcional)
        **kwargs: Argumentos nomeados adicionais (opcional)
    
    Returns:
        str: Resultado processado da função ou string vazia em caso de erro
        
    Example:
        >>> Funcs.nome_funcao("exemplo")
        "resultado_processado"
    """
    if not value:
        return str()
    
    try:
        # Implementar lógica da função aqui
        result = processar_value(value)
        return str(result) if result else str()
    except Exception:
        # Falhas silenciosas - retornar string vazia
        return str()
```

## Categorias de Funções Existentes

### 1. Funções de Hash e Criptografia

**Propósito**: Gerar hashes e codificações criptográficas.

**Exemplo - Hash SHA3-256**:
```python
@staticmethod
def sha3_256(value: str) -> str:
    """
    Gera hash SHA3-256 da string fornecida.
    
    SHA3-256 é uma função hash criptográfica que produz um hash
    de 256 bits (32 bytes). Faz parte da família SHA-3.
    
    Args:
        value (str): String para gerar o hash
    
    Returns:
        str: Hash SHA3-256 em hexadecimal ou string vazia
        
    Example:
        >>> Funcs.sha3_256("hello")
        "75d527c368f2efe848ecf6b073a36767800805e9eef2b1857d5f984f036eb6df"
    """
    if not value:
        return str()
    
    try:
        import hashlib
        return hashlib.sha3_256(value.encode('utf-8')).hexdigest()
    except Exception:
        return str()
```

### 2. Funções de Codificação

**Propósito**: Codificar/decodificar strings em diferentes formatos.

**Exemplo - Codificação ROT13**:
```python
@staticmethod  
def rot13(value: str) -> str:
    """
    Aplica codificação ROT13 à string.
    
    ROT13 é uma cifra de substituição simples que substitui cada letra
    pela letra 13 posições à frente no alfabeto. É seu próprio inverso.
    
    Args:
        value (str): String para codificar
    
    Returns:
        str: String codificada em ROT13 ou string vazia
        
    Example:
        >>> Funcs.rot13("hello")
        "uryyb"
        >>> Funcs.rot13("uryyb")  # Decodifica de volta
        "hello"
    """
    if not value:
        return str()
    
    try:
        import codecs
        return codecs.encode(value, 'rot_13')
    except Exception:
        return str()
```

### 3. Funções de Rede

**Propósito**: Operações relacionadas a rede e conectividade.

**Exemplo - Resolução Reversa de DNS**:
```python
@staticmethod
def reverse_dns(value: str) -> str:
    """
    Resolve o nome do host a partir de um endereço IP (DNS reverso).
    
    Realiza uma consulta DNS reversa (PTR record) para obter o nome
    do host associado ao endereço IP fornecido.
    
    Args:
        value (str): Endereço IP para resolver
    
    Returns:
        str: Nome do host ou string vazia se não resolvido
        
    Example:
        >>> Funcs.reverse_dns("8.8.8.8")
        "dns.google"
    """
    if not value:
        return str()
    
    try:
        import socket
        import ipaddress
        
        # Validar se é um IP válido
        ip = ipaddress.ip_address(value)
        
        # Resolver DNS reverso
        host, _, _ = socket.gethostbyaddr(str(ip))
        return host
    except Exception:
        return str()
```

### 4. Funções de Formatação

**Propósito**: Formatar e transformar strings.

**Exemplo - Slug URL**:
```python
@staticmethod
def slugify(value: str) -> str:
    """
    Converte string em formato slug para URLs.
    
    Remove acentos, converte para minúsculas, substitui espaços e
    caracteres especiais por hífens, criando um formato adequado para URLs.
    
    Args:
        value (str): String para converter em slug
    
    Returns:
        str: String no formato slug ou string vazia
        
    Example:
        >>> Funcs.slugify("Olá Mundo! Como você está?")
        "ola-mundo-como-voce-esta"
    """
    if not value:
        return str()
    
    try:
        import re
        import unicodedata
        
        # Normalizar caracteres Unicode (remover acentos)
        value = unicodedata.normalize('NFKD', value)
        value = value.encode('ascii', 'ignore').decode('ascii')
        
        # Converter para minúsculas
        value = value.lower()
        
        # Substituir caracteres não alfanuméricos por hífens
        value = re.sub(r'[^a-z0-9]+', '-', value)
        
        # Remover hífens do início e fim
        value = value.strip('-')
        
        return value
    except Exception:
        return str()
```

### 5. Funções de Validação

**Propósito**: Validar formatos e tipos de dados.

**Exemplo - Validador de CNPJ**:
```python
@staticmethod
def validate_cnpj(value: str) -> str:
    """
    Valida se a string é um CNPJ brasileiro válido.
    
    Verifica se o CNPJ está no formato correto e se os dígitos
    verificadores estão corretos segundo o algoritmo oficial.
    
    Args:
        value (str): CNPJ para validar (com ou sem formatação)
    
    Returns:
        str: "valid" se válido, "invalid" se inválido, string vazia se erro
        
    Example:
        >>> Funcs.validate_cnpj("11.222.333/0001-81")
        "valid"
        >>> Funcs.validate_cnpj("11.222.333/0001-80")
        "invalid"
    """
    if not value:
        return str()
    
    try:
        # Remover formatação
        cnpj = ''.join(filter(str.isdigit, value))
        
        # Verificar se tem 14 dígitos
        if len(cnpj) != 14:
            return "invalid"
        
        # Calcular primeiro dígito verificador
        sequence1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum1 = sum(int(cnpj[i]) * sequence1[i] for i in range(12))
        digit1 = 11 - (sum1 % 11) if sum1 % 11 >= 2 else 0
        
        # Calcular segundo dígito verificador
        sequence2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum2 = sum(int(cnpj[i]) * sequence2[i] for i in range(13))
        digit2 = 11 - (sum2 % 11) if sum2 % 11 >= 2 else 0
        
        # Verificar se os dígitos estão corretos
        if int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2:
            return "valid"
        else:
            return "invalid"
            
    except Exception:
        return str()
```

### 6. Funções de Geração

**Propósito**: Gerar valores aleatórios ou derivados.

**Exemplo - Gerador de UUID**:
```python
@staticmethod
def generate_uuid(value: str = None) -> str:
    """
    Gera um UUID (Universally Unique Identifier) aleatório.
    
    Gera um UUID versão 4 (aleatório). O parâmetro value é ignorado,
    mantido apenas para compatibilidade com o sistema de templates.
    
    Args:
        value (str): Parâmetro ignorado (mantido para compatibilidade)
    
    Returns:
        str: UUID no formato padrão ou string vazia em caso de erro
        
    Example:
        >>> Funcs.generate_uuid("")
        "550e8400-e29b-41d4-a716-446655440000"
    """
    try:
        import uuid
        return str(uuid.uuid4())
    except Exception:
        return str()
```

## Funções com Parâmetros Adicionais

As funções podem aceitar parâmetros adicionais através de `*args` e `**kwargs`:

**Exemplo - Função com Parâmetros**:
```python
@staticmethod
def truncate(value: str, length: str = "50", suffix: str = "...") -> str:
    """
    Trunca string para um comprimento específico.
    
    Corta a string no comprimento especificado e adiciona um sufixo
    se a string foi truncada.
    
    Args:
        value (str): String para truncar
        length (str): Comprimento máximo (padrão: "50")
        suffix (str): Sufixo para strings truncadas (padrão: "...")
    
    Returns:
        str: String truncada ou string original se menor que o limite
        
    Example:
        >>> Funcs.truncate("Esta é uma string muito longa", "10", "...")
        "Esta é um..."
    """
    if not value:
        return str()
    
    try:
        max_length = int(length) if length.isdigit() else 50
        
        if len(value) <= max_length:
            return value
            
        return value[:max_length - len(suffix)] + suffix
    except Exception:
        return str()
```

**Uso no Template**:
```bash
# Truncar para 20 caracteres
strx -s "String muito longa para exemplo" -st "truncate({STRING}, 20)" -ns -pf

# Truncar para 15 caracteres com sufixo personalizado
strx -s "String longa" -st "truncate({STRING}, 15, ' [...]')" -ns -pf
```

## Funções Assíncronas

Para operações que requerem acesso à rede ou I/O:

**Exemplo - Função com HTTP Request**:
```python
@staticmethod
def check_url_status(value: str) -> str:
    """
    Verifica o status HTTP de uma URL.
    
    Faz uma requisição HEAD para a URL e retorna o código de status HTTP.
    Inclui tratamento para redirecionamentos e timeouts.
    
    Args:
        value (str): URL para verificar
    
    Returns:
        str: Código de status HTTP ou string vazia em caso de erro
        
    Example:
        >>> Funcs.check_url_status("https://httpbin.org/status/200")
        "200"
        >>> Funcs.check_url_status("https://httpbin.org/status/404") 
        "404"
    """
    if not value:
        return str()
    
    try:
        import requests
        from urllib.parse import urlparse
        
        # Validar se é uma URL válida
        parsed = urlparse(value)
        if not all([parsed.scheme, parsed.netloc]):
            return str()
        
        # Fazer requisição HEAD com timeout
        response = requests.head(
            value,
            timeout=10,
            allow_redirects=True,
            headers={'User-Agent': 'String-X/1.0'}
        )
        
        return str(response.status_code)
        
    except requests.exceptions.RequestException:
        return str()
    except Exception:
        return str()
```

## Funções de Texto Avançadas

**Exemplo - Extrator de Palavras-chave**:
```python
@staticmethod
def extract_keywords(value: str, min_length: str = "4") -> str:
    """
    Extrai palavras-chave de um texto.
    
    Remove stop words e extrai palavras significativas baseadas no
    comprimento mínimo especificado.
    
    Args:
        value (str): Texto para extrair palavras-chave
        min_length (str): Comprimento mínimo das palavras (padrão: "4")
    
    Returns:
        str: Palavras-chave separadas por vírgula ou string vazia
        
    Example:
        >>> Funcs.extract_keywords("Este é um exemplo de texto")
        "exemplo, texto"
    """
    if not value:
        return str()
    
    try:
        import re
        
        # Stop words básicas em português
        stop_words = {
            'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'com',
            'para', 'por', 'que', 'não', 'se', 'na', 'no', 'ao', 'dos',
            'das', 'te', 'ele', 'ela', 'eu', 'nós', 'vós', 'eles', 'elas',
            'este', 'esta', 'esse', 'essa', 'isto', 'isso', 'aquele', 'aquela'
        }
        
        min_len = int(min_length) if min_length.isdigit() else 4
        
        # Extrair palavras alfabéticas
        words = re.findall(r'\b[a-záàâãéèêíìîóòôõúùûç]+\b', value.lower())
        
        # Filtrar palavras
        keywords = []
        for word in words:
            if len(word) >= min_len and word not in stop_words:
                keywords.append(word)
        
        # Remover duplicatas mantendo ordem
        unique_keywords = list(dict.fromkeys(keywords))
        
        return ', '.join(unique_keywords)
        
    except Exception:
        return str()
```

## Integração com APIs Externas

**Exemplo - Função com API**:
```python
@staticmethod
def get_ip_info(value: str) -> str:
    """
    Obtém informações geográficas de um endereço IP.
    
    Consulta um serviço público de geolocalização de IP e retorna
    informações básicas sobre localização.
    
    Args:
        value (str): Endereço IP para consultar
    
    Returns:
        str: Informações do IP no formato "País, Cidade" ou string vazia
        
    Example:
        >>> Funcs.get_ip_info("8.8.8.8")
        "United States, Mountain View"
    """
    if not value:
        return str()
    
    try:
        import requests
        import ipaddress
        import json
        
        # Validar IP
        ip = ipaddress.ip_address(value)
        
        # Consultar API pública (sem necessidade de chave)
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                country = data.get('country', '')
                city = data.get('city', '')
                return f"{country}, {city}" if country and city else country
        
        return str()
        
    except Exception:
        return str()
```

## Boas Práticas para Funções

### 1. Tratamento de Erros Silencioso
```python
@staticmethod
def minha_funcao(value: str) -> str:
    try:
        # Lógica da função
        return resultado
    except Exception:
        # Nunca gerar exceções - sempre retornar string vazia
        return str()
```

### 2. Validação de Entrada
```python
@staticmethod
def minha_funcao(value: str) -> str:
    if not value or not isinstance(value, str):
        return str()
    
    # Continuar processamento...
```

### 3. Documentação Completa
```python
@staticmethod
def minha_funcao(value: str, param: str = "default") -> str:
    """
    Linha de resumo da função.
    
    Descrição detalhada incluindo comportamento especial,
    limitações e exemplos de uso.
    
    Args:
        value (str): Descrição do parâmetro principal
        param (str): Descrição do parâmetro opcional
    
    Returns:
        str: Descrição do retorno
        
    Example:
        >>> Funcs.minha_funcao("teste")
        "resultado_exemplo"
    """
```

### 4. Performance e Recursos
```python
@staticmethod
def minha_funcao(value: str) -> str:
    if not value:
        return str()
    
    try:
        # Para operações caras, implementar cache ou limits
        if len(value) > 10000:  # Limite de tamanho
            value = value[:10000]
        
        # Implementar lógica...
        return resultado
        
    except Exception:
        return str()
```

### 5. Dependências Opcionais
```python
@staticmethod
def minha_funcao(value: str) -> str:
    try:
        import biblioteca_opcional
    except ImportError:
        return str()  # Biblioteca não disponível
    
    # Usar biblioteca...
```

## Exemplo Completo - Função de Análise de Senha

```python
@staticmethod
def password_strength(value: str) -> str:
    """
    Analisa a força de uma senha e retorna uma classificação.
    
    Avalia uma senha baseada em critérios como comprimento, variedade
    de caracteres, presença de símbolos e padrões comuns.
    
    Args:
        value (str): Senha para analisar
    
    Returns:
        str: Classificação da força (weak/medium/strong/very_strong) 
             ou string vazia em caso de erro
        
    Example:
        >>> Funcs.password_strength("123456")
        "weak"
        >>> Funcs.password_strength("MyP@ssw0rd123!")
        "very_strong"
    """
    if not value:
        return str()
    
    try:
        import re
        
        score = 0
        
        # Critério 1: Comprimento
        if len(value) >= 8:
            score += 1
        if len(value) >= 12:
            score += 1
        if len(value) >= 16:
            score += 1
        
        # Critério 2: Variedade de caracteres
        if re.search(r'[a-z]', value):  # Minúsculas
            score += 1
        if re.search(r'[A-Z]', value):  # Maiúsculas
            score += 1
        if re.search(r'\d', value):     # Números
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>?]', value):  # Símbolos
            score += 2
        
        # Critério 3: Penalizar padrões comuns
        common_patterns = [
            r'123456', r'password', r'qwerty', r'abc123',
            r'(.)\1{2,}',  # Repetições (aaa, 111)
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, value.lower()):
                score -= 2
                break
        
        # Classificar baseado na pontuação
        if score < 3:
            return "weak"
        elif score < 5:
            return "medium"
        elif score < 7:
            return "strong"
        else:
            return "very_strong"
            
    except Exception:
        return str()
```

**Uso da função**:
```bash
# Analisar força de senha
strx -s "MyPassword123!" -st "password_strength({STRING})" -ns -pf

# Usar em conjunto com outros dados
strx -l passwords.txt -st "Password: {STRING} - Strength: password_strength({STRING})" -ns -pf
```

## Lista de Funções Existentes

Para ver todas as funções disponíveis:
```bash
./strx -funcs
```

Para adicionar sua nova função:
1. Abra `src/stringx/utils/helper/functions.py`
2. Adicione sua função como método estático da classe `Funcs`
3. Siga o padrão de documentação e tratamento de erros
4. Teste a função antes de usar em produção
5. A função estará automaticamente disponível no sistema

## Testes de Funções

Para testar suas funções:

```python
# Teste simples no terminal Python
from stringx.utils.helper.functions import Funcs

# Testar função
resultado = Funcs.minha_funcao("valor_teste")
print(f"Resultado: {resultado}")
```

Ou criar testes unitários:

```python
# tests/test_functions.py
import unittest
from stringx.utils.helper.functions import Funcs

class TestCustomFunctions(unittest.TestCase):
    def test_minha_funcao(self):
        result = Funcs.minha_funcao("teste")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")
    
    def test_minha_funcao_empty(self):
        result = Funcs.minha_funcao("")
        self.assertEqual(result, "")
```

As funções são uma parte fundamental do poder do String-X, permitindo transformações dinâmicas e complexas de dados de forma simples e eficiente.