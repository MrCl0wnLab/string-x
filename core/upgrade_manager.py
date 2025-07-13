"""
Sistema de upgrade do String-X usando Git.
"""

# Biblioteca padrão
import os
import sys
import subprocess
from pathlib import Path

# Módulos locais
from core.style_cli import StyleCli

class UpgradeManager:
    def __init__(self):
        self.cli = StyleCli()
        self.repo_url = "https://github.com/MrCl0wnLab/string-x.git"
    
    def _run_command(self, command: str) -> tuple:
        """Executa comando e retorna (sucesso, saída)"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return (result.returncode == 0, result.stdout, result.stderr)
        except Exception as e:
            return (False, "", str(e))
    
    def _is_git_repo(self) -> bool:
        """Verifica se está em um repositório Git"""
        return Path('.git').exists()
    
    def _get_pending_commits(self):
        """Obtém os commits pendentes para download"""
        if not self._is_git_repo():
            return []
        
        # Atualiza as referências remotas
        self._run_command("git fetch origin main")
        
        # Obtém os commits entre HEAD local e origin/main
        success, stdout, _ = self._run_command("git log HEAD..origin/main --pretty=format:'%h - %s (%an, %ar)'")
        if success and stdout:
            return stdout.strip().split('\n')
        return []
    
    def upgrade(self):
        """Executa upgrade usando Git"""
        try:
            if self._is_git_repo():
                # Projeto já é um repositório Git
                self.cli.console.print("[blue]🔄 Verificando atualizações...[/blue]")
                
                # Obter commits pendentes
                pending_commits = self._get_pending_commits()
                
                if not pending_commits or pending_commits[0] == '':
                    self.cli.console.print("[green]✅ Seu código já está atualizado![/green]")
                    return True
                
                # Mostrar commits que serão baixados
                self.cli.console.print("[yellow]🔄 Commits que serão baixados:[/yellow]")
                for commit in pending_commits:
                    if commit:  # Ignora linhas vazias
                        self.cli.console.print(f"[cyan]  ↳ {commit}[/cyan]")
                
                # Confirmar atualização
                self.cli.console.print("[blue]🔄 Atualizando repositório Git...[/blue]")
                
                # Fazer stash das mudanças locais
                self._run_command("git stash")
                
                # Pull das atualizações
                success, _, _ = self._run_command("git pull origin main")
                if success:
                    self.cli.console.print("[green]✅ Código atualizado![/green]")
                else:
                    self.cli.console.print("[yellow]⚠️ Erro no git pull, tentando reset...[/yellow]")
                    self._run_command("git reset --hard origin/main")
                
                # Restaurar mudanças locais se necessário
                self._run_command("git stash pop")
                
            else:
                # Não é um repo Git, fazer clone
                self.cli.console.print("[blue]📥 Clonando repositório...[/blue]")
                self.cli.console.print("[yellow]ℹ️ Clone completo - todos os commits serão baixados[/yellow]")
                
                # Backup dos arquivos importantes
                if Path("output").exists():
                    self._run_command("cp -r output /tmp/strx_output_backup")
                
                # Clone do repositório
                success, _, _ = self._run_command(f"git clone {self.repo_url} /tmp/string-x-new")
                if success:
                    self.cli.console.print("[blue]📦 Aplicando atualização...[/blue]")
                    
                    # Substituir arquivos
                    self._run_command("cp -r /tmp/string-x-new/* .")
                    self._run_command("rm -rf /tmp/string-x-new")
                    
                    # Restaurar backup
                    if Path("/tmp/strx_output_backup").exists():
                        self._run_command("cp -r /tmp/strx_output_backup output")
                        self._run_command("rm -rf /tmp/strx_output_backup")
                else:
                    self.cli.console.print("[red]❌ Erro no clone[/red]")
                    return False
            
            # Permissão executável
            os.chmod("strx", 0o755)
            
            # Atualizar dependências
            self.cli.console.print("[blue]📦 Atualizando dependências...[/blue]")
            success, _, _ = self._run_command(f"{sys.executable} -m pip install -r requirements.txt --quiet")
            if success:
                self.cli.console.print("[green]✅ String-X atualizado com sucesso![/green]")
                self.cli.console.print("[blue]💡 Reinicie o terminal para garantir as mudanças[/blue]")
                return True
            else:
                self.cli.console.print("[yellow]⚠️ Erro ao atualizar dependências[/yellow]")
                return True  # Código foi atualizado mesmo assim
                
        except Exception as e:
            self.cli.console.print(f"[red]❌ Erro: {str(e)}[/red]")
            return False