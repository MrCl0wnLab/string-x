<center>

<h1 align="center">
  <br>
  🔧 String-X (STRX)
</h1>

<h4 align="center">أداة الأتمتة لمعالجة النصوص</h4>

<p align="center">
أداة أتمتة معيارية مطورة لمساعدة المحللين في OSINT، اختبار الاختراق وتحليل البيانات من خلال المعالجة الديناميكية للنصوص في أوامر Linux. نظام قائم على القوالب مع معالجة متوازية ووحدات قابلة للتوسيع.
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

## 📋 الفهرس

- [الميزات](#-الميزات)
- [التثبيت](#-التثبيت)
- [المفاهيم الأساسية](#-المفاهيم-الأساسية)
- [البنية المعيارية](#-البنية-المعيارية)
- [استخدام الأداة](#-استخدام-الأداة)
- [أمثلة عملية](#-أمثلة-عملية)
- [الوظائف المدمجة](#-الوظائف-المدمجة)
- [نظام الوحدات](#-نظام-الوحدات)
- [المساهمة](#-المساهمة)
- [المؤلف](#-المؤلف)

## ✨ الميزات

- 🚀 **معالجة متوازية**: نظام threads قابل للتكوين للحصول على أداء عالي
- 🔧 **بنية معيارية**: قابلة للتوسيع من خلال وحدات EXT، CLC، OUT، وCON
- 🔄 **قالب ديناميكي**: نظام استبدال النصوص مع العنصر النائب `{STRING}`
- 🛠️ **وظائف مدمجة**: وظائف hash، encoding، requests وتوليد قيم عشوائية
- 📁 **مصادر متعددة**: دعم للملفات، stdin والأنابيب
- 🎯 **تصفية متقدمة**: نظام مرشحات للمعالجة الانتقائية
- 💾 **إخراج مرن**: حفظ في ملفات مع timestamp تلقائي

## 📦 التثبيت

### المتطلبات
- Python 3.8+
- Linux/MacOS
- المكتبات المدرجة في `requirements.txt`

### التثبيت السريع
```bash
# نسخ المستودع
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x

# تثبيت التبعيات
pip install -r requirements.txt

# جعل الملف قابل للتنفيذ
chmod +x strx

# اختبار التثبيت
./strx --help
```

### التثبيت عبر Pip (قريباً)
```bash
pip install string-x
```

## 🧠 المفاهيم الأساسية

### نظام القالب {STRING}
تستخدم الأداة العنصر النائب `{STRING}` كلمة مفتاحية للاستبدال الديناميكي للقيم. يسمح هذا النظام بمعالجة كل سطر من المدخلات بشكل فردي، واستبدال `{STRING}` بالقيمة الحالية.

```bash
# ملف المدخل
host-01.com.br
host-02.com.br
host-03.com.br

# أمر مع قالب
./strx -l hosts.txt -st "host '{STRING}'"

# النتيجة المولدة
host 'host-01.com.br'
host 'host-02.com.br'
host 'host-03.com.br'
```

### سير المعالجة
1. **المدخل**: البيانات عبر ملف (`-l`) أو stdin (pipe)
2. **القالب**: تطبيق القالب مع `{STRING}`
3. **المعالجة**: تنفيذ الأوامر/الوحدات
4. **الأنبوب**: معالجة إضافية اختيارية (`-p`)
5. **المخرج**: النتيجة النهائية (الشاشة أو ملف)

<center>

![Screenshot](/asset/fluxo.jpg)

</center>

## 🏗️ البنية المعيارية

يستخدم String-X بنية معيارية قابلة للتوسيع مع أربعة أنواع رئيسية من الوحدات:

### أنواع الوحدات

| النوع | الكود | الوصف | الموقع |
|------|--------|-----------|-------------|
| **Extractor** | `ext` | استخراج بيانات محددة (email، URL، domain، phone) | `utils/auxiliary/ext/` |
| **Collector** | `clc` | جمع وتجميع المعلومات (DNS، whois) | `utils/auxiliary/clc/` |
| **Output** | `out` | تنسيق وإرسال النتائج (DB، API، files) | `utils/auxiliary/out/` |
| **Connection** | `con` | اتصالات متخصصة (SSH، FTP، إلخ) | `utils/auxiliary/con/` |

### هيكل الأدلة
```
string-x/
├── strx                    # الملف التنفيذي الرئيسي
├── config/                 # التكوينات العامة
├── core/                   # نواة التطبيق
│   ├── command.py         # معالجة الأوامر
│   ├── auto_module.py     # تحميل ديناميكي للوحدات
│   ├── thread_process.py  # نظام threads
│   ├── format.py          # التنسيق والترميز
│   └── style_cli.py       # واجهة CLI منسقة
└── utils/
    ├── auxiliary/         # وحدات مساعدة
    │   ├── ext/          # وحدات الاستخراج
    │   ├── clc/          # وحدات التجميع
    │   ├── out/          # وحدات الإخراج
    │   └── con/          # وحدات الاتصال
    └── helper/           # وظائف مساعدة
```

## 🚀 استخدام الأداة

### المساعدة والمعاملات
```bash
./strx --help
```

### المعاملات الرئيسية

| المعامل | الوصف | مثال |
|-----------|-----------|---------|
| `-l, --list` | ملف يحتوي على نصوص للمعالجة | `-l hosts.txt` |
| `-st, --str` | قالب أمر مع `{STRING}` | `-st "curl {STRING}"` |
| `-o, --out` | ملف إخراج للنتائج | `-o results.txt` |
| `-p, --pipe` | أمر إضافي عبر pipe | `-p "grep 200"` |
| `-v, --verbose` | وضع مفصل مع التفاصيل | `-v` |
| `-t, --thread` | عدد threads المتوازية | `-t 50` |
| `-f, --filter` | مرشح لاختيار النصوص | `-f ".gov.br"` |
| `-module` | اختيار وحدة محددة | `-module "ext:email"` |
| `-pm` | إظهار نتائج الوحدة فقط | `-pm` |
| `-pf` | إظهار نتائج الوظائف فقط | `-pf` |
| `-of` | حفظ نتائج الوظائف في ملف | `-of` |
| `-sleep` | تأخير بين threads (ثوانٍ) | `-sleep 2` |

### واجهة التطبيق

```bash
usage: strx [-h] [-list file] -str cmd [-out file] [-pipe cmd] [-verbose] 
            [-thread <10>] [-pf] [-of] [-filter value] [-sleep <5>] 
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
                                
                          String-X: Automation Tool for String Manipulation

options:
             -h, --help             عرض رسالة المساعدة هذه
             -list, -l file         ملف يحتوي على نصوص للتنفيذ
             -str, -st cmd          قالب أمر مع العنصر النائب {STRING}
             -out, -o file          ملف إخراج للنتائج
             -pipe, -p cmd          أمر منفذ بعد الأنبوب |
             -verbose, -v           وضع مفصل مع معلومات تفصيلية
             -thread, -t <10>       عدد threads للمعالجة المتوازية
             -pf                    إظهار نتائج الوظائف فقط
             -of                    حفظ نتائج الوظائف في ملف
             -filter, -f value      مرشح للاختيار المحدد للنصوص
             -sleep <5>             تأخير بالثواني بين تنفيذ threads
             -module <type:module>  تحديد نوع واسم الوحدة
             -pm                    إظهار نتائج الوحدة فقط
```

## 💡 أمثلة عملية

### أمثلة أساسية

#### 1. فحص المضيفين
```bash
# عبر ملف
./strx -l hosts.txt -st "host {STRING}" -v

# عبر pipe
cat hosts.txt | ./strx -st "host {STRING}" -v
```

#### 2. طلبات HTTP مع التحليل
```bash
# فحص حالة URLs
./strx -l urls.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 20

# استخراج عناوين الصفحات
./strx -l domains.txt -st "curl -sL https://{STRING}" -p "grep -o '<title>.*</title>'" -o titles.txt
```

#### 3. تحليل السجلات والبيانات
```bash
# البحث عن CPFs في التسريبات
./strx -l cpfs.txt -st "grep -Ei '{STRING}' -R ./database/" -v

# معالجة dump SQL
./strx -l dump.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u
```

### أمثلة متقدمة

#### 1. OSINT والاستطلاع
```bash
# معلومات IP
cat ips.txt | ./strx -st "curl -s 'https://ipinfo.io/{STRING}/json'" -p "jq -r '.org, .country'"

# فحص التصيد الاحتيالي
./strx -l suspicious.txt -st "curl -skL https://{STRING}/" -p "grep -i 'phish\|scam\|fake'" -t 30

# تعداد DNS
./strx -l subdomains.txt -st "dig +short {STRING}" -module "clc:dns" -pm
```

#### 2. الأمان واختبار الاختراق
```bash
# فحص المنافذ مع nmap
./strx -l targets.txt -st "nmap -p 80,443 {STRING}" -p "grep 'open'" -t 10

# اختبار حقن SQL
./strx -l urls.txt -st "sqlmap -u '{STRING}' --batch" -p "grep 'vulnerable'" -o sqli_results.txt

# bruteforce الأدلة
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

#### 3. معالجة البيانات
```bash
# استخراج emails من ملفات متعددة
./strx -l files.txt -st "cat {STRING}" -module "ext:email" -pm > all_emails.txt

# تحويل الترميز
./strx -l base64_data.txt -st "debase64({STRING})" -pf -of

# توليد hashes
./strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -pf -o hashes.txt
```

### دمج مع أنابيب النظام
```bash
# أنبوب معقد مع jq
curl -s 'https://api.github.com/users' | jq -r '.[].login' | ./strx -st "curl -s 'https://api.github.com/users/{STRING}'" -p "jq -r '.name, .location'"

# معالجة سجلات Apache
cat access.log | awk '{print $1}' | sort -u | ./strx -st "whois {STRING}" -p "grep -i 'country'" -t 5

# تحليل شهادات SSL
./strx -l domains.txt -st "echo | openssl s_client -connect {STRING}:443 2>/dev/null" -p "openssl x509 -noout -subject"
```

## 🔧 الوظائف المدمجة

يتضمن String-X وظائف مدمجة يمكن استخدامها داخل قوالب `{STRING}` وأوامر pipe. تتم معالجة هذه الوظائف قبل تنفيذ أوامر shell.

### البنية
```bash
# وظيفة بسيطة
./strx -l data.txt -st "funcao({STRING})" -pf

# وظائف متعددة
./strx -l data.txt -st "{STRING}; md5({STRING}); base64({STRING})" -pf

# وظيفة مع معاملات
./strx -l data.txt -st "str_rand(10); int_rand(5)" -pf
```

### جدول الوظائف المتاحة

| الوظيفة | الوصف | المعامل | مثال |
|--------|-----------|-----------|---------|
| `clear` | إزالة المسافات، tabs وكسرات الأسطر | str | `clear({STRING})` |
| `base64` | ترميز النص في Base64 | str | `base64({STRING})` |
| `debase64` | فك ترميز النص Base64 | str | `debase64({STRING})` |
| `sha1` | توليد hash SHA1 | str | `sha1({STRING})` |
| `sha256` | توليد hash SHA256 | str | `sha256({STRING})` |
| `md5` | توليد hash MD5 | str | `md5({STRING})` |
| `hex` | تحويل إلى hexadecimal | str | `hex({STRING})` |
| `dehex` | تحويل من hexadecimal | str | `dehex({STRING})` |
| `str_rand` | توليد نص عشوائي | int | `str_rand(10)` |
| `int_rand` | توليد رقم عشوائي | int | `int_rand(5)` |
| `ip` | حل IP لاسم مضيف | str | `ip({STRING})` |
| `replace` | استبدال قيم في النص | str | `replace(old,new,{STRING})` |
| `get` | تنفيذ طلب HTTP GET | str | `get(https://{STRING})` |
| `urlencode` | ترميز URL | str | `urlencode({STRING})` |
| `rev` | عكس النص | str | `rev({STRING})` |

### أمثلة استخدام الوظائف

#### Hashing والترميز
```bash
# توليد hashes متعددة
./strx -l passwords.txt -st "md5({STRING}); sha1({STRING}); sha256({STRING})" -pf

# العمل مع Base64
./strx -l data.txt -st "base64({STRING})" -pf
echo "SGVsbG8gV29ybGQ=" | ./strx -st "debase64({STRING})" -pf
```

#### توليد قيم عشوائية
```bash
# توليد نصوص عشوائية
./strx -l domains.txt -st "https://{STRING}/admin?token=str_rand(32)" -pf

# توليد أرقام عشوائية
./strx -l apis.txt -st "curl '{STRING}?id=int_rand(6)'" -pf
```

#### الطلبات والحل
```bash
# حل IPs
./strx -l hosts.txt -st "{STRING}; ip({STRING})" -pf

# تنفيذ طلبات GET
./strx -l urls.txt -st "get(https://{STRING})" -pf
```

#### معالجة النصوص
```bash
# استبدال البروتوكولات
./strx -l urls.txt -st "replace(http:,https:,{STRING})" -pf

# عكس النصوص
./strx -l data.txt -st "rev({STRING})" -pf

# ترميز URL
./strx -l params.txt -st "urlencode({STRING})" -pf
```

### معاملات التحكم

- **`-pf`**: إظهار نتائج الوظائف فقط (تجاهل تنفيذ shell)
- **`-of`**: حفظ نتائج الوظائف في ملف إخراج

```bash
# إظهار نتيجة الوظائف فقط
./strx -l domains.txt -st "{STRING}; md5({STRING})" -pf

# حفظ الوظائف في ملف
./strx -l data.txt -st "base64({STRING})" -pf -of -o encoded.txt
```

> **💡 نصيحة**: يمكنك إضافة وظائف مخصصة بتحرير ملف `utils/helper/functions.py`

## 🧩 نظام الوحدات

يستخدم String-X بنية معيارية قابلة للتوسيع تسمح بإضافة وظائف محددة دون تعديل الكود الرئيسي. الوحدات منظمة حسب النوع ومحملة ديناميكياً.

### أنواع الوحدات المتاحة

| النوع | الكود | الوصف | الموقع |
|------|--------|-----------|-------------|
| **Extractor** | `ext` | استخراج بيانات محددة باستخدام regex | `utils/auxiliary/ext/` |
| **Collector** | `clc` | جمع معلومات من APIs/الخدمات | `utils/auxiliary/clc/` |
| **Output** | `out` | تنسيق وإرسال البيانات | `utils/auxiliary/out/` |
| **Connection** | `con` | اتصالات متخصصة | `utils/auxiliary/con/` |

### وحدات Extractor (EXT)

تستخدم وحدات الاستخراج التعبيرات النمطية لاستخراج بيانات محددة من النصوص.

#### الوحدات المتاحة:
- **`email`**: استخراج عناوين email صحيحة
- **`domain`**: استخراج النطاقات والنطاقات الفرعية
- **`url`**: استخراج URLs كاملة (HTTP/HTTPS)
- **`phone`**: استخراج أرقام الهاتف (التنسيق البرازيلي)

```bash
# استخراج emails من dump البيانات
./strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm

# استخراج النطاقات من السجلات
cat access.log | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | sort -u

# استخراج URLs من ملفات HTML
./strx -l html_files.txt -st "cat {STRING}" -module "ext:url" -pm

# استخراج الهواتف من الوثائق
./strx -l documents.txt -st "cat {STRING}" -module "ext:phone" -pm
```

### وحدات Collector (CLC)

تقوم وحدات التجميع بطلبات إلى خدمات خارجية للحصول على معلومات إضافية.

#### الوحدات المتاحة:
- **`dns`**: جمع سجلات DNS (A، MX، TXT، إلخ)

```bash
# جمع معلومات DNS
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm

# DNS lookup مع verbose
./strx -l subdomains.txt -st "echo {STRING}" -module "clc:dns" -pm -v
```

### وحدات Output (OUT)

تقوم وحدات الإخراج بتنسيق وإرسال النتائج إلى وجهات مختلفة.

#### الوحدات المتاحة:
- **`sqlite`**: حفظ البيانات في قاعدة بيانات SQLite
- **`mysql`**: حفظ البيانات في قاعدة بيانات MySQL
- **`telegram`**: إرسال النتائج عبر Telegram Bot
- **`slack`**: إرسال النتائج عبر Slack Webhook

```bash
# حفظ في SQLite
./strx -l data.txt -st "process {STRING}" -module "out:sqlite" -pm

# إرسال إلى Telegram
./strx -l alerts.txt -st "echo '{STRING}'" -module "out:telegram" -pm

# إرسال إلى Slack
./strx -l reports.txt -st "generate_report {STRING}" -module "out:slack" -pm
```

### استخدام الوحدات

#### البنية الأساسية
```bash
./strx -module "نوع:اسم_الوحدة"
```

#### المعاملات ذات الصلة
- **`-module نوع:اسم`**: تحديد الوحدة المراد استخدامها
- **`-pm`**: إظهار نتائج الوحدة فقط (حذف إخراج shell)

#### أمثلة عملية

```bash
# 1. استخراج emails وحفظها مرتبة
./strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# 2. فحص DNS للنطاقات المشبوهة
./strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# 3. أنبوب مع وحدات متعددة
cat logs.txt | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | ./strx -st "echo {STRING}" -module "clc:dns" -pm

# 4. استخراج URLs وفحص الحالة
./strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | ./strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

### تطوير وحدات جديدة

لإنشاء وحدات جديدة، اتبع الهيكل المعياري:

#### وحدة Extractor (ext)
```python
"""
وحدة استخراج مخصصة.
"""

import re

def extract(data):
    """
    وظيفة الاستخراج الرئيسية.
    
    Args:
        data (str): بيانات المدخل للاستخراج
        
    Returns:
        list: قائمة العناصر المستخرجة
    """
    pattern = r'your_regex_here'
    matches = re.findall(pattern, data, re.IGNORECASE)
    return matches
```

#### وحدة Collector (clc)
```python
"""
وحدة تجميع مخصصة.
"""

import requests

def collect(target):
    """
    وظيفة التجميع الرئيسية.
    
    Args:
        target (str): الهدف لجمع المعلومات
        
    Returns:
        dict: البيانات المجمعة
    """
    # تنفيذ منطق التجميع
    pass
```

### المرشحات والوحدات

يمكنك دمج المرشحات مع الوحدات للمعالجة الأكثر تحديداً:

```bash
# استخراج emails فقط من نطاقات .gov
./strx -l data.txt -st "echo '{STRING}'" -module "ext:email" -pm -f ".gov"

# DNS lookup فقط للنطاقات .br
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm -f ".br"
```

## 🎯 المرشحات والمعالجة الانتقائية

يسمح نظام المرشحات بمعالجة النصوص التي تلبي معايير محددة فقط، مما يحسن الأداء والدقة.

### استخدام المرشحات
```bash
./strx -f "قيمة_المرشح" / ./strx --filter "قيمة_المرشح"
```

### أمثلة المرشحات
```bash
# تصفية النطاقات .gov.br فقط
./strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# تصفية URLs HTTPS فقط
./strx -l urls.txt -st "curl {STRING}" -f "https"

# تصفية IPs محددة
./strx -l logs.txt -st "analyze {STRING}" -f "192.168"

# تصفية امتدادات الملفات
./strx -l files.txt -st "process {STRING}" -f ".pdf"
```

### دمج مع الوحدات
```bash
# استخراج emails فقط من نطاقات محددة
./strx -l data.txt -st "echo '{STRING}'" -module "ext:email" -pm -f "gmail.com"

# DNS lookup فقط للنطاقات الفرعية
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm -f "sub."
```

## ⚡ المعالجة المتوازية

يدعم String-X المعالجة المتوازية من خلال threads لتسريع العمليات على كميات كبيرة من البيانات.

### تكوين Threads
```bash
# تحديد عدد threads
./strx -t 50 / ./strx --thread 50

# تحديد تأخير بين threads
./strx -sleep 2
```

### أمثلة مع Threading
```bash
# فحص سريع لحالة HTTP
./strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# حل DNS بالجملة
./strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1

# فحص المنافذ
./strx -l ip_list.txt -st "nmap -p 80,443 {STRING}" -t 20 -sleep 3
```

### أفضل الممارسات للThreading
- **تحديد المعدل**: استخدم `-sleep` لتجنب إرهاق الخدمات
- **عدد مناسب**: اضبط `-t` حسب الموارد المتاحة
- **المراقبة**: استخدم `-v` لتتبع التقدم

## 📸 أمثلة بصرية

### التنفيذ الأساسي
**الأمر**: `cat hosts.txt | ./strx -str 'host {STRING}'`

![Screenshot](/asset/img1.png)

### المعالجة مع Threading
**الأمر**: `cat hosts.txt | ./strx -str "curl -Iksw 'CODE:%{response_code};IP:%{remote_ip};HOST:%{url.host};SERVER:%header{server}' https://{STRING}" -p "grep -o -E 'CODE:.(.*)|IP:.(.*)|HOST:.(.*)|SERVER:.(.*)'" -t 30`

![Screenshot](/asset/img3.png)

### الوضع المفصل
**الأمر**: `cat hosts.txt | ./strx -str 'host {STRING}' -v`

![Screenshot](/asset/img2.png)

### تنسيق ملف الإخراج
```
output-%d-%m-%Y-%H.txt > output-15-06-2025-11.txt
```

## 🤝 المساهمة

المساهمات مرحب بها! للمساهمة:

1. **Fork** المستودع
2. **أنشئ** فرع لميزتك (`git checkout -b feature/AmazingFeature`)
3. **Commit** تغييراتك (`git commit -m 'Add some AmazingFeature'`)
4. **Push** إلى الفرع (`git push origin feature/AmazingFeature`)
5. **افتح** Pull Request

### أنواع المساهمة
- 🐛 **إصلاح الأخطاء**
- ✨ **ميزات جديدة**
- 📝 **تحسين التوثيق**
- 🧩 **وحدات جديدة**
- ⚡ **تحسينات الأداء**

### تطوير الوحدات
لإنشاء وحدات جديدة، راجع قسم [نظام الوحدات](#-نظام-الوحدات) واتبع المعايير المحددة.

## 📄 الرخصة

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 👨‍💻 المؤلف

**MrCl0wn**
- 🌐 **مدونة**: [http://blog.mrcl0wn.com](http://blog.mrcl0wn.com)
- 🐙 **GitHub**: [@MrCl0wnLab](https://github.com/MrCl0wnLab) | [@MrCl0wnLab](https://github.com/MrCl0wnLab)
- 🐦 **Twitter**: [@MrCl0wnLab](https://twitter.com/MrCl0wnLab)
- 📧 **البريد الإلكتروني**: mrcl0wnlab@gmail.com

---

<div align="center">

**⭐ إذا كان هذا المشروع مفيداً، فكر في إعطائه نجمة!**

**💡 الاقتراحات والتعليقات مرحب بها دائماً!**

**💀 Hacker Hackeia!**

</div>
