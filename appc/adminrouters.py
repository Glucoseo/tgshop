import gayboard as kb
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    Message,
)
from middleware import AdminMiddleware, CounterMiddleware
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine_prod = create_engine("sqlite:///products.sqlite")
engine_users = create_engine("sqlite:///users.sqlite")

SessionProd = sessionmaker(bind=engine_prod)
SessionUsers = sessionmaker(bind=engine_users)

prod_session = SessionProd()
users_session = SessionUsers()


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    content = Column(String)
    caption = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, unique=True)


Base.metadata.create_all(engine_prod)
Base.metadata.create_all(engine_users)


admin_router = Router()
admin_router.message.middleware(AdminMiddleware(admin_ids=[123456789]))


class ret(StatesGroup):
    waiting_for_product = State()
    waitmessage = State()
    shop = State()


@admin_router.message(Command("cadmin"))
async def admincom(message: Message):
    await message.answer("Admin panel", reply_markup=kb.admin_panel)


@admin_router.message(ret.waiting_for_product)
async def waitin(message: Message, state: FSMContext):
    if message.text:
        prod_session.add(
            Product(type="text", content=message.text, caption="no caption")
        )
        prod_session.commit()
    if message.photo:
        prod_session.add(
            Product(
                type="photo",
                content=message.photo[-1].file_id,
                caption=message.caption or "no caption",
            )
        )
        prod_session.commit()
    if message.video:
        prod_session.add(
            Product(
                type="video",
                content=message.video.file_id,
                caption=message.caption or "no caption",
            )
        )
        prod_session.commit()
    if message.from_user.id in admins_id:
        await message.answer("Admin panel", reply_markup=kb.admin_panel)
    await state.clear()


@admin_router.message(ret.waitmessage)
async def waitmessage(message: Message, state: FSMContext, bot: Bot):
    users = users_session.query(User).all()
    for user in users:
        try:
            if message.photo:
                await bot.send_photo(
                    chat_id=user.userid,
                    photo=message.photo[-1].file_id,
                    caption=message.caption or "",
                )
            elif message.video:
                await bot.send_video(
                    chat_id=user.userid,
                    video=message.video.file_id,
                    caption=message.caption or "",
                )
            else:
                await bot.send_message(chat_id=user.userid, text=message.text)
        except Exception as e:
            print(f"Failed to send message to {user.userid}: {e}")
    await message.answer("Message sent to all users.")
    await state.clear()


@admin_router.callback_query(F.data == "sendall")
async def sendall(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Write your message. If you have photos, send them together with the text."
    )
    await state.set_state(ret.waitmessage)


@admin_router.callback_query(F.data == "addprod")
async def addp(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Write your message. If you have photos or videos, send them together with the text."
    )
    await state.set_state(ret.waiting_for_product)


@admin_router.callback_query(F.data == "view")
async def admproduct(callback: CallbackQuery):
    await callback.message.answer(
        "here will be the products of your shop", reply_markup=kb.admin_shop
    )
