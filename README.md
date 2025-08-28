<center>

<h1 align="center">
  <a href="#/"><img src="./asset/img/logo.png"></a>
</h1>

<h4 align="center">Ferramenta de Automatização para Manipulação de Strings</h4>

<p align="center">
String-X (strx) é uma ferramenta modular de automatização desenvolvida para profissionais de Infosec e entusiastas de Hacking. Especializada na manipulação dinâmica de strings em ambiente Linux. 

Com arquitetura modular, oferece recursos avançados para OSINT, pentest e análise de dados, incluindo processamento paralelo, módulos especializados de extração, coleta e integração com APIs externas. Sistema baseado em templates flexíveis com mais de 25 funções integradas.
</p>

<p align="center">
  <a href="#/"><img src="https://img.shields.io/badge/python-3.12+-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/version-1.0.0-green.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/Supported_OS-Linux-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/Supported_OS-Mac-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
</p>

<p align="center">
  <a href="https://github.com/MrCl0wnLab/string-x/blob/main/LICENSE"><img src="https://img.shields.io/github/license/MrCl0wnLab/string-x?color=blue"></a>
  <a href="https://github.com/MrCl0wnLab/string-x/graphs/contributors"><img src="https://img.shields.io/github/contributors-anon/MrCl0wnLab/string-x"></a>
  <a href="https://github.com/MrCl0wnLab/string-x/issues"><img src="https://img.shields.io/github/issues-raw/MrCl0wnLab/string-x"></a>
  <a href="https://github.com/MrCl0wnLab/string-x/network/members"><img src="https://img.shields.io/github/forks/MrCl0wnLab/string-x"></a>
  <img src="https://img.shields.io/github/stars/MrCl0wnLab/string-x.svg?style=social" title="Stars" /> 
</p>

</center>

## 📋 Índice

- [Características](#-características)
- [Instalação](#-instalação)
- [Conceitos Fundamentais](#-conceitos-fundamentais)
- [Arquitetura Modular](#-arquitetura-modular)
- [Uso da Ferramenta](#-uso-da-ferramenta)
- [Exemplos Práticos](#-exemplos-práticos)
- [Funções Integradas](#-funções-integradas)
- [Sistema de Módulos](#-sistema-de-módulos)
- [Contribuição](#-contribuição)
- [Autor](#-autor)

## ✨ CARACTERÍSTICAS

- 🚀 **Processamento Paralelo**: Sistema multi-threading configurável para execução de alta performance
- 🧩 **Arquitetura Modular**: Estrutura extensível com módulos especializados (EXT, CLC, OUT, CON, AI)
- 🔗 **Encadeamento de Módulos**: Processamento sequencial com múltiplos módulos usando pipe (`|`)
- 🔄 **Template Dinâmico**: Sistema de substituição com placeholder `{STRING}` para manipulação flexível
- 🛠️ **+25 Funções Integradas**: Hash, encoding, requests, validação e geração de valores aleatórios
- 📁 **Múltiplas Fontes**: Suporte para strings únicas (`-s`), arquivos (`-l`), stdin e encadeamento de pipes
- 🎯 **Filtragem Inteligente**: Sistema de filtros para processamento seletivo de strings
- 💾 **Saída Flexível**: Formatação em TXT, CSV e JSON com timestamp automático
- 🔌 **Integrações Externas**: APIs, bancos de dados e serviços de notificação
- 🔍 **Extração Avançada**: Padrões complexos com regex e processamento especializado
- 🔒 **OSINT e Pentest**: Recursos otimizados para reconhecimento e análise de segurança
- 🌐 **Dorking Multi-Engine**: Integração com Google, Bing, Yahoo, DuckDuckGo e outros
- 🧠 **Integração com IA**: Módulo para processamento com Google Gemini
- 🐋 **Suporte Docker**: Execução containerizada para ambientes isolados
- 🛡️ **Validações de Segurança**: Sistema de proteção contra comando malicioso com opção de bypass

## 📦 INSTALAÇÃO

### Requisitos
- Python 3.12+
- Linux/MacOS
- Dependências definidas em `pyproject.toml`

### Instalação via pip (Recomendado)
```bash
# Instalar diretamente do repositório
pip install git+https://github.com/MrCl0wnLab/string-x.git

# Ou instalar em modo desenvolvimento
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x
pip install -e .

# Teste a instalação
strx -help

# Lista tipos de módulos 
strx -types

# Lista módulos e exemplos de uso
strx -examples

# Lista funções
strx -funcs

# Testando com string única
strx -s "exemplo.com" -st "dig {STRING}"
```

## Arquitetura

```mermaid
graph TD
  IN[Entrada]
  CORE[Core Núcleo]
  HELPERS[Helpers e Funções]
  CONFIG[Configuração]
  LOGS[Logs e Saída]
  MODS[Módulos string-x/utils/auxiliary/]
  EXT[ext: Extractor]
  CLC[clc: Collector]
  OUT[out: Output]
  CON[con: Connection]
  AI[ai: Inteligência Artificial]

  IN --> CORE
  CORE --> HELPERS
  CORE --> CONFIG
  CORE --> LOGS
  CORE --> MODS

  MODS --> EXT
  MODS --> CLC
  MODS --> OUT
  MODS --> CON
  MODS --> AI

  HELPERS --> FUNC_HELPER[Funções: hash, encoding, validação]
  LOGS --> FUNC_LOGS[Saída: txt, csv, json, db, api]
  EXT --> FUNC_EXT[Regex: email, domínio, url, ip]
  CLC --> FUNC_CLC[APIs, DNS, Whois, dorking]
  OUT --> FUNC_OUT[JSON, CSV, XML]
  CON --> FUNC_CON[DB, S3, SSH, FTP, Telegram]
  AI --> FUNC_AI[Gemini IA]

  classDef entrada fill:#f9f,stroke:#333,stroke-width:1px,color:#000
  classDef core fill:#ffe,stroke:#333,stroke-width:1px,color:#000
  classDef modulos fill:#cef,stroke:#333,stroke-width:1px,color:#000
  classDef suporte fill:#afa,stroke:#333,stroke-width:1px,color:#000
  classDef funcs fill:#fcf8e3,stroke:#333,stroke-width:1px,color:#000
  classDef logs fill:#ffd,stroke:#333,stroke-width:1px,color:#000

  class IN entrada
  class CORE core
  class MODS,EXT,CLC,OUT,CON,AI modulos
  class HELPERS,CONFIG suporte
  class FUNC_EXT,FUNC_CLC,FUNC_OUT,FUNC_CON,FUNC_AI,FUNC_HELPER funcs
  class LOGS,FUNC_LOGS logs

```

# Usando encadeamento de módulos
### Encadeamento de Módulos

O String-X suporta o encadeamento de múltiplos módulos usando o caractere pipe (`|`):

```bash
strx -l urls.txt -st "echo {STRING}" -module "ext:url|ext:domain|clc:dns" -pm
```

Neste exemplo:
1. Primeiro extrai URLs do texto
2. Em seguida, extrai domínios dessas URLs
3. Por fim, coleta informações DNS desses domínios

#### Usando o comando -pmc (Print Module Chain)

O parâmetro `-pmc` permite visualizar os resultados de cada módulo na cadeia separadamente, processando cada módulo com os dados de entrada originais, em vez de passar resultados entre módulos:

```bash
strx -l urls.txt -st "echo {STRING}" -module "ext:url|ext:domain|clc:dns" -pmc -pm

strx -l dorks.txt -st "echo {STRING}" -module "clc:google|clc:yahoo|clc:bing" -pmc -pm
```

Com `-pmc` ativado:
- Cada módulo processa os dados de entrada originais (não os resultados do módulo anterior)
- Os resultados de cada módulo são impressos separadamente
- Cada módulo é identificado com um cabeçalho claro (`[Módulo 1/3: ext:url]`)
- Cada resultado é exibido em sua própria linha, evitando concatenações

Este parâmetro é especialmente útil para:
- Processar os dados originais com múltiplos módulos independentemente
- Obter resultados de análise paralela sem encadeamento
- Comparar os resultados de diferentes módulos para o mesmo conjunto de dados
- Evitar que erros em um módulo interrompam a execução da cadeia completa

#### Exemplo prático com -pmc

```bash
# Coletar informações completas de domínios com visualização de cada etapa
strx -s "exemplo.com" -st "echo {STRING}" -module "ext:domain|clc:whois|clc:dns|clc:crtsh" -pmc

# Combinar com verbose para debug completo
strx -l targets.txt -st "echo {STRING}" -module "ext:url|ext:domain|clc:subdomain" -pmc -v all

# Análise de dorking com resultados intermediários
strx -l dorks.txt -st "echo {STRING}" -module "clc:google|ext:domain|clc:dns" -pmc
```

### Criando link simbólico (opcional) 
```bash
# Verificar o link atual
ls -la /usr/local/bin/strx

# Se necessário, recriar o link
sudo rm /usr/local/bin/strx
sudo ln -sf $HOME/Documentos/string-strx /usr/local/bin/strx
```

## ⏫ Sistema de Upgrade com Git
usa comandos git para baixar novas versões
```bash
# Atualizar String-X
strx -upgrade
```

## 🐋 DOCKER
O String-X está disponível como imagem Docker, permitindo execução em ambientes isolados sem necessidade de instalação local de dependências.

### Construindo a Imagem

```bash
# Construa a imagem Docker
docker build -t string-x .
```

### Uso Básico com Docker

```bash
# Executar com comando padrão (mostra exemplos)
docker run --rm string-x

# Visualizar ajuda
docker run --rm string-x -h

# Listar funções disponíveis
docker run --rm string-x -funcs

# Listar tipos de módulos
docker run --rm string-x -types
```

### Processamento de Arquivos Locais

Para processar arquivos do host, monte o diretório como volume:

```bash
# Montar diretório atual e processar arquivo
docker run --rm -v $(pwd):/dados string-x -l /dados/urls.txt -st "curl -I {STRING}"

# Processar com múltiplas threads
docker run --rm -v $(pwd):/dados string-x -l /dados/hosts.txt -st "nmap -p 80,443 {STRING}" -t 20

# Salvar resultados no host
docker run --rm -v $(pwd):/dados string-x -l /dados/domains.txt -st "dig +short {STRING}" -o /dados/results.txt
```

### Uso com Módulos

```bash
# Extrair emails de arquivo
docker run --rm -v $(pwd):/dados string-x -l /dados/dump.txt -st "echo {STRING}" -module "ext:email" -pm

# Dorking com Google
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Coletar informações DNS
docker run --rm -v $(pwd):/dados string-x -l /dados/domains.txt -st "echo {STRING}" -module "clc:dns" -pm
```

### Processamento via Pipe

```bash
# Pipe de comandos do host
echo "github.com" | docker run --rm -i string-x -st "whois {STRING}"

# Combinação com ferramentas do host
cat urls.txt | docker run --rm -i string-x -st "curl -skL {STRING}" -p "grep '<title>'"

# Pipeline complexo
cat domains.txt | docker run --rm -i string-x -st "echo {STRING}" -module "clc:crtsh" -pm | sort -u
```

### Configurações Avançadas

```bash
# Usar proxy dentro do container
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "http://172.17.0.1:8080" -pm

# Definir formato de saída
docker run --rm -v $(pwd):/dados string-x -l /dados/targets.txt -st "echo {STRING}" -format json -o /dados/output.json

# Executar com delay entre threads
docker run --rm -v $(pwd):/dados string-x -l /dados/apis.txt -st "curl {STRING}" -t 10 -sleep 2
```


## 🧠 CONCEITOS FUNDAMENTAIS

### Sistema de Template {STRING}
A ferramenta utiliza o placeholder `{STRING}` como palavra-chave para substituição dinâmica de valores. Este sistema permite que cada linha de entrada seja processada individualmente, substituindo `{STRING}` pelo valor atual.

```bash
# Arquivo de entrada
host-01.com.br
host-02.com.br
host-03.com.br

# Comando com template
strx -l hosts.txt -st "host '{STRING}'"

# Resultado gerado
host 'host-01.com.br'
host 'host-02.com.br'
host 'host-03.com.br'
```

### Fluxo de Processamento
1. **Entrada**: Dados via arquivo (`-l`) ou stdin (pipe)
2. **Template**: Aplicação do template com `{STRING}`
3. **Processamento**: Execução de comandos/módulos
4. **Pipe**: Processamento adicional opcional (`-p`)
5. **Saída**: Resultado final (tela ou arquivo)

<center>

![Screenshot](/asset/img/fluxo.jpg)

</center>

## 🏗️ ARQUITETURA MODULAR

String-X utiliza uma arquitetura modular extensível com quatro tipos principais de módulos:

### Tipos de Módulos

| Tipo | Código | Descrição | Localização |
|------|--------|-----------|-------------|
| **Extractor** | `ext` | Extração de dados específicos (email, URL, domain, phone) | `utils/auxiliary/ext/` |
| **Collector** | `clc` | Coleta e agregação de informações (DNS, whois) | `utils/auxiliary/clc/` |
| **Output** | `out` | Formatação e envio de resultados (DB, API, files) | `utils/auxiliary/out/` |
| **Connection** | `con` | Conexões especializadas (SSH, FTP, etc) | `utils/auxiliary/con/` |

### Estrutura de Diretórios
```bash
string-x/
      .
      ├── asset             # Imagens, banners e logos usados na documentação e interface CLI
      ├── config            # Arquivos de configuração global do projeto (settings, variáveis)
      ├── core              # Núcleo da aplicação, engine principal e lógica central
      │   └── banner        # Submódulo para banners ASCII art
      │       └── asciiart  # Arquivos de arte ASCII para exibição no terminal
      ├── output            # Diretório padrão para arquivos de saída e logs gerados pela ferramenta
      └── utils             # Utilitários e módulos auxiliares para extensões e integrações
          ├── auxiliary     # Módulos auxiliares organizados por função
          │   ├── ai        # Módulos de inteligência artificial (ex: prompts Gemini)
          │   ├── clc       # Módulos coletores (busca, DNS, whois, APIs externas)
          │   ├── con       # Módulos de conexão (SSH, FTP, HTTP probe)
          │   ├── ext       # Módulos extratores (regex: email, domínio, IP, hash, etc)
          │   └── out       # Módulos de saída/integradores (JSON, CSV, banco de dados, APIs)
          └── helper        # Funções utilitárias e helpers usados em todo o projeto
```

## 🚀 USO DA FERRAMENTA

### Ajuda e Parâmetros
```bash
strx -help
```

### Parâmetros Principais

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-h, -help`         | Mostrar help do projeto | `-h` |
| `-types`             | Lista tipos de módulos | `-types` |
| `-examples`          | Lista módulos e exemplos de uso | `-examples` |
| `-functions, -funcs` | Lista funções | `-funcs` |
| `-l, -list` | Arquivo com strings para processamento | `-l hosts.txt` |
| `-st, --str` | Template de comando com `{STRING}` | `-st "curl {STRING}"` |
| `-o, --out` | Arquivo de saída para resultados | `-o results.txt` |
| `-p, -pipe` | Comando adicional via pipe | `-p "grep 200"` |
| `-v, -verbose` | Modo verboso com níveis (1-5 ou 'all'). 1=info, 2=warning, 3=debug, 4=error, 5=exception | `-v 3` |
| `-ds, -disable-security` | Desabilitar validações de segurança (usar com cuidado) | `-ds` |
| `-ns, -no-shell` | Processar entrada diretamente através de módulos/funções sem execução de comandos shell | `-ns` |
| `-t, -thread` | Número de threads paralelas | `-t 50` |
| `-f, --filter` | Filtro para seleção de strings | `-f ".gov.br"` |
| `-iff` | Filtro para resultados de funções: retorna apenas resultados que contenham o valor especificado | `-iff "admin"` |
| `-ifm` | Filtro para resultados de módulos: retorna apenas resultados que contenham o valor especificado | `-ifm "hash"` |
| `-module` | Seleção de módulo específico | `-module "ext:email"` |
| `-pm` | Mostrar apenas resultados do módulo | `-pm` |
| `-pmc` | Mostrar resultados de cada módulo em uma cadeia separadamente | `-pmc` |
| `-pf` | Mostrar apenas resultados de funções | `-pf` |
| `-of` | Salvar resultados de funções em arquivo | `-of` |
| `-sleep` | Delay entre threads (segundos) | `-sleep 2` |
| `-proxy` | Setar proxy para requests | `-proxy "http://127.0.0.1:8080"` |
| `-format` | Formato de saída (txt, csv, json) | `-format json` |
| `-upgrade` | Atualizar String-X via Git | `-upgrade` |
| `-r, -retry` | Quantidade de tentativas | `-r 3` |

### Interface da Aplicação

```bash
usage: strx [-h] [-types] [-examples] [-functions] [-list file] [-s string] [-str cmd]
            [-out file] [-pipe cmd] [-verbose] [-thread <10>] [-pf] [-of]
            [-filter value] [-sleep <5>] [-module <type:module>] [-pm] [-proxy PROXY]
            [-format <format>] [-upgrade] [-retry <1>] [-no-shell]

 
                                             _
                                            (T)          _
                                        _         .=.   (R)
                                       (S)   _   /\/(`)_         ▓
                                        ▒   /\/`\/ |\ 0`\      ░
                                        b   |░-.\_|_/.-||
                                        r   )/ |_____| \(    _
                            █               0  #/\ /\#  ░   (X)
                             ░                _| + o |_                ░
                             b         _     ((|, ^ ,|))               b
                             r        (1)     `||\_/||`                r  
                                               || _ ||      _
                                ▓              | \_/ ░     (V)
                                b          0.__.\   /.__.0   ░
                                r           `._  `"`  _.'           ▒
                                               ) ;  \ (             b
                                        ░    1'-' )/`'-1            r
                                                 0`     
                        
                              ██████    ▄▄▄█████▓    ██▀███     ▒██   ██▒ 
                            ▒██    ▒    ▓  ██▒ ▓▒   ▓██ ▒ ██▒   ░▒ █ █ ▒░
                            ░ ▓██▄      ▒ ▓██░ ▒░   ▓██ ░▄█ ▒   ░░  █   ░
                              ▒   ██▒   ░ ▓██▓ ░    ▒██▀▀█▄      ░ █ █ ▒ 
                            ▒██████▒▒     ▒██▒ ░    ░██▓ ▒██▒   ▒██▒ ▒██▒
                            ▒ ▒▓▒ ▒ ░     ▒ ░░      ░ ▒▓ ░▒▓░   ▒▒ ░ ░▓ ░
                            ░ ░▒  ░ ░       ░         ░▒ ░ ▒░   ░░   ░▒ ░
                            ░  ░  ░       ░           ░░   ░     ░    ░  
                                  ░                    ░         ░    ░  
                                  ░                                      
                                
                              String-X: Tool for automating commands  1.0

options:
             -h, -help             show this help message and exit
             -types                 Lista tipos de módulos
             -examples              Lista módulos e exemplos de uso
             -functions, -funcs     Lista funções
             -list, -l file         Arquivo com strings para execução
             -s string              String única para execução
             -str, -st cmd          String template de comando
             -out, -o file          Arquivo output de valores da execução shell
             -pipe, -p cmd          Comando que será executado depois de um pipe |
             -verbose, -v           Modo verboso
             -thread, -t <10>       Quantidade de threads
             -pf                    Mostrar resultados da execução de função, ignora shell
             -of                    Habilitar output de valores da execução de função
             -filter, -f value      Valor para filtrar strings para execução
             -iff value             Filtrar resultados de função: retorna apenas resultados que contenham o valor especificado
             -ifm value             Filtrar resultados de módulo: retorna apenas resultados que contenham o valor especificado
             -sleep <5>             Segundos de delay entre threads
             -module <type:module>  Selecionar o tipo e module, possível usar encadeamento type1:module1|type:module2
             -pm                    Mostrar somente resultados de execução do module
             -pmc                   Mostrar resultados de cada módulo no encadeamento separadamente
             -no-shell, -ns         Processar entrada diretamente através de módulos/funções sem execução de comandos shell
             -proxy PROXY           Setar um proxy para request
             -format <format>       Formato de saída (txt, csv, json)
             -upgrade               Atualizar String-X via Git
             -retry, -r <1>         Quantidade de tentativas

```

## 💡 EXEMPLOS PRÁTICOS

### Níveis de Verbose
String-X oferece 5 níveis de verbosidade para controle detalhado da saída:

```bash
# Nível 1 (info) - Informações básicas
strx -l domains.txt -st "dig {STRING}" -v 1

# Nível 2 (warning) - Avisos e alertas
strx -l urls.txt -st "curl {STRING}" -v 2

# Nível 3 (debug) - Informações de depuração detalhadas
strx -l targets.txt -st "nmap {STRING}" -v 3

# Nível 4 (error) - Erros de execução
strx -l data.txt -st "process {STRING}" -v 4

# Nível 5 (exception) - Exceções com stack trace
strx -l complex.txt -st "analyze {STRING}" -v 5

# Todos os níveis - Saída máxima de informações
strx -l hosts.txt -st "scan {STRING}" -v all

# Combinar múltiplos níveis
strx -l mixed.txt -st "test {STRING}" -v "1,3,4"
```

### Modo No-Shell (-ns / --no-shell)

O String-X introduz a flag **-no-shell** que permite processamento direto de entrada através de módulos e funções, **sem execução de comandos shell**. Isso melhora segurança, performance e usabilidade.

#### Benefícios:
- **🔒 Segurança Aprimorada**: Elimina riscos de injeção shell
- **⚡ Performance Superior**: Remove overhead de subprocessos
- **💡 Sintaxe Simplificada**: Elimina necessidade de comandos wrapper como `echo {STRING}`

#### Comparação de Abordagens:

```bash
# Abordagem Tradicional
echo "https://example.com" | strx -st "echo {STRING}" -module "ext:url" -pm

# Nova Abordagem (No-Shell)
echo "https://example.com" | strx -st "{STRING}" -module "ext:url" -ns -pm
```

#### Exemplos com Módulos:
```bash
# Extração de URLs direta
curl 'https://blog.inurl.com.br' | strx -st "{STRING}" -module 'ext:url' -ns -pm

# Encadeamento de módulos sem shell
strx -l domains.txt -st "{STRING}" -module "ext:url|ext:domain|clc:dns" -ns -pm

# Processamento de dataset grande com melhor performance
strx -l huge_dataset.txt -st "{STRING}" -module "ext:email" -ns -pm -t 50
```

#### Exemplos com Funções:
```bash
# Funções diretamente aplicadas
echo 'https://example.com/path' | strx -st "extract_domain({STRING})" -ns -pf

# Múltiplas funções
strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -ns -pf
```

### Exemplos Básicos

#### 1. Verificação de Hosts
```bash
# Via arquivo
strx -l hosts.txt -st "host {STRING}" -v

# Via pipe
cat hosts.txt | strx -st "host {STRING}" -v
```

#### 2. Requisições HTTP com Análise
```bash
# Verificar status de URLs
strx -l urls.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 20

# Extrair títulos de páginas
strx -l domains.txt -st "curl -sL https://{STRING}" -p "grep -o '<title>.*</title>'" -o titles.txt
```

#### 3. Análise de Logs e Dados
```bash
# Buscar CPFs em leaks
strx -l cpfs.txt -st "grep -Ei '{STRING}' -R ./database/" -v

# Processar dump SQL
strx -l dump.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u
```

### Exemplos Avançados

#### 1. OSINT e Reconhecimento
```bash
# Informações de IP
cat ips.txt | strx -st "curl -s 'https://ipinfo.io/{STRING}/json'" -p "jq -r '.org, .country'"

# Verificação de phishing
strx -l suspicious.txt -st "curl -skL https://{STRING}/" -p "grep -i 'phish\|scam\|fake'" -t 30

# DNS enumeration
strx -l subdomains.txt -st "dig +short {STRING}" -module "clc:dns" -pm
```

#### 2. Segurança e Pentest
```bash
# Port scanning com nmap
strx -l targets.txt -st "nmap -p 80,443 {STRING}" -p "grep 'open'" -t 10

# SQL injection testing
strx -l urls.txt -st "sqlmap -u '{STRING}' --batch" -p "grep 'vulnerable'" -o sqli_results.txt

# Directory bruteforce
strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

#### 3. Processamento de Dados
```bash
# Extração de emails de múltiplos arquivos
strx -l files.txt -st "cat {STRING}" -module "ext:email" -pm > all_emails.txt

# Conversão de encoding
strx -l base64_data.txt -st "debase64({STRING})" -pf -of

# Geração de hashes
strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -pf -o hashes.txt

# Uso de formatação json
echo 'com.br' | strx  -st "echo {STRING}" -o bing.json -format json -module 'clc:bing' -pm -v
```

### Combinação com Pipes do Sistema
```bash
# Pipeline complexo com jq
curl -s 'https://api.github.com/users' | jq -r '.[].login' | strx -st "curl -s 'https://api.github.com/users/{STRING}'" -p "jq -r '.name, .location'"

# Processamento de logs do Apache
cat access.log | awk '{print $1}' | sort -u | strx -st "whois {STRING}" -p "grep -i 'country'" -t 5

# Análise de certificados SSL
strx -l domains.txt -st "echo | openssl s_client -connect {STRING}:443 2>/dev/null" -p "openssl x509 -noout -subject"
```

### Dorking e Mecanismos de Busca
```bash
# Dorking básico no Google
strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Busca de arquivos PDF em sites governamentais
echo 'site:gov filetype:pdf "confidential"' | strx -st "echo {STRING}" -module "clc:googlecse" -pm

# Encontrando painéis de administração expostos
echo 'inurl:admin intitle:"login"' | strx -st "echo {STRING}" -module "clc:yahoo" -pm

# Múltiplos motores de busca com a mesma dork
echo 'intext:"internal use only"' | strx -st "echo {STRING}" -module "clc:duckduckgo" -pm > duckduckgo_results.txt
echo 'intext:"internal use only"' | strx -st "echo {STRING}" -module "clc:bing" -pm > bing_results.txt

# Comparação de resultados entre motores
cat dorks.txt | strx -st "echo {STRING}" -module "clc:google" -pm | sort > google_results.txt
cat dorks.txt | strx -st "echo {STRING}" -module "clc:bing" -pm | sort > bing_results.txt
comm -23 google_results.txt bing_results.txt > google_exclusive.txt
```

### Dorking com Proxy
```bash
# Utilizando proxy com dorking para evitar bloqueios
strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "http://127.0.0.1:9050" -pm

# Utilizando proxy com autenticação
cat dorks.txt | strx -st "echo {STRING}" -module "clc:yahoo" -proxy "http://user:pass@server:8080" -pm

# Aplicando dorking com TOR
strx -l sensitive_dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "https://127.0.0.1:9050" -pm -t 1 -sleep 5

# Dorking com output estruturado + proxy com autenticação
strx -l sqli_dorks.txt -st "echo {STRING}" -module "clc:googlecse" -proxy "http://user:pass@10.0.0.1:8080" -pm -module "out:json" -pm

# Coleta distribuída através de lista de proxies
cat proxy_list.txt | while read proxy; do
  strx -l target_dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "$proxy" -pm -t 3 -sleep 2
done > combined_results.txt
```

## 🔧 FUNÇÕES INTEGRADAS


String-X inclui mais de 25 funções built-in que podem ser utilizadas dentro dos templates `{STRING}` e comandos pipe. Estas funções são processadas antes da execução dos comandos shell e cobrem desde hash, encoding, manipulação de strings, geração de valores aleatórios, análise de dados, validação de documentos, requisições HTTP, manipulação de arquivos e muito mais.

### Sintaxe
```bash
# Função simples
strx -l data.txt -st "funcao({STRING})" -pf

# Múltiplas funções
strx -l data.txt -st "{STRING}; md5({STRING}); base64({STRING})" -pf

# Função com parâmetros
strx -l data.txt -st "str_rand(10); int_rand(5)" -pf
```


### Funções Disponíveis (Principais)

| Função | Descrição | Exemplo |
|--------|-----------|---------|
| `clear` | Remove espaços, tabs e quebras de linha | `clear({STRING})` |
| `base64` / `debase64` | Codifica/decodifica Base64 | `base64({STRING})` |
| `hex` / `dehex` | Codifica/decodifica hexadecimal | `hex({STRING})` |
| `sha1`, `sha256`, `md5` | Gera hash | `sha256({STRING})` |
| `str_rand`, `int_rand` | Gera string/número aleatório | `str_rand(10)` |
| `ip` | Resolve hostname para IP | `ip({STRING})` |
| `replace` | Substitui substring | `replace(http:,https:,{STRING})` |
| `get` | Requisição HTTP GET | `get(https://{STRING})` |
| `urlencode` | Codifica URL | `urlencode({STRING})` |
| `rev` | Inverte string | `rev({STRING})` |
| `timestamp` | Timestamp atual | `timestamp()` |
| `extract_domain` | Extrai domínio de URL | `extract_domain({STRING})` |
| `jwt_decode` | Decodifica JWT (payload) | `jwt_decode({STRING})` |
| `whois_lookup` | Consulta WHOIS | `whois_lookup({STRING})` |
| `cert_info` | Info de certificado SSL | `cert_info({STRING})` |
| `user_agent` | User-Agent aleatório | `user_agent()` |
| `cidr_expand` | Expande faixa CIDR | `cidr_expand(192.168.0.0/30)` |
| `subdomain_gen` | Gera subdomínios comuns | `subdomain_gen({STRING})` |
| `email_validator` | Valida email | `email_validator({STRING})` |
| `hash_file` | Hashes de arquivo | `hash_file(path.txt)` |
| `encode_url_all` | Codifica URL (tudo) | `encode_url_all({STRING})` |
| `phone_format` | Formata telefone BR | `phone_format({STRING})` |
| `password_strength` | Força de senha | `password_strength({STRING})` |
| `social_media_extract` | Extrai handles sociais | `social_media_extract({STRING})` |
| `leak_check_format` | Formata email para leaks | `leak_check_format({STRING})` |
| `cpf_validate` | Valida CPF | `cpf_validate({STRING})` |


> Veja a lista completa e exemplos em `utils/helper/functions.py` ou use `-functions` na CLI para documentação detalhada.

#### Hashing e Encoding
```bash
# Gerar múltiplos hashes
strx -l passwords.txt -st "md5({STRING}); sha1({STRING}); sha256({STRING})" -pf

# Trabalhar com Base64
strx -l data.txt -st "base64({STRING})" -pf
echo "SGVsbG8gV29ybGQ=" | strx -st "debase64({STRING})" -pf
```

#### Geração de Valores Aleatórios
```bash
# Gerar strings aleatórias
strx -l domains.txt -st "https://{STRING}/admin?token=str_rand(32)" -pf

# Gerar números aleatórios
strx -l apis.txt -st "curl '{STRING}?id=int_rand(6)'" -pf
```

#### Requisições e Resolução
```bash
# Resolver IPs
strx -l hosts.txt -st "{STRING}; ip({STRING})" -pf

# Fazer requisições GET
strx -l urls.txt -st "get(https://{STRING})" -pf
```

#### Manipulação de Strings
```bash
# Substituir protocolos
strx -l urls.txt -st "replace(http:,https:,{STRING})" -pf

# Inverter strings
strx -l data.txt -st "rev({STRING})" -pf

# URL encoding
strx -l params.txt -st "urlencode({STRING})" -pf
```

### Parâmetros de Controle

- **`-pf`**: Mostrar apenas resultados das funções (ignora execução shell)
- **`-of`**: Salvar resultados das funções em arquivo de saída

```bash
# Apenas mostrar resultado das funções
strx -l domains.txt -st "{STRING}; md5({STRING})" -pf

# Salvar funções em arquivo
strx -l data.txt -st "base64({STRING})" -pf -of -o encoded.txt
```

### Exemplo de Function
> **💡 Dica**: Você pode adicionar funções personalizadas editando o arquivo `utils/helper/functions.py`
```python
@staticmethod
def check_admin_exemplo(value: str) -> str:
  try:
      if '<p>admin</p>' in value:
        return value
  except:
    return str()
```

### Usando o exemplo de function
```bash
# Executando a function criada
strx -l data.txt -st "check_admin_exemplo({STRING})" -pf
```


## 🧩 SISTEMA DE MÓDULOS

String-X utiliza uma arquitetura modular extensível que permite adicionar funcionalidades específicas sem modificar o código principal. Os módulos são organizados por tipo e carregados dinamicamente.

### Tipos de Módulos Disponíveis

| Tipo | Código | Descrição | Localização |
|------|--------|-----------|-------------|
| **Extractor** | `ext` | Extração de dados específicos usando regex | `utils/auxiliary/ext/` |
| **Collector** | `clc` | Coleta de informações de APIs/serviços | `utils/auxiliary/clc/` |
| **Output** | `out` | Formatação e envio de dados | `utils/auxiliary/out/` |
| **Connection** | `con` | Conexões especializadas | `utils/auxiliary/con/` |
| **AI** | `ai` | Inteligência artificial  | `utils/auxiliary/ai/` |


#### Sintaxe Básica
```bash
strx -module "tipo:nome_do_modulo"
```

#### Parâmetros Relacionados
- **`-module tipo:nome`**: Especifica o módulo a ser utilizado
- **`-pm`**: Mostra apenas resultados do módulo (omite saída shell)


### Módulos Extractor (EXT)
Módulos para extração de padrões e dados específicos usando regex:

| Módulo      | Descrição                                 | Exemplo CLI |
|-------------|-------------------------------------------|-------------|
| `email`     | Extrai endereços de email válidos         | `-module "ext:email"` |
| `domain`    | Extrai domínios e subdomínios             | `-module "ext:domain"` |
| `url`       | Extrai URLs completas (HTTP/HTTPS)         | `-module "ext:url"` |
| `phone`     | Extrai números de telefone (BR)            | `-module "ext:phone"` |
| `credential`| Extrai credenciais, tokens, chaves         | `-module "ext:credential"` |
| `ip`        | Extrai endereços IPv4/IPv6                 | `-module "ext:ip"` |
| `hash`      | Extrai hashes MD5, SHA1, SHA256, SHA512    | `-module "ext:hash"` |

```bash
# Exemplo: Extrair emails de dump de dados
strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm
```


### Módulos Collector (CLC)
Módulos para coleta de informações externas, APIs e análise:

| Módulo        | Descrição                                 | Exemplo CLI |
|---------------|-------------------------------------------|-------------|
| `archive`     | Coleta URLs arquivadas do Wayback Machine | `-module "clc:archive"` |
| `bing`        | Realiza buscas com dorks no Bing          | `-module "clc:bing"` |
| `crtsh`       | Coleta certificados SSL/TLS e subdomínios | `-module "clc:crtsh"` |
| `dns`         | Coleta registros DNS (A, MX, TXT, NS)     | `-module "clc:dns"` |
| `duckduckgo`  | Realiza buscas com dorks no DuckDuckGo    | `-module "clc:duckduckgo"` |
| `emailverify` | Verifica validade de emails (MX, SMTP)    | `-module "clc:emailverify"` |
| `ezilon`      | Realiza buscas com dorks no Ezilon        | `-module "clc:ezilon"` |
| `geoip`       | Geolocalização de IPs                     | `-module "clc:geoip"` |
| `google`      | Realiza buscas com dorks no Google        | `-module "clc:google"` |
| `googlecse`   | Realiza buscas com dorks usando Google CSE| `-module "clc:googlecse"` |
| `http_probe`  | Sondagem HTTP/HTTPS, análise de headers   | `-module "clc:http_probe"` |
| `ipinfo`      | Scanner de portas IP/host                 | `-module "clc:ipinfo"` |
| `lycos`       | Realiza buscas com dorks no Lycos         | `-module "clc:lycos"` |
| `naver`       | Realiza buscas com dorks no Naver (Coreano)| `-module "clc:naver"` |
| `netscan`     | Scanner de rede (hosts, serviços)         | `-module "clc:netscan"` |
| `shodan`      | Consulta API Shodan                       | `-module "clc:shodan"` |
| `sogou`       | Realiza buscas com dorks no Sogou (Chinês)| `-module "clc:sogou"` |
| `spider`      | Web spider para coleta recursiva de URLs  | `-module "clc:spider"` |
| `subdomain`   | Enumeração de subdomínios                 | `-module "clc:subdomain"` |
| `virustotal`  | Consulta API VirusTotal                   | `-module "clc:virustotal"` |
| `whois`       | Consulta WHOIS de domínios                | `-module "clc:whois"` |
| `yahoo`       | Realiza buscas com dorks no Yahoo         | `-module "clc:yahoo"` |

```bash
# Exemplo: Coletar informações DNS
strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm

# Exemplo: Coletar informações usando motores de busca
strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm
strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm
strx -l dorks.txt -st "echo {STRING}" -module "clc:googlecse" -pm
strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm

# Exemplo: Sondar e analisar servidores web
strx -l urls.txt -st "echo {STRING}" -module "clc:http_probe" -pm
strx -l dorks.txt -st "echo {STRING}" -module "clc:duckduckgo" -pm

# Exemplo: Spider para coleta recursiva de URLs
strx -s "https://example.com" -st "echo {STRING}" -module "clc:spider" -pm
strx -s "https://example.com" -st "echo {STRING}" -module "clc:spider" \
     -op depth=3,max_urls=50,delay=0.5 -pm

# Exemplos com dorking específico
echo 'site:fbi.gov filetype:pdf' | strx -st "echo {STRING}" -module "clc:google" -pm
echo 'site:github.com inurl:admin' | strx -st "echo {STRING}" -module "clc:googlecse" -pm
echo 'inurl:admin' | strx -st "echo {STRING}" -module "clc:lycos" -pm
echo 'site:github.com' | strx -st "echo {STRING}" -module "clc:ezilon" -pm
echo 'filetype:pdf' | strx -st "echo {STRING}" -module "clc:yahoo" -pm
```


### Módulos Output (OUT)
Módulos para saída e formatação de resultados:

| Módulo        | Descrição                                 | Exemplo CLI |
|---------------|-------------------------------------------|-------------|
| `json`        | Salva resultados em JSON                  | `-module "out:json"` |
| `csv`         | Salva resultados em CSV                   | `-module "out:csv"` |
| `xml`         | Salva resultados em XML                   | `-module "out:xml"` |

```bash
# Exemplo: Salvar em JSON
strx -l data.txt -st "process {STRING}" -module "out:json" -pm
```

### Módulos de Conexão (CON)
Módulos para conexão com serviços externos e integração de resultados:

| Módulo        | Descrição                                 | Exemplo CLI |
|---------------|-------------------------------------------|-------------|
| `sqlite`      | Salva dados em banco SQLite               | `-module "con:sqlite"` |
| `mysql`       | Salva dados em banco MySQL                | `-module "con:mysql"` |
| `telegram`    | Envia resultados via Telegram Bot         | `-module "con:telegram"` |
| `slack`       | Envia resultados via Slack Webhook        | `-module "con:slack"` |
| `opensearch`  | Indexa resultados em Open Search          | `-module "con:opensearch"` |
| `ftp`         | Conexão e transferência via FTP           | `-module "con:ftp"` |
| `ssh`         | Executa comandos via SSH                  | `-module "con:ssh"` |
| `s3`          | Upload/download de dados no Amazon S3     | `-module "con:s3"` |

```bash
# Exemplo: Salvar em SQLite
strx -l data.txt -st "process {STRING}" -module "con:sqlite" -pm

# Exemplo: Upload para S3
strx -l logs.txt -st "echo {STRING}" -module "con:s3" -pm

# Exemplo: Download do S3
strx -s "path/to/file.txt" -st "echo {STRING}" -module "con:s3" \
     -op operation=download,object_key={STRING} -pm

# Exemplo: Listar objetos no bucket S3
strx -s "bucket-name" -st "echo {STRING}" -module "con:s3" \
     -op operation=list,prefix=logs/ -pm
```


### Módulos Inteligência artificial  (AI)
Módulos para de prompts para Inteligência artificial:

| Módulo        | Descrição                                 | Exemplo CLI |
|---------------|-------------------------------------------|-------------|
| `gemini`      | Prompt para Google Gemini AI - ([Criar API Key](https://aistudio.google.com/app/apikey))    | `-module "ai:gemini"` |

```bash
# Exemplo: Uso de arquivos com Prompts
strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm

# Exemplo: Coletar urls e enviar para analise montando Prompt
strx -l urls.txt -st "echo 'Analisar URL: {STRING}'" -module "ai:gemini" -pm
```

#### Exemplos Práticos
```bash
# Extrair emails e salvar ordenados
strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# Verificar DNS de domínios suspeitos
strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# Pipeline com múltiplos módulos
cat logs.txt | strx -st "echo '{STRING}'" -module "ext:domain" -pm | strx -st "echo {STRING}" -module "clc:dns" -pm

# Extrair URLs e verificar status
strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

### Desenvolvimento de Novos Módulos

Para criar novos módulos, siga a estrutura padrão:

#### Módulo Extractor (ext)
```python
"""
Introdução do módulo
"""
from core.basemodule import BaseModule
import re

class ModuleName(BaseModule):
    
    def __init__(self):
      super().__init__()


      # Define informações de meta do módulo
      self.meta.update({
          "name": "Nome do módulo...",
          "description": "Descreva o módulo...",
          "author": "Nome do criador...",
          "type": "extractor | collector | Output..."
      })

      # Define opções requeridas para este módulo
      self.options = {
          "data":   str(),
          "regex":  str(),
          "proxy":  str()
      }
    
    # Função obrigatoria para execução
    def run(self):
        """
        Contexto para lógico do módulo
          > Acesse as informações de options via: self.options.get(key_name)
        """
        # Savar informações da exeução do módulo
        self.set_result(value_regex)
```

### Filtros e Módulos

Você pode combinar filtros com módulos para processamento mais específico:

```bash
# Extrair apenas emails de domínios .gov
strx -l data.txt -st "echo '{STRING}'" -module "ext:email" -pm -f ".gov"

# DNS lookup apenas para domínios .br
strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm -f ".br"
```

## 🎯 FILTROS E PROCESSAMENTO SELETIVO

O sistema de filtros permite processar apenas strings que atendam critérios específicos, otimizando performance e precisão.

### Uso de Filtros
```bash
strx -f "valor_filtro" / strx --filter "valor_filtro"
```

### Exemplos de Filtros
```bash
# Filtrar apenas domínios .gov.br
strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# Filtrar apenas URLs HTTPS
strx -l urls.txt -st "curl {STRING}" -f "https"

# Filtrar IPs específicos
strx -l logs.txt -st "analyze {STRING}" -f "192.168"

# Filtrar extensões de arquivo
strx -l files.txt -st "process {STRING}" -f ".pdf"

# Filtrar apenas resultados de função que contenham "admin"
strx -l urls.txt -st "{STRING}; md5({STRING})" -pf -iff "admin"

# Filtrar apenas resultados de módulo que contenham hash específico
strx -l domains.txt -st "echo {STRING}" -module "ext:hash" -pm -ifm "a1b2c3"

# Combinar filtros de função e módulo
strx -l data.txt -st "{STRING}; md5({STRING})" -module "ext:domain" -pf -pm -iff "google" -ifm "admin"
```

### Combinação com Módulos
```bash
# Extrair emails e salvar ordenados
strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# Verificar DNS de domínios suspeitos
strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# Pipeline com múltiplos módulos
cat logs.txt | strx -st "echo '{STRING}'" -module "ext:domain" -pm | strx -st "echo {STRING}" -module "clc:dns" -pm

# Extrair URLs e verificar status
strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

## ⚡ PROCESSAMENTO PARALELO

String-X suporta processamento paralelo através de threads para acelerar operações em grandes volumes de dados.

### Configuração de Threads
```bash
# Definir número de threads
strx -t 50 / strx -thread 50

# Definir delay entre threads
strx -sleep 2
```

### Exemplos com Threading
```bash
# Verificação rápida de status HTTP
strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# Resolução DNS em massa
strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1

# Scanning de portas
strx -l ip_list.txt -st "nmap -p 80,443 {STRING}" -t 20 -sleep 3
```

### Boas Práticas para Threading
- **Rate limiting**: Use `-sleep` para evitar sobrecarga de serviços
- **Número adequado**: Ajuste `-t` conforme recursos disponíveis
- **Monitoramento**: Use `-v 1` para info básica, `-v 3` para debug detalhado, `-v all` para máximo controle

### Processamento de Arquivos Grandes
String-X foi otimizado para processar arquivos grandes eficientemente:
```bash
# Processar arquivo grande com múltiplas threads
strx -l large_file.txt -st "echo {STRING}" -module "ext:email" -pm -t 20 -sleep 1

# Para arquivos muito grandes, use menos threads e mais delay
strx -l huge_dataset.txt -st "process {STRING}" -t 10 -sleep 2 -v
```

## 🛡️ SISTEMA DE SEGURANÇA

String-X inclui validações de segurança para prevenir execução de comandos maliciosos:

### Validações Ativas
- **Tamanho de entrada**: Limita dados de entrada a 1MB por padrão
- **Quantidade de strings**: Máximo de 10.000 strings por execução
- **Padrões perigosos**: Detecta e bloqueia comandos potencialmente maliciosos
- **Threads**: Limita threads concorrentes para evitar sobrecarga

### Desabilitando Validações de Segurança
**⚠️ ATENÇÃO**: Use apenas quando necessário e você confiar no conteúdo

```bash
# Desabilitar validações para comandos complexos legítimos
strx -l data.txt -st "echo {STRING}; md5sum {STRING}" -ds

# Processar arquivos grandes sem limitações
strx -l huge_file.txt -st "process {STRING}" -ds -t 50

# Usar com funções que podem gerar padrões detectados como suspeitos
echo "test" | strx -st "echo {STRING}; echo 'result'" -ds
```

### Modo Debug para Segurança
```bash
# Ver detalhes das validações de segurança (debug completo)
strx -l data.txt -st "command {STRING}" -v 3

# Verificar por que um comando foi bloqueado
strx -s "test" -st "suspicious_command" -v 3
```
## 📸 EXEMPLOS VISUAIS

### Execução Básica
**Comando**: `cat hosts.txt | strx -str 'host {STRING}'`

![Screenshot](/asset/img/img1.png)

### Processamento com Threading
**Comando**: `cat hosts.txt | strx -str "curl -Iksw 'CODE:%{response_code};IP:%{remote_ip};HOST:%{url.host};SERVER:%header{server}' https://{STRING}" -p "grep -o -E 'CODE:.(.*)|IP:.(.*)|HOST:.(.*)|SERVER:.(.*)'" -t 30`

![Screenshot](/asset/img/img3.png)

### Modo Verbose
**Comando**: `cat hosts.txt | strx -str 'host {STRING}' -v`

![Screenshot](/asset/img/img2.png)

### Formato de Arquivo de Saída
```
output-%d-%m-%Y-%H.txt > output-15-06-2025-11.txt
```

## 🤝 CONTRIBUIÇÃO

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Tipos de Contribuição
- 🐛 **Bug fixes**
- ✨ **Novas funcionalidades**
- 📝 **Melhoria da documentação**
- 🧩 **Novos módulos**
- ⚡ **Otimizações de performance**

### Desenvolvimento de Módulos
Para criar novos módulos, consulte a seção [Sistema de Módulos](#-sistema-de-módulos) e siga os padrões estabelecidos.

## 📄 LICENÇA

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 AUTOR

**MrCl0wn**
- 🌐 **Blog**: [http://blog.mrcl0wn.com](http://blog.mrcl0wn.com)
- 🐙 **GitHub**: [@MrCl0wnLab](https://github.com/MrCl0wnLab) | [@MrCl0wnLab](https://github.com/MrCl0wnLab)
- 🐦 **Twitter**: [@MrCl0wnLab](https://twitter.com/MrCl0wnLab)
- 📧 **Email**: mrcl0wnlab@gmail.com

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

**💡 Sugestões e feedbacks são sempre bem-vindos!**

**💀 Hacker Hackeia!**

</div>
