import asyncio
from abc import ABC, abstractmethod

from parsel import Selector


class BaseCrawler(ABC):
    urls = []

    def __init__(self, session):
        self.session = session

    async def execute(self, **kwargs):
        task = [self._start_request(url, **kwargs) for url in self.urls]
        await asyncio.gather(*task)

    async def _start_request(self, url, **kwargs):
        async with self.session.get(url.format(**kwargs)) as response:
            data = await response.text()
        self.parse(Selector(text=data))

    @abstractmethod
    def parse(self, data):
        raise NotImplementedError
