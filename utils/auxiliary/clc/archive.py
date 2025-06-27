"""
Módulo CLC para coleta de URLs arquivadas no Wayback Machine (archive.org).

Este módulo implementa um coletor de URLs arquivadas utilizando o serviço
Wayback Machine do Internet Archive (archive.org), permitindo recuperar 
histórico de URLs associadas a um domínio específico.
"""
from core.basemodule import BaseModule
from core.user_agent_generator import UserAgentGenerator
import httpx
import urllib.parse
import re
import backoff
from requests.exceptions import RequestException
import warnings

# Suprimir avisos relacionados a verificação de certificados
warnings.filterwarnings("ignore", category=Warning)

class archive(BaseModule):
    """
    Coletor de URLs arquivadas usando o Wayback Machine (archive.org).
    
    Esta classe permite coletar URLs que foram arquivadas pelo Internet Archive
    para um domínio específico, facilitando a descoberta de conteúdo histórico
    e mapeamento de sites.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de coleta do Wayback Machine.
        """
        # Chama o inicializador da classe pai para configurar estruturas básicas
        super().__init__()
        
        # Metadados do módulo
        self.meta = {
            'name': 'Wayback Machine URL Collector',
            "author": "OSINT Brazuca",
            'version': '1.0',
            'description': 'Coleta URLs arquivadas de um domínio usando o Wayback Machine (archive.org)',
            'type': 'collector'
        }
        
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),           # Domínio alvo
            'timeout': 30,           # Timeout para requisições
            'proxy': str(),          # Proxies para requisições
            'debug': False,          # Modo de debug para mostrar informações detalhadas
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:archive" -pm',
        }
    
    def log_debug(self, message):
        """
        Registra uma mensagem de debug se o modo de debug estiver ativado.
        
        Args:
            message (str): Mensagem de log
        """
        if self.options.get('debug'):
            print(f"[ARCHIVE-DEBUG] {message}")

    def run(self):
        """
        Executa a coleta de URLs arquivadas do Wayback Machine.
        
        Returns:
            Resultados da busca de URLs arquivadas para o domínio alvo.
        """
        # Obtém o domínio alvo da entrada
        domain = self.options.get('data')
        if not domain:
            self.log_debug("Nenhum domínio fornecido")
            return
        
        self.log_debug(f"Domínio alvo: {domain}")
        
        # Realiza consulta ao Wayback Machine
        try:
            self.log_debug("Iniciando consulta ao Wayback Machine")
            archived_urls = self._query_archive(domain)
            
            self.log_debug(f"Resultados obtidos: {len(archived_urls) if archived_urls else 0}")
            
            if not archived_urls:
                # Nenhum resultado encontrado
                self.log_debug("Nenhuma URL arquivada encontrada")
                self.set_result("")
                return
            
            # Converte para string com uma entrada por linha para compatibilidade com StringX
            self.set_result("\n".join(archived_urls))
                
        except Exception as e:
            error_msg = f"Erro na coleta de dados do Wayback Machine: {str(e)}"
            self.log_error(error_msg)
            self.log_debug(f"Exceção: {type(e).__name__}: {str(e)}")
            import traceback
            self.log_debug(traceback.format_exc())
            self.set_result("")
            return
    
    def log_error(self, message):
        """
        Registra uma mensagem de erro.
        
        Args:
            message (str): Mensagem de erro
        """
        print(f"[ARCHIVE-ERROR] {message}")

    @backoff.on_exception(
        backoff.expo,
        (httpx.HTTPError, httpx.TimeoutException, RequestException),
        max_tries=3,
        max_time=30
    )
    def _query_archive(self, domain: str) -> list:
        """
        Realiza consulta ao Wayback Machine e retorna as URLs arquivadas.
        
        Args:
            domain (str): Domínio para pesquisa
            
        Returns:
            list: Lista de URLs arquivadas para o domínio
        """
        # Sanitiza o domínio de entrada (remove espaços e caracteres não imprimíveis)
        domain = re.sub(r'[^\x20-\x7E]', '', domain).strip()
        url = f'http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey'

        
        # Prepara headers para requisição
        headers = {
            'User-Agent': UserAgentGenerator.get_random_user_agent(),
            'Accept': 'text/plain',
        }
        
        # Configurar parâmetros do cliente httpx
        client_kwargs = {
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None
        }
        
        self.log_debug(f"URL de consulta: {url}")
        
        try:
            # Realiza a requisição
            with httpx.Client(verify=False, **client_kwargs) as client:
                response = client.get(url, headers=headers)
            
            self.log_debug(f"Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                # Processa os resultados
                urls = response.text.strip().split('\n')
                # Remove linhas vazias
                urls = [url for url in urls if url.strip()]
                return urls
            else:
                self.log_debug(f"Resposta HTTP não-200: {response.status_code}")
                self.log_debug(f"Conteúdo da resposta: {response.text[:200]}...")
                return []
                
        except Exception as e:
            self.log_debug(f"Erro na requisição: {type(e).__name__}: {str(e)}")
            return []
