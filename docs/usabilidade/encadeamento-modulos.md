# Encadeamento de Módulos

O String-X suporta o encadeamento de múltiplos módulos utilizando o caractere pipe (`|`). Esta funcionalidade permite processar dados através de uma sequência de módulos, onde a saída de um módulo serve como entrada para o próximo.

## Sintaxe

```bash
./strx -l arquivo.txt -st "comando {STRING}" -module "tipo1:nome1|tipo2:nome2|tipo3:nome3" -pm
```

## Como Funciona

1. O String-X executa o primeiro módulo (`tipo1:nome1`) com os dados iniciais
2. O resultado deste módulo é passado como entrada para o segundo módulo (`tipo2:nome2`)
3. O processo continua até que todos os módulos na cadeia sejam executados
4. O resultado final é a saída do último módulo

## Exemplos

### Extração de URLs e Domínios

Extrair URLs e depois extrair os domínios dessas URLs:

```bash
./strx -l conteudo.txt -st "echo {STRING}" -module "ext:url|ext:domain" -pm
```

### Reconhecimento Completo

Extrair domínios, obter informações DNS e verificar se os hosts estão ativos:

```bash
./strx -l urls.txt -st "echo {STRING}" -module "ext:url|ext:domain|clc:dns|clc:http_probe" -pm
```

### Verificação de Disponibilidade Web

Extrair URLs e verificar a disponibilidade e informações dos servidores HTTP:

```bash
./strx -l sites.txt -st "echo {STRING}" -module "ext:domain|clc:http_probe" -pm
```

### OSINT Multi-Fonte

Coletar dados de múltiplas fontes OSINT em sequência:

```bash
./strx -s "alvo.com" -st "echo {STRING}" -module "clc:crtsh|clc:virustotal|clc:subdomain" -pm
```

## Considerações

- Se um módulo na cadeia não retornar resultados, o encadeamento é interrompido
- Cada módulo deve ser capaz de processar o tipo de dados fornecido pelo módulo anterior
- Para melhor visibilidade do processo, use a flag `-verbose`

## Casos de Uso Avançados

### Transformação e Filtragem

```bash
# Extrair emails, validá-los e verificar reputação
./strx -l texto.txt -st "echo {STRING}" -module "ext:email|ext:validation|clc:reputation" -pm
```

### Processamento e Análise

```bash
# Extrair subdomínios, verificar status HTTP e coletar cabeçalhos de segurança
./strx -s "example.com" -st "echo {STRING}" -module "clc:subdomain|clc:http_probe" -pm
```

O módulo `http_probe` coleta automaticamente informações como:

- Status HTTP (200, 404, 500, etc.)
- Título da página
- Servidor web utilizado
- Redirecionamentos
- Cabeçalhos de segurança
- Endereço IP do servidor
