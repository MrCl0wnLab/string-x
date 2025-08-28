# Criação de Módulos para String-X

Este guia explica como criar novos módulos para o String-X, desde a estrutura básica até a implementação avançada.

## Visão Geral dos Módulos

Os módulos do String-X são organizados em categorias funcionais, cada uma com sua responsabilidade específica:

### Tipos de Módulos

| Tipo | Pasta | Função | Exemplos |
|------|-------|--------|----------|
| **EXT** | `utils/auxiliary/ext/` | Extração de dados usando regex | email, url, ip, hash |
| **CLC** | `utils/auxiliary/clc/` | Coleta de dados de APIs/serviços externos | dns, whois, shodan, google |
| **CON** | `utils/auxiliary/con/` | Conexão com sistemas externos | mysql, mongodb, ssh, ftp |
| **OUT** | `utils/auxiliary/out/` | Formatação de saída | json, csv, xml, html |
| **AI** | `utils/auxiliary/ai/` | Integração com IA | gemini, openai |

## Estrutura Base de um Módulo

Todos os módulos devem herdar da classe `BaseModule` e seguir este padrão:

```python
"""
Descrição do módulo.

Documentação detalhada sobre a funcionalidade do módulo,
incluindo propósito, uso e exemplos.
"""
import re  # ou outras bibliotecas necessárias
from stringx.core.basemodule import BaseModule

class AuxNomeModulo(BaseModule):
    """
    Classe do módulo [Nome do Módulo].
    
    Descrição detalhada da funcionalidade do módulo,
    incluindo atributos e métodos disponíveis.
    
    Attributes:
        meta (dict): Metadados do módulo
        options (dict): Opções de configuração
    """
    
    def __init__(self):
        """
        Inicializa o módulo.
        
        Configura metadados, opções e validações específicas do módulo.
        """
        super().__init__()
        
        # Metadados obrigatórios
        self.meta.update({
            "name": "Nome do Módulo",
            "description": "Descrição clara e concisa",
            "author": "Seu Nome",
            "version": "1.0.0",
            "type": "extractor|collector|connector|output|ai"
        })
        
        
        # Opções específicas do módulo (adicionar após as obrigatórias)
        self.options = {
            "data": None,
            "proxy": None,
            "retry": None,
            "retry_delay": None,
            "pattern": str(),  # Padrão específico (se aplicável)
            "timeout": 30,  # Timeout personalizado
            # Outras opções específicas...
        }
    
    def run(self):
        """
        Executa a funcionalidade principal do módulo.
        
        Este método deve implementar a lógica central do módulo,
        processar os dados de entrada e armazenar os resultados.
        """
        data = self.options.get('data')
        if not data:
            self.log_debug("Nenhum dado fornecido")
            return
            
        try:
            # Implementar lógica do módulo aqui
            results = self._process_data(data)
            
            # Armazenar resultados
            if results:
                self.log_debug(f"Processados {len(results)} resultados")
                self.set_result("\n".join(result))
            else:
                self.log_debug("Nenhum resultado encontrado")
                
        except Exception as e:
            self.handle_error(
                e, 
                f"Erro ao processar dados no módulo {self.meta['name']}"
            )
    
    def _process_data(self, data) -> list:
        """
        Método privado para processar os dados.
        
        Args:
            data (str): Dados de entrada
            
        Returns:
            list: Lista de resultados processados
        """
        return ...
        
```

## Criação de Módulos por Tipo

### 1. Módulos EXT (Extratores)

**Localização**: `src/stringx/utils/auxiliary/ext/`

**Propósito**: Extrair dados específicos usando expressões regulares.

**Exemplo - Extrator de Telefones**:

```python
"""
Módulo extrator de números de telefone.

Este módulo extrai números de telefone brasileiros de textos usando regex.
Suporta diferentes formatos: (11) 99999-9999, 11999999999, +5511999999999.
"""
import re
from stringx.core.basemodule import BaseModule

class AuxRegexPhone(BaseModule):
    """
    Módulo para extração de números de telefone brasileiros.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta.update({
            "name": "Phone Extractor",
            "description": "Extrai números de telefone brasileiros",
            "author": "Seu Nome",
            "version": "1.0.0",
            "type": "extractor"
        })
        
        # Opções obrigatórias (sempre devem existir)
        self.options = {
            "data": None,
            "proxy": None,
            "retry": None,
            'retry_delay': None,
        }
        
        # Padrões regex para diferentes formatos
        self.phone_patterns = [
            r'\(\d{2}\)\s*\d{4,5}-?\d{4}',  # (11) 99999-9999
            r'\d{2}\s*\d{4,5}-?\d{4}',      # 11 99999-9999
            r'\+55\d{2}\d{8,9}',            # +5511999999999
        ]
    
    def run(self):
        data = self.options.get('data')
        if not data:
            return
            
        try:
            phones = []
            for pattern in self.phone_patterns:
                matches = re.findall(pattern, data, re.IGNORECASE)
                phones.extend(matches)
            
            # Remove duplicatas mantendo ordem
            unique_phones = list(dict.fromkeys(phones))
            
            if unique_phones:
                self.set_result(unique_phones)
                self.log_debug(f"Encontrados {len(unique_phones)} telefones únicos")
            
        except Exception as e:
            self.handle_error(e, "Erro ao extrair números de telefone")
```

### 2. Módulos CLC (Coletores)

**Localização**: `src/stringx/utils/auxiliary/clc/`

**Propósito**: Coletar dados de serviços externos via APIs ou scraping.

**Exemplo - Coletor de Certificados SSL**:

```python
"""
Módulo coletor de informações de certificados SSL.

Este módulo coleta informações detalhadas sobre certificados SSL/TLS
de domínios, incluindo validade, emissor e subject.
"""
import ssl
import socket
from datetime import datetime
from stringx.core.basemodule import BaseModule

class AuxSSLInfo(BaseModule):
    """
    Coletor de informações de certificados SSL.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta.update({
            "name": "SSL Certificate Info",
            "description": "Coleta informações de certificados SSL",
            "author": "Seu Nome", 
            "version": "1.0.0",
            "type": "collector"
        })
        
        # Opções obrigatórias (sempre devem existir)
        self.options = {
            "data": None,
            "proxy": None,
            "retry": None,
            'retry_delay': None,
            "port": 443,
            "timeout": 10
        }
    
    def run(self):
        domain = self.options.get('data')
        port = self.options.get('port', 443)
        timeout = self.options.get('timeout', 10)
        
        if not domain:
            return
            
        try:
            # Conectar e obter certificado
            context = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            # Processar informações do certificado
            cert_info = self._parse_certificate(cert)
            
            if cert_info:
                self.set_result(cert_info)
                self.log_debug(f"Informações SSL coletadas para {domain}")
                
        except Exception as e:
            self.handle_error(e, f"Erro ao obter certificado SSL de {domain}")
    
    def _parse_certificate(self, cert):
        """Processa informações do certificado."""
        try:
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
            
            return [
                f"Subject: {dict(x[0] for x in cert['subject'])['commonName']}",
                f"Issuer: {dict(x[0] for x in cert['issuer'])['organizationName']}",
                f"Valid From: {not_before.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Valid Until: {not_after.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Days Until Expiry: {(not_after - datetime.now()).days}"
            ]
        except Exception as e:
            self.log_debug(f"Erro ao processar certificado: {e}")
            return []
```

### 3. Módulos CON (Conectores)

**Localização**: `src/stringx/utils/auxiliary/con/`

**Propósito**: Conectar e enviar dados para sistemas externos.

**Exemplo - Conector Redis**:

```python
"""
Módulo conector para Redis.

Este módulo permite armazenar resultados do String-X em bancos Redis,
com suporte a diferentes estruturas de dados e configurações.
"""
import json
from datetime import datetime
try:
    import redis
except ImportError:
    redis = None

from stringx.core.basemodule import BaseModule

class AuxRedisConnector(BaseModule):
    """
    Conector para banco de dados Redis.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta.update({
            "name": "Redis Connector",
            "description": "Armazena dados no Redis",
            "author": "Seu Nome",
            "version": "1.0.0", 
            "type": "connector"
        })
        
        # Opções obrigatórias (sempre devem existir)
        self.options = {
            "data": None,
            "proxy": None,
            "retry": None,
            'retry_delay': None,
            "host": "localhost",
            "port": 6379,
            "db": 0,
            "password": None,
            "key_prefix": "strx:",
            "data_type": "list"  # list, set, hash
        }
    
    def run(self):
        if not redis:
            self.log_debug("Biblioteca redis não encontrada. pip install redis")
            return
            
        data = self.options.get('data')
        if not data:
            return
            
        try:
            # Conectar ao Redis
            client = redis.Redis(
                host=self.options.get('host', 'localhost'),
                port=self.options.get('port', 6379),
                db=self.options.get('db', 0),
                password=self.options.get('password'),
                decode_responses=True
            )
            
            # Testar conexão
            client.ping()
            
            # Armazenar dados
            key = self._generate_key()
            self._store_data(client, key, data)
            
            self.set_result(f"Dados armazenados no Redis com chave: {key}")
            self.log_debug(f"Dados salvos no Redis: {key}")
            
        except Exception as e:
            self.handle_error(e, "Erro ao conectar/armazenar no Redis")
    
    def _generate_key(self):
        """Gera chave única para os dados."""
        prefix = self.options.get('key_prefix', 'strx:')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}{timestamp}"
    
    def _store_data(self, client, key, data):
        """Armazena dados no Redis baseado no tipo configurado."""
        data_type = self.options.get('data_type', 'list')
        
        if data_type == 'list':
            if isinstance(data, list):
                client.lpush(key, *data)
            else:
                client.lpush(key, data)
        elif data_type == 'set':
            if isinstance(data, list):
                client.sadd(key, *data)
            else:
                client.sadd(key, data)
        elif data_type == 'hash':
            # Armazenar como hash com timestamp
            client.hset(key, 'data', json.dumps(data))
            client.hset(key, 'timestamp', datetime.now().isoformat())
        else:
            # Fallback para string
            client.set(key, json.dumps(data))
```

### 4. Módulos OUT (Formatadores)

**Localização**: `src/stringx/utils/auxiliary/out/`

**Propósito**: Formatar saída em diferentes formatos.

**Exemplo - Formatador Markdown**:

```python
"""
Módulo formatador de saída em Markdown.

Este módulo formata os resultados do String-X em formato Markdown,
criando tabelas e listas organizadas para documentação.
"""
import os
from datetime import datetime
from stringx.core.basemodule import BaseModule

class AuxMarkdownFormatter(BaseModule):
    """
    Formatador de saída em Markdown.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta.update({
            "name": "Markdown Formatter",
            "description": "Formata saída em Markdown",
            "author": "Seu Nome",
            "version": "1.0.0",
            "type": "output"
        })
        
        # Opções obrigatórias (sempre devem existir)
        self.options = {
            "data": None,
            "proxy": None,
            "retry": None,
            'retry_delay': None,
            "output_file": "results.md",
            "title": "String-X Results",
            "table_format": True,
            "add_timestamp": True
        }
    
    def run(self):
        data = self.options.get('data')
        if not data:
            return
            
        try:
            output_file = self.options.get('output_file', 'results.md')
            
            # Gerar conteúdo Markdown
            markdown_content = self._generate_markdown(data)
            
            # Salvar arquivo
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.set_result(f"Arquivo Markdown salvo: {output_file}")
            self.log_debug(f"Saída Markdown gerada: {output_file}")
            
        except Exception as e:
            self.handle_error(e, "Erro ao gerar arquivo Markdown")
    
    def _generate_markdown(self, data):
        """Gera conteúdo Markdown formatado."""
        content = []
        
        # Título
        title = self.options.get('title', 'String-X Results')
        content.append(f"# {title}\n")
        
        # Timestamp
        if self.options.get('add_timestamp', True):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content.append(f"**Gerado em**: {timestamp}\n")
        
        # Processar dados
        if isinstance(data, list):
            if self.options.get('table_format', True):
                content.append(self._create_table(data))
            else:
                content.append(self._create_list(data))
        else:
            content.append(f"```\n{data}\n```\n")
        
        return "\n".join(content)
    
    def _create_table(self, data):
        """Cria tabela Markdown."""
        if not data:
            return ""
            
        table = ["| Índice | Resultado |", "|--------|-----------|"]
        
        for i, item in enumerate(data, 1):
            # Escapar caracteres especiais do Markdown
            escaped_item = str(item).replace('|', '\\|').replace('\n', ' ')
            table.append(f"| {i} | {escaped_item} |")
        
        return "\n".join(table) + "\n"
    
    def _create_list(self, data):
        """Cria lista Markdown."""
        if not data:
            return ""
            
        list_items = []
        for item in data:
            list_items.append(f"- {item}")
        
        return "\n".join(list_items) + "\n"
```

## Organização e Estrutura de Arquivos

### Convenções de Nomenclatura

1. **Arquivos de Módulo**: `nome_descritivo.py`
2. **Classes de Módulo**: `AuxTipoNome` (ex: `AuxRegexEmail`, `AuxDNSCollector`)
3. **Métodos Privados**: Prefixar com `_` (ex: `_process_data()`)

### Estrutura de Diretórios

```
src/stringx/utils/auxiliary/
├── __init__.py
├── ext/                    # Módulos Extratores
│   ├── __init__.py
│   ├── email.py           # AuxRegexEmail
│   ├── url.py             # AuxRegexURL
│   └── new_extractor.py   # Seu novo extrator
├── clc/                    # Módulos Coletores
│   ├── __init__.py
│   ├── dns.py             # AuxDNSCollector
│   └── new_collector.py   # Seu novo coletor
├── con/                    # Módulos Conectores
│   ├── __init__.py
│   ├── mysql.py           # AuxMySQLConnector
│   └── new_connector.py   # Seu novo conector
├── out/                    # Módulos de Saída
│   ├── __init__.py
│   ├── json.py            # AuxJSONFormatter
│   └── new_formatter.py   # Seu novo formatador
└── ai/                     # Módulos de IA
    ├── __init__.py
    ├── gemini.py          # AuxGeminiAI
    └── new_ai.py          # Seu novo módulo de IA
```

## Boas Práticas

### 1. Inicialização de Opções
```python
def __init__(self):
    super().__init__()
    
    # Metadados do módulo
    self.meta = {
        'name': '{name}',
        "author": "{author}",
        'version': '{version}',
        'description': '{description}',
        'type': '{type: extractor|collector|connector|output|ai}',
        'example': '{example}'
    }

    # SEMPRE definir opções obrigatórias primeiro
    self.options = {
        "data": None,
        "proxy": None,
        "retry": None,
        'retry_delay': None,
        "custom_option": "default_value"
    }
```

### 2. Tratamento de Erros
```python
def run(self):
    try:
        # Lógica principal
        pass
    except SpecificException as e:
        self.handle_error(e, "Mensagem específica para o usuário")
    except Exception as e:
        self.handle_error(e, "Erro geral no módulo")
```

### 3. Logging e Debug
```python
def run(self):
    self.log_debug("Iniciando processamento...")
    
    # Processamento
    
    self.log_debug(f"Processados {count} itens")
```

### 4. Validação de Entrada
```python
def run(self):
    data = self.options.get('data')
    if not data or not isinstance(data, str):
        self.log_debug("Dados de entrada inválidos")
        return
```

### 5. Performance
```python
def run(self):
    # Para datasets grandes, processar em lotes
    data = self.options.get('data')
    batch_size = 1000
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        results = self._process_batch(batch)
        self.set_result(results)
```

### 6. Compatibilidade de Dependências
```python
try:
    import optional_library
except ImportError:
    optional_library = None

class AuxModule(BaseModule):
    def run(self):
        if not optional_library:
            self.log_debug("Biblioteca opcional não encontrada")
            return
        # Usar biblioteca...
```

## Testes de Módulos

Criar testes para cada módulo novo:

```python
# tests/test_modules/test_new_module.py
import unittest
from stringx.utils.auxiliary.ext.new_module import AuxNewModule

class TestNewModule(unittest.TestCase):
    def setUp(self):
        self.module = AuxNewModule()
    
    def test_basic_functionality(self):
        self.module.options['data'] = "test data"
        self.module.run()
        results = self.module.get_result()
        self.assertIsInstance(results, list)
    
    def test_empty_input(self):
        self.module.options['data'] = ""
        self.module.run()
        results = self.module.get_result()
        self.assertEqual(results, [])
```

## Integração e Registro

Os módulos são automaticamente detectados pelo String-X através do sistema de importação dinâmica. Certifique-se de:

1. Colocar o arquivo na pasta correta (`ext/`, `clc/`, `con/`, `out/`, `ai/`)
2. Seguir a convenção de nomenclatura da classe (`AuxTipoNome`)
3. Herdar de `BaseModule`
4. Implementar o método `run()`
5. Configurar metadados no `__init__()`

## Exemplo Completo

Veja um exemplo funcional completo de um módulo extrator de CEP:

```python
"""
Módulo extrator de CEPs brasileiros.

Este módulo extrai códigos de endereçamento postal (CEP) brasileiros
de textos usando expressões regulares. Suporta formatos com e sem hífen.
"""
import re
from stringx.core.basemodule import BaseModule

class AuxRegexCEP(BaseModule):
    """
    Módulo para extração de CEPs brasileiros.
    
    Extrai CEPs nos formatos:
    - 12345-678 (com hífen)
    - 12345678 (sem hífen)
    
    Valida se o CEP está no formato correto brasileiro (8 dígitos).
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta.update({
            "name": "CEP Extractor",
            "description": "Extrai CEPs brasileiros (formato 12345-678)",
            "author": "String-X Team",
            "version": "1.0.0",
            "type": "extractor"
        })
        
        # Opções obrigatórias (sempre devem existir)
        self.options = {
            "data": None,
            "proxy": None,
            "retry": None,
            'retry_delay': None,
        }
        
        # Padrão regex para CEPs brasileiros
        self.cep_pattern = r'\b\d{5}-?\d{3}\b'
    
    def run(self):
        """Executa a extração de CEPs."""
        data = self.options.get('data')
        if not data:
            self.log_debug("Nenhum dado fornecido para extração de CEP")
            return
            
        try:
            self.log_debug(f"Iniciando extração de CEPs em {len(data)} caracteres")
            
            # Buscar CEPs usando regex
            ceps_found = re.findall(self.cep_pattern, data, re.IGNORECASE)
            
            # Validar e formatar CEPs
            valid_ceps = []
            for cep in ceps_found:
                # Remover hífen para validação
                clean_cep = cep.replace('-', '')
                
                # Validar se tem exatamente 8 dígitos
                if len(clean_cep) == 8 and clean_cep.isdigit():
                    # Adicionar hífen se não tiver
                    formatted_cep = f"{clean_cep[:5]}-{clean_cep[5:]}"
                    valid_ceps.append(formatted_cep)
            
            # Remover duplicatas mantendo ordem
            unique_ceps = list(dict.fromkeys(valid_ceps))
            
            if unique_ceps:
                self.set_result(unique_ceps)
                self.log_debug(f"Encontrados {len(unique_ceps)} CEPs únicos")
                
                # Log detalhado para debug
                for i, cep in enumerate(unique_ceps, 1):
                    self.log_debug(f"  {i}. {cep}")
            else:
                self.log_debug("Nenhum CEP válido encontrado")
                
        except Exception as e:
            self.handle_error(e, "Erro ao extrair CEPs")

    def _validate_cep(self, cep):
        """
        Valida formato de CEP brasileiro.
        
        Args:
            cep (str): CEP a ser validado
            
        Returns:
            bool: True se CEP é válido, False caso contrário
        """
        # Remove hífen e espaços
        clean_cep = cep.replace('-', '').replace(' ', '')
        
        # Verifica se tem exatamente 8 dígitos
        return len(clean_cep) == 8 and clean_cep.isdigit()
```

Este módulo pode ser usado da seguinte forma:

```bash
# Extrair CEPs de um arquivo
./strx -l enderecos.txt -st "{STRING}" -module "ext:cep" -ns -pm

# Extrair CEPs de uma string
./strx -s "Meu endereço é Rua A, 123, CEP: 12345-678" -st "{STRING}" -module "ext:cep" -ns -pm
```

## Próximos Passos

Depois de criar seu módulo:

1. **Teste**: Execute testes básicos para verificar funcionalidade
2. **Documente**: Adicione comentários e docstrings completos
3. **Integre**: Teste a integração com o sistema principal
4. **Otimize**: Refine performance e tratamento de erros
5. **Compartilhe**: Considere contribuir com o projeto

Para dúvidas específicas sobre desenvolvimento de módulos, consulte os outros arquivos de documentação em `docs/dev/` ou examine os módulos existentes como referência.