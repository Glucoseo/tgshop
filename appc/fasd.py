from aiogram import F, Router, Bot, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, InputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
import pandas as pd
import sqlite3
import gays as kb
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
users_cursor.execute("SELECT id FROM your_table")
ids = users_cursor.fetchall()

router = Router()
admins_id = [5340682838]
class ret(StatesGroup):
    waiting_for_product = State()

@router.message(ret.waiting_for_product)
async def waitin(message: Message, state: FSMContext):
    await state.update_data()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if message.from_user.id in admins_id:
        await message.answer("Hello admin",reply_markup = kb.admin_panel)
    else:
        await state.update_data(user_id=message.from_user.id)
        data = await state.get_data()
        users_conn.execute("INSERT INTO users (userid) VALUES (?)",
        (data.get('message.from_user.id', 'не указано')))
        users_conn.commit()
        await message.answer("Its smth SHOP! Welcome press products button to shop.", reply_markup=kb.start)

@router.callback_query(F.data == 'sendall')
async def sendall(callback: CallbackQuery):
    await callback.message.answer("Write your message. If you have photos, send them together with the text.")
    for id_tuple in ids:
        id = id_tuple[0]
        print(f"Обрабатываю id: {id}")

@router.callback_query(F.data == 'addprod')
async def addp(message: Message, state:FSMContext, callback: CallbackQuery):
    await callback.message.answer("Write your message. If you have photos, send them together with the text.")
    await state.set_state(ret.waiting_for_product)
    
@router.callback_query(F.data == 'shop')
async def product(callback: CallbackQuery):
    await callback.message.answer("here will be the products of your shop", reply_markup=kb.shop)

@router.callback_query(F.data == 'view')
async def admproduct(callback: CallbackQuery):
    await callback.message.answer("here will be the products of your shop", reply_markup=kb.admin_shop)

@router.callback_query(F.data == 'sexyboi')
async def subcheck(callback: CallbackQuery, bot: Bot):
    await callback.answer('')
    user_channel_status = await bot.get_chat_member(chat_id='@testttae', user_id=callback.from_user.id)

    if user_channel_status.status != 'left':
        await callback.message.answer('Спасибо за подписку!', reply_markup=kb.getmat)
        
    else:
        await callback.message.answer('Для начала подпишись на наш канал')



