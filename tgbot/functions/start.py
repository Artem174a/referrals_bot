import time
from aiogram.types import Message
from tgbot.keyboards.inline import *
from tgbot.database.DB import Database as Db


def declension_of_referral(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return 'реферал'
    elif n % 10 in [2, 3, 4] and n % 100 not in [12, 13, 14]:
        return 'реферала'
    else:
        return 'рефералов'


def top_10(telegram_id: int):
    gv = {"3": 1, "2": 2, "1": 3}
    replace_key = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'}
    data = Db().up_sub()
    sorted_data = sorted(data, key=lambda x: x[4], reverse=True)
    # Получение первых 10 элементов
    top_10 = sorted_data[:10]
    # Формирование строки из первых 10 элементов
    output_str = '<b>🔥ТОП 10🔥</b>\n\n'
    output_str += '\n'.join(
        f'<b>{replace_key[number+1]}</b> @{i[1]}: <code>{i[4]}</code> {declension_of_referral(int(i[4]))}\n╚<b>Дата регистрации:</b><code> {time.strftime("%d.%m.%y", time.localtime(int(i[3])))}</code>\n'
        for number, i in enumerate(top_10))
    index = next((i for i, item in enumerate(sorted_data) if str(item[0]) == str(telegram_id)), None)
    output_str += f'\n\n<b>Вы на <code>{index+1}</code> месте из <code>{len(sorted_data)}</code></b>'
    return output_str


async def user_start(message: Message):
    print(message.from_user.id)
    print(message.from_user.username)
    bot_name = await message.bot.get_me()
    link = f"https://t.me/{bot_name.username}?start={message.from_user.id}"
    if Db().user_exist(message.from_user.id) is False:
        try:
            inviter_id = int(message.text.split()[1])
            Db().update("referrals", Db().get_user(inviter_id).referrals + 1, inviter_id)
            inviter_id = int(message.text.split()[1])
            referrals = int(Db().get_user(inviter_id).referrals)
            bot_name = await message.bot.get_me()
            link = f"https://t.me/{bot_name.username}?start={inviter_id}"
            await message.answer(text="Ты перешёл по ссылке")
            await message.bot.send_message(chat_id=843774957,
                            text=Db().get_message("new_referral").Message.replace('[referrals]', f"{referrals} {declension_of_referral(referrals)}").replace(
                                '[link]', link),
                            reply_markup=InlineKeyboard().reposts(link))
        except:
            pass

        Db().add_user(message)
        text = str(Db().get_message(role="start_msg").Message)
        if "[link]" in text:
            text = text.replace('[link]', link)
        if "[bot-name]" in text:
            text = text.replace('[bot_name]', bot_name.first_name)
        if "[top-10]" in text:
            text = text.replace('[top-10]', top_10(message.from_user.id))
        await message.answer(text=text, reply_markup=InlineKeyboard().reposts(link))
    else:
        text = str(Db().get_message(role="start_old_msg").Message)
        if "[link]" in text:
            text = text.replace('[link]', link)
        if "[bot_name]" in text:
            text = text.replace('[bot_name]', bot_name.first_name)
        if "[top-10]" in text:
            text = text.replace('[top-10]', top_10(message.from_user.id))
        await message.answer(text=text, reply_markup=InlineKeyboard().reposts(link))


async def listen_text(message: Message):
    admins = Db().get_admins()
    for admin in admins:
        print(admin[0])
        await message.forward(disable_notification=True, protect_content=True, chat_id=int(admin[0]))