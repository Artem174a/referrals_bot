from conf import *


def keyboard_admin():
    buttons = [
        types.InlineKeyboardButton(text="Параметры", callback_data="params"),
        types.InlineKeyboardButton(text="Текста", callback_data="texts"),
        types.InlineKeyboardButton(text="Статистика", callback_data="stat"),
        types.InlineKeyboardButton(text="Рассылка", callback_data="sender"),
        types.InlineKeyboardButton(text="Пользователи", callback_data="users")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def keyboard_admin_params():
    buttons = [
        types.InlineKeyboardButton(text="Сменить: код администратора", callback_data="code_admin"),
        types.InlineKeyboardButton(text="Назад ⏪", callback_data="back_admin")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def keyboard_text():
    buttons = [
        types.InlineKeyboardButton(text="Приветствие ч1", callback_data="rename_1"),
        types.InlineKeyboardButton(text="Приветствие ч2", callback_data="rename_2"),
        types.InlineKeyboardButton(text="С возвращением", callback_data="rename_3"),
        types.InlineKeyboardButton(text="Друг в течении часа ч1", callback_data="rename_4"),
        types.InlineKeyboardButton(text="Друг в течении часа ч2", callback_data="rename_5"),
        types.InlineKeyboardButton(text="Вы уже восп. реф. Ссылкой", callback_data="rename_6"),
        types.InlineKeyboardButton(text="бонус 1", callback_data="rename_7"),
        types.InlineKeyboardButton(text="бонус 2", callback_data="rename_8"),
        types.InlineKeyboardButton(text="привел 2 друзей в течение часа ч1", callback_data="rename_9"),
        types.InlineKeyboardButton(text="привел 2 друзей в течение часа ч2", callback_data="rename_10"),
        types.InlineKeyboardButton(text="привел 3 друзей в течение часа ч1", callback_data="rename_11"),
        types.InlineKeyboardButton(text="привел 3 друзей в течение часа ч2", callback_data="rename_12"),
        types.InlineKeyboardButton(text="привел 4 друзей в течение часа ч1", callback_data="rename_13"),
        types.InlineKeyboardButton(text="привел 4 друзей в течение часа ч2", callback_data="rename_14"),
        types.InlineKeyboardButton(text="привел 5 друзей в срок", callback_data="rename_15"),
        types.InlineKeyboardButton(text="привел 5 друзей не в срок", callback_data="rename_16"),
        types.InlineKeyboardButton(text="кстати - нажмите на кнопку 'универсальная'", callback_data="rename_17"),
        types.InlineKeyboardButton(text="привел 6 друзей", callback_data="rename_18"),
        types.InlineKeyboardButton(text="привел 7 друзей", callback_data="rename_19"),
        types.InlineKeyboardButton(text="привел 8 друзей", callback_data="rename_20"),
        types.InlineKeyboardButton(text="привел 9 друзей", callback_data="rename_21"),
        types.InlineKeyboardButton(text="привел 10 друзей", callback_data="rename_22"),
        types.InlineKeyboardButton(text="Назад ⏪", callback_data="back_admin")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def keyboard_admin_sender():
    buttons = [
        types.InlineKeyboardButton(text="Отправить сейчас", callback_data="send"),
        types.InlineKeyboardButton(text="Отправить в заданное время", callback_data="send_after"),
        types.InlineKeyboardButton(text="Назад ⏪", callback_data="back_send")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def keyboard_back_text():
    buttons = [
        types.InlineKeyboardButton(text="Назад ⏪", callback_data="back_text")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def keyboard_close():
    button1 = KeyboardButton('❌Отмена❌')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(button1)
    return keyboard

def keyboard_back_stat_menu():
    buttons = [
        types.InlineKeyboardButton(text="Назад ⏪", callback_data="back_stat_menu")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def keyboard_back_users():
    buttons = [
        types.InlineKeyboardButton(text="Назад ⏪", callback_data="back_users")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def keyboard_admin_stat():
    buttons = [
        types.InlineKeyboardButton(text="Последние 7 дней", callback_data="stat_7"),
        types.InlineKeyboardButton(text="Последние 30 дней", callback_data="stat_30"),
        types.InlineKeyboardButton(text="Количество пользователей", callback_data="stat_all"),
        types.InlineKeyboardButton(text="Назад ⏪", callback_data="stat_back")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def keyboard_link(link_tg, link_vk):
    buttons = [
        types.InlineKeyboardButton(text="Рассказать друзьям Telegram", switch_inline_query=link_tg),
        types.InlineKeyboardButton(text="Рассказать друзьям ВКонтакте", url=link_vk)]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard