# Desenvolvimento do String-X

Esta seção contém documentação técnica para desenvolvedores que desejam entender, contribuir ou estender as funcionalidades do String-X.

## Índice de Desenvolvimento

- [Estrutura do Projeto](estrutura-projeto.md) - Organização geral dos diretórios e arquivos ✅
- [Criação de Módulos](criacao-modulos.md) - Guia completo para criar novos módulos ✅
- [Criação de Funções](criacao-funcoes.md) - Guia para adicionar funções ao sistema de templates ✅
- [Uso como Biblioteca](uso-como-biblioteca.md) - Como usar String-X em scripts Python ✅
- [Arquitetura](arquitetura.md) - Design e arquitetura geral do String-X
- [Sistema de Tipos](sistema-tipos.md) - Como funciona o sistema de tipos e validação de dados
- [Sistema de Output](sistema-output.md) - Formatadores de saída e integração com sistemas externos
- [Contribuição](contribuicao.md) - Guia para contribuir com o projeto

## Visão Geral Técnica

O String-X é uma ferramenta de linha de comando escrita em Python 3.12+, projetada com uma arquitetura modular que permite fácil extensão através de plugins e módulos. O sistema foi construído seguindo princípios de design orientado a objetos e padrões de projeto que facilitam sua manutenção e extensibilidade.

### Principais Componentes

#### Core System

O núcleo do String-X gerencia:

1. **Processamento de Entrada**: lida com entradas de diferentes fontes (arquivos, linha de comando, stdin)
2. **Sistema de Templates**: implementa a substituição dinâmica de `{STRING}` 
3. **Gerenciamento de Threads**: controla a execução paralela de tarefas
4. **Sistema de Logging**: manipula logs e saídas de debug
5. **Gerenciador de Módulos**: carrega e executa módulos dinamicamente

#### Sistema de Módulos

O String-X implementa um sistema de plugins que categoriza módulos em diferentes tipos:

- **EXT**: Extratores para processar e validar tipos específicos (email, IP, URL, etc.)
- **CLC**: Coletores que obtêm dados de serviços externos (Google, Shodan, DNS, etc.) 
- **CON**: Conectores para comunicação com diferentes protocolos (HTTP, FTP, SSH)
- **OUT**: Formatadores de saída e conexão com sistemas de armazenamento
- **AI**: Módulos de Inteligência Artificial para análise e processamento

#### Sistema de Extensão

O String-X foi projetado para ser facilmente estendido através de:

1. **Herança de Classes Base**: Todos os módulos herdam de classes base que fornecem funcionalidades comuns
2. **Registro Automático**: Novos módulos são automaticamente detectados e registrados
3. **API Consistente**: Interface uniforme para módulos de mesmo tipo

## Fluxo de Processamento

1. **Parsing de Argumentos**: Processamento dos parâmetros de linha de comando
2. **Carregamento de Módulos**: Detecção e inicialização de módulos disponíveis
3. **Processamento de Entrada**: Leitura dos dados de entrada (arquivo, string, stdin)
4. **Execução de Comandos/Módulos**: Processamento dos dados através de comandos shell ou módulos
5. **Formatação de Saída**: Preparação dos resultados no formato solicitado
6. **Armazenamento/Exibição**: Gravação ou exibição dos resultados

## Guias Rápidos

### 🚀 Início Rápido para Desenvolvedores

1. **[Estrutura do Projeto](estrutura-projeto.md)** - Entenda a organização do código
2. **[Criação de Módulos](criacao-modulos.md)** - Crie seu primeiro módulo em 10 minutos
3. **[Criação de Funções](criacao-funcoes.md)** - Adicione novas funções ao sistema
4. **[Uso como Biblioteca](uso-como-biblioteca.md)** - Integre String-X em seus projetos

### 🔧 Principais Pontos de Extensão

#### Criar Novo Módulo Extrator
```python
# 1. Arquivo: src/stringx/utils/auxiliary/ext/meu_modulo.py
from stringx.core.basemodule import BaseModule

class AuxRegexMeuModulo(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta.update({
            "name": "Meu Módulo",
            "type": "extractor"
        })
    
    def run(self):
        # Implementar lógica
        pass
```

#### Adicionar Nova Função
```python
# 2. No arquivo: src/stringx/utils/helper/functions.py
@staticmethod
def minha_funcao(value: str) -> str:
    """Nova função para templates."""
    try:
        # Implementar transformação
        return resultado
    except:
        return str()
```

#### Usar como Biblioteca
```python
# 3. Em seu script Python
from stringx.utils.auxiliary.ext.email import AuxRegexEmail

extrator = AuxRegexEmail()
extrator.options['data'] = "Texto com email@exemplo.com"
extrator.run()
emails = extrator.get_result()
```

### 📊 Estatísticas do Projeto

- **25+** Módulos Extratores (EXT)
- **20+** Módulos Coletores (CLC) 
- **10+** Módulos Conectores (CON)
- **5+** Módulos de Saída (OUT)
- **25+** Funções Built-in
- **Multi-threading** nativo
- **Docker** support
- **5 idiomas** de documentação

### 🏗️ Arquitetura Modular

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │────│  Core Engine    │────│   Output        │
│                 │    │                 │    │                 │
│ • ArgumentParser│    │ • Command       │    │ • Formatters    │
│ • FileLocal     │    │ • AutoModulo    │    │ • FileLocal     │
│ • ThreadProcess │    │ • BaseModule    │    │ • Console       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                    ┌─────────────────┐
                    │ Module Ecosystem │
                    │                 │
                    │ EXT │ CLC │ CON  │
                    │ OUT │ AI  │ ...  │
                    └─────────────────┘
```

### 💡 Dicas de Desenvolvimento

#### Debugging
```bash
# Verbose mode para desenvolvimento
./strx -s "test" -st "{STRING}" -module "ext:email" -ns -pm -v 3
```

#### Testing
```python
# Teste unitário básico
import unittest
from stringx.utils.auxiliary.ext.email import AuxRegexEmail

class TestMeuModulo(unittest.TestCase):
    def test_basic(self):
        modulo = AuxRegexEmail()
        modulo.options['data'] = "test@example.com"
        modulo.run()
        self.assertTrue(len(modulo.get_result()) > 0)
```

#### Performance
```python
# Profile performance
import cProfile
cProfile.run('meu_modulo.run()')
```

Para detalhes específicos sobre cada componente, consulte as páginas de documentação listadas no índice.
