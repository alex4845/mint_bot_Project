from aiogram import Bot, types


async def admin_panel(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Список всех', callback_data='button1')
    button2 = types.InlineKeyboardButton(text='Удалить пользователя', callback_data='button2')
    button4 = types.InlineKeyboardButton(text='Список активированных', callback_data='button4')
    keyboard.add(button1, button2, button4)
    await message.answer("Варианты действий:", reply_markup=keyboard)


async def gender(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1_0 = types.InlineKeyboardButton(text='Мужчина', callback_data='М')
    button2_0 = types.InlineKeyboardButton(text='Девушка', callback_data='Ж')
    keyboard.add(button1_0, button2_0)
    await message.answer("Вы", reply_markup=keyboard)


async def get_manager(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    manager1 = types.InlineKeyboardButton(text='manager #1', callback_data='man1')
    manager2 = types.InlineKeyboardButton(text='manager #2', callback_data='man2')
    manager3 = types.InlineKeyboardButton(text='manager #3', callback_data='man3')
    manager4 = types.InlineKeyboardButton(text='manager #4', callback_data='man4')
    manager5 = types.InlineKeyboardButton(text='manager #5', callback_data='man5')
    keyboard.add(manager1, manager2, manager3, manager4, manager5)
    await message.answer("Выберите своего менеджера. Заменить его можно только завтра!", reply_markup=keyboard)
