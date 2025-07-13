"""
Módulo CON para conexões SSH.

Este módulo implementa funcionalidade para estabelecer conexões SSH
e executar comandos remotos.
"""
import os
import subprocess

from core.basemodule import BaseModule

class SSHConnector(BaseModule):
    """
    Módulo para conexões SSH.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'SSH Connector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Estabelece conexões SSH e executa comandos',
            'type': 'connection'
        }
        
        self.options = {
            'data': str(),  # host:port ou apenas host
            'username': 'root',
            'password': str(),
            'key_file': str(),
            'command': 'whoami',
            'timeout': 10,
            'example': './strx -l servers.txt -st "echo {STRING}" -module "con:ssh" -pm',
            'debug': False,  # Modo de debug para mostrar informações detalhadas  
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': 1,        # Atraso entre tentativas de requisição  
        }
    
    def run(self):
        """
        Executa a conexão SSH e comando especificado.
        
        Tenta estabelecer conexão SSH com o host especificado usando
        credenciais fornecidas e executa o comando configurado.
        """
        target = self.options.get("data", "").strip()
        if not target:
            return
            
        # Parse host:port
        if ':' in target:
            host, port = target.split(':', 1)
        else:
            host, port = target, '22'
        
        username = self.options.get('username', 'root')
        password = self.options.get('password', '')
        key_file = self.options.get('key_file', '')
        command = self.options.get('command', 'whoami')
        timeout = self.options.get('timeout', 10)
        
        try:
            # Construir comando SSH
            ssh_cmd = ['ssh', '-o', 'ConnectTimeout=5', 
                      '-o', 'StrictHostKeyChecking=no',
                      '-p', str(port)]
            
            if key_file and os.path.exists(key_file):
                ssh_cmd.extend(['-i', key_file])
            
            ssh_cmd.append(f"{username}@{host}")
            ssh_cmd.append(command)
            
            # Executar SSH
            if password:
                # Usar sshpass se disponível
                full_cmd = ['sshpass', '-p', password] + ssh_cmd
            else:
                full_cmd = ssh_cmd
            
            result = subprocess.run(full_cmd, capture_output=True, 
                                  text=True, timeout=timeout)
            
            if result.returncode == 0:
                output = f"SSH Success - {host}:{port}\n"
                output += f"Command: {command}\n"
                output += f"Output:\n{result.stdout}"
                self.set_result(output)
            else:
                error = f"SSH Failed - {host}:{port}\n"
                error += f"Error: {result.stderr}"
                self.set_result(error)
                
        except Exception as e:
            self.set_result(f"SSH Error - {host}:{port}: {str(e)}")
