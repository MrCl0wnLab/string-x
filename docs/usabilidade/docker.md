# Utilização com Docker

Este documento explica como utilizar o String-X através dos contêineres Docker disponíveis, simplificando sua instalação e execução em qualquer ambiente.

## Imagens Docker Disponíveis

O String-X oferece três opções principais de imagens Docker:

1. **String-X Base**: Contêiner com apenas o String-X e suas dependências básicas
2. **String-X Completo**: Contêiner com o String-X e ferramentas adicionais para reconhecimento
3. **String-X com Banco de Dados**: Inclui o String-X conectado a serviços de armazenamento (MySQL ou OpenSearch)

## Instalação

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (para configurações multi-contêiner)

### String-X Standalone

Para usar apenas a imagem básica do String-X:

```bash
# Baixar a imagem
docker pull osintbrazuca/string-x:latest

# Verificar a instalação
docker run --rm osintbrazuca/string-x:latest -version
```

## Utilização Básica

### Execução de Comandos Simples

```bash
# Executar o String-X com uma única string
docker run --rm osintbrazuca/string-x:latest -s "example.com" -st "dig +short {STRING}"

# Processar um arquivo local (montando um volume)
docker run --rm -v $(pwd):/data osintbrazuca/string-x:latest -l /data/dominios.txt -st "dig +short {STRING}" -o /data/resultados.txt
```

### Variáveis de Ambiente

É possível configurar o String-X através de variáveis de ambiente:

```bash
docker run --rm \
  -e STRX_THREADS=10 \
  -e STRX_TIMEOUT=30 \
  -e STRX_FORMAT=json \
  osintbrazuca/string-x:latest -l /data/dominios.txt -st "dig +short {STRING}"
```

## String-X Docker Compose

Para configurações mais complexas, use o Docker Compose disponível em `docker/strx-docker-compose`.

### Configuração

1. Clone o repositório do String-X:

```bash
git clone https://github.com/osintbrazuca/string-x.git
cd string-x/docker/strx-docker-compose
```

2. Edite o arquivo `.env` com suas configurações:

```
STRX_THREADS=10
STRX_TIMEOUT=30
MYSQL_ROOT_PASSWORD=sua_senha_segura
MYSQL_DATABASE=strx_db
```

3. Inicie os contêineres:

```bash
docker-compose up -d
```

### Utilização com Docker Compose

#### Executando o String-X

```bash
# Executar comando diretamente no contêiner
docker-compose exec strx -s "example.com" -module "clc:dns" -pm

# Processar arquivo local
docker-compose exec strx -l /data/alvos.txt -st "ping -c 1 {STRING}" -o /data/resultados.txt
```

#### Armazenamento no MySQL

O Docker Compose configura automaticamente a integração com MySQL:

```bash
# Coletar dados e armazenar diretamente no MySQL
docker-compose exec strx -l /data/dominios.txt -module "clc:subdomain|con:mysql" -pm
```

Acesse o PHPMyAdmin em `http://localhost:8080` para visualizar os resultados armazenados.

## String-X com OpenSearch

Para utilização com o OpenSearch, use o Docker Compose disponível em `docker/opensearch-docker-compose`.

### Configuração do OpenSearch

1. Navegue até o diretório do Docker Compose do OpenSearch:

```bash
cd string-x/docker/opensearch-docker-compose
```

2. Inicie os serviços:

```bash
docker-compose up -d
```

3. Verifique se os serviços estão funcionando:

```bash
# Verifique se o OpenSearch está respondendo
curl -X GET "http://localhost:9200"

# Verifique se o OpenSearch Dashboards está acessível
# Acesse http://localhost:5601 no navegador
```

### Utilização com OpenSearch

```bash
# Executar o String-X salvando resultados no OpenSearch
docker run --rm --network=host osintbrazuca/string-x:latest \
  -l dominios.txt -module "clc:subdomain|out:opensearch" -pm \
  -host localhost -port 9200 -index strx-domains
```

Acesse o OpenSearch Dashboards em `http://localhost:5601` para visualizar e analisar os dados coletados.

## Casos de Uso Avançados

### 1. Ambiente de Reconhecimento Completo

Utilize o Docker Compose para criar um ambiente completo de reconhecimento:

```yaml
# docker-compose.yml
version: '3'
services:
  strx:
    image: osintbrazuca/string-x:latest
    volumes:
      - ./dados:/data
    depends_on:
      - db
      - opensearch
    environment:
      - STRX_THREADS=20
      - STRX_TIMEOUT=60
  
  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=strx_data
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
  
  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    ports:
      - "8080:80"
    environment:
      - PMA_HOST=db
    depends_on:
      - db
  
  opensearch:
    image: opensearchproject/opensearch:latest
    environment:
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
      - "DISABLE_SECURITY_PLUGIN=true"
    ports:
      - "9200:9200"
    volumes:
      - opensearch_data:/usr/share/opensearch/data
  
  dashboards:
    image: opensearchproject/opensearch-dashboards:latest
    ports:
      - "5601:5601"
    environment:
      - OPENSEARCH_HOSTS=["http://opensearch:9200"]
      - "DISABLE_SECURITY_DASHBOARDS_PLUGIN=true"
    depends_on:
      - opensearch

volumes:
  mysql_data:
  opensearch_data:
```

### 2. Automatização com Cron

Configure um contêiner para executar tarefas programadas do String-X:

```Dockerfile
FROM osintbrazuca/string-x:latest

# Instalar cron
RUN apt-get update && apt-get install -y cron

# Adicionar trabalhos cron
COPY crontab /etc/cron.d/strx-cron
RUN chmod 0644 /etc/cron.d/strx-cron && \
    crontab /etc/cron.d/strx-cron

# Script de inicialização
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
```

Arquivo `crontab`:
```
# Executar coleta diária às 03:00
0 3 * * * /usr/local/bin/strx -l /data/alvos.txt -module "clc:subdomain|con:mysql" -pm >> /data/logs/coleta_diaria.log 2>&1
```

Arquivo `start.sh`:
```bash
#!/bin/bash
cron
tail -f /dev/null
```

## Dicas e Melhores Práticas

### Volumes e Persistência

Sempre use volumes Docker para garantir persistência de dados:

```bash
docker run --rm -v $(pwd)/data:/data -v $(pwd)/config:/etc/strx/config \
  osintbrazuca/string-x:latest -c /etc/strx/config/config.yaml -l /data/alvos.txt
```

### Redes Docker

Para comunicação entre contêineres, use redes Docker definidas:

```bash
# Criar rede
docker network create strx-network

# Executar MySQL na rede
docker run -d --name strx-mysql --network strx-network \
  -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=strx \
  mysql:8.0

# Executar String-X na mesma rede
docker run --rm --network strx-network \
  osintbrazuca/string-x:latest -l alvos.txt -module "clc:subdomain|con:mysql" -pm \
  -host strx-mysql -port 3306 -username root -password password -database strx
```

### Segurança

- Evite armazenar credenciais diretamente nos comandos Docker
- Use arquivos de ambiente (`.env`) ou o Docker Secrets para gerenciar credenciais
- Considere limitar os recursos disponíveis para os contêineres:

```bash
docker run --rm --cpus=2 --memory=2g osintbrazuca/string-x:latest -l alvos.txt -st "nmap -T4 {STRING}"
```

## Resolução de Problemas

### Erro de Permissão em Volumes

Se encontrar erros de permissão ao gravar em volumes montados:

```bash
# Corrigir permissões antes de montar o volume
mkdir -p data && chmod 777 data
docker run --rm -v $(pwd)/data:/data osintbrazuca/string-x:latest -l alvos.txt -o /data/resultados.txt
```

### Problemas de Rede em Docker Compose

Se os serviços não conseguirem se comunicar:

```bash
# Verificar redes configuradas
docker-compose ps
docker network ls

# Reiniciar os serviços
docker-compose down
docker-compose up -d
```

### Logs e Debugging

Para visualizar logs detalhados:

```bash
# Ver logs do contêiner
docker logs <container_id>

# Executar com modo de debug
docker run --rm osintbrazuca/string-x:latest -debug -s "example.com" -st "dig {STRING}"
```
