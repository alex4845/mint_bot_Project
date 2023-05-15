from aiogram import Bot, types





async def admin_panel(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text='Список всех', callback_data='button1')
    button2 = types.InlineKeyboardButton(text='Удалить пользователя', callback_data='button2')
    button3 = types.InlineKeyboardButton(text='Активировать', callback_data='button3')
    button4 = types.InlineKeyboardButton(text='Список активированных', callback_data='button4')
    keyboard.add(button1, button2, button3, button4)
    await message.answer("Варианты действий:", reply_markup=keyboard)

