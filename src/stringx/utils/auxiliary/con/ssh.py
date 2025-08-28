"""
Módulo CON para conexões SSH.

Este módulo implementa funcionalidade para estabelecer conexões SSH
e executar comandos remotos em servidores.

O SSH (Secure Shell) é um protocolo criptográfico para operações de rede seguras,
permitindo:
- Execução remota de comandos em servidores
- Transferência segura de dados
- Gerenciamento remoto de sistemas
- Tunelamento de conexões
- Autenticação por senha ou chave privada
"""
# Bibliotecas padrão
import os
import subprocess
from typing import Optional, Dict, Any, List, Tuple

# Módulos locais
from stringx.core.basemodule import BaseModule

class SSHConnector(BaseModule):
    """
    Módulo para conexões SSH.
    
    Esta classe implementa funcionalidades para estabelecer conexões SSH
    com servidores remotos e executar comandos, utilizando autenticação
    por senha ou chave privada.
    """
    
    def __init__(self) -> None:
        """
        Inicializa o módulo conector SSH.
        """
        super().__init__()
        
        self.meta = {
            'name': 'SSH Connector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Estabelece conexões SSH e executa comandos',
            'type': 'connection',
            'example': './strx -l servers.txt -st "echo {STRING}" -module "con:ssh" -pm'
        }
        
        self.options = {
            'data': str(),       # host:port ou apenas host
            'username': self.setting.STRX_SSH_USER,  # Nome de usuário para autenticação
            'password': self.setting.STRX_SSH_PASS,   # Senha para autenticação
            'key_file': str(),   # Arquivo de chave privada para autenticação
            'command': self.setting.STRX_SSH_CMD, # Comando a ser executado
            'timeout': self.setting.STRX_SSH_TIMEOUT,       # Timeout para conexão e execução            'debug': False,      # Modo de debug para mostrar informações detalhadas  
            'retry': 0,          # Número de tentativas de conexão
            'retry_delay': None,    # Atraso entre tentativas de conexão
        }
    

    
    def run(self) -> None:
        """
        Executa a conexão SSH e comando especificado.
        
        Esta função tenta estabelecer conexão SSH com o host especificado usando
        credenciais fornecidas e executa o comando configurado.
        
        Returns:
            None: Os resultados são armazenados através do método set_result
            
        Raises:
            ValueError: Se os parâmetros de conexão forem inválidos
            TimeoutError: Se a conexão ou execução exceder o tempo limite
            subprocess.SubprocessError: Se ocorrer erro na execução do comando
            FileNotFoundError: Se o arquivo de chave privada não for encontrado
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
        target = self.options.get("data", "").strip()
        if not target:
            self.log_debug("[X] Nenhum host alvo especificado")
            return
            
        # Parse host:port
        if ':' in target:
            host, port = target.split(':', 1)
        else:
            host, port = target, self.setting.STRX_SSH_PORT
        
        username = self.options.get('username', 'root')
        password = self.options.get('password', '')
        key_file = self.options.get('key_file', '')
        command = self.options.get('command', 'whoami')
        timeout = self.options.get('timeout', 10)
        
        self.log_debug(f"[*] Conectando a {host}:{port} como {username}")
        
        try:
            # Validar arquivo de chave se especificado
            if key_file and not os.path.exists(key_file):
                raise FileNotFoundError(f"Arquivo de chave não encontrado: {key_file}")
            
            # Construir comando SSH
            ssh_cmd = ['ssh', '-o', 'ConnectTimeout=5', 
                      '-o', 'StrictHostKeyChecking=no',
                      '-p', str(port)]
            
            if key_file and os.path.exists(key_file):
                ssh_cmd.extend(['-i', key_file])
                self.log_debug(f"[*] Usando autenticação por chave: {key_file}")
            elif password:
                self.log_debug("[*] Usando autenticação por senha")
            else:
                self.log_debug("[!] Nenhum método de autenticação especificado")
            
            ssh_cmd.append(f"{username}@{host}")
            ssh_cmd.append(command)
            
            self.log_debug(f"[*] Executando comando: {command}")
            
            # Executar SSH
            if password:
                # Usar sshpass se disponível
                full_cmd = ['sshpass', '-p', password] + ssh_cmd
            else:
                full_cmd = ssh_cmd
            
            result = subprocess.run(full_cmd, capture_output=True, 
                                  text=True, timeout=timeout)
            
            if result.returncode == 0:
                self.log_debug("[+] Comando executado com sucesso")
                output = f"SSH Success - {host}:{port}\n"
                output += f"Command: {command}\n"
                output += f"Output:\n{result.stdout}"
                self.set_result(output)
            else:
                self.log_debug(f"[X] Falha na execução do comando: {result.stderr}")
                error = f"SSH Failed - {host}:{port}\n"
                error += f"Error: {result.stderr}"
                self.set_result(error)
                
        except FileNotFoundError as e:
            self.log_debug(f"[X] Arquivo não encontrado: {str(e)}")
            self.set_result(f"SSH Error - {host}:{port}: {str(e)}")
        except subprocess.TimeoutExpired as e:
            self.log_debug(f"[X] Timeout: {str(e)}")
            self.set_result(f"SSH Timeout - {host}:{port}: operação excedeu {timeout} segundos")
        except subprocess.SubprocessError as e:
            self.log_debug(f"[X] Erro no subprocess: {str(e)}")
            self.set_result(f"SSH Error - {host}:{port}: erro na execução do comando: {str(e)}")
        except ValueError as e:
            self.log_debug(f"[X] Erro de validação: {str(e)}")
            self.set_result(f"SSH Error - {host}:{port}: parâmetro inválido: {str(e)}")
        except Exception as e:
            self.handle_error(e, "Erro inesperado na conexão SSH")
