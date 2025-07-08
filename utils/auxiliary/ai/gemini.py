"""
Módulo Google Gemini AI para String-X.

Este módulo fornece integração com a API Gemini AI do Google para processamento
de linguagem natural, geração de texto e outras capacidades de IA.
"""

from core.basemodule import BaseModule
import httpx
import json


class GeminiAI(BaseModule):
    """
    Módulo para interagir com a API Gemini AI do Google.
    
    Este módulo permite enviar prompts para a API Gemini e receber
    respostas geradas para várias tarefas de processamento de texto.
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
            'type': 'ai'
        }
        
        self.options = {
            'api_key': str(),  # Chave API Gemini
            'model': 'gemini-2.0-flash',  # Versão do modelo
            'data': str(),  # O texto do prompt
            'temperature': 0.7,  # Controla aleatoriedade (0.0 a 1.0)
            'max_tokens': 800,  # Máximo de tokens na resposta
            'example': './strx -l prompts.txt -st "echo {STRING}" -module "ai:gemini" -pm',
            'debug': False  # Modo de debug para mostrar informações detalhadas
        }
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/"
    
    def run(self):
        """
        Executa a requisição à API Gemini.
        
        Envia o prompt para a API Gemini e processa a resposta.
        """
        try:
            data = self.options.get('data', '').strip()
            api_key = self.options.get('api_key', '')
            model = self.options.get('model', 'gemini-2.0-flash')
            temperature = float(self.options.get('temperature', 0.7))
            max_tokens = int(self.options.get('max_tokens', 800))
            
            if not data:
                self.set_result("✗ Erro: Nenhum dado de prompt fornecido")
                return
                
            if not api_key:
                self.set_result("✗ Erro: A chave API Gemini é necessária")
                return
            
            result = self._query_gemini(
                prompt=data,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if result:
                self.set_result(result)
                
        except Exception as e:
            self.set_result(f"✗ Erro da API Gemini: {str(e)}")
    
    def _query_gemini(self, prompt: str, api_key: str, model: str, 
                     temperature: float = 0.7, max_tokens: int = 800) -> str:
        """
        Consulta a API Gemini com o prompt fornecido.
        
        Args:
            prompt (str): O texto do prompt a ser enviado ao Gemini
            api_key (str): A chave API para autenticação
            model (str): O modelo Gemini a ser usado
            temperature (float): Controla a aleatoriedade na geração
            max_tokens (int): Número máximo de tokens na resposta
            
        Returns:
            str: O texto de resposta gerado ou mensagem de erro
        """
        try:
            url = f"{self.base_url}{model}:generateContent?key={api_key}"
            
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
            
            with httpx.Client() as client:
                response = client.post(
                    url, 
                    headers=headers, 
                    json=payload, 
                    timeout=30
                )
            
            if response.status_code != 200:
                return f"✗ Erro de API: {response.status_code} - {response.text}"
            
            result = response.json()
            
            # Extrai o texto gerado da resposta
            if 'candidates' in result and len(result['candidates']) > 0:
                if 'content' in result['candidates'][0]:
                    content = result['candidates'][0]['content']
                    if 'parts' in content and len(content['parts']) > 0:
                        return content['parts'][0]['text']
            
            return f"✗ Formato de Resposta da API Inesperado: {json.dumps(result)[:100]}..."
            
        except Exception as e:
            return f"✗ Erro de Requisição: {str(e)}"