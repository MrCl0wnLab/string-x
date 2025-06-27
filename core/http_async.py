# core/http_client.py
import httpx
from typing import Optional

class HTTPClient:
    def __init__(self):
        self.client = httpx.Client(
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            timeout=httpx.Timeout(30.0)
        )
    
    async def get_async(self, url: str, **kwargs):
        async with httpx.AsyncClient() as client:
            return await client.get(url, **kwargs)