from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from utils import db_commands as db
from keyboards.inline.ChannelLink import links
from keyboards.inline import InviteButton
from data.config import ADMINS

CHANNEL_CHAT_ID = "@multileveltest"
photo_path = "D:\PythonProjects\med-telegram-bot\photo_2023-09-27_21-58-22.jpg"


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.get_user_by_id(message.from_user.id)
    if user is None:
        await db.add_user(message.from_user.username, message.from_user.first_name, message.from_user.id)
    await message.answer_photo(
        photo=open(photo_path, "rb"),
        caption="Announcing free Multilevel courses for "
                "those in need. Learn without financial "
                "barriers. Join us for a brighter future! "
                "📚💫 #EducationForAll"
    )

    await check_authenticity(message)


async def check_authenticity(message: types.Message):
    user_id = message.from_user.id
    member = await bot.get_chat_member(CHANNEL_CHAT_ID, user_id=user_id)

    if member.status in ["member", "administrator", "creator"]:
        await message.answer("Invite at least 5 friends to receive the link to the closed channel", reply_markup=InviteButton.inviteKey)
    else:
        await message.answer("To use this bot, please join the channels", reply_markup=links)


@dp.callback_query_handler(text=['verify'])
async def verify_authentication(call: types.CallbackQuery):
    member = await bot.get_chat_member(CHANNEL_CHAT_ID, user_id=call.from_user.id)
    if not member.status in ["member", "administrator", "creator"]:
        await call.answer("You have not joined the channel❌", show_alert=True)
    else:
        await call.answer("Done", cache_time=60)
        await call.message.answer("Invite at least 5 friends to receive the link to the closed channel", reply_markup=InviteButton.inviteKey)
        await call.message.delete()


@dp.message_handler(commands=['users'], chat_id=ADMINS[0])
async def show_users(message: types.Message):
    await message.answer(f"The number of users: {await db.count_users()}")


@dp.message_handler(commands=['dropDB'], chat_id=ADMINS[0])
async def drop_users(message: types.Message):
    await db.delete_all_users()
    await message.answer(f"The users dropped")
