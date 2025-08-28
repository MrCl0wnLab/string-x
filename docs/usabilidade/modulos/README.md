# Documentação de Módulos do String-X

Esta seção contém documentação detalhada para cada módulo disponível no String-X.

## Tipos de Módulos

O String-X oferece vários tipos de módulos para diferentes propósitos:

- **EXT (Extrator)**: Módulos para extrair dados específicos como URLs, emails, IPs, etc.
- **CLC (Coletor)**: Módulos para coletar informações de fontes externas
- **OUT (Output)**: Módulos para formatar e exportar dados
- **CON (Conexão)**: Módulos para estabelecer conexões com sistemas externos
- **AI (Inteligência Artificial)**: Módulos para processamento com serviços de IA

## Módulos Disponíveis

### Módulos Coletores (CLC)

| Nome | Descrição | Exemplo de Uso |
|------|-----------|----------------|
| http_probe | Verifica disponibilidade de servidores web | `clc:http_probe` |
| spider | Web spider para coleta recursiva de URLs | `clc:spider` |
| dns | Coleta informações de registros DNS | `clc:dns` |
| subdomain | Enumera subdomínios | `clc:subdomain` |
| whois | Coleta informações WHOIS | `clc:whois` |
| crtsh | Busca certificados SSL em crt.sh | `clc:crtsh` |
| virustotal | Coleta informações do VirusTotal | `clc:virustotal` |
| google | Realiza buscas no Google | `clc:google` |
| googlecse | Realiza buscas avançadas no Google CSE | `clc:googlecse` |
| bing | Realiza buscas no Bing | `clc:bing` |
| duckduckgo | Realiza buscas no DuckDuckGo | `clc:duckduckgo` |
| yahoo | Realiza buscas no Yahoo | `clc:yahoo` |
| sogou | Realiza buscas no Sogou | `clc:sogou` |
| lycos | Realiza buscas no Lycos | `clc:lycos` |
| ezilon | Realiza buscas no Ezilon | `clc:ezilon` |
| shodan | Consulta dados do Shodan | `clc:shodan` |
| ipinfo | Coleta informações sobre IPs | `clc:ipinfo` |
| geoip | Coleta informações geográficas de IPs | `clc:geoip` |
| emailverify | Verifica validade de emails | `clc:emailverify` |
| archive | Busca páginas arquivadas (Wayback Machine) | `clc:archive` |
| netscan | Realiza varreduras em redes | `clc:netscan` |

### Módulos Extratores (EXT)

| Nome | Descrição | Exemplo de Uso |
|------|-----------|----------------|
| url | Extrai URLs de textos | `ext:url` |
| domain | Extrai domínios de textos ou URLs | `ext:domain` |
| email | Extrai endereços de email | `ext:email` |
| ip | Extrai endereços IP | `ext:ip` |
| hash | Extrai valores de hash | `ext:hash` |
| phone | Extrai números de telefone | `ext:phone` |
| mac | Extrai endereços MAC | `ext:mac` |
| documents | Extrai números de documentos (CPF, CNPJ, etc.) | `ext:documents` |
| cryptocurrency | Extrai endereços de criptomoedas | `ext:cryptocurrency` |
| metadata | Extrai metadados de arquivos | `ext:metadata` |
| file_hash | Gera hashes de arquivos | `ext:file_hash` |
| credential | Extrai credenciais de textos | `ext:credential` |

### Módulos de Conexão (CON)

| Nome | Descrição | Exemplo de Uso |
|------|-----------|----------------|
| s3 | Conexão com Amazon S3 | `con:s3` |
| mysql | Conexão com banco de dados MySQL | `con:mysql` |
| sqlite | Conexão com banco de dados SQLite | `con:sqlite` |
| opensearch | Conexão com OpenSearch | `con:opensearch` |
| ssh | Conexão SSH com servidores | `con:ssh` |
| ftp | Conexão FTP com servidores | `con:ftp` |
| telegram | Envio de mensagens via Telegram | `con:telegram` |
| slack | Envio de mensagens via Slack | `con:slack` |

### Módulos de Saída (OUT)

| Nome | Descrição | Exemplo de Uso |
|------|-----------|----------------|
| json | Formata saída em JSON | `out:json` |
| csv | Formata saída em CSV | `out:csv` |
| xml | Formata saída em XML | `out:xml` |

### Módulos de Inteligência Artificial (AI)

| Nome | Descrição | Exemplo de Uso |
|------|-----------|----------------|
| openai | Processamento com OpenAI | `ai:openai` |
| gemini | Processamento com Google Gemini | `ai:gemini` |

## Utilizando Módulos

Para utilizar um módulo no String-X, use o parâmetro `-module` seguido do tipo e nome do módulo:

```bash
./strx -l input.txt -st "echo {STRING}" -module "tipo:nome" -pm
```

Para exibir apenas os resultados do módulo, adicione o parâmetro `-pm` (print module).

## Encadeando Módulos

O String-X suporta encadeamento de múltiplos módulos usando o caractere pipe (`|`):

```bash
./strx -l input.txt -st "echo {STRING}" -module "ext:url|ext:domain|clc:dns" -pm
```

Para mais informações sobre encadeamento de módulos, consulte [Encadeamento de Módulos](../encadeamento-modulos.md).