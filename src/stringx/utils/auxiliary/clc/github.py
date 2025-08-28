"""
Módulo de coleta GitHub.

Este módulo implementa funcionalidade para buscar repositórios, usuários,
código e informações no GitHub via API, facilitando OSINT e reconnaissance.
"""
import json
import urllib.parse
import urllib.request
import base64

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class GitHubCollector(BaseModule):
    """
    Módulo de coleta GitHub.
    
    Esta classe permite buscar informações no GitHub incluindo:
    - Repositórios por palavra-chave
    - Usuários e organizações
    - Código fonte
    - Issues e commits
    """
    
    def __init__(self):
        """
        Inicializa o módulo de coleta GitHub.
        """
        super().__init__()
        
        self.meta = {
            'name': 'GitHub Collector',
             "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Busca repositórios, usuários e código no GitHub',
            'type': 'osint',
            'example': './strx -st "api_keys" -module "clc:github" -pm'
        }
        
        self.options = {
            'api_token': self.setting.STRX_GITHUB_TOKEN,
            'query': str(),
            'search_type': 'repositories',  # repositories, users, code, issues, commits
            'sort': 'updated',  # stars, forks, help-wanted-issues, updated
            'order': 'desc',    # asc, desc
            'per_page': 30,     # max 100
            'language': '',     # filtro por linguagem
            'user': '',         # filtro por usuário/organização
            'data': str(),
            'debug': False
        }
    
    def run(self):
        """
        Executa busca no GitHub.
        """
        try:
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            
            query = self.options.get('query', '').strip()
            if not query:
                query = Format.clear_value(self.options.get('data', ''))
            
            if not query:
                self.log_debug("[!] Nenhuma query fornecida para busca no GitHub")
                return
            
            search_type = self.options.get('search_type', 'repositories')
            api_token = self.options.get('api_token', '')
            
            self.log_debug(f"[*] Iniciando busca GitHub: '{query}' (tipo: {search_type})")
            
            # Construir URL da API
            base_url = "https://api.github.com/search"
            endpoint = f"{base_url}/{search_type}"
            
            # Preparar parâmetros
            params = {
                'q': self._build_query(query),
                'sort': self.options.get('sort', 'updated'),
                'order': self.options.get('order', 'desc'),
                'per_page': min(int(self.options.get('per_page', 30)), 100)
            }
            
            # Construir URL completa
            url = f"{endpoint}?{urllib.parse.urlencode(params)}"
            
            self.log_debug(f"[*] URL da busca: {url}")
            
            # Preparar requisição
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/vnd.github.v3+json')
            req.add_header('User-Agent', 'String-X/1.0')
            
            # Adicionar token se disponível
            if api_token:
                req.add_header('Authorization', f'token {api_token}')
                self.log_debug("[*] Usando autenticação via token")
            else:
                self.log_debug("[!] Sem token - limitado a 60 requests/hora")
            
            # Fazer requisição
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status != 200:
                    self.log_debug(f"[x] Erro na API GitHub: Status {response.status}")
                    return
                
                data = json.loads(response.read().decode('utf-8'))
                
                # Processar resultados
                self._process_results(data, search_type)
                
        except Exception as e:
            self.handle_error(e, "Erro ao buscar no GitHub")
    
    def _build_query(self, base_query):
        """
        Constrói query com filtros adicionais.
        """
        query_parts = [base_query]
        
        # Filtro por linguagem
        language = self.options.get('language', '').strip()
        if language:
            query_parts.append(f"language:{language}")
        
        # Filtro por usuário/organização
        user = self.options.get('user', '').strip()
        if user:
            query_parts.append(f"user:{user}")
        
        return ' '.join(query_parts)
    
    def _process_results(self, data, search_type):
        """
        Processa e formata os resultados da busca.
        """
        if 'items' not in data:
            self.log_debug("[!] Nenhum resultado encontrado")
            return
        
        items = data['items']
        total_count = data.get('total_count', 0)
        
        self.log_debug(f"[+] Encontrados {len(items)} resultados de {total_count} totais")
        
        results = []
        
        for item in items:
            if search_type == 'repositories':
                result = self._format_repository(item)
            elif search_type == 'users':
                result = self._format_user(item)
            elif search_type == 'code':
                result = self._format_code(item)
            elif search_type == 'issues':
                result = self._format_issue(item)
            elif search_type == 'commits':
                result = self._format_commit(item)
            else:
                result = str(item)
            
            results.append(result)
            self.log_debug(f"   [*] {result.split('\\n')[0]}")
        
        # Salvar resultados
        final_result = f"GitHub Search Results ({len(results)} items):\\n\\n"
        final_result += "\\n\\n".join(results)
        
        self.set_result(final_result)
    
    def _format_repository(self, repo):
        """
        Formata informações de repositório.
        """
        return f"""Repository: {repo['full_name']}
URL: {repo['html_url']}
Description: {repo.get('description', 'N/A')}
Language: {repo.get('language', 'N/A')}
Stars: {repo['stargazers_count']}
Forks: {repo['forks_count']}
Updated: {repo['updated_at']}"""
    
    def _format_user(self, user):
        """
        Formata informações de usuário.
        """
        return f"""User: {user['login']}
URL: {user['html_url']}
Type: {user['type']}
Profile: {user.get('avatar_url', 'N/A')}"""
    
    def _format_code(self, code):
        """
        Formata informações de código.
        """
        return f"""File: {code['name']}
Repository: {code['repository']['full_name']}
URL: {code['html_url']}
Path: {code['path']}"""
    
    def _format_issue(self, issue):
        """
        Formata informações de issue.
        """
        return f"""Issue: {issue['title']}
Repository: {issue.get('repository_url', '').split('/')[-2:]}
URL: {issue['html_url']}
State: {issue['state']}
Created: {issue['created_at']}"""
    
    def _format_commit(self, commit):
        """
        Formata informações de commit.
        """
        return f"""Commit: {commit['sha'][:8]}
Repository: {commit['repository']['full_name']}
Message: {commit['commit']['message'][:100]}...
Author: {commit['commit']['author']['name']}
Date: {commit['commit']['author']['date']}"""
