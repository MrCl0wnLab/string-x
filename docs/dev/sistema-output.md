# Sistema de Output

Este documento detalha o sistema de saída (output) do String-X, que é responsável por formatar, exibir e armazenar os resultados das operações.

## Visão Geral

O sistema de saída do String-X foi projetado para ser flexível e extensível, permitindo que os resultados sejam:

1. **Formatados** em diferentes formatos (texto, JSON, CSV, etc.)
2. **Exibidos** na interface de linha de comando com estilos e cores
3. **Armazenados** em arquivos locais ou sistemas externos
4. **Filtrados** através de pipes ou expressões
5. **Transformados** antes de serem exibidos ou armazenados

Este sistema é implementado através de classes formatadoras no núcleo e módulos de output (OUT) para integração com sistemas externos.

## Componentes do Sistema de Saída

### 1. Core Output Formatter

A classe principal `OutputFormatter` em `core/output_formatter.py` é responsável por:

- Definir formatos padrão de saída
- Converter resultados entre diferentes formatos
- Aplicar estilos e formatação visual
- Gerenciar a saída para arquivos ou console

### 2. Módulos de Output (OUT)

Os módulos de output em `utils/auxiliary/out/` fornecem integrações com sistemas externos:

- **MySQL**: Armazenamento em bancos de dados relacionais
- **OpenSearch**: Indexação e busca em OpenSearch
- **Custom**: Formatos personalizados ou sistemas externos

### 3. Sistema de Estilo CLI

O componente `core/style_cli.py` gerencia a aparência visual da saída no terminal:

- Cores para diferentes tipos de mensagens
- Formatação de texto (negrito, itálico, sublinhado)
- Barras de progresso e indicadores de status
- Tabelas e layouts estruturados

## Formatos de Saída Suportados

O String-X suporta vários formatos de saída nativamente:

| Formato | Descrição | Uso |
|---------|-----------|-----|
| **TXT** | Texto plano, uma linha por resultado | `-format txt` |
| **CSV** | Valores separados por vírgula | `-format csv` |
| **JSON** | JavaScript Object Notation | `-format json` |
| **JSONL** | JSON Lines (um objeto JSON por linha) | `-format jsonl` |
| **XML** | Extensible Markup Language | `-format xml` |
| **HTML** | HTML formatado para visualização em navegador | `-format html` |
| **TABLE** | Tabela formatada para terminal | `-format table` |
| **YAML** | YAML Ain't Markup Language | `-format yaml` |

## Arquitetura do Sistema de Saída

### Diagrama de Fluxo

```
┌─────────────────┐        ┌──────────────────────┐
│  Resultados     │───────▶│ OutputFormatter      │
│  (raw data)     │        │ (core/output_formatter.py) │
└─────────────────┘        └──────────────┬───────┘
                                         │
                                         ▼
                ┌─────────────────────────────────────────┐
                │          Formatação de Saída            │
                │                                         │
┌───────────────┼───────────────┬───────────────┬────────┼───────────┐
▼               ▼               ▼               ▼        ▼           ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ TXT     │  │ CSV     │  │ JSON    │  │ XML     │  │ TABLE   │  │ Outros  │
│ Format  │  │ Format  │  │ Format  │  │ Format  │  │ Format  │  │ Formatos│
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     │            │            │            │            │            │
     └────────────┴─────┬──────┴────────────┴────────────┴────────────┘
                        │
                        ▼
        ┌─────────────────────────────────────────┐
        │          Destino de Saída               │
        │                                         │
┌───────┴────────┐   ┌────────────────┐   ┌──────┴─────────┐
▼                ▼   ▼                ▼   ▼                ▼
┌─────────────┐  │ ┌─────────────┐    │ ┌─────────────┐    │
│ Console     │  │ │ Arquivo     │    │ │ Módulos OUT │    │
│ (stdout)    │  │ │ Local       │    │ │ (Sistemas   │    │
│             │  │ │             │    │ │ Externos)   │    │
└─────────────┘  │ └─────────────┘    │ └─────────────┘    │
                 │                    │                    │
                 └────────────────────┴────────────────────┘
```

### Classe Base de Output

A classe base para módulos de output (`BaseOutput`) em `core/basemodule.py`:

```python
class BaseOutput:
    """Classe base para módulos de output."""
    
    def __init__(self):
        self.name = ""
        self.description = ""
        self.author = ""
        self.version = ""
    
    def output(self, data, **kwargs):
        """
        Método principal que deve ser implementado por todas as subclasses.
        
        Args:
            data (list/dict): Dados a serem exportados
            **kwargs: Parâmetros adicionais para controlar o comportamento da saída
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário
        """
        raise NotImplementedError("Método output deve ser implementado")
```

## Formatos de Saída Detalhados

### Texto (TXT)

O formato mais simples, onde cada resultado é exibido em uma linha separada:

```
resultado1
resultado2
resultado3
```

Exemplo de uso:
```bash
./strx -l dominios.txt -st "dig +short {STRING}" -format txt -o resultados.txt
```

### CSV (Comma-Separated Values)

Formato tabular com valores separados por vírgula, adequado para importação em planilhas:

```
campo1,campo2,campo3
valor1,valor2,valor3
valor4,valor5,valor6
```

Exemplo de uso:
```bash
./strx -l dominios.txt -module "clc:dns" -pm -format csv -o dns_results.csv
```

### JSON (JavaScript Object Notation)

Formato estruturado adequado para dados hierárquicos:

```json
[
  {
    "campo1": "valor1",
    "campo2": "valor2",
    "campo3": {
      "subcampo1": "subvalor1",
      "subcampo2": "subvalor2"
    }
  },
  {
    "campo1": "valor3",
    "campo2": "valor4",
    "campo3": {
      "subcampo1": "subvalor3",
      "subcampo2": "subvalor4"
    }
  }
]
```

Exemplo de uso:
```bash
./strx -l ips.txt -module "clc:shodan" -pm -format json -o shodan_results.json
```

### JSONL (JSON Lines)

Similar ao JSON, mas com um objeto por linha, adequado para processamento de streaming:

```
{"campo1": "valor1", "campo2": "valor2"}
{"campo1": "valor3", "campo2": "valor4"}
```

Exemplo de uso:
```bash
./strx -l urls.txt -module "ext:url" -pm -format jsonl -o urls.jsonl
```

### TABLE

Formato tabular para exibição em terminal:

```
+----------+----------+----------+
| Campo 1  | Campo 2  | Campo 3  |
+----------+----------+----------+
| valor1   | valor2   | valor3   |
| valor4   | valor5   | valor6   |
+----------+----------+----------+
```

Exemplo de uso:
```bash
./strx -l emails.txt -module "clc:emailverify" -pm -format table
```

## Implementação de Formatadores

### Classe OutputFormatter

A classe principal que gerencia a formatação de saída:

```python
class OutputFormatter:
    """
    Formatador de saída para o String-X.
    
    Esta classe gerencia a conversão, formatação e exportação
    dos resultados em diferentes formatos.
    """
    
    def __init__(self, format_type="txt"):
        """
        Inicializa o formatador.
        
        Args:
            format_type (str): O tipo de formato (txt, json, csv, etc.)
        """
        self.format_type = format_type.lower()
        self.supported_formats = ["txt", "csv", "json", "jsonl", "xml", "html", "table", "yaml"]
        
        if self.format_type not in self.supported_formats:
            raise ValueError(f"Formato não suportado: {format_type}")
    
    def format(self, data):
        """
        Formata os dados de acordo com o tipo de formato selecionado.
        
        Args:
            data: Os dados a serem formatados
            
        Returns:
            str: Os dados formatados
        """
        if self.format_type == "txt":
            return self._format_txt(data)
        elif self.format_type == "csv":
            return self._format_csv(data)
        elif self.format_type == "json":
            return self._format_json(data)
        # ... outros formatos
        
    def _format_txt(self, data):
        """Formata os dados como texto plano."""
        if isinstance(data, list):
            return "\n".join(str(item) for item in data)
        return str(data)
        
    def _format_csv(self, data):
        """Formata os dados como CSV."""
        # Implementação CSV
        
    def _format_json(self, data):
        """Formata os dados como JSON."""
        import json
        return json.dumps(data, indent=2)
        
    # ... outros métodos de formatação
    
    def output(self, data, file_path=None, append=False):
        """
        Envia a saída formatada para o destino apropriado.
        
        Args:
            data: Os dados a serem enviados
            file_path (str, optional): Caminho para arquivo de saída
            append (bool): Adicionar ao arquivo ao invés de sobrescrever
            
        Returns:
            bool: True se bem-sucedido
        """
        formatted_data = self.format(data)
        
        if file_path:
            mode = 'a' if append else 'w'
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(formatted_data)
                if not formatted_data.endswith('\n'):
                    f.write('\n')
        else:
            print(formatted_data)
            
        return True
```

## Módulos de Output

Os módulos OUT permitem exportar resultados para sistemas externos.

### Exemplo: Módulo MySQL

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from core.basemodule import BaseOutput
from core.logger import get_logger

class MySQLOutput(BaseOutput):
    """
    Módulo de output para MySQL.
    
    Este módulo permite armazenar resultados em um banco de dados MySQL.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "mysql"
        self.description = "Armazena resultados em MySQL"
        self.author = "String-X Team"
        self.version = "1.0"
        self.logger = get_logger(__name__)
        
    def output(self, data, **kwargs):
        """
        Armazena dados em um banco MySQL.
        
        Args:
            data: Dados a serem armazenados
            **kwargs: Parâmetros de conexão:
                - host: Host do banco (padrão: localhost)
                - port: Porta (padrão: 3306)
                - username: Nome de usuário
                - password: Senha
                - database: Nome do banco de dados
                - table: Nome da tabela
                - create_table: Criar tabela se não existir (padrão: True)
                
        Returns:
            bool: True se bem-sucedido
        """
        # Extrair parâmetros
        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 3306)
        username = kwargs.get('username', 'root')
        password = kwargs.get('password', '')
        database = kwargs.get('database', 'strx')
        table = kwargs.get('table', 'results')
        create_table = kwargs.get('create_table', True)
        
        # Validar dados
        if not data:
            self.logger.warning("Nenhum dado a ser armazenado")
            return True
            
        # Normalizar dados para lista
        if not isinstance(data, list):
            data = [data]
            
        try:
            # Conectar ao MySQL
            self.logger.debug(f"Conectando ao MySQL em {host}:{port}")
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            cursor = conn.cursor()
            
            # Criar tabela se necessário
            if create_table:
                self._ensure_table_exists(cursor, table)
                
            # Inserir dados
            self._insert_data(cursor, table, data)
                
            # Commit e finalização
            conn.commit()
            cursor.close()
            conn.close()
            
            self.logger.info(f"Dados armazenados com sucesso em {database}.{table}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao armazenar dados no MySQL: {str(e)}")
            return False
            
    def _ensure_table_exists(self, cursor, table):
        """
        Garante que a tabela existe, criando-a se necessário.
        """
        # Verificar se tabela existe
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        result = cursor.fetchone()
        
        if not result:
            # Criar tabela results com estrutura flexível
            self.logger.info(f"Criando tabela {table}")
            cursor.execute(f"""
                CREATE TABLE {table} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    source VARCHAR(255),
                    target VARCHAR(255),
                    data TEXT,
                    type VARCHAR(50),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
    def _insert_data(self, cursor, table, data):
        """
        Insere os dados na tabela.
        """
        for item in data:
            if isinstance(item, dict):
                # Para dicionários, usar chaves como campos
                source = item.get('source', '')
                target = item.get('target', '')
                data_value = item.get('data', '')
                type_value = item.get('type', '')
            else:
                # Para strings ou outros tipos, usar como target
                source = ''
                target = str(item)
                data_value = ''
                type_value = ''
                
            # Inserir na tabela
            cursor.execute(f"""
                INSERT INTO {table} (source, target, data, type)
                VALUES (%s, %s, %s, %s)
            """, (source, target, data_value, type_value))
```

### Exemplo: Módulo OpenSearch

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from datetime import datetime
from core.basemodule import BaseOutput
from core.logger import get_logger

class OpenSearchOutput(BaseOutput):
    """
    Módulo de output para OpenSearch.
    
    Este módulo permite indexar resultados em um cluster OpenSearch.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "opensearch"
        self.description = "Indexa resultados em OpenSearch"
        self.author = "String-X Team"
        self.version = "1.0"
        self.logger = get_logger(__name__)
        
    def output(self, data, **kwargs):
        """
        Indexa dados em um cluster OpenSearch.
        
        Args:
            data: Dados a serem indexados
            **kwargs: Parâmetros de conexão:
                - host: Host do cluster (padrão: localhost)
                - port: Porta (padrão: 9200)
                - username: Nome de usuário (opcional)
                - password: Senha (opcional)
                - index: Nome do índice (padrão: strx-data)
                - create_index: Criar índice se não existir (padrão: True)
                
        Returns:
            bool: True se bem-sucedido
        """
        # Extrair parâmetros
        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 9200)
        username = kwargs.get('username', '')
        password = kwargs.get('password', '')
        index = kwargs.get('index', 'strx-data')
        create_index = kwargs.get('create_index', True)
        
        # Validar dados
        if not data:
            self.logger.warning("Nenhum dado a ser indexado")
            return True
            
        # Normalizar dados para lista
        if not isinstance(data, list):
            data = [data]
            
        try:
            # Configurar autenticação
            auth = None
            if username and password:
                auth = (username, password)
                
            # Verificar conexão
            base_url = f"http://{host}:{port}"
            self.logger.debug(f"Conectando ao OpenSearch em {base_url}")
            
            response = requests.get(base_url, auth=auth)
            if response.status_code != 200:
                self.logger.error(f"Erro ao conectar ao OpenSearch: {response.status_code}")
                return False
                
            # Criar índice se necessário
            if create_index:
                self._ensure_index_exists(base_url, index, auth)
                
            # Indexar dados
            bulk_data = self._prepare_bulk_data(data, index)
            
            # Enviar para o OpenSearch
            bulk_url = f"{base_url}/_bulk"
            headers = {"Content-Type": "application/x-ndjson"}
            
            response = requests.post(bulk_url, headers=headers, data=bulk_data, auth=auth)
            
            if response.status_code >= 200 and response.status_code < 300:
                self.logger.info(f"Dados indexados com sucesso em {index}")
                return True
            else:
                self.logger.error(f"Erro ao indexar dados: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao indexar dados no OpenSearch: {str(e)}")
            return False
            
    def _ensure_index_exists(self, base_url, index, auth):
        """
        Garante que o índice existe, criando-o se necessário.
        """
        # Verificar se índice existe
        index_url = f"{base_url}/{index}"
        response = requests.head(index_url, auth=auth)
        
        if response.status_code == 404:
            # Criar índice
            self.logger.info(f"Criando índice {index}")
            
            # Configuração básica do índice
            index_config = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "source": {"type": "keyword"},
                        "target": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "data": {"type": "text"},
                        "type": {"type": "keyword"},
                        "timestamp": {"type": "date"}
                    }
                }
            }
            
            response = requests.put(index_url, json=index_config, auth=auth)
            
            if response.status_code >= 200 and response.status_code < 300:
                self.logger.info(f"Índice {index} criado com sucesso")
            else:
                self.logger.error(f"Erro ao criar índice: {response.text}")
                
    def _prepare_bulk_data(self, data, index):
        """
        Prepara dados no formato bulk para indexação.
        """
        bulk_data = ""
        timestamp = datetime.utcnow().isoformat()
        
        for item in data:
            # Metadata
            action = {"index": {"_index": index}}
            bulk_data += json.dumps(action) + "\n"
            
            # Document
            if isinstance(item, dict):
                # Adicionar timestamp se não existir
                if 'timestamp' not in item:
                    item['timestamp'] = timestamp
                doc = item
            else:
                # Para strings ou outros tipos, criar documento padrão
                doc = {
                    "target": str(item),
                    "timestamp": timestamp
                }
                
            bulk_data += json.dumps(doc) + "\n"
            
        return bulk_data
```

## Personalização da Saída

O String-X oferece várias maneiras de personalizar a saída:

### 1. Formatação Visual (Terminal)

```python
from core.style_cli import Style

# Texto colorido
print(Style.red("Erro: Conexão falhou"))
print(Style.green("Sucesso: Dados processados"))

# Formatação
print(Style.bold("Texto em negrito"))
print(Style.italic("Texto em itálico"))

# Combinações
print(Style.bold(Style.blue("Texto em negrito e azul")))

# Tabelas
headers = ["ID", "Nome", "Status"]
rows = [
    ["1", "Item 1", "Ativo"],
    ["2", "Item 2", "Inativo"],
    ["3", "Item 3", "Pendente"]
]
print(Style.table(headers, rows))

# Barras de progresso
with Style.progress_bar(total=100) as bar:
    for i in range(100):
        # Processamento...
        bar.update(1)
```

### 2. Filtros de Saída

O parâmetro `-p` (pipe) permite filtrar a saída antes de exibi-la:

```bash
# Filtrar apenas linhas contendo "open"
./strx -l ips.txt -st "nmap -p 80,443 {STRING}" -p "grep open"

# Contar ocorrências de uma palavra
./strx -l dominios.txt -st "dig {STRING}" -p "grep -c 'NXDOMAIN'"
```

### 3. Transformação de Formato

O sistema permite converter entre formatos:

```python
from core.output_formatter import OutputFormatter

# Converter de JSON para CSV
with open('data.json', 'r') as f:
    data = json.load(f)
    
formatter = OutputFormatter(format_type="csv")
csv_data = formatter.format(data)

with open('data.csv', 'w') as f:
    f.write(csv_data)
```

## Integração com Sistemas Externos

Os módulos OUT permitem integração com diversos sistemas:

### 1. Bancos de Dados

```bash
# MySQL
./strx -l domains.txt -module "clc:dns|out:mysql" -pm \
  -host localhost -port 3306 -username user -password pass \
  -database recon -table dns_records

# OpenSearch
./strx -l domains.txt -module "clc:subdomain|out:opensearch" -pm \
  -host localhost -port 9200 -index strx-subdomains
```

### 2. APIs e Web Services

```bash
# Enviar para webhook
./strx -l urls.txt -module "clc:http_probe|out:webhook" -pm \
  -url "https://hooks.example.com/incoming" \
  -headers '{"Authorization": "Bearer token123"}'
```

### 3. Sistemas de Arquivos

```bash
# Exportar para arquivo local em formato específico
./strx -l ips.txt -module "clc:shodan" -pm -format json -o shodan_results.json

# Anexar a um arquivo existente
./strx -l new_ips.txt -module "clc:shodan" -pm -format json -o shodan_results.json -a
```

## Melhores Práticas

### Para Usuários

1. **Escolha o Formato Adequado**:
   - Use TXT para resultados simples e processamento em pipe
   - Use JSON para preservar estruturas de dados complexas
   - Use CSV para análise em planilhas
   - Use TABLE para visualização no terminal

2. **Filtragem Eficiente**:
   - Utilize o parâmetro `-p` para filtrar resultados
   - Combine com ferramentas como `grep`, `awk`, `jq` para análises mais complexas

3. **Armazenamento Persistente**:
   - Para resultados pequenos: arquivos locais
   - Para grandes volumes: bancos de dados ou OpenSearch
   - Para análises complexas: exportação para formatos estruturados

### Para Desenvolvedores

1. **Implementação de Novos Formatadores**:
   - Siga a interface existente
   - Mantenha a consistência com outros formatadores
   - Documente claramente o formato de saída

2. **Criação de Módulos OUT**:
   - Implemente tratamento de erros robusto
   - Ofereça opções de configuração flexíveis
   - Garanta que o módulo seja resiliente a falhas de conexão

3. **Extensão do Sistema de Estilo**:
   - Mantenha compatibilidade com diferentes terminais
   - Ofereça fallbacks para ambientes sem suporte a cores
   - Teste em diferentes tamanhos de terminal

## Limitações e Considerações

1. **Formatação de Dados Complexos**: Alguns formatos (como TXT) podem não preservar adequadamente estruturas de dados aninhadas

2. **Desempenho**: Para grandes volumes de dados, considere o impacto de performance da formatação e exportação

3. **Compatibilidade de Terminal**: Nem todos os recursos visuais são suportados em todos os terminais

4. **Segurança**: Ao exportar para sistemas externos, considere as implicações de segurança (armazenamento de credenciais, sanitização de dados)

## Futuras Direções

O sistema de saída pode evoluir em várias direções:

1. **Visualizações Avançadas**: Gráficos e visualizações no terminal

2. **Templates Personalizados**: Sistema de templates para formatos de saída personalizados

3. **Streaming de Saída**: Suporte para processamento e saída em stream para grandes volumes

4. **Mais Integrações**: Módulos para mais sistemas externos (ElasticSearch, MongoDB, etc.)

5. **Exportação Multi-formato**: Exportar os mesmos resultados em múltiplos formatos simultaneamente
