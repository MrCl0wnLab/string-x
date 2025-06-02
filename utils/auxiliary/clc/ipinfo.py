"""
Módulo CLC para scanner de portas.

Este módulo implementa um scanner de portas básico usando sockets
para verificação de conectividade com suporte a threads.
"""
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from core.basemodule import BaseModule

class PortScanner(BaseModule):
    """
    Scanner de portas básico usando sockets com threads.
    """
    
    def __init__(self):
        super().__init__()
        
        self.meta = {
            'name': 'Port Scanner',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Scanner de portas usando sockets com threads',
            'type': 'collector'
        }
        
        self.options = {
            'data': str(),  # IP ou hostname
            'ports': '22,80,443,21,25,53,110,143,993,995,3389',
            'timeout': 2,
            'threads': 50,
            'example': './strx -l targets.txt -st "echo {STRING}" -module "clc:ipinfo" -pm'
        }
    
    def run(self):
        """
        Executa o scanner de portas com threads.
        
        Verifica as portas especificadas no host e armazena os resultados.
        """
        target = self.options.get("data", "").strip()
        if not target:
            return
            
        ports_str = self.options.get('ports', '80,443')
        
        # Parse portas
        ports = []
        for port_range in ports_str.split(','):
            port_range = port_range.strip()
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(port_range))
        
        # Scanner com threads
        open_ports = []
        with ThreadPoolExecutor(max_workers=self.options.get('threads', 50)) as executor:
            futures = [executor.submit(self._scan_port, target, port) for port in ports]
            for future in futures:
                result = future.result()
                if result:
                    open_ports.append(result)
        
        # Formatação dos resultados
        if open_ports:
            result = f"Target: {target}\nOpen Ports:\n"
            for port_info in sorted(open_ports):
                result += f"  {port_info}\n"
            self.set_result(result)
        else:
            self.set_result(f"Target: {target}\nNo open ports found")
    
    def _scan_port(self, target: str, port: int) -> str:
        """Escaneia uma porta específica."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.options.get('timeout', 2))
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                service = self._get_service(port)
                return f"{port}/tcp - {service}"
        except Exception:
            pass
        return None
    
    def _get_service(self, port: int) -> str:
        """Retorna serviço comum para a porta."""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 993: 'IMAPS', 995: 'POP3S', 3389: 'RDP',
            3306: 'MySQL', 5432: 'PostgreSQL', 6379: 'Redis'
        }
        return services.get(port, 'Unknown')