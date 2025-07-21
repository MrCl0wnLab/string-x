# Comandos Essenciais do String-X

Este guia fornece uma referência rápida aos comandos e parâmetros mais utilizados do String-X.

## Parâmetros de Entrada

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-s`, `--string` | Define uma string única para processamento | `-s "example.com"` |
| `-l`, `--list` | Especifica um arquivo com múltiplas linhas | `-l dominios.txt` |
| `-st`, `--stringtemplate` | Define o comando a ser executado com a string | `-st "dig +short {STRING}"` |
| `-module` | Especifica o módulo a ser utilizado | `-module "ext:email"` |

## Parâmetros de Controle de Saída

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-o`, `--output` | Arquivo para salvar os resultados | `-o resultados.txt` |
| `-pm`, `--printmodule` | Imprime a saída do módulo | `-pm` |
| `-p`, `--pipe` | Define um comando para filtrar a saída | `-p "grep open"` |
| `-format` | Define o formato de saída (txt, csv, json) | `-format json` |

## Parâmetros de Performance

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-t`, `--thread` | Número de threads para processamento paralelo | `-t 10` |
| `-sleep` | Tempo de espera entre execuções (segundos) | `-sleep 2` |
| `-timeout` | Tempo limite para execução do comando (segundos) | `-timeout 30` |
| `-retry` | Número de tentativas em caso de falha | `-retry 3` |

## Comandos Informativos

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `--help` | Exibe ajuda geral | `./strx --help` |
| `-types` | Lista os tipos de módulos disponíveis | `./strx -types` |
| `-examples` | Lista exemplos de uso dos módulos | `./strx -examples` |
| `-funcs` | Lista as funções integradas | `./strx -funcs` |
| `-upgrade` | Atualiza o String-X para a última versão | `./strx -upgrade` |
| `-version` | Exibe a versão atual do String-X | `./strx -version` |

## Exemplos de Comando Completos

### Exemplo Básico

```bash
# Processar uma lista de domínios e salvar os resultados
./strx -l dominios.txt -st "dig +short {STRING}" -o resultados.txt
```

### Usando Módulos

```bash
# Extrair emails de um texto e salvar em CSV
./strx -l texto.txt -st "echo {STRING}" -module "ext:email" -pm -format csv -o emails.csv
```

### Multi-threading com Filtros

```bash
# Verificar portas abertas em múltiplos hosts com 20 threads
./strx -l hosts.txt -st "nmap -p 80,443,8080 {STRING}" -t 20 -p "grep open" -o portas_abertas.txt
```

### Encadeamento de Módulos

```bash
# Extrair URLs, depois domínios e verificar DNS
./strx -l arquivo.txt -module "ext:url" -pm -o resultados.txt
```

### Filtragem Avançada

```bash
# Realizar uma busca e filtrar resultados específicos
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm -p "grep -E '\.gov\.br|\.edu\.br'" -o dominios_gov_edu.txt
```

### Redirecionamento com Pipes

```bash
# Encadear com pipes do sistema
cat dominios.txt | ./strx -st "host {STRING}" | grep "has address" | ./strx -st "echo {STRING}" -module "ext:ip" -pm
```

## Próximos Passos

- Veja [Parâmetros](parametros.md) para detalhes completos de todas as opções
- Explore [Exemplos Práticos](exemplos-praticos.md) para casos de uso reais
- Consulte [Docker](docker.md) para uso em contêineres
