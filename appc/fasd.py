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
from middleware import CounterMiddleware
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

router = Router()
router.message.middleware(CounterMiddleware())

router = Router()
admins_id = [5340682838]


class ret(StatesGroup):
    waiting_for_product = State()
    waitmessage = State()
    shop = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in admins_id:
        await message.answer(
            "Hello admin You can reach admin panel by writing /cadmin",
            reply_markup=kb.admin_panel,
        )
    else:
        users_session.add(User(userid=message.from_user.id))
        users_session.commit()
        await message.send_document(
            chat_id=message.from_user.id,
            document=FSInputFile("D:\\shopbot\\YOUR LOGO.png"),
            reply_markup=kb.start,
            caption="Its smth SHOP! Press products button below to shop.",
        )


@router.callback_query(F.data == "shop")
async def product(callback: CallbackQuery):
    await callback.message.answer(
        "here will be the products of your shop", reply_markup=kb.shop
    )
