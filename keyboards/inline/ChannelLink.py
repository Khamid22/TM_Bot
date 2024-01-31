from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

links = InlineKeyboardMarkup(row_width=1)
buttons_data = [
    {"text": "teacher_Muzaffar", "url": "https://t.me/+jBiGiD_oNl44MjAy"},
    {"text": "Verify✅", "callback_data": "verify"}
]

# Add buttons to the InlineKeyboardMarkup
for button_data in buttons_data:
    button = InlineKeyboardButton(**button_data)
    links.add(button)