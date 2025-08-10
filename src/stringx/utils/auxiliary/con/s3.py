"""
Módulo de conexão para Amazon S3.

Este módulo implementa funcionalidade para upload e download de arquivos
no Amazon S3 (Simple Storage Service), permitindo armazenamento em nuvem
escalável e durável dos dados processados pelo String-X.

O Amazon S3 é um serviço de armazenamento de objetos que oferece:
- Escalabilidade ilimitada
- Alta durabilidade (99.999999999%)
- Controle de acesso granular
- Versionamento de objetos
- Criptografia em trânsito e em repouso
- Integração com outros serviços AWS
"""
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from io import StringIO

from stringx.core.basemodule import BaseModule
from stringx.core.format import Format

class S3Connector(BaseModule):
    """
    Módulo de conexão para Amazon S3.
    
    Esta classe permite upload e download de dados para/do Amazon S3,
    oferecendo armazenamento em nuvem confiável e escalável.
    """
    
    def __init__(self) -> None:
        """
        Inicializa o módulo de conexão S3.
        """
        super().__init__()
        
        self.meta = {
            'name': 'Amazon S3 Connector',
            'author': 'MrCl0wn',
            'version': '1.0',
            'description': 'Upload e download de dados para Amazon S3',
            'type': 'connection',
            'example': './strx -l data.txt -st "echo {STRING}" -module "con:s3" -pm'
        }
        
        self.options = {
            'data': str(),  # Dados para upload ou chave do objeto para download
            'access_key': self.setting.STRX_S3_ACCESS_KEY,     # AWS Access Key ID
            'secret_key': self.setting.STRX_S3_SECRET_KEY,     # AWS Secret Access Key
            'bucket_name': self.setting.STRX_S3_BUCKET_NAME,   # Nome do bucket S3
            'region': self.setting.STRX_S3_REGION,             # Região AWS
            'endpoint_url': self.setting.STRX_S3_ENDPOINT_URL, # URL customizada (para S3-compatible)
            'use_ssl': self.setting.STRX_S3_USE_SSL,           # Usar SSL/TLS
            'timeout': self.setting.STRX_S3_TIMEOUT,           # Timeout da operação
            'operation': 'upload',     # Operação: 'upload', 'download', 'list'
            'object_key': str(),       # Chave do objeto no S3 (path/filename)
            'local_file': str(),       # Arquivo local para upload/download
            'content_type': 'text/plain',  # Content-Type do objeto
            'acl': 'private',          # ACL do objeto (private, public-read, etc.)
            'metadata': str(),         # Metadados adicionais (JSON string)
            'prefix': str(),           # Prefixo para listagem de objetos
            'max_keys': 100,           # Máximo de objetos para listar
            'debug': False,            # Modo de debug
            'retry': 0,                # Número de tentativas
            'retry_delay': None,       # Atraso entre tentativas
        }

    def _get_s3_client(self):
        """
        Cria e retorna um cliente S3 configurado.
        
        Returns:
            boto3.client: Cliente S3 configurado
            
        Raises:
            ImportError: Se boto3 não estiver instalado
            ValueError: Se as credenciais não forem fornecidas
        """
        try:
            import boto3
            from botocore.config import Config
        except ImportError:
            raise ImportError("boto3 não está instalado. Execute: pip install boto3")
        
        access_key = self.options.get('access_key', '').strip()
        secret_key = self.options.get('secret_key', '').strip()
        
        if not access_key or not secret_key:
            raise ValueError("Access Key e Secret Key são obrigatórios")
        
        # Configuração do cliente
        config = Config(
            region_name=self.options.get('region', 'us-east-1'),
            connect_timeout=self.options.get('timeout', 30),
            read_timeout=self.options.get('timeout', 30),
            retries={'max_attempts': max(1, self.options.get('retry', 0) + 1)}
        )
        
        # Parâmetros de conexão
        client_params = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'config': config,
            'use_ssl': self.options.get('use_ssl', True)
        }
        
        # URL customizada para S3-compatible services
        endpoint_url = self.options.get('endpoint_url', '').strip()
        if endpoint_url:
            client_params['endpoint_url'] = endpoint_url
        
        return boto3.client('s3', **client_params)

    def _upload_data(self, s3_client, data: str) -> str:
        """
        Faz upload de dados para o S3.
        
        Args:
            s3_client: Cliente S3 configurado
            data: Dados para upload
            
        Returns:
            str: Mensagem de resultado
        """
        bucket_name = self.options.get('bucket_name', '').strip()
        if not bucket_name:
            raise ValueError("Nome do bucket é obrigatório")
        
        # Gerar chave do objeto se não fornecida
        object_key = self.options.get('object_key', '').strip()
        if not object_key:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_key = f"string-x/{timestamp}.txt"
        
        # Metadados adicionais
        extra_args = {
            'ContentType': self.options.get('content_type', 'text/plain'),
            'ACL': self.options.get('acl', 'private')
        }
        
        # Adicionar metadados customizados
        metadata_str = self.options.get('metadata', '').strip()
        if metadata_str:
            try:
                metadata = json.loads(metadata_str)
                if isinstance(metadata, dict):
                    extra_args['Metadata'] = {k: str(v) for k, v in metadata.items()}
            except json.JSONDecodeError:
                self.log_debug(f"[x] Metadados inválidos (JSON): {metadata_str}")
        
        # Upload usando StringIO para dados em texto
        data_stream = StringIO(data)
        s3_client.upload_fileobj(data_stream, bucket_name, object_key, ExtraArgs=extra_args)
        
        return f"✓ Upload realizado: s3://{bucket_name}/{object_key}"

    def _download_data(self, s3_client) -> str:
        """
        Faz download de dados do S3.
        
        Args:
            s3_client: Cliente S3 configurado
            
        Returns:
            str: Conteúdo do objeto ou mensagem de resultado
        """
        bucket_name = self.options.get('bucket_name', '').strip()
        object_key = self.options.get('object_key', '').strip()
        
        if not bucket_name or not object_key:
            raise ValueError("Nome do bucket e chave do objeto são obrigatórios para download")
        
        local_file = self.options.get('local_file', '').strip()
        
        if local_file:
            # Download para arquivo local
            s3_client.download_file(bucket_name, object_key, local_file)
            return f"✓ Download realizado: s3://{bucket_name}/{object_key} -> {local_file}"
        else:
            # Download para memória
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read().decode('utf-8')
            return content

    def _list_objects(self, s3_client) -> str:
        """
        Lista objetos no bucket S3.
        
        Args:
            s3_client: Cliente S3 configurado
            
        Returns:
            str: Lista de objetos formatada
        """
        bucket_name = self.options.get('bucket_name', '').strip()
        if not bucket_name:
            raise ValueError("Nome do bucket é obrigatório")
        
        # Parâmetros de listagem
        list_params = {
            'Bucket': bucket_name,
            'MaxKeys': self.options.get('max_keys', 100)
        }
        
        prefix = self.options.get('prefix', '').strip()
        if prefix:
            list_params['Prefix'] = prefix
        
        response = s3_client.list_objects_v2(**list_params)
        
        if 'Contents' not in response:
            return f"Nenhum objeto encontrado no bucket: {bucket_name}"
        
        objects = response['Contents']
        result_lines = [f"Objetos no bucket '{bucket_name}':\n"]
        
        for obj in objects:
            size = obj['Size']
            key = obj['Key']
            modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
            result_lines.append(f"  {key} ({size} bytes) - {modified}")
        
        return "\n".join(result_lines)

    def run(self) -> None:
        """
        Executa a operação S3 especificada.
        
        Suporta as seguintes operações:
        - upload: Envia dados para o S3
        - download: Baixa dados do S3
        - list: Lista objetos no bucket
        """
        try:
            # Limpar resultados anteriores
            self._result[self._get_cls_name()].clear()
            
            operation = self.options.get('operation', 'upload').lower()
            data = Format.clear_value(self.options.get('data', ''))
            
            if operation == 'upload' and not data:
                self.log_debug("[!] Nenhum dado fornecido para upload")
                return
            
            # Criar cliente S3
            s3_client = self._get_s3_client()
            
            # Executar operação
            if operation == 'upload':
                result = self._upload_data(s3_client, data)
            elif operation == 'download':
                result = self._download_data(s3_client)
            elif operation == 'list':
                result = self._list_objects(s3_client)
            else:
                raise ValueError(f"Operação não suportada: {operation}")
            
            self.set_result(result)
            
            if self.options.get('debug'):
                self.log_debug(f"[+] S3 {operation} executado com sucesso")
                
        except ImportError as e:
            self.handle_error(e, "Erro de importação")
        except ValueError as e:
            self.handle_error(e, "Erro de configuração")
        except Exception as e:
            # Capturar erros específicos do boto3
            error_code = getattr(e, 'response', {}).get('Error', {}).get('Code', 'Unknown')
            error_msg = f"Erro S3 ({error_code}): {str(e)}"
            self.handle_error(e, error_msg)
