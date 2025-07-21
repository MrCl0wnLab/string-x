# Parâmetros do String-X

Este documento fornece uma referência completa de todos os parâmetros disponíveis no String-X.

## Parâmetros de Entrada

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-s` | `--string` | String única para processamento | String | Não¹ | `-s "example.com"` |
| `-l` | `--list` | Arquivo com múltiplas linhas | String (caminho) | Não¹ | `-l dominios.txt` |
| `-st` | `--stringtemplate` | Comando a ser executado com a string | String | Sim² | `-st "dig +short {STRING}"` |

¹ Pelo menos um tipo de entrada é obrigatório: `-s`, `-l` ou entrada padrão (pipe)  
² Obrigatório a menos que esteja usando apenas módulos

## Parâmetros de Módulos

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-module` | - | Módulo(s) a ser(em) utilizado(s) | String | Não | `-module "ext:email"` |
| `-pm` | `--printmodule` | Imprime a saída do módulo | Flag | Não | `-pm` |

### Sintaxe para Encadeamento de Módulos

```
-module "tipo1:nome1|tipo2:nome2|..."
```

O caractere pipe (`|`) é usado para encadear múltiplos módulos, onde:
- A saída do primeiro módulo (`tipo1:nome1`) é passada como entrada para o segundo módulo (`tipo2:nome2`)
- O processo continua até o último módulo, cuja saída será o resultado final

Exemplo: `-module "ext:url|ext:domain|clc:dns"`

Para mais detalhes sobre encadeamento de módulos, consulte [Encadeamento de Módulos](encadeamento-modulos.md).

## Parâmetros de Controle de Saída

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-o` | `--output` | Arquivo para salvar os resultados | String (caminho) | Não | `-o resultados.txt` |
| `-p` | `--pipe` | Comando para filtrar a saída | String | Não | `-p "grep open"` |
| `-format` | - | Formato de saída (txt, csv, json) | String | Não | `-format json` |
| `-a` | `--append` | Adicionar ao invés de sobrescrever arquivo | Flag | Não | `-a` |
| `-q` | `--quiet` | Modo silencioso (sem output na tela) | Flag | Não | `-q` |

## Parâmetros de Performance

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-t` | `-thread` | Número de threads para processamento paralelo | Inteiro | Não | `-t 10` |
| `-sleep` | - | Tempo de espera entre execuções (segundos) | Float | Não | `-sleep 1.5` |
| `-retry` | - | Número de tentativas em caso de falha | Inteiro | Não | `-retry 3` |

## Parâmetros de Conectividade

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-proxy` | - | Proxy para requisições HTTP | String | Não | `-proxy "http://127.0.0.1:8080"` |

## Parâmetros Específicos de Módulos

### Parâmetros para Módulos de Saída (OUT)

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-host` | Host para conexão (MySQL, OpenSearch, etc.) | `-host "localhost"` |
| `-port` | Porta para conexão | `-port 3306` |
| `-username` | Nome de usuário para autenticação | `-username "usuario"` |
| `-password` | Senha para autenticação | `-password "senha"` |
| `-database` | Nome do banco de dados | `-database "strx_db"` |
| `-table` | Nome da tabela | `-table "resultados"` |
| `-index` | Nome do índice (para OpenSearch) | `-index "strx-dados"` |

### Parâmetros para Módulos de Coleta (CLC)

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-limit` | Limite de resultados | `-limit 100` |
| `-api-key` | Chave de API para serviços | `-api-key "abc123"` |
| `-depth` | Profundidade de busca | `-depth 2` |
| `-fields` | Campos específicos a coletar | `-fields "title,url,date"` |

## Parâmetros Informativos

| Parâmetro | Forma Longa | Descrição | Tipo | Exemplo |
|-----------|-------------|-----------|------|---------|
| `--help` | - | Exibe ajuda geral | Flag | `./strx --help` |
| `-types` | - | Lista os tipos de módulos disponíveis | Flag | `./strx -types` |
| `-examples` | - | Lista exemplos de uso dos módulos | Flag | `./strx -examples` |
| `-funcs` | - | Lista as funções integradas | Flag | `./strx -funcs` |
| `-upgrade` | - | Atualiza o String-X para a última versão | Flag | `./strx -upgrade` |
| `-version` | - | Exibe a versão atual do String-X | Flag | `./strx -version` |
| `-debug` | - | Ativa o modo de debug para saída detalhada | Flag | `./strx -debug` |

## Parâmetros Avançados

| Parâmetro | Forma Longa | Descrição | Tipo | Exemplo |
|-----------|-------------|-----------|------|---------|
| `-c` | `--config` | Arquivo de configuração personalizado | String (caminho) | `-c config.yaml` |
| `-e` | `--encoding` | Codificação dos arquivos de entrada/saída | String | `-e utf-8` |
| `-no-banner` | - | Suprime a exibição do banner | Flag | `-no-banner` |
| `-timestamp` | - | Adiciona timestamp aos logs | Flag | `-timestamp` |
| `-log-level` | - | Define o nível de log | String | `-log-level debug` |

## Exemplos de Combinação de Parâmetros

### Exemplo 1: Coleta Básica

```bash
./strx -l dominios.txt -st "dig +short {STRING}" -o resultados.txt -t 5
```

### Exemplo 2: Módulos com Parâmetros Específicos

```bash
./strx -l alvos.txt -module "clc:dns" -pm -retry 3 -format json -o dns_results.json
```

### Exemplo 3: Configurações Avançadas de Rede

```bash
./strx -l urls.txt -st "curl -s {STRING}" -proxy "http://127.0.0.1:8080" -retry 5 -p "grep 'title'" -o titulos.txt
```

### Exemplo 4: Módulos de Banco de Dados

```bash
./strx -l emails.txt -st "echo {STRING}" -module "ext:email" -pm
```
