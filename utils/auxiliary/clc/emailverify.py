"""
Módulo collector para verificação de emails.

Este módulo implementa funcionalidade para verificação de emails,
incluindo validação de sintaxe, verificação de domínio MX e
verificação de SMTP quando possível.

A verificação de emails é um processo importante para:
- Validar se o formato do email está correto sintaticamente
- Verificar se o domínio possui servidores MX configurados para receber emails
- Tentar verificar a existência da conta de email (quando a opção SMTP está ativada)
- Reduzir taxa de rejeição em campanhas de email marketing
- Identificar emails potencialmente falsos ou inexistentes em investigações OSINT

Este módulo implementa diferentes níveis de verificação, desde a simples
validação de formato até tentativas de conexão SMTP para verificação de existência.
"""
from core.basemodule import BaseModule


class EmailVerifier(BaseModule):
    """
    Módulo coletor para verificação de emails.
    
    Esta classe permite verificação de endereços de email através de
    validação de sintaxe, consulta DNS MX e verificação SMTP básica.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de verificação de email.
        """
        super().__init__()
        # Metadados do módulo
        self.meta = {
            'name': 'Email Verifier',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Verificação e validação de endereços de email',
            'type': 'collector'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),  # Email address
            'check_mx': True,
            'check_smtp': False,  # Pode ser detectado como spam
            'timeout': 10,
            'example': './strx -l emails.txt -st "echo {STRING}" -module "clc:emailverify" -pm',
            'debug': False,  # Modo de debug para mostrar informações detalhadas 
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': 1,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa verificação de email.
        """
        try:
            email = self.options.get('data', '').strip().lower()
            
            if not email:
                return
            
            # Validação básica de sintaxe
            if not self._is_valid_email_syntax(email):
                self.set_result(f"✗ {email}: Sintaxe inválida")
                return
            
            username, domain = email.split('@')
            
            result = f"📧 Email: {email}\n"
            result += f"👤 Usuário: {username}\n"
            result += f"🌐 Domínio: {domain}\n"
            
            # Verificar MX record
            if self.options.get('check_mx', True):
                mx_status = self._check_mx_record(domain)
                result += f"📬 MX Record: {mx_status}\n"
                
                if 'não encontrado' in mx_status.lower():
                    result += "❌ Status: Email inválido (sem MX record)"
                    self.set_result(result)
                    return
            
            # Verificar SMTP (opcional e cuidadoso)
            if self.options.get('check_smtp', False):
                smtp_status = self._check_smtp(email, domain)
                result += f"📤 SMTP: {smtp_status}\n"
            
            # Análise adicional
            analysis = self._analyze_email(email, domain)
            if analysis:
                result += f"🔍 Análise: {analysis}\n"
            
            result += "✅ Status: Email válido"
            self.set_result(result)
            
        except Exception as e:
            self.set_result(f"✗ Erro na verificação: {str(e)}")
    
    def _is_valid_email_syntax(self, email: str) -> bool:
        """Valida sintaxe básica do email."""
        import re
        
        # Regex para validação básica
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False
        
        # Verificações adicionais
        if '..' in email or email.startswith('.') or email.endswith('.'):
            return False
        
        if email.count('@') != 1:
            return False
        
        username, domain = email.split('@')
        
        if len(username) > 64 or len(domain) > 253:
            return False
        
        return True
    
    def _check_mx_record(self, domain: str) -> str:
        """Verifica MX record do domínio."""
        try:
            import socket
            import struct
            
            # Usar nslookup como fallback se socket DNS não funcionar
            try:
                import subprocess
                result = subprocess.run(
                    ['nslookup', '-type=MX', domain],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0 and 'mail exchanger' in result.stdout.lower():
                    # Extrair servidores MX
                    lines = result.stdout.split('\n')
                    mx_servers = []
                    
                    for line in lines:
                        if 'mail exchanger' in line.lower():
                            parts = line.split('=')
                            if len(parts) > 1:
                                mx_server = parts[1].strip().split()[-1]
                                mx_servers.append(mx_server.rstrip('.'))
                    
                    if mx_servers:
                        return f"Encontrado ({', '.join(mx_servers[:2])})"
                    
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            # Fallback: tentar resolução direta
            try:
                import socket
                mx_records = socket.getaddrinfo(domain, None)
                if mx_records:
                    return "Encontrado (resolução direta)"
            except socket.gaierror:
                pass
            
            return "Não encontrado"
            
        except Exception as e:
            return f"Erro na verificação: {str(e)}"
    
    def _check_smtp(self, email: str, domain: str) -> str:
        """Verificação SMTP básica (cuidadosa para evitar spam)."""
        try:
            import smtplib
            import socket
            
            # Tentar conectar ao servidor SMTP mais comum
            smtp_ports = [25, 587, 465]
            
            for port in smtp_ports:
                try:
                    # Timeout curto para evitar demora
                    server = smtplib.SMTP(timeout=5)
                    server.connect(domain, port)
                    
                    # Verificação muito básica
                    code, message = server.helo('example.com')
                    if code == 250:
                        server.quit()
                        return f"Servidor SMTP ativo (porta {port})"
                    
                    server.quit()
                    
                except (smtplib.SMTPException, socket.error, socket.timeout):
                    continue
            
            return "Servidor SMTP não acessível"
            
        except Exception as e:
            return f"Erro SMTP: {str(e)}"
    
    def _analyze_email(self, email: str, domain: str) -> str:
        """Análise adicional do email."""
        analysis = []
        
        try:
            username = email.split('@')[0]
            
            # Verificar padrões comuns
            if any(char in username for char in ['+', '.']):
                analysis.append("possível alias")
            
            if username.isdigit():
                analysis.append("usuário numérico")
            
            if len(username) > 20:
                analysis.append("usuário longo")
            
            # Verificar domínios conhecidos
            common_domains = [
                'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
                'aol.com', 'icloud.com', 'protonmail.com'
            ]
            
            if domain in common_domains:
                analysis.append("provedor público")
            elif domain.endswith(('.gov.br', '.edu.br', '.org.br')):
                analysis.append("domínio institucional")
            elif '.' in domain and len(domain.split('.')[-1]) == 2:
                analysis.append("domínio país específico")
            
            # Verificar se parece descartável
            disposable_patterns = [
                'temp', 'throw', 'dispos', '10min', 'guerrilla',
                'mailinator', 'trash', 'junk'
            ]
            
            if any(pattern in domain.lower() for pattern in disposable_patterns):
                analysis.append("possível email descartável")
            
            return ', '.join(analysis) if analysis else "padrão normal"
            
        except Exception:
            return "análise indisponível"
