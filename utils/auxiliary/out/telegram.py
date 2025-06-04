"""
Módulo de saída para Telegram.

Este módulo implementa funcionalidade para enviar resultados processados
via Telegram Bot API, permitindo notificações e compartilhamento de dados
extraídos pelo String-X.
"""
from core.basemodule import BaseModule
import json
import urllib.request
import urllib.parse
from core.format import Format

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
        }
        
        self.options = {
            'bot_token': str(),
            'chat_id': str(),
            'data': str(),
            'example': './strx -l results.txt -st "echo {STRING}" -module "out:telegram" -pm'
        }
    
    def run(self):
        """
        Executa envio via Telegram.
        """
        try:
           
            
            data = Format.clear_value(self.options.get('data', ''))
            bot_token = self.options.get('bot_token', '')
            chat_id = self.options.get('chat_id', '')
            
            if not data:
                return
            
            if not bot_token or not chat_id:
                self.set_result("✗ Erro: bot_token e chat_id são obrigatórios")
                return
            
            # Preparar mensagem
            message = f"🔍 *String-X Results*\n\n```\n{data}\n```"
            
            # URL da API do Telegram
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            # Parâmetros da requisição
            params = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            # Codificar dados
            data_encoded = urllib.parse.urlencode(params).encode('utf-8')
            
            # Fazer requisição
            req = urllib.request.Request(url, data=data_encoded, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('ok'):
                    self.set_result("✓ Mensagem enviada via Telegram")
                else:
                    self.set_result(f"✗ Erro Telegram: {result.get('description', 'Erro desconhecido')}")
                    
        except Exception as e:
            self.set_result(f"✗ Erro Telegram: {str(e)}")