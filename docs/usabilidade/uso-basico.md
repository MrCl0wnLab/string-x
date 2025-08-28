# Uso Básico do String-X

Este guia cobre os conceitos básicos para começar a utilizar o String-X.

## Instalação

### Requisitos
- Python 3.12+
- Linux/MacOS
- Bibliotecas listadas em `requirements.txt`

### Instalação rápida

```bash
# Clone o repositório
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x

# Instale as dependências
pip install -r requirements.txt

# Torne o arquivo executável
chmod +x strx

# Teste a instalação com help
./strx -help
```

### Criando link simbólico (opcional)

```bash
# Verifique o link atual
ls -la /usr/local/bin/strx

# Se necessário, recrie o link
sudo rm /usr/local/bin/strx
sudo ln -sf $HOME/caminho/para/string-x/strx /usr/local/bin/strx
```

## Primeiros Comandos

### Verificar ajuda e informações

```bash
# Exibir ajuda geral
./strx -help

# Listar tipos de módulos disponíveis
./strx -types

# Listar módulos e exemplos de uso
./strx -examples

# Listar funções integradas
./strx -funcs
```

### Processando uma String

```bash
# Processar uma única string
./strx -s "exemplo.com" -st "echo Testando domínio: {STRING}"
```

### Processando um Arquivo

```bash
# Processar cada linha de um arquivo
./strx -l lista_dominios.txt -st "dig +short {STRING}"

# Salvar resultados em arquivo
./strx -l lista_dominios.txt -st "dig +short {STRING}" -o resultados.txt
```

### Usando entrada padrão (STDIN)

```bash
# Receber dados via pipe
cat dominios.txt | ./strx -st "whois {STRING}"

# Encadear comandos
echo "exemplo.com" | ./strx -st "dig +short {STRING}" | ./strx -st "whois {STRING}"
```

## Uso de Módulos

Os módulos são um componente central do String-X que fornecem funcionalidades específicas.

### Modo No-Shell (Recomendado) 🆕

O String-X agora oferece o modo no-shell que permite processamento **direto** através de módulos sem execução de comandos shell:

#### Benefícios:
- **🔒 Segurança Aprimorada**: Elimina riscos de injeção shell
- **⚡ Performance Superior**: Remove overhead de subprocessos
- **💡 Sintaxe Simplificada**: Não requer comandos wrapper

#### Sintaxe:

```bash
# ❌ Sintaxe Tradicional
./strx -l entrada.txt -st "echo {STRING}" -module "tipo:nome" -pm

# ✅ Sintaxe No-Shell (Recomendada)
./strx -l entrada.txt -st "{STRING}" -module "tipo:nome" -ns -pm
```

O parâmetro `-module` especifica qual módulo usar, no formato `tipo:nome`.
O parâmetro `-pm` (print module) indica que a saída do módulo deve ser exibida.
O parâmetro `-ns` (no-shell) ativa o processamento direto sem shell.

### Exemplos de uso de módulos

```bash
# ❌ Extração tradicional de emails
./strx -l texto.txt -st "echo {STRING}" -module "ext:email" -pm

# ✅ Extração no-shell de emails (Recomendada)
./strx -l texto.txt -st "{STRING}" -module "ext:email" -ns -pm

# ❌ Consulta tradicional no Google
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# ✅ Consulta no-shell no Google (Recomendada)
./strx -l dorks.txt -st "{STRING}" -module "clc:google" -ns -pm

# ❌ Encadeamento tradicional de módulos
./strx -l texto.txt -st "echo {STRING}" -module "ext:url|ext:domain|clc:dns" -pm

# ✅ Encadeamento no-shell de módulos (Recomendada)
./strx -l texto.txt -st "{STRING}" -module "ext:url|ext:domain|clc:dns" -ns -pm
```

## Multi-threading

Para acelerar o processamento, o String-X suporta execução multi-thread:

```bash
# Processar com 10 threads
./strx -l lista_grande.txt -st "curl -I {STRING}" -t 10

# Adicionar delay entre as requisições
./strx -l apis.txt -st "curl {STRING}" -t 5 -sleep 2
```

## Próximos Passos

- Explore os [Comandos Essenciais](comandos-essenciais.md) para aprender mais sobre as opções disponíveis
- Veja [Exemplos Práticos](exemplos-praticos.md) para casos de uso reais
- Consulte [Parâmetros](parametros.md) para uma descrição detalhada de todas as opções
