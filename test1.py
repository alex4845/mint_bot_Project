
import qrcode
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from BD import telegramm_base, get_user, get_info, del_user, act_user, get_info_act
from admin_panel import admin_panel


storage = MemoryStorage()

bot = Bot('5873487596:AAF4SZzKOXe_YyF7_uUoNrWxyyChAEhPb3A')
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def info(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item1 = types.KeyboardButton("📋 Анкета")
    item2 = types.KeyboardButton("🐈 QR код")
    item3 = types.KeyboardButton("RSRV столик")
    item4 = types.KeyboardButton("🍸 Меню")
    item5 = types.KeyboardButton("🖥 Сайт")
    item6 = types.KeyboardButton("📲 Админ")
    markup.add(item1, item2, item3, item4, item5, item6)

    await message.answer('Добро пожаловать! Это бот клуба RASPUTIN.'
                         ' Заполните короткую анкету и получайте от нас угощение.', reply_markup=markup)

class FSMclient(StatesGroup):
    name = State()
    insta = State()
    sex = State()

class FSMadmin(StatesGroup):
    id = State()

class FSMadmin1(StatesGroup):
    act = State()

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=None)
async def get_start(message: types.Message):
    if message.text == '📋 Анкета':
        a = message.chat.id
        res = await get_user(a)
        if res == None:
            await FSMclient.name.set()
            await message.reply('Ваше имя/логин')
        else:
            await message.reply('Вы уже зарегистрированы')

    if message.text == '📲 Админ':
        if message.chat.id == 469632258:
            await admin_panel(message)
        else:
            await message.answer('Извините, вы не админ')

    if message.text == '🐈 QR код':
        a = message.chat.id
        res = await get_user(a)
        await bot.send_photo(message.chat.id, photo=res[6], caption="Ваш QR код")


@dp.message_handler(content_types=['text'], state=FSMclient.name)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMclient.next()
    await message.reply('Ваш инстаграмм')

@dp.message_handler(content_types=['text'], state=FSMclient.insta)
async def get_insta(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['insta'] = message.text
    await FSMclient.next()
    await message.reply('Ваш пол: М или Ж')

@dp.message_handler(content_types=['text'], state=FSMclient.sex)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sex'] = message.text
        data['username'] = message.chat.username
        data['user_id'] = message.chat.id

        dat = [message.chat.id]
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(dat)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save("qr_code.png")
        with open('qr_code.png', 'rb') as f:
            image = f.read()
        data['qr'] = image

    await telegramm_base(state)
    await bot.send_photo(message.chat.id, photo=image, caption="Вы зарегистрированы. Вот Ваш QR код")

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_button1(callback_query: types.CallbackQuery):
    a = await get_info()
    for i in a:
        await bot.send_message(callback_query.from_user.id, text=i)
    #await bot.answer_callback_query(callback_query.id, text=a, show_alert=True)

@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_button2(callback_query: types.CallbackQuery):
    await FSMadmin.id.set()
    await bot.send_message(callback_query.from_user.id, text='Введите ID клиента, которого хотите удалить')

@dp.message_handler(content_types=['text'], state=FSMadmin.id)
async def del_us(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
        a = data['id']
        res = await del_user(a)
    await message.answer(res)

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'button3')
async def process_button3(callback_query: types.CallbackQuery):
    await FSMadmin1.act.set()
    await bot.send_message(callback_query.from_user.id, text='Введите ID клиента для активации')

@dp.message_handler(content_types=['text'], state=FSMadmin1.act)
async def act_us(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['act'] = message.text
        a = data['act']
        b = await get_user(a)
        if b == None:
            await message.answer("Пользователь не найден в базе данных")
        else:
            res = await act_user(b)
            await message.answer(res)

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'button4')
async def process_button4(callback_query: types.CallbackQuery):
    a = await get_info_act()
    for i in a:
        await bot.send_message(callback_query.from_user.id, text=i)


executor.start_polling(dp)


