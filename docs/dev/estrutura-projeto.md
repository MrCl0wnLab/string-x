# Estrutura do Projeto

Este documento descreve a organização dos diretórios e arquivos do projeto String-X, explicando a função de cada componente da estrutura.

## Visão Geral

A estrutura do projeto String-X é organizada de forma modular, separando claramente as diferentes responsabilidades e funcionalidades do sistema. A estrutura geral é a seguinte:

```
string-x/
├── asset/                 # Recursos gráficos e imagens para documentação
├── config/                # Configurações e arquivos de configuração
├── core/                  # Núcleo da aplicação e funcionalidades principais
│   └── banner/            # Componente para exibição de banners ASCII
├── docker/                # Configurações para contêinerização com Docker
├── docs/                  # Documentação do projeto
├── output/                # Diretório para arquivos de saída (padrão)
├── strx                   # Script principal de execução
├── utils/                 # Módulos e utilitários
│   ├── auxiliary/         # Módulos auxiliares por categoria
│   └── helper/            # Funções auxiliares genéricas
├── .gitignore             # Padrões de arquivos a serem ignorados pelo git
├── LICENSE                # Licença do projeto
├── MANIFEST.in            # Instruções para inclusão de arquivos no pacote
├── README.md              # Documentação principal do projeto
├── pyproject.toml         # Configuração de build do projeto
├── requirements.txt       # Dependências do projeto
└── setup.cfg              # Configuração de instalação do projeto
```

## Componentes Principais

### 1. Script Principal (`strx`)

O ponto de entrada da aplicação é o script `strx`, que gerencia o processamento de argumentos da linha de comando e inicia o fluxo de execução do programa.

### 2. Core (`/core`)

O diretório `core/` contém os componentes fundamentais do String-X:

- **`__init__.py`**: Inicialização do módulo core
- **`auto_module.py`**: Sistema de carregamento automático de módulos
- **`basemodule.py`**: Classes base para todos os tipos de módulos
- **`command.py`**: Gerenciador de execução de comandos
- **`filelocal.py`**: Manipulação de arquivos locais
- **`format.py`**: Formatadores genéricos
- **`func_format.py`**: Funções de formatação específicas
- **`help_modules.py`**: Sistema de ajuda e documentação
- **`http_async.py`**: Cliente HTTP assíncrono para requisições paralelas
- **`logger.py`**: Sistema de logging
- **`output_formatter.py`**: Formatadores de saída (TXT, CSV, JSON, etc.)
- **`randomvalue.py`**: Gerador de valores aleatórios
- **`retry.py`**: Sistema de retry para operações que podem falhar
- **`style_cli.py`**: Estilização da interface de linha de comando
- **`thread_process.py`**: Gerenciador de threads e processamento paralelo
- **`upgrade_manager.py`**: Sistema de atualização automática
- **`user_agent_generator.py`**: Gerador de User-Agents
- **`validators.py`**: Validadores de dados e tipos

#### Banner (`/core/banner`)

- **`__init__.py`**: Inicialização do módulo de banner
- **`asciiart.py`**: Gerenciador de arte ASCII
- **`asciiart/`**: Diretório com arquivos de arte ASCII

### 3. Config (`/config`)

Armazena arquivos de configuração:

- **`__init__.py`**: Inicialização do módulo de configuração
- **`google_cse_id.txt`**: ID para o Google Custom Search Engine
- **`setting.py`**: Configurações gerais da aplicação

### 4. Utils (`/utils`)

Os utilitários são organizados em duas categorias principais:

#### Auxiliary (`/utils/auxiliary`)

Contém módulos auxiliares categorizados:

- **`__init__.py`**: Inicialização do módulo de auxiliares
- **`ai/`**: Módulos de Inteligência Artificial
  - **`gemini.py`**: Integração com Gemini AI
  - **`openai.py`**: Integração com OpenAI
- **`clc/`**: Módulos Coletores (Collectors)
  - **`archive.py`**: Coleta de dados de arquivos web
  - **`bing.py`**: Integração com Bing Search
  - **`crtsh.py`**: Integração com crt.sh
  - **`dns.py`**: Resolução e consulta DNS
  - **`duckduckgo.py`**: Integração com DuckDuckGo
  - **`emailverify.py`**: Verificação de emails
  - **`ezilon.py`**: Integração com Ezilon
  - **`geoip.py`**: Geolocalização de IPs
  - **`google.py`**: Integração com Google Search
  - **`googlecse.py`**: Integração com Google Custom Search
  - **`ipinfo.py`**: Informações detalhadas sobre IPs
  - **`lycos.py`**: Integração com Lycos Search
  - **`naver.py`**: Integração com Naver Search
  - **`netscan.py`**: Scanner de rede básico
  - **`shodan.py`**: Integração com Shodan
  - **`sogou.py`**: Integração com Sogou Search
  - **`subdomain.py`**: Enumeração de subdomínios
  - **`virustotal.py`**: Integração com VirusTotal
  - **`whois.py`**: Consulta WHOIS
  - **`yahoo.py`**: Integração com Yahoo Search
- **`con/`**: Módulos de Conexão (Connectors)
  - **`ftp.py`**: Cliente FTP
  - **`http_probe.py`**: Verificador de serviços HTTP
  - **`ssh.py`**: Cliente SSH
- **`ext/`**: Módulos Extratores (Extractors)
  - **`credential.py`**: Extração de credenciais
  - **`cryptocurrency.py`**: Extração de endereços de criptomoedas
  - **`documents.py`**: Extração de metadados de documentos
  - **`domain.py`**: Extração de domínios
  - **`email.py`**: Extração de endereços de email
  - **`hash.py`**: Extração de hashes
  - **`ip.py`**: Extração de endereços IP
  - **`mac.py`**: Extração de endereços MAC
  - **`phone.py`**: Extração de números de telefone
  - **`url.py`**: Extração de URLs

#### Helper (`/utils/helper`)

- **`__init__.py`**: Inicialização do módulo de helpers
- **`functions.py`**: Funções auxiliares genéricas

### 5. Docker (`/docker`)

Contém configurações para diferentes setups Docker:

- **`opensearch-docker-compose/`**: Configuração Docker para OpenSearch
  - **`Dockerfile`**: Definição da imagem Docker
- **`strx-docker-compose/`**: Configuração Docker para String-X
  - **`Dockerfile`**: Definição da imagem Docker

### 6. Docs (`/docs`)

Documentação organizada do projeto:

- **`usabilidade/`**: Documentação de uso
- **`dev/`**: Documentação para desenvolvedores
- **`tunning/`**: Documentação de otimização e ajuste fino

### 7. Arquivos de Configuração do Projeto

- **`pyproject.toml`**: Configuração do sistema de build do projeto
- **`setup.cfg`**: Configuração para instalação via setuptools
- **`MANIFEST.in`**: Lista de arquivos a serem incluídos no pacote
- **`requirements.txt`**: Dependências do projeto

## Fluxo de Arquivos

Durante a execução do String-X, o fluxo de dados geralmente segue este caminho:

1. O script principal `strx` é invocado com argumentos
2. Os argumentos são processados pelo sistema em `core/`
3. As entradas são lidas (de arquivos, stdin ou diretamente)
4. Os módulos apropriados são carregados de `utils/auxiliary/`
5. O processamento é executado (com possível multithreading via `core/thread_process.py`)
6. Os resultados são formatados usando `core/output_formatter.py`
7. A saída é exibida ou salva em arquivo (geralmente em `output/`)

## Convenções de Código

O String-X segue algumas convenções específicas:

- **Módulos**: Todos os módulos do mesmo tipo compartilham uma interface comum
- **Naming**: Módulos são nomeados com snake_case, classes com PascalCase
- **Documentação**: Funções e classes têm docstrings descritivas
- **Imports**: Imports são organizados em grupos (stdlib, third-party, local)
- **Base Classes**: Todos os módulos estendem classes base apropriadas

## Extensão e Criação de Novos Módulos

Para criar um novo módulo, deve-se:

1. Identificar o tipo adequado (EXT, CLC, CON, etc.)
2. Criar um arquivo no diretório correspondente em `utils/auxiliary/`
3. Implementar a classe principal estendendo a classe base apropriada
4. Adicionar métodos obrigatórios de acordo com o tipo de módulo
5. Registrar o módulo no sistema (geralmente automático)

Para mais detalhes sobre como criar módulos, consulte o documento [Criação de Módulos](criacao-modulos.md).
