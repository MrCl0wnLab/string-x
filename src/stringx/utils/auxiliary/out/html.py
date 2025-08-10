"""
Módulo de saída HTML.

Este módulo implementa funcionalidade para gerar relatórios em formato HTML
com estilização e visualização aprimorada dos dados do String-X.
"""
import os
import html
from datetime import datetime
from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class HTMLOutput(BaseModule):
    """
    Módulo de saída HTML.
    
    Esta classe gera relatórios HTML formatados com CSS incorporado
    para visualização profissional dos resultados do String-X.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de saída HTML.
        """
        super().__init__()
        
        self.meta = {
            'name': 'HTML Report Output',
             "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Gera relatórios em HTML',
            'type': 'output',
            'example': './strx -l results.txt -module "out:html" -pm'
        }
        
        self.options = {
            'data': str(),
            'output_file': '',          # Arquivo de saída (auto se vazio)
            'title': 'String-X Report', # Título do relatório
            'theme': self.setting.STRX_HTML_REPORT_THEME,           # dark, light, auto
            'include_timestamp': True, # Incluir timestamp
            'include_stats': True,     # Incluir estatísticas
            'auto_open': self.setting.STRX_HTML_REPORT_OUTO_OPEN,        # Abrir automaticamente no browser
            'template': 'default',     # Template a usar
            'custom_css': '',          # CSS customizado
            'debug': False
        }
    
    def run(self):
        """
        Executa geração do relatório HTML.
        """
        try:
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            
            data = self.options.get('data', '')
            
            if not data:
                self.log_debug("[!] Nenhum dado fornecido para gerar relatório")
                return
            
            self.log_debug("[*] Iniciando geração de relatório HTML")
            
            # Determinar arquivo de saída
            output_file = self._get_output_file()
            
            # Gerar conteúdo HTML
            html_content = self._generate_html(data)
            
            # Salvar arquivo
            self._save_html_file(output_file, html_content)
            
            # Abrir automaticamente se solicitado
            if self.options.get('auto_open', False):
                self._open_in_browser(output_file)
            
        except Exception as e:
            self.handle_error(e, "Erro na geração de relatório HTML")
    
    def _get_output_file(self):
        """
        Determina o arquivo de saída HTML.
        """
        output_file = self.options.get('output_file', '').strip()
        
        if not output_file:
            # Gerar nome automático
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"stringx_report_{timestamp}.html"
        
        # Garantir extensão .html
        if not output_file.lower().endswith('.html'):
            output_file += '.html'
        
        # Usar diretório de saída do projeto se disponível
        if hasattr(self.setting, 'STRX_LOG_DIRECTORY'):
            output_dir = self.setting.STRX_LOG_DIRECTORY
            if output_dir and os.path.exists(output_dir):
                output_file = os.path.join(output_dir, output_file)
        
        return output_file
    
    def _generate_html(self, data):
        """
        Gera o conteúdo HTML completo.
        """
        title = self.options.get('title', 'String-X Report')
        theme = self.options.get('theme', 'dark')
        include_timestamp = self.options.get('include_timestamp', True)
        include_stats = self.options.get('include_stats', True)
        
        # Preparar dados
        escaped_data = html.escape(data)
        lines = data.split("\n")
        stats = self._calculate_stats(data)
        
        # Gerar HTML
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        {self._get_css_styles(theme)}
    </style>
</head>
<body class="theme-{theme}">
    <div class="container">
        <header class="header">
            <h1>🔍 {html.escape(title)}</h1>
            <div class="subtitle">Gerado pelo String-X Framework</div>
            {self._get_timestamp_html() if include_timestamp else ''}
        </header>
        
        {self._get_stats_html(stats) if include_stats else ''}
        
        <main class="content">
            <div class="data-section">
                <h2>📄 Resultados</h2>
                <div class="data-container">
                    <pre class="data-content">{escaped_data}</pre>
                </div>
            </div>
            
            {self._get_lines_section(lines)}
        </main>
        
        <footer class="footer">
            <p>Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
            <p>String-X Framework - Ferramenta de Extração e Análise de Dados</p>
        </footer>
    </div>
    
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>"""
        
        return html_content
    
    def _get_css_styles(self, theme):
        """
        Retorna estilos CSS baseado no tema.
        """
        base_css = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            transition: all 0.3s ease;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            border-radius: 10px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.1em;
            opacity: 0.8;
        }
        
        .timestamp {
            margin-top: 15px;
            font-size: 0.9em;
            opacity: 0.7;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .content {
            margin-bottom: 30px;
        }
        
        .data-section h2,
        .lines-section h2 {
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .data-container {
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 30px;
        }
        
        .data-content {
            padding: 20px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-word;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .lines-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 10px;
        }
        
        .line-item {
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            border-left: 3px solid;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            border-top: 1px solid;
            margin-top: 30px;
            opacity: 0.7;
        }
        
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1.2em;
        }
        """
        
        # Temas específicos
        if theme == 'dark':
            theme_css = """
            .theme-dark {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #e0e0e0;
            }
            
            .theme-dark .header {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            }
            
            .theme-dark .stat-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .theme-dark .data-container {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .theme-dark .line-item {
                background: rgba(255, 255, 255, 0.05);
                border-left-color: #00d4ff;
            }
            
            .theme-dark .footer {
                border-top-color: rgba(255, 255, 255, 0.2);
            }
            """
        else:  # light theme
            theme_css = """
            .theme-light {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #333;
            }
            
            .theme-light .header {
                background: rgba(255, 255, 255, 0.8);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .theme-light .stat-card {
                background: rgba(255, 255, 255, 0.8);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .theme-light .data-container {
                background: rgba(255, 255, 255, 0.9);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .theme-light .line-item {
                background: rgba(255, 255, 255, 0.7);
                border-left-color: #007acc;
            }
            
            .theme-light .footer {
                border-top-color: rgba(0, 0, 0, 0.1);
            }
            """
        
        custom_css = self.options.get('custom_css', '')
        
        return base_css + theme_css + custom_css
    
    def _get_timestamp_html(self):
        """
        Retorna HTML do timestamp.
        """
        now = datetime.now()
        return f'<div class="timestamp">📅 {now.strftime("%d/%m/%Y")} ⏰ {now.strftime("%H:%M:%S")}</div>'
    
    def _get_stats_html(self, stats):
        """
        Retorna HTML das estatísticas.
        """
        return f"""
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{stats['total_chars']}</div>
                <div class="stat-label">Total de Caracteres</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['total_lines']}</div>
                <div class="stat-label">Total de Linhas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['non_empty_lines']}</div>
                <div class="stat-label">Linhas com Dados</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['avg_line_length']}</div>
                <div class="stat-label">Média Chars/Linha</div>
            </div>
        </div>
        """
    
    def _get_lines_section(self, lines):
        """
        Retorna seção com linhas individuais.
        """
        if len(lines) <= 1:
            return ""
        
        lines_html = ""
        for i, line in enumerate(lines[:100], 1):  # Limitar a 100 linhas
            if line.strip():
                escaped_line = html.escape(line)
                lines_html += f'<div class="line-item" title="Linha {i}">{escaped_line}</div>'
        
        more_lines = ""
        if len(lines) > 100:
            more_lines = f'<p style="text-align: center; margin-top: 15px; opacity: 0.7;">... e mais {len(lines) - 100} linhas</p>'
        
        return f"""
        <div class="lines-section">
            <h2>📋 Linhas de Dados ({len([l for l in lines if l.strip()])} linhas)</h2>
            <div class="lines-grid">
                {lines_html}
            </div>
            {more_lines}
        </div>
        """
    
    def _calculate_stats(self, data):
        """
        Calcula estatísticas dos dados.
        """
        lines = data.split('\\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        avg_length = 0
        if non_empty_lines:
            avg_length = round(sum(len(line) for line in non_empty_lines) / len(non_empty_lines), 1)
        
        return {
            'total_chars': len(data),
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'avg_line_length': avg_length
        }
    
    def _get_javascript(self):
        """
        Retorna código JavaScript para interatividade.
        """
        return """
        // Funcionalidade de alternância de tema
        function toggleTheme() {
            const body = document.body;
            if (body.classList.contains('theme-dark')) {
                body.classList.remove('theme-dark');
                body.classList.add('theme-light');
                localStorage.setItem('theme', 'light');
            } else {
                body.classList.remove('theme-light');
                body.classList.add('theme-dark');
                localStorage.setItem('theme', 'dark');
            }
        }
        
        // Carregar tema salvo
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                document.body.className = 'theme-' + savedTheme;
            }
            
            // Adicionar botão de alternância de tema
            const themeButton = document.createElement('button');
            themeButton.className = 'theme-toggle';
            themeButton.innerHTML = '🌓';
            themeButton.title = 'Alternar tema';
            themeButton.onclick = toggleTheme;
            document.body.appendChild(themeButton);
        });
        
        // Copiar texto ao clicar
        document.querySelectorAll('.line-item').forEach(item => {
            item.style.cursor = 'pointer';
            item.addEventListener('click', function() {
                navigator.clipboard.writeText(this.textContent).then(() => {
                    const original = this.style.background;
                    this.style.background = 'rgba(0, 255, 0, 0.3)';
                    setTimeout(() => {
                        this.style.background = original;
                    }, 300);
                });
            });
        });
        """
    
    def _save_html_file(self, output_file, html_content):
        """
        Salva o arquivo HTML.
        """
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                self.log_debug(f"[+] Relatório HTML salvo: {output_file}")
                self.log_debug(f"[*] Tamanho do arquivo: {file_size} bytes")
                
                self.set_result(f"{output_file}; {file_size}")
            else:
                self.log_debug("[x] Falha ao salvar arquivo HTML")
                
        except Exception as e:
            self.log_debug(f"[x] Erro ao salvar HTML: {e}")
    
    def _open_in_browser(self, file_path):
        """
        Abre o arquivo HTML no navegador.
        """
        try:
            import webbrowser
            file_url = f"file://{os.path.abspath(file_path)}"
            webbrowser.open(file_url)
            self.log_debug("[+] Relatório aberto no navegador")
        except Exception as e:
            self.log_debug(f"[!] Não foi possível abrir o navegador: {e}")
