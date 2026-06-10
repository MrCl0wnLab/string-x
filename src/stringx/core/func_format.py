
"""
Módulo de formatação de funções.

Este módulo contém a classe FuncFormat responsável por detectar e processar
funções especiais dentro de strings de comando, permitindo a execução de
transformações dinâmicas nos dados.
"""
import re
from stringx.utils.helper.functions import Funcs


class FuncFormat:
    """
    Classe para formatação e processamento de funções em strings.
    
    Esta classe detecta padrões de função dentro de strings de comando e
    executa as funções correspondentes, substituindo os padrões pelos
    resultados das execuções.
    
    Attributes:
        _func_name_list (list): Lista de nomes de funções disponíveis
        is_func (bool): Flag indicando se funções foram detectadas
    """
    def __init__(self):
        """
        Inicializa FuncFormat com lista de funções disponíveis.
        """
        self._func_name_list: list = [func for func in dir(Funcs) if func.startswith('_') is False] 
        self.is_func: bool = False

    def _find_func(self, func_name: str, value: str) -> str:
        """
        Encontra e executa uma função específica.
        
        Args:
            func_name (str): Nome da função a ser executada
            value (str): Valor a ser passado como parâmetro
            
        Returns:
            str: Resultado da execução da função ou string vazia
        """
        if func_name and value:
            for attribute in self._func_name_list:
                # atributo é uma string que representa o nome do função / method
                if (attribute == str(func_name.split("(")[0])):
                    attribute_value = getattr(Funcs, attribute)
                    return attribute_value(value)
        return str()
                
    def _detect_func(self, text: str, func_name: str) -> list[str]:
        """
        Detecta padrões de função em um texto.
        
        Args:
            text (str): Texto onde buscar padrões de função
            func_name (str): Nome da função a ser detectada
            
        Returns:
            list[str]: Lista de tuplas com função e parâmetros ou None
        """
        if text and func_name:
            # procurando padrão de função na string {text}
            findall = re.findall(rf'({func_name}\((.*?)\))',text,re.MULTILINE)
            if findall:
                return list(set(findall))
            self.is_func = False
            return None
    
    def _find_innermost_call(self, text: str, func_set: set) -> tuple | None:
        """
        Localiza a chamada de função mais interna (à esquerda) no texto.

        Faz matching balanceado de parênteses: encontra o primeiro `)`, casa-o
        com seu `(` correspondente e lê o identificador imediatamente antes.
        Como é o primeiro `)`, o argumento não contém parênteses — portanto é
        sempre a chamada mais interna, permitindo avaliação de dentro para fora
        (ex.: em `md5(get(url))`, resolve `get(url)` antes de `md5(...)`).

        Args:
            text (str): Texto a inspecionar
            func_set (set): Nomes de funções conhecidas

        Returns:
            tuple | None: (início, fim, nome, arg) da chamada conhecida, onde
                `text[início:fim]` é o trecho `nome(arg)`; None se não houver.
        """
        i = 0
        n = len(text)
        while i < n:
            if text[i] == ')':
                # Caminha para trás até a '(' correspondente
                depth = 1
                j = i - 1
                while j >= 0:
                    if text[j] == ')':
                        depth += 1
                    elif text[j] == '(':
                        depth -= 1
                        if depth == 0:
                            break
                    j -= 1
                if j < 0:
                    # Parêntese desbalanceado: nada a processar
                    return None
                # Extrai o identificador imediatamente antes da '('
                k = j - 1
                while k >= 0 and (text[k].isalnum() or text[k] == '_'):
                    k -= 1
                name = text[k + 1:j]
                arg = text[j + 1:i]
                if name in func_set and arg:
                    return (k + 1, i + 1, name, arg)
                # Grupo de parênteses que não é função conhecida: segue adiante
                i += 1
                continue
            i += 1
        return None

    def func_format(self, cmd_str: str) -> str:
        """
        Processa todas as funções detectadas em uma string de comando.

        Avalia as funções de dentro para fora usando matching balanceado de
        parênteses, suportando argumentos com parênteses aninhados
        (ex.: `md5(get(http://x))`). A substituição é posicional, garantindo
        ordem determinística entre execuções.

        Args:
            cmd_str (str): String de comando contendo padrões de função

        Returns:
            str: String processada com funções substituídas por seus resultados
        """
        if cmd_str:
            func_set = set(self._func_name_list)
            # Itera resolvendo a chamada mais interna a cada passo, até não
            # restar nenhuma função conhecida. O teto evita loops patológicos.
            max_iterations = len(cmd_str) + 1
            for _ in range(max_iterations):
                call = self._find_innermost_call(cmd_str, func_set)
                if not call:
                    break
                start, end, name, arg = call
                self.is_func = True
                result = str(self._find_func(f"{name}({arg})", arg))
                cmd_str = cmd_str[:start] + result + cmd_str[end:]
            if cmd_str:
                return cmd_str
        return str()
    

