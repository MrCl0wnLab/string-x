# Exemplos de Uso com Strings Únicas

A partir da versão mais recente, o String-X suporta o uso de strings únicas através do parâmetro `-s`. Esta funcionalidade permite executar comandos ou módulos em uma única string sem a necessidade de criar arquivos de entrada.

## Sintaxe

```bash
./strx -s "string_unica" -st "comando {STRING}"
```

## Exemplos

### Consultas DNS
```bash
# Consulta DNS simples
./strx -s "exemplo.com" -st "dig {STRING}"
```

### Requisições HTTP
```bash
# Fazer uma requisição HTTP
./strx -s "https://exemplo.com" -st "curl -I {STRING}"
```

### Extrair Informações
```bash
# Extrair email de uma string
./strx -s "email: user@gmail.com" -st "echo {STRING}" -module "ext:email" -pm
```

### Escaneamento
```bash
# Escanear um único host
./strx -s "192.168.1.25" -st "nmap -p 80,443 {STRING}"
```

### Usar Coletores
```bash
# Coletar informações de subdomínio
./strx -s "exemplo.com" -module "clc:subdomain" -pm
```

Para mais exemplos e detalhes, consulte a [documentação completa](docs/usabilidade/strings-unicas.md).
