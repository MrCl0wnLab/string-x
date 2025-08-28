<center>

<h1 align="center">
  <a href="#/"><img src="./asset/img/logo.png"></a>
</h1>

<h4 align="center">字符串操作自动化工具</h4>

<p align="center">
String-X (strx) 是一个专为信息安全专业人员和黑客爱好者开发的模块化自动化工具。专注于Linux环境中的动态字符串操作。

采用模块化架构，为OSINT、渗透测试和数据分析提供高级功能，包括并行处理、专业化提取模块、收集功能和外部API集成。基于灵活模板的系统，集成超过25个功能。
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

## 📋 目录

- [特性](#-特性)
- [安装](#-安装)
- [基本概念](#-基本概念)
- [模块化架构](#-模块化架构)
- [工具使用](#-工具使用)
- [实际示例](#-实际示例)
- [集成函数](#-集成函数)
- [模块系统](#-模块系统)
- [贡献](#-贡献)
- [作者](#-作者)

## ✨ 特性

- 🚀 **并行处理**：可配置的多线程系统，实现高性能执行
- 🧩 **模块化架构**：可扩展结构，包含专业化模块(EXT、CLC、OUT、CON、AI)
- 🔄 **动态模板**：使用`{STRING}`占位符的替换系统，实现灵活操作
- 🛠️ **25+集成函数**：哈希、编码、请求、验证和随机值生成
- 📁 **多种数据源**：支持文件、stdin和管道链
- 🎯 **智能过滤**：用于选择性字符串处理的过滤系统
- 💾 **灵活输出**：TXT、CSV和JSON格式，自动时间戳
- 🔌 **外部集成**：API、数据库和通知服务
- 🔍 **高级提取**：复杂正则表达式模式和专业化处理
- 🔒 **OSINT和渗透测试**：优化的侦察和安全分析资源
- 🌐 **多引擎探查**：集成Google、Bing、Yahoo、DuckDuckGo等
- 🧠 **AI集成**：Google Gemini处理模块
- 🐋 **Docker支持**：隔离环境的容器化执行
- 🛡️ **安全验证**：防止恶意命令的保护系统，带有绕过选项

## 📦 安装

### 系统要求
- Python 3.12+
- Linux/MacOS
- `requirements.txt`中列出的库

### 快速安装
```bash
# 克隆仓库
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x

# 安装依赖
pip install -r requirements.txt

# 设置可执行权限
chmod +x strx

# 测试安装并查看帮助
./strx -help

# 列出模块类型
./strx -types

# 列出模块和使用示例
./strx -examples

# 列出函数
./strx -funcs

```

### 创建符号链接(可选) 
```bash
# 检查当前链接
ls -la /usr/local/bin/strx

# 如有必要，重新创建链接
sudo rm /usr/local/bin/strx
sudo ln -sf $HOME/Documentos/string-x/strx /usr/local/bin/strx
```

## ⏫ 基于Git的升级系统
使用git命令下载新版本
```bash
# 更新String-X
./strx -upgrade
```

## 🐋 DOCKER
String-X提供Docker镜像，允许在隔离环境中运行，无需本地安装依赖。

### 构建镜像

```bash
# 构建Docker镜像
docker build -t string-x .
```

### Docker基本使用

```bash
# 使用默认命令运行（显示示例）
docker run --rm string-x

# 查看帮助
docker run --rm string-x -h

# 列出可用函数
docker run --rm string-x -funcs

# 列出模块类型
docker run --rm string-x -types
```

### 处理本地文件

为了处理主机文件，将目录挂载为卷：

```bash
# 挂载当前目录并处理文件
docker run --rm -v $(pwd):/dados string-x -l /dados/urls.txt -st "curl -I {STRING}"

# 使用多线程处理
docker run --rm -v $(pwd):/dados string-x -l /dados/hosts.txt -st "nmap -p 80,443 {STRING}" -t 20

# 将结果保存到主机
docker run --rm -v $(pwd):/dados string-x -l /dados/domains.txt -st "dig +short {STRING}" -o /dados/results.txt
```

### 使用模块

```bash
# 从文件提取邮箱
docker run --rm -v $(pwd):/dados string-x -l /dados/dump.txt -st "echo {STRING}" -module "ext:email" -pm

# Google探查
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# 收集DNS信息
docker run --rm -v $(pwd):/dados string-x -l /dados/domains.txt -st "echo {STRING}" -module "clc:dns" -pm
```

### 通过管道处理

```bash
# 从主机命令的管道
echo "github.com" | docker run --rm -i string-x -st "whois {STRING}"

# 与主机工具结合
cat urls.txt | docker run --rm -i string-x -st "curl -skL {STRING}" -p "grep '<title>'"

# 复杂管道
cat domains.txt | docker run --rm -i string-x -st "echo {STRING}" -module "clc:crtsh" -pm | sort -u
```

### 高级配置

```bash
# 在容器内使用代理
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "http://172.17.0.1:8080" -pm

# 定义输出格式
docker run --rm -v $(pwd):/dados string-x -l /dados/targets.txt -st "echo {STRING}" -format json -o /dados/output.json

# 设置线程间延迟执行
docker run --rm -v $(pwd):/dados string-x -l /dados/apis.txt -st "curl {STRING}" -t 10 -sleep 2
```


## 🧠 基本概念

### {STRING} 模板系统
工具使用`{STRING}`占位符作为动态值替换的关键字。此系统允许单独处理每个输入行，将`{STRING}`替换为当前值。

```bash
# 输入文件
host-01.com.br
host-02.com.br
host-03.com.br

# 使用模板的命令
./strx -l hosts.txt -st "host '{STRING}'"

# 生成的结果
host 'host-01.com.br'
host 'host-02.com.br'
host 'host-03.com.br'
```

### 处理流程
1. **输入**：通过文件(`-l`)或stdin(管道)获取数据
2. **模板**：应用带有`{STRING}`的模板
3. **处理**：执行命令/模块
4. **管道**：可选的额外处理(`-p`)
5. **输出**：最终结果(屏幕或文件)

<center>

![Screenshot](/asset/img/fluxo.jpg)

</center>

## 🏗️ 模块化架构

String-X使用可扩展的模块化架构，包含四种主要模块类型：

### 模块类型

| 类型 | 代码 | 描述 | 位置 |
|------|--------|-----------|-------------|
| **Extractor** | `ext` | 特定数据提取(email、URL、domain、phone) | `utils/auxiliary/ext/` |
| **Collector** | `clc` | 信息收集和聚合(DNS、whois) | `utils/auxiliary/clc/` |
| **Output** | `out` | 结果格式化和发送(DB、API、files) | `utils/auxiliary/out/` |
| **Connection** | `con` | 专业化连接(SSH、FTP等) | `utils/auxiliary/con/` |

### 目录结构
```bash
string-x/
      .
      ├── asset             # 文档和CLI界面使用的图片、横幅和标志
      ├── config            # 项目的全局配置文件(settings、变量)
      ├── core              # 应用核心、主引擎和中央逻辑
      │   └── banner        # ASCII艺术横幅子模块
      │       └── asciiart  # 终端显示的ASCII艺术文件
      ├── output            # 工具生成的输出文件和日志的默认目录
      └── utils             # 扩展和集成的实用工具和辅助模块
          ├── auxiliary     # 按功能组织的辅助模块
          │   ├── ai        # 人工智能模块(例：Gemini提示)
          │   ├── clc       # 收集器模块(搜索、DNS、whois、外部API)
          │   ├── con       # 连接模块(SSH、FTP、HTTP探测)
          │   ├── ext       # 提取器模块(正则表达式：email、域名、IP、哈希等)
          │   └── out       # 输出/集成模块(JSON、CSV、数据库、API)
          └── helper        # 整个项目使用的实用函数和辅助工具
```

## 🚀 工具使用

### 帮助和参数
```bash
./strx -help
```

### 主要参数

| 参数 | 描述 | 示例 |
|-----------|-----------|---------|
| `-h, -help`         | 显示项目帮助 | `-h` |
| `-types`             | 列出模块类型 | `-types` |
| `-examples`          | 列出模块和使用示例 | `-examples` |
| `-functions, -funcs` | 列出函数 | `-funcs` |
| `-l, -list` | 包含处理字符串的文件 | `-l hosts.txt` |
| `-st, --str` | 带有`{STRING}`的命令模板 | `-st "curl {STRING}"` |
| `-o, --out` | 结果输出文件 | `-o results.txt` |
| `-p, -pipe` | 通过管道的额外命令 | `-p "grep 200"` |
| `-v, -verbose` | 详细模式带级别 (1-5 或 'all'). 1=信息, 2=警告, 3=调试, 4=错误, 5=异常 | `-v 3` |
| `-ds, -disable-security` | 禁用安全验证(谨慎使用) | `-ds` |
| `-ns, -no-shell` | 直接通过模块/函数处理输入而无需执行shell命令 | `-ns` |
| `-t, -thread` | 并行线程数 | `-t 50` |
| `-f, --filter` | 字符串选择过滤器 | `-f ".gov.br"` |
| `-iff` | 函数结果过滤器：仅返回包含指定值的结果 | `-iff "admin"` |
| `-ifm` | 模块结果过滤器：仅返回包含指定值的结果 | `-ifm "hash"` |
| `-module` | 选择特定模块 | `-module "ext:email"` |
| `-pm` | 仅显示模块结果 | `-pm` |
| `-pf` | 仅显示函数结果 | `-pf` |
| `-of` | 将函数结果保存到文件 | `-of` |
| `-sleep` | 线程间延迟(秒) | `-sleep 2` |
| `-proxy` | 为请求设置代理 | `-proxy "http://127.0.0.1:8080"` |
| `-format` | 输出格式(txt、csv、json) | `-format json` |
| `-upgrade` | 通过Git更新String-X | `-upgrade` |
| `-r, -retry` | 重试次数 | `-r 3` |

### 应用界面

```bash
usage: strx [-h] [-types] [-examples] [-functions] [-list file] [-str cmd] 
            [-out file] [-pipe cmd] [-verbose] [-debug] [-thread <10>] [-pf] [-of] 
            [-filter value] [-sleep <5>] [-module <type:module>] [-pm] [-proxy PROXY]
            [-format <format>] [-upgrade] [-retry <0>]

 
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
                                
                              String-X: Tool for automating commands  1.0

options:
             -h, -help             show this help message and exit
             -types                 列出模块类型
             -examples              列出模块和使用示例
             -functions, -funcs     列出函数
             -list, -l file         执行字符串的文件
             -str, -st cmd          命令字符串模板
             -out, -o file          shell执行值的输出文件
             -pipe, -p cmd          将在管道 | 后执行的命令
             -verbose, -v           详细模式
             -debug                 启用模块调试
             -thread, -t <10>       线程数量
             -pf                    显示函数执行结果，忽略shell
             -of                    启用函数执行值的输出
             -filter, -f value      过滤执行字符串的值
             -iff value             函数结果过滤器：仅返回包含指定值的结果
             -ifm value             模块结果过滤器：仅返回包含指定值的结果
             -sleep <5>             线程间延迟秒数
             -module <type:module>  选择类型和模块
             -pm                    仅显示模块执行结果
             -proxy PROXY           为请求设置代理
             -format <format>       输出格式(txt、csv、json)
             -upgrade               通过Git更新String-X
             -retry, -r <0>         重试次数


```

## 💡 实际示例

### 详细级别
String-X提供5个详细级别以进行详细的输出控制：

```bash
# 级别 1 (info) - 基本信息
strx -l domains.txt -st "dig {STRING}" -v 1

# 级别 2 (warning) - 警告和提醒
strx -l urls.txt -st "curl {STRING}" -v 2

# 级别 3 (debug) - 详细调试信息
strx -l targets.txt -st "nmap {STRING}" -v 3

# 级别 4 (error) - 执行错误
strx -l data.txt -st "process {STRING}" -v 4

# 级别 5 (exception) - 异常与堆栈跟踪
strx -l complex.txt -st "analyze {STRING}" -v 5

# 所有级别 - 最大信息输出
strx -l hosts.txt -st "scan {STRING}" -v all

# 组合多个级别
strx -l mixed.txt -st "test {STRING}" -v "1,3,4"
```

### No-Shell 模式 (-ns / --no-shell)

String-X 引入了 **-no-shell** 标志，允许直接通过模块和函数处理输入，**无需执行shell命令**。这提高了安全性、性能和可用性。

#### 优势:
- **🔒 增强安全性**: 消除shell注入风险
- **⚡ 卓越性能**: 移除子进程开销
- **💡 简化语法**: 消除对包装命令如 `echo {STRING}` 的需求

#### 方法比较:

```bash
# 传统方法
echo "https://example.com" | strx -st "echo {STRING}" -module "ext:url" -pm

# 新的No-Shell方法
echo "https://example.com" | strx -st "{STRING}" -module "ext:url" -ns -pm
```

#### 模块示例:
```bash
# 直接URL提取
curl 'https://blog.inurl.com.br' | strx -st "{STRING}" -module 'ext:url' -ns -pm

# 无shell的模块链接
strx -l domains.txt -st "{STRING}" -module "ext:url|ext:domain|clc:dns" -ns -pm

# 大数据集处理，性能更佳
strx -l huge_dataset.txt -st "{STRING}" -module "ext:email" -ns -pm -t 50
```

#### 函数示例:
```bash
# 直接应用函数
echo 'https://example.com/path' | strx -st "extract_domain({STRING})" -ns -pf

# 多重函数
strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -ns -pf
```

### 基本示例

#### 1. 主机验证
```bash
# 通过文件
./strx -l hosts.txt -st "host {STRING}" -v

# 通过管道
cat hosts.txt | ./strx -st "host {STRING}" -v
```

#### 2. HTTP请求与分析
```bash
# 检查URL状态
./strx -l urls.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 20

# 提取页面标题
./strx -l domains.txt -st "curl -sL https://{STRING}" -p "grep -o '<title>.*</title>'" -o titles.txt
```

#### 3. 日志和数据分析
```bash
# 在泄露中搜索CPF
./strx -l cpfs.txt -st "grep -Ei '{STRING}' -R ./database/" -v

# 处理SQL转储
./strx -l dump.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u
```

### 高级示例

#### 1. OSINT和侦察
```bash
# IP信息
cat ips.txt | ./strx -st "curl -s 'https://ipinfo.io/{STRING}/json'" -p "jq -r '.org, .country'"

# 钓鱼验证
./strx -l suspicious.txt -st "curl -skL https://{STRING}/" -p "grep -i 'phish\|scam\|fake'" -t 30

# DNS枚举
./strx -l subdomains.txt -st "dig +short {STRING}" -module "clc:dns" -pm
```

#### 2. 安全和渗透测试
```bash
# 使用nmap进行端口扫描
./strx -l targets.txt -st "nmap -p 80,443 {STRING}" -p "grep 'open'" -t 10

# SQL注入测试
./strx -l urls.txt -st "sqlmap -u '{STRING}' --batch" -p "grep 'vulnerable'" -o sqli_results.txt

# 目录暴力破解
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

#### 3. 数据处理
```bash
# 从多个文件提取邮箱
./strx -l files.txt -st "cat {STRING}" -module "ext:email" -pm > all_emails.txt

# 编码转换
./strx -l base64_data.txt -st "debase64({STRING})" -pf -of

# 生成哈希
./strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -pf -o hashes.txt

# 使用json格式
echo 'com.br' | ./strx  -st "echo {STRING}" -o bing.json -format json -module 'clc:bing' -pm -v
```

### 与系统管道结合
```bash
# 使用jq的复杂管道
curl -s 'https://api.github.com/users' | jq -r '.[].login' | ./strx -st "curl -s 'https://api.github.com/users/{STRING}'" -p "jq -r '.name, .location'"

# Apache日志处理
cat access.log | awk '{print $1}' | sort -u | ./strx -st "whois {STRING}" -p "grep -i 'country'" -t 5

# SSL证书分析
./strx -l domains.txt -st "echo | openssl s_client -connect {STRING}:443 2>/dev/null" -p "openssl x509 -noout -subject"
```

### 探查和搜索引擎
```bash
# Google基本探查
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# 在政府网站搜索PDF文件
echo 'site:gov filetype:pdf "confidential"' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm

# 查找暴露的管理面板
echo 'inurl:admin intitle:"login"' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm

# 使用相同探查的多个搜索引擎
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:duckduckgo" -pm > duckduckgo_results.txt
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:bing" -pm > bing_results.txt

# 引擎间结果比较
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:google" -pm | sort > google_results.txt
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:bing" -pm | sort > bing_results.txt
comm -23 google_results.txt bing_results.txt > google_exclusive.txt
```

### 使用代理进行探查
```bash
# 使用代理进行探查以避免封锁
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "http://127.0.0.1:9050" -pm

# 使用认证代理
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:yahoo" -proxy "http://user:pass@server:8080" -pm

# 使用TOR进行探查
./strx -l sensitive_dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "https://127.0.0.1:9050" -pm -t 1 -sleep 5

# 结构化输出探查 + 认证代理
./strx -l sqli_dorks.txt -st "echo {STRING}" -module "clc:googlecse" -proxy "http://user:pass@10.0.0.1:8080" -pm -module "out:json" -pm

# 通过代理列表的分布式收集
cat proxy_list.txt | while read proxy; do
  ./strx -l target_dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "$proxy" -pm -t 3 -sleep 2
done > combined_results.txt
```

## 🔧 集成函数


String-X包含超过25个内置函数，可在模板`{STRING}`和管道命令中使用。这些函数在shell命令执行前处理，涵盖哈希、编码、字符串操作、随机值生成、数据分析、文档验证、HTTP请求、文件操作等。

### 语法
```bash
# 简单函数
./strx -l data.txt -st "funcao({STRING})" -pf

# 多个函数
./strx -l data.txt -st "{STRING}; md5({STRING}); base64({STRING})" -pf

# 带参数的函数
./strx -l data.txt -st "str_rand(10); int_rand(5)" -pf
```


### 可用函数(主要)

| 函数 | 描述 | 示例 |
|--------|-----------|---------|
| `clear` | 删除空格、制表符和换行符 | `clear({STRING})` |
| `base64` / `debase64` | Base64编码/解码 | `base64({STRING})` |
| `hex` / `dehex` | 十六进制编码/解码 | `hex({STRING})` |
| `sha1`, `sha256`, `md5` | 生成哈希 | `sha256({STRING})` |
| `str_rand`, `int_rand` | 生成随机字符串/数字 | `str_rand(10)` |
| `ip` | 将主机名解析为IP | `ip({STRING})` |
| `replace` | 替换子字符串 | `replace(http:,https:,{STRING})` |
| `get` | HTTP GET请求 | `get(https://{STRING})` |
| `urlencode` | URL编码 | `urlencode({STRING})` |
| `rev` | 反转字符串 | `rev({STRING})` |
| `timestamp` | 当前时间戳 | `timestamp()` |
| `extract_domain` | 从URL提取域名 | `extract_domain({STRING})` |
| `jwt_decode` | 解码JWT(载荷) | `jwt_decode({STRING})` |
| `whois_lookup` | WHOIS查询 | `whois_lookup({STRING})` |
| `cert_info` | SSL证书信息 | `cert_info({STRING})` |
| `user_agent` | 随机User-Agent | `user_agent()` |
| `cidr_expand` | 展开CIDR范围 | `cidr_expand(192.168.0.0/30)` |
| `subdomain_gen` | 生成常见子域名 | `subdomain_gen({STRING})` |
| `email_validator` | 验证邮箱 | `email_validator({STRING})` |
| `hash_file` | 文件哈希 | `hash_file(path.txt)` |
| `encode_url_all` | URL编码(全部) | `encode_url_all({STRING})` |
| `phone_format` | 格式化巴西电话 | `phone_format({STRING})` |
| `password_strength` | 密码强度 | `password_strength({STRING})` |
| `social_media_extract` | 提取社交媒体句柄 | `social_media_extract({STRING})` |
| `leak_check_format` | 格式化邮箱用于泄露检查 | `leak_check_format({STRING})` |
| `cpf_validate` | 验证CPF | `cpf_validate({STRING})` |


> 查看`utils/helper/functions.py`中的完整列表和示例，或在CLI中使用`-functions`获取详细文档。

#### 哈希和编码
```bash
# 生成多个哈希
./strx -l passwords.txt -st "md5({STRING}); sha1({STRING}); sha256({STRING})" -pf

# 使用Base64
./strx -l data.txt -st "base64({STRING})" -pf
echo "SGVsbG8gV29ybGQ=" | ./strx -st "debase64({STRING})" -pf
```

#### 随机值生成
```bash
# 生成随机字符串
./strx -l domains.txt -st "https://{STRING}/admin?token=str_rand(32)" -pf

# 生成随机数字
./strx -l apis.txt -st "curl '{STRING}?id=int_rand(6)'" -pf
```

#### 请求和解析
```bash
# 解析IP
./strx -l hosts.txt -st "{STRING}; ip({STRING})" -pf

# 发送GET请求
./strx -l urls.txt -st "get(https://{STRING})" -pf
```

#### 字符串操作
```bash
# 替换协议
./strx -l urls.txt -st "replace(http:,https:,{STRING})" -pf

# 反转字符串
./strx -l data.txt -st "rev({STRING})" -pf

# URL编码
./strx -l params.txt -st "urlencode({STRING})" -pf
```

### 控制参数

- **`-pf`**: 仅显示函数结果(忽略shell执行)
- **`-of`**: 将函数结果保存到输出文件

```bash
# 仅显示函数结果
./strx -l domains.txt -st "{STRING}; md5({STRING})" -pf

# 将函数保存到文件
./strx -l data.txt -st "base64({STRING})" -pf -of -o encoded.txt
```

### 函数示例
> **💡 提示**: 您可以通过编辑`utils/helper/functions.py`文件添加自定义函数
```python
@staticmethod
def check_admin_exemplo(value: str) -> str:
  try:
      if '<p>admin</p>' in value:
        return value
  except:
    return str()
```

### 使用示例函数
```bash
# 执行创建的函数
./strx -l data.txt -st "check_admin_exemplo({STRING})" -pf
```


## 🧩 模块系统

String-X使用可扩展的模块化架构，允许在不修改主代码的情况下添加特定功能。模块按类型组织并动态加载。

### 可用模块类型

| 类型 | 代码 | 描述 | 位置 |
|------|--------|-----------|-------------|
| **Extractor** | `ext` | 使用正则表达式提取特定数据 | `utils/auxiliary/ext/` |
| **Collector** | `clc` | 从API/服务收集信息 | `utils/auxiliary/clc/` |
| **Output** | `out` | 数据格式化和发送 | `utils/auxiliary/out/` |
| **Connection** | `con` | 专业化连接 | `utils/auxiliary/con/` |
| **AI** | `ai` | 人工智能  | `utils/auxiliary/ai/` |


#### 基本语法
```bash
./strx -module "类型:模块名"
```

#### 相关参数
- **`-module 类型:名称`**: 指定要使用的模块
- **`-pm`**: 仅显示模块结果(省略shell输出)


### 提取器模块(EXT)
使用正则表达式提取模式和特定数据的模块：

| 模块      | 描述                                 | CLI示例 |
|-------------|-------------------------------------------|-------------|
| `email`     | 提取有效电子邮件地址         | `-module "ext:email"` |
| `domain`    | 提取域名和子域名             | `-module "ext:domain"` |
| `url`       | 提取完整URL(HTTP/HTTPS)         | `-module "ext:url"` |
| `phone`     | 提取电话号码(巴西)            | `-module "ext:phone"` |
| `credential`| 提取凭据、令牌、密钥         | `-module "ext:credential"` |
| `ip`        | 提取IPv4/IPv6地址                 | `-module "ext:ip"` |
| `hash`      | 提取MD5、SHA1、SHA256、SHA512哈希    | `-module "ext:hash"` |

```bash
# 示例：从数据转储中提取邮箱
./strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm
```


### 收集器模块(CLC)
用于外部信息收集、API和分析的模块：

| 模块        | 描述                                 | CLI示例 |
|---------------|-------------------------------------------|-------------|
| `archive`     | 从Wayback Machine收集存档URL | `-module "clc:archive"` |
| `bing`        | 在Bing中进行探查搜索          | `-module "clc:bing"` |
| `crtsh`       | 收集SSL/TLS证书和子域名 | `-module "clc:crtsh"` |
| `dns`         | 收集DNS记录(A、MX、TXT、NS)     | `-module "clc:dns"` |
| `duckduckgo`  | 在DuckDuckGo中进行探查搜索    | `-module "clc:duckduckgo"` |
| `emailverify` | 验证邮箱有效性(MX、SMTP)    | `-module "clc:emailverify"` |
| `ezilon`      | 在Ezilon中进行探查搜索        | `-module "clc:ezilon"` |
| `geoip`       | IP地理位置                     | `-module "clc:geoip"` |
| `google`      | 在Google中进行探查搜索        | `-module "clc:google"` |
| `googlecse`   | 使用Google CSE进行探查搜索| `-module "clc:googlecse"` |
| `ipinfo`      | IP/主机端口扫描                 | `-module "clc:ipinfo"` |
| `lycos`       | 在Lycos中进行探查搜索         | `-module "clc:lycos"` |
| `naver`       | 在Naver中进行探查搜索(韩语)| `-module "clc:naver"` |
| `netscan`     | 网络扫描(主机、服务)         | `-module "clc:netscan"` |
| `shodan`      | 查询Shodan API                       | `-module "clc:shodan"` |
| `sogou`       | 在Sogou中进行探查搜索(中文)| `-module "clc:sogou"` |
| `spider`      | 网络爬虫递归收集URL | `-module "clc:spider"` |
| `subdomain`   | 子域名枚举                 | `-module "clc:subdomain"` |
| `virustotal`  | 查询VirusTotal API                   | `-module "clc:virustotal"` |
| `whois`       | 域名WHOIS查询                | `-module "clc:whois"` |
| `yahoo`       | 在Yahoo中进行探查搜索         | `-module "clc:yahoo"` |

```bash
# 示例：收集DNS信息
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm

# 示例：使用搜索引擎收集信息
./strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:googlecse" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:duckduckgo" -pm

# 特定探查示例
echo 'site:fbi.gov filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:google" -pm
echo 'site:github.com inurl:admin' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm
echo 'inurl:admin' | ./strx -st "echo {STRING}" -module "clc:lycos" -pm
echo 'site:github.com' | ./strx -st "echo {STRING}" -module "clc:ezilon" -pm
echo 'filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm
```


### 输出模块(OUT)
用于结果格式化和输出的模块：

| 模块        | 描述                                 | CLI示例 |
|---------------|-------------------------------------------|-------------|
| `json`        | 将结果保存为JSON                  | `-module "out:json"` |
| `csv`         | 将结果保存为CSV                   | `-module "out:csv"` |
| `xml`         | 将结果保存为XML                   | `-module "out:xml"` |

```bash
# 示例：保存到JSON
./strx -l data.txt -st "process {STRING}" -module "out:json" -pm
```


### 连接模块(CON)
用于外部服务连接和结果集成的模块：

| 模块        | 描述                                 | CLI示例 |
|---------------|-------------------------------------------|-------------|
| `sqlite`      | 将数据保存到SQLite数据库               | `-module "con:sqlite"` |
| `mysql`       | 将数据保存到MySQL数据库                | `-module "con:mysql"` |
| `telegram`    | 通过Telegram Bot发送结果         | `-module "con:telegram"` |
| `slack`       | 通过Slack Webhook发送结果        | `-module "con:slack"` |
| `opensearch`  | 在Open Search中索引结果          | `-module "con:opensearch"` |
| `ftp`         | 通过FTP连接和传输                | `-module "con:ftp"` |
| `ssh`         | 通过SSH执行命令                 | `-module "con:ssh"` |
| `s3`          | 在Amazon S3上传/下载数据         | `-module "con:s3"` |

```bash
# 示例：保存到SQLite
./strx -l data.txt -st "process {STRING}" -module "con:sqlite" -pm
```


### 人工智能模块(AI)
用于人工智能提示的模块：

| 模块        | 描述                                 | CLI示例 |
|---------------|-------------------------------------------|-------------|
| `gemini`      | Google Gemini AI提示 - ([创建API密钥](https://aistudio.google.com/app/apikey))    | `-module "ai:gemini"` |

```bash
# 示例：使用提示文件
./strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm

# 示例：收集URL并发送分析构建提示
./strx -l urls.txt -st "echo '分析URL: {STRING}'" -module "ai:gemini" -pm
```

#### 实际示例
```bash
# 提取邮箱并保存排序
./strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# 检查可疑域名的DNS
./strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# 多模块管道
cat logs.txt | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | ./strx -st "echo {STRING}" -module "clc:dns" -pm

# 提取URL并检查状态
./strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | ./strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

### 新模块开发

要创建新模块，请遵循标准结构：

#### 提取器模块(ext)
```python
"""
模块介绍
"""
from core.basemodule import BaseModule
import re

class ModuleName(BaseModule):
    
    def __init__(self):
      super().__init__()


      # 定义模块元信息
      self.meta.update({
          "name": "模块名称...",
          "description": "描述模块...",
          "author": "创建者姓名...",
          "type": "extractor | collector | Output..."
      })

      # 定义此模块所需的选项
      self.options = {
          "data":   str(),
          "regex":  str(),
          "proxy":  str()
      }
    
    # 执行的必需函数
    def run(self):
        """
        模块逻辑上下文
          > 通过以下方式访问选项信息：self.options.get(key_name)
        """
        # 保存模块执行信息
        self.set_result(value_regex)
```

### 过滤器和模块

您可以将过滤器与模块结合使用，进行更具体的处理：

```bash
# 仅提取.gov域名的邮箱
./strx -l data.txt -st "echo '{STRING}'" -module "ext:email" -pm -f ".gov"

# 仅对.br域名进行DNS查找
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm -f ".br"
```

## 🎯 过滤器和选择性处理

过滤器系统允许仅处理符合特定条件的字符串，优化性能和精度。

### 过滤器使用
```bash
./strx -f "过滤器值" / ./strx --filter "过滤器值"
```

### 过滤器示例
```bash
# 仅过滤.gov.br域名
./strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# 仅过滤HTTPS URL
./strx -l urls.txt -st "curl {STRING}" -f "https"

# 过滤特定IP
./strx -l logs.txt -st "analyze {STRING}" -f "192.168"

# 过滤文件扩展名
./strx -l files.txt -st "process {STRING}" -f ".pdf"

# 仅过滤包含"admin"的函数结果
./strx -l urls.txt -st "{STRING}; md5({STRING})" -pf -iff "admin"

# 仅过滤包含特定hash的模块结果
./strx -l domains.txt -st "echo {STRING}" -module "ext:hash" -pm -ifm "a1b2c3"

# 结合函数和模块过滤器
./strx -l data.txt -st "{STRING}; md5({STRING})" -module "ext:domain" -pf -pm -iff "google" -ifm "admin"
```

### 与模块结合
```bash
# 提取邮箱并保存排序
./strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# 检查可疑域名的DNS
./strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# 多模块管道
cat logs.txt | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | ./strx -st "echo {STRING}" -module "clc:dns" -pm

# 提取URL并检查状态
./strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | ./strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

## ⚡ 并行处理

String-X通过线程支持并行处理，以加速大数据量操作。

### 线程配置
```bash
# 定义线程数
./strx -t 50 / ./strx -thread 50

# 定义线程间延迟
./strx -sleep 2
```

### 线程示例
```bash
# 快速HTTP状态检查
./strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# 批量DNS解析
./strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1

# 端口扫描
./strx -l ip_list.txt -st "nmap -p 80,443 {STRING}" -t 20 -sleep 3
```

### 线程最佳实践
- **速率限制**：使用`-sleep`避免服务过载
- **适当的数量**：根据可用资源调整`-t`
- **监控**：使用`-v 1`获取基本信息，`-v 3`获取详细调试，`-v all`获取最大控制

### 大文件处理
String-X已优化用于高效处理大文件：
```bash
# 用多线程处理大文件
strx -l 大文件.txt -st "echo {STRING}" -module "ext:email" -pm -t 20 -sleep 1

# 对于超大文件，使用更少线程和更多延迟
strx -l 巨大数据集.txt -st "process {STRING}" -t 10 -sleep 2 -v
```

## 🛡️ 安全系统

String-X包含安全验证以防止恶意命令执行：

### 活动验证
- **输入大小**：默认限制输入数据为1MB
- **字符串数量**：每次执行最多10,000个字符串
- **危险模式**：检测并阻止潜在恶意命令
- **线程**：限制并发线程以避免系统过载

### 禁用安全验证
**⚠️ 警告**：仅在必要且信任内容时使用

```bash
# 为合法的复杂命令禁用验证
strx -l 数据.txt -st "echo {STRING}; md5sum {STRING}" -ds

# 处理大文件时不受限制
strx -l 巨大文件.txt -st "process {STRING}" -ds -t 50

# 与可能生成被检测为可疑模式的函数一起使用
echo "test" | strx -st "echo {STRING}; echo '结果'" -ds
```

### 安全调试模式
```bash
# 查看安全验证详情（完整调试）
strx -l 数据.txt -st "command {STRING}" -v 3

# 检查命令被阻止的原因
strx -s "test" -st "可疑命令" -v 3
```
## 📸 视觉示例

### 基本执行
**命令**: `cat hosts.txt | ./strx -str 'host {STRING}'`

![Screenshot](/asset/img/img1.png)

### 线程处理
**命令**: `cat hosts.txt | ./strx -str "curl -Iksw 'CODE:%{response_code};IP:%{remote_ip};HOST:%{url.host};SERVER:%header{server}' https://{STRING}" -p "grep -o -E 'CODE:.(.*)|IP:.(.*)|HOST:.(.*)|SERVER:.(.*)'" -t 30`

![Screenshot](/asset/img/img3.png)

### 详细模式
**命令**: `cat hosts.txt | ./strx -str 'host {STRING}' -v`

![Screenshot](/asset/img/img2.png)

### 输出文件格式
```
output-%d-%m-%Y-%H.txt > output-15-06-2025-11.txt
```

## 🤝 贡献

欢迎贡献！要贡献：

1. **Fork** 仓库
2. **创建** 您的功能分支(`git checkout -b feature/AmazingFeature`)
3. **提交** 您的更改(`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支(`git push origin feature/AmazingFeature`)
5. **打开** Pull Request

### 贡献类型
- 🐛 **错误修复**
- ✨ **新功能**
- 📝 **文档改进**
- 🧩 **新模块**
- ⚡ **性能优化**

### 模块开发
要创建新模块，请参考[模块系统](#-模块系统)部分并遵循既定标准。

## 📄 许可证

本项目根据MIT许可证获得许可 - 有关详细信息，请参阅[LICENSE](LICENSE)文件。

## 👨‍💻 作者

**MrCl0wn**
- 🌐 **博客**: [http://blog.mrcl0wn.com](http://blog.mrcl0wn.com)
- 🐙 **GitHub**: [@MrCl0wnLab](https://github.com/MrCl0wnLab) | [@MrCl0wnLab](https://github.com/MrCl0wnLab)
- 🐦 **Twitter**: [@MrCl0wnLab](https://twitter.com/MrCl0wnLab)
- 📧 **邮箱**: mrcl0wnlab@gmail.com

---

<div align="center">

**⭐ 如果这个项目对您有用，请考虑给个星星！**

**💡 欢迎建议和反馈！**

**💀 黑客入侵！**

</div>
