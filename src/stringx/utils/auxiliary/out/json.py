"""
Módulo de saída JSON.

Este módulo implementa funcionalidade para salvar resultados em formato JSON
estruturado, útil para integração com outras ferramentas.
"""
import os
import json
import atexit
import threading
from datetime import datetime

from stringx.core.basemodule import BaseModule

# Variáveis globais para armazenamento compartilhado entre instâncias
_COLLECTED_DATA = set()  # Armazena dados únicos
_JSON_LOCK = threading.Lock()  # Lock para sincronização
_INITIALIZED = False  # Flag para indicar se já inicializamos


class JSONOutput(BaseModule):
    """
    Módulo de saída para formato JSON.
    """

    def __init__(self):
        super().__init__()
        global _INITIALIZED

        self.meta = {
            'name': 'JSON Output',
            'author': 'MrCl0wn',
            'version': '2.0',
            'description': 'Salva resultados em formato JSON estruturado',
            'type': 'output',
            'example': ('./strx -l data.txt -st "echo {STRING}" '
                        '-module "out:json" -pm')
        }

        self.options = {
            'data': str(),
            'file': 'output.json',
            'append': True,
            'pretty': True,
            'debug': True,  # Modo de debug para mostrar informações detalhadas
            'retry': 0,     # Número de tentativas de requisição
            'retry_delay': None,  # Atraso entre tentativas de requisição
            'batch_size': 50,  # Número de itens a coletar antes de salvar
        }

        # Inicialização única no processo
        if not _INITIALIZED:
            # Registra uma função para salvar dados na saída do processo
            atexit.register(self._save_all_data)
            _INITIALIZED = True
            self.log_debug("[*] Registered atexit handler for final data save")

    @staticmethod
    def _get_output_filepath():
        """
        Obtém o caminho completo para o arquivo de saída.
        """
        # Determina o caminho base do projeto
        # Assumindo que este arquivo está em utils/auxiliary/out/json.py
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(current_file))))
        output_dir = os.path.join(project_root, 'output')

        # Cria o diretório output se não existir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Constrói o caminho completo do arquivo
        return os.path.join(output_dir, 'output.json')

    def _save_all_data(self):
        """
        Salva todos os dados coletados ao finalizar o programa.
        Esta função será chamada pelo registro atexit.
        """

        with _JSON_LOCK:
            if not _COLLECTED_DATA:
                return

            self.log_debug(f"[+] Final save: saving {len(_COLLECTED_DATA)} items")

            # Converte set para lista para serializar
            unique_data = list(_COLLECTED_DATA)
            file_path = self._get_output_filepath()

            try:
                entries = []
                timestamp = datetime.now().isoformat()

                # Cria as entradas para todos os dados coletados
                for item in unique_data:
                    entry = {
                        'timestamp': timestamp,
                        'data': item,
                        'source': 'string-x'
                    }
                    entries.append(entry)

                # Escreve diretamente no arquivo, sem tentar carregar o arquivo
                # existente
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(entries, f, indent=2, ensure_ascii=False)

                self.log_debug(
                    f"[+] Successfully saved {
                        len(entries)} items to {file_path}")
                # Limpar dados após salvar com sucesso
                _COLLECTED_DATA.clear()

            except Exception as e:
                self.handle_error(e, "Erro ao salvar dados coletados em JSON")

    def run(self):
        """
        Coleta dados para salvar em formato JSON.
        """

        # Pega o dado passado
        data = self.options.get("data", "")
        if not data or not isinstance(data, str):
            return

        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()

        # Limpa o dado
        data = data.strip()
        if not data:
            return

        self.log_debug(
            f"[*] Processing data: {data[:50]}{'...' if len(data) > 50 else ''}")

        # Adiciona ao conjunto global de dados
        with _JSON_LOCK:
            _COLLECTED_DATA.add(data)
            count = len(_COLLECTED_DATA)
            self.log_debug(f"[*] Total collected: {count} unique items")

            # Salva intermediariamente se atingir o limite de batch
            batch_size = int(self.options.get('batch_size', 50))
            if count > 0 and count % batch_size == 0:
                self.log_debug(
                    f"[*] Batch size {batch_size} reached, triggering "
                    f"intermediary save")
                self._save_intermediary_batch()

        return True

    def _save_intermediary_batch(self):
        """
        Salva um lote intermediário de dados durante a execução.
        """

        try:
            # Copia os dados atuais para evitar modificações durante o
            # processamento
            current_data = list(_COLLECTED_DATA)
            file_path = self._get_output_filepath()

            # Cria as entradas para o arquivo JSON
            entries = []
            timestamp = datetime.now().isoformat()

            for item in current_data:
                entry = {
                    'timestamp': timestamp,
                    'data': item,
                    'source': 'string-x'
                }
                entries.append(entry)

            # Escreve no arquivo sem tentar ler o existente para evitar
            # corrupção
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)

            self.log_debug(
                f"[+] Intermediary save: {
                    len(entries)} items to {file_path}")

            # NÃO limpa os dados aqui, apenas no final do programa

            return True

        except Exception as e:
            self.handle_error(e, "Erro ao salvar dados intermediários em JSON")
            return False
