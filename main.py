import cv2
from pyzbar.pyzbar import decode

import telegram
import telebot
from telebot import types
import sqlite3
import qrcode

def telegramm_base():
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS list_1
           (number INTEGER PRIMARY KEY, name TEXT (30), insta TEXT (50), 
           username TEXT (30), user_id INTEGER (20), sex TEXT (10), qr BLOB, a_p TEXT (10), sur TEXT (20))""")
    cursor.execute('INSERT INTO list_1 (name, insta, username, user_id, sex, qr, a_p) VALUES (?,?,?,?,?,?,?)',
                   (name, insta, username, user_id, sex, image, a_p))
    conn.commit()
    conn.close()

bot = telebot.TeleBot('5873487596:AAF4SZzKOXe_YyF7_uUoNrWxyyChAEhPb3A')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item1 = types.KeyboardButton("📋 Анкета")
    item2 = types.KeyboardButton("🐈 QR код")
    item3 = types.KeyboardButton("RSRV столик")
    item4 = types.KeyboardButton("🍸 Меню")
    item5 = types.KeyboardButton("🖥 Сайт")
    item6 = types.KeyboardButton("📲 Админ")

    markup.add(item1, item2, item3, item4, item5, item6)
    # photo = open('Rasputin_logo_main_gold.png', 'rb')
    # bot.send_photo(message.from_user.id, photo, caption="Привет, это бот клуба Распутин")
    # photo.close()

    bot.send_message(message.from_user.id, "Добро пожаловать! Это бот клуба RASPUTIN. "
                                           "Заполните короткую анкету и станьте нашим клиентом.", reply_markup=markup)

    # keyboard = types.InlineKeyboardMarkup(row_width=2)
    # key_rus = types.InlineKeyboardButton(text='Русский', callback_data='rus')
    # key_engl = types.InlineKeyboardButton(text='English', callback_data='engl')
    # keyboard.add(key_engl, key_rus)
    # bot.send_message(message.from_user.id, text="Выберите язык:", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global user_id
    user_id = message.chat.id
    if message.text == "📋 Анкета":
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
    elif message.text == "🐈 QR код":
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
    elif message.text == "📲 Админ":
        if user_id == 469632258:
            get_admin(message)
        else:
            bot.send_message(message.from_user.id, "Вы не администратор, сорри")
    else:
        bot.send_message(message.from_user.id, "Ну пока...")

def get_admin(message):
    keyboard = types.InlineKeyboardMarkup()
    key_scan = types.InlineKeyboardButton(text='Сканировать', callback_data='scan')
    keyboard.add(key_scan)
    key_active = types.InlineKeyboardButton(text='Активировать', callback_data='active')
    keyboard.add(key_active)
    key_passive = types.InlineKeyboardButton(text='Убрать активный статус', callback_data='passive')
    keyboard.add(key_passive)
    key_del = types.InlineKeyboardButton(text='Удалить пользователя', callback_data='del')
    keyboard.add(key_del)
    key_present = types.InlineKeyboardButton(text='Добавить угощение', callback_data='present')
    keyboard.add(key_present)
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
        cursor.execute("UPDATE list_1 SET a_p = ? WHERE number = ?", ('A', record_id))
        conn.commit()
        bot.send_message(message.chat.id, f"Статус для пользователя {res[1]} активирован")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")
    conn.close()

def get_passive(message):
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list_1 WHERE user_id = ?", (message.text,))
    res = cursor.fetchone()
    if res is not None:
        record_id = res[0]
        cursor.execute("UPDATE list_1 SET a_p = ? WHERE number = ?", ('P', record_id))
        conn.commit()
        bot.send_message(message.chat.id, f"Активный статус для пользователя {res[1]} убран")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")
    conn.close()

def del_user(message):
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list_1 WHERE user_id = ?", (message.text,))
    res = cursor.fetchone()
    if res is not None:
        record_id = res[0]
        cursor.execute("DELETE FROM list_1 WHERE number = ?", (record_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"Пользователь {res[1]} удален")
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
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    key_man = types.InlineKeyboardButton(text='Мужчина', callback_data='man')
    key_woman = types.InlineKeyboardButton(text='Девушка', callback_data='woman')
    keyboard.add(key_man, key_woman)
    bot.send_message(message.from_user.id, text="Хорошо. Последний важный вопрос. Вы мужчина или девушка?", reply_markup=keyboard)

def get_username(call):
    global username
    username = str(call.message.chat.username)
    global sex
    sex = call.data
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Итак: Вас зовут {name}, Ваш инстаграмм: {insta} и Ваш телеграмм: {username}?'
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM list_1")
        res = cursor.fetchall()
        b = 0
        for i in res:
            ii = str(i)
            if str(user_id) == ii[1:-2]:
                bot.send_message(call.message.chat.id, "Пользователь с таким ID уже зарегистрирован")
                b += 1
        if b < 1:
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

    elif call.data == "man" or call.data == "woman":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        get_username(call)

    elif call.data == "scan":

        cap = cv2.VideoCapture(0)
        scanned = False
        while not scanned:
            _, frame = cap.read()
            for code in decode(frame):
                data = code.data.decode('utf-8')
                print(f'Scanned data: {data}')
                scanned = True
                bot.send_message(call.message.chat.id, f'Сканирование завершено. Результат: {data}')

            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


    elif call.data == "active":
        bot.send_message(call.message.chat.id, "Введите ID клиента чтобы присвоить ему активный статус")
        bot.register_next_step_handler(call.message, get_active)

    elif call.data == "passive":
        bot.send_message(call.message.chat.id, "Введите ID клиента чтобы убрать у него активный статус")
        bot.register_next_step_handler(call.message, get_passive)

    elif call.data == "del":
        bot.send_message(call.message.chat.id, "Введите ID клиента, которого хотите удалить")
        bot.register_next_step_handler(call.message, del_user)

    elif call.data == "list":
        bot.send_message(call.message.chat.id, "Зарегистрированы на данный момент:")
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("SELECT number, name, username, user_id, a_p, sex, sur FROM list_1")
        res = cursor.fetchall()
        for i in res:
            a = str(i)
            bot.send_message(call.message.chat.id, a[1:-1])


bot.polling(none_stop=True, interval=0)
