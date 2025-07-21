# Arquitetura do String-X

Este documento descreve a arquitetura geral do String-X, explicando os principais componentes, suas interações e os padrões de design utilizados no projeto.

## Visão Arquitetural

O String-X foi projetado seguindo princípios de design modular, com uma clara separação de responsabilidades entre seus componentes. A arquitetura geral pode ser dividida em camadas:

```
┌───────────────────────────────────────────────────────┐
│                  Interface de Usuário                 │
│  (Linha de comando, Argumentos, Banners, Formatação)  │
└───────────────────────────────────────────────────────┘
                            ▲
                            │
                            ▼
┌───────────────────────────────────────────────────────┐
│                      Core Engine                      │
│  (Processamento, Threading, Logging, Configurações)   │
└───────────────────────────────────────────────────────┘
                            ▲
                            │
                            ▼
┌───────────────────────────────────────────────────────┐
│                  Sistema de Módulos                   │
│      (Extratores, Coletores, Conectores, Output)      │
└───────────────────────────────────────────────────────┘
                            ▲
                            │
                            ▼
┌───────────────────────────────────────────────────────┐
│               Sistemas Externos / APIs                │
│  (Serviços Web, Bancos de Dados, Ferramentas Externas)│
└───────────────────────────────────────────────────────┘
```

## Componentes Principais

### 1. Interface de Usuário

O componente de interface de usuário é responsável por:

- **Processamento de Argumentos**: Interpretação dos parâmetros fornecidos via linha de comando
- **Exibição de Saídas**: Formatação e exibição dos resultados para o usuário
- **Feedback Visual**: Banners, barras de progresso e indicadores de status
- **Tratamento de Erros**: Exibição de mensagens de erro amigáveis

Arquivos Principais:
- `strx` (script principal)
- `core/style_cli.py`
- `core/banner/asciiart.py`

### 2. Core Engine

O Core Engine é o coração do String-X, responsável pelo:

- **Fluxo de Execução**: Gerenciamento do fluxo geral de processamento
- **Multi-threading**: Execução paralela de tarefas
- **Gestão de Recursos**: Controle de utilização de recursos do sistema
- **Logging**: Registro de operações e erros
- **Configuração**: Gerenciamento de configurações globais e locais

Arquivos Principais:
- `core/command.py`
- `core/thread_process.py`
- `core/logger.py`
- `config/setting.py`

### 3. Sistema de Módulos

O sistema de módulos implementa uma arquitetura de plugins, permitindo:

- **Extensibilidade**: Adição fácil de novos módulos sem modificar o código-base
- **Categorização**: Organização de módulos por tipo e funcionalidade
- **Interface Consistente**: API padronizada para cada tipo de módulo
- **Descoberta Automática**: Detecção e carregamento dinâmico de módulos

Arquivos Principais:
- `core/basemodule.py`
- `core/auto_module.py`
- `utils/auxiliary/` (diretórios de módulos)

### 4. Sistema de Entrada/Saída

Gerencia o fluxo de dados através do sistema:

- **Leitura de Entrada**: Processamento de arquivos, stdin, ou strings diretas
- **Template System**: Substituição dinâmica de `{STRING}` em templates
- **Formatação de Saída**: Transformação dos resultados em diferentes formatos
- **Persistência**: Armazenamento dos resultados em arquivos ou bancos de dados

Arquivos Principais:
- `core/filelocal.py`
- `core/format.py`
- `core/output_formatter.py`

## Padrões de Design

O String-X utiliza diversos padrões de design para garantir um código modular, extensível e de fácil manutenção:

### 1. Factory Method

Utilizado para instanciar diferentes tipos de módulos sem acoplar o código à implementação específica.

**Exemplo**:
```python
# Em core/auto_module.py
def create_module(module_type, module_name):
    module_class = find_module_class(module_type, module_name)
    if module_class:
        return module_class()
    return None
```

### 2. Strategy Pattern

Implementado na forma como diferentes módulos de mesmo tipo (ex: vários coletores CLC) compartilham uma interface comum mas têm implementações distintas.

**Exemplo**:
```python
# Em core/basemodule.py
class BaseCollector:
    def collect(self, query, **kwargs):
        raise NotImplementedError("Collector modules must implement collect method")

# Em utils/auxiliary/clc/google.py
class GoogleCollector(BaseCollector):
    def collect(self, query, **kwargs):
        # Implementação específica do Google
        return results
```

### 3. Command Pattern

Usado no sistema de execução de comandos e na forma como o String-X processa operações.

**Exemplo**:
```python
# Em core/command.py
class Command:
    def __init__(self, cmd_template):
        self.cmd_template = cmd_template
    
    def execute(self, string_value):
        cmd = self.cmd_template.replace("{STRING}", string_value)
        # Execução do comando
        return result
```

### 4. Template Method

Aplicado nas classes base que definem o "esqueleto" de um algoritmo, permitindo que subclasses implementem etapas específicas.

**Exemplo**:
```python
# Em core/basemodule.py
class BaseExtractor:
    def process(self, data):
        cleaned_data = self.clean(data)
        extracted = self.extract(cleaned_data)
        validated = self.validate(extracted)
        return validated
        
    def clean(self, data):
        # Implementação padrão
        return data
        
    def extract(self, data):
        raise NotImplementedError("Extractor modules must implement extract method")
        
    def validate(self, data):
        # Implementação padrão
        return data
```

### 5. Observer Pattern

Utilizado no sistema de logging e monitoramento de eventos.

**Exemplo**:
```python
# Em core/logger.py
class Logger:
    def __init__(self):
        self.observers = []
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def log(self, message, level):
        for observer in self.observers:
            observer.update(message, level)
```

## Fluxo de Dados

O fluxo de dados através do sistema String-X segue estas etapas:

1. **Entrada**
   - O usuário fornece uma string, arquivo ou dados via stdin
   - O parser de argumentos interpreta os parâmetros fornecidos

2. **Pré-processamento**
   - Os dados de entrada são normalizados
   - O sistema identifica os comandos ou módulos a serem executados

3. **Execução**
   - Para cada item de entrada:
     - O template é preenchido com o valor atual
     - O comando é executado ou o módulo é invocado
     - Os resultados são capturados

4. **Pós-processamento**
   - Os resultados são formatados de acordo com o formato solicitado
   - Filtros adicionais são aplicados, se especificados

5. **Saída**
   - Os resultados são exibidos no terminal ou
   - Gravados em um arquivo de saída ou
   - Enviados para sistemas externos (banco de dados, etc.)

## Integração com Sistemas Externos

O String-X foi projetado para integrar-se facilmente com sistemas externos:

### 1. Execução de Comandos do Sistema

O String-X pode executar praticamente qualquer comando do sistema operacional através de seu sistema de templates, permitindo integração com ferramentas externas.

### 2. APIs Web

Através dos módulos coletores (CLC), o String-X pode interagir com diversas APIs web para obter dados de:
- Motores de busca (Google, Bing, DuckDuckGo)
- Plataformas de segurança (Shodan, VirusTotal)
- Serviços de informação (WHOIS, DNS)

### 3. Bancos de Dados

Os módulos de saída (OUT) permitem armazenar resultados em:
- Bancos relacionais (MySQL)
- Sistemas de busca (OpenSearch)
- Sistemas NoSQL (opcional através de módulos personalizados)

### 4. Serviços de AI

Módulos AI integram com serviços de inteligência artificial:
- OpenAI (GPT)
- Google Gemini

## Escalabilidade e Performance

A arquitetura do String-X foi projetada considerando escalabilidade e performance:

### 1. Processamento Paralelo

- O sistema de multi-threading permite executar tarefas em paralelo
- A quantidade de threads é configurável para adaptar-se aos recursos disponíveis

### 2. Controle de Recursos

- Mecanismos de timeout evitam que operações bloqueiem indefinidamente
- Sistema de retry para lidar com falhas transitórias

### 3. Processamento Assíncrono

- Operações de rede são realizadas de forma assíncrona quando possível
- O cliente HTTP assíncrono permite executar múltiplas requisições simultaneamente

## Extensibilidade

A arquitetura modular do String-X facilita sua extensão:

### 1. Novos Módulos

- Criação de módulos através de herança das classes base
- Registro automático de novos módulos sem modificar o código principal

### 2. Funcionalidades Adicionais

- A arquitetura de plugins permite adicionar novas funcionalidades sem alterar o núcleo
- Sistema de configuração permite personalização sem modificação de código

### 3. Integração com Novas Ferramentas

- O sistema de templates permite integração com praticamente qualquer ferramenta de linha de comando
- Novos módulos conectores podem ser adicionados para integrar com sistemas específicos

## Considerações de Segurança

A arquitetura considera aspectos de segurança:

- **Validação de Entrada**: Os dados de entrada são validados antes do processamento
- **Sanitização de Comandos**: Proteções contra injeção de comandos maliciosos
- **Gestão de Credenciais**: Mecanismos para armazenar e proteger credenciais de APIs
- **Controle de Acesso**: Limitação de operações conforme permissões do usuário

## Limitações e Considerações

- **Dependência de Ferramentas Externas**: Algumas funcionalidades dependem de ferramentas que precisam estar instaladas
- **Overhead de Processos**: A execução de comandos externos pode gerar overhead
- **Compatibilidade**: Certas funcionalidades podem variar entre diferentes sistemas operacionais
