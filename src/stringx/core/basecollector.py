"""
Classe base para módulos coletores (tipo ``clc``).

Centraliza o boilerplate comum dos coletores HTTP — construção de headers,
User-Agent de navegador e resolução de timeout — que hoje aparece duplicado em
dezenas de módulos. Coletores devem herdar de ``BaseCollector`` em vez de
``BaseModule`` e usar os helpers ``_default_headers()`` e ``_get_timeout()``.
"""
from typing import Dict, Optional

from stringx.core.basemodule import BaseModule


class BaseCollector(BaseModule):
    """Base para coletores HTTP, com helpers de header e timeout."""

    # User-Agent de navegador: muitos serviços/APIs bloqueiam clientes que não
    # se identificam como navegador. Mantém paridade com o UA antes hardcoded
    # nos módulos.
    DEFAULT_USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )

    def _default_headers(
        self,
        accept: str = 'application/json',
        extra: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """
        Monta os headers HTTP padrão de um coletor.

        Args:
            accept: Valor do header ``Accept``.
            extra: Headers adicionais/sobrescritas (ex.: tokens de API).

        Returns:
            Dict[str, str]: Headers prontos para a requisição.
        """
        headers = {
            'User-Agent': self.options.get('user-agent') or self.DEFAULT_USER_AGENT,
            'Accept': accept,
        }
        if extra:
            headers.update({k: v for k, v in extra.items() if v is not None})
        return headers

    def _get_timeout(self, default: int = 10) -> int:
        """
        Resolve o timeout de requisição.

        Usa o valor da opção ``timeout`` do módulo, se definido; caso contrário,
        cai para ``STRX_REQUEST_TIMEOUT`` da configuração e, por fim, ``default``.

        Args:
            default: Valor usado se nada estiver configurado.

        Returns:
            int: Timeout em segundos.
        """
        value = self.options.get('timeout')
        if value:
            return value
        return getattr(self.setting, 'STRX_REQUEST_TIMEOUT', default)
