"""
Módulo de formatação de saída.

Este módulo contém classes e funções para formatar a saída dos resultados
em diferentes formatos, incluindo texto simples (txt), CSV e JSON.
"""
import uuid
import csv
import json
import io
from datetime import datetime
from typing import Any, Dict, List, Union, Optional


class OutputFormatter:
    """
    Classe para formatar a saída em diferentes formatos.

    Esta classe fornece métodos estáticos para converter resultados em
    formatos específicos como texto simples, CSV, ou JSON.
    
    Attributes:
        formats (dict): Dicionário com os formatadores disponíveis
    """
    
    @staticmethod
    def format_txt(data: Union[List[Any], str, Any], module: str = "", function: str = "") -> str:
        """
        Formata os dados como texto simples.
        
        Args:
            data: Dados a serem formatados (string, lista ou outro tipo)
            module: Nome do módulo usado (opcional)
            function: Nome da função usada (opcional)
            
        Returns:
            str: Dados formatados como texto simples
        """
        if isinstance(data, list):
            return '\n'.join(str(item) for item in data)
        return str(data)
    
    @staticmethod
    def format_csv(data: Union[List[Any], str, Any], 
                   columns: Optional[List[str]] = None,
                   module: str = "",
                   function: str = "") -> str:
        """
        Formata os dados como CSV.
        
        Args:
            data: Dados a serem formatados
            columns: Nomes das colunas (padrão: id, data, value, module, function)
            module: Nome do módulo usado (opcional)
            function: Nome da função usada (opcional)
            
        Returns:
            str: Dados formatados em CSV
        """
        output = io.StringIO()
        if columns is None:
            columns = ['id', 'data', 'value', 'module', 'function']
        
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        
        if isinstance(data, list):
            for i, item in enumerate(data):
                row = {
                    'id': str(uuid.uuid4())[:8],
                    'data': datetime.now().isoformat(),
                    'value': str(item),
                    'module': module,
                    'function': function
                }
                writer.writerow(row)
        else:
            row = {
                'id': str(uuid.uuid4())[:8],
                'data': datetime.now().isoformat(),
                'value': str(data),
                'module': module,
                'function': function
            }
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def format_json(data: Union[List[Any], str, Any], module: str = "", function: str = "") -> str:
        """
        Formata os dados como JSON.
        
        Args:
            data: Dados a serem formatados
            module: Nome do módulo usado (opcional)
            function: Nome da função usada (opcional)
            
        Returns:
            str: Dados formatados em JSON
        """
        timestamp = datetime.now().isoformat()
        
        if isinstance(data, list):
            json_data = []
            for i, item in enumerate(data):
                entry = {
                    'id': str(uuid.uuid4())[:8],
                    'data': timestamp,
                    'value': str(item),
                    'module': module,
                    'function': function
                }
                json_data.append(entry)
        else:
            json_data = {
                'id': str(uuid.uuid4())[:8],
                'data': timestamp,
                'value': str(data),
                'module': module,
                'function': function
            }
        
        return json.dumps(json_data, indent=2, ensure_ascii=False)
    
    # Dicionário para mapeamento de formato para método
    formats = {
        'txt': format_txt,
        'csv': format_csv,
        'json': format_json
    }
    
    @classmethod
    def format(cls, format_name: str, data: Any, module: str = "", function: str = "", **kwargs) -> str:
        """
        Formata dados no formato especificado.
        
        Args:
            format_name: Nome do formato (txt, csv, json)
            data: Dados a serem formatados
            module: Nome do módulo usado (opcional)
            function: Nome da função usada (opcional)
            **kwargs: Argumentos adicionais para o formatador
            
        Returns:
            str: Dados formatados
        
        Raises:
            ValueError: Se o formato não for suportado
        """
        if format_name not in cls.formats:
            raise ValueError(f"Formato não suportado: {format_name}")
        
        formatter = cls.formats[format_name]
        return formatter.__func__(data, module=module, function=function, **kwargs)
    
    @staticmethod
    def format_output(data, output_format="txt", include_rich=False):
        """
        Formata dados para o formato de saída especificado.
        
        Args:
            data: Dados a serem formatados
            output_format: Formato desejado (txt, json, csv)
            include_rich: Se deve incluir formatação Rich/ANSI
            
        Returns:
            str: Dados formatados
        """
        if not include_rich:
            # Remover formatação Rich/ANSI dos dados
            if isinstance(data, list):
                data = [OutputFormatter._strip_formatting(item) if isinstance(item, str) else item for item in data]
            elif isinstance(data, str):
                data = OutputFormatter._strip_formatting(data)
        
        if output_format == "json":
            return json.dumps(data, indent=2, ensure_ascii=False)
        elif output_format == "csv":
            output = io.StringIO()
            if isinstance(data, list) and data and isinstance(data[0], dict):
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            elif isinstance(data, list):
                writer = csv.writer(output)
                for item in data:
                    writer.writerow([item])
            return output.getvalue()
        else:  # txt
            if isinstance(data, list):
                return "\n".join(str(item) for item in data)
            return str(data)

    @staticmethod
    def _strip_formatting(text):
        """Remove códigos de formatação Rich/ANSI."""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
