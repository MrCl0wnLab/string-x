# Contribuição

Este documento fornece diretrizes para contribuir com o projeto String-X, incluindo processo de desenvolvimento, padrões de código e fluxo de trabalho para submissão de contribuições.

## Primeiros Passos

### Preparando o Ambiente de Desenvolvimento

1. **Fork do repositório**

   Faça um fork do repositório String-X para sua conta pessoal no GitHub.

2. **Clone do repositório**

   ```bash
   git clone https://github.com/seu-usuario/string-x.git
   cd string-x
   ```

3. **Configuração do ambiente de desenvolvimento**

   Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   pip install -e .  # Instala o projeto em modo de desenvolvimento
   ```

4. **Configure um branch para sua contribuição**

   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```

## Padrões de Código

### Estilo de Código

O String-X segue as diretrizes PEP 8 para código Python, com algumas adaptações:

1. **Indentação**: 4 espaços (não tabs)
2. **Comprimento máximo de linha**: 100 caracteres
3. **Docstrings**: Obrigatórias para todas as funções, classes e módulos
4. **Convenções de nomenclatura**:
   - Classes: `PascalCase`
   - Funções e variáveis: `snake_case`
   - Constantes: `UPPER_CASE`
   - Módulos: `snake_case`
   - Privado/Interno: prefixado com underscore (`_private_method`)

### Estrutura de Documentação

Cada módulo, classe e função deve ter documentação adequada:

```python
def process_data(data, options=None):
    """
    Processa os dados de acordo com as opções fornecidas.
    
    Args:
        data (str): Os dados a serem processados
        options (dict, optional): Opções para controlar o processamento
            
    Returns:
        dict: Os dados processados
        
    Raises:
        ValueError: Se os dados forem inválidos
        
    Examples:
        >>> process_data("exemplo", {"option1": True})
        {'processed': 'exemplo', 'status': 'success'}
    """
```

### Organização de Imports

Os imports devem ser organizados em blocos na seguinte ordem:

1. Bibliotecas padrão do Python
2. Bibliotecas de terceiros
3. Módulos do String-X

```python
# Bibliotecas padrão
import os
import sys
import json
from datetime import datetime

# Bibliotecas de terceiros
import requests
from bs4 import BeautifulSoup

# Módulos do String-X
from core.basemodule import BaseExtractor
from utils.helper.functions import normalize_text
```

### Gestão de Dependências

- Novas dependências devem ser adicionadas ao `requirements.txt`
- Utilize a versão mínima necessária (`requests>=2.25.0` em vez de `requests==2.28.1`)
- Para dependências opcionais, documente-as no arquivo README do módulo

## Fluxo de Trabalho de Desenvolvimento

### 1. Identificar uma Tarefa

- Procure por issues abertos no GitHub
- Verifique a lista de tarefas pendentes (TODO)
- Proponha novas funcionalidades na seção de issues

### 2. Implementar a Mudança

Ao implementar uma mudança:

- Mantenha o escopo da mudança focado
- Escreva testes para novas funcionalidades
- Mantenha a compatibilidade com versões anteriores quando possível
- Documente suas mudanças

### 3. Testes

O String-X utiliza o framework `unittest` para testes:

```python
import unittest
from utils.auxiliary.ext.my_module import MyExtractor

class TestMyExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = MyExtractor()
        
    def test_basic_extraction(self):
        data = "Sample text with example@email.com"
        result = self.extractor.extract(data)
        self.assertIn("example@email.com", result)
        
    def test_empty_input(self):
        result = self.extractor.extract("")
        self.assertEqual(result, [])
```

Para executar os testes:

```bash
python -m unittest discover tests
```

### 4. Commit e Push

Siga as convenções para mensagens de commit:

```
tipo(escopo): resumo conciso

Descrição detalhada das mudanças (opcional)
```

Tipos comuns:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação de código
- `refactor`: Refatoração de código
- `test`: Adição ou modificação de testes
- `chore`: Tarefas de manutenção

Exemplo:

```
feat(ext): adiciona extrator para URLs de mídias sociais

- Implementa regex para detectar URLs do Twitter, Facebook e Instagram
- Adiciona validação de URLs específicas de cada plataforma
- Inclui testes para diferentes formatos de URL
```

### 5. Criar Pull Request

- Crie um Pull Request (PR) a partir do seu branch para o repositório principal
- Descreva claramente o que sua contribuição faz
- Referencie quaisquer issues relacionados
- Verifique se todos os testes passam
- Solicite revisão dos mantenedores

## Estrutura de Diretórios

Ao adicionar novos arquivos, siga a estrutura de diretórios existente:

- **Módulos EXT**: `utils/auxiliary/ext/`
- **Módulos CLC**: `utils/auxiliary/clc/`
- **Módulos CON**: `utils/auxiliary/con/`
- **Módulos OUT**: `utils/auxiliary/out/`
- **Módulos AI**: `utils/auxiliary/ai/`
- **Testes**: `tests/utils/auxiliary/{tipo}/`
- **Documentação**: `docs/`

## Diretrizes para Tipos Específicos de Contribuição

### 1. Novos Módulos

Ao criar um novo módulo:

1. Use a classe base apropriada
2. Implemente todos os métodos obrigatórios
3. Adicione documentação clara
4. Escreva testes abrangentes
5. Atualize a documentação geral se necessário

### 2. Correções de Bugs

Para correções de bugs:

1. Identifique claramente o problema
2. Forneça um caso de teste que reproduza o bug
3. Explique sua solução
4. Adicione testes para evitar regressões

### 3. Melhorias de Performance

Para otimizações:

1. Meça o desempenho antes e depois
2. Documente os ganhos de performance
3. Garanta que a funcionalidade permaneça intacta

### 4. Documentação

Para melhorias na documentação:

1. Siga o estilo existente
2. Inclua exemplos práticos
3. Verifique ortografia e gramática
4. Mantenha a documentação atualizada com o código

## Guias Específicos

### 1. Criando um Novo Extrator (EXT)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from core.basemodule import BaseExtractor

class MeuExtrator(BaseExtractor):
    """
    Descrição detalhada do que o extrator faz.
    
    Exemplos:
        >>> extrator = MeuExtrator()
        >>> extrator.extract("Texto com padrão123")
        ["padrão123"]
    """
    
    def __init__(self):
        super().__init__()
        self.name = "meu_extrator"
        self.description = "Extrai padrões específicos"
        self.author = "Seu Nome"
        self.version = "1.0"
        
        # Definir padrões regex ou outras constantes
        self.pattern = r'padrão\d+'
        
    def extract(self, data, **kwargs):
        """
        Extrai padrões do texto.
        
        Args:
            data (str): Texto para análise
            **kwargs: Parâmetros opcionais
                - case_sensitive (bool): Considerar maiúsculas/minúsculas
                
        Returns:
            list: Padrões encontrados
        """
        if not data or not isinstance(data, str):
            return []
            
        case_sensitive = kwargs.get('case_sensitive', True)
        
        # Definir flags da regex
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # Encontrar padrões
        matches = re.finditer(self.pattern, data, flags=flags)
        return [match.group() for match in matches]
```

### 2. Criando um Novo Coletor (CLC)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from core.basemodule import BaseCollector
from core.logger import get_logger

class MeuColetor(BaseCollector):
    """
    Descrição detalhada do que o coletor faz.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "meu_coletor"
        self.description = "Coleta dados de alguma fonte"
        self.author = "Seu Nome"
        self.version = "1.0"
        self.requires_apikey = True  # Se precisar de API key
        self.logger = get_logger(__name__)
        
    def collect(self, query, **kwargs):
        """
        Coleta dados com base na consulta.
        
        Args:
            query (str): Consulta para busca
            **kwargs: Parâmetros opcionais
                - api_key (str): Chave de API
                - limit (int): Limite de resultados
                
        Returns:
            list: Resultados coletados
        """
        api_key = kwargs.get('api_key', '')
        limit = kwargs.get('limit', 10)
        
        if not api_key and self.requires_apikey:
            self.logger.error("API key é obrigatória")
            return []
            
        try:
            # Implementação da coleta
            self.logger.debug(f"Coletando dados para: {query}")
            
            # Exemplo de requisição
            response = requests.get(
                "https://api.exemplo.com/search",
                params={"q": query, "limit": limit},
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                results = self._process_results(data)
                self.logger.info(f"Coletados {len(results)} resultados")
                return results
            else:
                self.logger.error(f"Erro na API: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Erro na coleta: {str(e)}")
            return []
            
    def _process_results(self, data):
        """
        Processa os resultados da API.
        """
        # Implementação específica para processar dados
        return []
```

## Lista de Verificação para Contribuições

Antes de submeter uma contribuição, verifique se:

- [ ] O código segue as diretrizes de estilo
- [ ] A documentação foi atualizada
- [ ] Foram adicionados testes para novas funcionalidades
- [ ] Todos os testes estão passando
- [ ] As dependências foram atualizadas apropriadamente
- [ ] O código foi testado em diferentes ambientes
- [ ] Não foram introduzidas vulnerabilidades de segurança

## Guia para Revisores

Ao revisar Pull Requests, considere:

1. **Funcionalidade**: O código faz o que se propõe?
2. **Qualidade**: O código segue as diretrizes de estilo e boas práticas?
3. **Testes**: Existem testes adequados que cobrem a funcionalidade?
4. **Documentação**: A documentação é clara e completa?
5. **Performance**: O código é eficiente?
6. **Segurança**: Existem potenciais problemas de segurança?
7. **Compatibilidade**: O código mantém compatibilidade com versões anteriores?

## Política de Branches

- `main`: Branch principal, sempre estável
- `develop`: Branch de desenvolvimento, para integração de features
- `feature/*`: Branches para novas funcionalidades
- `fix/*`: Branches para correções de bugs
- `release/*`: Branches para preparação de releases
- `hotfix/*`: Branches para correções urgentes em produção

## Processo de Release

O processo para criar uma nova release:

1. Merge das features para `develop`
2. Criação de branch `release/vX.Y.Z`
3. Testes finais e correções
4. Atualização de versão e changelog
5. Merge para `main` e tag da versão
6. Merge de volta para `develop`

## Dicas Adicionais

### Integração com Ferramentas Externas

Para módulos que integram com ferramentas externas:

1. Forneça instruções claras para instalação das ferramentas
2. Implemente verificações para garantir que as ferramentas estão disponíveis
3. Ofereça fallbacks quando possível

### Considerações de Segurança

Ao trabalhar com dados potencialmente sensíveis:

1. Não armazene credenciais no código
2. Sanitize entradas para evitar injeções
3. Valide respostas de APIs externas

### Contribuição com Documentação

A documentação é tão importante quanto o código. Considere:

1. Atualizar o README geral
2. Adicionar exemplos práticos
3. Criar tutoriais para casos de uso específicos
4. Melhorar mensagens de erro e ajuda

## Código de Conduta

Ao contribuir com o String-X, você concorda em:

1. Tratar todos os participantes com respeito
2. Aceitar críticas construtivas
3. Focar no que é melhor para a comunidade
4. Mostrar empatia com outros membros da comunidade

## Agradecimentos

Suas contribuições são fundamentais para o sucesso do String-X. Agradecemos pelo seu tempo e esforço para melhorar este projeto!
