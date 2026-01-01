from aiogram import F, Router, Bot, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, InputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
import sqlite3
import appc.gayboard as kb
prod_conn = sqlite3.connect("products.sqlite")
prod_cursor = prod_conn.cursor()
prod_cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    content TEXT,
    caption TEXT
)
""")
prod_conn.commit()


users_conn = sqlite3.connect("users.sqlite")
users_cursor = users_conn.cursor()

users_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    userid INTEGER
)
""")
users_conn.commit()
users_cursor.execute("SELECT id FROM users")
ids = users_cursor.fetchall()

router = Router()
admins_id = [5340682838]
class ret(StatesGroup):
    waiting_for_product = State()
    waitmessage = State()
    shop = State()

prodcounter = 0

@router.message(ret.waiting_for_product)
async def waitin(message: Message, state: FSMContext):
    if message.text:
        prod_cursor.execute("INSERT INTO products (type, content, caption) VALUES (?, ?, ?)",
        ('text', message.text, 'no caption'))
        prod_conn.commit()
    if message.photo:
        prod_cursor.execute("INSERT INTO products (type, content, caption) VALUES (?, ?, ?)",
        ('photo', message.photo[-1].file_id, message.caption or 'no caption'))
        prod_conn.commit()
    if message.video:
        prod_cursor.execute("INSERT INTO products (type, content, caption) VALUES (?, ?, ?)",
        ('video', message.video.file_id, message.caption or 'no caption'))
        prod_conn.commit()
    if message.from_user.id in admins_id:
        await message.answer("Admin panel", reply_markup=kb.admin_panel)
    await state.clear()

@router.message(CommandStart())
async def cmd_start(bot: Bot, message: Message, state: FSMContext):
    if message.from_user.id in admins_id:
        await message.answer("Hello admin " \
        "You can reach admin panel by writing /cadmin",reply_markup = kb.admin_panel)
    else:
        await state.update_data(user_id=message.from_user.id)
        data = await state.get_data()
        users_conn.execute("INSERT INTO users (userid) VALUES (?)",
        (data.get('message.from_user.id', 'не указано')))
        users_conn.commit()
        await bot.send_document(chat_id=message.from_user.id, document=FSInputFile("D:\\shopbot\\YOUR LOGO.png"), reply_markup=kb.start, caption="Its smth SHOP! Press products button below to shop.")

@router.message(Command("cadmin"))
async def admincom(message: Message):
    if message.from_user.id in admins_id:
        await message.answer("Admin panel", reply_markup=kb.admin_panel)
    else:
        await message.answer("Access denied.", reply_markup=kb.start)

@router.message(ret.waitmessage)
async def waitmessage(message: Message, state: FSMContext, bot: Bot):  
    users_cursor.execute("SELECT userid FROM users")
    ids = users_cursor.fetchall()
    for user_id in ids:
        try:
            if message.photo:
                await bot.send_photo(chat_id=user_id[0], photo=message.photo[-1].file_id, caption=message.caption or "")
            elif message.video:
                await bot.send_video(chat_id=user_id[0], video=message.video.file_id, caption=message.caption or "")
            else:
                await bot.send_message(chat_id=user_id[0], text=message.text)
        except Exception as e:
            print(f"Failed to send message to {user_id[0]}: {e}")
    if message.from_user.id in admins_id:
        await message.answer("Admin panel", reply_markup=kb.admin_panel)
    await message.answer("Message sent to all users.")
    await state.clear()

@router.callback_query(F.data == 'sendall')
async def sendall(callback: CallbackQuery,  state: FSMContext):
    await callback.message.answer("Write your message. If you have photos, send them together with the text.")
    await state.set_state(ret.waitmessage)  
    

@router.callback_query(F.data == 'addprod')
async def addp(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Write your message. If you have photos or videos, send them together with the text.")
    await state.set_state(ret.waiting_for_product)
    
@router.callback_query(F.data == 'shop')
async def product(callback: CallbackQuery):
    await callback.message.answer("here will be the products of your shop", reply_markup=kb.shop)

@router.callback_query(F.data == 'view')
async def admproduct(callback: CallbackQuery):
    await callback.message.answer("here will be the products of your shop", reply_markup=kb.admin_shop)


