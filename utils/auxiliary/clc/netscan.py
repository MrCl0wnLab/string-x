"""
Módulo collector para escaneamento de rede.

Este módulo implementa funcionalidade para escaneamento de redes,
descoberta de hosts ativos e análise de serviços em rede.

O escaneamento de rede é uma técnica fundamental para mapeamento de infraestrutura
e descoberta de ativos, permitindo:
- Identificar hosts ativos em uma rede ou faixa de IPs
- Detectar portas abertas e serviços disponíveis
- Mapear a topologia de rede básica
- Identificar potenciais alvos para análises posteriores
- Descobrir dispositivos e serviços expostos indevidamente
- Realizar reconhecimento passivo e ativo de infraestrutura

Este módulo suporta diferentes métodos de escaneamento, incluindo
ping sweeps para descoberta de hosts, port scans para identificação
de serviços disponíveis e fingerprinting básico de serviços.
"""
# Bibliotecas padrão
import time
import ipaddress
import threading
import subprocess
import platform
from typing import List, Dict, Any, Optional

# Módulos locais
from core.basemodule import BaseModule

class NetworkScanner(BaseModule):
    """
    Módulo coletor para escaneamento de rede.
    
    Esta classe permite escaneamento de redes para descoberta de hosts
    ativos, análise de portas abertas e identificação de serviços.
    Implementa diferentes métodos de varredura como ping, port e service scan.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de escaneamento de rede.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Network Scanner',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Escaneamento de rede e descoberta de hosts',
            'type': 'collector'
        ,
            'example': './strx -l networks.txt -st "echo {STRING}" -module "clc:netscan" -pm'
        }
        
        self.options = {
            'data': str(),  # IP, CIDR ou range
            'scan_type': 'ping',  # ping, port, service
            'ports': '22,23,53,80,443,993,995',
            'threads': 50,
            'timeout': 3,
            'service_detection': False,            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': 1,        # Atraso entre tentativas de requisição
        }
        
        self.results = []
        self.lock = threading.Lock()
    
    def run(self) -> None:
        """
        Executa escaneamento de rede.
        
        Este método coordena todo o processo de escaneamento, incluindo
        a validação de entrada, descoberta de hosts, análise de portas
        e serviços, dependendo do tipo de scan selecionado.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
        
        Raises:
            ValueError: Erro na validação dos parâmetros
            ConnectionError: Erro de conexão durante o scan
            TimeoutError: Timeout durante o scan
        """
        try:
            data = self.options.get('data', '').strip()
            scan_type = self.options.get('scan_type', 'ping')
            
            if not data:
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            # Gerar lista de hosts
            hosts = self._parse_targets(data)
            if not hosts:
                self.set_result("✗ Erro: Targets inválidos")
                return
            
            # Executar escaneamento baseado no tipo
            if scan_type == 'ping':
                self._ping_scan(hosts)
            elif scan_type == 'port':
                self._port_scan(hosts)
            elif scan_type == 'service':
                self._service_scan(hosts)
            else:
                self.set_result("✗ Erro: Tipo de scan inválido (ping, port, service)")
                return
            
            # Compilar resultados
            if self.results:
                result_str = f"🔍 Escaneamento: {scan_type}\n"
                result_str += f"🎯 Targets: {len(hosts)}\n"
                result_str += f"✅ Ativos: {len(self.results)}\n\n"
                
                for host_result in self.results[:20]:
                    result_str += f"{host_result}\n"
                
                if len(self.results) > 20:
                    result_str += f"... e mais {len(self.results) - 20} hosts\n"
                
                self.set_result(result_str)
            else:
                self.set_result("ℹ️ Nenhum host ativo encontrado")
                
        except ValueError as e:
            self.set_result(f"✗ Erro de validação: {str(e)}")
        except ConnectionError as e:
            self.set_result(f"✗ Erro de conexão: {str(e)}")
        except TimeoutError as e:
            self.set_result(f"✗ Timeout no escaneamento: {str(e)}")
        except Exception as e:
            self.set_result(f"✗ Erro no escaneamento: {str(e)}")
    
    def _parse_targets(self, data: str) -> List[str]:
        """
        Processa e valida os targets para escaneamento.
        
        Este método analisa a entrada que pode ser um único IP,
        um range de IPs, uma notação CIDR, ou um hostname,
        e converte em uma lista de alvos para escaneamento.
        
        Args:
            data (str): String contendo IPs, CIDR ou range
            
        Returns:
            List[str]: Lista de hosts para escaneamento
            
        Raises:
            ValueError: Se os alvos forem inválidos ou não puderem ser processados
        """
        hosts = []
        
        try:
            # CIDR notation
            if '/' in data:
                
                network = ipaddress.ip_network(data, strict=False)
                hosts = [str(ip) for ip in network.hosts()]
                
                # Limitar para evitar escaneamentos muito grandes
                if len(hosts) > 254:
                    hosts = hosts[:254]
                    
            # Range notation (192.168.1.1-10)
            elif '-' in data and '.' in data:
                base_ip, range_part = data.rsplit('.', 1)
                if '-' in range_part:
                    start, end = range_part.split('-')
                    for i in range(int(start), int(end) + 1):
                        hosts.append(f"{base_ip}.{i}")
                        
            # Single IP
            else:
                ipaddress.ip_address(data)  # Validar
                hosts = [data]
                
        except ValueError:
            # Se falhar na validação de IP, lançar erro
            raise ValueError(f"Endereço IP inválido: {data}")
        except Exception:
            # Se falhar por outro motivo, tentar como hostname
            hosts = [data]
        
        return hosts
    
    def _ping_scan(self, hosts: List[str]) -> None:
        """
        Realiza escaneamento de ping para descoberta de hosts.
        
        Este método executa um ping sweep para identificar hosts
        ativos na rede usando ICMP Echo Request ou equivalente.
        
        Args:
            hosts (List[str]): Lista de hosts para verificar
            
        Returns:
            None: Os resultados são armazenados no atributo self.results
        """
        
        def ping_host(host):
            try:
                # Comando ping baseado no SO
                if platform.system().lower() == 'windows':
                    cmd = ['ping', '-n', '1', '-w', '3000', host]
                else:
                    cmd = ['ping', '-c', '1', '-W', '3', host]
                
                result = subprocess.run(cmd, capture_output=True, timeout=5)
                
                if result.returncode == 0:
                    with self.lock:
                        self.results.append(f"✅ {host} - Host ativo")
                        
            except Exception:
                pass
        
        # Executar threads
        threads = []
        max_threads = min(self.options.get('threads', 50), len(hosts))
        
        for host in hosts:
            if len(threads) >= max_threads:
                # Aguardar threads terminarem
                for t in threads:
                    t.join()
                threads = []
            
            thread = threading.Thread(target=ping_host, args=(host,))
            thread.start()
            threads.append(thread)
            time.sleep(0.01)  # Pequeno delay
        
        # Aguardar threads restantes
        for t in threads:
            t.join()
    
    def _port_scan(self, hosts: list):
        """Escaneamento de portas."""
        import socket
        
        ports_str = self.options.get('ports', '22,23,53,80,443,993,995')
        ports = [int(p.strip()) for p in ports_str.split(',') if p.strip().isdigit()]
        timeout = self.options.get('timeout', 3)
        
        def scan_port(host, port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    with self.lock:
                        self.results.append(f"🔓 {host}:{port} - Porta aberta")
                        
            except Exception:
                pass
        
        # Executar threads
        threads = []
        max_threads = self.options.get('threads', 50)
        
        for host in hosts:
            for port in ports:
                if len(threads) >= max_threads:
                    # Aguardar algumas threads terminarem
                    for t in threads[:10]:
                        t.join()
                    threads = threads[10:]
                
                thread = threading.Thread(target=scan_port, args=(host, port))
                thread.start()
                threads.append(thread)
                time.sleep(0.001)
        
        # Aguardar threads restantes
        for t in threads:
            t.join()
    
    def _service_scan(self, hosts: list):
        """Escaneamento com detecção de serviços."""
        import socket
        
        ports_str = self.options.get('ports', '22,23,53,80,443,993,995')
        ports = [int(p.strip()) for p in ports_str.split(',') if p.strip().isdigit()]
        timeout = self.options.get('timeout', 3)
        
        def scan_service(host, port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                
                if result == 0:
                    service = self._detect_service(sock, port)
                    sock.close()
                    
                    with self.lock:
                        self.results.append(f"🔓 {host}:{port} - {service}")
                else:
                    sock.close()
                        
            except Exception:
                pass
        
        # Executar threads
        threads = []
        max_threads = self.options.get('threads', 50)
        
        for host in hosts:
            for port in ports:
                if len(threads) >= max_threads:
                    for t in threads[:10]:
                        t.join()
                    threads = threads[10:]
                
                thread = threading.Thread(target=scan_service, args=(host, port))
                thread.start()
                threads.append(thread)
                time.sleep(0.001)
        
        for t in threads:
            t.join()
    
    def _detect_service(self, sock, port: int) -> str:
        """Detecta serviço baseado na porta e banner."""
        try:
            # Tentar receber banner
            sock.settimeout(2)
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            
            if banner:
                # Análise básica de banner
                banner_lower = banner.lower()
                
                if 'ssh' in banner_lower:
                    return f"SSH ({banner[:50]})"
                elif 'http' in banner_lower or 'html' in banner_lower:
                    return f"HTTP ({banner[:50]})"
                elif 'ftp' in banner_lower:
                    return f"FTP ({banner[:50]})"
                elif 'smtp' in banner_lower:
                    return f"SMTP ({banner[:50]})"
                else:
                    return f"Unknown ({banner[:30]})"
                    
        except Exception:
            pass
        
        # Fallback para serviços conhecidos
        common_services = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S'
        }
        
        return common_services.get(port, f'Port {port}')
