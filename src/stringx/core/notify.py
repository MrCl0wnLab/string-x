"""
Módulo de notificações para String-X.

Este módulo fornece funcionalidade para enviar notificações desktop quando
comandos String-X são finalizados, incluindo um resumo detalhado da execução.
"""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from notifypy import Notify
    NOTIFY_AVAILABLE = True
    
    # Test if notifications are actually available in the current environment
    # Some environments (Docker, headless, CI/CD) may have notify_py but no notification system
    try:
        test_notification = Notify()
        test_notification.title = "Test"
        test_notification.message = "Test"
        # Don't actually send the test notification
        NOTIFY_FUNCTIONAL = True
    except Exception:
        NOTIFY_FUNCTIONAL = False
        
except ImportError:
    NOTIFY_AVAILABLE = False
    NOTIFY_FUNCTIONAL = False

from stringx.core.logger import logger
from stringx.config import setting


class NotificationManager:
    """
    Gerenciador de notificações desktop para String-X.
    
    Esta classe é responsável por coletar informações de execução e enviar
    notificações desktop com resumos detalhados quando comandos são finalizados.
    
    Attributes:
        enabled (bool): Flag indicando se as notificações estão habilitadas
        start_time (float): Timestamp de início da execução
        end_time (float): Timestamp de fim da execução
        command_executed (str): Comando que foi executado
        total_results (int): Total de resultados obtidos
        modules_used (List[str]): Lista de módulos utilizados
        functions_used (List[str]): Lista de funções utilizadas
        execution_details (Dict): Detalhes adicionais da execução
    """
    
    def __init__(self):
        """
        Inicializa o gerenciador de notificações.
        
        Verifica se a biblioteca notify_py está disponível e funcional no
        ambiente atual, configurando as variáveis de controle da execução.
        """
        self.enabled = False
        self.available = NOTIFY_AVAILABLE and NOTIFY_FUNCTIONAL
        
        # Estatísticas de execução
        self.start_time = None
        self.end_time = None
        self.command_executed = ""
        self.total_results = 0
        self.modules_used = []
        self.functions_used = []
        self.execution_details = {}
        
        # Configurações da notificação (usando variáveis do setting.py)
        self.app_name = setting.STRX_NOTIFICATION_APP_NAME
        
        # Set the String-X icon path
        icon_path = self._get_icon_path()
        self.app_icon = icon_path if icon_path and os.path.exists(icon_path) else None
        self.debug_mode = False  # Para testes sem enviar notificações reais
        
        if not self.available:
            logger.warning("notify_py não está disponível ou não funcional neste ambiente. Notificações desabilitadas.")
    
    def enable(self) -> bool:
        """
        Habilita as notificações se a biblioteca estiver disponível.
        
        Returns:
            bool: True se as notificações foram habilitadas com sucesso
        """
        if not self.available:
            logger.error("Não é possível habilitar notificações: notify_py não está disponível")
            return False
            
        self.enabled = True
        logger.debug("Notificações habilitadas")
        return True
    
    def disable(self):
        """Desabilita as notificações."""
        self.enabled = False
        logger.debug("Notificações desabilitadas")
    
    def start_execution(self, command: str):
        """
        Marca o início da execução de um comando.
        
        Args:
            command (str): Comando que está sendo executado
        """
        if not self.enabled:
            return
            
        self.start_time = time.time()
        self.command_executed = command
        self.total_results = 0
        self.modules_used = []
        self.functions_used = []
        self.execution_details = {}
        
        logger.debug(f"Iniciando rastreamento de execução: {command}")
    
    def add_result(self, count: int = 1):
        """
        Adiciona ao contador de resultados.
        
        Args:
            count (int): Número de resultados a adicionar
        """
        if not self.enabled:
            return
            
        self.total_results += count
    
    def add_module_used(self, module_name: str):
        """
        Adiciona um módulo à lista de módulos utilizados.
        
        Args:
            module_name (str): Nome do módulo utilizado
        """
        if not self.enabled:
            return
            
        if module_name and module_name not in self.modules_used:
            self.modules_used.append(module_name)
    
    def add_function_used(self, function_name: str):
        """
        Adiciona uma função à lista de funções utilizadas.
        
        Args:
            function_name (str): Nome da função utilizada
        """
        if not self.enabled:
            return
            
        if function_name and function_name not in self.functions_used:
            self.functions_used.append(function_name)
    
    def add_execution_detail(self, key: str, value: Any):
        """
        Adiciona um detalhe da execução.
        
        Args:
            key (str): Chave do detalhe
            value (Any): Valor do detalhe
        """
        if not self.enabled:
            return
            
        self.execution_details[key] = value
    
    def end_execution(self):
        """
        Marca o fim da execução e envia a notificação com o resumo.
        """
        if not self.enabled:
            return
            
        self.end_time = time.time()
        
        # Envia a notificação
        self._send_notification()
    
    def _format_execution_time(self) -> str:
        """
        Formata o tempo de execução em uma string legível.
        
        Returns:
            str: Tempo de execução formatado
        """
        if not self.start_time or not self.end_time:
            return "Tempo não disponível"
            
        duration = self.end_time - self.start_time
        
        if duration < 1:
            return f"{duration * 1000:.0f}ms"
        elif duration < 60:
            return f"{duration:.2f}s"
        else:
            minutes = int(duration // 60)
            seconds = duration % 60
            return f"{minutes}m {seconds:.2f}s"
    
    def _format_datetime(self, timestamp: float) -> str:
        """
        Formata um timestamp em string de data/hora legível.
        
        Args:
            timestamp (float): Timestamp a ser formatado
            
        Returns:
            str: Data/hora formatada
        """
        return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
    
    def _create_notification_message(self) -> tuple[str, str]:
        """
        Cria o título e mensagem da notificação.
        
        Returns:
            tuple[str, str]: Título e mensagem da notificação
        """
        title = "String-X - Execução Finalizada"
        
        # Constrói a mensagem com resumo da execução
        message_parts = []
        
        # Comando executado
        if self.command_executed:
            cmd_short = self.command_executed[:50] + "..." if len(self.command_executed) > 50 else self.command_executed
            message_parts.append(f"Comando: {cmd_short}")
        
        # Total de resultados
        message_parts.append(f"Resultados: {self.total_results}")
        
        # Módulos utilizados
        if self.modules_used:
            modules_str = ", ".join(self.modules_used[:3])  # Limita a 3 módulos
            if len(self.modules_used) > 3:
                modules_str += f" (+{len(self.modules_used) - 3} mais)"
            message_parts.append(f"Módulos: {modules_str}")
        
        # Funções utilizadas
        if self.functions_used:
            functions_str = ", ".join(self.functions_used[:3])  # Limita a 3 funções
            if len(self.functions_used) > 3:
                functions_str += f" (+{len(self.functions_used) - 3} mais)"
            message_parts.append(f"Funções: {functions_str}")
        
        # Tempo de execução
        execution_time = self._format_execution_time()
        message_parts.append(f"Tempo: {execution_time}")
        
        # Horários de início e fim
        if self.start_time and self.end_time:
            start_str = self._format_datetime(self.start_time)
            end_str = self._format_datetime(self.end_time)
            message_parts.append(f"Período: {start_str} - {end_str}")
        
        message = "\n".join(message_parts)
        
        return title, message
    
    def _get_icon_path(self) -> str:
        """
        Obtém o caminho para o ícone do String-X.
        
        Procura primeiro por variáveis de ambiente ou arquivo default.json,
        depois usa o caminho relativo padrão do projeto.
        
        Environment variables checked (via setting.py):
        - STRX_NOTIFICATION_ICON_PATH: Caminho completo para o ícone
        - STRX_PROJECT_ROOT: Diretório raiz do projeto (setting.PROJECT_ROOT)
        
        Returns:
            str: Caminho absoluto para o ícone ou None se não encontrado
        """
        try:
            # 1. Check setting.py configured icon path (from STRX_NOTIFICATION_ICON_PATH)
            if setting.STRX_NOTIFICATION_ICON_PATH and os.path.exists(setting.STRX_NOTIFICATION_ICON_PATH):
                return str(Path(setting.STRX_NOTIFICATION_ICON_PATH).absolute())
            
            # 2. Check PROJECT_ROOT from setting.py + asset/img/icon.png
            if hasattr(setting, 'PROJECT_ROOT') and setting.PROJECT_ROOT:
                icon_path = setting.PROJECT_ROOT / "asset" / "img" / "icon.png"
                if icon_path.exists():
                    return str(icon_path.absolute())
            
            # 3. Fallback to relative path detection
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent.parent
            icon_path = project_root / "asset" / "img" / "icon.png"
            
            if icon_path.exists():
                return str(icon_path.absolute())
            else:
                return None
                
        except Exception:
            return None
    
    def _get_audio_path(self) -> str:
        """
        Obtém o caminho para o arquivo de áudio da notificação.
        
        Procura o arquivo de áudio configurado em setting.py ou nos caminhos padrão.
        
        Returns:
            str: Caminho absoluto para o arquivo de áudio ou None se não encontrado
        """
        try:
            if not setting.STRX_NOTIFICATION_AUDIO_ENABLED:
                return None
            # 1. Check setting.py configured audio path (from STRX_NOTIFICATION_AUDIO_PATH)
            if setting.STRX_NOTIFICATION_AUDIO_PATH:
                # If it's an absolute path, use as-is
                if Path(setting.STRX_NOTIFICATION_AUDIO_PATH).is_absolute():
                    if Path(setting.STRX_NOTIFICATION_AUDIO_PATH).exists():
                        return str(Path(setting.STRX_NOTIFICATION_AUDIO_PATH).absolute())
                else:
                    # If it's relative, resolve from PROJECT_ROOT
                    if hasattr(setting, 'PROJECT_ROOT') and setting.PROJECT_ROOT:
                        audio_path = setting.PROJECT_ROOT / setting.STRX_NOTIFICATION_AUDIO_PATH
                        if audio_path.exists():
                            return str(audio_path.absolute())
            
            # 2. Fallback to default locations in asset/song/
            if hasattr(setting, 'PROJECT_ROOT') and setting.PROJECT_ROOT:
                # Try different audio formats
                for filename in ['notification.wav', 'notification.mp3', 'notification.ogg']:
                    audio_path = setting.PROJECT_ROOT / "asset" / "song" / filename
                    if audio_path.exists():
                        return str(audio_path.absolute())
            
            # 3. Fallback to relative path detection
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent.parent
            for filename in ['notification.wav', 'notification.mp3', 'notification.ogg']:
                audio_path = project_root / "asset" / "song" / filename
                if audio_path.exists():
                    return str(audio_path.absolute())
            
            return None
                
        except Exception:
            return None
    
    def _send_notification(self):
        """
        Envia a notificação desktop com o resumo da execução.
        """
        if not self.available:
            logger.error("Não é possível enviar notificação: notify_py não está disponível")
            return
            
        try:
            title, message = self._create_notification_message()
            
            # Cria e configura a notificação
            notification = Notify()
            notification.title = title
            notification.message = message
            notification.application_name = self.app_name
            
            # Define ícone se disponível
            if self.app_icon:
                notification.icon = self.app_icon
            
            # Define áudio se disponível e arquivo existir
            if setting.STRX_NOTIFICATION_AUDIO_PATH:
                audio_path = self._get_audio_path()
                if audio_path:
                    notification.audio = audio_path
                    logger.debug(f"Audio configurado: {audio_path}")
            
            # Envia a notificação
            notification.send(block=False)
            
            logger.info("Notificação enviada com sucesso")
            logger.debug(f"Título: {title}")
            logger.debug(f"Mensagem: {message.replace(chr(10), ' | ')}")  # Replace newlines for log
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")
    
    def send_custom_notification(self, title: str, message: str):
        """
        Envia uma notificação customizada.
        
        Args:
            title (str): Título da notificação
            message (str): Mensagem da notificação
        """
        if not self.enabled or not self.available:
            logger.warning("Notificações não estão disponíveis ou habilitadas")
            return
            
        try:
            notification = Notify()
            notification.title = title
            notification.message = message
            notification.application_name = self.app_name
            
            # Define ícone se disponível
            if self.app_icon:
                notification.icon = self.app_icon
            
            # Define áudio se disponível e arquivo existir
            if setting.STRX_NOTIFICATION_AUDIO_PATH:
                audio_path = self._get_audio_path()
                if audio_path:
                    notification.audio = audio_path
                    logger.debug(f"Audio customizado configurado: {audio_path}")
            
            notification.send(block=False)
            logger.info(f"Notificação customizada enviada: {title}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação customizada: {e}")


# Instância global para uso em todo o projeto
notification_manager = NotificationManager()