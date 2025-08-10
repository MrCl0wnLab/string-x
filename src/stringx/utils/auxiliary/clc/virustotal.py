"""
Módulo collector para VirusTotal API.

Este módulo implementa funcionalidade para consultar a API do VirusTotal
e obter informações sobre análise de arquivos, URLs, domínios e IPs,
incluindo detecções de malware e reputação.

O VirusTotal é um serviço que agrega múltiplos mecanismos de antivírus e
ferramentas de análise, oferecendo informações críticas para segurança:
- Análise de arquivos por dezenas de mecanismos antivírus diferentes
- Verificação da reputação de URLs, domínios e endereços IP
- Detecção de phishing, malware e outros conteúdos maliciosos
- Inteligência de ameaças baseada em dados históricos e atuais
- Informações detalhadas sobre comportamentos suspeitos
- Relacionamentos entre amostras de malware, domínios e infraestrutura

Este módulo permite integrar os recursos do VirusTotal ao fluxo de trabalho
do String-X, auxiliando na identificação de recursos maliciosos e avaliação
de risco durante investigações OSINT.
"""
import re
import json
import asyncio

from stringx.core.basemodule import BaseModule
from stringx.core.http_async import HTTPClient

class VirusTotalCollector(BaseModule):
    """
    Módulo coletor para API do VirusTotal.
    
    Esta classe permite consultar a API do VirusTotal para análise de
    arquivos, URLs, domínios e endereços IP, obtendo informações sobre
    detecções de malware e reputação de segurança.
    """
    
    def __init__(self):
        """
        Inicializa o módulo coletor VirusTotal.
        """
        super().__init__()
        # Instância do cliente HTTP assíncrono
        self.request = HTTPClient()
        # Metadados do módulo
        self.meta = {
            'name': 'VirusTotal Collector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Coleta informações via API VirusTotal',
            'type': 'collector'
        ,
            'example': './strx -l suspicious_files.txt -st "echo {STRING}" -module "clc:virustotal" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # URL, IP, domain ou hash
            'api_key': self.setting.STRX_VIRUSTOTAL_APIKEY,  # API key do VirusTotal
            'resource_type': 'auto',  # auto, url, ip, domain, file
            'include_details': True,
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa consulta na API do VirusTotal.
        """
        try:
           
            
            data = self.options.get('data', '').strip()
            api_key = self.options.get('api_key', '')
            resource_type = self.options.get('resource_type', 'auto')
            
            if not data:
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            if not api_key:
                self.log_debug("[x] Erro: API key do VirusTotal é obrigatória")
                return
            
            # Detectar tipo automaticamente se necessário
            if resource_type == 'auto':
                resource_type = self._detect_resource_type(data)
            
            # Executar consulta baseada no tipo
            if resource_type == 'url':
                result = self._query_url(data, api_key)
            elif resource_type == 'ip':
                result = self._query_ip(data, api_key)
            elif resource_type == 'domain':
                result = self._query_domain(data, api_key)
            elif resource_type == 'file':
                result = self._query_file(data, api_key)
            else:
                self.log_debug(f"[x] Erro: Tipo de recurso não suportado: {resource_type}")
                return
            
            if result:
                self.set_result(result)
                
        except Exception as e:
            self.handle_error(e, "Erro VirusTotal")
    
    def _detect_resource_type(self, data: str) -> str:
        """Detecta automaticamente o tipo de recurso."""
        # Hash (MD5, SHA1, SHA256)
        if re.match(r'^[a-fA-F0-9]{32}$', data):
            return 'file'  # MD5
        elif re.match(r'^[a-fA-F0-9]{40}$', data):
            return 'file'  # SHA1
        elif re.match(r'^[a-fA-F0-9]{64}$', data):
            return 'file'  # SHA256
        
        # URL
        elif data.startswith(('http://', 'https://')):
            return 'url'
        
        # IP
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', data):
            return 'ip'
        
        # Domain
        elif '.' in data and not '/' in data:
            return 'domain'
        
        return 'unknown'
    
    async def _query_url_async(self, url: str, api_key: str) -> str:
        """Consulta análise de URL."""
        try:
            import base64
            
            # Codificar URL em base64 sem padding
            url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip('=')
            
            api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
            
            kwargs = {
                'headers': {
                    'x-apikey': api_key,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': 15,
            }
            
            response = await self.request.send_request([api_url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                attributes = data.get('data', {}).get('attributes', {})
                stats = attributes.get('last_analysis_stats', {})
                
                result = f"🔗 URL: {url}\n"
                result += f"🛡️ Análise:\n"
                result += f"  • Maliciosos: {stats.get('malicious', 0)}\n"
                result += f"  • Suspeitos: {stats.get('suspicious', 0)}\n"
                result += f"  • Limpos: {stats.get('harmless', 0)}\n"
                result += f"  • Não detectados: {stats.get('undetected', 0)}\n"
                
                # Categorias
                categories = attributes.get('categories', {})
                if categories:
                    cats = list(categories.values())[:3]
                    result += f"Categorias: {', '.join(cats)}\n"
                
                # Redirect chain
                redirects = attributes.get('redirection_chain', [])
                if redirects and len(redirects) > 1:
                    result += f"Redirecionamentos: {len(redirects)}\n"
                
                return result
            elif response.status_code == 404:
                return f"URL {url}: Não analisada ainda"
            else:
                return f"Erro HTTP {response.status_code}"
                
        except Exception as e:
            return self.handle_error(e, "Erro na consulta de URL VirusTotal")
            
    def _query_url(self, url: str, api_key: str) -> str:
        """Consulta análise de URL (wrapper para método assíncrono)."""
        return asyncio.run(self._query_url_async(url, api_key))
    
    async def _query_ip_async(self, ip: str, api_key: str) -> str:
        """Consulta análise de IP."""
        try:
            api_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
            
            kwargs = {
                'headers': {
                    'x-apikey': api_key,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': 15,
            }
            
            response = await self.request.send_request([api_url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                attributes = data.get('data', {}).get('attributes', {})
                stats = attributes.get('last_analysis_stats', {})
                
                result = f"🌐 IP: {ip}\n"
                result += f"🛡️ Análise:\n"
                result += f"  • Maliciosos: {stats.get('malicious', 0)}\n"
                result += f"  • Suspeitos: {stats.get('suspicious', 0)}\n"
                result += f"  • Limpos: {stats.get('harmless', 0)}\n"
                result += f"  • Não detectados: {stats.get('undetected', 0)}\n"
                
                # Geolocalização
                country = attributes.get('country', 'N/A')
                asn = attributes.get('asn', 'N/A')
                as_owner = attributes.get('as_owner', 'N/A')
                
                result += f"🌍 País: {country}\n"
                result += f"🏢 ASN: {asn} ({as_owner})\n"
                
                return result
            elif response.status_code == 404:
                return f"IP {ip}: Nenhuma informação disponível"
            else:
                return f"Erro HTTP {response.status_code}"
                
        except Exception as e:
            return self.handle_error(e, "Erro na consulta de IP VirusTotal")
            
    def _query_ip(self, ip: str, api_key: str) -> str:
        """Consulta análise de IP (wrapper para método assíncrono)."""
        return asyncio.run(self._query_ip_async(ip, api_key))
    
    async def _query_domain_async(self, domain: str, api_key: str) -> str:
        """Consulta análise de domínio."""
        try:
            api_url = f"https://www.virustotal.com/api/v3/domains/{domain}"
            
            kwargs = {
                'headers': {
                    'x-apikey': api_key,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': 15,
            }
            
            response = await self.request.send_request([api_url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                attributes = data.get('data', {}).get('attributes', {})
                stats = attributes.get('last_analysis_stats', {})
                
                result = f"🌐 Domínio: {domain}\n"
                result += f"🛡️ Análise:\n"
                result += f"  • Maliciosos: {stats.get('malicious', 0)}\n"
                result += f"  • Suspeitos: {stats.get('suspicious', 0)}\n"
                result += f"  • Limpos: {stats.get('harmless', 0)}\n"
                result += f"  • Não detectados: {stats.get('undetected', 0)}\n"
                
                # Informações de DNS
                records = attributes.get('last_dns_records', [])
                if records:
                    a_records = [r['value'] for r in records if r['type'] == 'A'][:3]
                    if a_records:
                        result += f"📍 IPs: {', '.join(a_records)}\n"
                
                # Categorias
                categories = attributes.get('categories', {})
                if categories:
                    cats = list(categories.values())[:3]
                    result += f"Categorias: {', '.join(cats)}\n"
                
                # Whois
                whois_date = attributes.get('whois_date')
                if whois_date:
                    import datetime
                    date_obj = datetime.datetime.fromtimestamp(whois_date)
                    result += f"📅 Whois: {date_obj.strftime('%Y-%m-%d')}\n"
                
                return result
            elif response.status_code == 404:
                return f"Domínio {domain}: Nenhuma informação disponível"
            else:
                return f"Erro HTTP {response.status_code}"
                
        except Exception as e:
            return self.handle_error(e, "Erro na consulta de domínio VirusTotal")
            
    def _query_domain(self, domain: str, api_key: str) -> str:
        """Consulta análise de domínio (wrapper para método assíncrono)."""
        return asyncio.run(self._query_domain_async(domain, api_key))
    
    async def _query_file_async(self, file_hash: str, api_key: str) -> str:
        """Consulta análise de arquivo por hash."""
        try:
            api_url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            
            kwargs = {
                'headers': {
                    'x-apikey': api_key,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                },
                'timeout': 15,
            }
            
            response = await self.request.send_request([api_url], **kwargs)
            response = response[0]
            
            if response.status_code == 200:
                data = json.loads(response.text)
                
                attributes = data.get('data', {}).get('attributes', {})
                stats = attributes.get('last_analysis_stats', {})
                
                result = f"📁 Hash: {file_hash}\n"
                result += f"🛡️ Análise:\n"
                result += f"  • Maliciosos: {stats.get('malicious', 0)}\n"
                result += f"  • Suspeitos: {stats.get('suspicious', 0)}\n"
                result += f"  • Limpos: {stats.get('harmless', 0)}\n"
                result += f"  • Não detectados: {stats.get('undetected', 0)}\n"
                
                # Informações do arquivo
                file_type = attributes.get('type_description', 'N/A')
                size = attributes.get('size', 0)
                names = attributes.get('names', [])
                
                result += f"📄 Tipo: {file_type}\n"
                result += f"💾 Tamanho: {size} bytes\n"
                if names:
                    result += f"📛 Nome: {names[0]}\n"
                
                # Top detecções
                engines = attributes.get('last_analysis_results', {})
                detections = []
                for engine, result_data in engines.items():
                    if result_data.get('category') == 'malicious':
                        malware_name = result_data.get('result', 'Malware')
                        detections.append(f"{engine}: {malware_name}")
                
                if detections:
                    result += f"Detecções: {'; '.join(detections[:3])}\n"
                
                return result
            elif response.status_code == 404:
                return f"Hash {file_hash}: Arquivo não encontrado"
            else:
                return f"Erro HTTP {response.status_code}"
                
        except Exception as e:
            return self.handle_error(e, "Erro na consulta de arquivo VirusTotal")
            
    def _query_file(self, file_hash: str, api_key: str) -> str:
        """Consulta análise de arquivo por hash (wrapper para método assíncrono)."""
        return asyncio.run(self._query_file_async(file_hash, api_key))