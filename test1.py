import telebot

bot = telebot.TeleBot('5873487596:AAF4SZzKOXe_YyF7_uUoNrWxyyChAEhPb3A')

@bot.message_handler(commands=['start'])
def start_message(message):
    sent = bot.send_message(message.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(sent, hello_message)

def hello_message(message):
    bot.delete_message(message.chat.id, message.message_id - 1)  # удаление предыдущего сообщения бота
    bot.send_message(message.chat.id, 'Как дела?')

bot.polling()