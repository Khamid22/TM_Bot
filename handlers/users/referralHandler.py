from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.deep_linking import get_start_link, decode_payload
from loader import dp, bot
from utils import db_commands as db


@dp.callback_query_handler(text=['invite'])
async def get_link(call: types.CallbackQuery):
    link = await get_start_link(str(call.message.from_user.id), encode=True)
    await call.message.answer(f"Your referral link: {link}")
    await handle_referral(call)
    await call.answer(60)


async def handle_referral(call: types.CallbackQuery):
    referral_id = call.message.get_args()
    if referral_id:
        referrer = await db.get_user_by_id(referral_id)
        if referrer:
            referrer.invited_friends += 1
            await db.update_user(referrer)
            remaining_invites = 5 - referrer.invited_friends
            if remaining_invites > 0:
                await bot.send_message(referral_id, f"You have invited {referrer.invited_friends} user(s). {remaining_invites} to go!")
            else:
                await bot.send_message(referral_id, "You have invited 5 friends!")
                await call.message.answer("Here is your link to the channel: https://t.me/+BgGE9XmDvBNkZjcy")
