# OpenSearch para String-X

Este diretório contém a configuração Docker para executar o OpenSearch e o OpenSearch Dashboards como parte da infraestrutura do String-X. O OpenSearch é uma solução poderosa de busca e análise de dados que pode ser usado para armazenar, indexar e buscar grandes volumes de informações coletadas pela ferramenta String-X.

## Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Iniciando os Serviços](#iniciando-os-serviços)
- [Acessando o Dashboard](#acessando-o-dashboard)
- [Usando o Módulo OpenSearch](#usando-o-módulo-opensearch)
- [Exemplos Práticos](#exemplos-práticos)
- [Configurações Avançadas](#configurações-avançadas)
- [Resolução de Problemas](#resolução-de-problemas)

## Características

- **OpenSearch**: Motor de busca e análise de dados
- **OpenSearch Dashboards**: Interface web para visualização e gerenciamento
- **Configuração Single-Node**: Otimizado para desenvolvimento local
- **Docker Compose**: Fácil inicialização e configuração
- **Indexação Automática**: Compatível com o módulo out:opensearch do String-X

## Requisitos

- Docker e Docker Compose instalados
- Pelo menos 2GB de RAM disponível para os contêineres
- String-X com o módulo opensearch configurado
- Python 3.10+ com opensearch-py e httpx instalados

## Iniciando os Serviços

### Inicialização básica

```bash
# Navegar até o diretório do docker-compose
cd docker/opensearch-docker-compose

# Iniciar os serviços em background
docker-compose up -d
```

### Verificando o status

```bash
# Verificar se os contêineres estão rodando
docker ps | grep opensearch

# Verificar logs
docker logs opensearch-node1
docker logs opensearch-dashboards
```

### Parando os serviços

```bash
# Parar os serviços mantendo os volumes
docker-compose down

# Parar os serviços e remover volumes (apaga todos os dados)
docker-compose down -v
```

## Acessando o Dashboard

### Acesso à interface web

1. **Abra seu navegador** e acesse: https://localhost:5601
   
2. **Aceite o aviso de segurança** (certificado autoassinado)
   
3. **Faça login com as credenciais**:
   - Usuário: `admin`
   - Senha: `Str1ngX_p4ss!` (a senha deve ser definda internamente no modulo)



### Primeiros passos no Dashboard

1. **Criar um Index Pattern**:
   - Navegue até "Stack Management" > "Index Patterns"
   - Clique em "Create index pattern"
   - Digite o padrão `strx*` (ou o nome do índice usado)
   - Selecione `timestamp` como campo de tempo

2. **Explorar dados**:
   - Navegue até "Discover" no menu lateral
   - Selecione o índice criado para visualizar os dados
   - Use a barra de pesquisa para filtrar resultados

3. **Criar visualizações**:
   - Navegue até "Visualize" para criar gráficos, tabelas, etc.
   - Escolha o tipo de visualização e selecione o índice
   - Configure os campos e filtros desejados

## Usando o Módulo OpenSearch

O String-X inclui um módulo `con:opensearch` que permite enviar dados diretamente para o OpenSearch. Este módulo facilita a indexação de resultados para posterior análise e busca.

- `con:opensearch`: `utils/auxiliary/con/opensearch.py`

### Instalação de dependências

Antes de usar o módulo, certifique-se de que as dependências necessárias estão instaladas:

```bash
# Instalar dependências do módulo OpenSearch
pip install opensearch-py httpx
```

### Configuração do módulo

O módulo `con:opensearch` suporta as seguintes opções:

| Opção | Descrição | Valor Padrão |
|-------|-----------|--------------|
| `host` | Host do OpenSearch | `localhost` |
| `port` | Porta do OpenSearch | `9200` |
| `index` | Nome do índice | `strx-data` |
| `username` | Nome de usuário | `admin` |
| `password` | Senha do usuário | - |
| `use_ssl` | Usar conexão SSL | `true` |
| `verify_certs` | Verificar certificados SSL | `false` |
| `client_type` | Tipo de cliente ('low' ou 'high') | `high` |
| `data` | Dados a serem enviados | - |
| `verbose` | Nível de verbosidade (1-5 ou 'all') | `1` |
| `timeout` | Timeout da conexão (segundos) | `60` |
| `retry` | Tentativas de reconexão | `3` |
| `retry_delay` | Atraso entre tentativas (segundos) | `5` |

### Exemplos básicos de uso

**Exemplo 1**: Indexar URLs extraídas de um arquivo

```bash
# Extrair URLs de um arquivo e salvá-las no OpenSearch
strx -l arquivo.txt -st "echo {STRING}" -module "con:opensearch" -pm
```

**Exemplo 2**: Salvar resultados de busca do Google

```bash
# Realizar busca e salvar resultados
strx -l dorks.txt -st "echo {STRING}" -module "con:opensearch" -pm
```

**Exemplo 3**: Usando modo debug para verificar detalhes

```bash
# Modo verbose nível 3 para ver detalhes da operação
strx -l domains.txt -st "echo {STRING}" -module "con:opensearch" -pm -v 3
```

## Exemplos Práticos

### Pipeline completo de coleta e armazenamento

```bash
# Coletar subdomínios, validar e salvar no OpenSearch
strx -l targets.txt -st "echo {STRING}" -module "con:opensearch" -pm

# Com validação de segurança desabilitada para comandos complexos
strx -l targets.txt -st "complex_command && other_cmd {STRING}" -module "con:opensearch" -pm -ds

# Com verbose nível 4 para mostrar errors
strx -l targets.txt -st "echo {STRING}" -module "con:opensearch" -pm -v 4
```

### Busca e visualização de dados

Uma vez que os dados estejam no OpenSearch, você pode usar a interface do Dashboard para realizar buscas avançadas:

1. Abra o OpenSearch Dashboards (https://localhost:5601)
2. Vá para "Discover"
3. Use a linguagem KQL (Kibana Query Language) para filtrar:
   - `data.content: *gov*` - Busca por domínios governamentais
   - `module_type: "ext:email"` - Filtra por emails extraídos
   - `timestamp > now-1d` - Dados das últimas 24 horas

### Exportação de dados

Você também pode exportar os dados do Dashboard:

1. Faça sua busca em "Discover"
2. Clique em "Share" (Compartilhar) no canto superior direito
3. Selecione "CSV Reports" ou "PDF Reports"
4. Configure as opções e faça o download dos resultados

## Configurações Avançadas

### Aumentar recursos do OpenSearch

Para casos com grande volume de dados, edite o arquivo docker-compose.yml:

```yaml
opensearch-node1:
  # ...
  environment:
    # Aumentar memória para 4GB
    - "OPENSEARCH_JAVA_OPTS=-Xms4g -Xmx4g"
  # ...
```

### Ajuste de índices

Para otimizar o desempenho do OpenSearch para seu caso específico:

```bash
# Criar índice otimizado com configurações personalizadas
curl -k -X PUT "https://localhost:9200/strx-optimized" \
  -u "admin:Str1ngX_p4ss!" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": {
      "index": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "refresh_interval": "30s"
      }
    },
    "mappings": {
      "properties": {
        "data": {
          "dynamic": true,
          "properties": {
            "content": { "type": "text", "analyzer": "standard" }
          }
        }
      }
    }
  }'
```

## Resolução de Problemas

### OpenSearch não inicia

```bash
# Verificar logs detalhados
docker logs opensearch-node1

# Problema comum: falta de memória
# Solução: Aumentar memória disponível ou reduzir a alocação no docker-compose.yml
```

### Erro de conexão no módulo

Se o módulo `con:opensearch` apresentar erros de conexão:

1. Verifique se o OpenSearch está rodando: `docker ps | grep opensearch`
2. Teste conexão básica: `curl -k -u 'admin:Str1ngX_p4ss!' https://localhost:9200`
3. Verifique as configurações SSL (use_ssl=true e verify_certs=false para ambiente local)
4. Aumente o timeout: `-timeout 120` para redes lentas

### Erro de autenticação

```bash
# Redefinir senha do admin
docker exec opensearch-node1 /usr/share/opensearch/bin/opensearch-reset-password -u admin -p YourNewPassword
```

### Dashboard não carrega

```bash
# Verifique se o Dashboard está rodando
docker logs opensearch-dashboards

# Reinicie o container se necessário
docker restart opensearch-dashboards
```
