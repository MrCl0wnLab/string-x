"""
Módulo de formatação de saída.

Este módulo contém classes e funções para formatar a saída dos resultados
em diferentes formatos, incluindo texto simples (txt), CSV, JSON e XML.
"""
import uuid
import csv
import json
import io
import re
import xml.etree.ElementTree as ET
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
    def _parse_structured_data(data: Union[List[Any], str, Any]) -> List[Dict[str, Any]]:
        """
        Converte dados em lista estruturada para formatação.
        
        Args:
            data: Dados a serem analisados
            
        Returns:
            List[Dict]: Lista de dicionários estruturados
        """
        structured_data = []
        
        if isinstance(data, list):
            for item in data:
                structured_data.extend(OutputFormatter._parse_structured_data(item))
        elif isinstance(data, str):
            # Dividir por linhas se contiver múltiplos resultados
            lines = data.strip().split('\n') if '\n' in data else [data]
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Tentar detectar padrão "TIPO: VALOR"
                type_value_match = re.match(r'^([A-Z0-9]+):\s*(.+)$', line)
                if type_value_match:
                    structured_data.append({
                        'type': type_value_match.group(1),
                        'value': type_value_match.group(2).strip()
                    })
                else:
                    # Valor simples
                    structured_data.append({
                        'type': 'result',
                        'value': line
                    })
        else:
            # Valor único não-string
            structured_data.append({
                'type': 'result',
                'value': str(data)
            })
            
        return structured_data

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
        Formata os dados como CSV com estrutura melhorada.
        
        Args:
            data: Dados a serem formatados
            columns: Nomes das colunas (padrão: id, timestamp, type, value, module, function)
            module: Nome do módulo usado (opcional)
            function: Nome da função usada (opcional)
            
        Returns:
            str: Dados formatados em CSV
        """
        output = io.StringIO()
        if columns is None:
            columns = ['id', 'timestamp', 'type', 'value', 'module', 'function']
        
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        
        # Converter para dados estruturados
        structured_data = OutputFormatter._parse_structured_data(data)
        timestamp = datetime.now().isoformat()
        
        for item in structured_data:
            row = {
                'id': str(uuid.uuid4())[:8],
                'timestamp': timestamp,
                'type': item.get('type', 'result'),
                'value': item.get('value', ''),
                'module': module,
                'function': function
            }
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def format_json(data: Union[List[Any], str, Any], module: str = "", function: str = "") -> str:
        """
        Formata os dados como JSON estruturado.
        
        Args:
            data: Dados a serem formatados
            module: Nome do módulo usado (opcional)
            function: Nome da função usada (opcional)
            
        Returns:
            str: Dados formatados em JSON
        """
        timestamp = datetime.now().isoformat()
        
        # Converter para dados estruturados
        structured_data = OutputFormatter._parse_structured_data(data)
        
        json_data = []
        for item in structured_data:
            entry = {
                'id': str(uuid.uuid4())[:8],
                'timestamp': timestamp,
                'type': item.get('type', 'result'),
                'value': item.get('value', ''),
                'module': module,
                'function': function
            }
            json_data.append(entry)
        
        # Se apenas um item, retornar objeto único ao invés de array
        if len(json_data) == 1:
            return json.dumps(json_data[0], indent=2, ensure_ascii=False)
        
        return json.dumps(json_data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def format_xml(data: Union[List[Any], str, Any], module: str = "", function: str = "") -> str:
        """
        Formata os dados como XML estruturado.
        
        Args:
            data: Dados a serem formatados
            module: Nome do módulo usado (opcional)
            function: Nome da função usada (opcional)
            
        Returns:
            str: Dados formatados em XML
        """
        # Converter para dados estruturados
        structured_data = OutputFormatter._parse_structured_data(data)
        timestamp = datetime.now().isoformat()
        
        # Criar elemento raiz
        root = ET.Element('stringx_results')
        root.set('timestamp', timestamp)
        if module:
            root.set('module', module)
        if function:
            root.set('function', function)
        
        # Adicionar cada item como elemento
        for item in structured_data:
            result_elem = ET.SubElement(root, 'result')
            result_elem.set('id', str(uuid.uuid4())[:8])
            result_elem.set('type', item.get('type', 'result'))
            result_elem.text = item.get('value', '')
        
        # Converter para string formatada
        rough_string = ET.tostring(root, encoding='unicode')
        
        # Formatar XML com indentação
        try:
            import xml.dom.minidom
            dom = xml.dom.minidom.parseString(rough_string)
            return dom.toprettyxml(indent="  ")
        except:
            # Fallback sem formatação se minidom não estiver disponível
            return rough_string
    
    # Dicionário para mapeamento de formato para método
    formats = {
        'txt': format_txt,
        'csv': format_csv,
        'json': format_json,
        'xml': format_xml
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
    
