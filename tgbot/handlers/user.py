from aiogram import Dispatcher
from tgbot.functions.start import *


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*", content_types=types.ContentType.ANY)
    dp.register_message_handler(listen_text, state="*", content_types=types.ContentType.ANY, is_admin=False, is_blocked=False)
