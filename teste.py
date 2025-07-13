import asyncio
from core.retry import retry_operation
import httpx

LIST_URLS = [
        'http://0000000000c0.x9xcax2a.workers.dev' ,
        'http://000000000a0uutlook.weebly.com' ,
        'http://00000002.c1.biz' ,
        'http://0000-1t8.pages.dev' ,
        'http://000025123.com/banks/cibc' ,
        'http://000025123.com/banks/desjardins' ,
        'http://000025123.com/banks/scotia' ,
        'http://000025123.com/banks/simplii' ,
        'http://00003485.com/banks/tangerine' ,
        'http://00003485.com/banks/td' ,
        'http://0.0.0.0forum.cryptonight.net' ,
        'http://0000h00003.byethost7.com/?i=1' ,
        'http://0.0.0.0mailgate.cryptonight.net' ,
        'http://0.0.0.0ns10.cryptonight.net' ,
        'http://0.0.0.0ssl.cryptonight.net' ,
        'http://0001.353527440.workers.dev' ,
        'http://0001home.webflow.io' ,
        'http://0007854.atwebpages.com/desk/index.html'
]
class ola:
    """
    Classe de exemplo para demonstrar o uso do decorator retry_operation.
    Esta classe deve ser substituída por uma implementação real.
    """
    def __init__(self):
        """
        Inicializa a classe com opções de retry.
        """
        self.options = {
            'retry': 0,
            'retry_delay': 1,
            # outros parâmetros...
        }

    @retry_operation
    async def exec_request(self, url):
        try:
            result = httpx.get(url, timeout=5)
            return {url, result.status_code}
        except Exception as e:
            print(f"Falhou! {url}")
            return []
            #raise ValueError(e)
    def exec(self):
        # Executa as requisições
        for url in LIST_URLS:
            try:
                result = asyncio.run(self.exec_request(url))
                print(f"Resultado para {url}: {result}")
            except Exception as e:
                print(f"Erro ao processar {url}: {e}")

# Exemplo de uso da classe ola
#obj_teste = ola()
#obj_teste.exec()
#print('Fim do teste') 

# Teste fora de class
print('Teste fora de class')  

options = {
        'retry': 3,
        'retry_delay': 1,
        # outros parâmetros...
    }

@retry_operation
async def exec_request(url, **options):
    import httpx
    try:
        result = httpx.get(url, timeout=5)
        return {url, result.status_code}
    except Exception as e:
        print(f"Falhou! {url}")
        raise ValueError(e)
        

# Chamando com parâmetros explícitos:
import asyncio

for url in LIST_URLS:
    try:
        result = asyncio.run(exec_request(url, **options))
        print(f"Resultado para {url}: {result}")
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
