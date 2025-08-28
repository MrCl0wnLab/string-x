"""
Módulo de saída para Discord.

Este módulo implementa funcionalidade para enviar resultados processados
via Discord Webhook, permitindo notificações e compartilhamento de dados
extraídos pelo String-X.
"""
import json
import urllib.parse
import urllib.request

from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class DiscordOutput(BaseModule):
    """
    Módulo de saída para Discord.
    
    Esta classe permite enviar dados processados via Discord Webhook,
    facilitando notificações em tempo real e compartilhamento de resultados.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de saída Discord.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Discord Webhook Output',
             "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Envia dados via Discord Webhook',
            'type': 'output',
            'example': './strx -l results.txt -st "echo {STRING}" -module "con:discord" -pm'
        }
        
        self.options = {
            'webhook_url': self.setting.STRX_DISCORD_WEBHOOK,
            'username': self.setting.STRX_DISCORD_USERNAME,
            'avatar_url': self.setting.STRX_DISCORD_AVATAR_URL,
            'color':self.setting.STRX_DISCORD_COLOR,
            'data': str(),
            'debug': False,
            'retry': 0,
            'retry_delay': None,
        }
    
    def run(self):
        """
        Executa envio via Discord Webhook.
        """
        try:
            data = Format.clear_value(self.options.get('data', ''))
            webhook_url = self.options.get('webhook_url', '')
            username = self.options.get('username', 'String-X Bot')
            
            if not data:
                self.log_debug("[!] Nenhum dado fornecido para enviar via Discord")
                return
            
            # Limpar resultados anteriores para evitar acúmulo
            self._result[self._get_cls_name()].clear()

            if not webhook_url:
                self.log_debug("[x] Erro: webhook_url é obrigatório")
                return
            
            self.log_debug("[*] Preparando mensagem para Discord")
            
            # Preparar embed
            embed = {
                "title": "[+] String-X Results",
                "description": f"```\n{data[:1900]}\n```",  # Limite do Discord
                "color": self.options.get('color', 0x00ff00),
                "timestamp": self._get_current_timestamp()
            }
            
            # Se os dados forem muito longos, adicionar nota
            if len(data) > 1900:
                embed["footer"] = {
                    "text": f"Dados truncados. Total: {len(data)} caracteres"
                }
            
            # Payload do webhook
            payload = {
                "username": username,
                "embeds": [embed]
            }
            
            # Adicionar avatar se fornecido
            avatar_url = self.options.get('avatar_url', '')
            if avatar_url:
                payload["avatar_url"] = avatar_url
            
            # Codificar dados
            data_encoded = json.dumps(payload).encode('utf-8')
            
            self.log_debug(f"[*] Enviando dados para Discord: {len(data)} caracteres")
            
            # Fazer requisição
            req = urllib.request.Request(webhook_url, data=data_encoded, method='POST')
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 204:
                    self.log_debug("[+] Mensagem enviada via Discord")
                    self.set_result(f"Discord: Mensagem enviada com sucesso")
                else:
                    self.log_debug(f"[x] Erro Discord: Status {response.status}")
                    
        except Exception as e:
            self.handle_error(e, "Erro ao enviar mensagem para Discord")
    
    def _get_current_timestamp(self):
        """
        Retorna timestamp atual no formato ISO.
        """
        from datetime import datetime
        return datetime.utcnow().isoformat()
