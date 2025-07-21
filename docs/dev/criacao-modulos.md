# Criação de Módulos

Este documento fornece um guia detalhado sobre como criar novos módulos para o String-X, abordando desde o processo básico até técnicas avançadas.

## Tipos de Módulos

O String-X suporta diferentes tipos de módulos, cada um com propósito específico:

| Tipo | Descrição | Diretório |
|------|-----------|-----------|
| **EXT** | **Extratores**: Processam e extraem informações de strings | `utils/auxiliary/ext/` |
| **CLC** | **Coletores**: Obtêm dados de fontes externas | `utils/auxiliary/clc/` |
| **CON** | **Conectores**: Comunicação com serviços e protocolos | `utils/auxiliary/con/` |
| **OUT** | **Output**: Formatam e exportam resultados | `utils/auxiliary/out/` |
| **AI** | **Inteligência Artificial**: Integram com serviços de AI | `utils/auxiliary/ai/` |

## Estrutura Básica de um Módulo

Todo módulo no String-X segue uma estrutura semelhante:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.basemodule import BaseExtractor  # Ou outro tipo base apropriado

class MeuModulo(BaseExtractor):  # Herda da classe base apropriada
    """
    Descrição do que o módulo faz.
    """
    
    def __init__(self):
        """
        Inicializa o módulo e define seus atributos básicos.
        """
        super().__init__()
        self.name = "meu_modulo"
        self.description = "Descrição curta do módulo"
        self.author = "Seu Nome"
        self.version = "1.0"
        
    def extract(self, data, **kwargs):
        """
        Método principal que implementa a funcionalidade do módulo.
        
        Args:
            data (str): Os dados de entrada a serem processados
            **kwargs: Argumentos adicionais específicos do módulo
            
        Returns:
            list: Resultados processados
        """
        # Implementação específica do módulo
        resultado = []
        
        # Lógica de processamento
        # ...
        
        return resultado
```

## Passos para Criar um Novo Módulo

### 1. Decidir o Tipo de Módulo

Escolha o tipo de módulo baseado na funcionalidade que deseja implementar:
- **EXT**: Para extrair padrões ou validar tipos de dados
- **CLC**: Para coletar informações de serviços externos
- **CON**: Para conectar-se a serviços através de protocolos específicos
- **OUT**: Para exportar dados para diferentes formatos ou sistemas
- **AI**: Para integrar com APIs de inteligência artificial

### 2. Criar o Arquivo do Módulo

Crie um novo arquivo Python no diretório correspondente ao tipo escolhido:

```bash
touch utils/auxiliary/[tipo]/meu_modulo.py
```

Onde `[tipo]` é um dos seguintes: `ext`, `clc`, `con`, `out`, `ai`.

### 3. Implementar a Classe do Módulo

Cada tipo de módulo deve herdar da classe base apropriada e implementar os métodos obrigatórios:

#### Para Módulos Extratores (EXT):

```python
from core.basemodule import BaseExtractor

class MeuExtrator(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.name = "meu_extrator"
        self.description = "Extrai informações específicas"
        
    def extract(self, data, **kwargs):
        """
        Implementação da lógica de extração.
        
        Args:
            data (str): Dados para extrair informações
            
        Returns:
            list: Elementos extraídos
        """
        # Lógica para extrair dados específicos
        resultados = []
        # Processo de extração...
        return resultados
```

#### Para Módulos Coletores (CLC):

```python
from core.basemodule import BaseCollector

class MeuColetor(BaseCollector):
    def __init__(self):
        super().__init__()
        self.name = "meu_coletor"
        self.description = "Coleta dados de alguma fonte"
        self.requires_apikey = True  # Se precisar de API key
        
    def collect(self, query, **kwargs):
        """
        Implementação da lógica de coleta.
        
        Args:
            query (str): Consulta para busca
            **kwargs: Pode incluir 'api_key', 'limit', etc.
            
        Returns:
            list: Resultados coletados
        """
        # Lógica para coletar dados
        api_key = kwargs.get('api_key', '')
        limit = kwargs.get('limit', 10)
        
        # Processo de coleta...
        resultados = []
        
        return resultados
```

#### Para Módulos Conectores (CON):

```python
from core.basemodule import BaseConnector

class MeuConector(BaseConnector):
    def __init__(self):
        super().__init__()
        self.name = "meu_conector"
        self.description = "Conecta a um serviço específico"
        
    def connect(self, target, **kwargs):
        """
        Implementação da lógica de conexão.
        
        Args:
            target (str): Alvo da conexão
            **kwargs: Parâmetros de conexão (porta, usuário, etc.)
            
        Returns:
            dict: Resultado da conexão
        """
        # Lógica para estabelecer conexão
        port = kwargs.get('port', 80)
        
        # Processo de conexão...
        resultado = {}
        
        return resultado
```

#### Para Módulos de Output (OUT):

```python
from core.basemodule import BaseOutput

class MeuOutput(BaseOutput):
    def __init__(self):
        super().__init__()
        self.name = "meu_output"
        self.description = "Exporta dados para algum formato/sistema"
        
    def output(self, data, **kwargs):
        """
        Implementação da lógica de saída.
        
        Args:
            data (list/dict): Dados a serem exportados
            **kwargs: Parâmetros de saída (arquivo, formato, etc.)
            
        Returns:
            bool: Sucesso ou falha da operação
        """
        # Lógica para exportar dados
        formato = kwargs.get('format', 'json')
        destino = kwargs.get('destination', 'output.txt')
        
        # Processo de exportação...
        
        return True  # Ou False em caso de erro
```

#### Para Módulos de AI (AI):

```python
from core.basemodule import BaseAI

class MeuModuloAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "meu_ai"
        self.description = "Integração com serviço de AI"
        self.requires_apikey = True
        
    def process(self, data, **kwargs):
        """
        Implementação da lógica de processamento com AI.
        
        Args:
            data (str/list): Dados a serem processados
            **kwargs: Parâmetros como API key, modelo, etc.
            
        Returns:
            dict: Resultado do processamento
        """
        # Lógica para integração com AI
        api_key = kwargs.get('api_key', '')
        model = kwargs.get('model', 'default')
        
        # Processamento com AI...
        resultados = {}
        
        return resultados
```

### 4. Implementar Métodos Auxiliares

Além do método principal, você pode adicionar métodos auxiliares para melhorar a organização do código:

```python
def _normalize_data(self, data):
    """
    Normaliza os dados de entrada para processamento.
    """
    # Lógica de normalização
    return data
    
def _validate_result(self, result):
    """
    Valida o resultado antes de retorná-lo.
    """
    # Lógica de validação
    return result
```

### 5. Registro do Módulo

O String-X utiliza um sistema de descoberta automática de módulos. Apenas garantindo que:

1. O módulo esteja no diretório correto para seu tipo
2. A classe herde da classe base correta
3. O método principal esteja implementado

O módulo será automaticamente descoberto e registrado sem necessidade de modificações adicionais.

## Práticas Recomendadas

### 1. Documentação

Sempre documente seu módulo adequadamente:

- Adicione docstrings para a classe e todos os métodos
- Explique claramente os parâmetros e valores de retorno
- Inclua exemplos de uso no docstring da classe

```python
class MeuModulo(BaseExtractor):
    """
    Extrai endereços de email de texto.
    
    Este módulo procura por padrões de email em uma string e retorna 
    todos os endereços de email válidos encontrados.
    
    Exemplos:
        >>> from utils.auxiliary.ext.meu_modulo import MeuModulo
        >>> modulo = MeuModulo()
        >>> modulo.extract("Contate-nos em: info@exemplo.com ou suporte@exemplo.com")
        ['info@exemplo.com', 'suporte@exemplo.com']
    """
```

### 2. Tratamento de Erros

Implemente tratamento de erros adequado para tornar seu módulo robusto:

```python
def collect(self, query, **kwargs):
    try:
        # Lógica principal
        response = self._make_api_request(query, **kwargs)
        return self._parse_response(response)
    except ConnectionError:
        self.logger.error("Erro de conexão ao serviço externo")
        return []
    except ValueError as e:
        self.logger.error(f"Erro de valor: {str(e)}")
        return []
    except Exception as e:
        self.logger.error(f"Erro desconhecido: {str(e)}")
        return []
```

### 3. Parâmetros Configuráveis

Torne seu módulo flexível através de parâmetros configuráveis:

```python
def extract(self, data, **kwargs):
    """
    Extrai padrões de acordo com os parâmetros fornecidos.
    
    Args:
        data (str): Texto para análise
        **kwargs: Parâmetros opcionais:
            - max_results (int): Número máximo de resultados (padrão: 100)
            - min_length (int): Comprimento mínimo do padrão (padrão: 3)
            - only_valid (bool): Retornar apenas resultados validados (padrão: True)
    
    Returns:
        list: Padrões extraídos
    """
    max_results = kwargs.get('max_results', 100)
    min_length = kwargs.get('min_length', 3)
    only_valid = kwargs.get('only_valid', True)
    
    # Lógica usando estes parâmetros
```

### 4. Logging

Utilize o sistema de logging do String-X para fornecer informações úteis:

```python
from core.logger import get_logger

class MeuModulo(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)
        
    def extract(self, data, **kwargs):
        self.logger.debug(f"Iniciando extração com {len(data)} caracteres")
        
        # Lógica de processamento
        
        self.logger.info(f"Extração concluída. {len(resultados)} itens encontrados")
        return resultados
```

### 5. Reutilização de Código

Evite duplicação utilizando funções auxiliares comuns:

```python
from utils.helper.functions import normalize_text, validate_pattern

class MeuModulo(BaseExtractor):
    def extract(self, data, **kwargs):
        # Reutilizar funções auxiliares
        normalized = normalize_text(data)
        patterns = self._find_patterns(normalized)
        return [p for p in patterns if validate_pattern(p)]
```

## Exemplos Completos de Módulos

### Exemplo de Extrator (EXT)

Um módulo para extrair coordenadas geográficas:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from core.basemodule import BaseExtractor

class GeoCoordinatesExtractor(BaseExtractor):
    """
    Extrator de coordenadas geográficas.
    
    Este módulo extrai coordenadas geográficas em diferentes formatos de um texto:
    - Decimal: 40.7128, -74.0060
    - Graus, minutos, segundos: 40°42'51.3"N 74°00'21.5"W
    """
    
    def __init__(self):
        super().__init__()
        self.name = "geocoord"
        self.description = "Extrai coordenadas geográficas"
        self.author = "String-X Team"
        self.version = "1.0"
        
        # Padrões regex para diferentes formatos de coordenadas
        self.decimal_pattern = r'[-+]?[0-9]*\.?[0-9]+,\s*[-+]?[0-9]*\.?[0-9]+'
        self.dms_pattern = r'(\d+)°(\d+)\'(\d+\.?\d*)\"([NS])\s+(\d+)°(\d+)\'(\d+\.?\d*)\"([EW])'
    
    def extract(self, data, **kwargs):
        """
        Extrai coordenadas geográficas do texto.
        
        Args:
            data (str): Texto contendo possíveis coordenadas
            **kwargs: Parâmetros opcionais:
                - format (str): Formato desejado ('all', 'decimal', 'dms')
                
        Returns:
            list: Coordenadas encontradas
        """
        format_type = kwargs.get('format', 'all')
        results = []
        
        if format_type in ['all', 'decimal']:
            decimal_coords = self._extract_decimal(data)
            results.extend(decimal_coords)
            
        if format_type in ['all', 'dms']:
            dms_coords = self._extract_dms(data)
            results.extend(dms_coords)
            
        return results
    
    def _extract_decimal(self, text):
        """
        Extrai coordenadas em formato decimal.
        """
        matches = re.finditer(self.decimal_pattern, text)
        return [match.group() for match in matches]
    
    def _extract_dms(self, text):
        """
        Extrai coordenadas em formato graus, minutos, segundos.
        """
        matches = re.finditer(self.dms_pattern, text)
        return [match.group() for match in matches]
    
    def _convert_dms_to_decimal(self, degrees, minutes, seconds, direction):
        """
        Converte coordenadas de DMS para decimal.
        """
        decimal = float(degrees) + float(minutes)/60 + float(seconds)/3600
        
        if direction in ['S', 'W']:
            decimal = -decimal
            
        return decimal
```

### Exemplo de Coletor (CLC)

Um módulo para coletar informações meteorológicas:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from core.basemodule import BaseCollector
from core.logger import get_logger

class WeatherCollector(BaseCollector):
    """
    Coletor de informações meteorológicas.
    
    Este módulo coleta dados meteorológicos de uma localização usando
    a API OpenWeatherMap.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "weather"
        self.description = "Coleta dados meteorológicos"
        self.author = "String-X Team"
        self.version = "1.0"
        self.requires_apikey = True
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.logger = get_logger(__name__)
        
    def collect(self, query, **kwargs):
        """
        Coleta dados meteorológicos para uma localização.
        
        Args:
            query (str): Cidade ou coordenadas para consulta
            **kwargs: Parâmetros opcionais:
                - api_key (str): Chave API para OpenWeatherMap
                - units (str): Unidade de temperatura ('metric', 'imperial')
                - lang (str): Código do idioma (ex: 'pt_br')
                
        Returns:
            dict: Dados meteorológicos ou vazio em caso de erro
        """
        api_key = kwargs.get('api_key', '')
        if not api_key:
            self.logger.error("API key is required for weather collection")
            return {}
            
        units = kwargs.get('units', 'metric')
        lang = kwargs.get('lang', 'en')
        
        params = {
            'q': query,
            'appid': api_key,
            'units': units,
            'lang': lang
        }
        
        # Verificar se a consulta parece ser coordenadas
        if ',' in query and len(query.split(',')) == 2:
            try:
                lat, lon = [float(c.strip()) for c in query.split(',')]
                params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': api_key,
                    'units': units,
                    'lang': lang
                }
                del params['q']
            except ValueError:
                # Não são coordenadas válidas, manter a consulta original
                pass
                
        try:
            self.logger.debug(f"Requesting weather data for {query}")
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"Successfully collected weather data for {query}")
                return self._format_weather_data(data)
            else:
                self.logger.error(f"Error collecting weather: {response.status_code}")
                return {}
                
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return {}
            
    def _format_weather_data(self, data):
        """
        Formata os dados meteorológicos para um formato mais amigável.
        """
        try:
            result = {
                'location': {
                    'name': data.get('name', ''),
                    'country': data.get('sys', {}).get('country', ''),
                    'coordinates': {
                        'lat': data.get('coord', {}).get('lat', 0),
                        'lon': data.get('coord', {}).get('lon', 0)
                    }
                },
                'weather': {
                    'condition': data.get('weather', [{}])[0].get('main', ''),
                    'description': data.get('weather', [{}])[0].get('description', ''),
                    'temperature': data.get('main', {}).get('temp', 0),
                    'feels_like': data.get('main', {}).get('feels_like', 0),
                    'humidity': data.get('main', {}).get('humidity', 0),
                    'pressure': data.get('main', {}).get('pressure', 0),
                    'wind': {
                        'speed': data.get('wind', {}).get('speed', 0),
                        'direction': data.get('wind', {}).get('deg', 0)
                    },
                    'clouds': data.get('clouds', {}).get('all', 0),
                    'visibility': data.get('visibility', 0)
                },
                'timestamp': data.get('dt', 0),
                'timezone': data.get('timezone', 0)
            }
            return result
        except Exception as e:
            self.logger.error(f"Error formatting weather data: {str(e)}")
            return {}
```

## Testando Seu Módulo

### 1. Teste Direto

Crie um script simples para testar seu módulo diretamente:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.auxiliary.clc.my_collector import MyCollector

def test_collector():
    collector = MyCollector()
    result = collector.collect("test query", api_key="your_test_key")
    print(f"Result: {result}")
    
if __name__ == "__main__":
    test_collector()
```

### 2. Teste via String-X

Teste seu módulo através da interface normal do String-X:

```bash
./strx -s "exemplo.com" -module "clc:my_collector" -pm -api-key "your_test_key"
```

### 3. Testes Unitários

Para testes mais formais, crie testes unitários:

```python
import unittest
from utils.auxiliary.ext.my_extractor import MyExtractor

class TestMyExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = MyExtractor()
        
    def test_basic_extraction(self):
        data = "Text with pattern123 and pattern456"
        result = self.extractor.extract(data)
        self.assertEqual(len(result), 2)
        self.assertIn("pattern123", result)
        self.assertIn("pattern456", result)
        
    def test_empty_input(self):
        result = self.extractor.extract("")
        self.assertEqual(result, [])
        
if __name__ == "__main__":
    unittest.main()
```

## Distribuição do Módulo

### 1. Contribuindo para o String-X

Se deseja que seu módulo seja incluído na distribuição oficial do String-X:

1. Faça um fork do repositório
2. Adicione seu módulo no diretório apropriado
3. Certifique-se de que segue os padrões de código
4. Adicione testes para seu módulo
5. Atualize a documentação
6. Envie um pull request

### 2. Distribuição Separada

Para distribuir seu módulo separadamente:

1. Crie um repositório para seu módulo
2. Inclua instruções claras sobre como instalá-lo no diretório de módulos do String-X
3. Forneça exemplos de uso

## Considerações Avançadas

### 1. Dependências Externas

Se seu módulo requer bibliotecas adicionais, documente-as claramente:

```python
"""
Requisitos:
    - requests>=2.25.0
    - beautifulsoup4>=4.9.0
"""

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Este módulo requer as bibliotecas 'requests' e 'beautifulsoup4'")
    print("Instale com: pip install requests beautifulsoup4")
    raise
```

### 2. Configuração Persistente

Para módulos que requerem configuração complexa, implemente um sistema de configuração persistente:

```python
import os
import json
from config.setting import get_config_path

class ComplexModule(BaseCollector):
    def __init__(self):
        super().__init__()
        self.config_file = os.path.join(get_config_path(), "complex_module_config.json")
        self.config = self._load_config()
        
    def _load_config(self):
        """Carrega configuração do arquivo ou usa padrão"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuração padrão
        return {
            "setting1": "default",
            "setting2": 123,
            "enabled_features": ["feature1", "feature2"]
        }
        
    def _save_config(self):
        """Salva configuração atual no arquivo"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
```

### 3. Módulos Compostos

Para funcionalidades complexas, considere dividir seu módulo em componentes:

```python
# utils/auxiliary/clc/social_media.py
from core.basemodule import BaseCollector

class SocialMediaCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.name = "social"
        self.description = "Coleta informações de mídias sociais"
        
    def collect(self, query, **kwargs):
        platform = kwargs.get('platform', 'all')
        
        results = {}
        
        if platform in ['all', 'twitter']:
            from .social_collectors.twitter import TwitterCollector
            twitter = TwitterCollector()
            results['twitter'] = twitter.collect_data(query, **kwargs)
            
        if platform in ['all', 'linkedin']:
            from .social_collectors.linkedin import LinkedinCollector
            linkedin = LinkedinCollector()
            results['linkedin'] = linkedin.collect_data(query, **kwargs)
            
        return results
```
