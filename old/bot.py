import asyncio
import time
import types

from keyboard import *

# инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



class Text(StatesGroup):
    send_message = State()
    send_message_after = State()
    send_message_everyone = State()
    time_after = State()
    time_everyone = State()
    code_admin = State()
    send_code = State()
    rename_1 = State()
    rename_2 = State()
    rename_3 = State()
    rename_4 = State()
    rename_5 = State()
    rename_6 = State()
    rename_7 = State()
    rename_8 = State()
    rename_9 = State()
    rename_10 = State()
    rename_11 = State()
    rename_12 = State()
    rename_13 = State()
    rename_14 = State()
    rename_15 = State()
    rename_16 = State()
    rename_17 = State()
    rename_18 = State()
    rename_19 = State()
    rename_20 = State()
    rename_21 = State()
    rename_22 = State()



# обработка хэндлера /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    personal_link = f"http://t.me/top100_business_bot?start={message.from_user.id}"
    if not DataBase().userExist(message.from_user.id):
        try:
            inviter_id = int(message.text.split()[1])
            if DataBase().checkUser(inviter_id):
                user = DataBase().getUser(inviter_id)
                value = user[3] + 1
                DataBase().update("referals", value, inviter_id)
                inviter_link = f"http://t.me/top100_business_bot?start={inviter_id}"
                await counting_referals(inviter_id, inviter_link)
        except IndexError:
            pass
        user = [message.from_user.id, message.from_user.first_name, str(message.date).split()[0], 0,
                f"@{message.from_user.username}", 0, int(time.time()), 0, 1]
        add = DataBase().addUser(user)
        if not add:
            try:
                inviter_id = int(message.text.split()[1])
                user = DataBase().getUser(inviter_id)
                value = user[3] - 1
                DataBase().update("referals", value, inviter_id)
                await message.answer(text=f'{static_messages[4]}')
            except IndexError:
                pass
        else:
            await message.answer(
                text=f'{static_messages[0]} \n\n{personal_link} \n\n {static_messages[1]} \n\n{personal_link}',
                reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {personal_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={personal_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {personal_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))
            await asyncio.sleep(172800)
            await bot.send_message(chat_id=message.from_user.id, text=f'{static_messages[24]}')
    else:
        await message.answer(f"{static_messages[2]} Ваша ссылка: \n\n{personal_link}", reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {personal_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={personal_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {personal_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if DataBase().getUser(message.from_user.id)[5] == 0:
        await message.answer('У вас нет прав на использование данной команды')
    else:
        await message.answer('Панель администратора', reply_markup=keyboard_admin())


@dp.message_handler(commands=['new_admin'])
async def new_admin(message: types.Message):
    if DataBase().getUser(message.from_user.id)[5] == 0:
        await message.answer('Введите код администратора')
        await Text.send_code.set()
    else:
        await message.answer('Вы уже администратор\n\nВоспользуйтесь командой\n/admin')

@dp.message_handler(state=Text.send_code, content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(send_code=message.text)
    code = await state.get_data()
    await state.finish()
    try:
        if code['send_code'] == str(static_messages[23]):
            admins = DataBase().check_admin()
            DataBase().update("admin", 1, message.from_user.id)
            await message.answer(f'Поздравляем, {message.from_user.first_name}\nВы администратор',
                                 reply_markup=keyboard_admin())
            for i in range(len(admins)):
                if message.from_user.username is None:
                    await bot.send_message(chat_id=admins[i],
                                           text=f"Добавлен новый администратор\n@{message.from_user.first_name}")
                else:
                    await bot.send_message(chat_id=admins[i],
                                           text=f"Добавлен новый администратор\n@{message.from_user.username}")
        else:
            await message.answer('Неверный код')
    except:
        await message.answer('Неверный код')


# Сеня доработает, когда тема добавил таймер. Ради всего святого не лезь править ее сам
async def counting_referals(inviter_id, inviter_link):
    if DataBase().getUser(inviter_id)[3] == 1:
        await bot.send_message(chat_id=inviter_id,
                               text=f"{static_messages[3]}\n\n{inviter_link}\n\n{static_messages[4]}", reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {inviter_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={inviter_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {inviter_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))
    if DataBase().getUser(inviter_id)[3] == 2:
        await bot.send_message(chat_id=inviter_id,
                               text=f"{static_messages[8]}\n\n{inviter_link}\n\n{static_messages[9]}", reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {inviter_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={inviter_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {inviter_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))
    if DataBase().getUser(inviter_id)[3] == 3:
        await bot.send_message(chat_id=inviter_id,
                               text=f"{static_messages[10]}\n\n{inviter_link}\n\n{static_messages[11]}", reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {inviter_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={inviter_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {inviter_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))
    if DataBase().getUser(inviter_id)[3] == 4:
        await bot.send_message(chat_id=inviter_id,
                               text=f"{static_messages[12]}\n\n{inviter_link}\n\n{static_messages[13]}", reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {inviter_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={inviter_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {inviter_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))
    # успел за час
    if DataBase().getUser(inviter_id)[3] == 5:
        user = DataBase().getUser(inviter_id)
        if int(time.time()) - user[6] <= 3600:
            admins = DataBase().check_admin()
            await bot.send_message(chat_id=inviter_id,
                                   text=f"{static_messages[14]}")
            for i in range(len(admins)):
                if user[4] == "@None":
                    await bot.send_message(chat_id=admins[i],
                                           text=f"Успел уложится в один час:\n{user[1]}\nid{user[0]}")
                else:
                    await bot.send_message(chat_id=admins[i],
                                           text=f"Успел уложится в один час:\n{user[4]}")
        else:
            await bot.send_message(chat_id=inviter_id,
                                   text=f"{static_messages[15]}")
    if 5 < DataBase().getUser(inviter_id)[3] < 10:
        await bot.send_message(chat_id=inviter_id,
                               text=f"{static_messages[DataBase().getUser(inviter_id)[3] + 11]}\n\n{inviter_link}\n\n{static_messages[16]}", reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {inviter_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={inviter_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {inviter_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))
    if DataBase().getUser(inviter_id)[3] == 10:

        await bot.send_message(chat_id=inviter_id,
                               text=f"{static_messages[21]}")
        await bot.send_message(chat_id=inviter_id,
                               text=f"{static_messages[22]}\n\n{inviter_link}\n\n{static_messages[16]}", reply_markup=keyboard_link(f'\n🟢Появился новый телеграм канал «Народный бизнес»!\n\n💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!\n\n🎁Приведите друзей и получите денежный приз и подарки!\n\nСсылка на инструкцию: {inviter_link}\n\n🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!', f"""https://vk.com/share.php?url={inviter_link}&comment=🟢Появился новый телеграм канал Народный бизнес!💰Присоединяйтесь к нашему каналу и  сможете получить прибыль уже в первый день!🎁Приведите друзей и получите денежный приз и подарки!Ссылка на инструкцию: {inviter_link}🎈С нами уже зарабатывают тысячи людей без копейки вложений! Всем рекомендуем!"""))

@dp.callback_query_handler(
    lambda call: call.data == "params" or call.data == "texts" or call.data == "stat" or call.data == "sender" or call.data == "users" or call.data == "code_admin" or call.data == "back_admin" or call.data == "back_text" or call.data == "back_users" or call.data == "back_send")
async def admin_params(call: types.CallbackQuery):
    if call.data == 'back_admin':
        await call.message.edit_reply_markup(reply_markup=keyboard_admin())
    elif call.data == 'back_text':
        await call.message.edit_text('Панель администратора', reply_markup=keyboard_text())
    elif call.data == 'back_send':
        await call.message.edit_text('Панель администратора', reply_markup=keyboard_admin())
    elif call.data == 'back_users':
        await call.message.edit_text('Панель администратора', reply_markup=keyboard_admin())
    elif call.data == 'params':
        if call.from_user.id == 376729425:
            await message.answer('Сорян бро')
        else:
            await call.message.edit_reply_markup(reply_markup=keyboard_admin_params())
    elif call.data == 'texts':
        if call.from_user.id == 376729425:
            await message.answer('Сорян бро')
        else:
            await call.message.edit_reply_markup(reply_markup=keyboard_text())
    elif call.data == 'users':
        data = DataBase().check_ref()
        id_ = data["id"].split()
        username = data["username"].split()
        ref = data["ref"].split()
        active = data["active"].split()
        act = {'1': '🟢', '0': '🛑'}
        data_ = []
        for i in range(len(id_)):
            data_ += [id_[i] + " " + username[i] + " " + ref[i] + " " + active[i]]
        data_ = sorted(data_, key=lambda x: int(x.split()[2]), reverse=True)
        message_ = ''
        n = len(ref) // 50
        mess = ''
        for G in range(len(ref[n*50:])):
            c = n*50 + G
            mess += f'{c + 1}. {data_[c].split()[1]} ({data_[c].split()[0]}) - {data_[c].split()[2]} рефералов {act[data_[c].split()[3]]}\n'
        for j in range(n):
            for i in range(len(ref[j * 50:(j + 1) * 50])):
                g = j * 50 + i
                message_ += f'{g + 1}. {data_[g].split()[1]} ({data_[g].split()[0]}) - {data_[g].split()[2]} рефералов {act[data_[g].split()[3]]}\n'
            if j == n - 1:
                await call.message.answer(f'{message_}')
                message_ = ''
                await call.message.answer(f'{mess}', reply_markup=keyboard_back_users())
            else:
                await call.message.answer(f'{message_}')
                message_ = ''
    elif call.data == 'sender':
        if call.from_user.id == 376729425:
            await message.answer('Сорян бро')
        else:
            await call.message.edit_reply_markup(reply_markup=keyboard_admin_sender())
    elif call.data == 'stat':
        await call.message.edit_reply_markup(reply_markup=keyboard_admin_stat())
    elif call.data == 'code_admin':
        await bot.send_message(chat_id=call.from_user.id, text='Введите новый код администратора')
        await Text.code_admin.set()

@dp.message_handler(state=Text.code_admin, content_types=types.ContentTypes.TEXT)
async def send_message(message: types.Message, state: FSMContext):
    await state.update_data(code_admin=message.text)
    code = await state.get_data()
    await state.finish()
    static_messages[23] = code['code_admin']
    with open('messages.txt', 'w', encoding='utf-8') as file:
        for elem in static_messages:
            file.write("**" + elem + "***\n\n")
    await bot.send_message(chat_id=message.from_user.id, text=f'Новый код администратора: {static_messages[23]}')


@dp.callback_query_handler(lambda call: call.data == "stat_7" or call.data == "close" or call.data == "stat_30" or call.data == "stat_all" or call.data == "stat_back" or call.data == "back_stat_menu")
async def admin_params(call: types.CallbackQuery):
    if call.data == "stat_back":
        await call.message.edit_reply_markup(reply_markup=keyboard_admin())
    if call.data == "back_stat_menu":
        await call.message.edit_text(text='Панель администратора', reply_markup=keyboard_admin_stat())
    if call.data == "stat_all":
        count_ = 0
        data = DataBase().check_ref()
        active = (data['active'].split()).count('1')
        users = DataBase().get_users_start_data().split()
        for j in range(len(users)):
            count_ += 1
        d = DataBase().getUser_d()
        first_date = datetime.datetime(int(d[:4]), int(d[5:7]), int(d[8:]))
        now = datetime.datetime.now()
        n = int(str(now - first_date).split()[0])
        text = "Новые пользователи за всё время:\n"
        for i in range(n+1):
            date_ago = now - datetime.timedelta(days=i)
            date = str(date_ago)[:10]
            text += str(date_ago)[:10] + ":  +"
            users = DataBase().get_users_start_data().split()
            count = 0
            for j in range(len(users)):
                if users[j] == date:
                    count += 1
            text += str(count) + '\n'
        await call.message.edit_text(text=f'Общее количество пользователей: {count_}\nАктивных: {active}\n\n{text}',
                                     reply_markup=keyboard_back_stat_menu())
    if call.data == "stat_7":
        count_ = 0
        data = DataBase().check_ref()
        active = (data['active'].split()).count('1')
        users = DataBase().get_users_start_data().split()
        for j in range(len(users)):
            count_ += 1
        now = datetime.datetime.now()
        text = "Новые пользователи за последнюю неделю:\n"
        for i in range(7):
            date_ago = now - datetime.timedelta(days=i)
            date = str(date_ago)[:10]
            text += str(date_ago)[:10] + ":  +"
            users = DataBase().get_users_start_data().split()
            count = 0
            for j in range(len(users)):
                if users[j] == date:
                    count += 1
            text += str(count) + '\n'
        await call.message.edit_text(text=f'Общее количество пользователей: {count_}\nАктивных: {active}\n\n{text}', reply_markup=keyboard_back_stat_menu())
    if call.data == 'stat_30':
        count_ = 0
        data = DataBase().check_ref()
        active = (data['active'].split()).count('1')
        users = DataBase().get_users_start_data().split()
        for j in range(len(users)):
            count_ += 1
        now = datetime.datetime.now()
        text = "Новые пользователи за последние 30 дней:\n"
        for i in range(30):
            date_ago = now - datetime.timedelta(days=i)
            date = str(date_ago)[:10]
            text += str(date_ago)[:10] + ":  +"
            users = DataBase().get_users_start_data().split()
            count = 0
            for j in range(len(users)):
                if users[j] == date:
                    count += 1
            text += str(count) + '\n'
        await call.message.edit_text(text=f'Общее количество пользователей: {count_}\nАктивных: {active}\n\n{text}', reply_markup=keyboard_back_stat_menu())


'''Рассылка'''

#Обработчик кнопок
@dp.callback_query_handler(lambda call: call.data == "send" or call.data == "send_after" or call.data == "send_everyone", state='*')
async def admin_params(call: types.CallbackQuery):
    if call.data == "send":
        await bot.send_message(chat_id=call.from_user.id, text='Введите текст сообщения:')
        await Text.send_message.set()
    elif call.data == "send_after":
        await bot.send_message(chat_id=call.from_user.id, text='Укажите время:\n -Пример-\n\n 2022-11-14 10:25\n(14 ноября в 10:25)')
        await Text.time_after.set()
    elif call.data == "send_everyone":
        await call.answer('Укажите время:\n -Пример-\n\n 00:05:00\n(каждые 5 часов)')
        await Text.time_everyone.set()


# Функции с рассылкой
#Отправить сейчас
@dp.message_handler(state=Text.send_message, content_types=types.ContentTypes.TEXT)
async def send_message(message: types.Message, state: FSMContext):
    if message.text == "❌Отмена❌":
        await state.finish()
        await message.answer('Панель администратора', reply_markup=keyboard_admin_sender())
    else:
        await state.update_data(send_message=message.text)
        message_ = await state.get_data()
        await state.finish()
        users = DataBase().getUsersID().split()
        for i in range(len(users)):
            await bot.send_message(chat_id=users[i], text=f"{message_['send_message']}")


#Отправить через (Добавить обраточик времени. Напричер через time.time())
@dp.message_handler(state=Text.time_after, content_types=types.ContentTypes.TEXT)
async def send_message_after(message: types.Message, state: FSMContext):
    if message.text == "❌Отмена❌":
        await state.finish()
        await message.answer('Панель администратора', reply_markup=keyboard_admin_sender())
    else:
        await state.update_data(time_after=message.text)
        message_ = await state.get_data()
        time = str(message_['time_after']).split()
        time_date = list(map(int, time[0].split('-')))
        time_time = list(map(int, time[1].split(':')))
        date_time = datetime.datetime(year=time_date[0], month=time_date[1], day=time_date[2], hour=time_time[0],
                                      minute=time_time[1], second=0)
        try:
            if str(date_time - datetime.datetime.now()) >= '0':
                await bot.send_message(chat_id=message.from_user.id, text='Введите текст сообщения')
                await Text.send_message_after.set()
            else:
                await bot.send_message(chat_id=message.from_user.id, text='Введена неверная дата')
        except:
            await bot.send_message(chat_id=message.from_user.id, text='Введена неверная дата')


@dp.message_handler(state=Text.send_message_after, content_types=types.ContentTypes.TEXT)
async def send_message_after(message: types.Message, state: FSMContext):
    if message.text == "❌Отмена❌":
        await state.finish()
        await message.answer('Панель администратора', reply_markup=keyboard_admin_sender())
    else:
        await state.update_data(send_message_after=message.text)
        message_ = await state.get_data()
        await state.finish()
        users = DataBase().getUsersID().split()
        await bot.send_message(chat_id=message.from_user.id, text=f'Сообщения будут отправлены: {message_["time_after"]}')
        time = str(message_['time_after']).split()
        time_date = list(map(int, time[0].split('-')))
        time_time = list(map(int, time[1].split(':')))
        date_time = datetime.datetime(year=time_date[0], month=time_date[1], day=time_date[2], hour=time_time[0], minute=time_time[1], second=0)
        sleep = date_time - datetime.datetime.now()
        sec_sleep = sleep.seconds + sleep.days * 24 * 3600
        await asyncio.sleep(sec_sleep)
        for i in range(len(users)):
            await bot.send_message(chat_id=users[i], text=f"{message_['send_message_after']}")

#Отправить каждые (Добавить обраточик времени. Напричер через time.time())
@dp.message_handler(state=Text.send_message_everyone, content_types=types.ContentTypes.TEXT)
async def send_message_after(message: types.Message, state: FSMContext):
    await state.update_data(send_message_everyone=message.text)
    message_ = await state.get_data()
    await state.finish()
    users = DataBase().getUsersID().split()
    for i in range(len(users)):
        await bot.send_message(chat_id=users[i], text=f"{message_['send_message_everyone']}")



@dp.message_handler(commands=['send_id_message'])
async def send_answer(message: types.Message):
    print(message.text)
    index_1 = message.text.find('[')+1
    index_2 = message.text.find(']')
    telegram_id = message.text[index_1:index_2]
    print(telegram_id)
    user = DataBase().getUser(int(telegram_id))
    text_ = auto_messages(user[7] - 51)
    await bot.send_message(chat_id=user[0],
                           text=f'{text_.replace("[username]", f"{user[1]}") if "[username]" in text_ else ""}', disable_web_page_preview=True)
    DataBase().update('count_message', user[7] + 1, user[0])



@dp.message_handler(commands=['send_id'])
async def send_answer(message: types.Message):
    print(message.text)
    index_1 = message.text.find('[')+1
    index_2 = message.text.find(']')
    telegram_id = message.text[index_1:index_2]
    print(telegram_id)
    index_1_text = message.text.find('*')+1
    message_text = message.text[index_1_text:]
    print(message_text)
    await bot.send_message(chat_id=telegram_id, text=f'<b>Сообщение от <a href="https://t.me/mihail_yakovlev">Михаила Яковлева</a>:</b>\n{message_text}', parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)


@dp.message_handler(content_types=['any'])
async def reg_any_message(message: types.Message):
    await message.answer(text='Здравствуйте, я получил ваше сообщение\nПродублируйте его мне по этим контактам\n\nТелеграм: @mihail_yakovlev\nВКонтакте: https://vk.com/yakovlev_mihail\nE-mail: mihailjakovlew@yandex.ru')
    users = DataBase().up_sub()
    for user in users:
        if user[5] == 1:
            if message.text is not None:
                await bot.send_message(chat_id=user[0],
                                       text=f"<b>Новое сообщение от (@{message.from_user.username}):</b>\n<b>ID:</b> <code>{message.from_user.id}</code>\n\n{message.text}",
                                       parse_mode=types.ParseMode.HTML)
            elif message.photo is not None:
                if message.caption is not None:
                    await bot.send_photo(chat_id=user[0], photo=message.photo[-1].file_id,
                                         caption=f"<b>Новое сообщение от (@{message.from_user.username}):@{message.from_user.username}</b>\n<b>ID:</b> <code>{message.from_user.id}</code>\n\n{message.caption}",
                                         parse_mode=types.ParseMode.HTML)
                else:
                    await bot.send_photo(chat_id=user[0], photo=message.photo[-1].file_id,
                                         caption=f"<b>Новое сообщение от (@{message.from_user.username}):</b>\n<b>ID:</b> <code>{message.from_user.id}</code>",
                                         parse_mode=types.ParseMode.HTML)
            elif message.document is not None:
                await bot.send_document(chat_id=user[0], document=message.document.file_id,
                                        caption=f"<b>Новое сообщение от (@{message.from_user.username}):</b>\n<b>ID:</b> <code>{message.from_user.id}</code>",
                                        parse_mode=types.ParseMode.HTML)

'''Конец рассылки'''

@dp.callback_query_handler(lambda call: call.data[:6] == "rename")
async def admin_params(call: types.CallbackQuery):
    for i in range(len(rename)):
        if rename[i] == call.data:
            await call.message.answer(f'- Действующий текст -\n\n{static_messages[i]}\n\nВведите новый текст', reply_markup=keyboard_close())
            await eval(f'Text.{call.data}.set()')


@dp.message_handler(state="*", content_types=types.ContentTypes.TEXT)
async def name(message: types.Message, state: FSMContext):
    if message.text == "❌Отмена❌":
        await state.finish()
        await message.answer('Панель администратора', reply_markup=keyboard_text())
    else:
        current_state = await state.get_state()
        for i in range(len(rename)):
            if rename[i] == current_state[5:]:
                static_messages[i] = f'{message.text}'
                static_messages[i] = message.text
                text = ""
                for j in range(len(static_messages)):
                    text += f"**{static_messages[j]}***\n\n"
                with open('messages.txt', 'w', encoding='utf-8') as file:
                    file.write(text)
                await message.answer(f'- Действующий текст -\n\n{static_messages[i]}', reply_markup=keyboard_back_text())
                await state.finish()



async def send_auto_message():
    print('Start Sender')
    users = DataBase().getUsersID().split()
    for i_ in range(len(users)):
        user = DataBase().getUser(int(users[i_]))
        if user[7] <= 100 and int(time.gmtime(user[6]).tm_mday) != int(time.gmtime(int(time.time())).tm_mday):
            print(f'Send > {user[0]}')
            #time_send = int(time.gmtime(user[6]).tm_hour) * 3600
            #await asyncio.sleep(time_send)
            try:
                if 50 < user[7] <= 100:
                    text_ = auto_messages(user[7] - 51)
                    await bot.send_message(chat_id=user[0],
                                           text=f'{text_.replace("[username]", f"{user[1]}") if "[username]" in text_ else ""}')
                    DataBase().update('count_message', user[7] + 1, user[0])
                    DataBase().update('active', 1, user[0])
                else:
                    text_ = auto_messages(user[7])
                    await bot.send_message(chat_id=user[0],
                                           text=f'{text_.replace("[username]", f"{user[1]}") if "[username]" in text_ else ""}')
                    DataBase().update('count_message', user[7] + 1, user[0])
                    DataBase().update('active', 1, user[0])
            except:
                DataBase().update('active', 0, user[0])

async def scheduler():
    aioschedule.every().day.at("17:03").do(send_auto_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    print('RUNNING')
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())