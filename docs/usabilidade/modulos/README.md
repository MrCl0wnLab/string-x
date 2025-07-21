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
| [http_probe](http_probe.md) | Verifica disponibilidade de servidores web | `clc:http_probe` |
| dns | Coleta informações de registros DNS | `clc:dns` |
| subdomain | Enumera subdomínios | `clc:subdomain` |
| whois | Coleta informações WHOIS | `clc:whois` |
| crtsh | Busca certificados SSL em crt.sh | `clc:crtsh` |
| virustotal | Coleta informações do VirusTotal | `clc:virustotal` |
| google | Realiza buscas no Google | `clc:google` |
| bing | Realiza buscas no Bing | `clc:bing` |
| shodan | Consulta dados do Shodan | `clc:shodan` |

### Módulos Extratores (EXT)

| Nome | Descrição | Exemplo de Uso |
|------|-----------|----------------|
| url | Extrai URLs de textos | `ext:url` |
| domain | Extrai domínios de textos ou URLs | `ext:domain` |
| email | Extrai endereços de email | `ext:email` |
| ip | Extrai endereços IP | `ext:ip` |
| hash | Extrai valores de hash | `ext:hash` |

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