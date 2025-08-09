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
# Bibliotecas padrão
import re
import socket
import smtplib
import subprocess
from typing import List, Dict, Any, Optional, Tuple

# Módulos locais
from stringx.core.basemodule import BaseModule


class EmailVerifier(BaseModule):
    """
    Módulo coletor para verificação de emails.
    
    Esta classe permite verificação de endereços de email através de
    validação de sintaxe, consulta DNS MX e verificação SMTP básica.
    """
    
    def __init__(self) -> None:
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
        ,
            'example': './strx -l emails.txt -st "echo {STRING}" -module "clc:emailverify" -pm'
        }
        # Opções configuráveis do módulo
        self.options = {
            'data': str(),      # Email address
            'check_mx': True,   # Verificar registros MX do domínio
            'check_smtp': False,  # Verificar servidor SMTP (pode ser detectado como spam)
            'timeout': 10,      # Timeout para operações            'debug': False,     # Modo de debug para mostrar informações detalhadas 
            'retry': 0,         # Número de tentativas de requisição
            'retry_delay': None,   # Atraso entre tentativas de requisição
        }
    

    
    def run(self) -> None:
        """
        Executa verificação de email.
        
        Esta função realiza a verificação do endereço de email fornecido,
        validando sua sintaxe, verificando registros MX e opcionalmente
        tentando uma verificação SMTP básica.
        
        Returns:
            None: Os resultados são armazenados através do método set_result
            
        Raises:
            ValueError: Se o email tiver formato inválido
            socket.gaierror: Se ocorrer erro na resolução DNS
            smtplib.SMTPException: Se ocorrer erro na conexão SMTP
            subprocess.SubprocessError: Se ocorrer erro na execução do nslookup
        """
        try:
            email = self.options.get('data', '').strip().lower()
            
            if not email:
                self.log_debug("Nenhum email fornecido")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            self.log_debug(f"Verificando email: {email}")
            
            # Validação básica de sintaxe
            if not self._is_valid_email_syntax(email):
                self.log_debug("Sintaxe de email inválida")
                self.set_result(f"{email}: Sintaxe inválida")
                return
            
            username, domain = email.split('@')
            self.log_debug(f"Email dividido em: usuário={username}, domínio={domain}")
            
            result = f"📧 Email: {email}\n"
            result += f"👤 Usuário: {username}\n"
            result += f"🌐 Domínio: {domain}\n"
            
            # Verificar MX record
            if self.options.get('check_mx', True):
                self.log_debug(f"Verificando registros MX para {domain}")
                mx_status = self._check_mx_record(domain)
                result += f"📬 MX Record: {mx_status}\n"
                
                if 'não encontrado' in mx_status.lower():
                    self.log_debug("Nenhum registro MX encontrado")
                    result += "❌ Status: Email inválido (sem MX record)"
                    self.set_result(result)
                    return
            
            # Verificar SMTP (opcional e cuidadoso)
            if self.options.get('check_smtp', False):
                self.log_debug("Realizando verificação SMTP")
                smtp_status = self._check_smtp(email, domain)
                result += f"📤 SMTP: {smtp_status}\n"
            
            # Análise adicional
            self.log_debug("Realizando análise adicional do email")
            analysis = self._analyze_email(email, domain)
            if analysis:
                result += f"🔍 Análise: {analysis}\n"
            
            result += "Status: Email válido"
            self.log_debug("Verificação concluída com sucesso")
            self.set_result(result)
            
        except ValueError as e:
            self.handle_error(f"Erro de validação: {str(e)}")
        except socket.gaierror as e:
            self.handle_error(f"Erro de resolução DNS: {str(e)}")
        except smtplib.SMTPException as e:
            self.handle_error(e, "Erro SMTP EmailVerify")
        except subprocess.SubprocessError as e:
            self.handle_error(e, "Erro subprocess EmailVerify")
        except Exception as e:
            self.handle_error(e, "Erro EmailVerify")
    
    def _is_valid_email_syntax(self, email: str) -> bool:
        """
        Valida sintaxe básica do email.
        
        Args:
            email: Endereço de email a ser validado
            
        Returns:
            True se a sintaxe do email for válida, False caso contrário
        """
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
        """
        Verifica MX record do domínio.
        
        Args:
            domain: Domínio do email a ser verificado
            
        Returns:
            String com o resultado da verificação MX
            
        Raises:
            socket.gaierror: Se ocorrer erro na resolução DNS
            subprocess.SubprocessError: Se ocorrer erro na execução do nslookup
        """
        try:
            self.log_debug(f"Verificando registros MX para: {domain}")
            
            # Usar nslookup como fallback se socket DNS não funcionar
            try:
                self.log_debug("Tentando verificação com nslookup")
                result = subprocess.run(
                    ['nslookup', '-type=MX', domain],
                    capture_output=True,
                    text=True,
                    timeout=self.options.get('timeout', 10)
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
                        self.log_debug(f"Servidores MX encontrados: {mx_servers}")
                        return f"Encontrado ({', '.join(mx_servers[:2])})"
                    
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                self.log_debug(f"Erro na verificação com nslookup: {str(e)}")
                pass
            
            # Fallback: tentar resolução direta
            try:
                self.log_debug("Tentando resolução direta")
                mx_records = socket.getaddrinfo(domain, None)
                if mx_records:
                    self.log_debug("Domínio resolvido diretamente")
                    return "Encontrado (resolução direta)"
            except socket.gaierror as e:
                self.log_debug(f"Erro na resolução direta: {str(e)}")
                pass
            
            self.log_debug("Nenhum registro MX encontrado")
            return "Não encontrado"
            
        except Exception as e:
            self.log_debug(f"Erro na verificação MX: {str(e)}")
            return f"Erro na verificação: {str(e)}"
    
    def _check_smtp(self, email: str, domain: str) -> str:
        """
        Verificação SMTP básica.
        
        Esta função tenta conectar aos servidores SMTP mais comuns para verificar
        se o domínio aceita conexões. É feita com cautela para evitar detecção como spam.
        
        Args:
            email: Endereço de email completo
            domain: Domínio do email
            
        Returns:
            String com o resultado da verificação SMTP
            
        Raises:
            smtplib.SMTPException: Se ocorrer erro específico na conexão SMTP
            socket.error: Se ocorrer erro de socket
            socket.timeout: Se a conexão exceder o tempo limite
        """
        try:
            self.log_debug(f"Iniciando verificação SMTP para {domain}")
            
            # Tentar conectar ao servidor SMTP mais comum
            smtp_ports = [25, 587, 465]
            
            for port in smtp_ports:
                try:
                    self.log_debug(f"Tentando conexão SMTP na porta {port}")
                    # Timeout curto para evitar demora
                    server = smtplib.SMTP(timeout=5)
                    server.connect(domain, port)
                    
                    # Verificação muito básica
                    code, message = server.helo('example.com')
                    if code == 250:
                        server.quit()
                        self.log_debug(f"Servidor SMTP ativo na porta {port}")
                        return f"Servidor SMTP ativo (porta {port})"
                    
                    server.quit()
                    
                except (smtplib.SMTPException, socket.error, socket.timeout) as e:
                    self.log_debug(f"Falha na porta {port}: {str(e)}")
                    continue
            
            self.log_debug("Nenhum servidor SMTP acessível")
            return "Servidor SMTP não acessível"
            
        except Exception as e:
            self.log_debug(f"Erro na verificação SMTP: {str(e)}")
            return f"Erro SMTP: {str(e)}"
    
    def _analyze_email(self, email: str, domain: str) -> str:
        """
        Realiza análise adicional do email.
        
        Esta função verifica padrões e características do email para
        fornecer informações adicionais sobre sua natureza.
        
        Args:
            email: Endereço de email completo
            domain: Domínio do email
            
        Returns:
            String com análises e observações sobre o email
        """
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
            
        except Exception as e:
            self.log_debug(f"Erro na análise adicional: {str(e)}")
            return "análise indisponível"
