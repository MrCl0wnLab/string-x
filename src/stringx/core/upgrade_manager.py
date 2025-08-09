"""
Sistema de upgrade do String-X usando Git.

Este módulo gerencia atualizações automáticas do String-X,
permitindo ao usuário confirmar antes de aplicar as mudanças.
"""

# Biblioteca padrão
import os
import sys
import subprocess
import re
from pathlib import Path
from typing import Tuple, List, Optional

# Módulos locais
from stringx.core.style_cli import StyleCli

class UpgradeManager:
    """
    Gerenciador de atualizações do String-X.
    
    Esta classe é responsável por verificar e aplicar atualizações
    do código-fonte usando Git, com suporte a confirmação do usuário.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de atualizações."""
        self.cli = StyleCli()
        self.repo_url = "https://github.com/MrCl0wnLab/string-x.git"
    
    def _run_command(self, command: str) -> Tuple[bool, str, str]:
        """
        Executa um comando shell de forma segura.
        
        Args:
            command (str): Comando a ser executado
            
        Returns:
            tuple: (sucesso, stdout, stderr)
        """
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return (result.returncode == 0, result.stdout, result.stderr)
        except Exception as e:
            return (False, "", str(e))
    
    def _ask_confirmation(self, message: str = "Continuar?") -> bool:
        """
        Solicita confirmação do usuário.
        
        Args:
            message (str): Mensagem a ser exibida
            
        Returns:
            bool: True se confirmado, False caso contrário
        """
        try:
            response = input(f"\n{message} [N/y]: ").lower().strip()
            return response == 'y'
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return False
    
    def _is_git_repo(self) -> bool:
        """Verifica se está em um repositório Git"""
        return Path('.git').exists()
    
    def _get_pending_commits(self) -> List[str]:
        """
        Obtém os commits pendentes para download.
        
        Returns:
            List[str]: Lista de commits pendentes formatados
        """
        if not self._is_git_repo():
            return []
        
        # Atualiza as referências remotas
        self._run_command("git fetch origin main")
        
        # Obtém os commits entre HEAD local e origin/main
        success, stdout, _ = self._run_command("git log HEAD..origin/main --pretty=format:'%h - %s (%an, %ar)'")
        if success and stdout:
            commits = stdout.strip().split('\n')
            return [commit for commit in commits if commit]  # Remove linhas vazias
        return []
    
    def _format_commit_message(self, commit: str) -> str:
        """
        Formata uma mensagem de commit para exibição com destaque para tipos comuns.
        
        Args:
            commit (str): Mensagem de commit original
            
        Returns:
            str: Mensagem formatada com destaque
        """
        # Destacar tipos de commit comuns
        commit_types = {
            'feat': '[bright_green]FEATURE[/bright_green]',
            'fix': '[bright_red]FIX[/bright_red]',
            'docs': '[bright_blue]DOCS[/bright_blue]',
            'style': '[magenta]STYLE[/magenta]',
            'refactor': '[yellow]REFACTOR[/yellow]',
            'perf': '[bright_cyan]PERF[/bright_cyan]',
            'test': '[bright_magenta]TEST[/bright_magenta]',
            'chore': '[dim]CHORE[/dim]',
            'security': '[bright_red]SECURITY[/bright_red]'
        }
        
        # Tenta extrair o tipo do commit da mensagem
        match = re.search(r'([a-z0-9]{7}) - ((?:feat|fix|docs|style|refactor|perf|test|chore|security)(?:\([^)]+\))?:)?\s*(.*)', commit)
        if match:
            hash_commit, type_commit, message = match.groups()
            
            if type_commit:
                # Extrair apenas o tipo sem os parênteses
                commit_type = type_commit.split('(')[0].strip(':')
                if commit_type in commit_types:
                    return f"[cyan]{hash_commit}[/cyan] {commit_types[commit_type]} {message}"
                    
        # Se não conseguiu extrair ou não é um tipo conhecido, retorna o original
        return f"[cyan]  ↳[/cyan] {commit}"
    
    def upgrade(self) -> bool:
        """
        Executa o processo de upgrade usando Git com confirmação do usuário.
        
        Returns:
            bool: True se o upgrade foi bem-sucedido, False caso contrário
        """
        try:
            self.cli.console.print("\n[bold cyan]╔════════════════════════════╗[/bold cyan]")
            self.cli.console.print("[bold cyan]║[/bold cyan]  [bold white]String-X Upgrade Manager[/bold white]  [bold cyan]║[/bold cyan]")
            self.cli.console.print("[bold cyan]╚════════════════════════════╝[/bold cyan]\n")
            
            self.cli.console.print("[blue]Verificando atualizações...[/blue]")
            
            if self._is_git_repo():
                # Projeto já é um repositório Git
                # Obter commits pendentes
                pending_commits = self._get_pending_commits()
                
                if not pending_commits:
                    self.cli.console.print("[green]Seu código já está atualizado![/green]")
                    return True
                
                # Mostrar commits que serão baixados
                num_commits = len(pending_commits)
                self.cli.console.print(f"[yellow]{num_commits} novo(s) commit(s) disponíveis:[/yellow]")
                
                # Exibir commits formatados
                for commit in pending_commits:
                    self.cli.console.print(self._format_commit_message(commit))
                
                # Solicitar confirmação do usuário
                self.cli.console.print("\n[yellow]Arquivos modificados serão preservados quando possível.[/yellow]")
                if not self._ask_confirmation("Deseja atualizar para a última versão?"):
                    self.cli.console.print("[blue]Atualização cancelada pelo usuário.[/blue]")
                    return False
                
                self.cli.console.print("[blue]Atualizando repositório Git...[/blue]")
                
                # Fazer stash das mudanças locais (salva modificações locais)
                has_changes, _, _ = self._run_command("git diff-index --quiet HEAD -- || echo 'has-changes'")
                if has_changes:
                    self.cli.console.print("[yellow]Salvando suas modificações locais...[/yellow]")
                    self._run_command("git stash save 'Auto-stash before strx upgrade'")
                
                # Pull das atualizações
                success, _, stderr = self._run_command("git pull origin main")
                if success:
                    self.cli.console.print("[green]Código atualizado com sucesso![/green]")
                else:
                    self.cli.console.print("[yellow]Erro no git pull, tentando método alternativo...[/yellow]")
                    
                    if "local changes" in stderr:
                        # Conflito com alterações locais
                        self.cli.console.print("[yellow]Conflito detectado com alterações locais.[/yellow]")
                        
                        if self._ask_confirmation("Forçar atualização? (suas alterações locais serão perdidas)"):
                            self._run_command("git reset --hard origin/main")
                            self.cli.console.print("[green]Código atualizado forçadamente![/green]")
                        else:
                            self.cli.console.print("[blue]Atualização cancelada para preservar alterações locais.[/blue]")
                            return False
                    else:
                        # Outro tipo de erro, tentar reset
                        self._run_command("git reset --hard origin/main")
                
                # Restaurar mudanças locais do stash se houver
                if has_changes:
                    self.cli.console.print("[yellow]Restaurando suas modificações locais...[/yellow]")
                    stash_result, _, _ = self._run_command("git stash pop")
                    if not stash_result:
                        self.cli.console.print("[yellow]Houve conflitos ao restaurar suas mudanças.[/yellow]")
                        self.cli.console.print("[yellow]Suas alterações foram preservadas no git stash.[/yellow]")
                
            else:
                # Não é um repo Git, fazer clone
                self.cli.console.print("[blue]📥 Não é um repositório Git.[/blue]")
                self.cli.console.print("[yellow]Clone completo será executado - todos os commits serão baixados[/yellow]")
                
                # Solicitar confirmação do usuário
                if not self._ask_confirmation("Deseja baixar a versão mais recente do String-X?"):
                    self.cli.console.print("[blue]Atualização cancelada pelo usuário.[/blue]")
                    return False
                
                # Backup dos arquivos importantes
                important_dirs = ["output", "config"]
                backup_created = False
                
                for dir_name in important_dirs:
                    if Path(dir_name).exists():
                        self.cli.console.print(f"[yellow]Fazendo backup da pasta '{dir_name}'...[/yellow]")
                        self._run_command(f"cp -r {dir_name} /tmp/strx_{dir_name}_backup")
                        backup_created = True
                
                # Clone do repositório
                self.cli.console.print("[blue]📥 Clonando repositório...[/blue]")
                success, _, _ = self._run_command(f"git clone {self.repo_url} /tmp/string-x-new")
                if success:
                    self.cli.console.print("[blue]📦 Aplicando atualização...[/blue]")
                    
                    # Substituir arquivos
                    self._run_command("cp -r /tmp/string-x-new/* .")
                    self._run_command("rm -rf /tmp/string-x-new")
                    
                    # Restaurar backups
                    if backup_created:
                        self.cli.console.print("[yellow]Restaurando arquivos e configurações...[/yellow]")
                        for dir_name in important_dirs:
                            if Path(f"/tmp/strx_{dir_name}_backup").exists():
                                self._run_command(f"cp -r /tmp/strx_{dir_name}_backup/* {dir_name}/")
                                self._run_command(f"rm -rf /tmp/strx_{dir_name}_backup")
                else:
                    self.cli.console.print("[red]❌ Erro no clone[/red]")
                    return False
            
            # Tornar o script executável
            os.chmod("strx", 0o755)
            
            # Perguntar se deve atualizar dependências
            if self._ask_confirmation("Deseja atualizar as dependências Python?"):
                self.cli.console.print("[blue]📦 Atualizando dependências...[/blue]")
                success, _, _ = self._run_command(f"{sys.executable} -m pip install -r requirements.txt")
                if success:
                    self.cli.console.print("[green]Dependências atualizadas com sucesso![/green]")
                else:
                    self.cli.console.print("[yellow]Erro ao atualizar dependências[/yellow]")
            
            self.cli.console.print("\n[green bold]String-X atualizado com sucesso![/green bold]")
            self.cli.console.print("[blue]💡 Reinicie o terminal para garantir as mudanças[/blue]")
            return True
                
        except Exception as e:
            self.cli.console.print(f"[red]❌ Erro: {str(e)}[/red]")
            return False