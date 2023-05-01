
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import telebot
from telebot import types
import sqlite3
import qrcode

def telegramm_base():
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS list_1
           (number INTEGER PRIMARY KEY, name TEXT (30), insta TEXT (50), 
           username TEXT (30), user_id INTEGER (20), age INTEGER (5), qr BLOB, a_p TEXT (10))""")
    cursor.execute('INSERT INTO list_1 (name, insta, username, user_id, age, qr, a_p) VALUES (?,?,?,?,?,?,?)',
                   (name, insta, username, user_id, age, image, a_p))
    conn.commit()
    conn.close()


bot = telebot.TeleBot('5873487596:AAF4SZzKOXe_YyF7_uUoNrWxyyChAEhPb3A')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton("Анкета")
    item2 = types.KeyboardButton("QR код")
    item3 = types.KeyboardButton("RSRV столик")
    item4 = types.KeyboardButton("Меню")
    item5 = types.KeyboardButton("Сайт")
    item6 = types.KeyboardButton("Админ")
    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global user_id
    user_id = message.chat.id
    if message.text == "Анкета":

        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM list_1")
        res = cursor.fetchall()
        a = 0
        for i in res:
            ii = str(i)
            if str(user_id) == ii[1:-2]:
                bot.send_message(message.from_user.id, "Вы уже зарегистрированы")
                a = a + 1
        if a < 1:
            bot.send_message(message.from_user.id, "Ваше имя (login)?")
            bot.register_next_step_handler(message, get_name)
    elif message.text == "QR код":
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM list_1")
        res = cursor.fetchall()
        a = 0
        for i in res:
            ii = str(i)
            if str(user_id) == ii[1:-2]:
                cursor.execute("SELECT qr FROM list_1 WHERE user_id = ?", (user_id,))
                image_data = cursor.fetchone()[0]
                bot.send_photo(message.chat.id, photo=image_data, caption='Ваш QR код')
                a += 1
        if a < 1:
            bot.send_message(message.from_user.id, "Пройдите анкету")

    elif message.text == "Админ":
        get_admin(message)

    elif message.text == "очистить":
        bot.send_message(message.from_user.id, "Последняя запись удалена")
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM list_1 WHERE number = (SELECT MAX(number) FROM list_1)")
        conn.commit()
    else:
        bot.send_message(message.from_user.id, "Ну пока...")

def get_admin(message):
    keyboard = types.InlineKeyboardMarkup()
    key_active = types.InlineKeyboardButton(text='Активировать', callback_data='active')
    keyboard.add(key_active)
    key_remade = types.InlineKeyboardButton(text='Изменить', callback_data='remade')
    keyboard.add(key_remade)
    key_list = types.InlineKeyboardButton(text='Список', callback_data='list')
    keyboard.add(key_list)
    bot.send_message(message.from_user.id, text="Выберите действие:", reply_markup=keyboard)


def get_active(message):
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list_1 WHERE user_id = ?", (message.text,))
    res = cursor.fetchone()
    if res is not None:
        record_id = res[0]
        print(record_id)
        cursor.execute("UPDATE list_1 SET a_p = ? WHERE number = ?", ('A', record_id))
        conn.commit()
        bot.send_message(message.chat.id, f"Статус для пользователя {res[1]} активирован")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")
    conn.close()


def get_name(message):
    global name
    name = str(message.text)
    bot.send_message(message.from_user.id, f"Ваш instagramm, {message.text}?")
    bot.register_next_step_handler(message, get_insta)

def get_insta(message):
    global insta
    insta = str(message.text)
    bot.send_message(message.from_user.id, "Хорошо. Вы даете согласие на то, чтобы мы запомнили ваши данные и иногда напоминали о себе?")
    bot.register_next_step_handler(message, get_yesorno)

def get_yesorno(message):
    global username
    username = message.from_user.username
    if message.text == "да" or message.text == "Да":
        bot.send_message(message.from_user.id, "Ок, спасибо")
        bot.send_message(message.from_user.id, "Последний вопрос. Ваш возраст? Только цифры, можно округлить))")
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.from_user.id, "Ну пока...")

def get_age(message):
    global age
    age = str(message.text)
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Вам {age} лет, Вас зовут {name}, Ваш инстаграмм: {insta} и Ваш телеграмм: {username}?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Вы записаны. Получите Ваш QR код. Спасибо')
        data = [user_id]
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save("qr_code.png")

        global image
        with open('qr_code.png', 'rb') as f:
            image = f.read()
        bot.send_photo(call.message.chat.id, photo=image)
        global a_p
        a_p = "P"
        telegramm_base()

    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Что-то не так? Жмите "Анкета" и повторите регистрацию')

    elif call.data == "active":
        bot.send_message(call.message.chat.id, "Введите ID клиента")
        bot.register_next_step_handler(call.message, get_active)

    elif call.data == "list":
        bot.send_message(call.message.chat.id, "Зарегистрированы на данный момент:")
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT number, name, username, user_id, a_p FROM list_1")
        res = cursor.fetchall()
        for i in res:
            a = str(i)
            bot.send_message(call.message.chat.id, a[1:-1])


bot.polling(none_stop=True, interval=0)
