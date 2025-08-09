"""
Módulo CLC para enumeração de subdomínios.

Este módulo implementa um coletor de subdomínios usando múltiplas técnicas
incluindo certificate transparency e bruteforce DNS.

A enumeração de subdomínios é uma técnica essencial para mapeamento de superfície
de ataque e reconhecimento digital, permitindo:
- Descobrir domínios e serviços ocultos ou não divulgados publicamente
- Identificar sistemas de desenvolvimento, teste ou staging
- Mapear a infraestrutura completa de uma organização
- Encontrar pontos de entrada potenciais para testes de segurança
- Descobrir aplicações e sistemas esquecidos que podem conter vulnerabilidades
- Compreender a estrutura organizacional através da nomenclatura de subdomínios

Este módulo utiliza múltiplas fontes e técnicas para maximizar a descoberta
de subdomínios, incluindo:
- Registros de Certificate Transparency (CT)
- Consultas a serviços públicos especializados
- Técnicas passivas que não geram tráfego direto para o alvo
- Consolidação e deduplicação de resultados de múltiplas fontes
"""
import asyncio

from stringx.core.basemodule import BaseModule
from stringx.core.http_async import HTTPClient
from stringx.core.retry import retry_operation

class SubdomainEnum(BaseModule):
    """
    Coletor de subdomínios usando múltiplas fontes.
    """
    
    def __init__(self):
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        self.meta = {
            'name': 'Subdomain Enumerator',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Enumera subdomínios usando CT logs e bruteforce',
            'type': 'collector'
        ,
            'example': './strx -l domains.txt -st "echo {STRING}" -module "clc:subdomain" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Domínio alvo
            'methods': ['crtsh', 'certspotter', 'hackertarget'],
            'timeout': 10,            'proxy': str(),  # Proxies para requisições (opcional)
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição    
        }
    
    def run(self):
        """
        Executa a enumeração de subdomínios.
        
        Utiliza múltiplas fontes para encontrar subdomínios do domínio especificado.
        """
        try:
            domain = self.options.get("data", "").strip()
            if not domain:
                self.log_debug("Domínio não fornecido.")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()
                
            subdomains = set()
            methods = self.options.get('methods', ['crtsh'])
            
            for method in methods:
                try:
                    if method == 'crtsh':
                        subs = self._crtsh_search(domain)
                    elif method == 'certspotter':
                        subs = self._certspotter_search(domain)
                    elif method == 'hackertarget':
                        subs = self._hackertarget_search(domain)
                    else:
                        continue
                        
                    subdomains.update(subs)
                except Exception:
                    continue
                
            if not subdomains:
                self.log_debug("Nenhum subdomínio encontrado")
                return
                            
            # Deduplicar e formatar resultados
            subdomains = sorted(list(set(subdomains)))
            self.log_debug(f"Subdomínios encontrados: {len(subdomains)}")            
            self.set_result("\n".join(subdomains))
        except Exception as e:
            self.handle_error(e, "Erro Subdomain")

    @retry_operation
    def _crtsh_search(self, domain: str) -> set:
        """Busca subdomínios no crt.sh"""
        url = f"https://crt.sh/?q=%25.{domain}&output=json"

        # Configurar parâmetros para HTTPClient
        kwargs = {
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
            },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,  
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
        
        try:
        # Executar requisição assíncrona
            async def make_request():
                return await self.request.send_request([url], **kwargs)
            
            response = asyncio.run(make_request())[0]
            
            subdomains = set()
            if response.status_code == 200:
                try:
                    data = response.json()
                    for entry in data:
                        name = entry.get('name_value', '')
                        if '\n' in name:
                            subdomains.update(name.split('\n'))
                        else:
                            subdomains.add(name)
                except:
                    pass
            
            return {sub.strip() for sub in subdomains if sub.strip() and domain in sub}
        
        except Exception as e:
            self.handle_error(e, "Erro ao conectar ao crt.sh")
            raise ValueError(e)
        
    @retry_operation
    def _certspotter_search(self, domain: str) -> set:
        """Busca subdomínios no CertSpotter"""
        url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"

        # Configurar parâmetros para HTTPClient
        kwargs = {
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
            },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,  
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }
        
        try:
            # Executar requisição assíncrona
            async def make_request():
                return await self.request.send_request([url], **kwargs)
            
            response = asyncio.run(make_request())[0]
            
            subdomains = set()
            if response.status_code == 200:
                try:
                    data = response.json()
                    for entry in data:
                        dns_names = entry.get('dns_names', [])
                        subdomains.update(dns_names)
                except:
                    pass
            
            return {sub for sub in subdomains if domain in sub}
        except Exception as e:
            self.log_debug(f"Erro ao conectar ao CertSpotter: {str(e)}")
            raise ValueError(e)
        
    @retry_operation
    def _hackertarget_search(self, domain: str) -> set:
        """Busca subdomínios no HackerTarget"""
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"

        # Configurar parâmetros para HTTPClient
        kwargs = {
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            },
            'proxy': self.options.get('proxy') if self.options.get('proxy') else None,
            'timeout': self.options.get('timeout', 30),
            'follow_redirects': True,
        }

        try:     
            # Executar requisição assíncrona
            async def make_request():
                return await self.request.send_request([url], **kwargs)
            
            response = asyncio.run(make_request())[0]
            
            subdomains = set()
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines:
                    if ',' in line:
                        subdomain = line.split(',')[0].strip()
                        subdomains.add(subdomain)
            
            return subdomains
        except Exception as e:
            self.log_debug(f"Erro ao conectar ao HackerTarget: {str(e)}")
            raise ValueError(e)
