# Parâmetros do String-X

Este documento fornece uma referência completa de todos os parâmetros disponíveis no String-X.

## Parâmetros de Entrada

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-s` | `-string` | String única para processamento | String | Não¹ | `-s "example.com"` |
| `-l` | `-list` | Arquivo com múltiplas linhas | String (caminho) | Não¹ | `-l dominios.txt` |
| `-st` | `-stringtemplate` | Comando a ser executado com a string | String | Sim² | `-st "dig +short {STRING}"` |

¹ Pelo menos um tipo de entrada é obrigatório: `-s`, `-l` ou entrada padrão (pipe)  
² Obrigatório a menos que esteja usando apenas módulos

## Parâmetros de Módulos

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-module` | - | Módulo(s) a ser(em) utilizado(s) | String | Não | `-module "ext:email"` |
| `-pm` | `-printmodule` | Imprime a saída do módulo | Flag | Não | `-pm` |

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
| `-o` | `-output` | Arquivo para salvar os resultados | String (caminho) | Não | `-o resultados.txt` |
| `-p` | `-pipe` | Comando para filtrar a saída | String | Não | `-p "grep open"` |
| `-format` | - | Formato de saída (txt, csv, json) | String | Não | `-format json` |
| `-a` | `-append` | Adicionar ao invés de sobrescrever arquivo | Flag | Não | `-a` |
| `-q` | `-quiet` | Modo silencioso (sem output na tela) | Flag | Não | `-q` |

## Parâmetros de Filtragem

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|---------|
| `-f` | `-filter` | Filtro para seleção de strings de entrada | String | Não | `-f ".gov.br"` |
| `-iff` | - | Filtro para resultados de função: retorna apenas resultados que contenham o valor especificado | String | Não | `-iff "admin"` |
| `-ifm` | - | Filtro para resultados de módulo: retorna apenas resultados que contenham o valor especificado | String | Não | `-ifm "hash"` |

### Como Funcionam os Filtros

- **`-f` (filter)**: Aplica filtro nas strings de entrada antes da execução do comando. Apenas strings que contenham o valor especificado serão processadas.
- **`-iff` (if function)**: Aplica filtro nos resultados de função. Apenas resultados de função que contenham o valor especificado serão exibidos e salvos.
- **`-ifm` (if module)**: Aplica filtro nos resultados de módulo. Apenas resultados de módulo que contenham o valor especificado serão exibidos e salvos.

### Exemplos de Filtragem

```bash
# Filtrar entrada: processar apenas domínios .gov.br
strx -l dominios.txt -st "curl {STRING}" -f ".gov.br"

# Filtrar função: exibir apenas resultados de função que contenham "admin" 
strx -l urls.txt -st "{STRING}; md5({STRING})" -pf -iff "admin"

# Filtrar módulo: exibir apenas resultados de módulo que contenham hash específico
strx -l data.txt -st "echo {STRING}" -module "ext:hash" -pm -ifm "a1b2c3"

# Combinar filtros: função E módulo
strx -l dados.txt -st "{STRING}; md5({STRING})" -module "ext:domain" -pf -pm -iff "google" -ifm "admin"
```

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
| `-help` | - | Exibe ajuda geral | Flag | `./strx -help` |
| `-types` | - | Lista os tipos de módulos disponíveis | Flag | `./strx -types` |
| `-examples` | - | Lista exemplos de uso dos módulos | Flag | `./strx -examples` |
| `-funcs` | - | Lista as funções integradas | Flag | `./strx -funcs` |
| `-upgrade` | - | Atualiza o String-X para a última versão | Flag | `./strx -upgrade` |
| `-version` | - | Exibe a versão atual do String-X | Flag | `./strx -version` |
| `-v` | `-verbose` | Modo verboso com níveis (1-5 ou 'all'). 1=info, 2=warning, 3=debug, 4=error, 5=exception | String/Flag | `./strx -v 3` |

## Parâmetros de Segurança

| Parâmetro | Forma Longa | Descrição | Tipo | Obrigatório | Exemplo |
|-----------|-------------|-----------|------|-------------|----------|
| `-ds` | `-disable-security` | Desabilita validações de segurança (usar com cuidado) | Flag | Não | `-ds` |

⚠️ **Aviso sobre Segurança**: O parâmetro `-ds` desabilita validações importantes que protegem contra comandos maliciosos. Use apenas quando necessário e confiando no conteúdo.

## Parâmetros Avançados

| Parâmetro | Forma Longa | Descrição | Tipo | Exemplo |
|-----------|-------------|-----------|------|---------|
| `-c` | `-config` | Arquivo de configuração personalizado | String (caminho) | `-c config.yaml` |
| `-e` | `-encoding` | Codificação dos arquivos de entrada/saída | String | `-e utf-8` |
| `-no-banner` | - | Suprime a exibição do banner | Flag | `-no-banner` |
| `-timestamp` | - | Adiciona timestamp aos logs | Flag | `-timestamp` |

## Sistema de Verbosidade Detalhado

O String-X oferece um sistema de verbosidade com 5 níveis distintos para controle granular da saída:

### Níveis de Verbosidade

| Nível | Descrição | Tipo de Informação | Exemplo |
|-------|-----------|-------------------|---------|
| `1` | **Info** | Informações básicas de progresso | `-v 1` |
| `2` | **Warning** | Avisos e alertas | `-v 2` |
| `3` | **Debug** | Informações detalhadas de depuração | `-v 3` |
| `4` | **Error** | Erros de execução | `-v 4` |
| `5` | **Exception** | Exceções completas com stack trace | `-v 5` |
| `all` | **Todos** | Todas as informações disponíveis | `-v all` |

### Combinação de Níveis

Você pode combinar múltiplos níveis usando vírgulas:

```bash
# Mostrar apenas info e debug
./strx -l data.txt -st "process {STRING}" -v "1,3"

# Mostrar warning, error e exception
./strx -l data.txt -st "process {STRING}" -v "2,4,5"
```

### Casos de Uso Recomendados

- **Desenvolvimento/Debug**: Use `-v 3` ou `-v all`
- **Monitoramento**: Use `-v 1,2` para info básica e avisos
- **Troubleshooting**: Use `-v all` para máxima informação
- **Produção**: Use `-v 2,4` para avisos e erros

## Exemplos de Combinação de Parâmetros

### Exemplo 1: Coleta Básica com Verbose

```bash
./strx -l dominios.txt -st "dig +short {STRING}" -o resultados.txt -t 5 -v 1
```

### Exemplo 2: Módulos com Debug

```bash
./strx -l alvos.txt -module "clc:dns" -pm -retry 3 -format json -o dns_results.json -v 3
```

### Exemplo 3: Configurações Avançadas com Monitoring

```bash
./strx -l urls.txt -st "curl -s {STRING}" -proxy "http://127.0.0.1:8080" -retry 5 -p "grep 'title'" -o titulos.txt -v "1,2"
```

### Exemplo 4: Comandos Complexos com Segurança Desabilitada

```bash
./strx -l data.txt -st "echo {STRING}; md5sum {STRING}" -ds -v 3
```

### Exemplo 5: Processamento de Arquivos Grandes

```bash
./strx -l huge_file.txt -st "process {STRING}" -t 20 -sleep 1 -v 1 -ds
```

### Exemplo 6: Troubleshooting Completo

```bash
./strx -l problematic_data.txt -st "complex_command {STRING}" -v all -retry 3
```
