from aiogram.types.inline_keyboard import *

presets = {
    'greeting': """*бот для slounik.org*
<i>Адпраў слова на пераклад(бел -> ру)</i>\nАльбо перайдзі ў настройкі пошуку""",
    'settings': """У якіх слоўніках шукаць?
    """
}

btn_presets = {
    'home': 'Назад',
    'settings': 'Настройкі пошуку',
    'poshuk_un': 'Пошук толькі ў назве',
    'belru': '  Пераклад',
    'explain': 'Тлумачальныя',
    'lexical': 'Агульныя',
    'encyclopedia': 'Энцыкляпедыі',
    'dict_0': 'Пераклад',
    'dict_1': 'Тлумачальныя',
    'dict_2': 'Агульныя',
    'dict_3': 'Энцыкляпедыі',
    'poshuk': 'Пошук толькі ў назве'
}

class btn():
    inline_home = InlineKeyboardButton(btn_presets['home'], callback_data='home')
    inline_settings = InlineKeyboardButton(btn_presets['settings'], callback_data='settings')
    inline_poshuk = InlineKeyboardButton(btn_presets['poshuk_un'], callback_data='poshuk')
    inline_belru = InlineKeyboardButton(btn_presets['belru'], callback_data='dict_0')
    inline_explain = InlineKeyboardButton(btn_presets['explain'], callback_data='dict_1')
    inline_lexical = InlineKeyboardButton(btn_presets['lexical'], callback_data='dict_2')
    inline_encyclopedia = InlineKeyboardButton(btn_presets['encyclopedia'], callback_data='dict_3')

    inline_left = InlineKeyboardButton('⬅️', callback_data='-1')
    inline_right = InlineKeyboardButton('➡️', callback_data='1')
    inline_settings_light = InlineKeyboardButton('🔘', callback_data='settings_clear')

class format():
    bold = '<b>%s</b>'
    italic = '<i>%s</i>'
    underlined = '<u>%s</u>'
    striked = '<s>%s</s>'
    red = '<code>%s</code>'

class keyboard():
    settings = InlineKeyboardMarkup(row_width=2)
    settings.add(btn.inline_belru, btn.inline_explain)
    settings.add(btn.inline_lexical, btn.inline_encyclopedia)
    settings.row_width = 1
    settings.add(btn.inline_poshuk, btn.inline_home)

    home = InlineKeyboardMarkup().add(btn.inline_settings)

    navigate = InlineKeyboardMarkup(row_width=3)
    navigate.add(btn.inline_left, btn.inline_settings_light, btn.inline_right)