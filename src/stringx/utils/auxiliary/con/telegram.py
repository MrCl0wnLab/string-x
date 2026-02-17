"""
Módulo de saída para Telegram.

Este módulo implementa funcionalidade para enviar resultados processados
via Telegram Bot API, permitindo notificações e compartilhamento de dados
extraídos pelo String-X.
"""
import json
import urllib.parse
import urllib.request
import urllib.error

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class TelegramOutput(BaseModule):
    """
    Módulo de saída para Telegram.
    
    Esta classe permite enviar dados processados via Telegram Bot,
    facilitando notificações em tempo real e compartilhamento de resultados.
    
    TODO: Implementar funcionalidade de envio via Bot API.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de saída Telegram.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Telegram Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Envia dados via Telegram Bot',
            'type': 'output'
        ,
            'example': './strx -l results.txt -st "echo {STRING}" -module "con:telegram" -pm'
        }
        
        self.options = {
            'bot_token': self.setting.STRX_TELEGRAM_BOT_TOKEN,
            'chat_id': self.setting.STRX_TELEGRAM_CHAT_ID,
            'data': str(),
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def _escape_markdown(self, text: str) -> str:
        """
        Escapa caracteres especiais do Markdown para evitar erros de parsing.
        
        Args:
            text (str): Texto a ser escapado
            
        Returns:
            str: Texto com caracteres especiais escapados
        """
        # Lista de caracteres especiais do Markdown que precisam ser escapados
        # No modo MarkdownV2: _ * [ ] ( ) ~ ` > # + - = | { } . !
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        escaped_text = text
        for char in special_chars:
            escaped_text = escaped_text.replace(char, f'\\{char}')
        
        return escaped_text
    
    def run(self):
        """
        Executa envio via Telegram.
        """
        try:
           
            data = self.options.get('data', '')
            bot_token = self.options.get('bot_token', '')
            chat_id = self.options.get('chat_id', '')
            
            if not data:
                self.log_debug("[!] Nenhum dado fornecido para enviar via Telegram")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            if not bot_token or not chat_id:
                self.log_debug("[x] Erro: bot_token e chat_id são obrigatórios")
                return
            
            # Limpar e formatar mensagem corretamente
            # Substituir \n literal por quebra de linha real
            data = data.replace('\\n', '\n')
            
            # Limitar tamanho da mensagem (Telegram tem limite de 4096 chars)
            max_length = 4000
            if len(data) > max_length:
                data = data[:max_length] + "\n\n... (mensagem truncada)"
                self.log_debug(f"[!] Mensagem truncada de {len(self.options.get('data', ''))} para {max_length} caracteres")
            
            # Escapar caracteres especiais do Markdown
            data_escaped = self._escape_markdown(data)
            
            # Preparar mensagem com formatação Markdown
            message = f"🔍 *String\\-X Analysis*\n\n{data_escaped}"

            # URL da API do Telegram
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            # Parâmetros da requisição
            params = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'MarkdownV2',  # Usando MarkdownV2 que é mais robusto
                'disable_web_page_preview': True  # Evita preview de URLs
            }
            
            self.log_debug(f"[*] Preparando envio para Telegram - {len(message)} caracteres")
            
            # Codificar dados
            data_encoded = urllib.parse.urlencode(params).encode('utf-8')
            
            # Fazer requisição
            req = urllib.request.Request(url, data=data_encoded, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('ok'):
                    self.log_debug("[+] Mensagem enviada via Telegram com sucesso")
                    self.set_result("Message sent successfully")
                else:
                    error_desc = result.get('description', 'Erro desconhecido')
                    self.log_debug(f"[x] Erro na resposta da API Telegram: {error_desc}")
                    
        except urllib.error.HTTPError as e:
            # Captura o corpo da resposta de erro
            try:
                error_body = e.read().decode('utf-8')
                self.log_debug(f"[x] HTTP Error {e.code}: {error_body[:200]}")
                
                # Se for erro de parsing do Markdown, tenta enviar sem formatação
                if e.code == 400 and "can't parse entities" in error_body:
                    self.log_debug("[!] Erro de parsing Markdown detectado. Tentando enviar sem formatação...")
                    return self._send_plain_text(data, bot_token, chat_id)
                    
            except Exception:
                pass
                
            self.handle_error(e, f"Erro HTTP {e.code} ao enviar mensagem para Telegram")
            return ""
        except urllib.error.URLError as e:
            self.handle_error(e, "Erro de conexão ao enviar mensagem para Telegram")
            return ""
        except Exception as e:
            self.handle_error(e, "Erro inesperado ao enviar mensagem para Telegram")
            return ""
    
    def _send_plain_text(self, data: str, bot_token: str, chat_id: str) -> str:
        """
        Envia mensagem sem formatação Markdown (fallback).
        
        Args:
            data (str): Dados a serem enviados
            bot_token (str): Token do bot
            chat_id (str): ID do chat
            
        Returns:
            str: "sent" se enviado com sucesso, "" caso contrário
        """
        try:
            # Limpar e formatar mensagem
            data = data.replace('\\n', '\n')
            
            # Limitar tamanho
            max_length = 4000
            if len(data) > max_length:
                data = data[:max_length] + "\n\n... (mensagem truncada)"
            
            # Preparar mensagem SEM formatação Markdown
            message = f"🔍 String-X Analysis\n\n{data}"
            
            # URL da API do Telegram
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            # Parâmetros da requisição (SEM parse_mode)
            params = {
                'chat_id': chat_id,
                'text': message,
                'disable_web_page_preview': True
            }
            
            self.log_debug("[*] Tentando envio em modo texto simples (sem Markdown)")
            
            # Codificar dados
            data_encoded = urllib.parse.urlencode(params).encode('utf-8')
            
            # Criar requisição
            req = urllib.request.Request(url, data=data_encoded)
            
            # Enviar requisição
            with urllib.request.urlopen(req, timeout=10) as response:
                result = response.read().decode('utf-8')
                result_json = json.loads(result)
                
                if result_json.get('ok'):
                    self.log_debug("[+] Mensagem enviada via Telegram (modo texto simples)")
                    self.set_result("Message sent successfully")
                    return "sent"
                else:
                    error_desc = result_json.get('description', 'Unknown error')
                    self.log_debug(f"[!] Erro na resposta da API: {error_desc}")
                    return ""
                    
        except Exception as e:
            self.log_debug(f"[!] Falha ao enviar em modo texto simples: {e}")
            return ""