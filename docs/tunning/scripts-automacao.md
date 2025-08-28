# Scripts de Automação

Este documento apresenta técnicas e exemplos para automatizar fluxos de trabalho utilizando o String-X, permitindo operações programadas, processos em lote e integração com outras ferramentas.

## Fundamentos de Automação

A automação com o String-X pode ser implementada em vários níveis:

1. **Scripts de Shell** - Combinando o String-X com comandos do sistema
2. **Scripts Python** - Utilizando a API do String-X em código Python
3. **Agendadores de Tarefas** - Execução programada de comandos
4. **Pipelines** - Integração em fluxos de trabalho maiores
5. **Webhooks e Triggers** - Execução baseada em eventos

## Scripts de Shell

### Estrutura Básica

Um script de shell básico para automação com o String-X:

```bash
#!/bin/bash

# Configurações
INPUT_FILE="targets.txt"
OUTPUT_DIR="results_$(date +%Y%m%d)"
THREADS=10

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Executar String-X
echo "[+] Iniciando processamento em $(date)"
./strx -l "$INPUT_FILE" -st "comando {STRING}" -t "$THREADS" -o "$OUTPUT_DIR/output.txt"
echo "[+] Processamento concluído em $(date)"

# Processar resultados
echo "[+] Analisando resultados..."
grep "success" "$OUTPUT_DIR/output.txt" > "$OUTPUT_DIR/successful.txt"
grep "error" "$OUTPUT_DIR/output.txt" > "$OUTPUT_DIR/errors.txt"

# Relatório
echo "[+] Resumo:"
echo "- Total de alvos: $(wc -l < "$INPUT_FILE")"
echo "- Sucessos: $(wc -l < "$OUTPUT_DIR/successful.txt")"
echo "- Erros: $(wc -l < "$OUTPUT_DIR/errors.txt")"
```

### Processamento em Lote

Script para processar grandes arquivos em lotes menores:

```bash
#!/bin/bash

# Configurações
INPUT_FILE="huge_list.txt"
BATCH_SIZE=1000
OUTPUT_DIR="batch_results"
THREADS=15

# Preparação
mkdir -p "$OUTPUT_DIR"
total_lines=$(wc -l < "$INPUT_FILE")
batch_count=$(( (total_lines + BATCH_SIZE - 1) / BATCH_SIZE ))

echo "[+] Processando $total_lines linhas em $batch_count lotes"

# Dividir em lotes
split -l "$BATCH_SIZE" "$INPUT_FILE" "$OUTPUT_DIR/batch_"

# Processar cada lote
for batch_file in "$OUTPUT_DIR"/batch_*; do
    batch_name=$(basename "$batch_file")
    echo "[+] Processando lote $batch_name"
    
    ./strx -l "$batch_file" -st "comando {STRING}" -t "$THREADS" -o "$OUTPUT_DIR/result_$batch_name.txt"
    
    echo "[+] Lote $batch_name concluído"
done

# Combinar resultados
cat "$OUTPUT_DIR"/result_batch_* > "$OUTPUT_DIR/combined_results.txt"

echo "[+] Todos os lotes processados. Resultados combinados disponíveis em $OUTPUT_DIR/combined_results.txt"
```

### Pipeline de Reconhecimento

Script completo para reconhecimento de domínio:

```bash
#!/bin/bash

# Configurações
TARGET_DOMAIN=$1
WORKSPACE="recon_${TARGET_DOMAIN}_$(date +%Y%m%d)"
THREADS=20

if [ -z "$TARGET_DOMAIN" ]; then
    echo "Uso: $0 dominio.com"
    exit 1
fi

# Preparação
mkdir -p "$WORKSPACE"
cd "$WORKSPACE" || exit

echo "[+] Iniciando reconhecimento para $TARGET_DOMAIN em $(date)"

# Fase 1: Enumeração de subdomínios
echo "[+] Fase 1: Enumeração de subdomínios"
../strx -s "$TARGET_DOMAIN" -module "clc:subdomain" -pm -t "$THREADS" -o "subdomains.txt"
echo "[+] Encontrados $(wc -l < subdomains.txt) subdomínios"

# Fase 2: Resolução DNS
echo "[+] Fase 2: Resolução DNS"
../strx -l "subdomains.txt" -st "dig +short {STRING}" -t "$THREADS" -o "ips.txt"
sort -u "ips.txt" > "unique_ips.txt"
echo "[+] Encontrados $(wc -l < unique_ips.txt) IPs únicos"

# Fase 3: Verificação de portas abertas
echo "[+] Fase 3: Verificação de portas abertas"
../strx -l "unique_ips.txt" -st "nmap -T4 -p 80,443,8080,8443 {STRING}" -t 10 -o "port_scan.txt"

# Fase 4: Captura de screenshots de sites ativos
echo "[+] Fase 4: Captura de screenshots"
mkdir -p "screenshots"
grep -E "80/open|443/open" "port_scan.txt" | cut -d' ' -f1 > "http_targets.txt"
../strx -l "http_targets.txt" -st "gowitness single http://{STRING}" -t 5

# Fase 5: Análise de vulnerabilidades
echo "[+] Fase 5: Análise de vulnerabilidades"
../strx -l "subdomains.txt" -st "nuclei -target {STRING} -severity critical,high" -t 5 -o "vulnerabilities.txt"

# Relatório final
echo "[+] Reconhecimento concluído em $(date)"
echo "[+] Resumo:"
echo "- Subdomínios: $(wc -l < subdomains.txt)"
echo "- IPs únicos: $(wc -l < unique_ips.txt)"
echo "- Alvos HTTP: $(wc -l < http_targets.txt)"
echo "- Vulnerabilidades: $(grep -c "CRITICAL\|HIGH" vulnerabilities.txt)"

echo "[+] Os resultados estão disponíveis em $(pwd)"
```

## Scripts Python

### Processamento Avançado

Script Python para processamento e análise avançada:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
import pandas as pd
from datetime import datetime
from strx.api import StringX
from strx.utils.helper.functions import normalize_domain

def parse_args():
    parser = argparse.ArgumentParser(description="Script de automação avançada com String-X")
    parser.add_argument("-t", "--target", required=True, help="Domínio alvo ou arquivo de alvos")
    parser.add_argument("-o", "--output", default="output", help="Diretório de saída")
    parser.add_argument("-threads", type=int, default=10, help="Número de threads")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout em segundos")
    return parser.parse_args()

def load_targets(target):
    """Carrega alvos de um arquivo ou retorna o alvo único"""
    if os.path.isfile(target):
        with open(target, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    else:
        return [target]

def process_targets(targets, output_dir, threads, timeout):
    """Processa alvos com o String-X"""
    strx = StringX()
    
    # Fase 1: Coleta de subdomínios
    print(f"[+] Coletando subdomínios para {len(targets)} domínios")
    subdomains = []
    for target in targets:
        result = strx.run_module("clc:subdomain", target, threads=threads, timeout=timeout)
        if result:
            subdomains.extend(result)
    
    # Salvar subdomínios
    subdomains = list(set(subdomains))
    with open(f"{output_dir}/subdomains.txt", 'w') as f:
        f.write("\n".join(subdomains))
    print(f"[+] Encontrados {len(subdomains)} subdomínios únicos")
    
    # Fase 2: Verificação de serviços HTTP
    print(f"[+] Verificando serviços HTTP")
    http_results = strx.run_module("clc:http_probe", subdomains, threads=threads, timeout=timeout)
    
    # Salvar resultados HTTP
    with open(f"{output_dir}/http_services.json", 'w') as f:
        json.dump(http_results, f, indent=2)
    
    # Converter para DataFrame para análise
    df = pd.DataFrame(http_results)
    
    # Análise de tecnologias
    tech_counts = {}
    for result in http_results:
        for tech in result.get('technologies', []):
            tech_counts[tech] = tech_counts.get(tech, 0) + 1
    
    # Salvar análise de tecnologias
    with open(f"{output_dir}/technologies.json", 'w') as f:
        json.dump(tech_counts, f, indent=2)
    
    # Relatório resumido
    with open(f"{output_dir}/summary.txt", 'w') as f:
        f.write(f"# Relatório de Reconhecimento\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Estatísticas\n")
        f.write(f"- Domínios alvo: {len(targets)}\n")
        f.write(f"- Subdomínios encontrados: {len(subdomains)}\n")
        f.write(f"- Serviços HTTP ativos: {len(http_results)}\n")
        f.write(f"- Tecnologias detectadas: {len(tech_counts)}\n\n")
        f.write(f"## Top 10 Tecnologias\n")
        for tech, count in sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            f.write(f"- {tech}: {count}\n")
    
    return {
        'subdomains': subdomains,
        'http_services': http_results,
        'technologies': tech_counts
    }

def main():
    args = parse_args()
    
    # Preparação
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    # Carregar alvos
    targets = load_targets(args.target)
    print(f"[+] Carregados {len(targets)} alvos")
    
    # Processamento principal
    start_time = datetime.now()
    results = process_targets(targets, output_dir, args.threads, args.timeout)
    end_time = datetime.now()
    
    # Relatório final
    duration = (end_time - start_time).total_seconds()
    print(f"[+] Processamento concluído em {duration:.2f} segundos")
    print(f"[+] Resultados salvos em {output_dir}")
    
    # Retornar resultados
    return results

if __name__ == "__main__":
    main()
```

## Agendamento de Tarefas

### Agendamento com Cron

Para execução programada no Linux/macOS:

```bash
# Editar crontab
crontab -e

# Adicionar entradas:

# Executar diariamente às 02:00
0 2 * * * cd /path/to/stringx && ./strx -l daily_targets.txt -st "comando {STRING}" -o /path/to/logs/daily_$(date +\%Y\%m\%d).log

# Executar semanalmente aos domingos
0 3 * * 0 cd /path/to/stringx && ./scripts/weekly_scan.sh >> /path/to/logs/weekly_scan.log 2>&1

# Executar mensalmente no primeiro dia do mês
0 4 1 * * cd /path/to/stringx && ./scripts/monthly_report.sh
```

### Agendamento com Systemd

Para sistemas Linux com systemd:

1. Criar arquivo de serviço:

```
# /etc/systemd/system/strx-daily.service
[Unit]
Description=String-X Daily Scan
After=network.target

[Service]
Type=oneshot
User=username
WorkingDirectory=/path/to/stringx
ExecStart=/path/to/stringx/scripts/daily_scan.sh
StandardOutput=append:/var/log/strx/daily.log
StandardError=append:/var/log/strx/daily.log
```

2. Criar arquivo de timer:

```
# /etc/systemd/system/strx-daily.timer
[Unit]
Description=Run String-X Daily Scan

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

3. Ativar o timer:

```bash
sudo systemctl enable strx-daily.timer
sudo systemctl start strx-daily.timer
```

## Integração com Outras Ferramentas

### Integração com Notificações

Script para enviar resultados por email ou mensagens:

```bash
#!/bin/bash

# Configurações
EMAIL="usuario@exemplo.com"
SLACK_WEBHOOK="https://hooks.slack.com/services/XXX/YYY/ZZZ"
TARGET_DOMAIN=$1
OUTPUT_FILE="scan_results.txt"

# Executar scan
echo "[+] Iniciando scan de $TARGET_DOMAIN"
./strx -s "$TARGET_DOMAIN" -module "clc:subdomain|clc:http_probe" -pm -o "$OUTPUT_FILE"

# Contar resultados
TOTAL_COUNT=$(wc -l < "$OUTPUT_FILE")
CRITICAL_COUNT=$(grep -c "CRITICAL" "$OUTPUT_FILE")

# Verificar se há alertas críticos
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    # Enviar por email
    SUBJECT="[ALERTA] Scan de $TARGET_DOMAIN encontrou $CRITICAL_COUNT problemas críticos"
    echo "Resultados do scan de $TARGET_DOMAIN" | mailx -s "$SUBJECT" -a "$OUTPUT_FILE" "$EMAIL"
    
    # Enviar para Slack
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"*ALERTA*: Scan de $TARGET_DOMAIN encontrou $CRITICAL_COUNT problemas críticos. Veja o relatório anexo.\"}" \
        "$SLACK_WEBHOOK"
else
    echo "[+] Scan concluído sem alertas críticos"
fi

echo "[+] Resultados disponíveis em $OUTPUT_FILE"
```

### Integração com Docker

Automação com Docker para ambiente isolado:

```bash
#!/bin/bash

# Configurações
TARGET=$1
OUTPUT_DIR="$(pwd)/results"

if [ -z "$TARGET" ]; then
    echo "Uso: $0 alvo.com"
    exit 1
fi

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Executar com Docker
docker run --rm \
    -v "$OUTPUT_DIR:/data" \
    osintbrazuca/string-x:latest \
    -s "$TARGET" \
    -module "clc:subdomain|clc:whois|clc:dns" \
    -pm -o "/data/$TARGET-results.json" -format json

echo "[+] Scan concluído. Resultados em $OUTPUT_DIR/$TARGET-results.json"
```

### Integração com CI/CD

Exemplo de configuração para GitLab CI/CD:

```yaml
# .gitlab-ci.yml
stages:
  - scan
  - analyze
  - report

variables:
  OUTPUT_DIR: "./results"

scan_job:
  stage: scan
  image: osintbrazuca/string-x:latest
  script:
    - mkdir -p $OUTPUT_DIR
    - ./strx -l targets.txt -module "clc:subdomain" -pm -o $OUTPUT_DIR/subdomains.json -format json
  artifacts:
    paths:
      - $OUTPUT_DIR/subdomains.json

analyze_job:
  stage: analyze
  image: osintbrazuca/string-x:latest
  script:
    - ./strx -l $OUTPUT_DIR/subdomains.json -module "clc:http_probe" -pm -o $OUTPUT_DIR/http_results.json -format json
  dependencies:
    - scan_job
  artifacts:
    paths:
      - $OUTPUT_DIR/http_results.json

report_job:
  stage: report
  image: python:3.9
  script:
    - pip install pandas matplotlib
    - python scripts/generate_report.py --input $OUTPUT_DIR/http_results.json --output $OUTPUT_DIR/report.html
  dependencies:
    - analyze_job
  artifacts:
    paths:
      - $OUTPUT_DIR/report.html
```

## Pipelines Avançados

### Pipeline de Monitoramento

Script para monitoramento contínuo de ativos:

```bash
#!/bin/bash

# Configurações
ASSETS_FILE="assets.txt"
PREVIOUS_RESULTS="previous_results.json"
CURRENT_RESULTS="current_results.json"
DIFF_RESULTS="diff_results.json"
NOTIFICATION_SCRIPT="./notify.sh"

# Executar coleta atual
echo "[+] Iniciando coleta de dados em $(date)"
./strx -l "$ASSETS_FILE" -module "clc:subdomain|clc:dns|clc:http_probe" -pm -format json -o "$CURRENT_RESULTS"

# Verificar se existem resultados anteriores
if [ -f "$PREVIOUS_RESULTS" ]; then
    echo "[+] Comparando com resultados anteriores"
    
    # Extrair novos subdomínios
    jq -r '.[] | select(.type=="subdomain") | .data' "$CURRENT_RESULTS" > current_subdomains.txt
    jq -r '.[] | select(.type=="subdomain") | .data' "$PREVIOUS_RESULTS" > previous_subdomains.txt
    
    # Encontrar diferenças
    comm -13 previous_subdomains.txt current_subdomains.txt > new_subdomains.txt
    comm -23 previous_subdomains.txt current_subdomains.txt > removed_subdomains.txt
    
    # Contar alterações
    NEW_COUNT=$(wc -l < new_subdomains.txt)
    REMOVED_COUNT=$(wc -l < removed_subdomains.txt)
    
    # Criar relatório de diferenças
    echo "{" > "$DIFF_RESULTS"
    echo "  \"date\": \"$(date -Iseconds)\"," >> "$DIFF_RESULTS"
    echo "  \"new_subdomains\": $(cat new_subdomains.txt | jq -R -s 'split("\n")[:-1]')," >> "$DIFF_RESULTS"
    echo "  \"removed_subdomains\": $(cat removed_subdomains.txt | jq -R -s 'split("\n")[:-1]')," >> "$DIFF_RESULTS"
    echo "  \"total_new\": $NEW_COUNT," >> "$DIFF_RESULTS"
    echo "  \"total_removed\": $REMOVED_COUNT" >> "$DIFF_RESULTS"
    echo "}" >> "$DIFF_RESULTS"
    
    # Notificar se houver alterações
    if [ "$NEW_COUNT" -gt 0 ] || [ "$REMOVED_COUNT" -gt 0 ]; then
        echo "[+] Detectadas alterações: $NEW_COUNT novos, $REMOVED_COUNT removidos"
        $NOTIFICATION_SCRIPT "$DIFF_RESULTS"
    else
        echo "[+] Nenhuma alteração detectada"
    fi
else
    echo "[+] Nenhum resultado anterior para comparar"
fi

# Backup dos resultados atuais para próxima execução
cp "$CURRENT_RESULTS" "$PREVIOUS_RESULTS"

echo "[+] Monitoramento concluído em $(date)"
```

### Pipeline de Análise de Vulnerabilidades

Script para análise automatizada de vulnerabilidades:

```bash
#!/bin/bash

# Configurações
TARGET_FILE="targets.txt"
OUTPUT_DIR="vuln_scan_$(date +%Y%m%d)"
SEVERITY="high,critical"
THREADS=10

# Preparação
mkdir -p "$OUTPUT_DIR"
echo "[+] Iniciando análise de vulnerabilidades em $(date)"

# Fase 1: Preparação de alvos
echo "[+] Fase 1: Preparação de alvos"
./strx -l "$TARGET_FILE" -module "ext:domain|ext:url" -pm -o "$OUTPUT_DIR/validated_targets.txt"

# Fase 2: Detecção de serviços
echo "[+] Fase 2: Detecção de serviços"
./strx -l "$OUTPUT_DIR/validated_targets.txt" -module "clc:http_probe" -pm -format json -o "$OUTPUT_DIR/live_services.json"

# Extrair URLs vivas
jq -r '.[] | select(.status_code >= 200 and .status_code < 500) | .url' "$OUTPUT_DIR/live_services.json" > "$OUTPUT_DIR/live_urls.txt"
echo "[+] Encontrados $(wc -l < "$OUTPUT_DIR/live_urls.txt") serviços ativos"

# Fase 3: Fingerprinting de tecnologias
echo "[+] Fase 3: Fingerprinting de tecnologias"
./strx -l "$OUTPUT_DIR/live_urls.txt" -st "whatweb -a 1 {STRING}" -t "$THREADS" -o "$OUTPUT_DIR/technologies.txt"

# Fase 4: Verificação de vulnerabilidades comuns
echo "[+] Fase 4: Verificação de vulnerabilidades"
./strx -l "$OUTPUT_DIR/live_urls.txt" -st "nuclei -target {STRING} -severity $SEVERITY -silent" -t "$THREADS" -o "$OUTPUT_DIR/vulnerabilities.txt"

# Fase 5: Análise e categorização
echo "[+] Fase 5: Análise de resultados"
grep -i "critical" "$OUTPUT_DIR/vulnerabilities.txt" > "$OUTPUT_DIR/critical_vulns.txt"
grep -i "high" "$OUTPUT_DIR/vulnerabilities.txt" > "$OUTPUT_DIR/high_vulns.txt"

# Contagens
TOTAL_TARGETS=$(wc -l < "$TARGET_FILE")
LIVE_SERVICES=$(wc -l < "$OUTPUT_DIR/live_urls.txt")
CRITICAL_VULNS=$(grep -c . "$OUTPUT_DIR/critical_vulns.txt")
HIGH_VULNS=$(grep -c . "$OUTPUT_DIR/high_vulns.txt")

# Criar relatório
cat << EOF > "$OUTPUT_DIR/report.md"
# Relatório de Análise de Vulnerabilidades

Data: $(date +%Y-%m-%d)

## Estatísticas

- Alvos analisados: $TOTAL_TARGETS
- Serviços ativos: $LIVE_SERVICES
- Vulnerabilidades críticas: $CRITICAL_VULNS
- Vulnerabilidades altas: $HIGH_VULNS

## Vulnerabilidades Críticas

$(cat "$OUTPUT_DIR/critical_vulns.txt")

## Vulnerabilidades Altas

$(cat "$OUTPUT_DIR/high_vulns.txt")

## Detalhes de Tecnologias

As principais tecnologias identificadas incluem:

$(grep -o '[A-Za-z0-9]\+\s\+\[[0-9]\+\]' "$OUTPUT_DIR/technologies.txt" | sort | uniq -c | sort -nr | head -10)

EOF

echo "[+] Análise concluída. Relatório disponível em $OUTPUT_DIR/report.md"
```

## Melhores Práticas

### Logging e Monitoramento

Sempre inclua logging adequado nos scripts:

```bash
#!/bin/bash

# Configuração de logging
LOG_FILE="automation.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Iniciando script"

# Funções de logging
log_info() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [INFO] $1"
}

log_error() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [ERROR] $1" >&2
}

log_success() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [SUCCESS] $1"
}

# Exemplo de uso
log_info "Preparando ambiente"

if ./strx -l targets.txt -st "comando {STRING}" -o results.txt; then
    log_success "Processamento concluído com sucesso"
else
    log_error "Falha no processamento"
    exit 1
fi

log_info "Script finalizado"
```

### Gestão de Erros

Implemente tratamento robusto de erros:

```bash
#!/bin/bash

# Configuração
set -e  # Encerrar em caso de erro
trap 'echo "Erro na linha $LINENO" >&2' ERR

# Função de limpeza
cleanup() {
    echo "Realizando limpeza..."
    rm -f temp_*.txt
    echo "Limpeza concluída"
}

# Registrar função para execução ao sair
trap cleanup EXIT

# Função para verificação de erro
check_error() {
    if [ $? -ne 0 ]; then
        echo "Erro ao executar: $1" >&2
        exit 1
    fi
}

# Uso em comandos
./strx -l targets.txt -st "comando {STRING}" -o results.txt
check_error "processamento de alvos"

# Continua apenas se o comando anterior foi bem-sucedido
echo "Processamento concluído com sucesso"
```

### Configuração Modular

Use arquivos de configuração para maior flexibilidade:

```bash
#!/bin/bash

# Carregar configurações
if [ -f "config.env" ]; then
    source config.env
else
    echo "Arquivo config.env não encontrado. Usando valores padrão." >&2
    # Valores padrão
    THREADS=5
    OUTPUT_DIR="results"
    TARGET_FILE="targets.txt"
fi

# Permitir sobrescrever via parâmetros
while getopts "t:o:d:f:" opt; do
    case $opt in
        t) THREADS="$OPTARG" ;;
        d) OUTPUT_DIR="$OPTARG" ;;
        f) TARGET_FILE="$OPTARG" ;;
        *) echo "Opção inválida: -$OPTARG" >&2; exit 1 ;;
    esac
done

echo "Usando configuração:"
echo "- Threads: $THREADS"
echo "- Output: $OUTPUT_DIR"
echo "- Targets: $TARGET_FILE"

# Executar com configurações
./strx -l "$TARGET_FILE" -st "comando {STRING}" -t "$THREADS" -o "$OUTPUT_DIR/output.txt"
```

## Automação em Ambientes Específicos

### Automação em Nuvem

Script para automação em ambientes AWS:

```bash
#!/bin/bash

# Configuração AWS
AWS_REGION="us-east-1"
S3_BUCKET="security-scans"
EC2_INSTANCE_ID="i-1234567890abcdef0"
SNS_TOPIC="arn:aws:sns:us-east-1:123456789012:SecurityAlerts"

# Configuração scan
TARGET_DOMAIN="example.com"
SCAN_ID="scan-$(date +%Y%m%d-%H%M%S)"
RESULTS_DIR="/tmp/$SCAN_ID"
RESULTS_FILE="$RESULTS_DIR/results.json"

# Criar diretório
mkdir -p "$RESULTS_DIR"

# Executar scan
echo "[+] Iniciando scan para $TARGET_DOMAIN"
./strx -s "$TARGET_DOMAIN" -module "clc:subdomain" -pm -format json -o "$RESULTS_FILE"

# Verificar resultados críticos
CRITICAL_COUNT=$(jq -r '.[] | select(.severity=="critical") | .id' "$RESULTS_FILE" | wc -l)

# Enviar resultados para S3
echo "[+] Enviando resultados para S3"
aws s3 cp "$RESULTS_FILE" "s3://$S3_BUCKET/$SCAN_ID/results.json"

# Notificação de resultados
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    MESSAGE="Scan $SCAN_ID encontrou $CRITICAL_COUNT problemas críticos em $TARGET_DOMAIN"
    aws sns publish --topic-arn "$SNS_TOPIC" --message "$MESSAGE" --region "$AWS_REGION"
    echo "[+] Alerta enviado: $MESSAGE"
fi

echo "[+] Scan concluído. ID: $SCAN_ID"
```

### Automação em Ambiente Corporativo

Script para integração com sistemas corporativos:

```bash
#!/bin/bash

# Configurações
JIRA_URL="https://jira.empresa.com"
JIRA_API_TOKEN="YOUR_API_TOKEN"
JIRA_PROJECT="SEC"
JIRA_ISSUE_TYPE="Task"

CONFLUENCE_URL="https://confluence.empresa.com"
CONFLUENCE_API_TOKEN="YOUR_API_TOKEN"
CONFLUENCE_SPACE="SECURITY"
CONFLUENCE_PAGE_TITLE="Security Scan Results"

# Função para criar issue no Jira
create_jira_issue() {
    local summary="$1"
    local description="$2"
    local priority="$3"
    
    curl -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $JIRA_API_TOKEN" \
        --data "{
            \"fields\": {
                \"project\": {
                    \"key\": \"$JIRA_PROJECT\"
                },
                \"summary\": \"$summary\",
                \"description\": \"$description\",
                \"issuetype\": {
                    \"name\": \"$JIRA_ISSUE_TYPE\"
                },
                \"priority\": {
                    \"name\": \"$priority\"
                }
            }
        }" \
        "$JIRA_URL/rest/api/2/issue"
}

# Função para atualizar página no Confluence
update_confluence_page() {
    local content="$1"
    
    # Obter ID da página
    PAGE_ID=$(curl -s -H "Authorization: Bearer $CONFLUENCE_API_TOKEN" \
        "$CONFLUENCE_URL/wiki/rest/api/content?title=$CONFLUENCE_PAGE_TITLE&spaceKey=$CONFLUENCE_SPACE" | \
        jq -r '.results[0].id')
    
    # Obter versão atual
    VERSION=$(curl -s -H "Authorization: Bearer $CONFLUENCE_API_TOKEN" \
        "$CONFLUENCE_URL/wiki/rest/api/content/$PAGE_ID" | \
        jq -r '.version.number')
    
    NEW_VERSION=$((VERSION + 1))
    
    # Atualizar página
    curl -X PUT \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $CONFLUENCE_API_TOKEN" \
        --data "{
            \"version\": {
                \"number\": $NEW_VERSION
            },
            \"title\": \"$CONFLUENCE_PAGE_TITLE\",
            \"type\": \"page\",
            \"body\": {
                \"storage\": {
                    \"value\": \"$content\",
                    \"representation\": \"wiki\"
                }
            }
        }" \
        "$CONFLUENCE_URL/wiki/rest/api/content/$PAGE_ID"
}

# Executar scan
echo "[+] Iniciando scan de segurança"
./strx -l "corporate_assets.txt" -module "clc:http_probe|clc:virustotal" -pm -format json -o "corporate_scan.json"

# Processar resultados
echo "[+] Analisando resultados"
HIGH_VULNS=$(jq -r '.[] | select(.severity=="high")' corporate_scan.json)
CRITICAL_VULNS=$(jq -r '.[] | select(.severity=="critical")' corporate_scan.json)

# Criar issues no Jira para vulnerabilidades críticas
if [ ! -z "$CRITICAL_VULNS" ]; then
    echo "[+] Criando issues no Jira para vulnerabilidades críticas"
    
    echo "$CRITICAL_VULNS" | jq -c '.' | while read -r vuln; do
        TARGET=$(echo "$vuln" | jq -r '.target')
        DESC=$(echo "$vuln" | jq -r '.description')
        
        create_jira_issue \
            "Vulnerabilidade Crítica em $TARGET" \
            "Detecção automática de vulnerabilidade crítica:\n\n$DESC" \
            "Highest"
    done
fi

# Gerar relatório para Confluence
echo "[+] Gerando relatório"
REPORT_DATE=$(date +"%Y-%m-%d %H:%M")
REPORT_CONTENT="h1. Relatório de Scan de Segurança\n\nData: $REPORT_DATE\n\n"
REPORT_CONTENT+="h2. Resumo\n\n"
REPORT_CONTENT+="* Alvos analisados: $(jq -r '.[] | .target' corporate_scan.json | sort | uniq | wc -l)\n"
REPORT_CONTENT+="* Vulnerabilidades críticas: $(echo "$CRITICAL_VULNS" | jq -r '.' | grep -c .)\n"
REPORT_CONTENT+="* Vulnerabilidades altas: $(echo "$HIGH_VULNS" | jq -r '.' | grep -c .)\n\n"

# Atualizar página no Confluence
echo "[+] Atualizando documentação no Confluence"
update_confluence_page "$REPORT_CONTENT"

echo "[+] Processo de automação concluído"
```

## Conclusão

A automação com o String-X permite criar fluxos de trabalho sofisticados e eficientes, integrando-se com outras ferramentas e sistemas para maximizar seu valor. Ao desenvolver scripts de automação, foque na modularidade, tratamento de erros e documentação clara para garantir que sejam fáceis de manter e expandir conforme suas necessidades evoluem.
