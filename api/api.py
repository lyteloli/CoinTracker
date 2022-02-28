from typing import List, Optional
import aiohttp
import asyncio
from . import objects

try:
    import ujson as json
except ImportError:
    import json


class API:
    def __init__(self, endpoint: str = 'https://api.coingecko.com/api/v3'):
        self.endpoint: str = endpoint

    @staticmethod
    async def get_session() -> aiohttp.ClientSession:
        """
        Gets an aiohttp client session
        :return: aiohttp ClientSession object
        """
        return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def ping(self) -> str:
        async with await self.get_session() as session:
            r = await (await session.get(f'{self.endpoint}/ping')).json()
        return r['gecko_says']

    async def list_coins(self) -> List[objects.Coin]:
        coins: List[objects.Coin] = list()
        async with await self.get_session() as session:
            r = await (await session.get(f'{self.endpoint}/coins/list')).json()

        for coin in r:
            coins.append(objects.Coin(id=coin['id'], name=coin['name'], symbol=coin['symbol']))
        return coins

    async def get_coin(self, coin_id: str) -> objects.Coin:
        params: dict = dict(id=coin_id, localization='false', tickers=False, community_data=False, developer_data=False)
        async with await self.get_session() as session:
            r = await (await session.get(f'{self.endpoint}/coins/{coin_id}', params=json.dumps(params))).json()
        if r.get('error'):
            raise RuntimeError(r['error'])

        coin: objects.Coin = objects.Coin(id=coin_id, name=r['name'], symbol=r['symbol'],
                                          current_price=r['market_data']['current_price']['usd'],
                                          description=r.get('description', dict()).get('en', None))
        image: Optional[str] = r.get('image', dict()).get('large', None)
        if image is None:
            image = r.get('image', dict()).get('small', None)
            if image is None:
                image = r.get('image', dict()).get('thumb', None)
        coin.image = image
        return coin


if __name__ == '__main__':
    from pprint import pprint
    api = API()
    pprint(asyncio.get_event_loop().run_until_complete(api.get_coin('bitcoin')))
