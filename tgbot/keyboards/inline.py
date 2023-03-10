from aiogram import types, bot
from tgbot.database.DB import Database as Db


class InlineKeyboard:
    def __init__(self):
        self.inline_keyboard = types.InlineKeyboardMarkup
        self.button = types.InlineKeyboardButton
        pass

    def reposts_old(self, link, bot_name):
        buttons = [
            self.button(text="Рассказать друзьям Telegram",
                        switch_inline_query="test"),
            self.button(text="Рассказать друзьям ВКонтакте", url='https://ya.ru')
        ]
        keyboard = self.inline_keyboard(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    def reposts(self, link):
        switch = Db().get_message('Tg_repost_msg').Message
        buttons = [
            self.button(text="Рассказать друзьям Telegram",
                        switch_inline_query='\n' + switch.replace('[link]', link))
        ]
        keyboard = self.inline_keyboard(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    def menu_account(self):
        buttons = [
            self.button(text="Подписка", callback_data="back_to_account"),
            self.button(text="Инфо", callback_data="back_to_account"),
            self.button(text="Поддержка", callback_data="back_to_account"),
            self.button(text="Меню", callback_data="get_menu"),
        ]
        keyboard = self.inline_keyboard()
        keyboard.add(buttons[0])
        keyboard.add(buttons[1], buttons[2])
        keyboard.add(buttons[3])
        return keyboard


class InlineKeyboardAdmin:
    def __init__(self):
        self.inline_keyboard = types.InlineKeyboardMarkup
        self.button = types.InlineKeyboardButton
        pass

    def reposts(self, link):
        switch = Db().get_message('Tg_repost_msg').Message
        buttons = [
            self.button(text="Рассказать друзьям Telegram",
                        switch_inline_query='\n' + switch.replace('[link]', link))
        ]
        keyboard = self.inline_keyboard(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    """Меню"""

    def admin_menu(self):
        buttons = [
            self.button(text="Параметры", callback_data="ad_settings"),
            self.button(text="Текста", callback_data="ad_txt"),
            self.button(text="Статистика", callback_data="ad_sttistics"),
            self.button(text="Пользователи", callback_data="ad_users"),
            self.button(text="Рассылка", callback_data="ad_senders"),
        ]
        keyboard = self.inline_keyboard()
        keyboard.add(buttons[0], buttons[1])
        keyboard.add(buttons[2])
        return keyboard

    """Разделы"""

    def settings(self):
        buttons = [
            self.button(text="Администраторы", callback_data="ad_admins"),
            self.button(text="Заблокированные", callback_data="ad_blocked"),
            self.button(text="Назад", callback_data="ad_edit_menu")
        ]
        keyboard = self.inline_keyboard()
        keyboard.add(buttons[0])
        keyboard.add(buttons[1])
        keyboard.add(buttons[2])
        return keyboard

    def statistics(self):
        buttons = [
            self.button(text="Неделя", callback_data="ad_stat_week"),
            self.button(text="Месяц", callback_data="ad_stat_month"),
            self.button(text="Всё время", callback_data="ad_stat_all_time"),
            self.button(text="Назад", callback_data="ad_edit_menu")
        ]
        keyboard = self.inline_keyboard()
        keyboard.add(buttons[0], buttons[1])
        keyboard.add(buttons[2])
        keyboard.add(buttons[3])
        return keyboard

    def texts(self):
        buttons = [
            self.button(text="Приветствие", callback_data="ad_text_start"),
            self.button(text="Рефералы", callback_data="ad_text_referral"),
            self.button(text="Остальное", callback_data="ad_text_rest"),
            self.button(text="Назад", callback_data="ad_edit_menu")
        ]
        keyboard = self.inline_keyboard()
        keyboard.add(buttons[0], buttons[1])
        keyboard.add(buttons[2])
        keyboard.add(buttons[3])
        return keyboard

    def senders(self):
        buttons = [
            self.button(text="Запланированные", callback_data="ad_send_scheduled"),
            self.button(text="Автоматические", callback_data="ad_send_automatic"),
            self.button(text="Назад", callback_data="ad_edit_menu")
        ]
        keyboard = self.inline_keyboard()
        keyboard.add(buttons[0])
        keyboard.add(buttons[1])
        keyboard.add(buttons[2])
        return keyboard

    """Меню раздела"""
