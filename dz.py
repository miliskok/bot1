from telebot import types


def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)


# -----------------------------------------------------------------------
def my_inputInt(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt,
                                   ResponseHandler=ResponseHandler)


def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        if message.content_type != "text":
            raise ValueError
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                                 text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже


def dz1(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    name = my_input('Введите свое имя')
    bot.send_message(chat_id, text="обычно тебя зовут-" + name)


def dz2(bot, chat_id):
    age = my_inputInt('Введите свой возраст')
    bot.send_message(chat_id, text="твой возраст " + (str(age)))


def dz3(bot, chat_id):
    age2 = my_inputInt('Введите свой возраст')
    bot.send_message(chat_id, (str(age2)) * 5)


def dz4(bot, chat_id):
    name2 = my_input('как тебя зовут?')
    age3 = my_inputInt('сколько тебе лет?')
    bot.send_message(chat_id, text="ку," + name2)


def dz5(bot, chat_id):
    user_age = my_inputInt("сколько тебе лет?")
    if user_age > 30:
        bot.send_message(chat_id,
                         text="Судья говорит свидетельнице: -Ваш возраст? -Все дают мне 18 лет! -Будете выдумывать, я вам сейчас пожизненное дам")
    if user_age < 18:
        bot.send_message(chat_id,
                         text="ты сейчас в таком возрасте, что покупая новые ботинки, должен задуматься: а не в них ли меня будут хоронить?")
    else:
        bot.send_message(chat_id, text="вы где то между 18 и 30 - shit")


def dz6(bot, chat_id):
    name3 = my_input('Введите свое имя')
    lenght = len(name3)
    bot.send_message(chat_id, str(name3[1:lenght - 1:]))
    bot.send_message(chat_id, str(name3[:: -1]))
    bot.send_message(chat_id, str(name3[-3::]))
    bot.send_message(chat_id, str(name3[0:5:]))


def dz7(bot, chat_id):
    name4 = my_input('Введите свое имя')
    bot.send_message(chat_id, text='букв в твоеи имени: ' + str(len(name4)))
    user_age2 = my_inputInt("сколько тебе лет?")
    suma = 0
    nesuma = 1
    while user_age2 > 0:
        digit = user_age2 % 10
        suma = suma + digit
        nesuma = nesuma * digit
        user_age2 = user_age2 // 10
        bot.send_message(chat_id, text='сумма чисел твоего возраста: ' + str(suma))
        bot.send_message(chat_id, text='произведение чисел твоего возраста: ' + str(nesuma))


def dz8(bot, chat_id):
    name4 = my_input('Введите свое имя')
    bot.send_message(chat_id, name4.title())
    bot.send_message(chat_id, name4.lower())
    bot.send_message(chat_id, name4.upper())


def dz9(bot, chat_id):
    while True:
        user_age2 = my_input('сколько тебе лет?')
        if not user_age2.isnumeric():
            bot.send_message(chat_id, text='вы ввели не число, ошибка')
        elif not 0 <= int(user_age2) <= 150:
            bot.send_message(chat_id, text='ваше число не входит в диапазон существующих')
        else:
            bot.send_message(chat_id, text='ok')
        break


def dz10(bot, chat_id):
    key = types.InlineKeyboardMarkup()
    name44 = my_input('введите свое имя')
    if name44.isalpha() or name44.isspace():
        bot.send_message(chat_id, text='ok')
    else:
        bot.send_message(chat_id, text='bad')
