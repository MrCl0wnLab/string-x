# MySQL Docker para String-X

Este diretório contém a configuração do Docker para executar o MySQL como parte da infraestrutura do String-X.

## Características

- MySQL 8.0
- PHPMyAdmin para administração via web
- Estrutura simplificada de banco de dados compatível com o módulo MySQL do String-X
- Configuração otimizada para ambiente de desenvolvimento

## Requisitos

- Docker
- Docker Compose

## Uso

### Iniciar o contêiner MySQL:

```bash
cd docker/mysql-docker-compose
docker-compose up -d
```

### Verificar status:

```bash
docker ps | grep strx-mysql
```

### Acessar o MySQL via linha de comando:

```bash
docker exec -it strx-mysql mysql -u root -p
```

Quando solicitada, digite a senha: `Str1ngX_r00t!`

### Acessar o PHPMyAdmin:

Abra no navegador: http://localhost:8080

Credenciais:
- Servidor: mysql
- Usuário: root
- Senha: Str1ngX_r00t!

## Usando o módulo MySQL do String-X

O módulo MySQL já está configurado para funcionar com esta configuração. Por padrão, ele tentará se conectar a:

- Host: localhost
- Porta: 3306
- Banco: strx_db
- Usuário: strx_user
- Senha: Str1ngX_p4ss!

Exemplo de uso:

```bash
# Usando comando strx instalado
strx -l data.txt -st "echo {STRING}" -module "con:mysql" -pm

# Usando Python diretamente
python -m stringx.cli -l data.txt -st "echo {STRING}" -module "con:mysql" -pm

# Com verbose nível 3 para debug
strx -l data.txt -st "echo {STRING}" -module "con:mysql" -pm -v 3
```

## Segurança

As senhas incluídas neste arquivo são apenas para ambiente de desenvolvimento. Para produção:

1. Use variáveis de ambiente ou arquivos de segredos
2. Altere todas as senhas padrão
3. Limite o acesso à rede apenas aos serviços necessários
4. Configure backups automáticos

## Estrutura de tabelas

O script de inicialização `init/init.sql` cria uma única tabela simplificada:

- `results`: Armazena todos os resultados do processamento do String-X
  - `id`: Chave primária auto incremento
  - `data`: Conteúdo principal dos dados (TEXT)
  - `timestamp`: Data/hora automática da inserção
  - `module_type`: Tipo do módulo que gerou os dados
  - `processed_at`: Data/hora do processamento
  - `source`: Origem dos dados
  - `metadata`: Metadados adicionais em formato JSON

Esta estrutura é compatível com o módulo `con:mysql` existente no String-X.
