#!/usr/bin/env python3
"""
Demonstração do uso do campo 'example' nos módulos String-X.

Este script mostra como acessar e utilizar os exemplos de uso
que foram adicionados em todos os módulos.
"""

import os
import sys
import importlib.util
from core.style_cli import StyleCli

CLI = StyleCli()

# Diretórios dos módulos
MODULES_DIRS = {
        'EXT (Extractors)':     'utils/auxiliary/ext/',
        'CLC (Collectors)':     'utils/auxiliary/clc/', 
        'OUT (Output)':         'utils/auxiliary/out/',
        'CON (Connections)':    'utils/auxiliary/con/'
    }


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
    
    for category, dir_path in MODULES_DIRS.items():
        if category:
            CLI.console.print(f"📁 {category}")

def show_module_examples():
    """Mostra exemplos de uso de todos os módulos."""
    


    CLI.console.print("🔧 STRING-X - EXEMPLOS DE USO DOS MÓDULOS")
    CLI.console.print("=" * 60)
    CLI.console.print()
    
    for category, dir_path in MODULES_DIRS.items():
        CLI.console.print(f"📁 {category}")
        CLI.console.print("-" * 40)
        
        if os.path.exists(dir_path):
            py_files = [f for f in os.listdir(dir_path) if f.endswith('.py') and f != '__init__.py']
            
            for py_file in sorted(py_files):
                module_path = os.path.join(dir_path, py_file)
                module_name = py_file[:-3]
                
                instance = load_module_class(module_path, module_name)
                if instance:
                    example = instance.options.get('example', 'Sem exemplo disponível')
                    meta = getattr(instance, 'meta', {})
                    description = meta.get('description', 'Sem descrição')
                    
                    CLI.console.print(f"🔹 {module_name}")
                    CLI.console.print(f"   📝 {description}")
                    CLI.console.print(f"   💻 {example}")
                    CLI.console.print()
        
        CLI.console.print()

def show_specific_example(module_type, module_name):
    """Mostra exemplo específico de um módulo."""
    
    module_path = f"utils/auxiliary/{module_type}/{module_name}.py"
    
    if not os.path.exists(module_path):
        CLI.console.print(f"❌ Módulo {module_type}:{module_name} não encontrado!")
        return
    
    instance = load_module_class(module_path, module_name)
    if instance:
        example = instance.options.get('example', 'Sem exemplo disponível')
        meta = getattr(instance, 'meta', {})
        
        CLI.console.print(f"🔧 EXEMPLO DE USO - {module_type.upper()}:{module_name}")
        CLI.console.print("=" * 50)
        CLI.console.print(f"📝 Descrição: {meta.get('description', 'Sem descrição')}")
        CLI.console.print(f"👤 Autor: {meta.get('author', 'Não informado')}")
        CLI.console.print(f"🔢 Versão: {meta.get('version', 'Não informada')}")
        CLI.console.print()
        CLI.console.print("💻 Exemplo de uso:")
        CLI.console.print(f"   {example}")
        CLI.console.print()
        CLI.console.print("📋 Opções disponíveis:")
        for key, value in instance.options.items():
            if key != 'example':
                CLI.console.print(f"   • {key}: {value}")

