"""
Módulo extrator de metadados de arquivos.

Este módulo implementa funcionalidades para extrair metadados de diferentes
tipos de arquivos, incluindo informações como tamanho, datas de criação/modificação,
tipo MIME, propriedades específicas de formato e metadados EXIF para imagens.
"""

import os
import mimetypes
import magic
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json

# Imports opcionais para funcionalidades específicas
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import mutagen
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

from stringx.core.basemodule import BaseModule


class MetadataExtractor(BaseModule):
    """
    Módulo para extração de metadados de arquivos.
    
    Extrai informações detalhadas sobre arquivos incluindo:
    - Informações básicas do sistema de arquivos
    - Tipo MIME e detecção de formato
    - Metadados EXIF de imagens
    - Metadados de áudio/vídeo
    - Informações de documentos PDF
    """
    
    def __init__(self):
        """
        Inicializa o módulo extrator de metadados.
        
        Configura os metadados do módulo e define as opções necessárias,
        incluindo tipos de metadados a extrair e formatos de saída.
        """
        super().__init__()

        # Define informações de meta do módulo
        self.meta.update({
            "name": "Extrator de Metadados de Arquivos",
            "description": "Extrai metadados detalhados de arquivos incluindo informações do sistema, EXIF, e propriedades específicas por formato",
            "author": "MrCl0wn",
            "version": "1.0",
            "type": "extractor",
            "example": "./strx -l arquivos.txt -st 'echo {STRING}' -module 'ext:metadata' -pm"
        })

        # Define opções requeridas para este módulo
        self.options = {
            "data": str(),  # Caminho do arquivo ou lista de caminhos
            "include_exif": True,    # Incluir metadados EXIF para imagens
            "include_audio": True,   # Incluir metadados de áudio/vídeo
            "include_document": True, # Incluir metadados de documentos
            "output_format": "detailed",  # detailed, compact, json
            "file_size_limit": 100,  # Limite em MB para processamento (0 = sem limite)
            "debug": False,  # Modo de debug para mostrar informações detalhadas
            "retry": 0,      # Número de tentativas
            "retry_delay": None,  # Atraso entre tentativas
        }

    def run(self):
        """
        Executa o processo de extração de metadados.
        
        Processa o caminho do arquivo fornecido e extrai todos os metadados
        disponíveis conforme as opções configuradas.
        """
        # Limpar resultados anteriores
        self._result[self._get_cls_name()].clear()
        
        file_path = self.options.get("data", "").strip()
        if not file_path:
            if self.options.get('debug', False):
                self.log_debug("Nenhum caminho de arquivo especificado")
            return

        try:
            # Verificar se o arquivo existe
            if not os.path.exists(file_path):
                if self.options.get('debug', False):
                    self.log_debug(f"Arquivo não encontrado: {file_path}")
                return

            # Verificar limite de tamanho
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            size_limit = self.options.get("file_size_limit", 100)
            
            if size_limit > 0 and file_size_mb > size_limit:
                if self.options.get('debug', False):
                    self.log_debug(f"Arquivo muito grande ({file_size_mb:.2f}MB > {size_limit}MB): {file_path}")
                return

            # Extrair metadados
            metadata = self._extract_file_metadata(file_path)
            
            if metadata:
                # Definir resultados individuais sem quebras de linha
                lines = self._format_detailed_output_as_list(metadata)
                lines.append("")
                self.set_result("\n".join(lines))
                    
                if self.options.get('debug', False):
                    self.log_debug(f"Metadados extraídos com sucesso de: {file_path}")
                        
        except Exception as e:
            self.handle_error(e, f"Erro ao extrair metadados de {file_path}")

    def _extract_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extrai metadados completos de um arquivo.
        
        Args:
            file_path: Caminho para o arquivo
            
        Returns:
            Dicionário com todos os metadados extraídos
        """
        metadata = {}
        
        try:
            # Informações básicas do arquivo
            metadata.update(self._get_basic_file_info(file_path))
            
            # Detecção de tipo MIME
            metadata.update(self._get_mime_info(file_path))
            
            # Metadados específicos por tipo
            file_type = metadata.get("mime_type", "").lower()
            
            # Metadados de imagem (EXIF)
            if self.options.get("include_exif", True) and file_type.startswith("image/"):
                exif_data = self._get_image_metadata(file_path)
                if exif_data:
                    metadata["exif"] = exif_data
            
            # Metadados de áudio/vídeo
            if self.options.get("include_audio", True) and (file_type.startswith("audio/") or file_type.startswith("video/")):
                audio_data = self._get_audio_metadata(file_path)
                if audio_data:
                    metadata["audio"] = audio_data
            
            # Metadados de documento
            if self.options.get("include_document", True) and file_type == "application/pdf":
                doc_data = self._get_document_metadata(file_path)
                if doc_data:
                    metadata["document"] = doc_data
                    
        except Exception as e:
            self.handle_error(e, f"Erro durante extração de metadados de {file_path}")
            
        return metadata

    def _get_basic_file_info(self, file_path: str) -> Dict[str, Any]:
        """Extrai informações básicas do arquivo do sistema de arquivos."""
        try:
            path_obj = Path(file_path)
            stat_info = path_obj.stat()
            
            return {
                "filename": path_obj.name,
                "file_path": str(path_obj.absolute()),
                "file_size_bytes": stat_info.st_size,
                "file_size_human": self._human_readable_size(stat_info.st_size),
                "creation_time": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                "modification_time": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                "access_time": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                "file_extension": path_obj.suffix.lower(),
                "permissions": oct(stat_info.st_mode)[-3:],
            }
        except Exception as e:
            self.handle_error(e, "Erro ao obter informações básicas do arquivo")
            return {}

    def _get_mime_info(self, file_path: str) -> Dict[str, str]:
        """Detecta tipo MIME e informações de formato."""
        mime_info = {}
        
        try:
            # Usando mimetypes padrão
            mime_type, encoding = mimetypes.guess_type(file_path)
            mime_info["mime_type"] = mime_type or "unknown"
            if encoding:
                mime_info["encoding"] = encoding
            
            # Usando python-magic para detecção mais precisa
            try:
                file_type = magic.from_file(file_path)
                mime_type_magic = magic.from_file(file_path, mime=True)
                
                mime_info["file_type_description"] = file_type
                mime_info["mime_type_magic"] = mime_type_magic
            except:
                pass  # python-magic não disponível
                
        except Exception as e:
            self.handle_error(e, "Erro ao detectar tipo MIME")
            
        return mime_info

    def _get_image_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extrai metadados EXIF de imagens."""
        if not PILLOW_AVAILABLE:
            return None
            
        try:
            with Image.open(file_path) as image:
                image_info = {
                    "dimensions": f"{image.width}x{image.height}",
                    "mode": image.mode,
                    "format": image.format,
                }
                
                # Extrair EXIF
                exif_data = image.getexif()
                if exif_data:
                    exif_dict = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_dict[tag] = str(value)
                    
                    image_info["exif_data"] = exif_dict
                    
                return image_info
                
        except Exception as e:
            self.handle_error(e, "Erro ao extrair metadados de imagem")
            return None

    def _get_audio_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extrai metadados de arquivos de áudio/vídeo."""
        if not MUTAGEN_AVAILABLE:
            return None
            
        try:
            audio_file = mutagen.File(file_path)
            if audio_file is None:
                return None
                
            metadata = {
                "duration_seconds": getattr(audio_file.info, 'length', 0),
                "bitrate": getattr(audio_file.info, 'bitrate', 0),
            }
            
            # Tags comuns
            common_tags = ['title', 'artist', 'album', 'date', 'genre', 'track']
            for tag in common_tags:
                values = audio_file.get(tag) or audio_file.get(tag.upper())
                if values:
                    metadata[tag] = str(values[0]) if isinstance(values, list) else str(values)
                    
            return metadata
            
        except Exception as e:
            self.handle_error(e, "Erro ao extrair metadados de áudio")
            return None

    def _get_document_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extrai metadados de documentos PDF."""
        if not PYPDF2_AVAILABLE:
            return None
            
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                metadata = {
                    "page_count": len(pdf_reader.pages),
                    "encrypted": pdf_reader.is_encrypted,
                }
                
                # Metadados do documento
                if pdf_reader.metadata:
                    doc_info = {}
                    for key, value in pdf_reader.metadata.items():
                        clean_key = key.replace('/', '').lower()
                        doc_info[clean_key] = str(value)
                    
                    metadata["document_info"] = doc_info
                    
                return metadata
                
        except Exception as e:
            self.handle_error(e, "Erro ao extrair metadados de documento")
            return None

    def _format_metadata_output(self, metadata: Dict[str, Any], output_format: str) -> str:
        """Formata a saída dos metadados conforme o formato especificado."""
        try:
            if output_format == "json":
                return json.dumps(metadata, indent=2, ensure_ascii=False)
            
            elif output_format == "compact":
                return self._format_compact_output(metadata)
            
            else:  # detailed (padrão)
                return self._format_detailed_output(metadata)
                
        except Exception as e:
            self.handle_error(e, "Erro ao formatar saída de metadados")
            return ""

    def _format_detailed_output(self, metadata: Dict[str, Any]) -> str:
        """Formata saída detalhada dos metadados."""
        lines = []
        
        # Informações básicas
        lines.append(f"Arquivo: {metadata.get('filename', 'N/A')}")
        lines.append(f"Caminho: {metadata.get('file_path', 'N/A')}")
        lines.append(f"Tamanho: {metadata.get('file_size_human', 'N/A')} ({metadata.get('file_size_bytes', 0)} bytes)")
        lines.append(f"Extensão: {metadata.get('file_extension', 'N/A')}")
        lines.append(f"Tipo MIME: {metadata.get('mime_type', 'N/A')}")
        
        if 'file_type_description' in metadata:
            lines.append(f"Descrição do tipo: {metadata['file_type_description']}")
        
        if 'mime_type_magic' in metadata:
            lines.append(f"MIME (magic): {metadata['mime_type_magic']}")
        
        if 'encoding' in metadata:
            lines.append(f"Codificação: {metadata['encoding']}")
        
        # Datas (evitar duplicação)
        if 'creation_time' in metadata:
            lines.append(f"Data de criação: {metadata['creation_time']}")
        
        if 'modification_time' in metadata:
            lines.append(f"Data de modificação: {metadata['modification_time']}")
        
        if 'access_time' in metadata:
            lines.append(f"Data de acesso: {metadata['access_time']}")
        
        # Permissões
        if 'permissions' in metadata:
            lines.append(f"Permissões: {metadata['permissions']}")
        
        # Metadados de imagem
        if 'exif' in metadata:
            exif = metadata['exif']
            if 'dimensions' in exif:
                lines.append(f"Dimensões: {exif['dimensions']}")
            if 'format' in exif:
                lines.append(f"Formato da imagem: {exif['format']}")
            if 'mode' in exif:
                lines.append(f"Modo de cor: {exif['mode']}")
            
            # Dados EXIF
            if 'exif_data' in exif and exif['exif_data']:
                for key, value in exif['exif_data'].items():
                    lines.append(f"EXIF {key}: {value}")
        
        # Metadados de áudio/vídeo
        if 'audio' in metadata:
            audio = metadata['audio']
            if 'duration_seconds' in audio and audio['duration_seconds']:
                duration = int(audio['duration_seconds'])
                minutes, seconds = divmod(duration, 60)
                lines.append(f"Duração: {minutes}:{seconds:02d}")
            
            if 'bitrate' in audio and audio['bitrate']:
                lines.append(f"Bitrate: {audio['bitrate']} kbps")
            
            if 'title' in audio:
                lines.append(f"Título: {audio['title']}")
            
            if 'artist' in audio:
                lines.append(f"Artista: {audio['artist']}")
            
            if 'album' in audio:
                lines.append(f"Álbum: {audio['album']}")
            
            if 'date' in audio:
                lines.append(f"Data do áudio: {audio['date']}")
            
            if 'genre' in audio:
                lines.append(f"Gênero: {audio['genre']}")
            
            if 'track' in audio:
                lines.append(f"Faixa: {audio['track']}")
        
        # Metadados de documento
        if 'document' in metadata:
            doc = metadata['document']
            if 'page_count' in doc:
                lines.append(f"Número de páginas: {doc['page_count']}")
            
            if 'encrypted' in doc:
                lines.append(f"Documento criptografado: {'Sim' if doc['encrypted'] else 'Não'}")
            
            # Informações do documento
            if 'document_info' in doc:
                for key, value in doc['document_info'].items():
                    lines.append(f"Doc {key}: {value}")
        
        return "\n".join(lines)

    def _format_detailed_output_as_list(self, metadata: Dict[str, Any]) -> list:
        """Formata saída detalhada dos metadados como lista de strings."""
        lines = []
        
        # Informações básicas
        lines.append(f"Arquivo: {metadata.get('filename', 'N/A')}")
        lines.append(f"Caminho: {metadata.get('file_path', 'N/A')}")
        lines.append(f"Tamanho: {metadata.get('file_size_human', 'N/A')} ({metadata.get('file_size_bytes', 0)} bytes)")
        lines.append(f"Extensão: {metadata.get('file_extension', 'N/A')}")
        lines.append(f"Tipo MIME: {metadata.get('mime_type', 'N/A')}")
        
        if 'file_type_description' in metadata:
            lines.append(f"Descrição do tipo: {metadata['file_type_description']}")
        
        if 'mime_type_magic' in metadata:
            lines.append(f"MIME (magic): {metadata['mime_type_magic']}")
        
        if 'encoding' in metadata:
            lines.append(f"Codificação: {metadata['encoding']}")
        
        # Datas (evitar duplicação)
        if 'creation_time' in metadata:
            lines.append(f"Data de criação: {metadata['creation_time']}")
        
        if 'modification_time' in metadata:
            lines.append(f"Data de modificação: {metadata['modification_time']}")
        
        if 'access_time' in metadata:
            lines.append(f"Data de acesso: {metadata['access_time']}")
        
        # Permissões
        if 'permissions' in metadata:
            lines.append(f"Permissões: {metadata['permissions']}")
        
        # Metadados de imagem
        if 'exif' in metadata:
            exif = metadata['exif']
            if 'dimensions' in exif:
                lines.append(f"Dimensões: {exif['dimensions']}")
            if 'format' in exif:
                lines.append(f"Formato da imagem: {exif['format']}")
            if 'mode' in exif:
                lines.append(f"Modo de cor: {exif['mode']}")
            
            # Dados EXIF
            if 'exif_data' in exif and exif['exif_data']:
                for key, value in exif['exif_data'].items():
                    lines.append(f"EXIF {key}: {value}")
        
        # Metadados de áudio/vídeo
        if 'audio' in metadata:
            audio = metadata['audio']
            if 'duration_seconds' in audio and audio['duration_seconds']:
                duration = int(audio['duration_seconds'])
                minutes, seconds = divmod(duration, 60)
                lines.append(f"Duração: {minutes}:{seconds:02d}")
            
            if 'bitrate' in audio and audio['bitrate']:
                lines.append(f"Bitrate: {audio['bitrate']} kbps")
            
            if 'title' in audio:
                lines.append(f"Título: {audio['title']}")
            
            if 'artist' in audio:
                lines.append(f"Artista: {audio['artist']}")
            
            if 'album' in audio:
                lines.append(f"Álbum: {audio['album']}")
            
            if 'date' in audio:
                lines.append(f"Data do áudio: {audio['date']}")
            
            if 'genre' in audio:
                lines.append(f"Gênero: {audio['genre']}")
            
            if 'track' in audio:
                lines.append(f"Faixa: {audio['track']}")
        
        # Metadados de documento
        if 'document' in metadata:
            doc = metadata['document']
            if 'page_count' in doc:
                lines.append(f"Número de páginas: {doc['page_count']}")
            
            if 'encrypted' in doc:
                lines.append(f"Documento criptografado: {'Sim' if doc['encrypted'] else 'Não'}")
            
            # Informações do documento
            if 'document_info' in doc:
                for key, value in doc['document_info'].items():
                    lines.append(f"Doc {key}: {value}")
        
        return lines

    def _format_compact_output(self, metadata: Dict[str, Any]) -> str:
        """Formata saída compacta dos metadados."""
        parts = [
            metadata.get('filename', 'unknown'),
            metadata.get('file_size_human', '0B'),
            metadata.get('mime_type', 'unknown'),
        ]
        
        if 'exif' in metadata and 'dimensions' in metadata['exif']:
            parts.append(f"Dim:{metadata['exif']['dimensions']}")
        
        if 'audio' in metadata and 'duration_seconds' in metadata['audio']:
            duration = int(metadata['audio']['duration_seconds'])
            minutes, seconds = divmod(duration, 60)
            parts.append(f"Dur:{minutes}:{seconds:02d}")
        
        if 'document' in metadata and 'page_count' in metadata['document']:
            parts.append(f"Pgs:{metadata['document']['page_count']}")
        
        return " | ".join(parts)

    def _human_readable_size(self, size_bytes: int) -> str:
        """Converte bytes para formato legível."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}PB"