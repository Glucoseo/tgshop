from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


afterreg=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Tg channel", url='https://t.me/testttae')],
                                               [InlineKeyboardButton(text="Check for sub", callback_data='subcheck')]])

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text = "Add product", callback_data="addprod")],
                     [InlineKeyboardButton(text="View products", callback_data="view")],
                     [InlineKeyboardButton(text="Send message to all users", callback_data="sendall")]
                     
])

shop = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Buy",callback_data="buy")],
     [InlineKeyboardButton(text="Previous", callback_data="prev"),InlineKeyboardButton(text="Next",callback_data="next")]])
admin_shop = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Delete",callback_data="delete")],
     [InlineKeyboardButton(text="Previous", callback_data="prev"),InlineKeyboardButton(text="Next",callback_data="next")]])
start = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text = "Products", callback_data="shop")]
                     ])

request_contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Отправить контакт", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
  