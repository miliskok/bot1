# Телеграм-бот v.002 - бот создаёт меню, присылает собачку, и анекдот
from io import BytesIO

import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types

import requests
import bs4
import json

import menu
import dz
import botGames

# import botGames  # бот-игры, файл botGames.py
# from menuBot import menu, Users  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню


bot = telebot.TeleBot('5106619300:AAFyqqh_FvARsb5E_sATTgar1De4cqgjHOE')  # Создаем экземпляр бота


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start


# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAIaeWJEeEmCvnsIzz36cM0oHU96QOn7AAJUAANBtVYMarf4xwiNAfojBA")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=menu.Menu.getMenu(chat_id, "Главное меню").markup)


# -----------------------------------------------------------------------


# Получение голосовухи от юзера
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)


# Получение фото от юзера
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# Получение видео от юзера
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------
# Получение контактов от юзера
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text
    result = goto_menu(chat_id, ms_text)
    # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = menu.Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "/dog" or ms_text == "Прислать собаку":
            bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")

        elif ms_text == "Прислать анекдот":
            bot.send_message(chat_id, text=get_anekdot())

        elif ms_text == "Прислать новости":
            bot.send_message(chat_id, text=get_news())

        elif ms_text == "WEB-камера":
            key1 = types.InlineKeyboardMarkup()
            img2 = open('собака.jpg', 'rb')
            bot.send_photo(message.chat.id, img2, reply_markup=key1)

        elif ms_text == "Помощь" or ms_text == "/help":
            if ms_text == "Помощь":
                send_help(chat_id)

        elif ms_text == 'Прислать дз':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            n1 = types.KeyboardButton('Задание номер 1')
            n2 = types.KeyboardButton('Задание номер 2')
            n3 = types.KeyboardButton('Задание номер 3')
            n4 = types.KeyboardButton('Задание номер 4')
            n5 = types.KeyboardButton('Задание номер 5')
            n6 = types.KeyboardButton('Задание номер 6')
            n7 = types.KeyboardButton('Задание номер 7')
            n8 = types.KeyboardButton('Задание номер 8')
            n9 = types.KeyboardButton('Задание номер 9')
            n10 = types.KeyboardButton('Задание номер 10')
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, back)
            bot.send_message(chat_id, text="домашка", reply_markup=markup)
        elif ms_text == 'Задание номер 1':
            dz.dz1(bot, chat_id)
        elif ms_text == 'Задание номер 2':
            dz.dz2(bot, chat_id)
        elif ms_text == 'Задание номер 3':
            dz.dz3(bot, chat_id)
        elif ms_text == 'Задание номер 4':
            dz.dz4(bot, chat_id)
        elif ms_text == 'Задание номер 5':
            dz.dz5(bot, chat_id)
        elif ms_text == 'Задание номер 6':
            dz.dz6(bot, chat_id)
        elif ms_text == 'Задание номер 7':
            dz.dz7(bot, chat_id)
        elif ms_text == 'Задание номер 8':
            dz.dz8(bot, chat_id)
        elif ms_text == 'Задание номер 9':
            dz.dz9(bot, chat_id)
        elif ms_text == 'Задание номер 10':
            dz.dz10(bot, chat_id)
        elif ms_text == 'Прислать гороскоп':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            req_goro = requests.get('https://horo.mail.ru')
            soup = bs4.BeautifulSoup(req_goro.text, 'html.parser')
            result_find = soup.findAll('div', class_="article__item article__item_alignment_left article__item_html")
            bot.send_message(chat_id, text=str(result_find))
        elif ms_text == 'Прислать котика':
            url = ""
            req = requests.get('https://api.catboys.com')
            if req.status_code == 200:
                r_json = req.json()
                url = r_json['url']
                # url.split("/")[-1]
            return url
        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)
        elif ms_text == "Карту!":
            game21 = botGames.getGame(chat_id)
            if game21 is None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status is not None:  # выход, если игра закончена
                botGames.stopGame(chat_id)
                goto_menu(chat_id, "Выход")
                return

        elif ms_text == "Стоп!":
            botGames.stopGame(chat_id)
            goto_menu(chat_id, "Выход")
            return

        elif ms_text in botGames.GameRPS.values:
            # реализация игрыы Камень-ножницы-бумага
            gameRSP = botGames.getGame(chat_id)
            if gameRSP is None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return
            text_game = gameRSP.playerChoice(ms_text)
            bot.send_message(chat_id, text=text_game)
            gameRSP.newGame()

        else:
            bot.send_message(chat_id, text="Я тебя слышу!!! Ваше сообщение: " + ms_text)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки, использовать методы
    # Menu.getExtPar() и Menu.setExtPar()
    pass
    # if call.data == "ManOrNot_GoToSite": #call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    #
    # # После обработки каждого запроса нужно вызвать метод answer_callback_query, чтобы Telegram понял, что запрос
    # обработан. bot.answer_callback_query(call.id)


# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = menu.Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu is not None and cur_menu.parent is not None:
        target_menu = menu.Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = menu.Menu.getMenu(chat_id, name_menu)

    if target_menu is not None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Камень, ножницы, бумага":
            gameRSP = botGames.newGame(chat_id, botGames.GameRPS())  # создаём новый экземпляр игры
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу"
            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg", caption=text_game,
                           parse_mode='HTML')

        return True
    else:
        return False


# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias


# ---------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: милашк ")
    key1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите мне", url="https://t.me/p1zdyushka")
    key1.add(btn1)
    img3 = open('пип.png', 'rb')
    bot.send_photo(chat_id, img3, reply_markup=key1)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menu.Users.activeUsers:
        bot.send_message(chat_id, menu.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')


def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""


def get_news():
    array_news = []
    req_news = requests.get('https://www.banki.ru/news/lenta')
    if req_news.status_code == 200:
        soup = bs4.BeautifulSoup(req_news.text, "html.parser")
        result_find = soup.select('.doFpcq')
        for result in result_find:
            print(result)
    if len(array_news) > 0:
        return array_news[0]
    else:
        return ""


def get_ManOrNot(chat_id):
    global bot

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить",
                                      url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
bot.polling(none_stop=True, interval=0)  # Запускаем бота
