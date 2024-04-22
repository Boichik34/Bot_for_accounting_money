import telebot
import logic
import markups
import app


TOKEN = ""
bot = telebot.TeleBot(TOKEN)

application = app.App()


@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, f"Приветствую тебя, {message.from_user.first_name}.\n"
                                      f"Это Бот, который помогает пользователям управлять их личными"
                                      f" финансами, включая отслеживание расходов и доходов, "
                                      f"категоризацию финансовых операций и анализ личного бюджета.\n"
                                      f"Нажми меню для выбора комманды")


@bot.message_handler(commands=["register"])
def registration_handler(message):
    if logic.check_user(message.from_user.id):
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")
    else:
        registration(message)


@bot.message_handler(commands=["authorization"])
def authorization_handler(message):
    application.set_state("authorization")
    bot.send_message(message.chat.id, "Для авторизации введите пароль")


@bot.message_handler(commands=["add_income"])
def add_income_handler(message):
    to_add_income_category(message)








@bot.callback_query_handler(func=lambda call: call.data == "Повторить ввод пароля.")
def repeat_authorization(call):
    authorization_handler(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "Выйти из авторизации.")
def stop__authorization(call):
    markup = markups.clear_markup()
    bot.send_message(call.message.chat.id, "Авторизация остановлена. "
                                           "Перейдите в меню для выбора "
                                           "команды для продолжения", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "Восстановить пароль.")
def password_recovery(call):
    application.set_state("password recovery")
    question = logic.get_question(call.from_user.id)
    bot.send_message(call.message.chat.id, f"Oтветь на вопрос: {question}?")


@bot.callback_query_handler(func=lambda call: call.data == "Повторить ввод ответа.")
def continue_password_recovery(call):
    password_recovery(call)


@bot.callback_query_handler(func=lambda call: call.data == "Выйти из восстановления пароля.")
def stop_password_recovery(call):
    markup = markups.clear_markup()
    bot.send_message(call.message.chat.id, "Не удалось восстановить пароль! Надо было записывать!\n"
                                           "Для продолжения выбери команду в МЕНЮ", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["Да, добавить."])
def chose_question_for_password_recovery(call):
    markup = markups.get_marcup_for_chose_question()
    bot.send_message(call.message.chat.id, 'Выбери вопрос.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["Нет, не добавлять."])
def dont_add_question(call):
    markup = markups.clear_markup()
    bot.send_message(call.message.chat.id, 'Выбери комманду в Меню для продолжения', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["Номер твоей школы",
                                                            "Твой знак зодиака",
                                                            "Твой любимый фильм"])
def add_question_for_password_recovery(call):
    answer = bot.send_message(call.message.chat.id, f"{call.data}?")
    bot.register_next_step_handler(answer, add_question, f"{call.data}")


@bot.callback_query_handler(func=lambda call: application.get_state() == "chose_income_category")
def chose_income_category(call):
    if call.data == "Выбрать новую категорию":
        application.set_state("write_income_category")
        bot.send_message(call.message.chat.id, "Напишите название категории")
    else:
        application.set_category(call.data)
        input_income(call.message)






def registration(message):
    application.set_state("registration")
    bot.send_message(message.chat.id, f"Ваш 'ник' {message.from_user.first_name}. \n"
                                      f"Введите пароль\n"
                                      f"Его длина должна быть от 3 до 5 символов\n"
                                      f"он не должен содержать символов,\n"
                                      f"только буквы и цыфры")



def add_question(answer, string):
    logic.add_question_and_answer(string, answer.text, answer.from_user.id)
    bot.send_message(answer.chat.id, "Данные для восстановления пароля добавлены")


def to_add_income_category(message):
    category_lst = logic.get_income_category(message.from_user.id)
    if category_lst:
        show_income_category(message, category_lst)
    else:
        chose_new_income_category(message)


def show_income_category(message, category_list):
    application.set_state("chose_income_category")
    markup = markups.get_markup_for_income_category(category_list)
    bot.send_message(message.chat.id, "Выбери одну из уже добавленных категорий "
                                      "или добавь новую", reply_markup=markup)


def chose_new_income_category(message):
    application.set_state("write_income_category")
    bot.send_message(message.chat.id, "Это твоя первая категория, напиши ее название.")


def input_income(message):
    application.set_state("add_income")
    bot.send_message(message.chat.id, "Введи сумму")




@bot.message_handler(func=lambda message: application.get_state() == "write_income_category")
def new_income_category_handler(message):
    application.set_category(message.text)
    input_income(message)


@bot.message_handler(func=lambda message: application.get_state() == "add_income")
def add_income_message_handler(message):
    if logic.check_income(message.text):
        application.set_state(None)
        logic.add_income(message.text, message.from_user.id, application.get_category())
        bot.send_message(message.chat.id, "Доход добавлен.\n"
                                          "Выбери команду в Меню для продолжения.")
        application.set_category(None)
    else:
        bot.send_message(message.chat.id, "Некорректный ввод!")
        input_income(message)







@bot.message_handler(func=lambda message: application.get_state() == "password recovery")
def check_password_for_recovery(message):
    if message.text == logic.get_answer(message.from_user.id):
        bot.send_message(message.chat.id, f"Твой пароль:  {logic.get_password(message.from_user.id)}")
    else:
        application.set_state(None)
        markup = markups.get_markups_for_password_recovery()
        bot.send_message(message.chat.id, "Ответ неверный. Что будем делать", reply_markup=markup)


@bot.message_handler(func=lambda message: application.get_state() == "authorization")
def text_handler_for_authorization(message):
    if logic.check_password(message.text, message.from_user.id):
        application.set_authorization(True)
        application.set_state(None)
        bot.send_message(message.chat.id, "Авторизация прошла успешно")
    else:
        application.set_state(None)
        markup = markups.continuation_authorization()
        bot.send_message(message.chat.id, "Неверный пароль, что будем делать?", reply_markup=markup)


@bot.message_handler(func=lambda message: application.get_state() == "registration")
def text_handler(message):
    if logic.check_string_for_password(message.text):
        application.set_state(None)
        logic.start_registration(message.from_user.id, message.from_user.first_name, message.text)
        markup = markups.get_markup_for_continue_reg()
        bot.send_message(message.chat.id, "Регистрация успешно завершена!\n"
                                          "Хотите добавить вопрос для восстановления пароля?",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Некорректный ввод,\n"
                                          "Введите от 3 до 5 символов\n"
                                          "пароль не должен содержать символов,\n"
                                          "только буквы и цыфры")


# @bot.message_handler(content_types=["text"])
# def any_text_handler(message):
#     if message.text == "qqq":
#         answer = bot.send_message(message.chat.id, f"{message.text}")
#

 # @bot.message_handler(commands=["back"])
# def start_handler(message):
#     db = DataBase("data")
#     db.get_info()
#     bot.send_message(message.chat.id, message.from_user.id)



# @bot.message_handler(func=lambda message: message.text in ["Да"])
# def input_limit_handler(message):
#     bot.send_message(message.chat.id, 'ok')
#
#
# @bot.message_handler(func=lambda message: message.text in ["ok"])
# def input_limithandler(message):
#     bot.send_message(message.chat.id, 'Да')
#
#
# @bot.message_handler(func=lambda message: message.text in ["ye"])
# def inputlimithandler(message):
#     bot.send_message(message.chat.id, 'ye')



bot.infinity_polling()