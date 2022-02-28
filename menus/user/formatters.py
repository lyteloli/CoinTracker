from NekoGram import Neko, types, BuildResponse, NekoRouter

ROUTER: NekoRouter = NekoRouter()


@ROUTER.formatter()
async def menu_my_subs(data: BuildResponse, user: types.User, neko: Neko):
    markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=2)
    for sub in await neko.storage.get('SELECT u.coin_id, c.name, c.symbol FROM user_subscriptions u '
                                      'JOIN coins c ON c.id = u.coin_id '
                                      'WHERE user_id = %s', user.id, fetch_all=True):
        markup.add(types.InlineKeyboardButton(text=f'{sub["name"]} ({sub["symbol"].upper()})',
                                              callback_data=f'menu_sub#{sub["coin_id"]}'))
    await data.data.assemble_markup(markup=markup)


@ROUTER.formatter()
async def menu_sub(data: BuildResponse, user: types.User, neko: Neko):
    coin = await neko.storage.get('SELECT id, name, symbol, description, image, price FROM coins WHERE id = %s',
                                  data.data.call_data)
    coin['symbol'] = coin['symbol'].upper()
    await neko.storage.set_user_data(data={'selected_coin': coin['id']}, user_id=user.id)
    await data.data.assemble_markup(text_format=coin)
