from telebot import types


def get_markup_for_continue_reg():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Да, добавить.", callback_data="Да, добавить.")
    btn2 = types.InlineKeyboardButton(text="Нет, не добавлять.", callback_data="Нет, не добавлять.")
    markup.row(btn1, btn2)
    return markup


def get_marcup_for_chose_question():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Номер твоей школы",
                                      callback_data="Номер твоей школы")
    btn2 = types.InlineKeyboardButton(text="Твой знак зодиака",
                                      callback_data="Твой знак зодиака")
    btn3 = types.InlineKeyboardButton(text="Твой любимый фильм",
                                      callback_data="Твой любимый фильм")
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    return markup


def clear_markup():
    markup = types.ReplyKeyboardRemove(selective=False)
    return markup


def continuation_authorization():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Повторить ввод пароля.", callback_data="Повторить ввод пароля.")
    btn2 = types.InlineKeyboardButton(text="Выйти из авторизации.", callback_data="Выйти из авторизации.")
    btn3 = types.InlineKeyboardButton(text="Восстановить пароль.", callback_data="Восстановить пароль.")
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    return markup


def get_markups_for_password_recovery():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Повторить ввод ответа.", callback_data="Повторить ввод ответа.")
    btn2 = types.InlineKeyboardButton(text="Выйти из восстановления пароля.",
                                      callback_data="Выйти из восстановления пароля.")
    markup.row(btn1)
    markup.row(btn2)
    return markup