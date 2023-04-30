
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
           username TEXT (30), user_id INTEGER (20), age INTEGER (5), qr BLOB)""")
    cursor.execute('INSERT INTO list_1 (name, insta, username, user_id, age, qr) VALUES (?,?,?,?,?,?)',
                   (name, insta, username, user_id, age, image))
    conn.commit()
    conn.close()


bot = telebot.TeleBot('5873487596:AAF4SZzKOXe_YyF7_uUoNrWxyyChAEhPb3A')
# keyboard = [
#     [InlineKeyboardButton("Кнопка 1", callback_data='button1'),
#      InlineKeyboardButton("Кнопка 2", callback_data='button2')],
#     [InlineKeyboardButton("Кнопка 3", callback_data='button3'),
#      InlineKeyboardButton("Кнопка 4", callback_data='button4')]
# ]
#
# reply_markup = InlineKeyboardMarkup(keyboard)
#
# #pinned_message = bot.get_chat(chat_id='6117171405').pinned_message
#
# bot.edit_message_reply_markup(chat_id='6117171405', message_id=message_id, reply_markup=reply_markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global user_id
    user_id = message.chat.id
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Если ты хочешь участвовать в специальной программе"
                                               " бара 'МЯТА' с раздачей угощений, то пройди короткую процедуру регистрации."
                                               " Отправь 'да', если хочешь начать процесс регистрации")
    elif message.text == "да" or message.text == "Да":
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM list_1")
        res = cursor.fetchall()
        a = 0
        for i in res:
            ii = str(i)
            if str(user_id) == ii[1:-2]:
                bot.send_message(message.from_user.id, "Вы уже зарегистрированы")
                cursor.execute("SELECT qr FROM list_1 WHERE user_id = ?", (user_id,))
                image_data = cursor.fetchone()[0]
                bot.send_photo(message.chat.id, photo=image_data)
                a = a + 1
        if a < 1:
            bot.send_message(message.from_user.id, "Ваше имя (login)?")
            bot.register_next_step_handler(message, get_name)
    elif message.text == "Все" or message.text == "все":
        bot.send_message(message.from_user.id, "Зарегистрированы на данный момент:")
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT number, name, username FROM list_1")
        res = cursor.fetchall()
        for i in res:
            a = str(i)
            bot.send_message(message.from_user.id, a[1:-1])
    elif message.text == "очистить":
        bot.send_message(message.from_user.id, "данные удалены")
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM list_1")
        conn.commit()
    else:
        bot.send_message(message.from_user.id, "Ну пока...")

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
    print(user_id, username)
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
        data = [name, insta, username, user_id, age]
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save("qr_code.png")

        global image
        with open('qr_code.png', 'rb') as f:
            image = f.read()
        bot.send_photo(call.message.chat.id, photo=image)

        telegramm_base()

    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Что-то не так? Пишите "да" и повторите регистрацию')

bot.polling(none_stop=True, interval=0)
