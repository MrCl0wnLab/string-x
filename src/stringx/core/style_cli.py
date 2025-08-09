"""
Módulo de estilização da interface CLI.

Este módulo fornece classes para estilização e highlight da interface de linha
de comando usando a biblioteca Rich, incluindo temas customizados, highlighters
de sintaxe e formatação de argumentos.
"""
import argparse
from rich.theme import Theme
from rich.console import Console
from rich.highlighter import RegexHighlighter


class StyleHighlighter(RegexHighlighter):
    """
    Classe para highlight de sintaxe customizado.
    
    Esta classe define temas e padrões de regex para colorir automaticamente
    diferentes tipos de dados na saída da CLI, incluindo IPs, URLs, domínios,
    funções e strings especiais.
    
    Attributes:
        theme (Theme): Tema Rich com cores customizadas
        base_style (str): Prefixo base para estilos
        highlights (list): Lista de padrões regex para highlight
        
    References:
        https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
        https://rich.readthedocs.io/en/stable/markup.html#console-markup
        https://rich.readthedocs.io/en/stable/style.html#styles
        https://github.com/Textualize/rich/blob/master/examples/highlighter.py
    """
    theme = Theme(
        {
            # Existing styles
            "sty.param":        "bright_yellow",
            "sty.info":         "bold yellow1",
            "sty.label":        "yellow3",
            "sty.string":       "bright_magenta",
            "sty.strx":         "bright_magenta",
            "sty.domain":       "bright_black",
            "sty.url":          "cyan1",
            "sty.ipv4":         "bright_green",
            "sty.ipv6":         "spring_green3",
            "sty.error":        "bright_red",
            "sty.func":         "blue_violet",
            
            # Security & OSINT data types
            "sty.hash":         "gold3",
            "sty.crypto":       "green3",
            "sty.phone":        "dodger_blue2",
            "sty.mac":          "cyan3",
            "sty.apikey":       "red3",
            "sty.cve":          "orange_red1",
            
            # Module and system patterns
            "sty.module":       "bright_magenta",
            "sty.social":       "purple3",
            "sty.service":      "steel_blue1",
            "sty.port":         "green4",
            
            # Data formats
            "sty.json":         "khaki3",
            "sty.xml":          "light_salmon3",
            "sty.timestamp":    "grey70",
            "sty.coordinates":  "turquoise2",
            "sty.base64":       "orange3",
            
            # Network & protocols
            "sty.cidr":         "light_green",
            "sty.protocol":     "steel_blue3",
            "sty.cloud":        "sky_blue1",
            
            # Status and feedback
            "sty.success":      "green",
            "sty.warning":      "yellow",
            "sty.http_success": "green",
            "sty.http_redirect": "yellow",
            "sty.http_error":   "red",
            "sty.http_server":  "bright_red",
            
            # IOCs and security
            "sty.ioc":          "bright_red",
            "sty.useragent":    "grey50",
            "sty.file_sig":     "magenta3",
        }
    )
    
    base_style = "sty."
    highlights = [
        # Status and error patterns (high priority)
        r"(?P<error>(error|not found|timed out|failed|exception|invalid|denied|refused|unreachable))",
        r"(?P<success>(success|completed|ok|done|finished|passed|found|valid|active))",
        r"(?P<warning>(warning|caution|deprecated|timeout|slow|retry))",
        r"(?P<info>\[\!\]|INFO:|NOTE:|DEBUG:|VERBOSE:)",
        r"(?P<label>(TEMPLATE|COMMAND|PIPE|CONFIG|DATA|RESULT|Chain):)",
        
        # HTTP status codes
        r"(?P<http_success>\b(200|201|202|204)\b)",
        r"(?P<http_redirect>\b(301|302|303|307|308)\b)",
        r"(?P<http_error>\b(400|401|403|404|405|406|410|411|413|414|415|429)\b)",
        r"(?P<http_server>\b(500|501|502|503|504|505)\b)",
        
        # Security & OSINT data types
        r"(?P<hash>\b([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{56}|[a-fA-F0-9]{64}|[a-fA-F0-9]{96}|[a-fA-F0-9]{128})\b)",
        r"(?P<crypto>(\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|\b0x[a-fA-F0-9]{40}\b|\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b|\bD[5-9A-HJ-NP-U][1-9A-HJ-NP-Za-km-z]{32}\b))",
        r"(?P<phone>(\+?55\s?)?(\(?0?[1-9]{2}\)?\s?)([0-9]{4,5}[.-]?[0-9]{4})|(\+?[1-9]{1,4}[\s.-]?)?(\(?\d{1,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4})",
        r"(?P<mac>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))",
        r"(?P<cve>CVE-\d{4}-\d{4,7})",
        r"(?P<apikey>([Aa][Pp][Ii][_]?[Kk][Ee][Yy][_=:]\s*[a-zA-Z0-9+/=]{16,}|[Tt][Oo][Kk][Ee][Nn][_=:]\s*[a-zA-Z0-9+/=]{16,}))",
        
        # Module references and system patterns
        r"(?P<module>\b(ext|clc|con|out):[a-zA-Z0-9_]+)",
        r"(?P<social>(@[a-zA-Z0-9_]+|t\.me/[a-zA-Z0-9_]+))",
        r"(?P<service>\b(ssh|ftp|http|https|smtp|pop3|imap|dns|dhcp|ntp|snmp|telnet|mysql|postgresql|mongodb|redis|elasticsearch|docker)\b)",
        r"(?P<port>:([0-9]{1,5})\b)",
        
        # Data formats and protocols
        r"(?P<json>(\{[^{}]*\}|\[[^\[\]]*\]|\"[^\"]*\":[^,}]+))",
        r"(?P<xml>(<[^>]+>|<\/[^>]+>))",
        r"(?P<base64>\b[A-Za-z0-9+/]{16,}={0,2}\b)",
        r"(?P<timestamp>(\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}:\d{2}|\d{10}|\d{13}))",
        r"(?P<coordinates>(-?\d{1,3}\.\d{1,10}),?\s*(-?\d{1,3}\.\d{1,10}))",
        
        # Network patterns (ordered by specificity)
        r"(?P<url>(https?|ftp|ssh|sftp|ldap)://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*))",
        r"(?P<cidr>\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:[1-2]?[0-9]|3[0-2])\b)",
        r"(?P<ipv4>\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)",
        r"(?P<ipv6>\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b|\b::1\b|\b(?:[a-fA-F0-9]{1,4}:){0,6}::(?:[a-fA-F0-9]{1,4}:){0,6}[a-fA-F0-9]{1,4}\b)",
        r"(?P<domain>\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\b)",
        r"(?P<email>\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b)",
        
        # Cloud platform identifiers
        r"(?P<cloud>(arn:aws:[^:]+:[^:]*:[^:]*:[^:\s]+|projects/[a-z0-9-]+|subscriptions/[a-f0-9-]+|/subscriptions/[a-f0-9-]+))",
        
        # Functions and strings
        r"(?P<func>([a-zA-Z_][a-zA-Z0-9_]*\([^)]*\)))",
        r"(?P<string>(\{[^{}]*\}|\[[^\[\]]*\]|\"[^\"]*\"|'[^']*'))",
        r"(?P<strx>\bstrx\b|\bSTR[X\d]\b)",
        
        # File paths and parameters
        r"(?P<file>([\/\\][\w\-\.\s]+[\/\\])+[\w\-\.]+|[A-Za-z]:\\(?:[\w\-\.\s]+\\)*[\w\-\.]+)",
        r"(?P<param>--[a-zA-Z0-9_-]+(?:=\S*)?|-[a-zA-Z0-9])",
        
        # IOCs and security indicators
        r"(?P<ioc>(malware|trojan|virus|backdoor|rootkit|botnet|phishing|spam|suspicious))",
        r"(?P<useragent>(Mozilla/[0-9]\.[0-9]|Chrome/[0-9]+\.[0-9]+|Safari/[0-9]+\.[0-9]+))",
        r"(?P<file_sig>(\x7fELF|\x4d\x5a|\xff\xd8\xff|\x89PNG|PK\x03\x04))",
    ]


class RichArgumentParser(argparse.ArgumentParser):
    """
    Parser de argumentos customizado com suporte ao Rich.
    
    Esta classe estende ArgumentParser para suportar formatação Rich na
    exibição de mensagens e help do parser.
    """
    def _print_message(self, message, file=None):
        """
        Imprime mensagem usando console Rich.
        
        Args:
            message: Mensagem a ser impressa
            file: Arquivo de destino (não utilizado)
        """
        if message:
            cli = StyleCli()
            return cli.console.print(message)

    def _add_argument(self, *args, **kwargs):
        """
        Adiciona argumento com formatação Rich em verde.
        
        Args:
            *args: Argumentos posicionais do argparse
            **kwargs: Argumentos nomeados do argparse
            
        Returns:
            Grupo de argumentos formatado
        """
        group = super().add_argument(*args, **kwargs)
        group_option_strings = []
        group_option_strings.extend(group.option_strings)
        group.option_strings.clear()
        [group.option_strings.append(f"[green]{line.replace('\n', '')}[/green]") for line in group_option_strings]
        return group

    def _add_argument_dest(self, *args, **kwargs):
        """
        Adiciona argumento com destino formatado em vermelho.
        
        Args:
            *args: Argumentos posicionais do argparse
            **kwargs: Argumentos nomeados do argparse
            
        Returns:
            Destino formatado do argumento
        """
        group = super().add_argument(*args, **kwargs)
        group.dest = f"[red]{group.dest}[/red]"
        return group.dest


class RawDescriptionHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """
    Formatador customizado para descrições de help.
    
    Esta classe estende RawDescriptionHelpFormatter para aplicar formatação
    Rich às linhas de descrição do help dos argumentos.
    """
    def _split_lines(self, text: str, width):
        """
        Divide texto em linhas com formatação Rich.
        
        Args:
            text (str): Texto a ser dividido
            width: Largura máxima (não utilizado)
            
        Returns:
            Lista de linhas formatadas com markup Rich
        """
        if text:
            help_list = [f"[bright_white]{line}[/bright_white]" for line in text.splitlines()]
            return help_list


class StyleCli(RegexHighlighter):
    """
    Classe principal para interface CLI estilizada.
    
    Esta classe gerencia o console Rich com highlighter customizado e
    fornece métodos para saída formatada e logs verbose.
    
    Attributes:
        console_highlighter (StyleHighlighter): Instância do highlighter
        console (Console): Console Rich configurado
    """
    def __init__(self):
        """
        Inicializa StyleCli com console Rich configurado.
        """
        self.console_highlighter = StyleHighlighter()
        self.console = Console(
            highlighter=self.console_highlighter, 
            theme=self.console_highlighter.theme,
            log_path=False,
            highlight=True,
            log_time_format='[%f] %Y-%m-%d,%H:%M:%S'
        )

    def verbose(self, value: str, verbose: bool):
        """
        Exibe log verbose se habilitado.
        
        Args:
            value (str): Mensagem a ser exibida
            verbose (bool): Flag indicando se verbose está ativo
            
        Returns:
            Resultado do log ou None se verbose desabilitado
        """
        if value and verbose is True:
            return self.console.log(value)


