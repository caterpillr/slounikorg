import logging, os
from aiogram import Bot, Dispatcher, executor, types
from parser import get_translations
from presets import presets, keyboard, btn, btn_presets
from db import db
from json import dumps, loads

from config import api_token

logging.basicConfig(level=logging.INFO)

path = os.path.abspath("") + '/'

try:
    API_TOKEN = os.environ['API_TOKEN']
except Exception as ex:
    try:
        API_TOKEN = input('enter telegram bot token : ')
        bot = Bot(token=API_TOKEN)
        event = Dispatcher(bot)
    except Exception as e:
        print(e)
        print("\n Probably given token is not valid...")
        exit()
    print(ex)
    print("\n no token is stored in environment")
    exit()

udb = db()
sql_list = {'dict_0': 1, 'dict_1': 2, 'dict_2': 3, 'dict_3': 4, 'poshuk': 5,
            1: 'dict_0', 2: 'dict_1', 3: 'dict_2', 4: 'dict_3', 5: 'poshuk'}
button_to_id = {'poshuk': btn.inline_poshuk, 'dict_0': btn.inline_belru, 'dict_3': btn.inline_encyclopedia,
                'dict_1': btn.inline_explain, 'dict_2': btn.inline_lexical}
param_buttons = [btn.inline_belru, btn.inline_explain, btn.inline_lexical, btn.inline_encyclopedia, btn.inline_poshuk]

@event.message_handler(commands=['start', 'home'])
async def start(message: types.message):
    print('message:', message.text, ' | id == ', message.message_id)
    user_id = message.from_user.id
    msg_id = message.message_id
    user_data = udb.get_user(user_id)
    if user_data is None:
        udb.add_user(user_id)
    # I cant delete messages older than 48h
    try:
        await bot.delete_message(user_id, msg_id)
    except:
        pass
    await bot.send_message(user_id, presets['greeting'], reply_markup=keyboard.home, parse_mode='HTML')

@event.callback_query_handler(lambda c: c.data in ['dict_0', 'dict_1', 'dict_2', 'dict_3', 'poshuk', 'settings'])
async def settings(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data = udb.get_user(user_id)
    msg_id = callback_query.message.message_id

    if callback_query.data != 'settings':
        chg_id = callback_query.data
        needed_value = user_data[sql_list[chg_id]]
        needed_value = (needed_value + 1) % 2
        user_data[sql_list[chg_id]] = needed_value
        udb.update(user_id, chg_id, needed_value)

    for i in range(len(param_buttons)):
        check = user_data[i + 1]
        if check:
            param_buttons[i].text = '●' + btn_presets[sql_list[i + 1]]
        else:
            param_buttons[i].text = '○️' + btn_presets[sql_list[i + 1]]

    if callback_query.data != 'settings':
        await bot.edit_message_reply_markup(user_id, msg_id, reply_markup=keyboard.settings)
    else:
        # I cant delete messages older than 48h
        try:
            await bot.delete_message(user_id, msg_id)
        except:
            pass
        await bot.send_message(user_id, presets['settings'], reply_markup=keyboard.settings, parse_mode='HTML')

@event.callback_query_handler(lambda c: c.data == 'home')
async def back_home(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    msg_id = callback_query.message.message_id

    # I cant delete messages older than 48h
    try:
        await bot.delete_message(user_id, msg_id)
    except:
        pass
    await bot.send_message(user_id, presets['greeting'], reply_markup=keyboard.home, parse_mode='HTML')

@event.message_handler()
async def search(message: types.message):
    print('message:', message.text, ' | id == ', message.message_id)
    user_id = message.from_user.id
    msg_id = message.message_id
    user_data = udb.get_user(user_id)

    request = message.text
    translations = get_translations(request, dict=list(user_data[1:5]), un=user_data[5])
    udb.update(user_id, 'page', 0)
    udb.update(user_id, 'current_trnslt', dumps(translations).replace("'", "''"))
    page = 0
    if len(translations) < 1:
        response = '<code>Not found</code>'
        kb_pref = keyboard.home
    else:
        # print('trans: ', json.dumps(translations))
        response = '<i>Source: ' + translations[page][1] + '</i>\n'
        response += translations[page][0] + '\n' + '______________________________'
        response += '\n    page ' + str(page + 1) + ' of ' + str(len(translations))
        kb_pref = keyboard.navigate

    if message.text[0] == '/':
        # I cant delete messages older than 48h
        try:
            await bot.delete_message(user_id, msg_id)
        except:
            pass
        await bot.send_message(user_id, '<i>Command doesnt exist</i>', parse_mode='HTML')
    else:
        try:
            await bot.edit_message_reply_markup(user_id, msg_id - 1, reply_markup=None)
        except Exception as e:
            print('i guess no kb, but caught : ', e)
        try:
            await bot.send_message(user_id, response, reply_markup=kb_pref, parse_mode='HTML',
                                   disable_web_page_preview=True)
        except:
            await bot.send_message(user_id, 'response contains an unsupported HTML tag', reply_markup=kb_pref, parse_mode='HTML',
                                   disable_web_page_preview=True)

@event.callback_query_handler(lambda c: c.data == 'settings_clear')
async def settings(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    msg_id = callback_query.message.message_id

    await bot.edit_message_reply_markup(user_id, msg_id, reply_markup=None)
    await bot.send_message(user_id, presets['settings'], reply_markup=keyboard.settings, parse_mode='HTML')

@event.callback_query_handler(lambda c: c.data in ['-1', '1'])
async def change_page(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    msg_id = callback_query.message.message_id
    user_data = udb.get_user(user_id)

    # print(user_data[7])
    translations = loads(user_data[7][1:-1])
    page = (user_data[6] + int(callback_query.data)) % len(translations)
    # print('dump: ', dumps(translations))
    response = '<i>Source: ' + translations[page][1] + '</i>\n'
    response += translations[page][0] + '\n' + '______________________________'
    response += '\n    page ' + str(page + 1) + ' of ' + str(len(translations))

    udb.update(user_id, 'page', page)

    await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=response, parse_mode='HTML',
                                reply_markup=keyboard.navigate, disable_web_page_preview=True)





if __name__ == '__main__':
    try:
        executor.start_polling(event)
    except Exception as e:
        bot.send_message(299087009, '<b>vsem fuck thats an error\n</b>' + str(e), parse_mode='HTML')