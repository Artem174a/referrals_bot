from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.bot import Bot
from aiogram.dispatcher import FSMContext
from tgbot.database.DB import *
from tgbot.keyboards.inline import *


def register_admin_mess(dp: Dispatcher):
    dp.register_message_handler(menu, commands=["admin"], state="*", is_admin=True)
    dp.register_callback_query_handler(admin_callback, lambda call: call.data[:3] == "ad_", is_admin=True, state="*")
    dp.register_message_handler(admin_message, state='*', is_admin=True, content_types=types.ContentType.ANY)
    dp.register_message_handler(blocked_message, state='*', is_blocked=True, content_types=types.ContentType.ANY)


async def blocked_message(message: Message, state: FSMContext):
    await message.answer("Заблокированно")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)


async def admin_callback(call: CallbackQuery, state: FSMContext):
    name_functions = call.data[3:]
    if 'delete_admin' in name_functions:
        await eval(f'delete_admin(call=call, state=state)')
    if 'delete_blocked' in name_functions:
        await eval(f'delete_blocked(call=call, state=state)')
    if 'text' in name_functions:
        await eval(f'text(call=call, state=state)')
    if 'stat' in name_functions:
        await eval(f'stat(call=call, state=state)')
    else:
        await eval(name_functions + f'(call=call, state=state)')


async def admin_message(message: Message, state: FSMContext):
    data = await state.get_state()
    if data == 'add_blocked':
        await add_blocked(message=message, state=state)
    if 'edit_text' in data:
        await edit_text(message=message, state=state)


def declension_of_referral(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return 'реферал'
    elif n % 10 in [2, 3, 4] and n % 100 not in [12, 13, 14]:
        return 'реферала'
    else:
        return 'рефералов'


def top_10():
    top_users = sorted(Db().up_sub(), key=lambda x: x[4], reverse=True)[:10]
    return '<b>ТОП 10</b>\n' + '\n'.join(
        f'╠ @{i[1]}: <code>{i[4]}</code> {declension_of_referral(int(i[4]))}\n╠ <b>ID:</b> <code>{i[0]}</code>\n╚<b>Дата регистрации:</b><code> {time.strftime("%d.%m.%y", time.localtime(int(i[3])))}</code>\n'
        for i in top_users)


async def admin_start(message: types.Message):
    bot_name = await message.bot.get_me()
    link = f"https://t.me/{bot_name.username}?start={message.from_user.id}"
    await message.answer(f'''
<b>Добро пожаловать, администратор!</b>
<b>Ваша реферальная ссылка: </b>

<code>{link}</code>
''', reply_markup=InlineKeyboardAdmin().reposts(link))


"""Генерация меню"""


async def menu(message: types.Message = None, call: types.CallbackQuery = None, state: FSMContext = None):
    reply_markup = InlineKeyboardAdmin().admin_menu()
    data = Database().up_sub()
    all_users = len(data)
    active_users = 0
    for i in range(len(data)):
        if data[i][5] == 1:
            active_users += 1
    text = f'''
<b>Панель администратора</b>
<em>Нажмите на кнопку, чтобы выбрать</em>

<b>Пользовтели<em>
╠ Всего: <code>{all_users}</code>
╚ Активных: <code>{active_users}</code>
</em></b>

'''
    text += top_10()
    if message:
        await message.answer(text=text, reply_markup=reply_markup)
    if call:
        await call.message.answer(text=text, reply_markup=reply_markup)


async def edit_menu(message: types.Message = None, call: types.CallbackQuery = None, state: FSMContext = None):
    reply_markup = InlineKeyboardAdmin().admin_menu()
    data = Database().up_sub()
    all_users = len(data)
    active_users = 0
    for i in range(len(data)):
        if data[i][5] == 1:
            active_users += 1
    text = f'''
<b>Панель администратора</b>
<em>Нажмите на кнопку, чтобы выбрать</em>

<b>Пользовтели<em>
╠ Всего: <code>{all_users}</code>
╚ Активных: <code>{active_users}</code>
</em></b>
'''
    if message:
        await message.edit_text(text=text, reply_markup=reply_markup)
    if call:
        await call.message.edit_text(text=text, reply_markup=reply_markup)


"""Обработчики разделов"""


async def settings(call: CallbackQuery, state: FSMContext):
    reply_markup = InlineKeyboardAdmin().settings()
    admins = len(Database().get_admins())
    blocked = len(Database().up_blocked())
    text = f'''
<b>Параметры</b>
<em>Нажмите на кнопку, чтобы выбрать</em>

<b>Полезное<em>
╠ Администраторы: <code>{admins}</code>
╚ Заблокированные: <code>{blocked}</code>
</em></b>
'''
    await call.message.edit_text(text=text, reply_markup=reply_markup)


async def sttistics(call: CallbackQuery, state: FSMContext):
    reply_markup = InlineKeyboardAdmin().statistics()
    data = Database().up_sub()
    today_users = sum(1 for i in data if int(time.time()) - int(i[3]) <= 86400)
    week_users = sum(1 for i in data if (int(time.time()) - int(i[3])) <= 86400 * 7)
    month_users = sum(1 for i in data if (int(time.time()) - int(i[3])) <= 86400 * 30)
    text = f'''
<b>Статистика</b>
<em>Нажмите на кнопку, чтобы выбрать</em>

<b>Новые пользователи<em>
╠ Сегодня: <code>{today_users}</code>
╠ Неделя: <code>{week_users}</code>
╚ Месяц: <code>{month_users}</code></em></b>
'''
    await call.message.edit_text(text=text, reply_markup=reply_markup)


async def txt(call: CallbackQuery, state: FSMContext):
    try:
        if await state.get_state() != {}:
            await state.finish()
    except:
        pass
    reply_markup = InlineKeyboardAdmin().texts()
    data = Database().up_message()
    start_message = 0
    referral_message = 0
    rest_message = 0
    for i in range(len(data)):
        if 'start' in data[i][0]:
            start_message += 1
        if 'referral' in data[i][0]:
            referral_message += 1
        if 'start' not in data[i][0] and 'referral' not in data[i][0]:
            rest_message += 1
    text = f'''
<b>Текста</b>
<em>Нажмите на кнопку, чтобы выбрать</em>

<b>Сообщения<em>
╠ Приветствие: <code>{start_message}</code>
╠ Остальное: <code>{rest_message}</code>
╚ Рефералы: <code>{referral_message}</code>
</em></b>
'''
    await call.message.edit_text(text=text, reply_markup=reply_markup)


async def senders(call: CallbackQuery, state: FSMContext):
    reply_markup = InlineKeyboardAdmin().senders()
    admins = Database().get_admins()
    text = f'''
<b>Рассылка</b>
<em>Нажмите на кнопку, чтобы выбрать</em>

<b>Сообщения<em>
╠ Запланированные: <code></code>
╚ Автоматичексие: <code>{admins}</code>
</em></b>
'''
    await call.message.edit_text(text=text, reply_markup=reply_markup)


"""Функции разделов"""

"""Параметры"""


async def admins(call: types.CallbackQuery = None, state: FSMContext = None):
    buttons = [
        types.InlineKeyboardButton(text="Назад", callback_data="ad_edit_menu"),
        types.InlineKeyboardButton(text="Удалить", callback_data="ad_delete_admin")
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(buttons[1])
    keyboard.add(buttons[0])
    text = f'''
<b>Администраторы</b>
<em>Все администраторы:</em>

<b>Контакты</b>
'''
    admins = Database().get_admins()
    for i in range(len(admins)):
        text += f'<b><em>╠ ID: <code>{admins[i][0]}</code></em></b>\n' \
                f'<b><em>╚ Username: @{admins[i][1]}</em></b>\n'
    await call.message.edit_text(text=text, reply_markup=keyboard)


async def delete_admin(call: types.CallbackQuery = None, state: FSMContext = None):
    if call.data[3:] != "delete_admin":
        print(int(call.data[16:]))
        Database().delete_admin(int(call.data[16:]))
    buttons = []
    text = f'''
<b>Администраторы</b>
<em>Все администраторы:</em>

<b>Контакты</b>
'''
    admins = Database().get_admins()
    for i in range(len(admins)):
        text += f'<b><em>╠ ID: <code>{admins[i][0]}</code></em></b>\n' \
                f'<b><em>╚ Username: @{admins[i][1]}</em></b>\n'
        buttons.append(types.InlineKeyboardButton(text=f"Удалить ({admins[i][0]})",
                                                  callback_data=f"ad_delete_admin_{admins[i][0]}"))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_admins"))
    await call.message.edit_text(text=text, reply_markup=keyboard)


async def blocked(call: types.CallbackQuery = None, state: FSMContext = None):
    if await state.get_state() == 'add_blocked':
        await state.finish()
    buttons = [
        types.InlineKeyboardButton(text="Назад", callback_data="ad_settings"),
        types.InlineKeyboardButton(text="Удалить", callback_data="ad_delete_blocked"),
        types.InlineKeyboardButton(text="Добавить", callback_data="ad_add_blocked")
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(buttons[1], buttons[2])
    keyboard.add(buttons[0])
    text = f'''
<b>Заблокированные</b>
<em>Все заблокированные:</em>

<b>Контакты</b>
'''
    admins = Database().up_blocked()
    for i in range(len(admins)):
        text += f'<b><em>╠ ID: <code>{admins[i][0]}</code></em></b>\n' \
                f'<b><em>╚ Username: @{admins[i][1]}</em></b>\n'
    await call.message.edit_text(text=text, reply_markup=keyboard)


async def delete_blocked(call: types.CallbackQuery = None, state: FSMContext = None):
    if state.get_state() == "ad_blocked":
        await state.finish()
    if call.data[3:] != "delete_blocked":
        print(int(call.data[18:]))
        Database().del_block_user(int(call.data[18:]))
    buttons = []
    text = f'''
<b>Заблокированные</b>
<em>Все заблокированные:</em>

<b>Контакты</b>
'''
    admins = Database().up_blocked()
    for i in range(len(admins)):
        text += f'<b><em>╠ ID: <code>{admins[i][0]}</code></em></b>\n' \
                f'<b><em>╚ Username: @{admins[i][1]}</em></b>\n'
        buttons.append(types.InlineKeyboardButton(text=f"Удалить ({admins[i][0]})",
                                                  callback_data=f"ad_delete_blocked_{admins[i][0]}"))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_blocked"))
    await call.message.edit_text(text=text, reply_markup=keyboard)


async def add_blocked(call: types.CallbackQuery = None, state: FSMContext = None, message: types.Message = None):
    if call:
        text = f'''
<b>Заблокированные</b>
<em>Все заблокированные:</em>

<b>Контакты</b>
'''
        admins = Database().up_blocked()
        for i in range(len(admins)):
            text += f'<b><em>╠ ID: <code>{admins[i][0]}</code></em></b>\n' \
                    f'<b><em>╚ Username: @{admins[i][1]}</em></b>\n'
        text += f'\n<b>Напишите ID пользователя чтобы заблокировать его</b>'
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_blocked"))
        await call.message.edit_text(text=text, reply_markup=keyboard)
        await state.set_state('add_blocked')
    if message:
        print("Message")
        us_id = message.text
        try:
            Database().add_block_user(int(us_id))
        except:
            await message.reply(
                f'Не удалось заблокировать пользователя <code>{us_id}</code>\n\nОтсутствует в базе данных')
        await state.finish()
        text = f'''
<b>Заблокированные</b>
<em>Все заблокированные:</em>

<b>Контакты</b>
'''
        admins = Database().up_blocked()
        for i in range(len(admins)):
            text += f'<b><em>╠ ID: <code>{admins[i][0]}</code></em></b>\n' \
                    f'<b><em>╚ Username: @{admins[i][1]}</em></b>\n'
        text += f'\n<b>Напищите ID пользователя чтобы заблокировать его</b>'
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_blocked"))
        await message.answer(text=text, reply_markup=keyboard)
        await state.set_state(state='add_blocked')


"""Текста"""


async def text(call: types.CallbackQuery = None, state: FSMContext = None):
    text_start = f'''
<b>Сообщения</b>
<em>Все приветственные:</em>

<b>Сообщения</b>
'''
    text_referrals = f'''
<b>Сообщения</b>
<em>Все реферальные:</em>

<b>Сообщения</b>
'''
    text_rest = f'''
<b>Сообщения</b>
<em>Все прочие:</em>

<b>Сообщения</b>
'''
    data_msg = Database().up_message()
    callback = call.data[8:]

    if callback == "start":
        if await state.get_state() == 'edit_text':
            data = await state.get_data()
            print(data['msg_id'])
            Database().update_message(role=data['msg_id'], message=data['msg'])
            await call.answer(text='Сообщение изменено')
        buttons = []
        for i in range(len(data_msg)):
            if callback in data_msg[i][0]:
                text_start += f'<b><em>╠ ID: <code>{data_msg[i][0]}</code></em></b>\n'
                buttons.append(types.InlineKeyboardButton(text=f"ред({data_msg[i][0]})",
                                                          callback_data=f"ad_edit_text_{data_msg[i][0]}"))
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_txt"))
        await call.message.edit_text(text=text_start, reply_markup=keyboard)
    if callback == 'referral':
        if await state.get_state() == 'edit_text':
            data = await state.get_data()
            Database().update_message(role=data['msg_id'], message=data['msg'])
            await call.message.answer(text='<b>Сообщение изменено</b>')
        buttons = []
        for i in range(len(data_msg)):
            if callback in data_msg[i][0]:
                text_referrals += f'<b><em>╠ ID: <code>{data_msg[i][0]}</code></em></b>\n'
                buttons.append(types.InlineKeyboardButton(text=f"ред({data_msg[i][0]})",
                                                          callback_data=f"ad_edit_text_{data_msg[i][0]}"))
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_txt"))
        await call.message.edit_text(text=text_referrals, reply_markup=keyboard)
    if callback == 'rest':
        if await state.get_state() == 'edit_text':
            data = await state.get_data()
            Database().update_message(role=data['msg_id'], message=data['msg'])
            await call.message.answer(text='<b>Сообщение изменено</b>')
        buttons = []
        for i in range(len(data_msg)):
            if 'start' not in data_msg[i][0] and 'referral' not in data_msg[i][0]:
                text_rest += f'<b><em>╠ ID: <code>{data_msg[i][0]}</code></em></b>\n'
                buttons.append(types.InlineKeyboardButton(text=f"ред({data_msg[i][0]})",
                                                          callback_data=f"ad_edit_text_{data_msg[i][0]}"))
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_txt"))
        await call.message.edit_text(text=text_rest, reply_markup=keyboard)
    if 'ad_edit_text_' in call.data:
        msg_id = call.data[13:]
        text_msg = f'''
<b>Рабочий текст</b>
<em>ID: {msg_id}</em>

'''
        text_msg += f"{Database().get_message(msg_id).Message}\n\n<b>Введите новый текст:</b>"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Отмена", callback_data="ad_txt"))
        await call.message.edit_text(text=text_msg, reply_markup=keyboard)
        await state.set_state('edit_text')
        await state.update_data(msg_id=msg_id)


async def edit_text(message: Message, state: FSMContext):
    msg_id = await state.get_data()
    msg_id = msg_id['msg_id']
    text_msg = f'''
<b>Новый текст</b>
<em>ID: {msg_id}</em>

'''
    text_msg += f"{message.text}"
    h = msg_id.split('_')
    for i in range(len(h)):
        if h[i] in ['referral', 'rest', 'start']:
            h = h[i]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Готово", callback_data=f"ad_text_{h}"))
    keyboard.add(types.InlineKeyboardButton(text="Отмена", callback_data="ad_txt"))
    await state.update_data(msg_id=msg_id, msg=message.text)
    await message.answer(text=text_msg, reply_markup=keyboard)


async def stat(call: types.CallbackQuery = None, state: FSMContext = None):
    text_week = f'''
<b>Статистика</b>
<em>Все за последние 7 дней:</em>

<b>Для выхода в меню используйте:</b>
/admin
'''
    text_month = f'''
<b>Статистика</b>
<em>Все за последние 30 дней:</em>

<b>Для выхода в меню используйте:</b>
/admin
'''
    text_all_time = f'''
<b>Статистика</b>
<em>Все за всё время:</em>

<b>Для выхода в меню используйте:</b>
/admin
'''
    callback = call.data[8:]
    users = Database().up_sub()
    if callback == "week":
        buttons = []
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_txt"))
        msg = ''
        for i in range(len(users)):
            if int(time.time()) - int(users[i][3]) < 604800:
                msg += f'╠ ID: {users[i][3]}\n' \
                       f'╠ Username: @{users[i][1]}\n' \
                       f'╠ Fullname: @{users[i][2]}\n' \
                       f'╠ Registration: {time.strftime("%d.%m.%y", time.localtime(int(users[i][3])))}\n' \
                       f'╚ Referrals: {users[i][4]}\n'
        with open(f'week.txt', 'w+') as f:
            f.write(msg)
        file = open(f'week.txt', 'rb')
        await call.message.answer_document(file, caption=text_week)
    if callback == "month":
        buttons = []
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_txt"))
        msg = ''
        for i in range(len(users)):
            if int(time.time()) - int(users[i][3]) < 2592000:
                msg += f'╠ ID: {users[i][3]}\n' \
                       f'╠ Username: @{users[i][1]}\n' \
                       f'╠ Fullname: @{users[i][2]}\n' \
                       f'╠ Registration: {time.strftime("%d.%m.%y", time.localtime(int(users[i][3])))}\n' \
                       f'╚ Referrals: {users[i][4]}\n'
        with open(f'month.txt', 'w+') as f:
            f.write(msg)
        file = open(f'month.txt', 'rb')
        await call.message.answer_document(file, caption=text_month)
    if callback == "all_time":
        buttons = []
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="ad_txt"))
        msg = ''
        for i in range(len(users)):
            msg += f'╠ ID: {users[i][3]}\n' \
                   f'╠ Username: @{users[i][1]}\n' \
                   f'╠ Fullname: @{users[i][2]}\n' \
                   f'╠ Registration: {time.strftime("%d.%m.%y", time.localtime(int(users[i][3])))}\n' \
                   f'╚ Referrals: {users[i][4]}\n'
        with open(f'all_time.txt', 'w+') as f:
            f.write(msg)
        file = open(f'all_time.txt', 'rb')
        await call.message.answer_document(file, caption=text_all_time)