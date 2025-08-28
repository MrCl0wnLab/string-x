# Estrutura do Projeto String-X

Este documento fornece uma visão detalhada da organização e estrutura do projeto String-X, explicando a função de cada diretório e arquivo principal.

## Visão Geral da Arquitetura

O String-X foi projetado com uma arquitetura modular que separa responsabilidades e facilita a extensibilidade:

```
string-x/
├── 📁 src/                 # Código fonte principal
├── 📁 docs/                # Documentação do projeto
├── 📁 tests/               # Testes unitários e de integração
├── 📁 docker/              # Configurações Docker
├── 📁 asset/               # Recursos (imagens, templates)
├── 📁 output/              # Diretório padrão para arquivos de saída
├── 📄 requirements.txt     # Dependências Python
├── 📄 pyproject.toml       # Configuração do projeto Python
├── 📄 strx                 # Script executável principal
└── 📄 CLAUDE.md           # Guia para Claude Code
```

## Estrutura Detalhada

### 📁 `src/stringx/` - Código Fonte Principal

```
src/stringx/
├── 📄 __init__.py          # Inicialização do pacote
├── 📄 cli.py               # Interface de linha de comando
├── 📁 core/                # Núcleo do sistema
├── 📁 utils/               # Utilitários e módulos auxiliares
└── 📁 config/              # Configurações do sistema
```

#### 📁 `core/` - Núcleo do Sistema

```
core/
├── 📄 basemodule.py        # Classe base para todos os módulos
├── 📄 command.py           # Processamento de comandos
├── 📄 auto_modulo.py       # Sistema de carregamento automático de módulos
├── 📄 func_format.py       # Processamento de funções em templates
├── 📄 format.py            # Formatação e limpeza de dados
├── 📄 logger.py            # Sistema de logging
├── 📄 output_formatter.py  # Formatação de saídas
├── 📄 randomvalue.py       # Geração de valores aleatórios
├── 📄 http_async.py        # Cliente HTTP assíncrono
├── 📄 security_validator.py # Validação de segurança
├── 📄 thread_process.py    # Gerenciamento de threads
└── 📁 banner/              # Sistema de banners ASCII
    ├── 📄 asciiart.py      # Arte ASCII
    └── 📄 banner.py        # Geração de banners
```

**Responsabilidades do Core:**
- **`basemodule.py`**: Classe base que todos os módulos herdam, fornecendo funcionalidades comuns
- **`command.py`**: Classe principal que gerencia execução de comandos e módulos
- **`auto_modulo.py`**: Carregamento dinâmico e descoberta de módulos
- **`func_format.py`**: Detecção e execução de funções em templates `{STRING}`
- **`logger.py`**: Sistema de logging unificado com níveis de verbosidade
- **`security_validator.py`**: Validação de comandos para prevenir injeção shell

#### 📁 `utils/` - Utilitários

```
utils/
├── 📁 auxiliary/           # Módulos auxiliares organizados por tipo
│   ├── 📁 ext/            # Módulos extratores (EXT)
│   ├── 📁 clc/            # Módulos coletores (CLC)
│   ├── 📁 con/            # Módulos conectores (CON)
│   ├── 📁 out/            # Módulos de saída (OUT)
│   └── 📁 ai/             # Módulos de IA (AI)
└── 📁 helper/              # Funções auxiliares
    ├── 📄 functions.py     # Funções para templates dinâmicos
    ├── 📄 file_local.py    # Operações com arquivos locais
    └── 📄 style_cli.py     # Estilização da interface CLI
```

### 📁 `utils/auxiliary/` - Módulos por Categoria

#### 📁 `ext/` - Módulos Extratores
*Extraem dados específicos usando regex*

```
ext/
├── 📄 email.py             # AuxRegexEmail - extrai emails
├── 📄 url.py               # AuxRegexURL - extrai URLs
├── 📄 ip.py                # AuxRegexIP - extrai endereços IP
├── 📄 domain.py            # AuxRegexDomain - extrai domínios
├── 📄 phone.py             # AuxRegexPhone - extrai telefones
├── 📄 hash.py              # AuxRegexHash - extrai hashes
├── 📄 credential.py        # AuxRegexCredential - extrai credenciais
├── 📄 credit_card.py       # AuxRegexCreditCard - extrai cartões
├── 📄 cryptocurrency.py    # AuxRegexCrypto - extrai wallets crypto
├── 📄 documents.py         # AuxRegexDocuments - extrai CPF, CNPJ
├── 📄 file_hash.py         # AuxRegexFileHash - hashes de arquivos
├── 📄 mac.py               # AuxRegexMAC - extrai endereços MAC
├── 📄 metadata.py          # AuxRegexMetadata - extrai metadados
└── 📄 custom_regex.py      # AuxRegexCustom - regex personalizados
```

#### 📁 `clc/` - Módulos Coletores
*Coletam dados de serviços externos*

```
clc/
├── 📄 dns.py               # AuxDNSCollector - consultas DNS
├── 📄 whois.py             # AuxWhoisCollector - consultas Whois
├── 📄 shodan.py            # AuxShodanCollector - API Shodan
├── 📄 virustotal.py        # AuxVirusTotalCollector - API VirusTotal
├── 📄 google.py            # AuxGoogleCollector - busca Google
├── 📄 googlecse.py         # AuxGoogleCSECollector - Google Custom Search
├── 📄 bing.py              # AuxBingCollector - busca Bing
├── 📄 yahoo.py             # AuxYahooCollector - busca Yahoo
├── 📄 duckduckgo.py        # AuxDuckDuckGoCollector - busca DuckDuckGo
├── 📄 subdomain.py         # AuxSubdomainCollector - subdomínios
├── 📄 crtsh.py             # AuxCrtShCollector - certificados SSL
├── 📄 spider.py            # AuxSpiderCollector - web crawler
├── 📄 geoip.py             # AuxGeoIPCollector - geolocalização IP
├── 📄 ipinfo.py            # AuxIPInfoCollector - informações IP
├── 📄 http_probe.py        # AuxHTTPProbe - verificação HTTP
├── 📄 netscan.py           # AuxNetScanCollector - scan de rede
├── 📄 github.py            # AuxGitHubCollector - API GitHub
├── 📄 emailverify.py       # AuxEmailVerifyCollector - verificação email
├── 📄 archive.py           # AuxArchiveCollector - Wayback Machine
├── 📄 url_check.py         # AuxURLCheckCollector - verificação URLs
└── 📄 ezilon.py            # AuxEzilonCollector - diretório Ezilon
```

#### 📁 `con/` - Módulos Conectores
*Conectam com sistemas externos*

```
con/
├── 📄 mysql.py             # AuxMySQLConnector - MySQL
├── 📄 mongodb.py           # AuxMongoDBConnector - MongoDB
├── 📄 opensearch.py        # AuxOpenSearchConnector - OpenSearch
├── 📄 sqlite.py            # AuxSQLiteConnector - SQLite
├── 📄 ssh.py               # AuxSSHConnector - SSH
├── 📄 ftp.py               # AuxFTPConnector - FTP
├── 📄 s3.py                # AuxS3Connector - Amazon S3
├── 📄 telegram.py          # AuxTelegramConnector - Telegram Bot
├── 📄 slack.py             # AuxSlackConnector - Slack
└── 📄 discord.py           # AuxDiscordConnector - Discord
```

#### 📁 `out/` - Módulos de Saída
*Formatam saídas em diferentes formatos*

```
out/
├── 📄 json.py              # AuxJSONFormatter - saída JSON
├── 📄 csv.py               # AuxCSVFormatter - saída CSV
├── 📄 xml.py               # AuxXMLFormatter - saída XML
└── 📄 html.py              # AuxHTMLFormatter - saída HTML
```

#### 📁 `ai/` - Módulos de IA
*Integração com serviços de Inteligência Artificial*

```
ai/
├── 📄 gemini.py            # AuxGeminiAI - Google Gemini
└── 📄 openai.py            # AuxOpenAI - OpenAI GPT
```

### 📁 `config/` - Configurações

```
config/
├── 📄 __init__.py          # Inicialização
├── 📄 setting.py           # Configurações principais
└── 📄 default.json         # Valores padrão de configuração
```

**Arquivos de Configuração:**
- **`setting.py`**: Carrega configurações do `default.json` e exporta como módulo
- **`default.json`**: Configurações centralizadas (threads, timeouts, formatos, etc.)

### 📁 `tests/` - Testes

```
tests/
├── 📄 test_cli.py              # Testes da interface CLI
├── 📄 test_file_io.py          # Testes de operações com arquivos
├── 📄 test_pipeline.py         # Testes de pipeline end-to-end
├── 📄 test_template_substitution.py # Testes de substituição de templates
├── 📄 test_file_io_comprehensive.py # Testes abrangentes I/O
└── 📁 test_modules/            # Testes específicos de módulos
    ├── 📄 test_ext_modules.py  # Testes módulos EXT
    ├── 📄 test_clc_modules.py  # Testes módulos CLC
    └── 📄 test_functions.py    # Testes das funções auxiliares
```

### 📁 `docs/` - Documentação

```
docs/
├── 📄 README.md                # Visão geral da documentação
├── 📁 dev/                     # Documentação para desenvolvedores
│   ├── 📄 README.md           # Índice desenvolvimento
│   ├── 📄 criacao-modulos.md  # Guia criação de módulos
│   ├── 📄 criacao-funcoes.md  # Guia criação de funções
│   ├── 📄 uso-como-biblioteca.md # Usar String-X como lib
│   └── 📄 estrutura-projeto.md # Este documento
├── 📁 usabilidade/            # Documentação do usuário
│   ├── 📄 README.md           # Índice usabilidade
│   ├── 📄 parametros.md       # Referência parâmetros
│   ├── 📄 comandos-essenciais.md # Comandos essenciais
│   ├── 📄 exemplos-praticos.md # Exemplos práticos
│   ├── 📄 uso-basico.md       # Uso básico
│   ├── 📄 strings-unicas.md   # Processamento string única
│   ├── 📄 encadeamento-modulos.md # Encadeamento módulos
│   ├── 📄 docker.md           # Uso com Docker
│   └── 📁 modulos/            # Documentação específica módulos
└── 📁 tunning/                # Otimização e performance
    ├── 📄 README.md           # Índice tunning
    ├── 📄 otimizacao-performance.md # Otimização
    └── 📄 scripts-automacao.md # Scripts automação
```

### 📁 `docker/` - Containerização

```
docker/
├── 📁 strx-docker-compose/        # String-X com MySQL
│   ├── 📄 docker-compose.yml      # Compose principal
│   ├── 📄 Dockerfile              # Dockerfile String-X
│   ├── 📄 .env.example           # Variáveis ambiente
│   └── 📄 README.md              # Documentação Docker
├── 📁 mysql-docker-compose/       # MySQL standalone
│   ├── 📄 docker-compose.yml
│   └── 📄 README.md
└── 📁 opensearch-docker-compose/  # OpenSearch setup
    ├── 📄 docker-compose.yml
    └── 📄 README.md
```

### 📁 `asset/` - Recursos

```
asset/
├── 📁 img/                    # Imagens do projeto
│   ├── 📄 logo.png           # Logo principal
│   ├── 📄 banner.png         # Banner
│   └── 📄 screenshots/       # Capturas de tela
├── 📁 templates/             # Templates diversos
│   ├── 📄 report.html        # Template relatório HTML
│   └── 📄 notification.json  # Template notificação
└── 📁 audio/                 # Áudios para notificações
    ├── 📄 notification.wav   # Som notificação padrão
    └── 📄 complete.wav       # Som conclusão
```

## Fluxo de Dados no Sistema

### 1. Inicialização
```
strx (script) → cli.py → main_cli() → RichArgumentParser
```

### 2. Processamento de Entrada
```
CLI Args → FileLocal/stdin_get_list → Format.clear_value → ThreadProcess
```

### 3. Execução de Comandos
```
ThreadProcess → Command.command_template → AutoModulo/Shell
```

### 4. Processamento de Módulos
```
AutoModulo → BaseModule.run() → set_result() → OutputFormatter
```

### 5. Formatação e Saída
```
OutputFormatter → FileLocal.write_output → Console/File
```

## Convenções de Código

### Nomenclatura de Classes
- **Módulos Auxiliares**: `AuxTipoNome` (ex: `AuxRegexEmail`, `AuxDNSCollector`)
- **Classes Core**: `NomeClasse` (ex: `Command`, `BaseModule`)
- **Utilitários**: `NomeUtil` (ex: `Format`, `FileLocal`)

### Estrutura de Arquivos
- **Módulos**: Um módulo por arquivo, nome descritivo
- **Imports**: Ordem padrão (stdlib, terceiros, locais)
- **Docstrings**: Google style para todas as classes e métodos

### Organização de Imports
```python
# 1. Bibliotecas padrão
import os
import re
import json

# 2. Bibliotecas de terceiros
import requests
from rich.console import Console

# 3. Imports locais
from stringx.core.basemodule import BaseModule
from stringx.core.logger import logger
```

## Padrões de Design Utilizados

### 1. Strategy Pattern
- **Módulos auxiliares**: Diferentes estratégias para extrair/coletar dados
- **Formatadores**: Diferentes formatos de saída (JSON, CSV, XML)

### 2. Factory Pattern
- **AutoModulo**: Criação dinâmica de módulos baseada em strings
- **OutputFormatter**: Seleção de formatador baseado em parâmetro

### 3. Template Method Pattern
- **BaseModule**: Template para estrutura de módulos
- **Command**: Template para processamento de comandos

### 4. Observer Pattern
- **Logger**: Notificação de eventos para diferentes handlers
- **Progress**: Notificação de progresso para interface

## Pontos de Extensão

### 1. Adicionando Novos Tipos de Módulos
```python
# 1. Criar pasta em utils/auxiliary/
# 2. Implementar classe herdando BaseModule
# 3. Seguir convenção AuxTipoNome
# 4. Definir meta.type apropriado
```

### 2. Adicionando Novas Funções
```python
# 1. Abrir utils/helper/functions.py
# 2. Adicionar método estático à classe Funcs
# 3. Seguir padrão de documentação
# 4. Implementar tratamento de erros silencioso
```

### 3. Novos Formatadores de Saída
```python
# 1. Criar arquivo em utils/auxiliary/out/
# 2. Implementar classe herdando BaseModule
# 3. Definir meta.type = "output"
# 4. Implementar lógica de formatação
```

## Configuração e Personalização

### Arquivo de Configuração (`config/default.json`)
```json
{
  "STRX_THREAD_MAX": 10,
  "STRX_TIMEOUT": 30,
  "STRX_OUTPUT_FORMATS": ["txt", "json", "csv"],
  "STRX_DEFAULT_OUTPUT_FORMAT": "txt",
  "STRX_LOG_LEVEL": "INFO",
  "STRX_RETRY_OPERATIONS": 1,
  "STRX_RETRY_DELAY": 5
}
```

### Variáveis de Ambiente
```bash
export STRX_THREADS=20
export STRX_DEBUG=true
export STRX_OUTPUT_DIR="/custom/output"
```

## Dependências Principais

### Core Dependencies (`requirements.txt`)
```
requests>=2.31.0          # HTTP requests
rich>=13.0.0              # CLI interface rica
psutil>=5.9.0             # System monitoring
validators>=0.20.0        # Data validation
dnspython>=2.3.0          # DNS operations
```

### Optional Dependencies
```
mysql-connector-python    # MySQL support
pymongo                   # MongoDB support
opensearch-py            # OpenSearch support
paramiko                 # SSH support
```

## Performance e Otimização

### Áreas de Performance Críticas
1. **ThreadProcess**: Gerenciamento eficiente de threads
2. **AutoModulo**: Cache de módulos carregados
3. **Regex**: Compilação única e reutilização
4. **I/O**: Leitura em lotes para arquivos grandes

### Monitoramento
- **Logger**: Métricas de performance em debug mode
- **Memory**: Monitoramento de uso de memória
- **Network**: Timeout e retry em operações de rede

## Segurança

### Validações Implementadas
1. **Command Injection**: `SecurityValidator` para comandos shell
2. **Path Traversal**: Validação de caminhos de arquivo
3. **Resource Limits**: Limites de threads, timeouts, tamanho
4. **Input Sanitization**: Limpeza de entrada em `Format.clear_value`

### Modo No-Shell
- **Direct Processing**: Bypass de shell para módulos/funções
- **Enhanced Security**: Eliminação de riscos de injeção
- **Better Performance**: Sem overhead de subprocessos

Esta estrutura modular permite fácil manutenção, extensibilidade e contribuição da comunidade, mantendo separação clara de responsabilidades e fornecendo pontos de extensão bem definidos.