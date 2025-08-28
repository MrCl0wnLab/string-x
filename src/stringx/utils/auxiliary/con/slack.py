"""
Módulo de saída para Slack.

Este módulo implementa funcionalidade para enviar resultados processados
via Slack Webhook API, permitindo notificações e compartilhamento de dados
extraídos pelo String-X em canais Slack.
"""
import json
import urllib.request

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class SlackOutput(BaseModule):
    """
    Módulo de saída para Slack.
    
    Esta classe permite enviar dados processados via Slack Webhook,
    facilitando integração com workflows e notificações em equipe.
    
    TODO: Implementar funcionalidade de envio via Webhook.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de saída Slack.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Slack Output',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Envia dados via Slack Webhook',
            'type': 'output'
        ,
            'example': './strx -l alerts.txt -st "echo {STRING}" -module "con:slack" -pm'
        }
        
        self.options = {
            'webhook_url': str(),
            'channel': str(),
            'data': str(),
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'timeout': 10,  # Tempo limite para requisição HTTP
            'retry': 0,              # Número de tentativas de requisição
            'retry_delay': None,        # Atraso entre tentativas de requisição
        }
    
    def run(self):
        """
        Executa envio via Slack.
        """
        try:
            data = Format.clear_value(self.options.get('data', ''))
            webhook_url = self.options.get('webhook_url', '')
            channel = self.options.get('channel', '#general')
            
            if not data:
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            if not webhook_url:
                self.set_result("Erro: webhook_url é obrigatório")
                return
            
            # Preparar payload
            payload = {
                'channel': channel,
                'username': 'String-X Bot',
                'icon_emoji': ':mag:',
                'text': f"🔍 *String-X Results*",
                'attachments': [
                    {
                        'color': 'good',
                        'fields': [
                            {
                                'title': 'Dados Processados',
                                'value': f"```{data}```",
                                'short': False
                            }
                        ],
                        'footer': 'String-X OSINT Tool',
                        'ts': int(__import__('time').time())
                    }
                ]
            }
            
            # Converter para JSON
            json_data = json.dumps(payload).encode('utf-8')
            
            # Fazer requisição
            req = urllib.request.Request(webhook_url, data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    self.log_debug("[+] Mensagem enviada via Slack")
                else:
                    self.log_debug(f"[x] Erro Slack: Status {response.status}")
                    
        except Exception as e:
            self.handle_error(e, "Erro ao enviar mensagem para Slack")