import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path

from aiogram.types import Message


@dataclass
class User:
    telegram_id: int
    username: str
    fullname: str
    registration_time: int
    referrals: int
    active: int
    count_messages: int


@dataclass
class BlockUser:
    telegram_id: int
    username: str
    fullname: str
    registration_time: int
    referrals: int
    active: int
    count_messages: int


@dataclass
class MessageSend:
    Role: str
    Message: str
    Media_content: str


@dataclass
class MessageAutoSend:
    Role: str
    Message: str
    Media_content: str
    Schedule: bool
    Time_schedule: int
    Keyboard: str


class Database:
    def __init__(self):
        cwd_path = Path.cwd()
        users_path = Path(cwd_path, "tgbot", "database", "Users.db")
        setting_path = Path(cwd_path, "tgbot", "database", "Settings.db")
        self.conn_us = sqlite3.connect(users_path)
        self.cur_us = self.conn_us.cursor()
        self.cur_us.execute("""CREATE TABLE IF NOT EXISTS Пользователи(
        Telegram_id INT PRIMARY KEY,
        Username TEXT,
        Fullname TEXT,
        Registration_time TEXT,
        Referrals INT,
        Active INT,
        Count_messages INT
        );""")
        self.conn_us.commit()
        self.conn_set = sqlite3.connect(setting_path)
        self.cur_set = self.conn_set.cursor()
        self.cur_set.execute("""CREATE TABLE IF NOT EXISTS Сообщения(
        Role TEXT PRIMARY KEY,
        Message TEXT,
        Media_content TEXT
        );""")
        self.conn_set.commit()
        self.cur_set.execute("""CREATE TABLE IF NOT EXISTS АвтоCообщения(
        Role TEXT PRIMARY KEY,
        Message TEXT,
        Media_content TEXT,
        Schedule BOOL,
        Time_schedule INT,
        Keyboard TEXT)
        ;""")
        self.conn_set.commit()
        self.cur_set.execute("""CREATE TABLE IF NOT EXISTS Заблокированные(
        Telegram_id INT PRIMARY KEY,
        Username TEXT,
        Fullname TEXT,
        Registration_time TEXT,
        Referrals INT,
        Active INT,
        Count_messages INT
        );""")
        self.conn_set.commit()
        self.cur_set.execute("""CREATE TABLE IF NOT EXISTS Основные(
        ID INT PRIMARY KEY,
        Username TEXT
        );""")
        self.conn_set.commit()

    '''ПОЛЬЗОВАТЕЛИ'''

    def add_user(self, message: Message):
        telegram_id = message.from_user.id
        username = message.from_user.username
        fullname = f'{message.from_user.first_name} {message.from_user.last_name}'
        registration_time = int(time.time())
        referral = 0
        active = 1
        count_messages = 0
        self.cur_us.execute("INSERT INTO Пользователи VALUES(?,?,?,?,?,?,?);",
                            [telegram_id, username, fullname, registration_time, referral, active, count_messages])
        self.conn_us.commit()

    def update(self, index, val, user):
        self.cur_us.execute(f"UPDATE Пользователи SET {index} = '{val}' WHERE Telegram_id = {user};")
        self.conn_us.commit()

    def user_exist(self, user_id):
        self.cur_us.execute(f"SELECT COUNT(*) FROM Пользователи WHERE Telegram_id = {user_id}")
        count = self.cur_us.fetchone()[0]
        if count != 0:
            return True
        else:
            return False

    def get_user(self, user_id):
        self.cur_us.execute("SELECT * FROM Пользователи")
        users = self.cur_us.fetchall()
        if len(users) != 0:
            for i in range(len(users)):
                if users[i][0] == user_id:
                    return User(telegram_id=users[i][0], username=users[i][1], fullname=users[i][2],
                                registration_time=users[i][3], referrals=users[i][4], active=users[i][5],
                                count_messages=users[i][6])

    def up_sub(self):
        self.cur_us.execute("SELECT * FROM Пользователи")
        users = self.cur_us.fetchall()
        if len(users) != 0:
            return users

    '''Заблокированные'''

    def add_block_user(self, telegram_id):
        user = self.get_user(telegram_id)
        user = [user.telegram_id, user.username, user.fullname, user.registration_time, user.referrals, user.active,
                user.count_messages]
        self.cur_set.execute("INSERT INTO Заблокированные VALUES(?,?,?,?,?,?,?);", user)
        self.conn_set.commit()

    def get_block_user(self, telegram_id):
        self.cur_set.execute("SELECT * FROM Заблокированные WHERE Telegram_id =?", [telegram_id])
        users = self.cur_set.fetchall()
        if len(users) == 0:
            for i in range(len(users)):
                if users[i][0] == telegram_id:
                    return BlockUser(telegram_id=users[i][0], username=users[i][1], fullname=users[i][2],
                                     registration_time=users[i][3], referrals=users[i][4], active=users[i][5],
                                     count_messages=users[i][6])

    def del_block_user(self, telegram_id):
        self.cur_set.execute("DELETE FROM Заблокированные WHERE Telegram_id =?", [telegram_id])
        self.conn_set.commit()

    def up_blocked(self):
        self.cur_set.execute("SELECT * FROM Заблокированные")
        users = self.cur_set.fetchall()
        if len(users) != 0:
            return users
        else:
            return ''

    '''Сообщения'''

    def get_message(self, role):
        self.cur_set.execute("SELECT * FROM Сообщения")
        message = self.cur_set.fetchall()
        if len(message) != 0:
            for i in range(len(message)):
                if message[i][0] == role:
                    return MessageSend(Role=message[i][0], Message=message[i][1], Media_content=message[i][2])

    def update_message(self, role: str, message: str):
        self.cur_set.execute(f"UPDATE Сообщения SET Message = '{message}' WHERE Role = '{role}';")
        self.conn_set.commit()
        print("Updated")

    def up_message(self):
        self.cur_set.execute("SELECT * FROM Сообщения")
        message = self.cur_set.fetchall()
        if len(message) != 0:
            return message
        else:
            return ''

    def get_auto_message(self, role: str):
        self.cur_set.execute("SELECT * FROM АвтоCообщения")
        message = self.cur_set.fetchall()
        if len(message) != 0:
            for i in range(len(message)):
                if message[i][1] == role:
                    return MessageAutoSend(
                        Role=message[i][0],
                        Message=message[i][1],
                        Media_content=message[i][3],
                        Schedule=message[i][4],
                        Time_schedule=message[i][5],
                        Keyboard=message[i][6])

    def update_auto_message(self, role: str, message: str, media_content: str = None, keyboard: str = None,
                            schedule: bool = False, time_schedule: int = None):
        if media_content is not None:
            self.cur_set.execute(f"UPDATE АвтоCообщения SET Media_content = '{media_content}' WHERE Role = {role};")
        if schedule:
            self.cur_set.execute(f"UPDATE АвтоCообщения SET Schedule = '{schedule}' WHERE Role = {role};")
        if time_schedule is not None:
            self.cur_set.execute(f"UPDATE АвтоCообщения SET Time_schedule = '{time_schedule}' WHERE Role = {role};")
        if keyboard is not None:
            self.cur_set.execute(f"UPDATE АвтоCообщения SET Keyboard = '{keyboard}' WHERE Role = {role};")
        self.cur_set.execute(f"UPDATE АвтоCообщения SET Message = '{message}' WHERE Role = {role};")
        self.conn_set.commit()

    def add_auto_message(self, role: str, message: str, media_content: str = None, schedule: bool = False,
                         time_schedule: int = None, keyboard: str = None):
        self.cur_set.execute("INSERT INTO АвтоCообщения VALUES(?,?,?,?,?,?);",
                             [role, message, media_content, schedule, time_schedule, keyboard])
        self.conn_set.commit()

    def delete_auto_message(self, role):
        self.cur_us.execute(f"DELETE FROM АвтоCообщения WHERE Role = '{role}';")
        self.conn_us.commit()

    def up_auto_message(self):
        self.cur_set.execute("SELECT * FROM АвтоCообщения")
        message = self.cur_set.fetchall()
        if len(message) != 0:
            return message
        else:
            return ''

    '''Основные'''

    def get_admins(self):
        self.cur_set.execute("SELECT * FROM Основные")
        users = self.cur_set.fetchall()
        if len(users) != 0:
            return users
        else:
            return ''

    def delete_admin(self, user_id):
        self.cur_set.execute("DELETE FROM Основные WHERE ID =?", [user_id])
        self.conn_set.commit()
