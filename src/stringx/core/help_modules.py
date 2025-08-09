#!/usr/bin/env python3
"""
Módulo para exibição de informações tabulares no String-X.

Este módulo implementa funções para exibir os módulos e seus exemplos
em formato de tabela usando a biblioteca Rich.
"""

# Biblioteca padrão
import os
import sys
import importlib
import importlib.util
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED, SIMPLE, MINIMAL, DOUBLE

# Módulos locais
from stringx.core.style_cli import StyleCli


CLI = StyleCli()

# Obtém o diretório base do projeto (raiz do string-x)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Constante para o caminho base dos módulos (caminho absoluto)
BASE_MODULES_PATH = os.path.join(ROOT_DIR, 'utils/auxiliary')

def discover_module_types():
    """Descobre dinamicamente os tipos de módulos disponíveis."""
    modules_dirs = {}
    
    if os.path.exists(BASE_MODULES_PATH):
        for module_type in os.listdir(BASE_MODULES_PATH):
            module_path = os.path.join(BASE_MODULES_PATH, module_type)
            
            if os.path.isdir(module_path):
                # Verificar se a pasta contém módulos Python
                has_modules = any(f.endswith('.py') for f in os.listdir(module_path) 
                                 if f != '__init__.py')
                
                if has_modules and os.path.exists(os.path.join(module_path, '__init__.py')):
                    try:
                        # Importar dinamicamente o __init__.py para obter o MODULE_TYPE
                        module_name = f"stringx.utils.auxiliary.{module_type}"
                        module = importlib.import_module(module_name)
                        
                        # Obter o valor de MODULE_TYPE
                        if hasattr(module, 'MODULE_TYPE'):
                            module_desc = module.MODULE_TYPE.capitalize()
                            display_name = f"{module_type.upper()} ({module_desc})"
                            modules_dirs[display_name] = os.path.join(BASE_MODULES_PATH, module_type)
                        else:
                            # Se não encontrar MODULE_TYPE, usa o nome da pasta
                            display_name = f"{module_type.upper()}"
                            modules_dirs[display_name] = f'{BASE_MODULES_PATH}/{module_type}/'
                    except Exception as e:
                        # Em caso de erro, usa apenas o nome da pasta
                        display_name = f"{module_type.upper()}"
                        modules_dirs[display_name] = f'{BASE_MODULES_PATH}/{module_type}/'
    
    return modules_dirs


def load_module_class(file_path, module_name):
    """Carrega uma classe de módulo a partir de um arquivo."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Buscar a classe que herda de BaseModule
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (hasattr(attr, '__bases__') and 
                any('BaseModule' in str(base) for base in attr.__bases__)):
                return attr()
        return None
    except Exception as e:
        CLI.console.print(f"Erro ao carregar {module_name}: {e}")
        return None


def show_module_categories():
    """Exibe categorias de módulos em formato de tabela."""
    modules_dirs = discover_module_types()
    
    table = Table(title="📁 Module Categories", box=ROUNDED,  title_justify="left")
    table.add_column("Category", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Path", style="yellow")
    table.add_column("Modules", style="magenta")
    
    for category, dir_path in modules_dirs.items():
        if os.path.exists(dir_path):
            # Extrair o código da categoria (EXT, CLC, etc.)
            type_code = category.split(' ')[0]
            
            # Extrair o tipo (extractor, collector, etc.)
            if '(' in category and ')' in category:
                type_name = category.split('(')[1].split(')')[0]
            else:
                type_name = '-'
                
            # Contar módulos
            module_count = len([f for f in os.listdir(dir_path) 
                               if f.endswith('.py') and f != '__init__.py'])
            
            table.add_row(type_code, type_name, dir_path, str(module_count))
        
    CLI.console.print(table)


def show_module_examples():
    """Mostra exemplos de uso de todos os módulos em formato de tabela."""
    modules_dirs = discover_module_types()
    
    CLI.console.print(Panel("🔧 STRING-X - EXEMPLOS DE USO DOS MÓDULOS", 
                    style="bold", expand=False))
    
    for category, dir_path in modules_dirs.items():
        if not os.path.exists(dir_path):
            continue
            
        py_files = [f for f in os.listdir(dir_path) if f.endswith('.py') and f != '__init__.py']
        
        if not py_files:
            continue
            
        # Criar tabela para esta categoria
        table = Table(title=f"📁 {category}", box=ROUNDED, expand=False, title_justify="left")
        table.add_column("Module", style="cyan bold")
        table.add_column("Description", style="green")
        table.add_column("Example", style="yellow", overflow="fold")
        
        for py_file in sorted(py_files):
            module_path = os.path.join(dir_path, py_file)
            module_name = py_file[:-3]
            
            instance = load_module_class(module_path, module_name)
            if instance:
                meta = getattr(instance, 'meta', {})
                # Primeiro tenta obter o exemplo de meta, se não existir procura em options para compatibilidade
                example = meta.get('example', instance.options.get('example', 'No example available'))
                description = meta.get('description', 'No description')
                
                table.add_row(module_name, description, example)
        
        CLI.console.print(table)
        CLI.console.print()


def show_specific_example(module_type, module_name):
    """Mostra exemplo específico de um módulo em formato de tabela."""
    modules_dirs = discover_module_types()
    module_path = None
    
    # Primeiro tenta encontrar pelo código do tipo (ext, clc, etc.)
    module_type_lower = module_type.lower()
    direct_path = f"{BASE_MODULES_PATH}/{module_type_lower}/{module_name}.py"
    
    if os.path.exists(direct_path):
        module_path = direct_path
        module_type_folder = module_type_lower
    else:
        # Se não encontrar diretamente, procura em todas as categorias
        for category, path in modules_dirs.items():
            if module_type.upper() in category:
                possible_path = f"{path}{module_name}.py"
                if os.path.exists(possible_path):
                    module_path = possible_path
                    module_type_folder = os.path.basename(os.path.dirname(path))
                    break
    
    if not module_path or not os.path.exists(module_path):
        CLI.console.print(Panel(f"❌ Module {module_type}:{module_name} not found!", 
                        style="bold white on red"))
        return
    
    instance = load_module_class(module_path, module_name)
    if instance:
        # Obter o nome da categoria
        category_info = None
        for cat, path in modules_dirs.items():
            if module_type_folder in path.lower():
                category_info = cat
                break
        
        if not category_info:
            category_info = module_type.upper()
        
        meta = getattr(instance, 'meta', {})
        # Primeiro tenta obter o exemplo de meta, se não existir procura em options para compatibilidade
        example = meta.get('example', instance.options.get('example', 'No example available'))
        
        # Tabela de informações do módulo
        info_table = Table(title=f"🔧 {category_info} - {module_name}", box=ROUNDED)
        info_table.add_column("Attribute", style="cyan")
        info_table.add_column("Value", style="green")
        
        info_table.add_row("Description", meta.get('description', 'No description'))
        info_table.add_row("Author", meta.get('author', 'Not specified'))
        info_table.add_row("Version", meta.get('version', 'Not specified'))
        
        CLI.console.print(info_table)
        
        # Tabela de exemplo de uso
        example_table = Table(title="💻 Usage example", box=ROUNDED)
        example_table.add_column("Command", style="yellow", overflow="fold")
        example_table.add_row(example)
        
        CLI.console.print(example_table)
        
        # Tabela de opções do módulo
        options_table = Table(title="📋 Available options", box=ROUNDED)
        options_table.add_column("Opção", style="cyan")
        options_table.add_column("Valor", style="green")
        
        for key, value in instance.options.items():
            if key != 'example':
                options_table.add_row(key, str(value))
                
        CLI.console.print(options_table)


def show_helper_functions():
    """Lista todas as funções disponíveis no módulo helper/functions.py em formato de tabela."""
    # Usa o caminho absoluto para o arquivo de funções auxiliares
    functions_path = os.path.join(ROOT_DIR, 'utils/helper/functions.py')
    
    if not os.path.exists(functions_path):
        CLI.console.print(Panel(f"❌ Helper functions file not found: {functions_path}", 
                        style="bold white on red"))
        return
        
    # Tabela para exibir as funções
    table = Table(title="🛠️  Helper Functions", box=ROUNDED, expand=False, title_justify="left")
    table.add_column("Function", style="cyan bold")
    table.add_column("Description", style="green")
    table.add_column("Arguments", style="yellow")
    
    # Ler o arquivo para extrair as funções
    with open(functions_path, 'r') as file:
        content = file.read()
        
    # Extrair blocos de funções (def + docstring)
    function_blocks = []
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Detectar início de definição de função (excluindo __init__)
        if line.startswith('def ') and not '__init__' in line:
            function_name = line.split('def ')[1].split('(')[0].strip()
            function_args = line.split('(')[1].split(')')[0].strip()
            
            # Extrair docstring (se existir)
            description = "No description"
            
            # Avançar para próxima linha não vazia após a definição da função
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
                
            if j < len(lines):
                current_line = lines[j].strip()
                
                # Verificar se a próxima linha é uma docstring
                if current_line.startswith('"""'):
                    docstring_text = []
                    
                    # Docstring de linha única
                    if current_line.endswith('"""') and len(current_line) > 6:  # Mais do que apenas """
                        docstring_text = [current_line[3:-3]]  # Remove as aspas
                    else:
                        # Multi-line docstring
                        # Adicionar primeira linha sem as aspas iniciais
                        first_line = current_line[3:] if current_line.startswith('"""') else current_line
                        docstring_text.append(first_line)
                        
                        # Continuar lendo até encontrar o fechamento da docstring
                        j += 1
                        found_end = False
                        
                        while j < len(lines) and not found_end:
                            if '"""' in lines[j]:
                                # Encontrou o fechamento da docstring
                                closing_line = lines[j].split('"""')[0].strip()
                                if closing_line:  # Se há texto antes do fechamento
                                    docstring_text.append(closing_line)
                                found_end = True
                            else:
                                docstring_text.append(lines[j].strip())
                            j += 1
                    
                    # Juntar todas as linhas e extrair a primeira frase
                    full_docstring = ' '.join([line for line in docstring_text if line])
                    if full_docstring:
                        # Extrair a primeira frase (terminando com ponto)
                        parts = full_docstring.split('.')
                        if parts:
                            description = parts[0].strip()
                            if not description.endswith('.'):
                                description += '.'
            
            # Adicionar à lista de funções
            function_blocks.append({
                'name': function_name,
                'args': function_args,
                'description': description
            })
        
        i += 1
    
    # Adicionar funções à tabela
    for func in sorted(function_blocks, key=lambda x: x['name']):
        table.add_row(func['name'], func['description'], func['args'])
    
    CLI.console.print(Panel("📋 STRING-X - HELPER FUNCTIONS", 
                     style="bold", expand=False))
    CLI.console.print(table)