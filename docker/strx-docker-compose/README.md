# String-X Docker

Este diretório contém a configuração Docker para executar o String-X em um contêiner isolado. Isso permite usar todas as funcionalidades do String-X sem precisar instalar diretamente no seu sistema.

## Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Construção da Imagem](#construção-da-imagem)
- [Uso Básico](#uso-básico)
- [Exemplos Práticos](#exemplos-práticos)
- [Montando Volumes](#montando-volumes)
- [Uso em Pipeline](#uso-em-pipeline)
- [Dicas e Otimizações](#dicas-e-otimizações)
- [Resolução de Problemas](#resolução-de-problemas)

## Características

- Imagem leve baseada em Alpine Linux
- Todas as dependências pré-instaladas
- Acesso a todos os módulos do String-X
- Compatível com montagem de volumes para processamento de arquivos locais
- Suporte a encadeamento via pipes com comandos do host

## Requisitos

- Docker instalado e configurado
- Acesso à internet (para a primeira construção da imagem)
- Permissões para executar contêineres Docker

## Construção da Imagem

Para construir a imagem Docker do String-X:

```bash
# Navegar até o diretório do Dockerfile
cd docker/strx-docker-compose

# Construir a imagem
docker build -t string-x .
```

Se preferir usar a imagem oficial do Docker Hub (quando disponível):

```bash
# Baixar a imagem oficial
docker pull mrclownlab/string-x:latest
```

## Uso Básico

### Executar com parâmetros simples

```bash
# Ver ajuda do String-X
docker run --rm string-x -h

# Ver módulos disponíveis
docker run --rm string-x -types

# Ver exemplos de uso
docker run --rm string-x -examples

# Ver funções disponíveis
docker run --rm string-x -funcs
```

### Procesar uma string individual

```bash
# Executar um comando em uma string
docker run --rm string-x -s "example.com" -st "whois {STRING}"

# Extrair domínios
docker run --rm string-x -s "echo 'Visite https://example.com e http://test.org'" -module "ext:domain" -pm
```

## Exemplos Práticos

### 1. Processamento de arquivos

Para processar arquivos do seu sistema, monte o diretório como volume:

```bash
# Montar o diretório atual e processar arquivo local
docker run --rm -v $(pwd):/dados string-x -l /dados/urls.txt -st "curl -I {STRING}"

# Salvar resultado em arquivo local
docker run --rm -v $(pwd):/dados string-x -l /dados/dominios.txt -st "dig +short {STRING}" -o /dados/resultados.txt
```

### 2. Usando módulos específicos

```bash
# Extrair emails de um arquivo
docker run --rm -v $(pwd):/dados string-x -l /dados/texto.txt -st "echo {STRING}" -module "ext:email" -pm

# Busca no Google
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Multi-threading para consultas DNS
docker run --rm -v $(pwd):/dados string-x -l /dados/dominios.txt -st "dig {STRING}" -t 20

# Extrair, validar e salvar emails
docker run --rm -v $(pwd):/dados string-x -l /dados/texto.txt -module "ext:email" -pm -o /dados/emails.csv
```

### 3. Encadeando módulos

```bash
# Extrair URLs, depois extrair domínios e depois consultar DNS
docker run --rm -v $(pwd):/dados string-x -l /dados/texto.txt -module "ext:url|ext:domain" -pm

# Coletar subdomínios e verificar se estão ativos
docker run --rm -v $(pwd):/dados string-x -l /dados/alvos.txt -module "clc:subdomain" -pm
```

### 4. Filtrando resultados

```bash
# Extrair URLs e filtrar apenas HTTPS
docker run --rm -v $(pwd):/dados string-x -l /dados/links.txt -module "ext:url" -pm -p "grep https://"

# Executar comando e filtrar saída
docker run --rm -v $(pwd):/dados string-x -l /dados/ips.txt -st "nmap -p 80,443 {STRING}" -p "grep open"
```

## Montando Volumes

### Estrutura de diretórios sugerida

Para organizar melhor seu trabalho com o String-X em contêiner, crie uma estrutura de diretórios:

```bash
mkdir -p ~/strx-projeto/{input,output,wordlists}

# Usar a estrutura com o Docker
docker run --rm -v ~/strx-projeto:/dados string-x -l /dados/input/alvos.txt -o /dados/output/resultados.txt
```


## Uso em Pipeline

O String-X pode ser usado em pipelines com outros comandos:

```bash
# Enviar entrada via pipe
echo "example.com" | docker run --rm -i string-x -st "dig +short {STRING}"

# Encadear a saída para outros comandos
cat domains.txt | docker run --rm -i string-x -st "host {STRING}" | grep "has address"

# Pipe complexo
cat urls.txt | docker run --rm -i string-x -module "ext:domain" -pm | docker run --rm -i string-x -st "nslookup {STRING}" | grep "Address"
```

## Dicas e Otimizações

### Alias para facilitar o uso

Adicione ao seu `.bashrc` ou `.zshrc`:

```bash
# Alias para String-X Docker
alias strx-docker='docker run --rm -v $(pwd):/dados -i string-x'

# Uso simplificado
strx-docker -l /dados/alvos.txt -st "ping -c 1 {STRING}"
```

### Reuso do contêiner para múltiplas operações

```bash
# Iniciar contêiner interativo
docker run --rm -it -v $(pwd):/dados --entrypoint /bin/sh string-x

# Dentro do contêiner
strx -l /dados/alvos1.txt -st "dig {STRING}" -o /dados/resultado1.txt
strx -l /dados/alvos2.txt -st "whois {STRING}" -o /dados/resultado2.txt
exit
```

## Resolução de Problemas

### Imagem não encontrada

```
docker: Error response from daemon: pull access denied for string-x, repository does not exist or may require 'docker login'.
```

**Solução**: Certifique-se de ter construído a imagem localmente:
```bash
docker build -t string-x /caminho/para/docker/strx-docker-compose
```

### Erro de acesso a arquivos

```
Error opening file: Permission denied
```

**Solução**: Verifique as permissões ou execute com seu próprio usuário:
```bash
docker run --rm -v $(pwd):/dados --user $(id -u):$(id -g) string-x -l /dados/arquivo.txt
```

### Problemas de rede no contêiner

**Solução**: Use a rede do host para facilitar conexões:
```bash
docker run --rm --network host string-x -s "localhost" -st "curl {STRING}"
```

### Contêiner muito lento

**Solução**: Limite recursos ou aumente a alocação:
```bash
# Aumentar recursos
docker run --rm --memory=1g --cpus=2 string-x -l alvos.txt -st "comando pesado {STRING}"

# Para operações com muitas threads
docker run --rm string-x -l alvos.txt -st "comando {STRING}" -t 10
```
