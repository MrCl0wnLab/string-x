# Sistema de Tipos

Este documento explica o sistema de tipos do String-X, que é responsável por validar, processar e manipular diferentes tipos de dados através dos módulos extratores (EXT).

## Visão Geral

O sistema de tipos no String-X fornece uma forma consistente de:

1. **Identificar** tipos específicos de dados (URLs, IPs, emails, etc.)
2. **Validar** se uma string corresponde a um tipo específico
3. **Extrair** instâncias de um tipo específico de um texto mais amplo
4. **Transformar** dados entre tipos relacionados
5. **Enriquecer** dados com informações adicionais

Este sistema é implementado principalmente através de módulos extratores (EXT), que seguem uma interface comum e podem ser usados de forma intercambiável.

## Tipos Suportados

O String-X suporta vários tipos de dados integrados:

| Tipo | Módulo | Descrição | Exemplos |
|------|--------|-----------|----------|
| **URL** | `ext:url` | Uniform Resource Locators | `https://example.com/path?query=value` |
| **Domínio** | `ext:domain` | Nomes de domínio | `example.com`, `sub.example.co.uk` |
| **Email** | `ext:email` | Endereços de email | `user@example.com` |
| **IP** | `ext:ip` | Endereços IP (v4 e v6) | `192.168.1.1`, `2001:db8::1` |
| **Hash** | `ext:hash` | Valores hash (MD5, SHA1, etc.) | `5f4dcc3b5aa765d61d8327deb882cf99` |
| **Telefone** | `ext:phone` | Números de telefone | `+1 (555) 123-4567` |
| **MAC** | `ext:mac` | Endereços MAC | `00:1A:2B:3C:4D:5E` |
| **Criptomoeda** | `ext:cryptocurrency` | Endereços de criptomoedas | `1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2` |
| **Credencial** | `ext:credential` | Credenciais de login | `username:password` |
| **Documento** | `ext:documents` | Metadados de documentos | Diversos |

## Arquitetura do Sistema de Tipos

### Classe Base

Todos os tipos são implementados como módulos extratores que herdam da classe base `BaseExtractor` definida em `core/basemodule.py`:

```python
class BaseExtractor:
    """Classe base para todos os módulos extratores."""
    
    def __init__(self):
        self.name = ""
        self.description = ""
        self.author = ""
        self.version = ""
    
    def extract(self, data, **kwargs):
        """
        Método principal que deve ser implementado por todas as subclasses.
        
        Args:
            data (str): Dados a serem processados
            **kwargs: Parâmetros adicionais para controlar o comportamento da extração
            
        Returns:
            list: Lista de valores extraídos
        """
        raise NotImplementedError("Método extract deve ser implementado")
    
    def validate(self, item):
        """
        Valida se um único item corresponde a este tipo.
        
        Args:
            item (str): Item a ser validado
            
        Returns:
            bool: True se o item for válido, False caso contrário
        """
        # Implementação padrão que pode ser sobrescrita
        extracted = self.extract(item)
        return len(extracted) > 0 and extracted[0] == item
```

### Ciclo de Vida do Processamento

Quando um módulo extrator é utilizado, o ciclo de vida típico segue estas etapas:

1. **Inicialização**: O módulo é instanciado
2. **Entrada**: Os dados são passados para o método `extract()`
3. **Processamento**: O módulo processa os dados de acordo com sua lógica específica
4. **Validação**: Opcionalmente, os resultados são validados antes de serem retornados
5. **Saída**: Os resultados processados são retornados como uma lista

## Implementação de Tipos

Cada tipo é implementado como um módulo extrator separado. Vejamos um exemplo detalhado:

### Exemplo: Implementação de URL Extractor

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from core.basemodule import BaseExtractor

class URLExtractor(BaseExtractor):
    """
    Extrator de URLs.
    
    Este módulo identifica e extrai URLs válidas de um texto.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "url"
        self.description = "Extrai URLs de texto"
        self.author = "String-X Team"
        self.version = "1.0"
        
        # Regex para identificar URLs
        # Esta é uma versão simplificada, a real seria mais complexa
        self.url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        
    def extract(self, data, **kwargs):
        """
        Extrai URLs de um texto.
        
        Args:
            data (str): Texto contendo possíveis URLs
            **kwargs:
                - require_protocol (bool): Exigir protocolo http(s) (padrão: True)
                - validate (bool): Validar URLs após extração (padrão: True)
                
        Returns:
            list: Lista de URLs encontradas
        """
        if not data or not isinstance(data, str):
            return []
            
        require_protocol = kwargs.get('require_protocol', True)
        validate_results = kwargs.get('validate', True)
        
        # Ajustar o padrão baseado nos parâmetros
        pattern = self.url_pattern
        if not require_protocol:
            # Padrão mais flexível que aceita URLs sem protocolo
            pattern = r'(?:https?://)?(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        
        # Encontrar todas as ocorrências
        matches = re.finditer(pattern, data)
        results = [match.group() for match in matches]
        
        # Validar resultados se solicitado
        if validate_results:
            results = [url for url in results if self._validate_url(url)]
            
        return results
        
    def validate(self, item):
        """
        Verifica se um item é uma URL válida.
        
        Args:
            item (str): Item a validar
            
        Returns:
            bool: True se for uma URL válida, False caso contrário
        """
        if not item or not isinstance(item, str):
            return False
            
        return self._validate_url(item)
        
    def _validate_url(self, url):
        """
        Implementação interna da validação de URL.
        
        Verifica se a URL tem formato válido e componentes necessários.
        """
        # Verificação básica de formato
        basic_match = re.match(self.url_pattern, url)
        if not basic_match:
            return False
            
        # Verificações adicionais podem ser implementadas aqui
        # Por exemplo: verificar tamanho máximo, caracteres válidos, etc.
        
        return True
```

### Exemplo: Implementação de Email Extractor

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from core.basemodule import BaseExtractor

class EmailExtractor(BaseExtractor):
    """
    Extrator de endereços de email.
    
    Este módulo identifica e extrai endereços de email válidos de um texto.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "email"
        self.description = "Extrai endereços de email de texto"
        self.author = "String-X Team"
        self.version = "1.0"
        
        # Regex para identificar emails
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
    def extract(self, data, **kwargs):
        """
        Extrai endereços de email de um texto.
        
        Args:
            data (str): Texto contendo possíveis emails
            **kwargs:
                - strict (bool): Usar validação estrita (padrão: False)
                - lowercase (bool): Converter emails para minúsculas (padrão: True)
                
        Returns:
            list: Lista de emails encontrados
        """
        if not data or not isinstance(data, str):
            return []
            
        strict_mode = kwargs.get('strict', False)
        lowercase = kwargs.get('lowercase', True)
        
        # Encontrar todas as ocorrências
        matches = re.finditer(self.email_pattern, data)
        results = [match.group() for match in matches]
        
        # Aplicar validação se no modo estrito
        if strict_mode:
            results = [email for email in results if self._validate_email_strict(email)]
            
        # Converter para minúsculas se solicitado
        if lowercase:
            results = [email.lower() for email in results]
            
        return results
        
    def validate(self, item):
        """
        Verifica se um item é um email válido.
        
        Args:
            item (str): Item a validar
            
        Returns:
            bool: True se for um email válido, False caso contrário
        """
        if not item or not isinstance(item, str):
            return False
            
        # Verificação básica de formato
        basic_match = re.match(self.email_pattern, item)
        return basic_match is not None
        
    def _validate_email_strict(self, email):
        """
        Implementa validação mais rigorosa de email.
        
        Verifica regras adicionais como:
        - Comprimento máximo de componentes
        - Caracteres permitidos
        - Formato de domínio válido
        """
        # Verificar formato básico primeiro
        if not re.match(self.email_pattern, email):
            return False
            
        # Separar em componentes locais e de domínio
        local, domain = email.split('@', 1)
        
        # Verificar comprimentos
        if len(local) > 64 or len(domain) > 255:
            return False
            
        # Verificar se o domínio tem pelo menos um ponto
        if '.' not in domain:
            return False
            
        # Verificar partes do domínio
        domain_parts = domain.split('.')
        for part in domain_parts:
            if not part or len(part) > 63:
                return False
                
        return True
```

## Interação Entre Tipos

Os módulos de tipo podem trabalhar juntos para formar pipelines de processamento de dados:

```bash
# Extrair URLs de um texto, depois extrair domínios das URLs
./strx -l texto.txt -module "ext:url|ext:domain" -pm
```

Neste exemplo:
1. O módulo `ext:url` extrai todas as URLs do texto
2. O módulo `ext:domain` processa as URLs para extrair os domínios

Esta capacidade de encadeamento permite fluxos de trabalho sofisticados para transformação e enriquecimento de dados.

## Extensibilidade do Sistema de Tipos

O sistema de tipos é altamente extensível. Para criar um novo tipo:

1. Identifique um novo tipo de dado que seria útil extrair ou validar
2. Crie um novo módulo que herde de `BaseExtractor`
3. Implemente o método `extract()` para identificar/extrair o tipo
4. Opcionalmente, sobrescreva `validate()` para validação especializada
5. Adicione o arquivo do módulo ao diretório `utils/auxiliary/ext/`

### Exemplo: Criando um Extrator para Coordenadas GPS

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from core.basemodule import BaseExtractor

class GPSCoordinateExtractor(BaseExtractor):
    """
    Extrator de coordenadas GPS.
    
    Extrai coordenadas geográficas em formato decimal de um texto.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "gps"
        self.description = "Extrai coordenadas GPS"
        self.author = "Your Name"
        self.version = "1.0"
        
        # Regex para coordenadas GPS decimais
        # Exemplo: 40.7128, -74.0060
        self.decimal_pattern = r'[-+]?[0-9]*\.?[0-9]+,\s*[-+]?[0-9]*\.?[0-9]+'
        
    def extract(self, data, **kwargs):
        """
        Extrai coordenadas GPS de um texto.
        
        Args:
            data (str): Texto contendo possíveis coordenadas
            **kwargs:
                - format (str): Formato desejado ('decimal', 'dms', 'all')
                - validate (bool): Validar coordenadas após extração
                
        Returns:
            list: Lista de coordenadas encontradas
        """
        if not data or not isinstance(data, str):
            return []
            
        format_type = kwargs.get('format', 'decimal')
        validate_results = kwargs.get('validate', True)
        
        results = []
        
        # Extrair coordenadas decimais
        if format_type in ['decimal', 'all']:
            decimal_matches = re.finditer(self.decimal_pattern, data)
            decimal_coords = [match.group() for match in decimal_matches]
            results.extend(decimal_coords)
            
        # Validar resultados se solicitado
        if validate_results:
            results = [coord for coord in results if self._validate_coordinate(coord)]
            
        return results
        
    def _validate_coordinate(self, coordinate):
        """
        Valida uma coordenada para garantir que está em faixa válida.
        """
        try:
            # Assumindo formato "lat, lon"
            lat_str, lon_str = coordinate.split(',')
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            
            # Verificar faixas válidas
            if lat < -90 or lat > 90:
                return False
                
            if lon < -180 or lon > 180:
                return False
                
            return True
        except:
            return False
```

## Melhores Práticas

### Para Usuários do Sistema de Tipos

1. **Combinar Módulos**: Utilize o encadeamento de módulos para processamentos complexos
2. **Parâmetros Específicos**: Aproveite os parâmetros específicos de cada tipo para controlar o comportamento
3. **Validação**: Utilize o modo estrito quando a precisão for mais importante que a abrangência
4. **Filtragem**: Use pipes para filtrar resultados quando necessário

### Para Desenvolvedores de Novos Tipos

1. **Siga a Interface**: Implemente corretamente os métodos obrigatórios
2. **Documente Parâmetros**: Descreva claramente todos os parâmetros que seu módulo aceita
3. **Validação Robusta**: Implemente validação adequada para garantir qualidade dos resultados
4. **Tratamento de Erros**: Lide adequadamente com entradas inválidas ou inesperadas
5. **Otimização**: Para tipos que serão usados em grandes volumes de dados, otimize o desempenho
6. **Teste Abrangente**: Teste com uma variedade de casos, incluindo casos de borda

## Casos de Uso Avançados

### 1. Extração Multi-tipo

Extrair e categorizar diferentes tipos de dados de um texto:

```bash
./strx -l documento.txt -module "ext:email|ext:url|ext:ip|ext:phone" -pm -format json -o dados_extraidos.json
```

### 2. Transformação de Tipos

Converter entre tipos relacionados:

```bash
# Converter URLs para domínios
./strx -l urls.txt -module "ext:domain" -pm -o dominios.txt

# Extrair IPs de URLs
./strx -l urls.txt -module "ext:url|ext:ip" -pm -o ips.txt
```

### 3. Validação em Lote

Validar grandes conjuntos de dados:

```bash
# Filtrar apenas emails válidos de uma lista
./strx -l possivel_emails.txt -module "ext:email" -pm -strict true -o emails_validos.txt
```

### 4. Enriquecimento de Dados

Combinar tipos com coletores para enriquecer dados:

```bash
# Extrair domínios e obter informações DNS
./strx -l texto.txt -module "ext:domain|clc:dns" -pm -o info_dns.json -format json
```

## Limitações e Considerações

1. **Precisão vs. Abrangência**: Extrair tipos de texto livre sempre envolve um equilíbrio entre capturar todos os casos possíveis (abrangência) e evitar falsos positivos (precisão)

2. **Desempenho**: Para textos muito grandes, a extração de tipos pode ser intensiva em termos de recursos, especialmente com expressões regulares complexas

3. **Contexto**: A extração baseada em padrões não considera o contexto semântico, podendo ocasionalmente identificar falsos positivos

4. **Internacionalização**: Alguns tipos podem ter variações específicas de cada país ou região (como números de telefone)

## Futuras Direções

O sistema de tipos pode evoluir em várias direções:

1. **Aprendizado de Máquina**: Incorporar técnicas de ML para melhorar a precisão da extração

2. **Tipos Contextuais**: Desenvolver extratores que considerem o contexto semântico

3. **Validação Avançada**: Integrar verificação online para validar tipos em tempo real

4. **Mais Tipos Especializados**: Adicionar suporte para tipos como:
   - CPF/CNPJ e outros IDs nacionais
   - Endereços físicos
   - Coordenadas em diversos formatos
   - Identificadores de cartão de crédito
   - Chaves de API
   - Tokens JWT
   - Identificadores de serviços específicos
