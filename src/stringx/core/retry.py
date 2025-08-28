import time
import asyncio
import functools
import inspect

def retry_operation(func):
    """
    Decorador universal para retry em métodos de classe (usando self.options) e funções livres.
    Compatível com funções síncronas e assíncronas.
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        max_attempts, delay, debug_mode, set_result = _get_retry_params(args, kwargs)
        attempts = 0
        last_error = None
        while attempts < max_attempts:
            try:
                result = await func(*args, **kwargs)
                if result is not None:
                    return result
                if set_result:
                    set_result(f"Função retornou None. Tentativa {attempts+1}/{max_attempts}")
                attempts += 1
                if attempts < max_attempts:
                    await asyncio.sleep(delay)
            except Exception as e:
                last_error = e
                attempts += 1
                if debug_mode and set_result:
                    set_result(f"Tentativa {attempts}/{max_attempts} falhou. Tentando novamente em {delay}s...")
                if attempts < max_attempts:
                    await asyncio.sleep(delay)
        if set_result and debug_mode:
            set_result(f"Todas as {max_attempts} tentativas falharam: {str(last_error)}")
        # Don't raise exceptions that would be unhandled and cause the tool to exit
        if last_error:
            return None
        else:
            return None

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        max_attempts, delay, debug_mode, set_result = _get_retry_params(args, kwargs)
        attempts = 0
        last_error = None
        while attempts < max_attempts:
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    return result
                if set_result and debug_mode:
                    set_result(f"Função retornou None. Tentativa {attempts+1}/{max_attempts}")
                attempts += 1
                if attempts < max_attempts:
                    time.sleep(delay)
            except Exception as e:
                last_error = e
                attempts += 1
                if debug_mode and set_result:
                    set_result(f"Tentativa {attempts}/{max_attempts} falhou. Tentando novamente em {delay}s...")
                if attempts < max_attempts:
                    time.sleep(delay)
        if set_result and debug_mode:
            set_result(f"Todas as {max_attempts} tentativas falharam: {str(last_error)}")
        # Don't raise exceptions that would be unhandled and cause the tool to exit
        if last_error:
            return None
        else:
            return None

    def _get_retry_params(args, kwargs):
        # Defaults
        max_attempts = 3
        delay = 1
        debug_mode = False
        set_result = None

        # Se for método de instância, tenta buscar em self.options
        if args:
            obj = args[0]
            if hasattr(obj, 'options'):
                options = getattr(obj, 'options')
                max_attempts = options.get('retry', max_attempts)
                delay = options.get('retry_delay', delay)
                debug_mode = options.get('debug', False)
                set_result = getattr(obj, 'set_result', None)
        # Permite sobrescrever via kwargs (função livre)
        max_attempts = kwargs.get('retry', max_attempts)
        delay = kwargs.get('retry_delay', delay)
        debug_mode = kwargs.get('debug', debug_mode)
        set_result = kwargs.get('set_result', set_result)
        return max_attempts, delay, debug_mode, set_result

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
