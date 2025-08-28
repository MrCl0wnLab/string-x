"""
Módulo CLC para coleta de URLs arquivadas no Wayback Machine (archive.org).

Este módulo implementa um coletor de URLs arquivadas utilizando o serviço
Wayback Machine do Internet Archive (archive.org), permitindo recuperar 
histórico de URLs associadas a um domínio específico.

O Internet Archive mantém snapshots históricos de páginas web, o que é útil para:
- Análise histórica de conteúdos que não estão mais disponíveis online
- Mapeamento de mudanças em sites ao longo do tempo
- Recuperação de informações de versões anteriores de páginas
- Descoberta de subdomínios e paths que podem não estar mais ativos
"""
import re
import asyncio
import warnings
import traceback
from requests.exceptions import RequestException
from httpx import ConnectError, ReadTimeout, ConnectTimeout, TimeoutException

from stringx.core.http_async import HTTPClient
from stringx.core.basemodule import BaseModule
from stringx.core.retry import retry_operation
from stringx.core.user_agent_generator import UserAgentGenerator

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
        # Instância do cliente HTTP assíncrono
        self.request  = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'Wayback Machine URL Collector',
            "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Coleta URLs arquivadas de um domínio usando o Wayback Machine (archive.org)',
            'type': 'collector',
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:archive" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),           # Domínio alvo
            'timeout': self.setting.STRX_REQUEST_TIMEOUT,           # Timeout para requisições
            'proxy': str(),          # Proxies para requisições
            'debug': False,          # Modo de debug para mostrar informações detalhadas            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }


   
    


    def run(self):
        """
        Executa a coleta de URLs arquivadas do Wayback Machine.
        
        Returns:
            Resultados da busca de URLs arquivadas para o domínio alvo.
        """
        # Obtém o domínio alvo da entrada
        domain = self.options.get('data')
        if not domain:
            self.log_debug("[X] Nenhum domínio fornecido")
            return
        
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()

        self.log_debug(f"[*] Domínio alvo: {domain}")
        
        # Realiza consulta ao Wayback Machine
        try:
            self.log_debug("[*] Iniciando consulta ao Wayback Machine")
            archived_urls = self._query_archive(domain)
            
            self.log_debug(f"[+] Resultados obtidos: {len(archived_urls) if archived_urls else 0}")
            
            if not archived_urls:
                # Nenhum resultado encontrado
                self.log_debug("[!] Nenhuma URL arquivada encontrada")
                self.set_result("")
                return
            
            # Converte para string com uma entrada por linha para compatibilidade com StringX
            self.set_result("\n".join(archived_urls))
                
        except Exception as e:
            self.handle_error(e, "Erro na coleta de dados do Wayback Machine")
            self.set_result("")
            return
    

    def _query_archive(self, domain: str) -> list:
        """
        Wrapper síncrono para realizar consulta ao Wayback Machine e retornar as URLs arquivadas.
        
        Args:
            domain (str): Domínio para pesquisa
            
        Returns:
            list: Lista de URLs arquivadas para o domínio
        """
        return asyncio.run(self._query_archive_async(domain))
    
    
    @retry_operation
    async def _query_archive_async(self, domain: str) -> list:
        """
        Versão assíncrona para realizar consulta ao Wayback Machine e retornar as URLs arquivadas.
        
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
        
        # Configurar parâmetros para o HTTPClient
        kwargs = {
            'headers': headers,
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
        
        self.log_debug(f"[*] URL de consulta: {url}")
        
        try:
            # Realiza a requisição assíncrona
            response = await self.request.send_request([url], **kwargs)
            
            if not response or isinstance(response[0], Exception):
                self.log_debug(f"[X] Erro na requisição: {str(response[0]) if response else 'Sem resposta'}")
                return []
                
            response = response[0]
            
            self.log_debug(f"[*] Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                # Processa os resultados
                urls = response.text.strip().split('\n')
                # Remove linhas vazias
                urls = [url for url in urls if url.strip()]
                return urls
            else:
                self.log_debug(f"[X] Resposta HTTP não-200: {response.status_code}")
                self.log_debug(f"[*] Conteúdo da resposta: {response.text[:200]}...")
                return []
                
        except Exception as e:
            self.handle_error(e, "Erro na requisição ao Wayback Machine")
            raise ValueError(e)
            
