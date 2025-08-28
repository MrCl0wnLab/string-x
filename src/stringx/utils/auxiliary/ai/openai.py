"""
Módulo OpenAI para String-X.

Este módulo fornece integração com a API OpenAI para processa            self.log_debug(f"[*] Configuração carregada: modelo={model}, temperatura={temperature}, max_tokens={max_tokens}")ento
de linguagem natural, geração de texto e outras capacidades de IA.

A OpenAI oferece modelos avançados como GPT-4 que podem ser utilizados para:
- Análise de texto e extração de informações
- Geração de conteúdo criativo e técnico
- Análise de código e detecção de vulnerabilidades
- Avaliação de ameaças e análise de segurança
- Detecção de engenharia social e phishing
- Resumo e simplificação de textos complexos
- Tradução e adaptação de conteúdo entre idiomas
- Análise de logs e eventos de segurança
"""
# Bibliotecas padrão
import json
from typing import Dict, Any, Optional

# Bibliotecas de terceiros
import httpx
from httpx import HTTPError, RequestError, TimeoutException

# Módulos locais
from stringx.core.basemodule import BaseModule

class OpenAI(BaseModule):
    """
    Módulo para interagir com a API OpenAI.
    
    Esta classe permite enviar prompts para a API OpenAI e receber
    respostas geradas para várias tarefas de processamento de texto,
    incluindo análise de segurança, geração de conteúdo, análise de código
    e detecção de ameaças.
    """
    
    def __init__(self):
        """
        Inicializa o módulo OpenAI.
        """
        super().__init__()
        
        self.meta = {
            'name': 'OpenAI GPT',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Integração com OpenAI GPT para análise de texto, código e ameaças',
            'type': 'ai',
            'example': './strx -l prompts.txt -st "echo {STRING}" -module "ai:openai" -pm'
        }
        
        self.options = {
            'data': None,
            'proxy': None,
            'retry': None,
            'retry_delay': None,
            'api_key': self.setting.STRX_OPENAI_APIKEY,  # Chave API OpenAI
            'model': self.setting.STRX_OPENAI_MODEL,  # Modelo a ser usado (gpt-3.5-turbo, gpt-4, gpt-4-turbo)
            'temperature': self.setting.STRX_OPENAI_TEMPERATURE,  # Controla aleatoriedade (0.0 a 2.0)
            'max_tokens': self.setting.STRX_OPENAI_MAX_TOKENS,  # Máximo de tokens na resposta
            'system_prompt': self.setting.STRX_OPENAI_PROMPT_SYSTEM,  # Prompt do sistema para definir comportamento
            'debug': False,  # Modo de debug para mostrar informações detalhadas
        }
        
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.log_debug("[*] Módulo OpenAI inicializado com configurações padrão")
    
    def run(self) -> None:
        """
        Executa a requisição à API OpenAI.
        
        Este método coordena todo o processo de interação com a API OpenAI,
        incluindo a validação dos parâmetros de entrada, envio do prompt
        e processamento da resposta recebida.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
            
        Raises:
            ValueError: Erro na validação dos parâmetros
            HTTPError: Erro na comunicação com a API
            RequestError: Erro no processamento da requisição
        """
        # Only clear results if auto_clear is enabled (default behavior)
        if self._auto_clear_results:
            self._result[self._get_cls_name()].clear()
        
        try:
            self.log_debug("[*] Iniciando execução do módulo OpenAI")
            
            data = self.options.get('data', '').strip()
            api_key = self.options.get('api_key', '')
            model = self.options.get('model', 'gpt-3.5-turbo')
            temperature = float(self.options.get('temperature', 0.7))
            max_tokens = int(self.options.get('max_tokens', 1000))
            system_prompt = self.options.get('system_prompt', '')
            
            self.log_debug(f"[*] Configuração carregada: modelo={model}, temperatura={temperature}, max_tokens={max_tokens}")
            
            if not data:
                self.log_debug("[x] Erro: prompt vazio - requisição abortada")
                return
                
            if not api_key:
                self.log_debug("[x] Erro: chave API não fornecida - requisição abortada")
                return
            
            self.log_debug(f"[*] Prompt válido recebido com {len(data)} caracteres")
            
            result = self._query_openai(
                prompt=data,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_prompt
            )
            
            if result:
                self.log_debug(f"[+] Resposta do OpenAI processada com sucesso: {len(result)} caracteres")
                self.set_result(result)
            else:
                self.log_debug("[!] Alerta: resposta vazia recebida da API OpenAI")
                
        except ValueError as e:
            self.handle_error(e, "Erro de validação nos parâmetros da requisição")
        except HTTPError as e:
            self.handle_error(e, "Erro HTTP na comunicação com a API OpenAI")
        except Exception as e:
            self.handle_error(e, "Erro inesperado na execução OpenAI")
    
    def _query_openai(self, prompt: str, api_key: str, model: str, 
                     temperature: float = 0.7, max_tokens: int = 1000, 
                     system_prompt: str = '') -> str:
        """
        Consulta a API OpenAI com o prompt fornecido.
        
        Este método envia uma requisição HTTP para a API OpenAI com o prompt
        especificado e parâmetros de configuração, processa a resposta e
        extrai o texto gerado pelo modelo.
        
        Args:
            prompt (str): O texto do prompt a ser enviado ao OpenAI
            api_key (str): A chave API para autenticação
            model (str): O modelo OpenAI a ser usado
            temperature (float): Controla a aleatoriedade na geração (0.0 a 2.0)
            max_tokens (int): Número máximo de tokens na resposta
            system_prompt (str): Prompt do sistema para definir comportamento
            
        Returns:
            str: O texto de resposta gerado ou mensagem de erro
            
        Raises:
            HTTPError: Erro na comunicação com a API
            ValueError: Erro na validação ou formato dos dados
            TimeoutException: Timeout durante a requisição
        """
        try:
            self.log_debug(f"[*] Iniciando consulta à API OpenAI com modelo '{model}'")
            
            # Validar parâmetros
            if not (0.0 <= temperature <= 2.0):
                self.log_debug(f"[X] Parâmetro temperatura inválido: {temperature} (deve estar entre 0.0 e 2.0)")
                raise ValueError("Temperatura deve estar entre 0.0 e 2.0")
                
            if max_tokens <= 0:
                self.log_debug(f"[X] Parâmetro max_tokens inválido: {max_tokens} (deve ser positivo)")
                raise ValueError("max_tokens deve ser um número positivo")
            
            self.log_debug(f"[*] URL da API: {self.base_url}")
            
            # Preparar mensagens
            messages = []
            
            # Adicionar prompt do sistema se fornecido
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
                self.log_debug(f"[*] Prompt do sistema adicionado: {len(system_prompt)} caracteres")
            
            # Adicionar prompt do usuário
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            self.log_debug(f"[*] Payload JSON preparado com prompt de {len(prompt)} caracteres")
            self.log_debug("[*] Iniciando envio da requisição HTTP com timeout de 60 segundos")
            
            with httpx.Client() as client:
                self.log_debug("[*] Conexão cliente HTTP estabelecida")
                response = client.post(
                    self.base_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=60
                )
            
            self.log_debug(f"[*] Resposta da API recebida - Status HTTP: {response.status_code}")
            
            if response.status_code != 200:
                self.log_debug(f"[X] Corpo da resposta de erro: {response.text[:150]}...")
                return
            
            result = response.json()
            self.log_debug("[*] Resposta JSON decodificada com sucesso")
            
            # Extrai o texto gerado da resposta
            if 'choices' in result and len(result['choices']) > 0:
                self.log_debug(f"[*] Encontradas {len(result['choices'])} escolhas na resposta")
                choice = result['choices'][0]
                if 'message' in choice and 'content' in choice['message']:
                    content = choice['message']['content']
                    self.log_debug(f"[+] Texto extraído com sucesso: {len(content)} caracteres")
                    
                    # Adicionar informações de uso se disponíveis
                    usage_info = ""
                    if 'usage' in result:
                        usage = result['usage']
                        prompt_tokens = usage.get('prompt_tokens', 0)
                        completion_tokens = usage.get('completion_tokens', 0)
                        total_tokens = usage.get('total_tokens', 0)
                        usage_info = f"\n\n[Tokens: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total]"
                        self.log_debug(f"[*] Informações de uso: {total_tokens} tokens totais")
                    
                    return content + usage_info
            
            self.log_debug("[X] Erro: estrutura de resposta inesperada ou inválida")
            self.log_debug(f"[*] Estrutura recebida: {json.dumps(result)[:150]}...")
            return f"Formato de Resposta da API Inesperado: {json.dumps(result)[:100]}..."
            
        except HTTPError as e:
            return self.handle_error(e, "Erro HTTP durante a comunicação com a API")
        except TimeoutException as e:
            return self.handle_error(e, "Timeout na requisição após 60 segundos")
        except ValueError as e:
            return self.handle_error(e, "Erro de validação nos parâmetros da requisição")
        except Exception as e:
            return self.handle_error(e, "Erro inesperado no processamento OpenAI")
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        Define um prompt do sistema para configurar o comportamento do modelo.
        
        Args:
            prompt (str): O prompt do sistema que define como o modelo deve se comportar
        """
        self.options['system_prompt'] = prompt
        self.log_debug(f"[*] Prompt do sistema definido: {len(prompt)} caracteres")
    
    def get_available_models(self) -> list:
        """
        Retorna uma lista dos modelos disponíveis.
        
        Returns:
            list: Lista de modelos OpenAI disponíveis
        """
        return [
            'gpt-3.5-turbo',
            'gpt-3.5-turbo-16k',
            'gpt-4',
            'gpt-4-turbo',
            'gpt-4o',
            'gpt-4o-mini'
        ]
