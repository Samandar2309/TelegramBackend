import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import requests

bot_token = '6901637071:AAGUjoH4b1daS5dhfFT15tgpMVnNxzZxzx8'
API_URL = 'http://127.0.0.1:8000/api/book/'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(types.KeyboardButton('Location'), types.KeyboardButton('Kitoblar'))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        f'Assalamu alaykum {message.from_user.username}\nKerakli tugmalardan birini tanlashingiz mumkin!',
        reply_markup=main_menu)


@dp.message_handler(text='Location')
async def location(message: types.Message):
    await message.reply(
        "https://www.google.com/maps/place/%D0%90%D0%B9%D1%82%D0%B8+%D0%90%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D1%8F"
        "+%D0%90%D0%B9+%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC/@41.3245781,69.3224523,"
        "17z/data=!3m1!4b1!4m6!3m5!1s0x38aef572e5842f55:0xa87fc261e04f75ea!8m2!3d41.3245741!4d69.3250272!16s%2Fg"
        "%2F11q2vn0m7k?entry=ttu")


@dp.message_handler(text='Kitoblar')
async def book_list(message: types.Message):
    response = requests.get(API_URL)
    if response.status_code == 200:
        books = response.json()
        keyboard = InlineKeyboardMarkup(row_width=2)
        for book in books:
            keyboard.add(InlineKeyboardButton(book['title'], callback_data=f'book_{book["id"]}'))
        await message.answer('Kerakli kitobni tanlashingiz mumkin!', reply_markup=keyboard)
    else:
        await message.answer("Xatolik yuz berdi")


@dp.callback_query_handler(lambda query: query.data.startswith('book_'))
async def book_info(query: types.CallbackQuery):
    await query.answer('Assalamu alaykum')
    try:
        book_id = query.data.split('_')[1]
        response = requests.get(f'{API_URL}{book_id}/')
        if response.status_code == 200:
            book = response.json()
            book_info = (
                f"Title: {book['title']}\nAuthor: {book['author']}\nPrice: {book['price']}\nDescription: {book['description']}"
            )
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Order", callback_data=f'order_{book_id}'))
            keyboard.add(InlineKeyboardButton(text="Back", callback_data='back_to_menu'))
            await query.message.edit_text(book_info, reply_markup=keyboard)
        else:
            await query.answer("Xatolik yuz berdi")
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await bot.send_message(chat_id=query.from_user.id, text="Xatolik yuz berdi")


@dp.callback_query_handler(lambda query: query.data.startswith('order_'))
async def order_book(query: types.CallbackQuery):
    await query.answer(
        "Iltimos, ismingiz va telefon raqamingizni quyidagi formatda kiriting: \nIsm: [Ismingiz] \nTelefon: ["
        "   Raqamingiz]")

    @dp.message_handler()
    async def receive_order(message: types.Message):
        data = message.text.split('\n')
        if len(data) == 2:
            name, phone = data
            # Bu yerda buyurtmani saqlash logikasini qo'shing
            await message.answer(
                f"Raxmat, {name}. Telefon raqamingiz: {phone}\nBuyurtmangiz qabul qilindi, tez orada bog'lanamiz!")
        else:
            await message.answer("Ma'lumotlarni to'g'ri formatda kiriting: \nIsm: [Ismingiz] \nTelefon: [Raqamingiz]")


@dp.callback_query_handler(lambda query: query.data == 'back_to_menu')
async def back_to_menu(query: types.CallbackQuery):
    await query.answer("Orqaga qaytdingiz.")
    await start(query.message)  # Foydalanuvchini asosiy menyuga qaytaring


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
