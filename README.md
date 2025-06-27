<center>

<h1 align="center">
  <a href="#/"><img src="./asset/logo.png"></a>
</h1>

<h4 align="center">Ferramenta de Automatização para Manipulação de Strings</h4>

<p align="center">
String-X (strx) é uma ferramenta modular de automatização desenvolvida para profissionais de Infosec e entusiastas de Hacking. Especializada na manipulação dinâmica de strings em ambiente Linux. 

Com arquitetura modular, oferece recursos avançados para OSINT, pentest e análise de dados, incluindo processamento paralelo, módulos especializados de extração, coleta e integração com APIs externas. Sistema baseado em templates flexíveis com mais de 25 funções integradas.
</p>

<p align="center">
  <a href="#/"><img src="https://img.shields.io/badge/python-3.12-orange.svg"></a>
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
- 🔄 **Template Dinâmico**: Sistema de substituição com placeholder `{STRING}` para manipulação flexível
- 🛠️ **+25 Funções Integradas**: Operações de hash, encoding, requests, validação e geração de dados
- 📡 **Múltiplas Fontes de Entrada**: Suporte a arquivos, stdin e encadeamento de pipes
- 🎯 **Filtragem Inteligente**: Sistema de filtros para processamento seletivo de strings
- 📊 **Saída Configurável**: Formatação personalizável com timestamp automático e redirecionamento
- 🔌 **Integrações Externas**: Conexões com APIs, bancos de dados e serviços de notificação
- 🔍 **Análise Avançada**: Extração de padrões complexos com regex e processamento especializado
- 🔒 **Ferramentas para Segurança**: Recursos específicos para OSINT, pentest e análise de dados
- 🌐 **Dorking Automatizado**: Integração com múltiplos motores de busca para OSINT
- 🧠 **Integração com IA**: Módulo para processamento com Google Gemini

## 📦 INSTALAÇÃO

### Requisitos
- Python 3.12+
- Linux/MacOS
- Bibliotecas listadas em `requirements.txt`

### Instalação Rápida
```bash
# Clone o repositório
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x

# Instale as dependências
pip install -r requirements.txt

# Torne o arquivo executável
chmod +x strx

# Teste a instalação com help
./strx --help

# Lista tipos de módulos 
./strx -types

# Lista módulos e exemplos de uso
./strx -examples

# Lista funções
./strx -funcs

```

## ⏫ Sistema de Upgrade com Git
usa comandos git para baixar novas versões
```bash
# Atualizar String-X
./strx -upgrade
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
./strx -l hosts.txt -st "host '{STRING}'"

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

![Screenshot](/asset/fluxo.jpg)

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
./strx --help
```

### Parâmetros Principais

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-h, --help`         | Mostrar help do projeto | `-h` |
| `-types`             | Lista tipos de módulos | `-types` |
| `-examples`          | Lista módulos e exemplos de uso | `-examples` |
| `-functions, -funcs` | Lista funções | `-funcs` |
| `-l, --list` | Arquivo com strings para processamento | `-l hosts.txt` |
| `-st, --str` | Template de comando com `{STRING}` | `-st "curl {STRING}"` |
| `-o, --out` | Arquivo de saída para resultados | `-o results.txt` |
| `-p, --pipe` | Comando adicional via pipe | `-p "grep 200"` |
| `-v, --verbose` | Modo verboso com detalhes | `-v` |
| `-t, --thread` | Número de threads paralelas | `-t 50` |
| `-f, --filter` | Filtro para seleção de strings | `-f ".gov.br"` |
| `-module` | Seleção de módulo específico | `-module "ext:email"` |
| `-pm` | Mostrar apenas resultados do módulo | `-pm` |
| `-pf` | Mostrar apenas resultados de funções | `-pf` |
| `-of` | Salvar resultados de funções em arquivo | `-of` |
| `-sleep` | Delay entre threads (segundos) | `-sleep 2` |
| `-proxy` | Setar proxy para requests | `-proxy "http://127.0.0.1:8080"` |
| `-format` | Formato de saída (txt, csv, json) | `-format json` |

### Interface da Aplicação

```bash
usage: strx [-h] [-types] [-examples] [-functions] [-list file] [-str cmd] [-out file] 
            [-pipe cmd] [-verbose] [-thread <10>] [-pf] [-of] [-filter value] [-sleep <5>] 
            [-module <type:module>] [-pm] [-proxy PROXY] [-format <format>]

 
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
                                
                                String-X: Tool for automating commands

options:
             -h, --help             show this help message and exit
             -types                 Lista tipos de módulos
             -examples              Lista módulos e exemplos de uso
             -functions, -funcs     Lista funções
             -list, -l file         Arquivo com strings para execução
             -str, -st cmd          String template de comando
             -out, -o file          Arquivo output de valores da execução shell
             -pipe, -p cmd          Comando que será executado depois de um pipe |
             -verbose, -v           Modo verboso
             -thread, -t <10>       Quantidade de threads
             -pf                    Mostrar resultados da execução de função, ignora shell
             -of                    Habilitar output de valores da execução de função
             -filter, -f value      Valor para filtrar strings para execução
             -sleep <5>             Segundos de delay entre threads
             -module <type:module>  Selectionar o tipo e module
             -pm                    Mostrar somente resultados de execução do module
             -proxy PROXY           Setar um proxy para request
             -format <format>       Formato de saída (txt, csv, json)

```

## 💡 EXEMPLOS PRÁTICOS

### Exemplos Básicos

#### 1. Verificação de Hosts
```bash
# Via arquivo
./strx -l hosts.txt -st "host {STRING}" -v

# Via pipe
cat hosts.txt | ./strx -st "host {STRING}" -v
```

#### 2. Requisições HTTP com Análise
```bash
# Verificar status de URLs
./strx -l urls.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 20

# Extrair títulos de páginas
./strx -l domains.txt -st "curl -sL https://{STRING}" -p "grep -o '<title>.*</title>'" -o titles.txt
```

#### 3. Análise de Logs e Dados
```bash
# Buscar CPFs em leaks
./strx -l cpfs.txt -st "grep -Ei '{STRING}' -R ./database/" -v

# Processar dump SQL
./strx -l dump.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u
```

### Exemplos Avançados

#### 1. OSINT e Reconhecimento
```bash
# Informações de IP
cat ips.txt | ./strx -st "curl -s 'https://ipinfo.io/{STRING}/json'" -p "jq -r '.org, .country'"

# Verificação de phishing
./strx -l suspicious.txt -st "curl -skL https://{STRING}/" -p "grep -i 'phish\|scam\|fake'" -t 30

# DNS enumeration
./strx -l subdomains.txt -st "dig +short {STRING}" -module "clc:dns" -pm
```

#### 2. Segurança e Pentest
```bash
# Port scanning com nmap
./strx -l targets.txt -st "nmap -p 80,443 {STRING}" -p "grep 'open'" -t 10

# SQL injection testing
./strx -l urls.txt -st "sqlmap -u '{STRING}' --batch" -p "grep 'vulnerable'" -o sqli_results.txt

# Directory bruteforce
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

#### 3. Processamento de Dados
```bash
# Extração de emails de múltiplos arquivos
./strx -l files.txt -st "cat {STRING}" -module "ext:email" -pm > all_emails.txt

# Conversão de encoding
./strx -l base64_data.txt -st "debase64({STRING})" -pf -of

# Geração de hashes
./strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -pf -o hashes.txt

# Uso de formatação json
echo 'com.br' | ./strx  -st "echo {STRING}" -o bing.json -format json -module 'clc:bing' -pm -v
```

### Combinação com Pipes do Sistema
```bash
# Pipeline complexo com jq
curl -s 'https://api.github.com/users' | jq -r '.[].login' | ./strx -st "curl -s 'https://api.github.com/users/{STRING}'" -p "jq -r '.name, .location'"

# Processamento de logs do Apache
cat access.log | awk '{print $1}' | sort -u | ./strx -st "whois {STRING}" -p "grep -i 'country'" -t 5

# Análise de certificados SSL
./strx -l domains.txt -st "echo | openssl s_client -connect {STRING}:443 2>/dev/null" -p "openssl x509 -noout -subject"
```

### Dorking e Mecanismos de Busca
```bash
# Dorking básico no Google
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Busca de arquivos PDF em sites governamentais
echo 'site:gov filetype:pdf "confidential"' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm

# Encontrando painéis de administração expostos
echo 'inurl:admin intitle:"login"' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm

# Múltiplos motores de busca com a mesma dork
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:duckduckgo" -pm > duckduckgo_results.txt
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:bing" -pm > bing_results.txt

# Comparação de resultados entre motores
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:google" -pm | sort > google_results.txt
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:bing" -pm | sort > bing_results.txt
comm -23 google_results.txt bing_results.txt > google_exclusive.txt
```

### Dorking com Proxy
```bash
# Utilizando proxy com dorking para evitar bloqueios
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "http://127.0.0.1:9050" -pm

# Utilizando proxy com autenticação
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:yahoo" -proxy "http://user:pass@server:8080" -pm

# Aplicando dorking com TOR
./strx -l sensitive_dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "https://127.0.0.1:9050" -pm -t 1 -sleep 5

# Dorking com output estruturado + proxy com autenticação
./strx -l sqli_dorks.txt -st "echo {STRING}" -module "clc:googlecse" -proxy "http://user:pass@10.0.0.1:8080" -pm -module "out:json_output" -pm

# Coleta distribuída através de lista de proxies
cat proxy_list.txt | while read proxy; do
  ./strx -l target_dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "$proxy" -pm -t 3 -sleep 2
done > combined_results.txt
```

## 🔧 FUNÇÕES INTEGRADAS


String-X inclui mais de 25 funções built-in que podem ser utilizadas dentro dos templates `{STRING}` e comandos pipe. Estas funções são processadas antes da execução dos comandos shell e cobrem desde hash, encoding, manipulação de strings, geração de valores aleatórios, análise de dados, validação de documentos, requisições HTTP, manipulação de arquivos e muito mais.

### Sintaxe
```bash
# Função simples
./strx -l data.txt -st "funcao({STRING})" -pf

# Múltiplas funções
./strx -l data.txt -st "{STRING}; md5({STRING}); base64({STRING})" -pf

# Função com parâmetros
./strx -l data.txt -st "str_rand(10); int_rand(5)" -pf
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


> Veja a lista completa e exemplos em `utils/helper/functions.py` ou use `--functions` na CLI para documentação detalhada.

#### Hashing e Encoding
```bash
# Gerar múltiplos hashes
./strx -l passwords.txt -st "md5({STRING}); sha1({STRING}); sha256({STRING})" -pf

# Trabalhar com Base64
./strx -l data.txt -st "base64({STRING})" -pf
echo "SGVsbG8gV29ybGQ=" | ./strx -st "debase64({STRING})" -pf
```

#### Geração de Valores Aleatórios
```bash
# Gerar strings aleatórias
./strx -l domains.txt -st "https://{STRING}/admin?token=str_rand(32)" -pf

# Gerar números aleatórios
./strx -l apis.txt -st "curl '{STRING}?id=int_rand(6)'" -pf
```

#### Requisições e Resolução
```bash
# Resolver IPs
./strx -l hosts.txt -st "{STRING}; ip({STRING})" -pf

# Fazer requisições GET
./strx -l urls.txt -st "get(https://{STRING})" -pf
```

#### Manipulação de Strings
```bash
# Substituir protocolos
./strx -l urls.txt -st "replace(http:,https:,{STRING})" -pf

# Inverter strings
./strx -l data.txt -st "rev({STRING})" -pf

# URL encoding
./strx -l params.txt -st "urlencode({STRING})" -pf
```

### Parâmetros de Controle

- **`-pf`**: Mostrar apenas resultados das funções (ignora execução shell)
- **`-of`**: Salvar resultados das funções em arquivo de saída

```bash
# Apenas mostrar resultado das funções
./strx -l domains.txt -st "{STRING}; md5({STRING})" -pf

# Salvar funções em arquivo
./strx -l data.txt -st "base64({STRING})" -pf -of -o encoded.txt
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
./strx -l data.txt -st "check_admin_exemplo({STRING})" -pf
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
./strx -module "tipo:nome_do_modulo"
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
./strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm
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
| `ipinfo`      | Scanner de portas IP/host                 | `-module "clc:ipinfo"` |
| `lycos`       | Realiza buscas com dorks no Lycos         | `-module "clc:lycos"` |
| `naver`       | Realiza buscas com dorks no Naver (Coreano)| `-module "clc:naver"` |
| `netscan`     | Scanner de rede (hosts, serviços)         | `-module "clc:netscan"` |
| `shodan`      | Consulta API Shodan                       | `-module "clc:shodan"` |
| `sogou`       | Realiza buscas com dorks no Sogou (Chinês)| `-module "clc:sogou"` |
| `subdomain`   | Enumeração de subdomínios                 | `-module "clc:subdomain"` |
| `virustotal`  | Consulta API VirusTotal                   | `-module "clc:virustotal"` |
| `whois`       | Consulta WHOIS de domínios                | `-module "clc:whois"` |
| `yahoo`       | Realiza buscas com dorks no Yahoo         | `-module "clc:yahoo"` |

```bash
# Exemplo: Coletar informações DNS
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm

# Exemplo: Coletar informações usando motores de busca
./strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:googlecse" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:duckduckgo" -pm

# Exemplos com dorking específico
echo 'site:fbi.gov filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:google" -pm
echo 'site:github.com inurl:admin' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm
echo 'inurl:admin' | ./strx -st "echo {STRING}" -module "clc:lycos" -pm
echo 'site:github.com' | ./strx -st "echo {STRING}" -module "clc:ezilon" -pm
echo 'filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm
```


### Módulos Output (OUT)
Módulos para saída e integração de resultados:

| Módulo        | Descrição                                 | Exemplo CLI |
|---------------|-------------------------------------------|-------------|
| `sqlite`      | Salva dados em banco SQLite               | `-module "out:sqlite"` |
| `mysql`       | Salva dados em banco MySQL                | `-module "out:mysql"` |
| `telegram`    | Envia resultados via Telegram Bot         | `-module "out:telegram"` |
| `slack`       | Envia resultados via Slack Webhook        | `-module "out:slack"` |
| `json_output` | Salva resultados em JSON                  | `-module "out:json_output"` |
| `csv_output`  | Salva resultados em CSV                   | `-module "out:csv_output"` |
| `xml_output`  | Salva resultados em XML                   | `-module "out:xml_output"` |

```bash
# Exemplo: Salvar em SQLite
./strx -l data.txt -st "process {STRING}" -module "out:sqlite" -pm
```


### Módulos Connection (CON)
Módulos para conexões e sondagens especializadas:

| Módulo        | Descrição                                 | Exemplo CLI |
|---------------|-------------------------------------------|-------------|
| `ssh`         | Conexão SSH e execução remota             | `-module "con:ssh"` |
| `ftp`         | Conexão FTP e listagem/download           | `-module "con:ftp"` |
| `http_probe`  | Sondagem HTTP/HTTPS, análise de headers   | `-module "con:http_probe"` |

```bash
# Exemplo: Sondar servidores HTTP
./strx -l urls.txt -st "{STRING}" -module "con:http_probe" -pm
```

### Módulos Inteligência artificial  (AI)
Módulos para de prompts para Inteligência artificial:

| Módulo        | Descrição                                 | Exemplo CLI |
|---------------|-------------------------------------------|-------------|
| `gemini`      | Prompt para Google Gemini AI - ([Criar API Key](https://aistudio.google.com/app/apikey))    | `-module "ai:gemini"` |

```bash
# Exemplo: Uso de arquivos com Prompts
./strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm

# Exemplo: Coletar urls e enviar para analise montando Prompt
./strx -l urls.txt -st "echo 'Analisar URL: {STRING}'" -module "ai:gemini" -pm
```

#### Exemplos Práticos
```bash
# Extrair emails e salvar ordenados
./strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# Verificar DNS de domínios suspeitos
./strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# Pipeline com múltiplos módulos
cat logs.txt | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | ./strx -st "echo {STRING}" -module "clc:dns" -pm

# Extrair URLs e verificar status
./strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | ./strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
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
./strx -l data.txt -st "echo '{STRING}'" -module "ext:email" -pm -f ".gov"

# DNS lookup apenas para domínios .br
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm -f ".br"
```

## 🎯 FILTROS E PROCESSAMENTO SELETIVO

O sistema de filtros permite processar apenas strings que atendam critérios específicos, otimizando performance e precisão.

### Uso de Filtros
```bash
./strx -f "valor_filtro" / ./strx --filter "valor_filtro"
```

### Exemplos de Filtros
```bash
# Filtrar apenas domínios .gov.br
./strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# Filtrar apenas URLs HTTPS
./strx -l urls.txt -st "curl {STRING}" -f "https"

# Filtrar IPs específicos
./strx -l logs.txt -st "analyze {STRING}" -f "192.168"

# Filtrar extensões de arquivo
./strx -l files.txt -st "process {STRING}" -f ".pdf"
```

### Combinação com Módulos
```bash
# Extrair emails e salvar ordenados
./strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# Verificar DNS de domínios suspeitos
./strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# Pipeline com múltiplos módulos
cat logs.txt | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | ./strx -st "echo {STRING}" -module "clc:dns" -pm

# Extrair URLs e verificar status
./strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | ./strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

## ⚡ PROCESSAMENTO PARALELO

String-X suporta processamento paralelo através de threads para acelerar operações em grandes volumes de dados.

### Configuração de Threads
```bash
# Definir número de threads
./strx -t 50 / ./strx --thread 50

# Definir delay entre threads
./strx -sleep 2
```

### Exemplos com Threading
```bash
# Verificação rápida de status HTTP
./strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# Resolução DNS em massa
./strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1

# Scanning de portas
./strx -l ip_list.txt -st "nmap -p 80,443 {STRING}" -t 20 -sleep 3
```

### Boas Práticas para Threading
- **Rate limiting**: Use `-sleep` para evitar sobrecarga de serviços
- **Número adequado**: Ajuste `-t` conforme recursos disponíveis
- **Monitoramento (verbose)**: Use `-v` para acompanhar progresso
## 📸 EXEMPLOS VISUAIS

### Execução Básica
**Comando**: `cat hosts.txt | ./strx -str 'host {STRING}'`

![Screenshot](/asset/img1.png)

### Processamento com Threading
**Comando**: `cat hosts.txt | ./strx -str "curl -Iksw 'CODE:%{response_code};IP:%{remote_ip};HOST:%{url.host};SERVER:%header{server}' https://{STRING}" -p "grep -o -E 'CODE:.(.*)|IP:.(.*)|HOST:.(.*)|SERVER:.(.*)'" -t 30`

![Screenshot](/asset/img3.png)

### Modo Verbose
**Comando**: `cat hosts.txt | ./strx -str 'host {STRING}' -v`

![Screenshot](/asset/img2.png)

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
