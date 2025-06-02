"""
Módulo CON para conexões FTP.

Este módulo implementa funcionalidade para estabelecer conexões FTP
e listar diretórios ou baixar arquivos.
"""
from core.basemodule import BaseModule
import ftplib
import socket

class FTPConnector(BaseModule):
    """
    Módulo para conexões FTP.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'FTP Connector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Estabelece conexões FTP e lista diretórios',
            'type': 'connection'
        }
        
        self.options = {
            'data': str(),  # host:port ou apenas host
            'username': 'anonymous',
            'password': 'anonymous@example.com',
            'timeout': 10,
            'passive': True,
            'list_files': True,
            'example': './strx -l ftp_servers.txt -st "echo {STRING}" -module "con:ftp" -pm'
        }
    
    def run(self):
        """
        Executa a conexão FTP e operações especificadas.
        
        Tenta estabelecer conexão FTP com o host especificado usando
        credenciais fornecidas e lista arquivos/diretórios.
        """
        target = self.options.get("data", "").strip()
        if not target:
            return
            
        # Parse host:port
        if ':' in target:
            host, port = target.split(':', 1)
            port = int(port)
        else:
            host, port = target, 21
        
        username = self.options.get('username', 'anonymous')
        password = self.options.get('password', 'anonymous@example.com')
        timeout = self.options.get('timeout', 10)
        passive = self.options.get('passive', True)
        
        try:
            # Estabelecer conexão FTP
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout)
            
            # Configurar modo passivo
            if passive:
                ftp.set_pasv(True)
            
            # Fazer login
            ftp.login(username, password)
            
            # Obter informações do servidor
            result = f"FTP Success - {host}:{port}\n"
            result += f"Welcome: {ftp.getwelcome()}\n"
            
            # Listar arquivos se solicitado
            if self.options.get('list_files', True):
                try:
                    files = []
                    ftp.retrlines('LIST', files.append)
                    if files:
                        result += f"Directory listing:\n"
                        for file_line in files[:10]:  # Limitar a 10 linhas
                            result += f"  {file_line}\n"
                        if len(files) > 10:
                            result += f"  ... and {len(files) - 10} more files\n"
                except Exception as e:
                    result += f"Could not list files: {str(e)}\n"
            
            # Obter diretório atual
            try:
                pwd = ftp.pwd()
                result += f"Current directory: {pwd}\n"
            except:
                pass
            
            ftp.quit()
            self.set_result(result)
            
        except ftplib.error_perm as e:
            self.set_result(f"FTP Permission Error - {host}:{port}: {str(e)}")
        except socket.error as e:
            self.set_result(f"FTP Connection Error - {host}:{port}: {str(e)}")
        except Exception as e:
            self.set_result(f"FTP Error - {host}:{port}: {str(e)}")
