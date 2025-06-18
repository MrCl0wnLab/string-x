import httpx
from typing import Optional

class HTTPConnectionPool:
    _instance: Optional['HTTPConnectionPool'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._client = httpx.Client(
                timeout=30,
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
                http2=True
            )
        return cls._instance
    
    @property
    def client(self) -> httpx.Client:
        return self._client
    
    def close(self):
        if hasattr(self, '_client'):
            self._client.close()