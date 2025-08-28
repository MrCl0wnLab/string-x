# Usando String-X como Biblioteca Python

Este guia explica como integrar o String-X em seus próprios scripts Python, usando seus módulos e funcionalidades como biblioteca.

## Visão Geral

O String-X pode ser usado como uma biblioteca Python para:

- **Extrair dados** usando módulos EXT (email, URL, IP, etc.)
- **Coletar informações** usando módulos CLC (DNS, whois, APIs)
- **Conectar com sistemas** usando módulos CON (MySQL, MongoDB, APIs)
- **Formatar saídas** usando módulos OUT (JSON, CSV, XML)
- **Usar funções auxiliares** para transformações de dados
- **Processar dados em lote** com pipeline personalizado

## Instalação para Uso como Biblioteca

### 1. Instalação em Modo Desenvolvimento
```bash
git clone https://github.com/MrCl0wnLab/string-x.git
cd string-x
pip install -e .
```

### 2. Instalação via Pip (quando disponível)
```bash
pip install string-x
```

### 3. Importação Direta
```bash
# Adicionar ao PYTHONPATH
export PYTHONPATH="/path/to/string-x/src:$PYTHONPATH"
```

## Estrutura de Importação

```python
# Importações básicas
from stringx.core.basemodule import BaseModule
from stringx.utils.helper.functions import Funcs
from stringx.core.auto_modulo import AutoModulo
from stringx.core.output_formatter import OutputFormatter

# Importar módulos específicos
from stringx.utils.auxiliary.ext.email import AuxRegexEmail
from stringx.utils.auxiliary.ext.url import AuxRegexURL
from stringx.utils.auxiliary.clc.dns import AuxDNSCollector
from stringx.utils.auxiliary.con.mysql import AuxMySQLConnector
```

## Usando Módulos Extratores (EXT)

### Exemplo 1: Extração de Emails

```python
#!/usr/bin/env python3
"""
Exemplo: Extrair emails de um texto usando String-X como biblioteca.
"""
import sys
sys.path.insert(0, '/path/to/string-x/src')

from stringx.utils.auxiliary.ext.email import AuxRegexEmail

def extrair_emails(texto):
    """
    Extrai emails de um texto usando o módulo String-X.
    
    Args:
        texto (str): Texto para extrair emails
        
    Returns:
        list: Lista de emails encontrados
    """
    # Criar instância do módulo
    extrator = AuxRegexEmail()
    
    # Configurar dados de entrada
    extrator.options['data'] = texto
    
    # Executar extração
    extrator.run()
    
    # Obter resultados
    emails = extrator.get_result()
    
    return emails

# Exemplo de uso
if __name__ == "__main__":
    texto_exemplo = """
    Entre em contato conosco:
    - Email comercial: vendas@empresa.com
    - Suporte técnico: suporte@empresa.com.br
    - CEO: ceo@startup.io
    """
    
    emails_encontrados = extrair_emails(texto_exemplo)
    
    print("Emails encontrados:")
    for i, email in enumerate(emails_encontrados, 1):
        print(f"{i}. {email}")
```

### Exemplo 2: Extração de URLs com Filtros

```python
#!/usr/bin/env python3
"""
Exemplo: Extrair URLs com filtros personalizados.
"""
from stringx.utils.auxiliary.ext.url import AuxRegexURL

class ExtratorURLPersonalizado:
    """
    Classe para extração de URLs com funcionalidades adicionais.
    """
    
    def __init__(self):
        self.extrator = AuxRegexURL()
    
    def extrair_urls(self, texto, filtros=None):
        """
        Extrai URLs de um texto com filtros opcionais.
        
        Args:
            texto (str): Texto para extrair URLs
            filtros (list): Lista de filtros (domínios, extensões, etc.)
            
        Returns:
            dict: Resultados organizados
        """
        # Configurar e executar extração
        self.extrator.options['data'] = texto
        self.extrator.run()
        
        # Obter todas as URLs
        urls = self.extrator.get_result()
        
        resultado = {
            'total': len(urls),
            'urls': urls,
            'filtradas': []
        }
        
        # Aplicar filtros se fornecidos
        if filtros:
            for filtro in filtros:
                urls_filtradas = [url for url in urls if filtro in url]
                resultado['filtradas'].extend(urls_filtradas)
        
        return resultado
    
    def extrair_por_dominio(self, texto, dominio):
        """
        Extrai URLs de um domínio específico.
        
        Args:
            texto (str): Texto para buscar
            dominio (str): Domínio alvo (ex: "github.com")
            
        Returns:
            list: URLs do domínio especificado
        """
        resultado = self.extrair_urls(texto, [dominio])
        return resultado['filtradas']

# Exemplo de uso
if __name__ == "__main__":
    extrator = ExtratorURLPersonalizado()
    
    texto_html = """
    <p>Visite nossos repositórios:</p>
    <a href="https://github.com/usuario/projeto1">Projeto 1</a>
    <a href="https://github.com/usuario/projeto2">Projeto 2</a>
    <a href="https://gitlab.com/usuario/projeto3">Projeto 3</a>
    <a href="https://example.com/docs">Documentação</a>
    """
    
    # Extrair todas as URLs
    todos_resultados = extrator.extrair_urls(texto_html)
    print(f"Total de URLs encontradas: {todos_resultados['total']}")
    
    # Extrair apenas URLs do GitHub
    urls_github = extrator.extrair_por_dominio(texto_html, "github.com")
    print(f"URLs do GitHub: {len(urls_github)}")
    for url in urls_github:
        print(f"  - {url}")
```

## Usando Módulos Coletores (CLC)

### Exemplo 3: Consultas DNS Automáticas

```python
#!/usr/bin/env python3
"""
Exemplo: Realizar consultas DNS usando String-X como biblioteca.
"""
from stringx.utils.auxiliary.clc.dns import AuxDNSCollector
import time

class ConsultorDNS:
    """
    Classe para realizar consultas DNS em lote.
    """
    
    def __init__(self):
        self.coletor = AuxDNSCollector()
    
    def consultar_dominio(self, dominio, tipo_registro='A'):
        """
        Consulta DNS para um domínio específico.
        
        Args:
            dominio (str): Domínio para consultar
            tipo_registro (str): Tipo de registro DNS (A, MX, TXT, etc.)
            
        Returns:
            dict: Informações DNS organizadas
        """
        # Configurar consulta
        self.coletor.options['data'] = dominio
        self.coletor.options['record_type'] = tipo_registro
        
        # Executar consulta
        self.coletor.run()
        
        # Obter resultados
        registros = self.coletor.get_result()
        
        return {
            'dominio': dominio,
            'tipo': tipo_registro,
            'registros': registros,
            'quantidade': len(registros),
            'timestamp': time.time()
        }
    
    def consultar_multiplos_dominios(self, dominios, tipos=['A', 'MX']):
        """
        Consulta DNS para múltiplos domínios e tipos.
        
        Args:
            dominios (list): Lista de domínios
            tipos (list): Lista de tipos de registro
            
        Returns:
            list: Lista de resultados organizados
        """
        resultados = []
        
        for dominio in dominios:
            resultado_dominio = {'dominio': dominio, 'consultas': {}}
            
            for tipo in tipos:
                try:
                    consulta = self.consultar_dominio(dominio, tipo)
                    resultado_dominio['consultas'][tipo] = consulta
                    
                    # Pequeno delay para evitar rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    resultado_dominio['consultas'][tipo] = {
                        'erro': str(e),
                        'registros': []
                    }
            
            resultados.append(resultado_dominio)
        
        return resultados

# Exemplo de uso
if __name__ == "__main__":
    consultor = ConsultorDNS()
    
    dominios_teste = [
        "google.com",
        "github.com", 
        "stackoverflow.com"
    ]
    
    print("Iniciando consultas DNS...")
    
    # Consultar múltiplos domínios
    resultados = consultor.consultar_multiplos_dominios(dominios_teste)
    
    # Exibir resultados
    for resultado in resultados:
        dominio = resultado['dominio']
        print(f"\n=== {dominio} ===")
        
        for tipo, dados in resultado['consultas'].items():
            if 'erro' in dados:
                print(f"{tipo}: ERRO - {dados['erro']}")
            else:
                registros = dados['registros']
                print(f"{tipo}: {len(registros)} registro(s)")
                for registro in registros[:3]:  # Mostrar apenas os 3 primeiros
                    print(f"  - {registro}")
```

## Usando Módulos Conectores (CON)

### Exemplo 4: Integração com Banco de Dados

```python
#!/usr/bin/env python3
"""
Exemplo: Salvar dados no MySQL usando String-X como biblioteca.
"""
from stringx.utils.auxiliary.con.mysql import AuxMySQLConnector
from stringx.utils.auxiliary.ext.email import AuxRegexEmail
from stringx.utils.auxiliary.ext.url import AuxRegexURL
import json
from datetime import datetime

class ProcessadorDados:
    """
    Classe para processar dados e armazenar no banco.
    """
    
    def __init__(self, config_db):
        """
        Inicializa processador com configuração do banco.
        
        Args:
            config_db (dict): Configurações do MySQL
        """
        self.config_db = config_db
        self.extrator_email = AuxRegexEmail()
        self.extrator_url = AuxRegexURL()
        self.conector_mysql = AuxMySQLConnector()
        
        # Configurar conexão MySQL
        self.conector_mysql.options.update(config_db)
    
    def processar_e_armazenar(self, dados, tabela="dados_extraidos"):
        """
        Processa dados e armazena no MySQL.
        
        Args:
            dados (str): Dados para processar
            tabela (str): Nome da tabela no MySQL
            
        Returns:
            dict: Resumo do processamento
        """
        # Extrair emails
        self.extrator_email.options['data'] = dados
        self.extrator_email.run()
        emails = self.extrator_email.get_result()
        
        # Extrair URLs
        self.extrator_url.options['data'] = dados
        self.extrator_url.run()
        urls = self.extrator_url.get_result()
        
        # Preparar dados para armazenar
        resultado = {
            'timestamp': datetime.now().isoformat(),
            'emails_encontrados': emails,
            'urls_encontradas': urls,
            'total_emails': len(emails),
            'total_urls': len(urls),
            'dados_originais': dados[:200] + "..." if len(dados) > 200 else dados
        }
        
        # Salvar no MySQL
        self.conector_mysql.options.update({
            'table': tabela,
            'data': json.dumps(resultado)
        })
        
        self.conector_mysql.run()
        resultado_mysql = self.conector_mysql.get_result()
        
        resultado['mysql_status'] = resultado_mysql
        
        return resultado

# Exemplo de uso
if __name__ == "__main__":
    # Configuração do MySQL
    config_mysql = {
        'host': 'localhost',
        'port': 3306,
        'username': 'usuario',
        'password': 'senha',
        'database': 'stringx_db'
    }
    
    # Criar processador
    processador = ProcessadorDados(config_mysql)
    
    # Dados de exemplo
    texto_exemplo = """
    Nosso sistema de suporte está disponível através dos canais:
    
    Email: suporte@empresa.com
    Portal: https://suporte.empresa.com/tickets
    Documentação: https://docs.empresa.com
    
    Para emergências, contacte: emergencia@empresa.com.br
    Status do sistema: https://status.empresa.com
    """
    
    try:
        resultado = processador.processar_e_armazenar(texto_exemplo)
        
        print("Processamento concluído:")
        print(f"- Emails encontrados: {resultado['total_emails']}")
        print(f"- URLs encontradas: {resultado['total_urls']}")
        print(f"- Status MySQL: {resultado['mysql_status']}")
        
    except Exception as e:
        print(f"Erro durante processamento: {e}")
```

## Usando Funções Auxiliares

### Exemplo 5: Pipeline de Transformações

```python
#!/usr/bin/env python3
"""
Exemplo: Usar funções auxiliares do String-X em pipeline personalizado.
"""
from stringx.utils.helper.functions import Funcs

class ProcessadorTexto:
    """
    Pipeline de processamento usando funções String-X.
    """
    
    def __init__(self):
        self.funcs = Funcs()
    
    def pipeline_seguranca(self, dados):
        """
        Pipeline para análise de segurança de dados.
        
        Args:
            dados (list): Lista de strings para processar
            
        Returns:
            list: Dados processados com análise de segurança
        """
        resultados = []
        
        for item in dados:
            resultado = {
                'original': item,
                'md5': self.funcs.md5(item),
                'sha256': self.funcs.sha256(item),
                'base64': self.funcs.base64_encode(item),
                'url_encode': self.funcs.url_encode(item),
                'tamanho': len(item),
                'tem_ip': bool(self.funcs.extract_ip(item)),
                'tem_email': bool(self.funcs.extract_email(item))
            }
            
            resultados.append(resultado)
        
        return resultados
    
    def pipeline_urls(self, urls):
        """
        Pipeline específico para análise de URLs.
        
        Args:
            urls (list): Lista de URLs
            
        Returns:
            list: Análise detalhada das URLs
        """
        resultados = []
        
        for url in urls:
            resultado = {
                'url': url,
                'dominio': self.funcs.extract_domain(url),
                'ip_resolvido': self.funcs.resolve_ip(url),
                'status_http': self.funcs.check_http_status(url),
                'url_segura': url.startswith('https://'),
                'hash_url': self.funcs.sha256(url)
            }
            
            resultados.append(resultado)
        
        return resultados

# Exemplo de uso
if __name__ == "__main__":
    processador = ProcessadorTexto()
    
    # Dados de teste
    dados_teste = [
        "usuario@exemplo.com",
        "192.168.1.1",
        "senha123",
        "https://site-suspeito.com/login"
    ]
    
    urls_teste = [
        "https://google.com",
        "http://exemplo.com.br",
        "https://github.com/usuario/projeto"
    ]
    
    # Executar pipeline de segurança
    print("=== Pipeline de Segurança ===")
    resultados_seguranca = processador.pipeline_seguranca(dados_teste)
    
    for resultado in resultados_seguranca:
        print(f"\nItem: {resultado['original']}")
        print(f"  MD5: {resultado['md5']}")
        print(f"  SHA256: {resultado['sha256'][:16]}...")
        print(f"  Contém IP: {resultado['tem_ip']}")
        print(f"  Contém Email: {resultado['tem_email']}")
    
    # Executar pipeline de URLs
    print("\n=== Pipeline de URLs ===")
    resultados_urls = processador.pipeline_urls(urls_teste)
    
    for resultado in resultados_urls:
        print(f"\nURL: {resultado['url']}")
        print(f"  Domínio: {resultado['dominio']}")
        print(f"  IP: {resultado['ip_resolvido']}")
        print(f"  HTTPS: {resultado['url_segura']}")
```

## Criando uma Classe Wrapper Personalizada

### Exemplo 6: Wrapper Completo para String-X

```python
#!/usr/bin/env python3
"""
Exemplo: Wrapper personalizado para String-X como biblioteca.
"""
import json
import time
from datetime import datetime
from pathlib import Path

# Importações String-X
from stringx.utils.auxiliary.ext.email import AuxRegexEmail
from stringx.utils.auxiliary.ext.url import AuxRegexURL
from stringx.utils.auxiliary.ext.ip import AuxRegexIP
from stringx.utils.auxiliary.clc.dns import AuxDNSCollector
from stringx.utils.helper.functions import Funcs

class StringXLibrary:
    """
    Wrapper principal para usar String-X como biblioteca.
    """
    
    def __init__(self, config=None):
        """
        Inicializa a biblioteca String-X.
        
        Args:
            config (dict): Configurações personalizadas
        """
        self.config = config or {}
        self.funcs = Funcs()
        
        # Cache de resultados
        self.cache = {}
        
        # Estatísticas
        self.stats = {
            'operacoes_realizadas': 0,
            'emails_extraidos': 0,
            'urls_extraidas': 0,
            'ips_extraidos': 0,
            'inicio_sessao': datetime.now()
        }
    
    def extrair_dados(self, texto, tipos=['email', 'url', 'ip']):
        """
        Extrai múltiplos tipos de dados de um texto.
        
        Args:
            texto (str): Texto para processar
            tipos (list): Tipos de dados a extrair
            
        Returns:
            dict: Dados extraídos organizados por tipo
        """
        resultados = {}
        
        if 'email' in tipos:
            extrator = AuxRegexEmail()
            extrator.options['data'] = texto
            extrator.run()
            emails = extrator.get_result()
            resultados['emails'] = emails
            self.stats['emails_extraidos'] += len(emails)
        
        if 'url' in tipos:
            extrator = AuxRegexURL()
            extrator.options['data'] = texto
            extrator.run()
            urls = extrator.get_result()
            resultados['urls'] = urls
            self.stats['urls_extraidas'] += len(urls)
        
        if 'ip' in tipos:
            extrator = AuxRegexIP()
            extrator.options['data'] = texto
            extrator.run()
            ips = extrator.get_result()
            resultados['ips'] = ips
            self.stats['ips_extraidos'] += len(ips)
        
        self.stats['operacoes_realizadas'] += 1
        return resultados
    
    def processar_arquivo(self, caminho_arquivo, tipos=['email', 'url']):
        """
        Processa um arquivo completo.
        
        Args:
            caminho_arquivo (str): Caminho para o arquivo
            tipos (list): Tipos de dados a extrair
            
        Returns:
            dict: Resultados do processamento
        """
        arquivo = Path(caminho_arquivo)
        
        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        # Ler arquivo
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Extrair dados
        dados = self.extrair_dados(conteudo, tipos)
        
        # Adicionar metadados
        resultado = {
            'arquivo': str(arquivo),
            'tamanho_arquivo': arquivo.stat().st_size,
            'linhas': len(conteudo.splitlines()),
            'caracteres': len(conteudo),
            'dados_extraidos': dados,
            'timestamp': datetime.now().isoformat()
        }
        
        return resultado
    
    def pipeline_personalizado(self, dados, pipeline_config):
        """
        Executa pipeline personalizado de processamento.
        
        Args:
            dados (str|list): Dados para processar
            pipeline_config (dict): Configuração do pipeline
            
        Returns:
            dict: Resultados do pipeline
        """
        resultados = []
        
        # Normalizar dados para lista
        if isinstance(dados, str):
            dados = [dados]
        
        for item in dados:
            resultado_item = {'input': item}
            
            # Executar passos do pipeline
            for passo in pipeline_config.get('passos', []):
                tipo = passo.get('tipo')
                params = passo.get('parametros', {})
                
                if tipo == 'extrair':
                    dados_extraidos = self.extrair_dados(item, params.get('tipos', ['email']))
                    resultado_item['extraidos'] = dados_extraidos
                
                elif tipo == 'transformar':
                    funcao = params.get('funcao')
                    if hasattr(self.funcs, funcao):
                        resultado_funcao = getattr(self.funcs, funcao)(item)
                        resultado_item[funcao] = resultado_funcao
                
                elif tipo == 'validar':
                    validacoes = {}
                    for validacao in params.get('validacoes', []):
                        if validacao == 'email':
                            validacoes['tem_email'] = '@' in item
                        elif validacao == 'url':
                            validacoes['tem_url'] = item.startswith(('http://', 'https://'))
                    resultado_item['validacoes'] = validacoes
            
            resultados.append(resultado_item)
        
        return {
            'resultados': resultados,
            'total_processados': len(resultados),
            'pipeline_config': pipeline_config
        }
    
    def salvar_resultados(self, resultados, arquivo_saida, formato='json'):
        """
        Salva resultados em arquivo.
        
        Args:
            resultados (dict): Dados para salvar
            arquivo_saida (str): Caminho do arquivo de saída
            formato (str): Formato de saída (json, txt)
        """
        arquivo = Path(arquivo_saida)
        
        if formato == 'json':
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        elif formato == 'txt':
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(f"Relatório String-X - {datetime.now()}\n")
                f.write("=" * 50 + "\n\n")
                f.write(json.dumps(resultados, indent=2, ensure_ascii=False))
        
        print(f"Resultados salvos em: {arquivo}")
    
    def get_estatisticas(self):
        """
        Retorna estatísticas da sessão atual.
        
        Returns:
            dict: Estatísticas de uso
        """
        tempo_sessao = datetime.now() - self.stats['inicio_sessao']
        
        return {
            **self.stats,
            'tempo_sessao': str(tempo_sessao),
            'operacoes_por_minuto': round(
                self.stats['operacoes_realizadas'] / max(tempo_sessao.total_seconds() / 60, 1), 2
            )
        }

# Exemplo de uso completo
if __name__ == "__main__":
    # Inicializar biblioteca
    strx = StringXLibrary()
    
    # Exemplo 1: Extração simples
    print("=== Extração Simples ===")
    texto = """
    Entre em contato:
    Email: contato@empresa.com
    Site: https://empresa.com
    IP do servidor: 192.168.1.100
    """
    
    dados = strx.extrair_dados(texto)
    for tipo, itens in dados.items():
        print(f"{tipo.upper()}: {len(itens)} encontrado(s)")
        for item in itens:
            print(f"  - {item}")
    
    # Exemplo 2: Pipeline personalizado
    print("\n=== Pipeline Personalizado ===")
    config_pipeline = {
        'passos': [
            {
                'tipo': 'extrair',
                'parametros': {'tipos': ['email', 'url']}
            },
            {
                'tipo': 'transformar',
                'parametros': {'funcao': 'md5'}
            },
            {
                'tipo': 'validar',
                'parametros': {'validacoes': ['email', 'url']}
            }
        ]
    }
    
    dados_teste = [
        "admin@example.com",
        "https://github.com/projeto",
        "dados confidenciais"
    ]
    
    resultado_pipeline = strx.pipeline_personalizado(dados_teste, config_pipeline)
    
    for i, resultado in enumerate(resultado_pipeline['resultados'], 1):
        print(f"\nItem {i}: {resultado['input']}")
        if 'extraidos' in resultado:
            for tipo, valores in resultado['extraidos'].items():
                print(f"  {tipo}: {valores}")
        if 'md5' in resultado:
            print(f"  MD5: {resultado['md5']}")
        if 'validacoes' in resultado:
            print(f"  Validações: {resultado['validacoes']}")
    
    # Exemplo 3: Estatísticas
    print("\n=== Estatísticas ===")
    stats = strx.get_estatisticas()
    for chave, valor in stats.items():
        print(f"{chave}: {valor}")
    
    # Salvar resultados
    strx.salvar_resultados(resultado_pipeline, 'resultados_pipeline.json')
```

## Integração com Frameworks Web

### Exemplo 7: Integração com Flask

```python
#!/usr/bin/env python3
"""
Exemplo: API Flask usando String-X como biblioteca.
"""
from flask import Flask, request, jsonify
from stringx.utils.auxiliary.ext.email import AuxRegexEmail
from stringx.utils.auxiliary.ext.url import AuxRegexURL
from stringx.utils.helper.functions import Funcs

app = Flask(__name__)

class StringXAPI:
    """API String-X para Flask."""
    
    def __init__(self):
        self.funcs = Funcs()
    
    def extrair_dados(self, texto, tipos):
        """Extrai dados usando módulos String-X."""
        resultados = {}
        
        if 'email' in tipos:
            extrator = AuxRegexEmail()
            extrator.options['data'] = texto
            extrator.run()
            resultados['emails'] = extrator.get_result()
        
        if 'url' in tipos:
            extrator = AuxRegexURL()
            extrator.options['data'] = texto
            extrator.run()
            resultados['urls'] = extrator.get_result()
        
        return resultados

# Instância global
strx_api = StringXAPI()

@app.route('/extract', methods=['POST'])
def extrair_dados():
    """Endpoint para extração de dados."""
    dados = request.get_json()
    
    texto = dados.get('texto', '')
    tipos = dados.get('tipos', ['email', 'url'])
    
    if not texto:
        return jsonify({'erro': 'Texto é obrigatório'}), 400
    
    try:
        resultados = strx_api.extrair_dados(texto, tipos)
        return jsonify({
            'sucesso': True,
            'dados': resultados,
            'total': sum(len(v) for v in resultados.values())
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/hash/<algoritmo>', methods=['POST'])
def gerar_hash(algoritmo):
    """Endpoint para geração de hashes."""
    dados = request.get_json()
    valor = dados.get('valor', '')
    
    if not valor:
        return jsonify({'erro': 'Valor é obrigatório'}), 400
    
    # Mapear algoritmos para funções
    algoritmos = {
        'md5': strx_api.funcs.md5,
        'sha1': strx_api.funcs.sha1,
        'sha256': strx_api.funcs.sha256,
        'sha512': strx_api.funcs.sha512
    }
    
    if algoritmo not in algoritmos:
        return jsonify({'erro': 'Algoritmo não suportado'}), 400
    
    try:
        hash_resultado = algoritmos[algoritmo](valor)
        return jsonify({
            'algoritmo': algoritmo,
            'valor_original': valor,
            'hash': hash_resultado
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

**Uso da API**:
```bash
# Extrair dados
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"texto": "Email: teste@exemplo.com", "tipos": ["email"]}'

# Gerar hash
curl -X POST http://localhost:5000/hash/md5 \
  -H "Content-Type: application/json" \
  -d '{"valor": "senha123"}'
```

## Boas Práticas para Uso como Biblioteca

### 1. Gerenciamento de Recursos
```python
class StringXManager:
    def __enter__(self):
        # Inicialização de recursos
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Limpeza de recursos
        pass
```

### 2. Cache de Resultados
```python
import functools

@functools.lru_cache(maxsize=128)
def extrair_dados_cached(texto, tipos):
    # Implementação com cache
    pass
```

### 3. Logging Personalizado
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('stringx-lib')

def processar_com_log(dados):
    logger.info(f"Processando {len(dados)} itens")
    # Processamento...
    logger.info("Processamento concluído")
```

### 4. Tratamento de Erros
```python
try:
    resultados = processar_dados(entrada)
except Exception as e:
    logger.error(f"Erro no processamento: {e}")
    # Fallback ou re-raise
```

## Exemplos de Integração

### Django Integration
```python
# views.py
from django.http import JsonResponse
from .utils import StringXProcessor

def extract_data_view(request):
    processor = StringXProcessor()
    result = processor.extract(request.POST.get('text'))
    return JsonResponse(result)
```

### Celery Task
```python
from celery import Celery
from stringx_library import StringXLibrary

app = Celery('tasks')

@app.task
def process_large_dataset(data):
    strx = StringXLibrary()
    return strx.processar_arquivo(data)
```

### Jupyter Notebook
```python
# Em células Jupyter
%load_ext autoreload
%autoreload 2

from stringx_library import StringXLibrary
strx = StringXLibrary()

# Análise interativa
dados = strx.extrair_dados(texto_exemplo)
print(f"Encontrados {len(dados['emails'])} emails")
```

O String-X como biblioteca oferece flexibilidade total para integração em projetos Python, mantendo toda a funcionalidade dos módulos e funções while providing a programmatic interface for automation and integration scenarios.