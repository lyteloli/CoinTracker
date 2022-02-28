from NekoGram import Neko, types, BuildResponse, NekoRouter
from utils import strip_tags
from api import API

ROUTER: NekoRouter = NekoRouter()
api: API = API()


@ROUTER.function()
async def menu_new_sub(data: BuildResponse, message: types.Message, neko: Neko):
    coin = await neko.storage.get('SELECT id FROM coins WHERE id = %(query)s OR name = %(query)s OR symbol = %(query)s',
                                  dict(query=message.text))
    if coin:
        await neko.storage.apply('INSERT INTO user_subscriptions (user_id, coin_id) VALUES (%s, %s)',
                                 (message.from_user.id, coin['id']))
        data = await neko.build_text(text='menu_sub', user=message.from_user,
                                     formatter_extras={'call_data': coin['id']})
        await neko.storage.set_user_data(data={'selected_coin': coin['id']}, user_id=message.from_user.id)
    else:
        try:
            coin = await api.get_coin(coin_id=message.text)
            description = coin.description
            if len(description) > 1000:
                description = strip_tags(description)  # Remove HTML not to break it
                description = f'{description[:997]}...'
            await neko.storage.apply('INSERT INTO coins (id, name, symbol, image, price, description) VALUES '
                                     '(%s, %s, %s, %s, %s, %s)', (coin.id, coin.name, coin.symbol, coin.image,
                                                                  coin.current_price, description))
            await neko.storage.apply('INSERT INTO user_subscriptions (user_id, coin_id) VALUES (%s, %s)',
                                     (message.from_user.id, coin.id))
            data = await neko.build_text(text='menu_sub', user=message.from_user,
                                         formatter_extras={'call_data': coin.id})
            await neko.storage.set_user_data(data={'selected_coin': coin.id}, user_id=message.from_user.id)
        except RuntimeError:
            pass
    if not coin:
        data.data.text = data.data.extras['alt_text']
    await data.data.send_message(user_id=message.from_user.id, neko=neko)


@ROUTER.function()
async def menu_unsubscribe(_: BuildResponse, call: types.CallbackQuery, neko: Neko):
    user_data = await neko.storage.get_user_data(user_id=call.from_user.id)
    await neko.storage.apply('DELETE FROM user_subscriptions WHERE user_id = %s AND coin_id = %s',
                             (call.from_user.id, user_data['selected_coin']))
    data = await neko.build_text(text='menu_my_subs', user=call.from_user)
    await data.data.edit_text(message=call.message)
