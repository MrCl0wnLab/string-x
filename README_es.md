<center>

<h1 align="center">
  <br>
  🔧 String-X (STRX)
</h1>

<h4 align="center">Herramienta de Automatización para Manipulación de Strings</h4>

<p align="center">
Herramienta modular de automatización desarrollada para auxiliar analistas en OSINT, pentesting y análisis de datos a través de la manipulación dinámica de strings en líneas de comando Linux. Sistema basado en plantillas con procesamiento paralelo y módulos extensibles.
</p>

<p align="center">
  <a href="#/"><img src="https://img.shields.io/badge/python-3.12-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/Supported_OS-Linux-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/Supported_OS-Mac-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
</p>

<p align="center">
  <a href="https://github.com/MrCl0wnLab/string-x/blob/main/LICENSE"><img src="https://img.shields.io/github/license/MrCl0wnLab/string-x?color=blue"></a>
  <a href="https://github.com/MrCl0wnLab/string-x/graphs/contributors"><img src="https://img.shields.io/github/contributors-anon/MrCl0wnLab/string-x"></a>
  <a href="https://github.com/MrCl0wnLab/string-x/issues"><img src="https://img.shields.io/github/issues-raw/MrCl0wnLab/string-x"></a>
  <a href="https://github.com/MrCl0wnLab/string-x/network/members"><img src="https://img.shields.io/github/forks/MrCl0wnLab/string-x"></a>
  <img src="https://img.shields.io/github/stars/MrCl0wnLab/string-x.svg?style=social" title="Stars" /> 
</p>

</center>

## 📋 Índice

- [Características](#-características)
- [Instalación](#-instalación)
- [Conceptos Fundamentales](#-conceptos-fundamentales)
- [Arquitectura Modular](#-arquitectura-modular)
- [Uso de la Herramienta](#-uso-de-la-herramienta)
- [Ejemplos Prácticos](#-ejemplos-prácticos)
- [Funciones Integradas](#-funciones-integradas)
- [Sistema de Módulos](#-sistema-de-módulos)
- [Contribución](#-contribución)
- [Autor](#-autor)

## ✨ Características

- 🚀 **Procesamiento Paralelo**: Sistema de hilos configurable para alto rendimiento
- 🔧 **Arquitectura Modular**: Extensible a través de módulos EXT, CLC, OUT y CON
- 🔄 **Plantilla Dinámica**: Sistema de sustitución de strings con placeholder `{STRING}`
- 🛠️ **Funciones Integradas**: Funciones de hash, codificación, requests y generación de valores aleatorios
- 📁 **Múltiples Fuentes**: Soporte para archivos, stdin y pipes
- 🎯 **Filtrado Avanzado**: Sistema de filtros para procesamiento selectivo
- 💾 **Salida Flexible**: Guardado en archivos con timestamp automático

## 📦 INSTALACIÓN

### Requisitos
- Python 3.8+
- Linux/MacOS
- Librerías listadas en `requirements.txt`

### Instalación Rápida
```bash
# Clonar el repositorio
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x

# Instalar dependencias
pip install -r requirements.txt

# Hacer el archivo ejecutable
chmod +x strx

# Probar instalación
./strx --help
```

### Instalación vía Pip (próximamente)
```bash
pip install string-x
```

## 🧠 CONCEPTOS FUNDAMENTALES

### Sistema de Plantilla {STRING}
La herramienta utiliza el placeholder `{STRING}` como palabra clave para la sustitución dinámica de valores. Este sistema permite que cada línea de entrada sea procesada individualmente, reemplazando `{STRING}` por el valor actual.

```bash
# Archivo de entrada
host-01.com.br
host-02.com.br
host-03.com.br

# Comando con plantilla
./strx -l hosts.txt -st "host '{STRING}'"

# Resultado generado
host 'host-01.com.br'
host 'host-02.com.br'
host 'host-03.com.br'
```

### Flujo de Procesamiento
1. **Entrada**: Datos vía archivo (`-l`) o stdin (pipe)
2. **Plantilla**: Aplicación de la plantilla con `{STRING}`
3. **Procesamiento**: Ejecución de comandos/módulos
4. **Pipe**: Procesamiento adicional opcional (`-p`)
5. **Salida**: Resultado final (pantalla o archivo)

<center>

![Screenshot](/asset/fluxo.jpg)

</center>

## 🏗️ ARQUITECTURA MODULAR

String-X utiliza una arquitectura modular extensible con cuatro tipos principales de módulos:

### Tipos de Módulos

| Tipo | Código | Descripción | Ubicación |
|------|--------|-------------|-----------|
| **Extractor** | `ext` | Extracción de datos específicos (email, URL, domain, phone) | `utils/auxiliary/ext/` |
| **Collector** | `clc` | Recolección y agregación de información (DNS, whois) | `utils/auxiliary/clc/` |
| **Output** | `out` | Formateo y envío de resultados (DB, API, files) | `utils/auxiliary/out/` |
| **Connection** | `con` | Conexiones especializadas (SSH, FTP, etc) | `utils/auxiliary/con/` |

### Estructura de Directorios
```
string-x/
├── strx                    # Ejecutable principal
├── config/                 # Configuraciones globales
├── core/                   # Núcleo de la aplicación
│   ├── command.py         # Procesamiento de comandos
│   ├── auto_module.py     # Carga dinámica de módulos
│   ├── thread_process.py  # Sistema de hilos
│   ├── format.py          # Formateo y codificación
│   └── style_cli.py       # Interfaz CLI estilizada
└── utils/
    ├── auxiliary/         # Módulos auxiliares
    │   ├── ext/          # Módulos extractores
    │   ├── clc/          # Módulos recolectores
    │   ├── out/          # Módulos de salida
    │   └── con/          # Módulos de conexión
    └── helper/           # Funciones auxiliares
```

## 🚀 USO DE LA HERRAMIENTA

### Ayuda y Parámetros
```bash
./strx --help
```

### Parámetros Principales

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-h, --help`         |  Mostrar ayuda del proyecto | `-h` |
| `-types`             |  Lista tipos de módulos | `-types` |
| `-examples`          |  Lista módulos y ejemplos de uso | `-examples` |
| `-functions, -funcs` |  Lista funciones | `-funcs` |
| `-l, --list` | Archivo con strings para procesamiento | `-l hosts.txt` |
| `-st, --str` | Plantilla de comando con `{STRING}` | `-st "curl {STRING}"` |
| `-o, --out` | Archivo de salida para resultados | `-o results.txt` |
| `-p, --pipe` | Comando adicional vía pipe | `-p "grep 200"` |
| `-v, --verbose` | Modo verboso con detalles | `-v` |
| `-t, --thread` | Número de hilos paralelos | `-t 50` |
| `-f, --filter` | Filtro para selección de strings | `-f ".gov.br"` |
| `-module` | Selección de módulo específico | `-module "ext:email"` |
| `-pm` | Mostrar solo resultados del módulo | `-pm` |
| `-pf` | Mostrar solo resultados de funciones | `-pf` |
| `-of` | Guardar resultados de funciones en archivo | `-of` |
| `-sleep` | Retardo entre hilos (segundos) | `-sleep 2` |

### Interfaz de la Aplicación

```bash
usage: strx [-h] [-types] [-examples] [-functions] [-list file] [-str cmd] [-out file] 
            [-pipe cmd] [-verbose] [-thread <10>] [-pf] [-of] [-filter value] [-sleep <5>]
            [-module <type:module>] [-pm]

 
                                             _
                                            (T)          _
                                        _         .=.   (R)
                                       (S)   _   /\/(`)_         ▓
                                        ▒   /\/`\/ |\ 0`\      ░
                                        b   |░-.\_|_/.-||
                                        r   )/ |_____| \(    _
                            █               0  #/\ /\#  ░   (X)
                             ░                _| + o |_                ░
                             b         _     ((|, ^ ,|))               b
                             r        (1)     `||\_/||`                r  
                                               || _ ||      _
                                ▓              | \_/ ░     (V)
                                b          0.__.\   /.__.0   ░
                                r           `._  `"`  _.'           ▒
                                               ) ;  \ (             b
                                        ░    1'-' )/`'-1            r
                                                 0`     
                        
                              ██████    ▄▄▄█████▓    ██▀███     ▒██   ██▒ 
                            ▒██    ▒    ▓  ██▒ ▓▒   ▓██ ▒ ██▒   ░▒ █ █ ▒░
                            ░ ▓██▄      ▒ ▓██░ ▒░   ▓██ ░▄█ ▒   ░░  █   ░
                              ▒   ██▒   ░ ▓██▓ ░    ▒██▀▀█▄      ░ █ █ ▒ 
                            ▒██████▒▒     ▒██▒ ░    ░██▓ ▒██▒   ▒██▒ ▒██▒
                            ▒ ▒▓▒ ▒ ░     ▒ ░░      ░ ▒▓ ░▒▓░   ▒▒ ░ ░▓ ░
                            ░ ░▒  ░ ░       ░         ░▒ ░ ▒░   ░░   ░▒ ░
                            ░  ░  ░       ░           ░░   ░     ░    ░  
                                  ░                    ░         ░    ░  
                                  ░                                      
                                
                                String-X: Tool for automating commands

options:
             -h, --help             show this help message and exit
             -types                 Lista tipos de módulos
             -examples              Lista módulos e exemplos de uso
             -functions, -funcs     Lista funções
             -list, -l file         Arquivo com strings para execução
             -str, -st cmd          String template de comando
             -out, -o file          Arquivo output de valores da execução shell
             -pipe, -p cmd          Comando que será executado depois de um pipe |
             -verbose, -v           Modo verboso
             -thread, -t <10>       Quantidade de threads
             -pf                    Mostrar resultados da execução de função, ignora shell
             -of                    Habilitar output de valores da execução de função
             -filter, -f value      Valor para filtrar strings para execução
             -sleep <5>             Segundos de delay entre threads
             -module <type:module>  Selectionar o tipo e module
             -pm                    Mostrar somente resultados de execução do module
```

## 💡 EJEMPLOS PRÁCTICOS

### Ejemplos Básicos

#### 1. Verificación de Hosts
```bash
# Vía archivo
./strx -l hosts.txt -st "host {STRING}" -v

# Vía pipe
cat hosts.txt | ./strx -st "host {STRING}" -v
```

#### 2. Peticiones HTTP con Análisis
```bash
# Verificar estado de URLs
./strx -l urls.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 20

# Extraer títulos de páginas
./strx -l domains.txt -st "curl -sL https://{STRING}" -p "grep -o '<title>.*</title>'" -o titles.txt
```

#### 3. Análisis de Logs y Datos
```bash
# Buscar CPFs en leaks
./strx -l cpfs.txt -st "grep -Ei '{STRING}' -R ./database/" -v

# Procesar dump SQL
./strx -l dump.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u
```

### Ejemplos Avanzados

#### 1. OSINT y Reconocimiento
```bash
# Información de IP
cat ips.txt | ./strx -st "curl -s 'https://ipinfo.io/{STRING}/json'" -p "jq -r '.org, .country'"

# Verificación de phishing
./strx -l suspicious.txt -st "curl -skL https://{STRING}/" -p "grep -i 'phish\|scam\|fake'" -t 30

# Enumeración DNS
./strx -l subdomains.txt -st "dig +short {STRING}" -module "clc:dns" -pm
```

#### 2. Seguridad y Pentesting
```bash
# Escaneo de puertos con nmap
./strx -l targets.txt -st "nmap -p 80,443 {STRING}" -p "grep 'open'" -t 10

# Pruebas de inyección SQL
./strx -l urls.txt -st "sqlmap -u '{STRING}' --batch" -p "grep 'vulnerable'" -o sqli_results.txt

# Bruteforce de directorios
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

## 🔧 FUNCIONES INTEGRADAS

String-X incluye funciones built-in que pueden ser utilizadas dentro de las plantillas `{STRING}` y comandos pipe. Estas funciones son procesadas antes de la ejecución de los comandos shell.

### Tabla de Funciones Disponibles

| FUNCIÓN | DESCRIPCIÓN | EJEMPLO |
|--------|-----------|---------|
| `clear` | Remove espaços, tabs e quebras de linha | `clear({STRING})` |
| `base64` / `debase64` | Codifica/decodifica Base64 | `base64({STRING})` |
| `hex` / `dehex` | Codifica/decodifica hexadecimal | `hex({STRING})` |
| `sha1`, `sha256`, `md5` | Gera hash | `sha256({STRING})` |
| `str_rand`, `int_rand` | Gera string/número aleatório | `str_rand(10)` |
| `ip` | Resolve hostname para IP | `ip({STRING})` |
| `replace` | Substitui substring | `replace(http:,https:,{STRING})` |
| `get` | Requisição HTTP GET | `get(https://{STRING})` |
| `urlencode` | Codifica URL | `urlencode({STRING})` |
| `rev` | Inverte string | `rev({STRING})` |
| `timestamp` | Timestamp atual | `timestamp()` |
| `extract_domain` | Extrai domínio de URL | `extract_domain({STRING})` |
| `jwt_decode` | Decodifica JWT (payload) | `jwt_decode({STRING})` |
| `whois_lookup` | Consulta WHOIS | `whois_lookup({STRING})` |
| `cert_info` | Info de certificado SSL | `cert_info({STRING})` |
| `user_agent` | User-Agent aleatório | `user_agent()` |
| `cidr_expand` | Expande faixa CIDR | `cidr_expand(192.168.0.0/30)` |
| `subdomain_gen` | Gera subdomínios comuns | `subdomain_gen({STRING})` |
| `email_validator` | Valida email | `email_validator({STRING})` |
| `hash_file` | Hashes de arquivo | `hash_file(path.txt)` |
| `encode_url_all` | Codifica URL (tudo) | `encode_url_all({STRING})` |
| `phone_format` | Formata telefone BR | `phone_format({STRING})` |
| `password_strength` | Força de senha | `password_strength({STRING})` |
| `social_media_extract` | Extrai handles sociais | `social_media_extract({STRING})` |
| `leak_check_format` | Formata email para leaks | `leak_check_format({STRING})` |
| `cpf_validate` | Valida CPF | `cpf_validate({STRING})` |


## 🧩 SISTEMA DE MÓDULOS

String-X utiliza una arquitectura modular extensible que permite agregar funcionalidades específicas sin modificar el código principal. Los módulos están organizados por tipo y se cargan dinámicamente.

### Módulos Extractor (EXT)

Los módulos extractores utilizan expresiones regulares para extraer datos específicos de strings.

#### Módulos Disponibles:
- **`email`**: Extrae direcciones de email válidas
- **`domain`**: Extrae dominios y subdominios
- **`url`**: Extrae URLs completas (HTTP/HTTPS)
- **`phone`**: Extrae números de teléfono (formato brasileño)

```bash
# Extraer emails de dump de datos
./strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm

# Extraer dominios de logs
cat access.log | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | sort -u
```

### Módulos Collector (CLC)

Los módulos recolectores hacen peticiones a servicios externos para obtener información adicional.

#### Módulos Disponibles:
- **`dns`**: Recolecta registros DNS (A, MX, TXT, etc.)

```bash
# Recolectar información DNS
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm
```

## 🎯 FILTROS Y PROCESAMIENTO SELECTIVO

El sistema de filtros permite procesar solo strings que cumplan criterios específicos.

```bash
# Filtrar solo dominios .gov.br
./strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# Filtrar solo URLs HTTPS
./strx -l urls.txt -st "curl {STRING}" -f "https"
```

## ⚡ PROCESAMIENTO PARALELO

String-X soporta procesamiento paralelo a través de hilos para acelerar operaciones en grandes volúmenes de datos.

```bash
# Verificación rápida de estado HTTP
./strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# Resolución DNS masiva
./strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1
```

## 🤝 CONTRIBUCIÓN

¡Contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👨‍💻 AUTOR

```bash
 + Autor:   MrCl0wn
 + Blog:    http://blog.mrcl0wn.com
 + GitHub:  https://github.com/MrCl0wnLab
 + GitHub:  https://github.com/MrCl0wnLab
 + Twitter: https://twitter.com/MrCl0wnLab
 + Email:   mrcl0wnlab@gmail.com
```

## 📄 LICENCIA

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

### SALIDA TERMINAL

-  Comando ejemplo usado: ```cat hosts.txt  | ./strx -str 'host {STRING}'```

![Screenshot](/asset/img1.png)

-  Comando ejemplo usado: ```cat hosts.txt | ./strx -str "curl -Iksw 'CODE:%{response_code};IP:%{remote_ip};HOST:%{url.host};SERVER:%header{server}' https://{STRING}"  -p "grep -o -E 'CODE:.(.*)|IP:.(.*)|HOST:.(.*)|SERVER:.(.*)'" -t 30``` 

![Screenshot](/asset/img3.png)

### VERBOSE
> usando -v / -verbose

-  Comando ejemplo usado: ```cat hosts.txt  | ./strx -str 'host {STRING}' -v```

![Screenshot](/asset/img2.png)

### ARCHIVO DE SALIDA
> formato de archivo output

```
output-%d-%m-%Y-%H.txt > output-15-06-2025-11.txt
```

<div align="center">

**⭐ Si este proyecto te fue útil, ¡considera darle una estrella!**

**💡 ¡Sugerencias y feedback son siempre bienvenidos!**

**💀 Hacker Hackeia!**

</div>