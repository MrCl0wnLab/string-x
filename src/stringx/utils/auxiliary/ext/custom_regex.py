"""
Módulo de extração com regex customizada.

Este módulo implementa funcionalidade para extrair dados usando
padrões regex personalizados definidos pelo usuário.
"""
import re
from stringx.core.format import Format
from stringx.core.basemodule import BaseModule

class CustomRegexExtractor(BaseModule):
    """
    Módulo de extração com regex customizada.
    
    Esta classe permite extrair dados usando padrões regex personalizados
    com suporte a flags, grupos e validações customizadas.
    """
    
    def __init__(self):
        """
        Inicializa o módulo de extração regex customizada.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Custom Regex Extractor',
             "author": "MrCl0wn",
            'version': '1.0',
            'description': 'Extração com padrões regex personalizados',
            'type': 'extraction',
            'example': './strx -l data.txt -st "\\\\d{3}-\\\\d{2}-\\\\d{4}" -module "ext:custom_regex" -pm'
        }
        
        self.options = {
            'data': str(),
            'pattern': '',              # Padrão regex principal
            'flags': 'i',              # Flags regex (i=ignorecase, m=multiline, s=dotall)
            'group': 0,                # Grupo a extrair (0=match completo)
            'max_matches': 1000,       # Máximo de matches
            'unique_only': True,       # Apenas resultados únicos
            'min_length': 0,          # Tamanho mínimo do match
            'max_length': 0,          # Tamanho máximo do match (0=sem limite)
            'validate_pattern': '',    # Padrão adicional para validação
            'exclude_pattern': '',     # Padrão para exclusão
            'case_sensitive': False,   # Sensível a maiúsculas
            'multiline': False,        # Modo multiline
            'dotall': False,          # . corresponde a quebras de linha
            'debug': False
        }
    
    def run(self):
        """
        Executa extração com regex customizada.
        """
        try:
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            
            target_value = Format.clear_value(self.options.get('data', ''))
            pattern = self.options.get('pattern', '').strip()
            
            if not target_value:
                self.log_debug("[x] Dados não fornecidos")
                return
            
            if not pattern:
                self.log_debug("[x] Padrão regex não fornecido")
                return
            
            self.log_debug("[*] Iniciando extração com regex customizada")
            self.log_debug(f"[*] Processando {len(target_value)} caracteres de dados")
            self.log_debug(f"[*] Padrão regex: {pattern}")
            
            # Configurar flags
            regex_flags = self._build_flags()
            self.log_debug(f"[*] Flags aplicadas: {self._describe_flags(regex_flags)}")
            
            # Compilar regex
            try:
                compiled_pattern = re.compile(pattern, regex_flags)
            except re.error as e:
                self.log_debug(f"[x] Erro na compilação do regex: {e}")
                return
            
            # Executar busca
            matches = self._extract_matches(compiled_pattern, target_value)
            
            if not matches:
                self.log_debug("[!] Nenhum match encontrado")
                return
            
            self.log_debug(f"[+] Encontrados {len(matches)} matches iniciais")
            
            # Aplicar filtros
            filtered_matches = self._apply_filters(matches)
            
            if not filtered_matches:
                self.log_debug("[!] Nenhum match passou pelos filtros")
                return
            
            self.log_debug(f"[+] {len(filtered_matches)} matches após filtros")
            
            # Processar e formatar resultados
            self._process_results(filtered_matches)
            
        except Exception as e:
            self.handle_error(e, "Erro na extração com regex customizada")
    
    def _build_flags(self):
        """
        Constrói flags do regex baseado nas opções.
        """
        flags = 0
        
        # Flags por string
        flag_string = self.options.get('flags', '').lower()
        if 'i' in flag_string or not self.options.get('case_sensitive', False):
            flags |= re.IGNORECASE
        if 'm' in flag_string or self.options.get('multiline', False):
            flags |= re.MULTILINE
        if 's' in flag_string or self.options.get('dotall', False):
            flags |= re.DOTALL
        
        return flags
    
    def _describe_flags(self, flags):
        """
        Descreve as flags aplicadas.
        """
        descriptions = []
        if flags & re.IGNORECASE:
            descriptions.append("IGNORECASE")
        if flags & re.MULTILINE:
            descriptions.append("MULTILINE")
        if flags & re.DOTALL:
            descriptions.append("DOTALL")
        
        return ", ".join(descriptions) if descriptions else "None"
    
    def _extract_matches(self, pattern, text):
        """
        Extrai matches do texto usando o padrão.
        """
        group = self.options.get('group', 0)
        max_matches = self.options.get('max_matches', 1000)
        
        matches = []
        
        try:
            # Usar finditer para ter controle sobre o número de matches
            for i, match in enumerate(pattern.finditer(text)):
                if i >= max_matches:
                    self.log_debug(f"[!] Limite de {max_matches} matches atingido")
                    break
                
                # Extrair grupo específico
                if isinstance(group, int):
                    if group < len(match.groups()) + 1:
                        extracted = match.group(group)
                    else:
                        self.log_debug(f"[!] Grupo {group} não existe no match")
                        continue
                else:
                    # Grupo nomeado
                    try:
                        extracted = match.group(group)
                    except IndexError:
                        self.log_debug(f"[!] Grupo nomeado '{group}' não encontrado")
                        continue
                
                if extracted:
                    matches.append(extracted)
                    
        except Exception as e:
            self.log_debug(f"[x] Erro durante extração: {e}")
        
        return matches
    
    def _apply_filters(self, matches):
        """
        Aplica filtros aos matches encontrados.
        """
        filtered = matches.copy()
        
        # Filtro de tamanho mínimo
        min_length = self.options.get('min_length', 0)
        if min_length > 0:
            before_count = len(filtered)
            filtered = [m for m in filtered if len(m) >= min_length]
            if len(filtered) != before_count:
                self.log_debug(f"[*] Filtro min_length: {before_count} -> {len(filtered)}")
        
        # Filtro de tamanho máximo
        max_length = self.options.get('max_length', 0)
        if max_length > 0:
            before_count = len(filtered)
            filtered = [m for m in filtered if len(m) <= max_length]
            if len(filtered) != before_count:
                self.log_debug(f"[*] Filtro max_length: {before_count} -> {len(filtered)}")
        
        # Padrão de validação adicional
        validate_pattern = self.options.get('validate_pattern', '').strip()
        if validate_pattern:
            try:
                validate_regex = re.compile(validate_pattern)
                before_count = len(filtered)
                filtered = [m for m in filtered if validate_regex.search(m)]
                if len(filtered) != before_count:
                    self.log_debug(f"[*] Filtro validação: {before_count} -> {len(filtered)}")
            except re.error as e:
                self.log_debug(f"[!] Erro no padrão de validação: {e}")
        
        # Padrão de exclusão
        exclude_pattern = self.options.get('exclude_pattern', '').strip()
        if exclude_pattern:
            try:
                exclude_regex = re.compile(exclude_pattern)
                before_count = len(filtered)
                filtered = [m for m in filtered if not exclude_regex.search(m)]
                if len(filtered) != before_count:
                    self.log_debug(f"[*] Filtro exclusão: {before_count} -> {len(filtered)}")
            except re.error as e:
                self.log_debug(f"[!] Erro no padrão de exclusão: {e}")
        
        # Remover duplicatas se solicitado
        if self.options.get('unique_only', True):
            before_count = len(filtered)
            # Preservar ordem
            seen = set()
            unique_filtered = []
            for item in filtered:
                if item not in seen:
                    seen.add(item)
                    unique_filtered.append(item)
            filtered = unique_filtered
            if len(filtered) != before_count:
                self.log_debug(f"[*] Remoção de duplicatas: {before_count} -> {len(filtered)}")
        
        return filtered
    
    def _process_results(self, matches):
        """
        Processa e formata os resultados finais.
        """
        if not matches:
            return
        
        # Log de alguns exemplos
        self.log_debug("[+] Exemplos de matches encontrados:")
        for i, match in enumerate(matches[:5]):  # Mostrar até 5 exemplos
            self.log_debug(f"   [*] {i+1}. {match}")
        
        if len(matches) > 5:
            self.log_debug(f"   [*] ... e mais {len(matches) - 5} matches")
        
        # Preparar resultado final
        result = f"Custom Regex Extraction Results\\n"
        result += f"Pattern: {self.options.get('pattern', '')}\\n"
        result += f"Total matches: {len(matches)}\\n\\n"
        
        # Adicionar todos os matches
        for i, match in enumerate(matches, 1):
            result += f"{i}. {match}\\n"
        
        self.set_result(result)
