# Uso do String-X com Strings Únicas

O String-X suporta o uso de strings únicas através do parâmetro `-s`, permitindo executar comandos ou módulos em uma única string sem a necessidade de criar arquivos de entrada.

## Sintaxe Básica

```bash
./strx -s "string_unica" -st "comando {STRING}"
```

O placeholder `{STRING}` será substituído pela string fornecida via parâmetro `-s`.

## Exemplos Práticos

### 1. Consultas DNS

Executar uma consulta DNS para um único domínio:

```bash
./strx -s "exemplo.com" -st "dig {STRING}"
```

### 2. Requisições HTTP

Fazer uma requisição HTTP para um único URL:

```bash
./strx -s "https://example.com" -st "curl -I {STRING}"
```

### 3. Uso com Módulos

Extrair emails de uma única string:

```bash
./strx -s "contato: use@gmail.com" -st "echo {STRING}" -module "ext:email" -pm
```

### 4. Escaneamento de portas

Executar nmap em um único host:

```bash
./strx -s "192.168.1.25" -st "nmap -p 80,443 {STRING}"
```

### 5. Coleta de informações

Usar um coletor em um único domínio:

```bash
./strx -s "exemplo.com" -module "clc:subdomain" -pm
```

## Combinando com Outros Parâmetros

O parâmetro `-s` pode ser combinado com outros parâmetros do String-X:

```bash
# Usando verbose para ver mais informações
./strx -s "example.com" -st "dig {STRING}" -verbose

# Definindo formato de saída
./strx -s "example.com" -st "echo {STRING}" -module "clc:subdomain" -format json -pm

# Redirecionando saída para arquivo
./strx -s "example.com" -st "dig {STRING}" -o "resultados.txt"

# Usando multithreading com módulos
./strx -s "example.com" -st "echo {STRING}" -module "clc:crtsh" -pm -t 10
```

## Quando Usar `-s` vs `-l`

- Use `-s` quando:
  - Precisa processar rapidamente uma única string
  - Está testando comandos ou módulos
  - Não quer criar um arquivo de entrada temporário

- Use `-l` quando:
  - Tem múltiplas strings para processar
  - Precisa processar entradas de um arquivo
  - Recebe dados via pipe de outro comando
