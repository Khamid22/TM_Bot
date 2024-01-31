from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inviteKey = InlineKeyboardMarkup()
inviteKey.add(InlineKeyboardButton(text="invite", callback_data='invite'))
