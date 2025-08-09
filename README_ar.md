<center>

<h1 align="center">
  <a href="#/"><img src="./asset/logo.png"></a>
</h1>

<h4 align="center">أداة الأتمتة لمعالجة النصوص</h4>

<p align="center">
String-X (strx) هي أداة أتمتة معيارية مطورة لمحترفي أمن المعلومات وعشاق الهاكينغ. متخصصة في المعالجة الديناميكية للنصوص في بيئة Linux.

مع البنية المعيارية، تقدم ميزات متقدمة لـ OSINT واختبار الاختراق وتحليل البيانات، بما في ذلك المعالجة المتوازية، ووحدات الاستخراج المتخصصة، ووظائف التجميع، والتكامل مع واجهات برمجة التطبيقات الخارجية. نظام قائم على قوالب مرنة مع أكثر من 25 وظيفة متكاملة.
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

- 🚀 **معالجة متوازية**: نظام متعدد الخيوط قابل للتكوين لتنفيذ عالي الأداء
- 🧩 **بنية معيارية**: هيكل قابل للتوسيع مع وحدات متخصصة (EXT، CLC، OUT، CON، AI)
- 🔄 **قالب ديناميكي**: نظام استبدال باستخدام العنصر النائب `{STRING}` للمعالجة المرنة
- 🛠️ **25+ وظيفة متكاملة**: hash، encoding، requests، validation وتوليد قيم عشوائية
- 📁 **مصادر بيانات متعددة**: دعم للملفات، stdin وسلاسل الأنابيب
- 🎯 **تصفية ذكية**: نظام مرشحات للمعالجة الانتقائية للنصوص
- 💾 **إخراج مرن**: تنسيقات TXT، CSV وJSON مع طوابع زمنية تلقائية
- 🔌 **تكاملات خارجية**: واجهات برمجة التطبيقات، قواعد البيانات وخدمات الإشعارات
- 🔍 **استخراج متقدم**: أنماط تعبيرات نمطية معقدة ومعالجة متخصصة
- 🔒 **OSINT واختبار الاختراق**: موارد محسنة للاستطلاع وتحليل الأمان
- 🌐 **استكشاف متعدد المحركات**: تكامل مع Google، Bing، Yahoo، DuckDuckGo وغيرها
- 🧠 **تكامل الذكاء الاصطناعي**: وحدة معالجة Google Gemini
- 🐋 **دعم Docker**: تنفيذ مُحتوى في بيئات معزولة
- 🛡️ **التحقق من الأمان**: نظام حماية ضد الأوامر الخبيثة مع خيار التجاوز

## 📦 التثبيت

### متطلبات النظام
- Python 3.12+
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

# اختبار التثبيت وعرض المساعدة
./strx -help

# قائمة أنواع الوحدات
./strx -types

# قائمة الوحدات وأمثلة الاستخدام
./strx -examples

# قائمة الوظائف
./strx -funcs

```

### إنشاء رابط رمزي (اختياري)
```bash
# فحص الرابط الحالي
ls -la /usr/local/bin/strx

# إذا لزم الأمر، إعادة إنشاء الرابط
sudo rm /usr/local/bin/strx
sudo ln -sf $HOME/Documentos/string-x/strx /usr/local/bin/strx
```

## ⏫ نظام التحديث باستخدام Git
يستخدم أوامر git لتنزيل إصدارات جديدة
```bash
# تحديث String-X
./strx -upgrade
```

## 🐋 DOCKER
يتوفر String-X كصورة Docker، مما يسمح بالتشغيل في بيئات معزولة دون الحاجة لتثبيت التبعيات محلياً.

### بناء الصورة

```bash
# بناء صورة Docker
docker build -t string-x .
```

### الاستخدام الأساسي مع Docker

```bash
# تشغيل مع الأمر الافتراضي (عرض الأمثلة)
docker run --rm string-x

# عرض المساعدة
docker run --rm string-x -h

# قائمة الوظائف المتاحة
docker run --rm string-x -funcs

# قائمة أنواع الوحدات
docker run --rm string-x -types
```

### معالجة الملفات المحلية

لمعالجة ملفات المضيف، قم بتركيب الدليل كحجم:

```bash
# تركيب الدليل الحالي ومعالجة الملف
docker run --rm -v $(pwd):/dados string-x -l /dados/urls.txt -st "curl -I {STRING}"

# معالجة مع خيوط متعددة
docker run --rm -v $(pwd):/dados string-x -l /dados/hosts.txt -st "nmap -p 80,443 {STRING}" -t 20

# حفظ النتائج على المضيف
docker run --rm -v $(pwd):/dados string-x -l /dados/domains.txt -st "dig +short {STRING}" -o /dados/results.txt
```

### استخدام الوحدات

```bash
# استخراج رسائل البريد الإلكتروني من ملف
docker run --rm -v $(pwd):/dados string-x -l /dados/dump.txt -st "echo {STRING}" -module "ext:email" -pm

# استكشاف Google
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# جمع معلومات DNS
docker run --rm -v $(pwd):/dados string-x -l /dados/domains.txt -st "echo {STRING}" -module "clc:dns" -pm
```

### معالجة عبر الأنابيب

```bash
# أنبوب من أوامر المضيف
echo "github.com" | docker run --rm -i string-x -st "whois {STRING}"

# دمج مع أدوات المضيف
cat urls.txt | docker run --rm -i string-x -st "curl -skL {STRING}" -p "grep '<title>'"

# أنبوب معقد
cat domains.txt | docker run --rm -i string-x -st "echo {STRING}" -module "clc:crtsh" -pm | sort -u
```

### إعدادات متقدمة

```bash
# استخدام بروكسي داخل الحاوية
docker run --rm -v $(pwd):/dados string-x -l /dados/dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "http://172.17.0.1:8080" -pm

# تحديد تنسيق الإخراج
docker run --rm -v $(pwd):/dados string-x -l /dados/targets.txt -st "echo {STRING}" -format json -o /dados/output.json

# تنفيذ مع تأخير بين الخيوط
docker run --rm -v $(pwd):/dados string-x -l /dados/apis.txt -st "curl {STRING}" -t 10 -sleep 2
```


## 🧠 المفاهيم الأساسية

### نظام قالب {STRING}
تستخدم الأداة العنصر النائب `{STRING}` كلمة مفتاحية للاستبدال الديناميكي للقيم. يسمح هذا النظام بمعالجة كل سطر إدخال بشكل فردي، واستبدال `{STRING}` بالقيمة الحالية.

```bash
# ملف الإدخال
host-01.com.br
host-02.com.br
host-03.com.br

# أمر مع القالب
./strx -l hosts.txt -st "host '{STRING}'"

# النتيجة المُولدة
host 'host-01.com.br'
host 'host-02.com.br'
host 'host-03.com.br'
```

### تدفق المعالجة
1. **الإدخال**: البيانات عبر ملف (`-l`) أو stdin (أنبوب)
2. **القالب**: تطبيق القالب مع `{STRING}`
3. **المعالجة**: تنفيذ الأوامر/الوحدات
4. **الأنبوب**: معالجة إضافية اختيارية (`-p`)
5. **الإخراج**: النتيجة النهائية (الشاشة أو ملف)

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
```bash
string-x/
      .
      ├── asset             # الصور واللافتات والشعارات المستخدمة في الوثائق وواجهة CLI
      ├── config            # ملفات التكوين العامة للمشروع (الإعدادات، المتغيرات)
      ├── core              # نواة التطبيق، المحرك الرئيسي والمنطق المركزي
      │   └── banner        # وحدة فرعية للافتات ASCII الفنية
      │       └── asciiart  # ملفات الفن ASCII للعرض في الطرفية
      ├── output            # الدليل الافتراضي لملفات الإخراج والسجلات التي تُولدها الأداة
      └── utils             # أدوات مساعدة ووحدات مساعدة للتوسيعات والتكاملات
          ├── auxiliary     # وحدات مساعدة منظمة حسب الوظيفة
          │   ├── ai        # وحدات الذكاء الاصطناعي (مثال: مطالبات Gemini)
          │   ├── clc       # وحدات الجامع (البحث، DNS، whois، واجهات برمجة التطبيقات الخارجية)
          │   ├── con       # وحدات الاتصال (SSH، FTP، HTTP probe)
          │   ├── ext       # وحدات المستخرج (regex: email، domain، IP، hash، إلخ)
          │   └── out       # وحدات الإخراج/التكامل (JSON، CSV، قاعدة البيانات، واجهات برمجة التطبيقات)
          └── helper        # وظائف مساعدة ومساعدات تُستخدم في المشروع بأكمله
```

## 🚀 استخدام الأداة

### المساعدة والمعاملات
```bash
./strx -help
```

### المعاملات الرئيسية

| المعامل | الوصف | مثال |
|-----------|-----------|---------|
| `-h, -help`         | عرض مساعدة المشروع | `-h` |
| `-types`             | قائمة أنواع الوحدات | `-types` |
| `-examples`          | قائمة الوحدات وأمثلة الاستخدام | `-examples` |
| `-functions, -funcs` | قائمة الوظائف | `-funcs` |
| `-l, -list` | ملف يحتوي على نصوص للمعالجة | `-l hosts.txt` |
| `-st, --str` | قالب أمر مع `{STRING}` | `-st "curl {STRING}"` |
| `-o, --out` | ملف إخراج للنتائج | `-o results.txt` |
| `-p, -pipe` | أمر إضافي عبر أنبوب | `-p "grep 200"` |
| `-v, -verbose` | وضع مفصل مع مستويات (1-5 أو 'all'). 1=معلومات، 2=تحذيرات، 3=تصحيح، 4=أخطاء، 5=استثناءات | `-v 3` |
| `-ds, -disable-security` | تعطيل التحقق من الأمان (استخدم بحذر) | `-ds` |
| `-t, -thread` | عدد الخيوط المتوازية | `-t 50` |
| `-f, --filter` | مرشح لاختيار النصوص | `-f ".gov.br"` |
| `-iff` | مرشح نتائج الوظائف: يعيد فقط النتائج التي تحتوي على القيمة المحددة | `-iff "admin"` |
| `-ifm` | مرشح نتائج الوحدة: يعيد فقط النتائج التي تحتوي على القيمة المحددة | `-ifm "hash"` |
| `-module` | اختيار وحدة محددة | `-module "ext:email"` |
| `-pm` | عرض نتائج الوحدة فقط | `-pm` |
| `-pf` | عرض نتائج الوظائف فقط | `-pf` |
| `-of` | حفظ نتائج الوظائف في ملف | `-of` |
| `-sleep` | تأخير بين الخيوط (بالثواني) | `-sleep 2` |
| `-proxy` | تعيين بروكسي للطلبات | `-proxy "http://127.0.0.1:8080"` |
| `-format` | تنسيق الإخراج (txt، csv، json) | `-format json` |
| `-upgrade` | تحديث String-X عبر Git | `-upgrade` |
| `-r, -retry` | عدد المحاولات | `-r 3` |

### واجهة التطبيق

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
             -types                 قائمة أنواع الوحدات
             -examples              قائمة الوحدات وأمثلة الاستخدام
             -functions, -funcs     قائمة الوظائف
             -list, -l file         ملف نصوص للتنفيذ
             -str, -st cmd          قالب أمر نصي
             -out, -o file          ملف إخراج لقيم تنفيذ shell
             -pipe, -p cmd          أمر سيتم تنفيذه بعد الأنبوب |
             -verbose, -v           وضع مفصل
             -debug                 تمكين تصحيح الوحدات
             -thread, -t <10>       عدد الخيوط
             -pf                    عرض نتائج تنفيذ الوظائف، تجاهل shell
             -of                    تمكين إخراج قيم تنفيذ الوظائف
             -filter, -f value      قيمة لتصفية نصوص التنفيذ
             -iff value             مرشح نتائج الوظائف: يعيد فقط النتائج التي تحتوي على القيمة المحددة
             -ifm value             مرشح نتائج الوحدة: يعيد فقط النتائج التي تحتوي على القيمة المحددة
             -sleep <5>             ثواني التأخير بين الخيوط
             -module <type:module>  اختيار النوع والوحدة
             -pm                    عرض نتائج تنفيذ الوحدة فقط
             -proxy PROXY           تعيين بروكسي للطلب
             -format <format>       تنسيق الإخراج (txt، csv، json)
             -upgrade               تحديث String-X عبر Git
             -retry, -r <0>         عدد المحاولات


```

## 💡 أمثلة عملية

### مستويات Verbose
يوفر String-X 5 مستويات للإطراد للتحكم التفصيلي في المخرجات:

```bash
# المستوى 1 (info) - معلومات أساسية
strx -l domains.txt -st "dig {STRING}" -v 1

# المستوى 2 (warning) - تحذيرات وتنبيهات
strx -l urls.txt -st "curl {STRING}" -v 2

# المستوى 3 (debug) - معلومات تصحيح مفصلة
strx -l targets.txt -st "nmap {STRING}" -v 3

# المستوى 4 (error) - أخطاء التنفيذ
strx -l data.txt -st "process {STRING}" -v 4

# المستوى 5 (exception) - استثناءات مع تتبع المكدس
strx -l complex.txt -st "analyze {STRING}" -v 5

# جميع المستويات - أقصى إخراج للمعلومات
strx -l hosts.txt -st "scan {STRING}" -v all

# دمج مستويات متعددة
strx -l mixed.txt -st "test {STRING}" -v "1,3,4"
```

### أمثلة أساسية

#### 1. فحص المضيفين
```bash
# عبر ملف
./strx -l hosts.txt -st "host {STRING}" -v

# عبر أنبوب
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

# معالجة تفريغ SQL
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

# القوة الغاشمة للأدلة
./strx -l wordlist.txt -st "curl -s -o /dev/null -w '%{http_code}' https://target.com/{STRING}" -p "grep '^200$'"
```

#### 3. معالجة البيانات
```bash
# استخراج رسائل البريد الإلكتروني من ملفات متعددة
./strx -l files.txt -st "cat {STRING}" -module "ext:email" -pm > all_emails.txt

# تحويل الترميز
./strx -l base64_data.txt -st "debase64({STRING})" -pf -of

# توليد hashes
./strx -l passwords.txt -st "md5({STRING}); sha256({STRING})" -pf -o hashes.txt

# استخدام تنسيق json
echo 'com.br' | ./strx  -st "echo {STRING}" -o bing.json -format json -module 'clc:bing' -pm -v
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

### الاستكشاف ومحركات البحث
```bash
# استكشاف Google الأساسي
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm

# البحث عن ملفات PDF في المواقع الحكومية
echo 'site:gov filetype:pdf "confidential"' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm

# العثور على لوحات إدارة مكشوفة
echo 'inurl:admin intitle:"login"' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm

# محركات بحث متعددة مع نفس الاستكشاف
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:duckduckgo" -pm > duckduckgo_results.txt
echo 'intext:"internal use only"' | ./strx -st "echo {STRING}" -module "clc:bing" -pm > bing_results.txt

# مقارنة النتائج بين المحركات
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:google" -pm | sort > google_results.txt
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:bing" -pm | sort > bing_results.txt
comm -23 google_results.txt bing_results.txt > google_exclusive.txt
```

### الاستكشاف مع البروكسي
```bash
# استخدام بروكسي للاستكشاف لتجنب الحظر
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "http://127.0.0.1:9050" -pm

# استخدام بروكسي مع مصادقة
cat dorks.txt | ./strx -st "echo {STRING}" -module "clc:yahoo" -proxy "http://user:pass@server:8080" -pm

# الاستكشاف مع TOR
./strx -l sensitive_dorks.txt -st "echo {STRING}" -module "clc:google" -proxy "https://127.0.0.1:9050" -pm -t 1 -sleep 5

# استكشاف بإخراج منظم + بروكسي مع مصادقة
./strx -l sqli_dorks.txt -st "echo {STRING}" -module "clc:googlecse" -proxy "http://user:pass@10.0.0.1:8080" -pm -module "out:json" -pm

# جمع موزع عبر قائمة بروكسيات
cat proxy_list.txt | while read proxy; do
  ./strx -l target_dorks.txt -st "echo {STRING}" -module "clc:bing" -proxy "$proxy" -pm -t 3 -sleep 2
done > combined_results.txt
```

## 🔧 الوظائف المدمجة


يتضمن String-X أكثر من 25 وظيفة مدمجة يمكن استخدامها ضمن قوالب `{STRING}` وأوامر الأنابيب. تتم معالجة هذه الوظائف قبل تنفيذ أوامر shell وتغطي hash، encoding، معالجة النصوص، توليد قيم عشوائية، تحليل البيانات، التحقق من الوثائق، طلبات HTTP، معالجة الملفات وأكثر.

### بناء الجملة
```bash
# وظيفة بسيطة
./strx -l data.txt -st "funcao({STRING})" -pf

# وظائف متعددة
./strx -l data.txt -st "{STRING}; md5({STRING}); base64({STRING})" -pf

# وظيفة مع معاملات
./strx -l data.txt -st "str_rand(10); int_rand(5)" -pf
```


### الوظائف المتاحة (الرئيسية)

| الوظيفة | الوصف | مثال |
|--------|-----------|---------|
| `clear` | إزالة المساحات والتبويبات وفواصل الأسطر | `clear({STRING})` |
| `base64` / `debase64` | ترميز/فك ترميز Base64 | `base64({STRING})` |
| `hex` / `dehex` | ترميز/فك ترميز سادس عشري | `hex({STRING})` |
| `sha1`, `sha256`, `md5` | توليد hash | `sha256({STRING})` |
| `str_rand`, `int_rand` | توليد نص/رقم عشوائي | `str_rand(10)` |
| `ip` | حل اسم المضيف إلى IP | `ip({STRING})` |
| `replace` | استبدال نص فرعي | `replace(http:,https:,{STRING})` |
| `get` | طلب HTTP GET | `get(https://{STRING})` |
| `urlencode` | ترميز URL | `urlencode({STRING})` |
| `rev` | عكس النص | `rev({STRING})` |
| `timestamp` | الطابع الزمني الحالي | `timestamp()` |
| `extract_domain` | استخراج النطاق من URL | `extract_domain({STRING})` |
| `jwt_decode` | فك ترميز JWT (الحمولة) | `jwt_decode({STRING})` |
| `whois_lookup` | استعلام WHOIS | `whois_lookup({STRING})` |
| `cert_info` | معلومات شهادة SSL | `cert_info({STRING})` |
| `user_agent` | User-Agent عشوائي | `user_agent()` |
| `cidr_expand` | توسيع نطاق CIDR | `cidr_expand(192.168.0.0/30)` |
| `subdomain_gen` | توليد نطاقات فرعية شائعة | `subdomain_gen({STRING})` |
| `email_validator` | التحقق من البريد الإلكتروني | `email_validator({STRING})` |
| `hash_file` | hashes الملف | `hash_file(path.txt)` |
| `encode_url_all` | ترميز URL (الكل) | `encode_url_all({STRING})` |
| `phone_format` | تنسيق الهاتف البرازيلي | `phone_format({STRING})` |
| `password_strength` | قوة كلمة المرور | `password_strength({STRING})` |
| `social_media_extract` | استخراج معرفات وسائل التواصل الاجتماعي | `social_media_extract({STRING})` |
| `leak_check_format` | تنسيق البريد الإلكتروني للتسريبات | `leak_check_format({STRING})` |
| `cpf_validate` | التحقق من CPF | `cpf_validate({STRING})` |


> انظر القائمة الكاملة والأمثلة في `utils/helper/functions.py` أو استخدم `-functions` في CLI للحصول على وثائق مفصلة.

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

- **`-pf`**: عرض نتائج الوظائف فقط (تجاهل تنفيذ shell)
- **`-of`**: حفظ نتائج الوظائف في ملف إخراج

```bash
# عرض نتيجة الوظائف فقط
./strx -l domains.txt -st "{STRING}; md5({STRING})" -pf

# حفظ الوظائف في ملف
./strx -l data.txt -st "base64({STRING})" -pf -of -o encoded.txt
```

### مثال على الوظيفة
> **💡 نصيحة**: يمكنك إضافة وظائف مخصصة بتحرير ملف `utils/helper/functions.py`
```python
@staticmethod
def check_admin_exemplo(value: str) -> str:
  try:
      if '<p>admin</p>' in value:
        return value
  except:
    return str()
```

### استخدام مثال الوظيفة
```bash
# تنفيذ الوظيفة المُنشأة
./strx -l data.txt -st "check_admin_exemplo({STRING})" -pf
```


## 🧩 نظام الوحدات

يستخدم String-X بنية معيارية قابلة للتوسيع تسمح بإضافة وظائف محددة دون تعديل الكود الرئيسي. الوحدات منظمة حسب النوع ومحملة ديناميكياً.

### أنواع الوحدات المتاحة

| النوع | الكود | الوصف | الموقع |
|------|--------|-----------|-------------|
| **Extractor** | `ext` | استخراج بيانات محددة باستخدام regex | `utils/auxiliary/ext/` |
| **Collector** | `clc` | جمع معلومات من APIs/الخدمات | `utils/auxiliary/clc/` |
| **Output** | `out` | تنسيق وإرسال البيانات | `utils/auxiliary/out/` |
| **Connection** | `con` | اتصالات متخصصة | `utils/auxiliary/con/` |
| **AI** | `ai` | الذكاء الاصطناعي  | `utils/auxiliary/ai/` |


#### بناء الجملة الأساسي
```bash
./strx -module "النوع:اسم_الوحدة"
```

#### المعاملات ذات الصلة
- **`-module النوع:الاسم`**: تحديد الوحدة المراد استخدامها
- **`-pm`**: عرض نتائج الوحدة فقط (حذف إخراج shell)


### وحدات المستخرج (EXT)
وحدات لاستخراج الأنماط والبيانات المحددة باستخدام regex:

| الوحدة      | الوصف                                 | مثال CLI |
|-------------|-------------------------------------------|-------------|
| `email`     | استخراج عناوين بريد إلكتروني صحيحة         | `-module "ext:email"` |
| `domain`    | استخراج النطاقات والنطاقات الفرعية             | `-module "ext:domain"` |
| `url`       | استخراج URLs كاملة (HTTP/HTTPS)         | `-module "ext:url"` |
| `phone`     | استخراج أرقام الهاتف (البرازيل)            | `-module "ext:phone"` |
| `credential`| استخراج بيانات الاعتماد والرموز والمفاتيح         | `-module "ext:credential"` |
| `ip`        | استخراج عناوين IPv4/IPv6                 | `-module "ext:ip"` |
| `hash`      | استخراج hashes MD5، SHA1، SHA256، SHA512    | `-module "ext:hash"` |

```bash
# مثال: استخراج رسائل البريد الإلكتروني من تفريغ البيانات
./strx -l database_dump.txt -st "echo '{STRING}'" -module "ext:email" -pm
```


### وحدات الجامع (CLC)
وحدات لجمع المعلومات الخارجية وواجهات برمجة التطبيقات والتحليل:

| الوحدة        | الوصف                                 | مثال CLI |
|---------------|-------------------------------------------|-------------|
| `archive`     | جمع URLs مؤرشفة من Wayback Machine | `-module "clc:archive"` |
| `bing`        | إجراء بحث استكشاف في Bing          | `-module "clc:bing"` |
| `crtsh`       | جمع شهادات SSL/TLS والنطاقات الفرعية | `-module "clc:crtsh"` |
| `dns`         | جمع سجلات DNS (A، MX، TXT، NS)     | `-module "clc:dns"` |
| `duckduckgo`  | إجراء بحث استكشاف في DuckDuckGo    | `-module "clc:duckduckgo"` |
| `emailverify` | التحقق من صحة البريد الإلكتروني (MX، SMTP)    | `-module "clc:emailverify"` |
| `ezilon`      | إجراء بحث استكشاف في Ezilon        | `-module "clc:ezilon"` |
| `geoip`       | الموقع الجغرافي لـ IPs                     | `-module "clc:geoip"` |
| `google`      | إجراء بحث استكشاف في Google        | `-module "clc:google"` |
| `googlecse`   | إجراء بحث استكشاف باستخدام Google CSE| `-module "clc:googlecse"` |
| `ipinfo`      | فحص منافذ IP/المضيف                 | `-module "clc:ipinfo"` |
| `lycos`       | إجراء بحث استكشاف في Lycos         | `-module "clc:lycos"` |
| `naver`       | إجراء بحث استكشاف في Naver (كوري)| `-module "clc:naver"` |
| `netscan`     | فحص الشبكة (المضيفون، الخدمات)         | `-module "clc:netscan"` |
| `shodan`      | استعلام Shodan API                       | `-module "clc:shodan"` |
| `sogou`       | إجراء بحث استكشاف في Sogou (صيني)| `-module "clc:sogou"` |
| `subdomain`   | تعداد النطاقات الفرعية                 | `-module "clc:subdomain"` |
| `virustotal`  | استعلام VirusTotal API                   | `-module "clc:virustotal"` |
| `whois`       | استعلام WHOIS للنطاقات                | `-module "clc:whois"` |
| `yahoo`       | إجراء بحث استكشاف في Yahoo         | `-module "clc:yahoo"` |

```bash
# مثال: جمع معلومات DNS
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm

# مثال: جمع معلومات باستخدام محركات البحث
./strx -l dorks.txt -st "echo {STRING}" -module "clc:bing" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:google" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:googlecse" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:yahoo" -pm
./strx -l dorks.txt -st "echo {STRING}" -module "clc:duckduckgo" -pm

# أمثلة استكشاف محددة
echo 'site:fbi.gov filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:google" -pm
echo 'site:github.com inurl:admin' | ./strx -st "echo {STRING}" -module "clc:googlecse" -pm
echo 'inurl:admin' | ./strx -st "echo {STRING}" -module "clc:lycos" -pm
echo 'site:github.com' | ./strx -st "echo {STRING}" -module "clc:ezilon" -pm
echo 'filetype:pdf' | ./strx -st "echo {STRING}" -module "clc:yahoo" -pm
```


### وحدات الإخراج (OUT)
وحدات لتنسيق وإخراج النتائج:

| الوحدة        | الوصف                                 | مثال CLI |
|---------------|-------------------------------------------|-------------|
| `json`        | حفظ النتائج بتنسيق JSON                  | `-module "out:json"` |
| `csv`         | حفظ النتائج بتنسيق CSV                   | `-module "out:csv"` |
| `xml`         | حفظ النتائج بتنسيق XML                   | `-module "out:xml"` |

```bash
# مثال: الحفظ في JSON
./strx -l data.txt -st "process {STRING}" -module "out:json" -pm
```


### وحدات الاتصال (CON)
وحدات للاتصال بالخدمات الخارجية وتكامل النتائج:

| الوحدة        | الوصف                                 | مثال CLI |
|---------------|-------------------------------------------|-------------|
| `sqlite`      | حفظ البيانات في قاعدة بيانات SQLite               | `-module "con:sqlite"` |
| `mysql`       | حفظ البيانات في قاعدة بيانات MySQL                | `-module "con:mysql"` |
| `telegram`    | إرسال النتائج عبر Telegram Bot         | `-module "con:telegram"` |
| `slack`       | إرسال النتائج عبر Slack Webhook        | `-module "con:slack"` |
| `opensearch`  | فهرسة النتائج في Open Search          | `-module "con:opensearch"` |
| `http_probe`  | إجراء فحوصات HTTP على المضيفين      | `-module "con:http_probe"` |
| `ftp`         | اتصال ونقل عبر FTP                   | `-module "con:ftp"` |
| `ssh`         | تنفيذ الأوامر عبر SSH                | `-module "con:ssh"` |

```bash
# مثال: الحفظ في SQLite
./strx -l data.txt -st "process {STRING}" -module "con:sqlite" -pm
```


### وحدات الذكاء الاصطناعي (AI)
وحدات للمطالبات للذكاء الاصطناعي:

| الوحدة        | الوصف                                 | مثال CLI |
|---------------|-------------------------------------------|-------------|
| `gemini`      | مطالبة Google Gemini AI - ([إنشاء مفتاح API](https://aistudio.google.com/app/apikey))    | `-module "ai:gemini"` |

```bash
# مثال: استخدام ملفات المطالبات
./strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm

# مثال: جمع URLs وإرسال للتحليل ببناء المطالبة
./strx -l urls.txt -st "echo 'تحليل URL: {STRING}'" -module "ai:gemini" -pm
```

#### أمثلة عملية
```bash
# استخراج رسائل البريد الإلكتروني وحفظها مرتبة
./strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# فحص DNS للنطاقات المشبوهة
./strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# أنبوب متعدد الوحدات
cat logs.txt | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | ./strx -st "echo {STRING}" -module "clc:dns" -pm

# استخراج URLs وفحص الحالة
./strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | ./strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

### تطوير وحدات جديدة

لإنشاء وحدات جديدة، اتبع الهيكل القياسي:

#### وحدة المستخرج (ext)
```python
"""
مقدمة الوحدة
"""
from core.basemodule import BaseModule
import re

class ModuleName(BaseModule):
    
    def __init__(self):
      super().__init__()


      # تحديد معلومات ميتا الوحدة
      self.meta.update({
          "name": "اسم الوحدة...",
          "description": "وصف الوحدة...",
          "author": "اسم المنشئ...",
          "type": "extractor | collector | Output..."
      })

      # تحديد الخيارات المطلوبة لهذه الوحدة
      self.options = {
          "data":   str(),
          "regex":  str(),
          "proxy":  str()
      }
    
    # دالة إجبارية للتنفيذ
    def run(self):
        """
        سياق منطق الوحدة
          > الوصول لمعلومات الخيارات عبر: self.options.get(key_name)
        """
        # حفظ معلومات تنفيذ الوحدة
        self.set_result(value_regex)
```

### المرشحات والوحدات

يمكنك دمج المرشحات مع الوحدات للمعالجة الأكثر تحديداً:

```bash
# استخراج رسائل البريد الإلكتروني من نطاقات .gov فقط
./strx -l data.txt -st "echo '{STRING}'" -module "ext:email" -pm -f ".gov"

# بحث DNS للنطاقات .br فقط
./strx -l domains.txt -st "echo {STRING}" -module "clc:dns" -pm -f ".br"
```

## 🎯 المرشحات والمعالجة الانتقائية

نظام المرشحات يسمح بمعالجة النصوص التي تلبي معايير محددة فقط، مما يحسن الأداء والدقة.

### استخدام المرشحات
```bash
./strx -f "قيمة_المرشح" / ./strx --filter "قيمة_المرشح"
```

### أمثلة المرشحات
```bash
# تصفية نطاقات .gov.br فقط
./strx -l domains.txt -st "curl {STRING}" -f ".gov.br"

# تصفية URLs HTTPS فقط
./strx -l urls.txt -st "curl {STRING}" -f "https"

# تصفية IPs محددة
./strx -l logs.txt -st "analyze {STRING}" -f "192.168"

# تصفية امتدادات الملفات
./strx -l files.txt -st "process {STRING}" -f ".pdf"

# تصفية نتائج الوظائف التي تحتوي على "admin" فقط
./strx -l urls.txt -st "{STRING}; md5({STRING})" -pf -iff "admin"

# تصفية نتائج الوحدة التي تحتوي على hash محدد فقط
./strx -l domains.txt -st "echo {STRING}" -module "ext:hash" -pm -ifm "a1b2c3"

# دمج مرشحات الوظائف والوحدة
./strx -l data.txt -st "{STRING}; md5({STRING})" -module "ext:domain" -pf -pm -iff "google" -ifm "admin"
```

### دمج مع الوحدات
```bash
# استخراج رسائل البريد الإلكتروني وحفظها مرتبة
./strx -l breach_data.txt -st "echo '{STRING}'" -module "ext:email" -pm | sort -u > emails.txt

# فحص DNS للنطاقات المشبوهة
./strx -l suspicious_domains.txt -st "echo {STRING}" -module "clc:dns" -pm -v

# أنبوب متعدد الوحدات
cat logs.txt | ./strx -st "echo '{STRING}'" -module "ext:domain" -pm | ./strx -st "echo {STRING}" -module "clc:dns" -pm

# استخراج URLs وفحص الحالة
./strx -l pages.txt -st "cat {STRING}" -module "ext:url" -pm | ./strx -st "curl -I {STRING}" -p "grep 'HTTP/'"
```

## ⚡ المعالجة المتوازية

يدعم String-X المعالجة المتوازية عبر الخيوط لتسريع العمليات على كميات كبيرة من البيانات.

### تكوين الخيوط
```bash
# تحديد عدد الخيوط
./strx -t 50 / ./strx -thread 50

# تحديد التأخير بين الخيوط
./strx -sleep 2
```

### أمثلة الخيوط
```bash
# فحص سريع لحالة HTTP
./strx -l big_url_list.txt -st "curl -I {STRING}" -p "grep 'HTTP/'" -t 100

# حل DNS بالجملة
./strx -l huge_domain_list.txt -st "dig +short {STRING}" -t 50 -sleep 1

# فحص المنافذ
./strx -l ip_list.txt -st "nmap -p 80,443 {STRING}" -t 20 -sleep 3
```

### أفضل الممارسات للخيوط
- **تحديد المعدل**: استخدم `-sleep` لتجنب إرهاق الخدمات
- **العدد المناسب**: اضبط `-t` وفقاً للموارد المتاحة
- **المراقبة**: استخدم `-v 1` للمعلومات الأساسية، `-v 3` للتصحيح المفصل، `-v all` للتحكم الأقصى

### معالجة الملفات الكبيرة
تم تحسين String-X لمعالجة الملفات الكبيرة بكفاءة:
```bash
# معالجة ملف كبير بخيوط متعددة
strx -l ملف_كبير.txt -st "echo {STRING}" -module "ext:email" -pm -t 20 -sleep 1

# للملفات الكبيرة جداً، استخدم خيوط أقل وتأخير أكثر
strx -l مجموعة_بيانات_ضخمة.txt -st "process {STRING}" -t 10 -sleep 2 -v
```

## 🛡️ نظام الأمان

يتضمن String-X عمليات التحقق من الأمان لمنع تنفيذ الأوامر الخبيثة:

### عمليات التحقق النشطة
- **حجم المدخلات**: يحدد بيانات الإدخال إلى 1 ميجابايت افتراضياً
- **كمية النصوص**: حد أقصى 10,000 نص لكل تنفيذ
- **الأنماط الخطيرة**: يكتشف ويحجب الأوامر المحتمل أن تكون خبيثة
- **الخيوط**: يحدد الخيوط المتزامنة لتجنب إرهاق النظام

### تعطيل عمليات التحقق من الأمان
**⚠️ تحذير**: استخدم فقط عند الضرورة وعندما تثق في المحتوى

```bash
# تعطيل التحققات للأوامر المعقدة المشروعة
strx -l بيانات.txt -st "echo {STRING}; md5sum {STRING}" -ds

# معالجة ملفات كبيرة بدون قيود
strx -l ملف_ضخم.txt -st "process {STRING}" -ds -t 50

# الاستخدام مع وظائف قد تولد أنماط مكتشفة كمشبوهة
echo "test" | strx -st "echo {STRING}; echo 'نتيجة'" -ds
```

### وضع التصحيح للأمان
```bash
# عرض تفاصيل عمليات التحقق من الأمان (تصحيح كامل)
strx -l بيانات.txt -st "command {STRING}" -v 3

# التحقق من سبب حجب أمر
strx -s "test" -st "أمر_مشبوه" -v 3
```
## 📸 أمثلة بصرية

### التنفيذ الأساسي
**الأمر**: `cat hosts.txt | ./strx -str 'host {STRING}'`

![Screenshot](/asset/img1.png)

### معالجة الخيوط
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
2. **أنشئ** فرع ميزتك (`git checkout -b feature/AmazingFeature`)
3. **أرسل** تغييراتك (`git commit -m 'Add some AmazingFeature'`)
4. **ادفع** إلى الفرع (`git push origin feature/AmazingFeature`)
5. **افتح** Pull Request

### أنواع المساهمة
- 🐛 **إصلاح الأخطاء**
- ✨ **ميزات جديدة**
- 📝 **تحسين الوثائق**
- 🧩 **وحدات جديدة**
- ⚡ **تحسينات الأداء**

### تطوير الوحدات
لإنشاء وحدات جديدة، اطلع على قسم [نظام الوحدات](#-نظام-الوحدات) واتبع المعايير المحددة.

## 📄 الترخيص

هذا المشروع مرخص تحت ترخيص MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 👨‍💻 المؤلف

**MrCl0wn**
- 🌐 **المدونة**: [http://blog.mrcl0wn.com](http://blog.mrcl0wn.com)
- 🐙 **GitHub**: [@MrCl0wnLab](https://github.com/MrCl0wnLab) | [@MrCl0wnLab](https://github.com/MrCl0wnLab)
- 🐦 **Twitter**: [@MrCl0wnLab](https://twitter.com/MrCl0wnLab)
- 📧 **البريد الإلكتروني**: mrcl0wnlab@gmail.com

---

<div align="center">

**⭐ إذا كان هذا المشروع مفيداً، فكر في إعطائه نجمة!**

**💡 الاقتراحات والتعليقات مرحب بها دائماً!**

**💀 هاكر هاكيا!**

</div>
