"""
Execução de corrotinas com event loop reutilizável por thread.

Reusa um event loop dedicado por thread em vez de criar e destruir um novo
loop a cada chamada (como faz ``asyncio.run``), reduzindo o overhead quando
muitas requisições assíncronas são disparadas a partir do pool de threads do
String-X. Cada thread mantém o seu próprio loop, evitando conflitos entre as
threads worker.
"""
import asyncio
import threading
from typing import Any, Coroutine, TypeVar

_thread_local = threading.local()

T = TypeVar("T")


def get_thread_loop() -> asyncio.AbstractEventLoop:
    """
    Retorna o event loop desta thread, criando-o sob demanda.

    Returns:
        asyncio.AbstractEventLoop: Loop associado à thread atual.
    """
    loop = getattr(_thread_local, "loop", None)
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        _thread_local.loop = loop
    return loop


def run_async(coro: "Coroutine[Any, Any, T]") -> T:
    """
    Executa uma corrotina até a conclusão reusando o loop da thread atual.

    Substitui o uso de ``asyncio`` em loop descartável, evitando a
    criação/destruição de um novo event loop a cada chamada. Deve ser chamado
    a partir de um contexto
    síncrono (sem um event loop já em execução na thread atual).

    Args:
        coro: Corrotina a ser executada.

    Returns:
        O resultado produzido pela corrotina.
    """
    loop = get_thread_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)
