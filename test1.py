import telebot
from telebot import types

bot = telebot.TeleBot("5873487596:AAF4SZzKOXe_YyF7_uUoNrWxyyChAEhPb3A")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton("Анкета")
    item2 = types.KeyboardButton("QR код")
    item3 = types.KeyboardButton("RSRV столик")
    item4 = types.KeyboardButton("Меню")
    item5 = types.KeyboardButton("Сайт")
    item6 = types.KeyboardButton("Баллы")
    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == "Анкета":
        bot.send_message(message.from_user.id, "Ваш логин?")
        #bot.reply_to(message, "Вы нажали на первую кнопку")
    elif message.text == "Кнопка 2":
        bot.reply_to(message, "Вы нажали на вторую кнопку")
    elif message.text == "Кнопка 3":
        bot.reply_to(message, "Вы нажали на третью кнопку")
    elif message.text == "Кнопка 4":
        bot.reply_to(message, "Вы нажали на четвертую кнопку")
    elif message.text == "Кнопка 5":
        bot.reply_to(message, "Вы нажали на пятую кнопку")
    elif message.text == "Кнопка 6":
        bot.reply_to(message, "Вы нажали на шестую кнопку")
    else:
        bot.reply_to(message, "Я не понимаю, что вы хотите сделать. Пожалуйста, выберите одну из кнопок.")

# Запуск бота
bot.polling()