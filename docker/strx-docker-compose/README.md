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

- **Python 3.12+**: Compatível com a versão moderna do String-X
- **Alpine Linux**: Imagem leve e segura
- **Dependências pré-instaladas**: Todos os módulos e bibliotecas necessárias
- **Sistema de segurança**: Validações integradas com opção `-ds` para bypass
- **5 níveis de verbosidade**: Controle granular de saída (1-5 ou 'all')
- **Usuário não-root**: Execução segura com usuário limitado
- **Health checks**: Monitoramento automático do container
- **Suporte completo a módulos**: EXT, CLC, CON, OUT, AI

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

# Testar verbosidade (1=info, 2=warning, 3=debug, 4=error, 5=exception)
docker run --rm string-x -examples -v 3
```

### Procesar uma string individual

```bash
# Executar um comando em uma string
docker run --rm string-x -s "example.com" -st "whois {STRING}"

# Extrair domínios com verbose nível 3
docker run --rm string-x -s "echo 'Visite https://example.com e http://test.org'" -module "ext:domain" -pm -v 3

# Comando complexo com bypass de segurança
docker run --rm string-x -s "example.com" -st "whois {STRING} && echo 'Done'" -ds

# Modo verbose 'all' para debug completo
docker run --rm string-x -s "test@example.com" -module "ext:email" -pm -v all
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
# Extrair emails de um arquivo com debug
docker run --rm -v $(pwd):/dados string-x -l /dados/texto.txt -module "ext:email" -pm -v 3

# Busca no Google com bypass de segurança se necessário
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -module "clc:google" -pm -ds

# Multi-threading para consultas DNS com verbose warning
docker run --rm -v $(pwd):/dados string-x -l /dados/dominios.txt -st "dig {STRING}" -t 20 -v 2

# Extrair, validar e salvar emails com verbose completo
docker run --rm -v $(pwd):/dados string-x -l /dados/texto.txt -module "ext:email" -pm -o /dados/emails.csv -v all

# Conectar ao MySQL container
docker run --rm -v $(pwd):/dados string-x -l /dados/dominios.txt -module "con:mysql" -pm

# Enviar dados para OpenSearch
docker run --rm -v $(pwd):/dados string-x -l /dados/resultados.txt -module "con:opensearch" -pm
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

## Sistema de Verbosidade

String-X oferece 5 níveis de verbosidade para controle granular da saída:

| Nível | Descrição | Uso Recomendado |
|-------|-----------|-----------------|
| `-v 1` | **Info**: Informações básicas | Operações normais |
| `-v 2` | **Warning**: Avisos e alertas | Detecção de problemas |
| `-v 3` | **Debug**: Informações detalhadas | Debugging e desenvolvimento |
| `-v 4` | **Error**: Apenas erros críticos | Monitoramento de falhas |
| `-v 5` | **Exception**: Exceções e stack traces | Análise profunda de erros |
| `-v all` | **Todos**: Combinação de todos os níveis | Debug completo |

```bash
# Exemplos de uso com diferentes níveis
docker run --rm string-x -s "test.com" -st "dig {STRING}" -v 1    # Info básica
docker run --rm string-x -s "test.com" -st "dig {STRING}" -v 3    # Debug detalhado
docker run --rm string-x -s "test.com" -st "dig {STRING}" -v all  # Verbose completo
```

## Sistema de Segurança

String-X inclui validações de segurança para prevenir execução de comandos maliciosos:

```bash
# Comando normal (validação ativa)
docker run --rm string-x -s "test.com" -st "echo {STRING}"

# Comando complexo que pode ser bloqueado
docker run --rm string-x -s "test.com" -st "echo {STRING}; cat /etc/passwd"

# Bypass de segurança quando necessário (use com cuidado)
docker run --rm string-x -s "test.com" -st "complex_cmd && other {STRING}" -ds

# Troubleshooting com verbose + bypass
docker run --rm string-x -s "test.com" -st "comando_complexo {STRING}" -ds -v 3
```

⚠️ **Aviso**: Use `-ds` apenas quando necessário e em ambientes controlados.

## Dicas e Otimizações

### Alias para facilitar o uso

Adicione ao seu `.bashrc` ou `.zshrc`:

```bash
# Alias para String-X Docker
alias strx-docker='docker run --rm -v $(pwd):/dados -i string-x'

# Alias com verbose padrão
alias strx-debug='docker run --rm -v $(pwd):/dados -i string-x -v 3'

# Alias para operações inseguras (bypass)
alias strx-unsafe='docker run --rm -v $(pwd):/dados -i string-x -ds'

# Uso simplificado
strx-docker -l /dados/alvos.txt -st "ping -c 1 {STRING}"

# Debug simplificado
strx-debug -l /dados/alvos.txt -module "ext:domain" -pm
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
