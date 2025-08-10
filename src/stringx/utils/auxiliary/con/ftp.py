"""
Módulo CON para conexões FTP.

Este módulo implementa funcionalidade para estabelecer conexões FTP
e listar diretórios ou baixar arquivos.

O FTP (File Transfer Protocol) é um protocolo para transferência de arquivos,
que permite:
- Acesso a servidores de arquivos remotos
- Navegação em estruturas de diretórios
- Upload e download de arquivos
- Verificação de sistemas para análise de segurança
- Identificação de servidores FTP com acesso anônimo
- Enumeração de arquivos e diretórios potencialmente sensíveis
"""
# Bibliotecas padrão
import ftplib
import socket
from typing import List, Dict, Any, Optional, Union

# Módulos locais
from stringx.core.basemodule import BaseModule

class FTPConnector(BaseModule):
    """
    Módulo para conexões FTP.
    
    Esta classe implementa funcionalidades para estabelecer conexões FTP
    com servidores remotos e realizar operações como listagem de diretórios
    e verificação de acesso.
    """
    
    def __init__(self) -> None:
        """
        Inicializa o módulo conector FTP.
        """
        super().__init__()
        
        self.meta = {
            'name': 'FTP Connector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Estabelece conexões FTP e lista diretórios',
            'type': 'connection',
            'example': './strx -l ftp_servers.txt -st "echo {STRING}" -module "con:ftp" -pm'
        }
        
        self.options = {
            'data': str(),            # host:port ou apenas host
            'username': self.setting.STRX_FTP_USERNAME,   # Nome de usuário para autenticação
            'password': self.setting.STRX_FTP_PASS,  # Senha para autenticação
            'timeout': self.setting.STRX_FTP_TIMEOUT,            # Timeout para conexão e operações
            'passive': True,          # Usar modo passivo
            'list_files': True,       # Listar arquivos no diretório atual            'debug': False,           # Modo de debug para mostrar informações detalhadas
            'retry': 0,               # Número de tentativas de requisição
            'retry_delay': None,         # Atraso entre tentativas de requisição
        }
    

    
    def run(self) -> None:
        """
        Executa a conexão FTP e operações especificadas.
        
        Esta função tenta estabelecer conexão FTP com o host especificado usando
        credenciais fornecidas e lista arquivos/diretórios.
        
        Returns:
            None: Os resultados são armazenados através do método set_result
            
        Raises:
            ValueError: Se os parâmetros de conexão forem inválidos
            ftplib.error_perm: Se ocorrer erro de permissão (credenciais inválidas)
            socket.error: Se ocorrer erro de conexão
            TimeoutError: Se a conexão exceder o tempo limite
        """
        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        target = self.options.get("data", "").strip()
        if not target:
            self.log_debug("[!] Nenhum host alvo especificado")
            return
            
        # Parse host:port
        if ':' in target:
            host, port = target.split(':', 1)
            try:
                port = int(port)
            except ValueError:
                self.log_debug(f"[!] Porta inválida: {port}, usando porta padrão 21")
                port = 21
        else:
            host, port = target, self.setting.STRX_FTP_PORT
        
        username = self.options.get('username', 'anonymous')
        password = self.options.get('password', 'anonymous@example.com')
        timeout = self.options.get('timeout', 10)
        passive = self.options.get('passive', True)
        
        self.log_debug(f"[*] Conectando a {host}:{port} como {username}")
        
        try:
            # Estabelecer conexão FTP
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout)
            
            # Configurar modo passivo
            if passive:
                self.log_debug("[*] Usando modo passivo")
                ftp.set_pasv(True)
            
            # Fazer login
            self.log_debug(f"[*] Tentando login com usuário: {username}")
            ftp.login(username, password)
            self.log_debug("[+] Login bem-sucedido")
            
            # Obter informações do servidor
            welcome = ftp.getwelcome()
            self.log_debug(f"[*] Mensagem de boas-vindas: {welcome}")
            
            result = f"FTP Success - {host}:{port}\n"
            result += f"Welcome: {welcome}\n"
            
            # Listar arquivos se solicitado
            if self.options.get('list_files', True):
                self.log_debug("[*] Listando arquivos no diretório atual")
                try:
                    files = []
                    ftp.retrlines('LIST', files.append)
                    
                    if files:
                        self.log_debug(f"[+] Encontrados {len(files)} arquivos/diretórios")
                        result += f"Directory listing:\n"
                        for file_line in files[:10]:  # Limitar a 10 linhas
                            result += f"  {file_line}\n"
                        if len(files) > 10:
                            result += f"  ... and {len(files) - 10} more files\n"
                    else:
                        self.log_debug("[!] Diretório vazio")
                        result += "Directory is empty\n"
                except ftplib.error_perm as e:
                    self.handle_error(e, f"Erro de permissão ao listar arquivos")
                    result += f"Could not list files: Permission denied\n"
                except Exception as e:
                    self.handle_error(e, "Erro ao listar arquivos FTP")
                    result += f"Could not list files: {str(e)}\n"
            
            # Obter diretório atual
            try:
                pwd = ftp.pwd()
                self.log_debug(f"[*] Diretório atual: {pwd}")
                result += f"Current directory: {pwd}\n"
            except ftplib.error_perm:
                self.log_debug("[x] Não foi possível obter o diretório atual")
                pass
            
            # Encerrar conexão corretamente
            self.log_debug("[*] Encerrando conexão")
            ftp.quit()
            self.set_result(result)
            
        except ftplib.error_perm as e:
            self.handle_error(e, f"Erro de permissão FTP - {host}:{port}")
        except socket.timeout as e:
            self.handle_error(e, f"FTP Timeout - {host}:{port}: operação excedeu {timeout} segundos")
        except socket.error as e:
            self.handle_error(e, f"Erro de conexão FTP - {host}:{port}")
        except ValueError as e:
            self.handle_error(e, f"Erro de parâmetro FTP - {host}:{port}")
        except Exception as e:
            self.handle_error(e, "Erro inesperado na conexão FTP")
