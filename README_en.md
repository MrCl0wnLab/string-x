<center>

<h1 align="center">
  <a href="#/"><img src="./asset/img/logo.png"></a>
</h1>

<h4 align="center">Automation Tool for String Manipulation</h4>

<p align="center">
String-X (strx) is a modular automation tool developed for Infosec professionals and hacking enthusiasts. Specialized in dynamic string manipulation in Linux environments.

With modular architecture, it offers advanced features for OSINT, pentest, and data analysis, including parallel processing, specialized extraction modules, collection and integration with external APIs. Template-based system with more than 25 integrated functions.
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

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Fundamental Concepts](#-fundamental-concepts)
- [Modular Architecture](#-modular-architecture)
- [Tool Usage](#-tool-usage)
- [Practical Examples](#-practical-examples)
- [Integrated Functions](#-integrated-functions)
- [Module System](#-module-system)
- [Contributing](#-contributing)
- [Author](#-author)

## ✨ FEATURES

- 🚀 **Parallel Processing**: Configurable multi-threading system for high-performance execution
- 🧩 **Modular Architecture**: Extensible structure with specialized modules (EXT, CLC, OUT, CON, AI)
- 🔄 **Dynamic Template**: Substitution system with `{STRING}` placeholder for flexible manipulation
- 🛠️ **+25 Integrated Functions**: Hash, encoding, requests, validation and random value generation
- 📁 **Multiple Sources**: Support for files, stdin and pipe chaining
- 🎯 **Smart Filtering**: Filter system for selective string processing
- 💾 **Flexible Output**: TXT, CSV and JSON formatting with automatic timestamp
- 🔌 **External Integrations**: APIs, databases and notification services
- 🔍 **Advanced Extraction**: Complex patterns with regex and specialized processing
- 🔒 **OSINT and Pentest**: Features optimized for reconnaissance and security analysis
- 🌐 **Multi-Engine Dorking**: Integration with Google, Bing, Yahoo, DuckDuckGo and others
- 🧠 **AI Integration**: Module for processing with Google Gemini
- 🐋 **Docker Support**: Containerized execution for isolated environments
- 🛡️ **Security Validations**: Protection system against malicious commands with bypass option

## 📦 INSTALLATION

### Requirements
- Python 3.12+
- Linux/MacOS
- Libraries listed in `requirements.txt`

### Quick Installation
```bash
# Clone repository
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x

# Install dependencies
pip install -r requirements.txt

# Make file executable
chmod +x strx

# Test installation with help
./strx -help

# List module types
./strx -types

# List modules and usage examples
./strx -examples

# List functions
./strx -funcs
```

### Creating symbolic link (optional)
```bash
# Check current link
ls -la /usr/local/bin/strx

# If necessary, recreate the link
sudo rm /usr/local/bin/strx
sudo ln -sf $HOME/Documents/string-x/strx /usr/local/bin/strx
```

## ⏫ Git-based Upgrade System
Uses git commands to download new versions
```bash
# Update String-X
./strx -upgrade
```

## 🐋 DOCKER
String-X is available as a Docker image, allowing execution in isolated environments without the need for local dependency installation.

### Building the Image

```bash
# Build Docker image
docker build -t string-x .
```

### Basic Docker Usage

```bash
# Run with default command (shows examples)
docker run --rm string-x

# View help
docker run --rm string-x -h

# List available functions
docker run --rm string-x -funcs

# List module types
docker run --rm string-x -types
```

### Processing Local Files

To process host files, mount the directory as a volume:

```bash
# Mount current directory and process file
docker run --rm -v $(pwd):/data string-x -l /data/urls.txt -st "curl -I {STRING}"

# Process with multiple threads
docker run --rm -v $(pwd):/data string-x -l /data/hosts.txt -st "nmap -p 80,443 {STRING}" -t 20

# Save results on host
docker run --rm -v $(pwd):/data string-x -l /data/domains.txt -st "dig +short {STRING}" -o /data/results.txt
```

### Usage with Modules

```bash
# Extract emails from file
docker run --rm -v $(pwd):/data string-x -l /data/dump.txt -st "echo {STRING}" -module "ext:email" -pm

# Google dorking
docker run --rm -v $(pwd):/data string-x -l /data/dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Collect DNS information
docker run --rm -v $(pwd):/data string-x -l /data/domains.txt -st "echo {STRING}" -module "clc:dns" -pm
```

### Processing via Pipe

```bash
# Host command pipes
echo "github.com" | docker run --rm -i string-x -st "whois {STRING}"

# Combination with host tools
cat urls.txt | docker run --rm -i string-x -st "curl -skL {STRING}" -p "grep '<title>'"

# Complex pipeline
cat domains.txt | docker run --rm -i string-x -st "echo {STRING}" -module "clc:crtsh" -pm | sort -u
```

### Advanced Configurations

```bash
# Use proxy inside container
docker run --rm -v $(pwd):/data string-x -l /data/dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "http://172.17.0.1:8080" -pm

# Define output format
docker run --rm -v $(pwd):/data string-x -l /data/targets.txt -st "echo {STRING}" -format json -o /data/output.json

# Execute with delay between threads
docker run --rm -v $(pwd):/data string-x -l /data/apis.txt -st "curl {STRING}" -t 10 -sleep 2
```

## 🧠 FUNDAMENTAL CONCEPTS

### Template System {STRING}
The tool uses the `{STRING}` placeholder as a keyword for dynamic value substitution. This system allows each input line to be processed individually, replacing `{STRING}` with the current value.

```bash
# Input file
host-01.com.br
host-02.com.br
host-03.com.br

# Command with template
./strx -l hosts.txt -st "host '{STRING}'"

# Generated result
host 'host-01.com.br'
host 'host-02.com.br'
host 'host-03.com.br'
```

### Processing Flow
1. **Input**: Data via file (`-l`) or stdin (pipe)
2. **Template**: Template application with `{STRING}`
3. **Processing**: Command/module execution
4. **Pipe**: Optional additional processing (`-p`)
5. **Output**: Final result (screen or file)

<center>

![Screenshot](/asset/img/fluxo.jpg)

</center>

## 🏗️ MODULAR ARCHITECTURE

String-X uses an extensible modular architecture with four main types of modules:

### Module Types

| Type | Code | Description | Location |
|------|------|-------------|----------|
| **Extractor** | `ext` | Specific data extraction (email, URL, domain, phone) | `utils/auxiliary/ext/` |
| **Collector** | `clc` | Information collection and aggregation (DNS, whois) | `utils/auxiliary/clc/` |
| **Output** | `out` | Result formatting and sending (DB, API, files) | `utils/auxiliary/out/` |
| **Connection** | `con` | Specialized connections (SSH, FTP, etc) | `utils/auxiliary/con/` |

### Directory Structure
```bash
string-x/
      .
      ├── asset             # Images, banners and logos used in documentation and CLI interface
      ├── config            # Global project configuration files (settings, variables)
      ├── core              # Application core, main engine and central logic
      │   └── banner        # Submodule for ASCII art banners
      │       └── asciiart  # ASCII art files for terminal display
      ├── output            # Default directory for output files and logs generated by the tool
      └── utils             # Utilities and auxiliary modules for extensions and integrations
          ├── auxiliary     # Auxiliary modules organized by function
          │   ├── ai        # Artificial intelligence modules (ex: Gemini prompts)
          │   ├── clc       # Collector modules (search, DNS, whois, external APIs)
          │   ├── con       # Connection modules (SSH, FTP, HTTP probe)
          │   ├── ext       # Extractor modules (regex: email, domain, IP, hash, etc)
          │   └── out       # Output/integrator modules (JSON, CSV, database, APIs)
          └── helper        # Utility functions and helpers used throughout the project
```

## 🚀 TOOL USAGE

### Help and Parameters
```bash
./strx -help
```

### Main Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-h, -help`         | Show project help | `-h` |
| `-types`             | List module types | `-types` |
| `-examples`          | List modules and usage examples | `-examples` |
| `-functions, -funcs` | List functions | `-funcs` |
| `-l, -list` | File with strings for processing | `-l hosts.txt` |
| `-st, --str` | Command template with `{STRING}` | `-st "curl {STRING}"` |
| `-o, --out` | Output file for results | `-o results.txt` |
| `-p, -pipe` | Additional command via pipe | `-p "grep 200"` |
| `-v, -verbose` | Verbose mode with levels (1-5 or 'all'). 1=info, 2=warning, 3=debug, 4=error, 5=exception | `-v 3` |
| `-ds, -disable-security` | Disable security validations (use with caution) | `-ds` |
| `-ns, -no-shell` | Process input directly through modules/functions without shell command execution | `-ns` |
| `-t, -thread` | Number of parallel threads | `-t 50` |
| `-f, --filter` | Filter for string selection | `-f ".gov.br"` |
| `-iff` | Function result filter: returns only results containing the specified value | `-iff "admin"` |
| `-ifm` | Module result filter: returns only results containing the specified value | `-ifm "hash"` |
| `-module` | Selection of specific module | `-module "ext:email"` |
| `-pm` | Show only module results | `-pm` |
| `-pf` | Show only function results | `-pf` |
| `-of` | Save function results to file | `-of` |
| `-sleep` | Delay between threads (seconds) | `-sleep 2` |
| `-proxy` | Set proxy for requests | `-proxy "http://127.0.0.1:8080"` |
| `-format` | Output format (txt, csv, json) | `-format json` |
| `-upgrade` | Update String-X via Git | `-upgrade` |
| `-r, -retry` | Number of retry attempts | `-r 3` |

## 💡 PRACTICAL EXAMPLES

### Verbose Levels
String-X offers 5 verbosity levels for detailed output control:

```bash
# Level 1 (info) - Basic information
strx -l domains.txt -st "dig {STRING}" -v 1

# Level 2 (warning) - Warnings and alerts
strx -l urls.txt -st "curl {STRING}" -v 2

# Level 3 (debug) - Detailed debugging information
strx -l targets.txt -st "nmap {STRING}" -v 3

# Level 4 (error) - Execution errors
strx -l data.txt -st "process {STRING}" -v 4

# Level 5 (exception) - Exceptions with stack trace
strx -l complex.txt -st "analyze {STRING}" -v 5

# All levels - Maximum information output
strx -l hosts.txt -st "scan {STRING}" -v all

# Combine multiple levels
strx -l mixed.txt -st "test {STRING}" -v "1,3,4"
```

### No-Shell Mode (-ns / --no-shell)

String-X introduces the **-no-shell** flag that enables direct input processing through modules and functions, **without shell command execution**. This improves security, performance, and usability.

#### Benefits:
- **🔒 Enhanced Security**: Eliminates shell injection risks
- **⚡ Superior Performance**: Removes subprocess overhead
- **💡 Simplified Syntax**: Eliminates need for wrapper commands like `echo {STRING}`

#### Approach Comparison:

```bash
# Traditional Approach
echo "https://example.com" | strx -st "echo {STRING}" -module "ext:url" -pm

# New No-Shell Approach
echo "https://example.com" | strx -st "{STRING}" -module "ext:url" -ns -pm
```

#### Examples with Modules:
```bash
# Direct URL extraction
curl 'https://blog.inurl.com.br' | strx -st "{STRING}" -module 'ext:url' -ns -pm

# Module chaining without shell
strx -l domains.txt -st "{STRING}" -module "ext:url|ext:domain|clc:dns" -ns -pm

# Large dataset processing with better performance
strx -l huge_dataset.txt -st "{STRING}" -module "ext:email" -ns -pm -t 50
```

#### Examples with Functions:
```bash
# Functions directly applied
echo 'https://example.com/path' | strx -st "extract_domain({STRING})" -ns -pf

# Multiple functions
strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -ns -pf
```

### Basic Examples

#### 1. Host Verification
```bash
# Via file
./strx -l hosts.txt -st "host {STRING}" -v

# Via pipe
cat hosts.txt | ./strx -st "host {STRING}" -v
```

#### 2. HTTP Requests with Analysis
```bash
# Check URL status
./strx -l urls.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 20

# Extract page titles
./strx -l domains.txt -st "curl -sL https://{STRING}" -p "grep -o '<title>.*</title>'" -o titles.txt
```

#### 3. Log and Data Analysis
```bash
# Search CPFs in leaks
./strx -l cpfs.txt -st "grep -Ei '{STRING}' -R ./database/" -v

# Process SQL dump
./strx -l dump.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u
```

### Advanced Examples

#### 1. OSINT and Reconnaissance
```bash
# IP information
cat ips.txt | ./strx -st "curl -s 'https://ipinfo.io/{STRING}/json'" -p "jq -r '.org, .country'"

# Phishing verification
./strx -l suspicious.txt -st "curl -skL https://{STRING}/" -p "grep -i 'phish\|scam\|fake'" -t 30

# DNS enumeration
./strx -l subdomains.txt -st "dig +short {STRING}" -module "clc:dns" -pm
```

#### 2. Security and Pentest
```bash
# Port scanning with nmap
./strx -l targets.txt -st "nmap -p 80,443 {STRING}" -p "grep 'open'" -t 10

# SQL injection testing
./strx -l urls.txt -st "sqlmap -u '{STRING}' --batch" -p "grep 'vulnerable'" -o sqli_results.txt

# Directory bruteforce
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

#### 3. Data Processing
```bash
# Extract emails from multiple files
./strx -l files.txt -st "cat {STRING}" -module "ext:email" -pm > all_emails.txt

# Encoding conversion
./strx -l base64_data.txt -st "debase64({STRING})" -pf -of

# Hash generation
./strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -pf -o hashes.txt

# JSON formatting usage
echo 'com.br' | ./strx  -st "echo {STRING}" -o bing.json -format json -module 'clc:bing' -pm -v
```

### Dorking and Search Engines
```bash
# Basic Google dorking
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# Search for PDF files on government sites
echo 'site:gov filetype:pdf "confidential"' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm

# Finding exposed admin panels
echo 'inurl:admin intitle:"login"' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm

# Multiple search engines with same dork
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:duckduckgo" -pm > duckduckgo_results.txt
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:bing" -pm > bing_results.txt

# Compare results between engines
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:google" -pm | sort > google_results.txt
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:bing" -pm | sort > bing_results.txt
comm -23 google_results.txt bing_results.txt > google_exclusive.txt
```

### Dorking with Proxy
```bash
# Using proxy with dorking to avoid blocks
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "http://127.0.0.1:9050" -pm

# Using proxy with authentication
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:yahoo" -proxy "http://user:pass@server:8080" -pm

# Applying dorking with TOR
./strx -l sensitive_dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "https://127.0.0.1:9050" -pm -t 1 -sleep 5

# Dorking with structured output + proxy with authentication
./strx -l sqli_dorks.txt -st "echo {STRING}" -module "clc:googlecse" -proxy "http://user:pass@10.0.0.1:8080" -pm -module "out:json" -pm

# Distributed collection through proxy list
cat proxy_list.txt | while read proxy; do
  ./strx -l target_dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "$proxy" -pm -t 3 -sleep 2
done > combined_results.txt
```

## 🔧 INTEGRATED FUNCTIONS

String-X includes more than 25 built-in functions that can be used within `{STRING}` templates and pipe commands. These functions are processed before shell command execution and cover everything from hash, encoding, string manipulation, random value generation, data analysis, document validation, HTTP requests, file manipulation and much more.

### Syntax
```bash
# Simple function
./strx -l data.txt -st "function({STRING})" -pf

# Multiple functions
./strx -l data.txt -st "{STRING}; md5({STRING}); base64({STRING})" -pf

# Function with parameters
./strx -l data.txt -st "str_rand(10); int_rand(5)" -pf
```

### Available Functions (Main)

| Function | Description | Example |
|----------|-------------|---------|
| `clear` | Remove spaces, tabs and line breaks | `clear({STRING})` |
| `base64` / `debase64` | Encode/decode Base64 | `base64({STRING})` |
| `hex` / `dehex` | Encode/decode hexadecimal | `hex({STRING})` |
| `sha1`, `sha256`, `md5` | Generate hash | `sha256({STRING})` |
| `str_rand`, `int_rand` | Generate random string/number | `str_rand(10)` |
| `ip` | Resolve hostname to IP | `ip({STRING})` |
| `replace` | Replace substring | `replace(http:,https:,{STRING})` |
| `get` | HTTP GET request | `get(https://{STRING})` |
| `urlencode` | URL encode | `urlencode({STRING})` |
| `rev` | Reverse string | `rev({STRING})` |
| `timestamp` | Current timestamp | `timestamp()` |
| `extract_domain` | Extract domain from URL | `extract_domain({STRING})` |
| `jwt_decode` | Decode JWT (payload) | `jwt_decode({STRING})` |
| `whois_lookup` | WHOIS query | `whois_lookup({STRING})` |
| `cert_info` | SSL certificate info | `cert_info({STRING})` |
| `user_agent` | Random User-Agent | `user_agent()` |
| `cidr_expand` | Expand CIDR range | `cidr_expand(192.168.0.0/30)` |
| `subdomain_gen` | Generate common subdomains | `subdomain_gen({STRING})` |
| `email_validator` | Validate email | `email_validator({STRING})` |
| `hash_file` | File hashes | `hash_file(path.txt)` |
| `encode_url_all` | URL encode (everything) | `encode_url_all({STRING})` |
| `phone_format` | Format BR phone | `phone_format({STRING})` |
| `password_strength` | Password strength | `password_strength({STRING})` |
| `social_media_extract` | Extract social handles | `social_media_extract({STRING})` |
| `leak_check_format` | Format email for leaks | `leak_check_format({STRING})` |
| `cpf_validate` | Validate CPF | `cpf_validate({STRING})` |

> See the complete list and examples in `utils/helper/functions.py` or use `-functions` in CLI for detailed documentation.

#### Hashing and Encoding
```bash
# Generate multiple hashes
./strx -l passwords.txt -st "md5({STRING}); sha1({STRING}); sha256({STRING})" -pf

# Work with Base64
./strx -l data.txt -st "base64({STRING})" -pf
echo "SGVsbG8gV29ybGQ=" | ./strx -st "debase64({STRING})" -pf
```

#### Random Value Generation
```bash
# Generate random strings
./strx -l domains.txt -st "https://{STRING}/admin?token=str_rand(32)" -pf

# Generate random numbers
./strx -l apis.txt -st "curl '{STRING}?id=int_rand(6)'" -pf
```

#### Requests and Resolution
```bash
# Resolve IPs
./strx -l hosts.txt -st "{STRING}; ip({STRING})" -pf

# Make GET requests
./strx -l urls.txt -st "get(https://{STRING})" -pf
```

#### String Manipulation
```bash
# Replace protocols
./strx -l urls.txt -st "replace(http:,https:,{STRING})" -pf

# Reverse strings
./strx -l data.txt -st "rev({STRING})" -pf

# URL encoding
./strx -l params.txt -st "urlencode({STRING})" -pf
```

### Control Parameters

- **`-pf`**: Show only function results (ignore shell execution)
- **`-of`**: Save function results to output file

```bash
# Only show function results
./strx -l domains.txt -st "{STRING}; md5({STRING})" -pf

# Save functions to file
./strx -l data.txt -st "base64({STRING})" -pf -of -o encoded.txt
```

### Function Example
> **💡 Tip**: You can add custom functions by editing the file `utils/helper/functions.py`
```python
@staticmethod
def check_admin_example(value: str) -> str:
  try:
      if '<p>admin</p>' in value:
        return value
  except:
    return str()
```

### Using the example function
```bash
# Executing the created function
./strx -l data.txt -st "check_admin_example({STRING})" -pf
```

## 🧩 MODULE SYSTEM

String-X uses an extensible modular architecture that allows adding specific functionalities without modifying the main code. Modules are organized by type and loaded dynamically.

### Available Module Types

| Type | Code | Description | Location |
|------|------|-------------|----------|
| **Extractor** | `ext` | Specific data extraction using regex | `utils/auxiliary/ext/` |
| **Collector** | `clc` | Information collection from APIs/services | `utils/auxiliary/clc/` |
| **Output** | `out` | Data formatting and sending | `utils/auxiliary/out/` |
| **Connection** | `con` | Specialized connections | `utils/auxiliary/con/` |
| **AI** | `ai` | Artificial intelligence | `utils/auxiliary/ai/` |

#### Basic Syntax
```bash
./strx -module "type:module_name"
```

#### Related Parameters
- **`-module type:name`**: Specifies the module to be used
- **`-pm`**: Shows only module results (omits shell output)

### Extractor Modules (EXT)
Modules for extracting patterns and specific data using regex:

| Module      | Description                                 | CLI Example |
|-------------|---------------------------------------------|-------------|
| `email`     | Extract valid email addresses              | `-module "ext:email"` |
| `domain`    | Extract domains and subdomains             | `-module "ext:domain"` |
| `url`       | Extract complete URLs (HTTP/HTTPS)         | `-module "ext:url"` |
| `phone`     | Extract phone numbers (BR)                 | `-module "ext:phone"` |
| `credential`| Extract credentials, tokens, keys          | `-module "ext:credential"` |
| `ip`        | Extract IPv4/IPv6 addresses                | `-module "ext:ip"` |
| `hash`      | Extract MD5, SHA1, SHA256, SHA512 hashes   | `-module "ext:hash"` |

```bash
# Example: Extract emails from data dump
./strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm
```

### Collector Modules (CLC)
Modules for external information collection, APIs and analysis:

| Module        | Description                                 | CLI Example |
|---------------|---------------------------------------------|-------------|
| `archive`     | Collect archived URLs from Wayback Machine | `-module "clc:archive"` |
| `bing`        | Perform dork searches on Bing              | `-module "clc:bing"` |
| `crtsh`       | Collect SSL/TLS certificates and subdomains| `-module "clc:crtsh"` |
| `dns`         | Collect DNS records (A, MX, TXT, NS)       | `-module "clc:dns"` |
| `duckduckgo`  | Perform dork searches on DuckDuckGo        | `-module "clc:duckduckgo"` |
| `emailverify` | Verify email validity (MX, SMTP)           | `-module "clc:emailverify"` |
| `ezilon`      | Perform dork searches on Ezilon            | `-module "clc:ezilon"` |
| `geoip`       | IP geolocation                             | `-module "clc:geoip"` |
| `google`      | Perform dork searches on Google            | `-module "clc:google"` |
| `googlecse`   | Perform dork searches using Google CSE     | `-module "clc:googlecse"` |
| `http_probe`  | HTTP/HTTPS probing, header analysis        | `-module "clc:http_probe"` |
| `ipinfo`      | IP/host port scanner                       | `-module "clc:ipinfo"` |
| `lycos`       | Perform dork searches on Lycos             | `-module "clc:lycos"` |
| `naver`       | Perform dork searches on Naver (Korean)    | `-module "clc:naver"` |
| `netscan`     | Network scanner (hosts, services)          | `-module "clc:netscan"` |
| `shodan`      | Query Shodan API                           | `-module "clc:shodan"` |
| `sogou`       | Perform dork searches on Sogou (Chinese)   | `-module "clc:sogou"` |
| `spider`      | Web spider for recursive URL collection    | `-module "clc:spider"` |
| `subdomain`   | Subdomain enumeration                      | `-module "clc:subdomain"` |
| `virustotal`  | Query VirusTotal API                       | `-module "clc:virustotal"` |
| `whois`       | Domain WHOIS query                         | `-module "clc:whois"` |
| `yahoo`       | Perform dork searches on Yahoo             | `-module "clc:yahoo"` |

```bash
# Example: Collect DNS information
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm

# Example: Collect information using search engines
./strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:googlecse" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:duckduckgo" -pm

# Example: Probe and analyze web servers
./strx -l urls.txt -st "echo {STRING}" -module "clc:http_probe" -pm

# Examples with specific dorking
echo 'site:fbi.gov filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:google" -pm
echo 'site:github.com inurl:admin' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm
echo 'inurl:admin' | ./strx -st "echo {STRING}" -module "clc:lycos" -pm
echo 'site:github.com' | ./strx -st "echo {STRING}" -module "clc:ezilon" -pm
echo 'filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm
```

### Output Modules (OUT)
Modules for output and result formatting:

| Module        | Description                                 | CLI Example |
|---------------|---------------------------------------------|-------------|
| `json`        | Save results to JSON                       | `-module "out:json"` |
| `csv`         | Save results to CSV                        | `-module "out:csv"` |
| `xml`         | Save results to XML                        | `-module "out:xml"` |

```bash
# Example: Save to JSON
./strx -l data.txt -st "process {STRING}" -module "out:json" -pm
```

### Connection Modules (CON)
Modules for connecting to external services and integrating results:

| Module        | Description                                 | CLI Example |
|---------------|---------------------------------------------|-------------|
| `sqlite`      | Save data to SQLite database               | `-module "con:sqlite"` |
| `mysql`       | Save data to MySQL database                | `-module "con:mysql"` |
| `telegram`    | Send results via Telegram Bot              | `-module "con:telegram"` |
| `slack`       | Send results via Slack Webhook             | `-module "con:slack"` |
| `opensearch`  | Index results in Open Search               | `-module "con:opensearch"` |
| `ftp`         | Connection and transfer via FTP            | `-module "con:ftp"` |
| `ssh`         | Execute commands via SSH                   | `-module "con:ssh"` |
| `s3`          | Upload/download data to Amazon S3          | `-module "con:s3"` |

```bash
# Example: Save to SQLite
./strx -l data.txt -st "process {STRING}" -module "con:sqlite" -pm
```


### Artificial Intelligence Modules (AI)
Modules for AI prompts:

| Module        | Description                                 | CLI Example |
|---------------|---------------------------------------------|-------------|
| `gemini`      | Prompt for Google Gemini AI - ([Create API Key](https://aistudio.google.com/app/apikey)) | `-module "ai:gemini"` |

```bash
# Example: Using files with Prompts
./strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm

# Example: Collect URLs and send for analysis building Prompt
./strx -l urls.txt -st "echo 'Analyze URL: {STRING}'" -module "ai:gemini" -pm
```

### Developing New Modules

To create new modules, follow the standard structure:

#### Extractor Module (ext)
```python
"""
Module introduction
"""
from core.basemodule import BaseModule
import re

class ModuleName(BaseModule):
    
    def __init__(self):
      super().__init__()

      # Define module meta information
      self.meta.update({
          "name": "Module name...",
          "description": "Describe the module...",
          "author": "Creator name...",
          "type": "extractor | collector | Output..."
      })

      # Define required options for this module
      self.options = {
          "data":   str(),
          "regex":  str(),
          "proxy":  str()
      }
    
    # Mandatory function for execution
    def run(self):
        """
        Context for module logic
          > Access options information via: self.options.get(key_name)
        """
        # Save module execution information
        self.set_result(value_regex)
```

### Filters and Modules

You can combine filters with modules for more specific processing:

```bash
# Extract only .gov emails
./strx -l data.txt -st "echo '{STRING}'" -module "ext:email" -pm -f ".gov"

# DNS lookup only for .br domains
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm -f ".br"
```

## 🎯 FILTERS AND SELECTIVE PROCESSING

The filter system allows processing only strings that meet specific criteria, optimizing performance and precision.

### Using Filters
```bash
./strx -f "filter_value" / ./strx --filter "filter_value"
```

### Filter Examples
```bash
# Filter only .gov.br domains
./strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# Filter only HTTPS URLs
./strx -l urls.txt -st "curl {STRING}" -f "https"

# Filter specific IPs
./strx -l logs.txt -st "analyze {STRING}" -f "192.168"

# Filter file extensions
./strx -l files.txt -st "process {STRING}" -f ".pdf"

# Filter only function results containing "admin"
./strx -l urls.txt -st "{STRING}; md5({STRING})" -pf -iff "admin"

# Filter only module results containing specific hash
./strx -l domains.txt -st "echo {STRING}" -module "ext:hash" -pm -ifm "a1b2c3"

# Combine function and module filters
./strx -l data.txt -st "{STRING}; md5({STRING})" -module "ext:domain" -pf -pm -iff "google" -ifm "admin"
```

## ⚡ PARALLEL PROCESSING

String-X supports parallel processing through threads to accelerate operations on large data volumes.

### Thread Configuration
```bash
# Define number of threads
./strx -t 50 / ./strx -thread 50

# Define delay between threads
./strx -sleep 2
```

### Examples with Threading
```bash
# Fast HTTP status verification
./strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# Mass DNS resolution
./strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1

# Port scanning
./strx -l ip_list.txt -st "nmap -p 80,443 {STRING}" -t 20 -sleep 3
```

### Threading Best Practices
- **Rate limiting**: Use `-sleep` to avoid service overload
- **Adequate number**: Adjust `-t` according to available resources
- **Monitoring**: Use `-v 1` for basic info, `-v 3` for detailed debug, `-v all` for maximum control

### Large File Processing
String-X has been optimized to process large files efficiently:
```bash
# Process large file with multiple threads
strx -l large_file.txt -st "echo {STRING}" -module "ext:email" -pm -t 20 -sleep 1

# For very large files, use fewer threads and more delay
strx -l huge_dataset.txt -st "process {STRING}" -t 10 -sleep 2 -v
```

## 🛡️ SECURITY SYSTEM

String-X includes security validations to prevent execution of malicious commands:

### Active Validations
- **Input size**: Limits input data to 1MB by default
- **String quantity**: Maximum of 10,000 strings per execution
- **Dangerous patterns**: Detects and blocks potentially malicious commands
- **Threads**: Limits concurrent threads to avoid system overload

### Disabling Security Validations
**⚠️ WARNING**: Use only when necessary and you trust the content

```bash
# Disable validations for legitimate complex commands
strx -l data.txt -st "echo {STRING}; md5sum {STRING}" -ds

# Process large files without limitations
strx -l huge_file.txt -st "process {STRING}" -ds -t 50

# Use with functions that may generate patterns detected as suspicious
echo "test" | strx -st "echo {STRING}; echo 'result'" -ds
```

### Debug Mode for Security
```bash
# See security validation details (full debug)
strx -l data.txt -st "command {STRING}" -v 3

# Check why a command was blocked
strx -s "test" -st "suspicious_command" -v 3
```

## 📸 VISUAL EXAMPLES

### Basic Execution
**Command**: `cat hosts.txt | ./strx -str 'host {STRING}'`

![Screenshot](/asset/img/img1.png)

### Processing with Threading
**Command**: `cat hosts.txt | ./strx -str "curl -Iksw 'CODE:%{response_code};IP:%{remote_ip};HOST:%{url.host};SERVER:%header{server}' https://{STRING}" -p "grep -o -E 'CODE:.(.*)|IP:.(.*)|HOST:.(.*)|SERVER:.(.*)'" -t 30`

![Screenshot](/asset/img/img3.png)

### Verbose Mode
**Command**: `cat hosts.txt | ./strx -str 'host {STRING}' -v`

![Screenshot](/asset/img/img2.png)

### Output File Format
```
output-%d-%m-%Y-%H.txt > output-15-06-2025-11.txt
```

## 🤝 CONTRIBUTING

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Types of Contribution
- 🐛 **Bug fixes**
- ✨ **New features**
- 📝 **Documentation improvements**
- 🧩 **New modules**
- ⚡ **Performance optimizations**

### Module Development
To create new modules, consult the [Module System](#-module-system) section and follow established patterns.

## 📄 LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 AUTHOR

**MrCl0wn**
- 🌐 **Blog**: [http://blog.mrcl0wn.com](http://blog.mrcl0wn.com)
- 🐙 **GitHub**: [@MrCl0wnLab](https://github.com/MrCl0wnLab) | [@MrCl0wnLab](https://github.com/MrCl0wnLab)
- 🐦 **Twitter**: [@MrCl0wnLab](https://twitter.com/MrCl0wnLab)
- 📧 **Email**: mrcl0wnlab@gmail.com

---

<div align="center">

**⭐ If this project was useful, consider giving it a star!**

**💡 Suggestions and feedback are always welcome!**

**💀 Hacker Hackeia!**

</div>
