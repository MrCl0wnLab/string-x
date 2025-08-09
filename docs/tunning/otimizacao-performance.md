# Otimização de Performance

Este documento fornece técnicas e configurações para otimizar a performance do String-X em diferentes cenários e cargas de trabalho.

## Fundamentos de Performance

A performance do String-X depende de vários fatores:

1. **Tipo de Operação** - I/O-bound vs. CPU-bound
2. **Volume de Dados** - Quantidade de strings a processar
3. **Complexidade de Processamento** - Operações simples vs. complexas
4. **Recursos de Hardware** - CPU, memória, disco e rede disponíveis
5. **Configuração de Software** - Parâmetros e ajustes do String-X

## Otimização de Threading

O processamento paralelo através de threads é uma das formas mais eficazes de otimizar o String-X.

### Configuração Ideal de Threads

```bash
# Configuração básica de threads
./strx -l domains.txt -st "dig +short {STRING}" -t 10
```

O número ideal de threads depende de:

| Tipo de Operação | Fator Limitante | Threads Recomendadas |
|------------------|-----------------|----------------------|
| Rede (HTTP, DNS) | Latência de rede | 10-30× o número de núcleos |
| Processo externo | I/O do sistema | 5-10× o número de núcleos |
| Processamento de regex | CPU | 1-2× o número de núcleos |
| Operações de arquivo | I/O de disco | 2-4× o número de núcleos |

### Estratégias por Tipo de Operação

#### Operações de Rede

Para comandos ou módulos que dependem principalmente da rede:

```bash
# Ideal para consultas DNS, HTTP, etc.
./strx -l urls.txt -module "clc:http_probe" -pm -t 30 
```

#### Operações de CPU

Para comandos ou módulos que realizam processamento intensivo:

```bash
# Ideal para processamento de regex, análise de texto, etc.
./strx -l large_text.txt -module "ext:dns|ext:ip" -pm -t 4
```

#### Operações de I/O de Disco

Para comandos ou módulos que realizam muitas operações de arquivo:

```bash
# Ideal para operações de arquivo
./strx -l files.txt -st "exiftool {STRING}" -t 8 -sleep 0.1
```

### Ajuste Fino de Threading

Parâmetros adicionais para otimizar o uso de threads:

- **`-sleep`**: Adiciona um intervalo entre execuções para evitar sobrecarga
- **`-retry`**: Configura novas tentativas para operações que falham
- **`-retry-delay`**: Define o intervalo entre tentativas

```bash
# Configuração otimizada para APIs com rate limiting
./strx -l targets.txt -module "clc:shodan" -pm -t 10 -sleep 0.5 -retry 3
```

## Otimização de Memória

O gerenciamento eficiente de memória é crucial para processar grandes volumes de dados.

### Processamento em Lotes (Chunking)

Para arquivos muito grandes, divida-os em lotes menores:

```bash
# Dividir um arquivo grande em lotes de 1000 linhas
split -l 1000 huge_file.txt chunk_

# Processar cada lote separadamente
for chunk in chunk_*; do
  ./strx -l $chunk -st "comando {STRING}" -o results_$chunk.txt
done

# Combinar resultados
cat results_chunk_* > final_results.txt
```

### Controle de Buffer

Para resultados muito grandes, ajuste o buffer de saída:

```bash
# Reduzir uso de memória em resultados grandes
./strx -l domains.txt -module "clc:subdomain" -pm -o subdomains.txt
```

### Otimização de Módulos Específicos

Alguns módulos possuem parâmetros específicos para otimização de memória:

```bash
# Limitar resultados por consulta
./strx -l keywords.txt -module "clc:google" -pm

# Paginar resultados
./strx -l targets.txt -module "clc:yahoo" -pm
```

## Otimização de I/O

A entrada e saída de dados pode ser um gargalo significativo.

### Uso Eficiente de Arquivos

```bash
# Processar apenas as primeiras N linhas para teste
head -n 100 large_file.txt | ./strx -st "comando {STRING}"

# Amostrar linhas aleatórias
shuf -n 100 large_file.txt | ./strx -st "comando {STRING}"
```

### Formato de Saída Otimizado

Escolha o formato de saída mais eficiente para seu caso de uso:

- Use `txt` para saída mínima e rápida
- Use `csv` para compatibilidade com ferramentas de análise
- Evite `json` ou `xml` completos para grandes volumes de dados

```bash
# Formato otimizado para processamento linha a linha
./strx -l urls.txt -module "clc:http_probe" -pm -format json -o results.json
```

### Compressão de Saída

Para resultados muito grandes, use compressão:

```bash
# Compressão on-the-fly
./strx -l domains.txt -module "clc:subdomain" -pm -o - | gzip > subdomains.txt.gz

# Descompressão para processamento
zcat subdomains.txt.gz | ./strx -st "dig +short {STRING}" -o resolved.txt
```

## Otimização de Rede

Para operações que dependem de rede, a otimização da conectividade é essencial.

### Gerenciamento de Conexões

```bash
# Limitar número de conexões simultâneas
./strx -l urls.txt -module "clc:http_probe" -pm
```

### Uso de Proxy

Um proxy pode melhorar a performance em certos cenários:

```bash
# Proxy único
./strx -l urls.txt -st "curl {STRING}" -proxy "http://proxy:8080"
```

### Cache de DNS

Para operações com muitas consultas DNS:

```bash
# Cache de DNS
./strx -l domains.txt -st "dig +short {STRING}"
```

## Otimização para Hardware Específico

### Sistemas com Pouca Memória

```bash
# Configurações para sistemas com memória limitada
./strx -l urls.txt -st "comando {STRING}" -t 3
```

### Sistemas com Muitos Núcleos

```bash
# Maximizar uso em sistemas multicore
./strx -l targets.txt -st "comando {STRING}" -t 32
```

### Sistemas em Rede

```bash
# Otimizar para operação em rede com alta latência
./strx -l apis.txt -st "curl {STRING}" -t 50 -retry 5
```

## Técnicas Avançadas de Otimização

### Filtragem Precoce

Reduza o volume de dados o mais cedo possível no pipeline:

```bash
# Filtrar entradas antes do processamento principal
cat huge_list.txt | grep -E '\.com$|\.org$' | ./strx -st "comando {STRING}"
```


### Pipeline de Processamento Eficiente

Organize operações em ordem de eficiência crescente:

```bash
# Fluxo de processamento eficiente
./strx -l domains.txt -module "ext:domain|clc:http_probe" -pm
```

### Comparação de Configurações

```bash
# Script para comparar diferentes configurações
for t in 5 10 20 50; do
  echo "Testando com $t threads"
  time ./strx -l sample.txt -st "comando {STRING}" -t $t
done
```

### Análise de Gargalos

```bash
# Identificação de gargalos
./strx -v 3 -l sample.txt -st "comando {STRING}" 2>&1 | grep "TIMING"
```

## Cenários de Otimização Comuns

### 1. Processamento de Grande Volume de Domínios

```bash
# Otimização para milhões de domínios
./strx -l domains_huge.txt -module "ext:domain|clc:dns" -pm \
  -t 30 -retry 2 \
  -format json -o results.json
```

### 2. Varredura Rápida de Portas

```bash
# Otimização para scan de portas
./strx -l ips.txt -st "nmap -T4 -p- {STRING}" \
  -t 20 -p "grep -E 'open|filtered'" \
  -o open_ports.txt
```

### 3. Coleta Distribuída de OSINT

```bash
# Otimização para coleta OSINT
./strx -l targets.txt -module "clc:subdomain|clc:crtsh|clc:virustotal" -pm \
  -t 15 -sleep 1 -format json \
  -o osint_results.json
```

### 4. Processamento de Texto em Grande Escala

```bash
# Otimização para análise de texto em massa
./strx -l text_files.txt -st "cat {STRING}" -t 8 \
  -module "ext:email|ext:url|ext:ip|ext:hash" -pm \
  -format csv -o extracted_data.csv
```

## Limites e Considerações

### Limites de APIs e Serviços

Respeite os limites de taxa (rate limits) de APIs externas:

```bash
# Configuração consciente de limites de API
./strx -l targets.txt -module "clc:shodan" -pm \
  -sleep 1.2 
```

### Impacto em Sistemas Alvo

Considere o impacto das suas operações em sistemas alvo:

```bash
# Varredura gentil
./strx -l websites.txt -st "curl -s -o /dev/null -w '%{http_code}' {STRING}" \
  -t 5 -sleep 2
```

## Estratégias de Otimização por Caso de Uso

### Para Pentesting

```bash
# Configuração otimizada para testes de penetração
./strx -l targets.txt -module "ext:url|clc:http_probe|ext:domain" -pm \
  -t 20 -retry 2 -format json \
  -o pentest_targets.json
```

### Para Monitoramento Contínuo

```bash
# Configuração otimizada para monitoramento
./strx -l assets.txt -st "comando {STRING}" \
  -t 5 -sleep 1 -retry 3 \
  -o monitoring_log.txt
```

### Para Busca Forense

```bash
# Configuração otimizada para forense digital
./strx -l evidence.txt -module "ext:email|ext:hash|ext:credential" -pm \
  -t 8 -format csv -timestamp \
  -o forensic_findings.csv
```

## Conclusão

A otimização de performance do String-X envolve um equilíbrio entre velocidade, eficiência de recursos e confiabilidade. Experimente diferentes configurações para encontrar a combinação ideal para seu caso de uso específico, sempre considerando o impacto em sistemas externos e o uso responsável de recursos.
