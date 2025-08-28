"""
Módulo Google Gemini AI para String-X.

Este módulo fornece integração com a API Gemini AI do Google para processamento
de linguagem natural, geração de texto e outras capacidades de IA.

O Google Gemini é um modelo de linguagem avançado que pode ser utilizado para:
- Geração de conteúdo e texto criativo
- Análise e extração de informações de dados não estruturados
- Respostas a perguntas baseadas em conhecimento geral
- Resumo e simplificação de textos complexos
- Tradução e adaptação de conteúdo entre idiomas
- Conversão entre diferentes formatos de dados e textos
"""
# Bibliotecas padrão
import json
from typing import Dict, Any, Optional

# Bibliotecas de terceiros
import httpx
from httpx import HTTPError, RequestError, TimeoutException

# Módulos locais
from stringx.core.basemodule import BaseModule

class GeminiAI(BaseModule):
    """
    Módulo para interagir com a API Gemini AI do Google.
    
    Esta classe permite enviar prompts para a API Google Gemini e receber
    respostas geradas para várias tarefas de processamento de texto,
    incluindo geração de conteúdo, análise de dados e resposta a perguntas.
    """
    
    def __init__(self):
        """
        Inicializa o módulo Gemini AI.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Gemini AI',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Prompt para usar os modelos Google Gemini AI',
            'type': 'ai',
            'example': './strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm'
        }
        
        self.options = {
            'api_key': self.setting.STRX_GEMINI_APIKEY,  # Chave API Gemini
            'model': self.setting.STRX_GEMINI_MODEL,  # Versão do modelo
            'temperature': self.setting.STRX_GEMINI_TEMPERATURE,  # Controla aleatoriedade (0.0 a 1.0)
            'max_tokens': self.setting.STRX_GEMINI_MAX_TOKENS,  # Máximo de tokens na resposta
            'debug': False,  # Modo de debug para mostrar informações detalhadas
            'data': str(),  # O texto do prompt
        }
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/"
        self.log_debug("[*] Módulo Gemini AI inicializado com configurações padrão")
    
    def run(self) -> None:
        """
        Executa a requisição à API Gemini.
        
        Este método coordena todo o processo de interação com a API Gemini,
        incluindo a validação dos parâmetros de entrada, envio do prompt
        e processamento da resposta recebida.
        
        Returns:
            None: Os resultados são armazenados internamente através do método set_result
            
        Raises:
            ValueError: Erro na validação dos parâmetros
            HTTPError: Erro na comunicação com a API
            RequestError: Erro no processamento da requisição
        """

        # Limpar resultados anteriores para evitar acúmulo
        self._result[self._get_cls_name()].clear()
        
        try:
            self.log_debug("[*] Iniciando execução do módulo Gemini AI")
            
            data = self.options.get('data', '').strip()
            api_key = self.options.get('api_key', '')
            model = self.options.get('model', 'gemini-2.0-flash')
            temperature = float(self.options.get('temperature', 0.7))
            max_tokens = int(self.options.get('max_tokens', 800))
            
            self.log_debug(f"[*] Configuração carregada: modelo={model}, temperatura={temperature}, max_tokens={max_tokens}")
            
            if not data:
                self.log_debug("[x] Erro: prompt vazio - requisição abortada")
                return
                
            if not api_key:
                self.log_debug("[x] Erro: chave API não fornecida - requisição abortada")
                return
            
            self.log_debug(f"[*] Prompt válido recebido com {len(data)} caracteres")
            
            result = self._query_gemini(
                prompt=data,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if result:
                self.log_debug(f"[+] Resposta do Gemini processada com sucesso: {len(result)} caracteres")
                self.set_result(result)
            else:
                self.log_debug("[!] Alerta: resposta vazia recebida da API Gemini")
                
        except ValueError as e:
            self.handle_error(e, "Erro de validação nos parâmetros da requisição")
        except HTTPError as e:
            self.handle_error(e, "Erro HTTP na comunicação com a API Gemini")
        except Exception as e:
            self.handle_error(e, "Erro inesperado na execução Gemini AI")
    
    def _query_gemini(self, prompt: str, api_key: str, model: str, 
                     temperature: float = 0.7, max_tokens: int = 800) -> str:
        """
        Consulta a API Gemini com o prompt fornecido.
        
        Este método envia uma requisição HTTP para a API Gemini com o prompt
        especificado e parâmetros de configuração, processa a resposta e
        extrai o texto gerado pelo modelo.
        
        Args:
            prompt (str): O texto do prompt a ser enviado ao Gemini
            api_key (str): A chave API para autenticação
            model (str): O modelo Gemini a ser usado
            temperature (float): Controla a aleatoriedade na geração (0.0 a 1.0)
            max_tokens (int): Número máximo de tokens na resposta
            
        Returns:
            str: O texto de resposta gerado ou mensagem de erro
            
        Raises:
            HTTPError: Erro na comunicação com a API
            ValueError: Erro na validação ou formato dos dados
            TimeoutException: Timeout durante a requisição
        """
        try:
            self.log_debug(f"[*] Iniciando consulta à API Gemini com modelo '{model}'")
            
            # Validar parâmetros
            if not (0.0 <= temperature <= 1.0):
                self.log_debug(f"[!] Parâmetro temperatura inválido: {temperature} (deve estar entre 0.0 e 1.0)")
                raise ValueError("Temperatura deve estar entre 0.0 e 1.0")
                
            if max_tokens <= 0:
                self.log_debug(f"[!] Parâmetro max_tokens inválido: {max_tokens} (deve ser positivo)")
                raise ValueError("max_tokens deve ser um número positivo")
            
            url = f"{self.base_url}{model}:generateContent?key={api_key}"
            self.log_debug(f"[*] URL da API configurada: {self.base_url}{model}:generateContent")
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            self.log_debug(f"[*] Payload JSON preparado com prompt de {len(prompt)} caracteres")
            self.log_debug("[*] Iniciando envio da requisição HTTP com timeout de 30 segundos")
            
            with httpx.Client() as client:
                self.log_debug("[+] Conexão cliente HTTP estabelecida")
                response = client.post(
                    url, 
                    headers=headers, 
                    json=payload, 
                    timeout=30
                )
            
            self.log_debug(f"[*] Resposta da API recebida - Status HTTP: {response.status_code}")
            
            if response.status_code != 200:
                return self.log_debug(f"[x] Corpo da resposta de erro: {response.text[:150]}...")
            
            result = response.json()
            self.log_debug("[+] Resposta JSON decodificada com sucesso")
            
            # Extrai o texto gerado da resposta
            if 'candidates' in result and len(result['candidates']) > 0:
                self.log_debug(f"[+] Encontrados {len(result['candidates'])} candidatos na resposta")
                if 'content' in result['candidates'][0]:
                    content = result['candidates'][0]['content']
                    if 'parts' in content and len(content['parts']) > 0:
                        self.log_debug(f"[+] Texto extraído com sucesso: {len(content['parts'][0]['text'])} caracteres")
                        return content['parts'][0]['text']
            
            self.log_debug("[x] Erro: estrutura de resposta inesperada ou inválida")
            self.log_debug(f"Estrutura recebida: {json.dumps(result)[:150]}...")
            return self.log_debug(f"Corpo da resposta de erro: {response.text[:150]}...")
            
        except HTTPError as e:
            self.handle_error(e, "Erro HTTP durante a comunicação com a API Gemini")
            return ""
        except TimeoutException as e:
            self.handle_error(e, "Timeout na requisição após 30 segundos")
            return ""
        except ValueError as e:
            self.handle_error(e, "Erro de validação nos parâmetros da requisição")
            return ""
        except Exception as e:
            self.handle_error(e, "Erro inesperado no processamento Gemini AI")
            return ""