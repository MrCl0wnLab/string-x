"""
Módulo de execução de código Python para String-X.

Este módulo fornece funcionalidade para executar código Python dinamicamente
dentro do contexto do String-X, com acesso a todas as funções e módulos
do sistema, usando o placeholder {STRING} para substituição dinâmica.
"""

import os
import re
import sys
import traceback
from io import StringIO
from typing import Any, Dict, Optional, Union
from contextlib import redirect_stdout, redirect_stderr

from stringx.core.logger import logger
from stringx.utils.helper.functions import Funcs
from stringx.core.format import Format
from stringx.config import setting


class PythonExecutor:
    """
    Classe responsável pela execução segura de código Python no contexto String-X.
    
    Fornece capacidade de executar código Python com acesso controlado ao
    namespace do String-X, incluindo funções helper e módulos auxiliares.
    """
    
    def __init__(self):
        """
        Inicializa o executor Python com configurações de segurança.
        """
        self.namespace = self._create_safe_namespace()
        self.output_buffer = StringIO()
        self.error_buffer = StringIO()
        
    def _create_safe_namespace(self) -> Dict[str, Any]:
        """
        Cria um namespace seguro para execução de código Python.
        
        Returns:
            Dict[str, Any]: Namespace com acesso a funções e módulos String-X
        """
        # Import safe modules
        import json
        import datetime
        
        # Create base namespace with String-X functions
        namespace = {
            '__builtins__': {
                # Safe built-ins only
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'print': print,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'sorted': sorted,
                'reversed': reversed,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                'round': round,
                're': re,
                'json': json,
                'datetime': datetime,
                'type': type,
                'isinstance': isinstance,
            }
        }
        
        # Add String-X functions from Funcs class
        for func_name in dir(Funcs):
            if not func_name.startswith('_') and callable(getattr(Funcs, func_name)):
                namespace[func_name] = getattr(Funcs, func_name)
        
        # Add format functions
        namespace['Format'] = Format
        
        # Add modules to top-level namespace as well
        namespace['json'] = json
        namespace['datetime'] = datetime
            
        return namespace
    
    def execute_code(self, code: str, target_value: str) -> Optional[str]:
        """
        Executa código Python com substituição do placeholder {STRING}.
        
        Args:
            code (str): Código Python a ser executado
            target_value (str): Valor para substituir {STRING}
            
        Returns:
            Optional[str]: Resultado da execução ou None se houver erro
        """
        if not code:
            return None
            
        try:
            # Substitute {STRING} placeholder with properly quoted value
            quoted_value = repr(target_value)
            processed_code = re.sub(r'\{[sS][tT][rR][iI][nN][gG]\}', quoted_value, code)
            logger.verbose(f"[!] PYTHON CODE SUBSTITUTION: {code} -> {processed_code}")
            
            # Add target value to namespace
            execution_namespace = self.namespace.copy()
            execution_namespace['STRING'] = target_value
            execution_namespace['target'] = target_value
            execution_namespace['result'] = None
            
            # Reset output buffers
            self.output_buffer = StringIO()
            self.error_buffer = StringIO()
            
            # Execute code with output capture
            with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
                exec(processed_code, execution_namespace)
            
            # Get output
            stdout_output = self.output_buffer.getvalue()
            stderr_output = self.error_buffer.getvalue()
            
            # Check for explicit result variable
            if 'result' in execution_namespace and execution_namespace['result'] is not None:
                return str(execution_namespace['result'])
            
            # Return stdout if available
            if stdout_output.strip():
                return stdout_output.strip()
                
            # Log stderr if present
            if stderr_output.strip():
                logger.debug(f"Python stderr: {stderr_output.strip()}")
                
            return None
            
        except Exception as e:
            error_msg = f"Python execution error: {str(e)}"
            logger.error(error_msg)
            logger.debug(f"Python traceback: {traceback.format_exc()}")
            return f"ERROR: {str(e)}"
    
    def execute_file(self, file_path: str, target_value: str) -> Optional[str]:
        """
        Executa código Python de um arquivo.
        
        Args:
            file_path (str): Caminho para arquivo Python
            target_value (str): Valor para substituir {STRING}
            
        Returns:
            Optional[str]: Resultado da execução ou None se houver erro
        """
        if not file_path or not os.path.isfile(file_path):
            logger.error(f"Arquivo Python não encontrado: {file_path}")
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            logger.verbose(f"[!] EXECUTING PYTHON FILE: {file_path}")
            return self.execute_code(code_content, target_value)
            
        except Exception as e:
            error_msg = f"Erro ao ler arquivo Python {file_path}: {str(e)}"
            logger.error(error_msg)
            return f"ERROR: {str(e)}"
    
    def validate_code_safety(self, code: str) -> tuple[bool, str]:
        """
        Valida se código Python é seguro para execução.
        
        Args:
            code (str): Código Python a ser validado
            
        Returns:
            tuple[bool, str]: (is_safe, reason)
        """
        if not code:
            return False, "Empty code"
            
        # Dangerous patterns in Python code
        dangerous_patterns = [
            r'import\s+os',
            r'import\s+sys',
            r'import\s+subprocess',
            r'from\s+os\s+import',
            r'from\s+sys\s+import', 
            r'from\s+subprocess\s+import',
            r'__import__\s*\(',
            r'eval\s*\(',
            r'exec\s*\(',
            r'compile\s*\(',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'vars\s*\(',
            r'dir\s*\(',
            r'getattr\s*\(',
            r'setattr\s*\(',
            r'delattr\s*\(',
            r'hasattr\s*\(',
            r'\.read\s*\(',
            r'\.write\s*\(',
            r'\.system\s*\(',
            r'\.popen\s*\(',
            r'\.call\s*\(',
            r'\.run\s*\(',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False, f"Dangerous pattern detected: {pattern}"
                
        return True, "Code appears safe"