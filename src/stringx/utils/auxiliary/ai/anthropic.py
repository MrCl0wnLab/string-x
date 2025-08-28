"""
Módulo Anthropic Claude AI para String-X.

Este módulo fornece integração com a API Anthropic Claude para processamento
de linguagem natural, geração de texto e análise de dados.

O Anthropic Claude é um assistente de IA avançado que pode ser utilizado para:
- Análise de texto e extração de informações
- Análise de código e detecção de vulnerabilidades
- Avaliação de ameaças e análise de segurança
- Detecção de engenharia social e phishing
- Geração de conteúdo criativo e técnico
- Resumo e simplificação de textos complexos
- Tradução e adaptação de conteúdo entre idiomas
- Análise de logs e eventos de segurança
- Conversão entre diferentes formatos de dados
"""
# Bibliotecas padrão
import json
from typing import Dict, Any, Optional

# Bibliotecas de terceiros
import httpx
from httpx import HTTPError, RequestError, TimeoutException

# Módulos locais
from stringx.core.basemodule import BaseModule

class AnthropicAI(BaseModule):
    """
    Módulo para interagir com a API Anthropic Claude.
    
    Esta classe permite enviar prompts para a API Anthropic Claude e receber
    respostas geradas para várias tarefas de processamento de texto,
    incluindo análise de segurança, geração de conteúdo, análise de código
    e detecção de ameaças.
    """
    
    def __init__(self):
        """
        Inicializa o módulo Anthropic Claude.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Anthropic Claude AI',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Integração com Anthropic Claude para análise de texto, código e ameaças',
            'type': 'ai',
            'example': './strx -l prompts.txt -st "echo {STRING}" -module "ai:anthropic" -pm'
        }
        
        self.options = {
            'data': None,
            'proxy': None,
            'retry': None,
            'retry_delay': None,
            'api_key': self.setting.STRX_ANTHROPIC_APIKEY,  # Chave API Anthropic
            'model': self.setting.STRX_ANTHROPIC_MODEL,  # Modelo Claude (claude-3-5-sonnet, claude-3-opus, etc.)
            'temperature': self.setting.STRX_ANTHROPIC_TEMPERATURE,  # Controla aleatoriedade (0.0 a 1.0)
            'max_tokens': self.setting.STRX_ANTHROPIC_MAX_TOKENS,  # Máximo de tokens na resposta
            'system_prompt': self.setting.STRX_ANTHROPIC_PROMPT_SYSTEM,  # Prompt do sistema para definir comportamento
            'debug': False,  # Modo de debug para mostrar informações detalhadas
        }
        
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.log_debug("[*] Módulo Anthropic Claude inicializado com configurações padrão")
    
    def run(self) -> None:
        """
        Executa a requisição à API Anthropic Claude.
        
        Este método coordena todo o processo de interação com a API Anthropic,
        incluindo a validação dos parâmetros de entrada, envio do prompt
        e processamento da resposta recebida.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
            
        Raises:
            ValueError: Erro na validação dos parâmetros
            HTTPError: Erro na comunicação com a API
            RequestError: Erro no processamento da requisição
        """
        try:
            self.log_debug("[*] Iniciando execução do módulo Anthropic Claude")
            
            data = self.options.get('data', '').strip()
            api_key = self.options.get('api_key', '')
            model = self.options.get('model', 'claude-3-5-sonnet-20241022')
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
            
            result = self._query_anthropic(
                prompt=data,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_prompt
            )
            
            if result:
                self.log_debug(f"[+] Resposta do Claude processada com sucesso: {len(result)} caracteres")
                self.set_result(result)
            else:
                self.log_debug("[!] Alerta: resposta vazia recebida da API Claude")
                
        except ValueError as e:
            self.handle_error(e, "Erro de validação nos parâmetros da requisição")
        except HTTPError as e:
            self.handle_error(e, "Erro HTTP na comunicação com a API Claude")
        except Exception as e:
            self.handle_error(e, "Erro inesperado na execução Anthropic Claude")
    
    def _query_anthropic(self, prompt: str, api_key: str, model: str, 
                        temperature: float = 0.7, max_tokens: int = 1000, 
                        system_prompt: str = '') -> str:
        """
        Consulta a API Anthropic Claude com o prompt fornecido.
        
        Este método envia uma requisição HTTP para a API Anthropic com o prompt
        especificado e parâmetros de configuração, processa a resposta e
        extrai o texto gerado pelo modelo.
        
        Args:
            prompt (str): O texto do prompt a ser enviado ao Claude
            api_key (str): A chave API para autenticação
            model (str): O modelo Claude a ser usado
            temperature (float): Controla a aleatoriedade na geração (0.0 a 1.0)
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
            self.log_debug(f"[*] Iniciando consulta à API Claude com modelo '{model}'")
            
            # Validar parâmetros
            if not (0.0 <= temperature <= 1.0):
                self.log_debug(f"[X] Parâmetro temperatura inválido: {temperature} (deve estar entre 0.0 e 1.0)")
                raise ValueError("Temperatura deve estar entre 0.0 e 1.0")
                
            if max_tokens <= 0:
                self.log_debug(f"[X] Parâmetro max_tokens inválido: {max_tokens} (deve ser positivo)")
                raise ValueError("max_tokens deve ser um número positivo")
            
            self.log_debug(f"[*] URL da API: {self.base_url}")
            
            # Preparar payload
            payload = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Adicionar prompt do sistema se fornecido
            if system_prompt:
                payload["system"] = system_prompt
                self.log_debug(f"[*] Prompt do sistema adicionado: {len(system_prompt)} caracteres")
            
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
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
                return f"Erro na API Claude: {response.status_code} - {response.text[:100]}"
            
            result = response.json()
            self.log_debug("[*] Resposta JSON decodificada com sucesso")
            
            # Extrai o texto gerado da resposta
            if 'content' in result and len(result['content']) > 0:
                self.log_debug(f"[*] Encontrados {len(result['content'])} blocos de conteúdo na resposta")
                
                # Claude retorna uma lista de content blocks
                content_parts = []
                for content_block in result['content']:
                    if content_block.get('type') == 'text' and 'text' in content_block:
                        content_parts.append(content_block['text'])
                
                if content_parts:
                    full_content = '\n'.join(content_parts)
                    self.log_debug(f"[+] Texto extraído com sucesso: {len(full_content)} caracteres")
                    
                    # Adicionar informações de uso se disponíveis
                    usage_info = ""
                    if 'usage' in result:
                        usage = result['usage']
                        input_tokens = usage.get('input_tokens', 0)
                        output_tokens = usage.get('output_tokens', 0)
                        total_tokens = input_tokens + output_tokens
                        usage_info = f"\n\n[Tokens: {input_tokens} input + {output_tokens} output = {total_tokens} total]"
                        self.log_debug(f"[*] Informações de uso: {total_tokens} tokens totais")
                    
                    return full_content + usage_info
            
            self.log_debug("[X] Erro: estrutura de resposta inesperada ou inválida")
            self.log_debug(f"[*] Estrutura recebida: {json.dumps(result)[:150]}...")
            return f"Formato de Resposta da API Inesperado: {json.dumps(result)[:100]}..."
            
        except HTTPError as e:
            self.handle_error(e, "Erro HTTP durante a comunicação com a API Claude")
            return ""
        except TimeoutException as e:
            self.handle_error(e, "Timeout na requisição após 60 segundos")
            return ""
        except ValueError as e:
            self.handle_error(e, "Erro de validação nos parâmetros da requisição")
            return ""
        except Exception as e:
            self.handle_error(e, "Erro inesperado no processamento Claude")
            return ""
    
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
            list: Lista de modelos Claude disponíveis
        """
        return [
            'claude-3-5-sonnet-20241022',
            'claude-3-5-sonnet-20240620',
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307'
        ]