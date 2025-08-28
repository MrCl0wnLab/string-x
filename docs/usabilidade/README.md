# Usabilidade do String-X

Esta seção fornece documentação detalhada sobre como utilizar efetivamente o String-X em diferentes cenários e com diversas configurações.

## Índice de Usabilidade

- [Uso Básico](uso-basico.md) - Primeiros passos com o String-X
- [Comandos Essenciais](comandos-essenciais.md) - Guia de referência rápida dos principais comandos
- [Parâmetros](parametros.md) - Descrição detalhada de todos os parâmetros disponíveis
- [Sistema de Segurança](seguranca.md) - Validações de segurança e parâmetro `-ds`
- [Níveis de Verbosidade](verbosidade.md) - Sistema de logging com 5 níveis detalhados
- [Exemplos Práticos](exemplos-praticos.md) - Casos de uso e exemplos do mundo real
- [Strings Únicas](strings-unicas.md) - Como usar o parâmetro `-s` para processar strings únicas
- [Encadeamento de Módulos](encadeamento-modulos.md) - Como encadear múltiplos módulos usando o caractere pipe (`|`)
- [Módulos](modulos/README.md) - Documentação detalhada dos módulos disponíveis
- [Docker](docker.md) - Instruções para uso do String-X em contêineres Docker

## Conceitos Fundamentais

O String-X baseia-se no conceito de processamento de strings através de um sistema de template que utiliza o placeholder `{STRING}`. Este sistema permite substituir dinamicamente valores em comandos, facilitando a automatização de tarefas repetitivas.

### {STRING} Template System

O núcleo do String-X é o sistema de template que utiliza `{STRING}` como palavra-chave para substituição dinâmica de valores. Este sistema permite processar cada linha de entrada individualmente, substituindo `{STRING}` pelo valor atual.

```bash
# Exemplo básico com arquivo de entrada contendo domínios
./strx -l dominios.txt -st "dig +short {STRING}"

# Exemplo com pipe do terminal
cat dominios.txt | ./strx -st "whois {STRING}"
```

### Multi-Threading

O String-X permite executar tarefas em paralelo utilizando threads, o que pode acelerar significativamente o processamento de grandes listas:

```bash
# Executar com 10 threads
./strx -l grandes-listas.txt -st "curl -I {STRING}" -t 10
```

### Pipe & Filter

O sistema de pipe e filter permite encadear múltiplos comandos e processar seus resultados:

```bash
# Filtrar resultados
./strx -l urls.txt -st "curl -s {STRING}" -p "grep '<title>'"
```

### Sistema de Segurança

O String-X inclui validações automáticas para proteger contra comandos maliciosos:

```bash
# Comandos seguros são executados normalmente
./strx -l data.txt -st "echo {STRING}"

# Comandos complexos podem ser executados desabilitando validações
./strx -l data.txt -st "echo {STRING}; md5sum {STRING}" -ds
```

### Verbosidade Granular

Sistema de logging com 5 níveis diferentes para controle preciso da saída:

```bash
# Informações básicas
./strx -l data.txt -st "process {STRING}" -v 1

# Debug completo
./strx -l data.txt -st "process {STRING}" -v 3

# Todos os níveis
./strx -l data.txt -st "process {STRING}" -v all
```

## Fluxo Básico de Uso

1. Defina sua fonte de dados (arquivo, string direta ou entrada padrão)
2. Escolha seu comando ou módulo para processamento
3. Configure opções como threads, filtros ou saída
4. Execute e analise os resultados

Para instruções mais detalhadas, consulte as páginas específicas listadas no índice.
