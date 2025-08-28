<center>

<h1 align="center">
  <a href="#/"><img src="./asset/img/logo.png"></a>
</h1>

<h4 align="center">Herramienta de Automatización para Manipulación de Strings</h4>

<p align="center">
String-X (strx) es una herramienta de automatización modular desarrollada para profesionales de Infosec y entusiastas del hacking. Especializada en manipulación dinámica de strings en entornos Linux.

Con arquitectura modular, ofrece características avanzadas para OSINT, pentest y análisis de datos, incluyendo procesamiento paralelo, módulos especializados de extracción, recolección e integración con APIs externas. Sistema basado en plantillas con más de 25 funciones integradas.
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

## ✨ CARACTERÍSTICAS

- 🚀 **Procesamiento Paralelo**: Sistema multi-threading configurable para ejecución de alto rendimiento
- 🧩 **Arquitectura Modular**: Estructura extensible con módulos especializados (EXT, CLC, OUT, CON, AI)
- 🔄 **Plantilla Dinámica**: Sistema de sustitución con placeholder `{STRING}` para manipulación flexible
- 🛠️ **+25 Funciones Integradas**: Hash, encoding, requests, validación y generación de valores aleatorios
- 📁 **Múltiples Fuentes**: Soporte para archivos, stdin y encadenamiento de pipes
- 🎯 **Filtrado Inteligente**: Sistema de filtros para procesamiento selectivo de strings
- 💾 **Salida Flexible**: Formateo TXT, CSV y JSON con timestamp automático
- 🔌 **Integraciones Externas**: APIs, bases de datos y servicios de notificación
- 🔍 **Extracción Avanzada**: Patrones complejos con regex y procesamiento especializado
- 🔒 **OSINT y Pentest**: Características optimizadas para reconocimiento y análisis de seguridad
- 🌐 **Dorking Multi-Motor**: Integración con Google, Bing, Yahoo, DuckDuckGo y otros
- 🧠 **Integración con IA**: Módulo para procesamiento con Google Gemini
- 🐋 **Soporte Docker**: Ejecución containerizada para entornos aislados
- 🛡️ **Validaciones de Seguridad**: Sistema de protección contra comandos maliciosos con opción de bypass

## 📦 INSTALACIÓN

### Requisitos
- Python 3.12+
- Linux/MacOS
- Bibliotecas listadas en `requirements.txt`

### Instalación Rápida
```bash
# Clonar repositorio
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x

# Instalar dependencias
pip install -r requirements.txt

# Hacer archivo ejecutable
chmod +x strx

# Probar instalación con ayuda
./strx -help

# Listar tipos de módulos
./strx -types

# Listar módulos y ejemplos de uso
./strx -examples

# Listar funciones
./strx -funcs
```

### Creando enlace simbólico (opcional)
```bash
# Verificar enlace actual
ls -la /usr/local/bin/strx

# Si es necesario, recrear el enlace
sudo rm /usr/local/bin/strx
sudo ln -sf $HOME/Documents/string-x/strx /usr/local/bin/strx
```

## ⏫ Sistema de Actualización con Git
Usa comandos git para descargar nuevas versiones
```bash
# Actualizar String-X
./strx -upgrade
```

## 🐋 DOCKER
String-X está disponible como imagen Docker, permitiendo ejecución en entornos aislados sin necesidad de instalación local de dependencias.

### Construyendo la Imagen

```bash
# Construir imagen Docker
docker build -t string-x .
```

### Uso Básico con Docker

```bash
# Ejecutar con comando por defecto (muestra ejemplos)
docker run --rm string-x

# Ver ayuda
docker run --rm string-x -h

# Listar funciones disponibles
docker run --rm string-x -funcs

# Listar tipos de módulos
docker run --rm string-x -types
```

### Procesando Archivos Locales

Para procesar archivos del host, montar el directorio como volumen:

```bash
# Montar directorio actual y procesar archivo
docker run --rm -v $(pwd):/datos string-x -l /datos/urls.txt -st "curl -I {STRING}"

# Procesar con múltiples threads
docker run --rm -v $(pwd):/datos string-x -l /datos/hosts.txt -st "nmap -p 80,443 {STRING}" -t 20

# Guardar resultados en el host
docker run --rm -v $(pwd):/datos string-x -l /datos/domains.txt -st "dig +short {STRING}" -o /datos/results.txt
```

### Uso con Módulos

```bash
# Extraer emails de archivo
docker run --rm -v $(pwd):/datos string-x -l /datos/dump.txt -st "echo {STRING}" -module "ext:email" -pm

# Dorking con Google
docker run --rm -v $(pwd):/datos string-x -l /datos/dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Recopilar información DNS
docker run --rm -v $(pwd):/datos string-x -l /datos/domains.txt -st "echo {STRING}" -module "clc:dns" -pm
```

### Procesamiento vía Pipe

```bash
# Pipes de comandos del host
echo "github.com" | docker run --rm -i string-x -st "whois {STRING}"

# Combinación con herramientas del host
cat urls.txt | docker run --rm -i string-x -st "curl -skL {STRING}" -p "grep '<title>'"

# Pipeline complejo
cat domains.txt | docker run --rm -i string-x -st "echo {STRING}" -module "clc:crtsh" -pm | sort -u
```

### Configuraciones Avanzadas

```bash
# Usar proxy dentro del container
docker run --rm -v $(pwd):/datos string-x -l /datos/dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "http://172.17.0.1:8080" -pm

# Definir formato de salida
docker run --rm -v $(pwd):/datos string-x -l /datos/targets.txt -st "echo {STRING}" -format json -o /datos/output.json

# Ejecutar con delay entre threads
docker run --rm -v $(pwd):/datos string-x -l /datos/apis.txt -st "curl {STRING}" -t 10 -sleep 2
```

## 🧠 CONCEPTOS FUNDAMENTALES

### Sistema de Plantilla {STRING}
La herramienta utiliza el placeholder `{STRING}` como palabra clave para sustitución dinámica de valores. Este sistema permite que cada línea de entrada se procese individualmente, reemplazando `{STRING}` con el valor actual.

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
2. **Plantilla**: Aplicación de plantilla con `{STRING}`
3. **Procesamiento**: Ejecución de comandos/módulos
4. **Pipe**: Procesamiento adicional opcional (`-p`)
5. **Salida**: Resultado final (pantalla o archivo)

<center>

![Screenshot](/asset/img/fluxo.jpg)

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
```bash
string-x/
      .
      ├── asset             # Imágenes, banners y logos usados en documentación e interfaz CLI
      ├── config            # Archivos de configuración global del proyecto (settings, variables)
      ├── core              # Núcleo de la aplicación, motor principal y lógica central
      │   └── banner        # Submódulo para banners ASCII art
      │       └── asciiart  # Archivos ASCII art para visualización en terminal
      ├── output            # Directorio por defecto para archivos de salida y logs generados por la herramienta
      └── utils             # Utilidades y módulos auxiliares para extensiones e integraciones
          ├── auxiliary     # Módulos auxiliares organizados por función
          │   ├── ai        # Módulos de inteligencia artificial (ej: prompts Gemini)
          │   ├── clc       # Módulos recolectores (búsqueda, DNS, whois, APIs externas)
          │   ├── con       # Módulos de conexión (SSH, FTP, HTTP probe)
          │   ├── ext       # Módulos extractores (regex: email, dominio, IP, hash, etc)
          │   └── out       # Módulos de salida/integradores (JSON, CSV, base de datos, APIs)
          └── helper        # Funciones utilitarias y helpers usados en todo el proyecto
```

## 🚀 USO DE LA HERRAMIENTA

### Ayuda y Parámetros
```bash
./strx -help
```

### Parámetros Principales

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-h, -help`         | Mostrar ayuda del proyecto | `-h` |
| `-types`             | Listar tipos de módulos | `-types` |
| `-examples`          | Listar módulos y ejemplos de uso | `-examples` |
| `-functions, -funcs` | Listar funciones | `-funcs` |
| `-l, -list` | Archivo con strings para procesamiento | `-l hosts.txt` |
| `-st, --str` | Plantilla de comando con `{STRING}` | `-st "curl {STRING}"` |
| `-o, --out` | Archivo de salida para resultados | `-o results.txt` |
| `-p, -pipe` | Comando adicional vía pipe | `-p "grep 200"` |
| `-v, -verbose` | Modo verboso con niveles (1-5 o 'all'). 1=info, 2=warning, 3=debug, 4=error, 5=exception | `-v 3` |
| `-ds, -disable-security` | Deshabilitar validaciones de seguridad (usar con cuidado) | `-ds` |
| `-ns, -no-shell` | Procesar entrada directamente a través de módulos/funciones sin ejecución de comandos shell | `-ns` |
| `-t, -thread` | Número de threads paralelos | `-t 50` |
| `-f, --filter` | Filtro para selección de strings | `-f ".gov.br"` |
| `-iff` | Filtro de resultados de función: retorna solo resultados que contengan el valor especificado | `-iff "admin"` |
| `-ifm` | Filtro de resultados de módulo: retorna solo resultados que contengan el valor especificado | `-ifm "hash"` |
| `-module` | Selección de módulo específico | `-module "ext:email"` |
| `-pm` | Mostrar solo resultados del módulo | `-pm` |
| `-pf` | Mostrar solo resultados de funciones | `-pf` |
| `-of` | Guardar resultados de funciones en archivo | `-of` |
| `-sleep` | Delay entre threads (segundos) | `-sleep 2` |
| `-proxy` | Establecer proxy para requests | `-proxy "http://127.0.0.1:8080"` |
| `-format` | Formato de salida (txt, csv, json) | `-format json` |
| `-upgrade` | Actualizar String-X vía Git | `-upgrade` |
| `-r, -retry` | Número de intentos de reintento | `-r 3` |

## 💡 EJEMPLOS PRÁCTICOS

### Niveles de Verbose
String-X ofrece 5 niveles de verbosidad para control detallado de la salida:

```bash
# Nivel 1 (info) - Información básica
strx -l domains.txt -st "dig {STRING}" -v 1

# Nivel 2 (warning) - Avisos y alertas
strx -l urls.txt -st "curl {STRING}" -v 2

# Nivel 3 (debug) - Información detallada de depuración
strx -l targets.txt -st "nmap {STRING}" -v 3

# Nivel 4 (error) - Errores de ejecución
strx -l data.txt -st "process {STRING}" -v 4

# Nivel 5 (exception) - Excepciones con stack trace
strx -l complex.txt -st "analyze {STRING}" -v 5

# Todos los niveles - Máxima salida de información
strx -l hosts.txt -st "scan {STRING}" -v all

# Combinar múltiples niveles
strx -l mixed.txt -st "test {STRING}" -v "1,3,4"
```

### Modo No-Shell (-ns / --no-shell)

String-X introduce la flag **-no-shell** que permite procesamiento directo de entrada a través de módulos y funciones, **sin ejecución de comandos shell**. Esto mejora la seguridad, rendimiento y usabilidad.

#### Beneficios:
- **🔒 Seguridad Mejorada**: Elimina riesgos de inyección shell
- **⚡ Rendimiento Superior**: Remueve overhead de subprocesos
- **💡 Sintaxis Simplificada**: Elimina necesidad de comandos wrapper como `echo {STRING}`

#### Comparación de Enfoques:

```bash
# Enfoque Tradicional
echo "https://example.com" | strx -st "echo {STRING}" -module "ext:url" -pm

# Nuevo Enfoque No-Shell
echo "https://example.com" | strx -st "{STRING}" -module "ext:url" -ns -pm
```

#### Ejemplos con Módulos:
```bash
# Extracción directa de URLs
curl 'https://blog.inurl.com.br' | strx -st "{STRING}" -module 'ext:url' -ns -pm

# Encadenamiento de módulos sin shell
strx -l domains.txt -st "{STRING}" -module "ext:url|ext:domain|clc:dns" -ns -pm

# Procesamiento de datasets grandes con mejor rendimiento
strx -l huge_dataset.txt -st "{STRING}" -module "ext:email" -ns -pm -t 50
```

#### Ejemplos con Funciones:
```bash
# Funciones aplicadas directamente
echo 'https://example.com/path' | strx -st "extract_domain({STRING})" -ns -pf

# Múltiples funciones
strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -ns -pf
```

### Ejemplos Básicos

#### 1. Verificación de Hosts
```bash
# Vía archivo
./strx -l hosts.txt -st "host {STRING}" -v

# Vía pipe
cat hosts.txt | ./strx -st "host {STRING}" -v
```

#### 2. Requests HTTP con Análisis
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

#### 2. Seguridad y Pentest
```bash
# Escaneo de puertos con nmap
./strx -l targets.txt -st "nmap -p 80,443 {STRING}" -p "grep 'open'" -t 10

# Pruebas de inyección SQL
./strx -l urls.txt -st "sqlmap -u '{STRING}' --batch" -p "grep 'vulnerable'" -o sqli_results.txt

# Bruteforce de directorios
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

#### 3. Procesamiento de Datos
```bash
# Extraer emails de múltiples archivos
./strx -l files.txt -st "cat {STRING}" -module "ext:email" -pm > all_emails.txt

# Conversión de encoding
./strx -l base64_data.txt -st "debase64({STRING})" -pf -of

# Generación de hashes
./strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -pf -o hashes.txt

# Uso de formateo json
echo 'com.br' | ./strx  -st "echo {STRING}" -o bing.json -format json -module 'clc:bing' -pm -v
```

### Dorking y Motores de Búsqueda
```bash
# Dorking básico en Google
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Búsqueda de archivos PDF en sitios gubernamentales
echo 'site:gov filetype:pdf "confidential"' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm

# Encontrar paneles de admin expuestos
echo 'inurl:admin intitle:"login"' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm

# Múltiples motores de búsqueda con mismo dork
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:duckduckgo" -pm > duckduckgo_results.txt
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:bing" -pm > bing_results.txt

# Comparar resultados entre motores
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:google" -pm | sort > google_results.txt
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:bing" -pm | sort > bing_results.txt
comm -23 google_results.txt bing_results.txt > google_exclusive.txt
```

### Dorking con Proxy
```bash
# Usando proxy con dorking para evitar bloqueos
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "http://127.0.0.1:9050" -pm

# Usando proxy con autenticación
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:yahoo" -proxy "http://user:pass@server:8080" -pm

# Aplicando dorking con TOR
./strx -l sensitive_dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "https://127.0.0.1:9050" -pm -t 1 -sleep 5

# Dorking con salida estructurada + proxy con autenticación
./strx -l sqli_dorks.txt -st "echo {STRING}" -module "clc:googlecse" -proxy "http://user:pass@10.0.0.1:8080" -pm -module "out:json" -pm

# Recolección distribuida a través de lista de proxies
cat proxy_list.txt | while read proxy; do
  ./strx -l target_dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "$proxy" -pm -t 3 -sleep 2
done > combined_results.txt
```

## 🔧 FUNCIONES INTEGRADAS

String-X incluye más de 25 funciones incorporadas que pueden utilizarse dentro de plantillas `{STRING}` y comandos pipe. Estas funciones se procesan antes de la ejecución de comandos shell y cubren desde hash, encoding, manipulación de strings, generación de valores aleatorios, análisis de datos, validación de documentos, requests HTTP, manipulación de archivos y mucho más.

### Sintaxis
```bash
# Función simple
./strx -l data.txt -st "funcion({STRING})" -pf

# Múltiples funciones
./strx -l data.txt -st "{STRING}; md5({STRING}); base64({STRING})" -pf

# Función con parámetros
./strx -l data.txt -st "str_rand(10); int_rand(5)" -pf
```

### Funciones Disponibles (Principales)

| Función | Descripción | Ejemplo |
|---------|-------------|---------|
| `clear` | Eliminar espacios, tabs y saltos de línea | `clear({STRING})` |
| `base64` / `debase64` | Codificar/decodificar Base64 | `base64({STRING})` |
| `hex` / `dehex` | Codificar/decodificar hexadecimal | `hex({STRING})` |
| `sha1`, `sha256`, `md5` | Generar hash | `sha256({STRING})` |
| `str_rand`, `int_rand` | Generar string/número aleatorio | `str_rand(10)` |
| `ip` | Resolver hostname a IP | `ip({STRING})` |
| `replace` | Reemplazar substring | `replace(http:,https:,{STRING})` |
| `get` | Request HTTP GET | `get(https://{STRING})` |
| `urlencode` | Codificar URL | `urlencode({STRING})` |
| `rev` | Invertir string | `rev({STRING})` |
| `timestamp` | Timestamp actual | `timestamp()` |
| `extract_domain` | Extraer dominio de URL | `extract_domain({STRING})` |
| `jwt_decode` | Decodificar JWT (payload) | `jwt_decode({STRING})` |
| `whois_lookup` | Consulta WHOIS | `whois_lookup({STRING})` |
| `cert_info` | Info de certificado SSL | `cert_info({STRING})` |
| `user_agent` | User-Agent aleatorio | `user_agent()` |
| `cidr_expand` | Expandir rango CIDR | `cidr_expand(192.168.0.0/30)` |
| `subdomain_gen` | Generar subdominios comunes | `subdomain_gen({STRING})` |
| `email_validator` | Validar email | `email_validator({STRING})` |
| `hash_file` | Hashes de archivo | `hash_file(path.txt)` |
| `encode_url_all` | Codificar URL (todo) | `encode_url_all({STRING})` |
| `phone_format` | Formatear teléfono BR | `phone_format({STRING})` |
| `password_strength` | Fuerza de contraseña | `password_strength({STRING})` |
| `social_media_extract` | Extraer handles sociales | `social_media_extract({STRING})` |
| `leak_check_format` | Formatear email para leaks | `leak_check_format({STRING})` |
| `cpf_validate` | Validar CPF | `cpf_validate({STRING})` |

> Ver la lista completa y ejemplos en `utils/helper/functions.py` o usar `-functions` en CLI para documentación detallada.

## 🧩 SISTEMA DE MÓDULOS

String-X utiliza una arquitectura modular extensible que permite agregar funcionalidades específicas sin modificar el código principal. Los módulos están organizados por tipo y se cargan dinámicamente.

### Tipos de Módulos Disponibles

| Tipo | Código | Descripción | Ubicación |
|------|--------|-------------|-----------|
| **Extractor** | `ext` | Extracción de datos específicos usando regex | `utils/auxiliary/ext/` |
| **Collector** | `clc` | Recolección de información de APIs/servicios | `utils/auxiliary/clc/` |
| **Output** | `out` | Formateo y envío de datos | `utils/auxiliary/out/` |
| **Connection** | `con` | Conexiones especializadas | `utils/auxiliary/con/` |
| **AI** | `ai` | Inteligencia artificial | `utils/auxiliary/ai/` |

#### Sintaxis Básica
```bash
./strx -module "tipo:nombre_del_modulo"
```

#### Parámetros Relacionados
- **`-module tipo:nombre`**: Especifica el módulo a utilizar
- **`-pm`**: Muestra solo resultados del módulo (omite salida shell)

### Módulos Extractor (EXT)
Módulos para extracción de patrones y datos específicos usando regex:

| Módulo      | Descripción                                 | Ejemplo CLI |
|-------------|---------------------------------------------|-------------|
| `email`     | Extraer direcciones de email válidas       | `-module "ext:email"` |
| `domain`    | Extraer dominios y subdominios              | `-module "ext:domain"` |
| `url`       | Extraer URLs completas (HTTP/HTTPS)        | `-module "ext:url"` |
| `phone`     | Extraer números de teléfono (BR)           | `-module "ext:phone"` |
| `credential`| Extraer credenciales, tokens, claves       | `-module "ext:credential"` |
| `ip`        | Extraer direcciones IPv4/IPv6              | `-module "ext:ip"` |
| `hash`      | Extraer hashes MD5, SHA1, SHA256, SHA512   | `-module "ext:hash"` |

```bash
# Ejemplo: Extraer emails de dump de datos
./strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm
```

### Módulos Collector (CLC)
Módulos para recolección de información externa, APIs y análisis:

| Módulo        | Descripción                                 | Ejemplo CLI |
|---------------|---------------------------------------------|-------------|
| `archive`     | Recopilar URLs archivadas de Wayback Machine | `-module "clc:archive"` |
| `bing`        | Realizar búsquedas con dorks en Bing       | `-module "clc:bing"` |
| `crtsh`       | Recopilar certificados SSL/TLS y subdominios| `-module "clc:crtsh"` |
| `dns`         | Recopilar registros DNS (A, MX, TXT, NS)   | `-module "clc:dns"` |
| `duckduckgo`  | Realizar búsquedas con dorks en DuckDuckGo | `-module "clc:duckduckgo"` |
| `emailverify` | Verificar validez de emails (MX, SMTP)     | `-module "clc:emailverify"` |
| `ezilon`      | Realizar búsquedas con dorks en Ezilon     | `-module "clc:ezilon"` |
| `geoip`       | Geolocalización de IPs                     | `-module "clc:geoip"` |
| `google`      | Realizar búsquedas con dorks en Google     | `-module "clc:google"` |
| `googlecse`   | Realizar búsquedas con dorks usando Google CSE | `-module "clc:googlecse"` |
| `http_probe`  | Sondeo HTTP/HTTPS, análisis de headers     | `-module "clc:http_probe"` |
| `ipinfo`      | Escáner de puertos IP/host                 | `-module "clc:ipinfo"` |
| `lycos`       | Realizar búsquedas con dorks en Lycos      | `-module "clc:lycos"` |
| `naver`       | Realizar búsquedas con dorks en Naver (Coreano) | `-module "clc:naver"` |
| `netscan`     | Escáner de red (hosts, servicios)          | `-module "clc:netscan"` |
| `shodan`      | Consultar API Shodan                       | `-module "clc:shodan"` |
| `sogou`       | Realizar búsquedas con dorks en Sogou (Chino) | `-module "clc:sogou"` |
| `spider`      | Web spider para recolección recursiva de URLs | `-module "clc:spider"` |
| `subdomain`   | Enumeración de subdominios                 | `-module "clc:subdomain"` |
| `virustotal`  | Consultar API VirusTotal                   | `-module "clc:virustotal"` |
| `whois`       | Consulta WHOIS de dominios                 | `-module "clc:whois"` |
| `yahoo`       | Realizar búsquedas con dorks en Yahoo      | `-module "clc:yahoo"` |

```bash
# Ejemplo: Recopilar información DNS
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm

# Ejemplo: Recopilar información usando motores de búsqueda
./strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:googlecse" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:duckduckgo" -pm

# Ejemplo: Sondear y analizar servidores web
./strx -l urls.txt -st "echo {STRING}" -module "clc:http_probe" -pm

# Ejemplos con dorking específico
echo 'site:fbi.gov filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:google" -pm
echo 'site:github.com inurl:admin' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm
echo 'inurl:admin' | ./strx -st "echo {STRING}" -module "clc:lycos" -pm
echo 'site:github.com' | ./strx -st "echo {STRING}" -module "clc:ezilon" -pm
echo 'filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm
```

### Módulos Output (OUT)
Módulos para formateo y salida de resultados:

| Módulo        | Descripción                                 | Ejemplo CLI |
|---------------|---------------------------------------------|-------------|
| `json`        | Guardar resultados en JSON                 | `-module "out:json"` |
| `csv`         | Guardar resultados en CSV                  | `-module "out:csv"` |
| `xml`         | Guardar resultados en XML                  | `-module "out:xml"` |

```bash
# Ejemplo: Guardar en JSON
./strx -l data.txt -st "process {STRING}" -module "out:json" -pm
```

### Módulos Connection (CON)
Módulos para conexiones con servicios externos e integración de resultados:

| Módulo        | Descripción                                 | Ejemplo CLI |
|---------------|---------------------------------------------|-------------|
| `sqlite`      | Guardar datos en base SQLite               | `-module "con:sqlite"` |
| `mysql`       | Guardar datos en base MySQL                | `-module "con:mysql"` |
| `telegram`    | Enviar resultados vía Telegram Bot         | `-module "con:telegram"` |
| `slack`       | Enviar resultados vía Slack Webhook        | `-module "con:slack"` |
| `opensearch`  | Indexar resultados en Open Search          | `-module "con:opensearch"` |
| `ftp`         | Conexión y transferencia vía FTP           | `-module "con:ftp"` |
| `ssh`         | Ejecutar comandos vía SSH                  | `-module "con:ssh"` |
| `s3`          | Subir/descargar datos en Amazon S3         | `-module "con:s3"` |

```bash
# Ejemplo: Guardar en SQLite
./strx -l data.txt -st "process {STRING}" -module "con:sqlite" -pm
```


### Módulos de Inteligencia Artificial (AI)
Módulos para prompts de IA:

| Módulo        | Descripción                                 | Ejemplo CLI |
|---------------|---------------------------------------------|-------------|
| `gemini`      | Prompt para Google Gemini AI - ([Crear API Key](https://aistudio.google.com/app/apikey)) | `-module "ai:gemini"` |

```bash
# Ejemplo: Usar archivos con Prompts
./strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm

# Ejemplo: Recopilar URLs y enviar para análisis construyendo Prompt
./strx -l urls.txt -st "echo 'Analizar URL: {STRING}'" -module "ai:gemini" -pm
```

## 🎯 FILTROS Y PROCESAMIENTO SELECTIVO

El sistema de filtros permite procesar solo strings que cumplan criterios específicos, optimizando rendimiento y precisión.

### Uso de Filtros
```bash
./strx -f "valor_filtro" / ./strx --filter "valor_filtro"
```

### Ejemplos de Filtros
```bash
# Filtrar solo dominios .gov.br
./strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# Filtrar solo URLs HTTPS
./strx -l urls.txt -st "curl {STRING}" -f "https"

# Filtrar IPs específicos
./strx -l logs.txt -st "analyze {STRING}" -f "192.168"

# Filtrar extensiones de archivo
./strx -l files.txt -st "process {STRING}" -f ".pdf"

# Filtrar solo resultados de función que contengan "admin"
./strx -l urls.txt -st "{STRING}; md5({STRING})" -pf -iff "admin"

# Filtrar solo resultados de módulo que contengan hash específico
./strx -l domains.txt -st "echo {STRING}" -module "ext:hash" -pm -ifm "a1b2c3"

# Combinar filtros de función y módulo
./strx -l data.txt -st "{STRING}; md5({STRING})" -module "ext:domain" -pf -pm -iff "google" -ifm "admin"
```

## ⚡ PROCESAMIENTO PARALELO

String-X soporta procesamiento paralelo a través de threads para acelerar operaciones en grandes volúmenes de datos.

### Configuración de Threads
```bash
# Definir número de threads
./strx -t 50 / ./strx -thread 50

# Definir delay entre threads
./strx -sleep 2
```

### Ejemplos con Threading
```bash
# Verificación rápida de estado HTTP
./strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# Resolución DNS masiva
./strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1

# Escaneo de puertos
./strx -l ip_list.txt -st "nmap -p 80,443 {STRING}" -t 20 -sleep 3
```

### Mejores Prácticas para Threading
- **Rate limiting**: Usar `-sleep` para evitar sobrecarga de servicios
- **Número adecuado**: Ajustar `-t` según recursos disponibles
- **Monitoreo**: Usar `-v 1` para info básica, `-v 3` para debug detallado, `-v all` para máximo control

### Procesamiento de Archivos Grandes
String-X ha sido optimizado para procesar archivos grandes eficientemente:
```bash
# Procesar archivo grande con múltiples threads
strx -l archivo_grande.txt -st "echo {STRING}" -module "ext:email" -pm -t 20 -sleep 1

# Para archivos muy grandes, usar menos threads y más delay
strx -l dataset_enorme.txt -st "process {STRING}" -t 10 -sleep 2 -v
```

## 🛡️ SISTEMA DE SEGURIDAD

String-X incluye validaciones de seguridad para prevenir la ejecución de comandos maliciosos:

### Validaciones Activas
- **Tamaño de entrada**: Limita datos de entrada a 1MB por defecto
- **Cantidad de strings**: Máximo de 10,000 strings por ejecución
- **Patrones peligrosos**: Detecta y bloquea comandos potencialmente maliciosos
- **Threads**: Limita threads concurrentes para evitar sobrecarga del sistema

### Deshabilitando Validaciones de Seguridad
**⚠️ ADVERTENCIA**: Usar solo cuando sea necesario y confíe en el contenido

```bash
# Deshabilitar validaciones para comandos complejos legítimos
strx -l datos.txt -st "echo {STRING}; md5sum {STRING}" -ds

# Procesar archivos grandes sin limitaciones
strx -l archivo_enorme.txt -st "process {STRING}" -ds -t 50

# Usar con funciones que pueden generar patrones detectados como sospechosos
echo "test" | strx -st "echo {STRING}; echo 'resultado'" -ds
```

### Modo Debug para Seguridad
```bash
# Ver detalles de las validaciones de seguridad (debug completo)
strx -l datos.txt -st "command {STRING}" -v 3

# Verificar por qué un comando fue bloqueado
strx -s "test" -st "comando_sospechoso" -v 3
```

## 📸 EJEMPLOS VISUALES

### Ejecución Básica
**Comando**: `cat hosts.txt | ./strx -str 'host {STRING}'`

![Screenshot](/asset/img/img1.png)

### Procesamiento con Threading
**Comando**: `cat hosts.txt | ./strx -str "curl -Iksw 'CODE:%{response_code};IP:%{remote_ip};HOST:%{url.host};SERVER:%header{server}' https://{STRING}" -p "grep -o -E 'CODE:.(.*)|IP:.(.*)|HOST:.(.*)|SERVER:.(.*)'" -t 30`

![Screenshot](/asset/img/img3.png)

### Modo Verbose
**Comando**: `cat hosts.txt | ./strx -str 'host {STRING}' -v`

![Screenshot](/asset/img/img2.png)

### Formato de Archivo de Salida
```
output-%d-%m-%Y-%H.txt > output-15-06-2025-11.txt
```

## 🤝 CONTRIBUCIÓN

¡Las contribuciones son bienvenidas! Para contribuir:

1. **Fork** del repositorio
2. **Crear** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abrir** un Pull Request

### Tipos de Contribución
- 🐛 **Corrección de bugs**
- ✨ **Nuevas características**
- 📝 **Mejoras de documentación**
- 🧩 **Nuevos módulos**
- ⚡ **Optimizaciones de rendimiento**

### Desarrollo de Módulos
Para crear nuevos módulos, consultar la sección [Sistema de Módulos](#-sistema-de-módulos) y seguir patrones establecidos.

## 📄 LICENCIA

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 AUTOR

**MrCl0wn**
- 🌐 **Blog**: [http://blog.mrcl0wn.com](http://blog.mrcl0wn.com)
- 🐙 **GitHub**: [@MrCl0wnLab](https://github.com/MrCl0wnLab) | [@MrCl0wnLab](https://github.com/MrCl0wnLab)
- 🐦 **Twitter**: [@MrCl0wnLab](https://twitter.com/MrCl0wnLab)
- 📧 **Email**: mrcl0wnlab@gmail.com

---

<div align="center">

**⭐ ¡Si este proyecto fue útil, considera darle una estrella!**

**💡 ¡Sugerencias y feedback son siempre bienvenidos!**

**💀 Hacker Hackeia!**

</div>