import asyncio
import io
import os

import qrcode
from datetime import datetime
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from BD import telegramm_base, get_user, get_info, del_user, get_info_act, interval, write_manager
from admin_panel import admin_panel, gender, get_manager

storage = MemoryStorage()

bot = Bot('5873487596:AAF4SZzKOXe_YyF7_uUoNrWxyyChAEhPb3A')
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def info(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item1 = types.KeyboardButton("📋 Зарегистрироваться")
    item2 = types.KeyboardButton("🐈 QR код")
    item3 = types.KeyboardButton("RSRV столик")
    item4 = types.KeyboardButton("🍸 Меню")
    item5 = types.KeyboardButton("⭐ Best Manager")
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

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=None)
async def get_start(message: types.Message):
    if message.text == '📋 Зарегистрироваться':
        a = message.chat.id
        res = await get_user(a)
        if res == None:
            await FSMclient.name.set()
            await message.reply('Ваше имя (логин)')
        else:
            await message.reply('Вы уже зарегистрированы')

    if message.text == '📲 Админ':
        if message.chat.id == 469632258 or message.chat.id == 686296818:
            await admin_panel(message)
        else:
            await message.answer('Извините, вы не админ')

    if message.text == '🐈 QR код':
        a = message.chat.id
        res = await get_user(a)
        await bot.send_photo(message.chat.id, photo=res[6], caption="Ваш QR код")

    if message.text == '⭐ Best Manager':
        a = message.chat.id
        res = await get_user(a)
        if res:
            if res[5] != "Ж":
                await message.answer('Извините, вам эта функция не доступна')
            else:
                await get_manager(message)
        else:
            await message.answer("Пройдите пожалуйста регистрацию")

    if message.text == 'RSRV столик':
        await message.answer("Для заказа столика свяжитесь с нашим администратором https://t.me/endry_7979")

    if message.text == '🍸 Меню':
        with open('menu_foto/photo_2023-07-30_12-07-50.jpg', 'rb') as f1:
            image = io.BytesIO(f1.read())
        await bot.send_photo(message.chat.id, photo=image, caption="Вашему вниманию - следующие напитки:")
        with open('menu_foto/photo_2023-07-30_12-54-41.jpg', 'rb') as f2:
            image1 = io.BytesIO(f2.read())

        with open('menu_foto/photo_2023-07-30_12-54-48.jpg', 'rb') as f3:
             image2 = io.BytesIO(f3.read())
        with open('menu_foto/photo_2023-07-30_13-07-00.jpg', 'rb') as f4:
             image3 = io.BytesIO(f4.read())
        with open('menu_foto/photo_2023-07-30_13-07-11.jpg', 'rb') as f5:
             image4 = io.BytesIO(f5.read())
        with open('menu_foto/photo_2023-07-30_13-07-17.jpg', 'rb') as f6:
             image5 = io.BytesIO(f6.read())
        media = [
            types.InputMediaPhoto(media=image1, caption="Крепкие напитки"),
            types.InputMediaPhoto(media=image2, caption="Крепкие напитки"),
            types.InputMediaPhoto(media=image3, caption="Вино, пиво"),
            types.InputMediaPhoto(media=image4, caption="Коктейли"),
            types.InputMediaPhoto(media=image5, caption="Коктейли"),
        ]
        await bot.send_media_group(message.chat.id, media=media)

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
        data['username'] = message.chat.username
        data['user_id'] = message.chat.id
    await FSMclient.next()
    await gender(message)

@dp.callback_query_handler(lambda c: c.data in ['М', 'Ж'], state=FSMclient.sex)
async def process_button1_0(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    async with state.proxy() as data:
        data['sex'] = callback_query.data

        dat = callback_query.from_user.id
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(dat)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save("qr_code.png")
        with open('qr_code.png', 'rb') as f:
            image = f.read()
        data['qr'] = image

    await telegramm_base(state)
    await bot.send_photo(callback_query.from_user.id, photo=image, caption="Вы зарегистрированы. Вот Ваш QR код")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_button1(callback_query: types.CallbackQuery):
    a = await get_info()
    await bot.send_message(callback_query.from_user.id, text=f'Всех зарегистрированных: {a[0][0]}. Из них мужчин: '
                                                             f'{a[1][0]}. Женщин: {a[2][0]}')

@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_button2(callback_query: types.CallbackQuery):
    await FSMadmin.id.set()
    await bot.send_message(callback_query.from_user.id, text='Введите ID клиента, которого хотите удалить')

@dp.callback_query_handler(lambda c: c.data in ['man1', 'man2', 'man3', 'man4', 'man5'])
async def process_manager(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    a = callback_query.data
    u = callback_query.from_user.id
    r = await write_manager(a, u)
    await bot.send_message(callback_query.from_user.id, text=r)

@dp.message_handler(content_types=['text'], state=FSMadmin.id)
async def del_us(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
        a = data['id']
        res = await del_user(a)
    await message.answer(res)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'button4')
async def process_button4(callback_query: types.CallbackQuery):
    a = await get_info_act()
    if a:
        await bot.send_message(callback_query.from_user.id, text="Активированы:")
        for i in a:
            await bot.send_message(callback_query.from_user.id, text=f"{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}, {i[5]},"
                                                                     f"{i[6]}, {i[7]}, {i[8]}, {i[9]}")
    else:
        await bot.send_message(callback_query.from_user.id, text="Активированных нет")

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        l_sur = await interval()
        if l_sur:
            if l_sur == "fin":
                chat_id = 469632258 # кому отправлять отчет
                t_n1 = datetime.now().strftime("%Y-%m-%d")
                filename = f'Отчет_{t_n1}.xlsx'
                with open(f'reports/{filename}', 'rb') as file:
                    await bot.send_document(chat_id=chat_id, document=file)
            else:
                for i in l_sur:
                    await bot.send_message(i, 'Вам угощение! Уточняйте на баре. Приятного отдыха!')

loop = asyncio.get_event_loop()
loop.create_task(scheduled(300))
executor.start_polling(dp, loop=loop, skip_updates=True)




