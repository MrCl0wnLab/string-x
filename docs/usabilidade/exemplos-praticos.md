# Exemplos Práticos

Este documento apresenta exemplos práticos de uso do String-X para diversas situações comuns, desde tarefas básicas até cenários mais avançados.

## Exemplos Básicos

### 1. Processamento de uma única string com o parâmetro -s

```bash
# Extrair endereços IP de um domínio
./strx -s "example.com" -st "dig +short {STRING}"

# Fazer uma requisição HTTP
./strx -s "https://example.com" -st "curl -I {STRING}"

# Executar nmap em um único host
./strx -s "192.168.1.1" -st "nmap -p 80,443 {STRING}"
```

Para mais exemplos de uso do parâmetro `-s`, veja [Exemplos com Strings Únicas](exemplos-string-unica.md).

### 2. Processamento em lote a partir de um arquivo

```bash
# Verificar status HTTP de múltiplos sites
./strx -l sites.txt -st "curl -s -o /dev/null -w '%{http_code}' {STRING}" -t 10
```

### 3. Processamento com pipe (stdin)

```bash
# Extrair subdomínios a partir de uma lista
cat dominios.txt | ./strx -st "subfinder -d {STRING} -silent" -o subdomains.txt
```

## Exemplos com Módulos

### 1. Utilização de um único módulo

```bash
# Extrair emails de múltiplos sites
./strx -l sites.txt -module "ext:email" -pm -o emails.txt
```

### 2. Encadeamento de módulos

O String-X suporta encadeamento de módulos com o caractere pipe (`|`), permitindo que a saída de um módulo seja processada pelo próximo na cadeia.

```bash
# Extrair domínios e verificar informações DNS
./strx -l urls.txt -module "ext:url|ext:domain|clc:dns" -pm -format json -o resultados.json

# Extrair e validar diferentes tipos de dados
./strx -l arquivo.txt -module "ext:email|ext:url|ext:ip" -pm -verbose

# Coletando informações de diferentes fontes
./strx -s "exemplo.com" -module "clc:subdomain|clc:whois|clc:dns" -pm
```

Para mais informações sobre encadeamento de módulos, consulte [Encadeamento de Módulos](encadeamento-modulos.md).

### 3. Módulos com parâmetros específicos

```bash
# Busca no Shodan com limite de resultados
./strx -l ips.txt -module "clc:shodan" -pm -api-key "SUA_API_KEY" -limit 50 -o shodan_results.json
```

## Exemplos com Saída Personalizada

### 1. Formatação específica

```bash
# Saída em formato CSV
./strx -l domains.txt -st "dig +short {STRING}" -format csv -o resultados.csv
```

### 2. Filtragem com pipe

```bash
# Filtragem de resultados
./strx -l urls.txt -st "curl -s {STRING}" -p "grep -o 'href=\"[^\"]*\"'" -o links.txt
```

### 3. Saída para banco de dados

```bash
# Salvar resultados no MySQL
./strx -l subdomains.txt -st "nmap -sV {STRING}" -module "out:mysql" -pm \
  -host localhost -port 3306 -username user -password pass -database recon -table nmap_results
```

## Exemplos de OSINT e Reconhecimento

### 1. Enumeração de subdomínios

```bash
# Coleta básica de subdomínios
./strx -s "empresa.com" -module "clc:subdomain" -pm -o subdomains.txt
```

### 2. Busca combinada em múltiplos serviços

```bash
# Busca em múltiplos serviços OSINT
./strx -s "alvo.com" -module "clc:crtsh|clc:duckduckgo|clc:virustotal" -pm -o osint_results.json -format json
```

### 3. Reconhecimento completo

```bash
# Pipeline completo de reconhecimento
./strx -s "alvo.com" -module "clc:subdomain" -pm -o subdomains.txt
./strx -l subdomains.txt -st "dig +short {STRING}" -o ips.txt
./strx -l ips.txt -st "nmap -sV -p- {STRING}" -o nmap_results.txt -t 5
```

## Exemplos de Análise de Dados

### 1. Extração de padrões

```bash
# Extrair hashes de arquivos
./strx -l arquivos.txt -st "sha256sum {STRING}" -module "ext:hash" -pm -o hashes.txt
```

### 2. Validação de dados

```bash
# Validar emails em uma lista
./strx -l emails_suspeitos.txt -module "ext:email" -pm -o emails_validos.txt
```

### 3. Processamento e transformação

```bash
# Converter URLs para seus respectivos IPs
./strx -l urls.txt -module "ext:domain|ext:ip" -pm -format json -o dominios_ips.json
```

## Exemplos Avançados

### 1. Multi-threading com controle de tempo

```bash
# Varredura com controle de tempo e threads
./strx -l alvos.txt -st "nmap -T4 -p 80,443,8080 {STRING}" -t 20 -sleep 0.5 -timeout 120 -o scan_results.txt
```

### 2. Processos resilientes com retry

```bash
# Coleta com retry em caso de falha
./strx -l apis.txt -st "curl -s {STRING}" -retry 5 -retry-delay 2 -o api_results.txt
```

### 3. Processamento com configuração de proxy

```bash
# Requisições através de proxy
./strx -l sites.txt -st "curl -s {STRING}" -proxy "http://127.0.0.1:8080" \
  -user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -o resultados_via_proxy.txt
```

## Exemplos para Testes de Segurança

### 1. Detecção de vulnerabilidades básicas

```bash
# Teste de SQL Injection básico
./strx -l urls.txt -st "curl -s '{STRING}?id=1%27'" -p "grep -i 'error\\|sql\\|syntax'" -o sqli_candidates.txt
```

### 2. Fuzzing de endpoints

```bash
# Fuzzing básico de endpoints
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://alvo.com/{STRING}" \
  -t 20 -o endpoints_status.txt
```

### 3. Coleta e análise de cabeçalhos de segurança

```bash
# Verificar cabeçalhos de segurança
./strx -l sites.txt -st "curl -s -I {STRING}" -p "grep -i 'content-security\\|x-xss\\|strict-transport'" \
  -o security_headers.txt
```

## Exemplos com Integração AI

### 1. Análise de texto com OpenAI

```bash
# Análise de conteúdo com GPT
./strx -l textos.txt -module "ai:openai" -pm -api-key "SUA_API_KEY" -o analises.json -format json
```

### 2. Análise de texto com Gemini

```bash
# Análise de conteúdo com Gemini
./strx -l textos.txt -module "ai:gemini" -pm -api-key "SUA_API_KEY" -o analises.json -format json
```

## Exemplos de Workflow Completo

### 1. Reconhecimento e análise

```bash
# Pipeline completo: reconhecimento, coleta e análise
./strx -s "empresa.com" -module "clc:subdomain" -pm -o subdomains.txt
./strx -l subdomains.txt -st "httpx -silent -status-code" -o live_subdomains.txt
./strx -l live_subdomains.txt -st "nuclei -silent -severity critical,high" -o vulnerabilities.txt
./strx -l vulnerabilities.txt -module "ai:openai" -pm -api-key "SUA_API_KEY" -o report.md
```

### 2. Coleta, processamento e armazenamento

```bash
# Coleta de dados, processamento e armazenamento em banco
./strx -s "empresa.com" -module "clc:google" -pm -limit 100 -o google_results.txt
./strx -l google_results.txt -module "ext:url|ext:domain" -pm -o processed_domains.txt
./strx -l processed_domains.txt -module "out:mysql" -pm \
  -host localhost -username user -password pass -database osint -table domains
```
