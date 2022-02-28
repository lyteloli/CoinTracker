from aiogram import types, exceptions
from contextlib import suppress
from api import API
import asyncio
import menus
import const

api: API = API()
loop = asyncio.get_event_loop()


async def broadcast(coin_id: str):
    coin_data = await const.STORAGE.get('SELECT name, symbol, price FROM coins WHERE id = %s', coin_id)
    coin_data['symbol'] = coin_data['symbol'].upper()
    async for user in const.STORAGE.select('SELECT user_id FROM user_subscriptions WHERE coin_id = %s', coin_id):
        data = await const.NEKO.build_text(text='price_update', user=types.User(id=user['user_id']),
                                           text_format=coin_data)
        with suppress(exceptions.TelegramAPIError):
            await data.data.send_message(user_id=user['user_id'], neko=const.NEKO)
        await asyncio.sleep(.3)


async def price_pool():
    while True:
        async for item in const.STORAGE.select('SELECT id, name, symbol, price FROM coins'):
            coin = None
            while not coin:
                try:
                    coin = await api.get_coin(coin_id=item['id'])
                except RuntimeError:  # In case we hit API limits
                    await asyncio.sleep(1)

            if item['price'] != float(coin.current_price):
                await const.STORAGE.apply('UPDATE coins SET price = %s WHERE id = %s', (coin.current_price, coin.id))
                loop.create_task(broadcast(coin_id=coin.id))
            await asyncio.sleep(2)


if __name__ == '__main__':
    loop.create_task(price_pool())
    const.NEKO.add_texts()
    menus.user.FORMATTERS_ROUTER.attach_router(const.NEKO)
    menus.user.FUNCTIONS_ROUTER.attach_router(const.NEKO)
    const.NEKO.start_polling()
