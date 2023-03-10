from aiogram import *
import datetime
import aioschedule
from datetime import date
from database import DataBase
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import asyncio



TOKEN = "5600687214:AAHm76vFT2PZ6ze0OWYPN-Xi3tQuPtWhtA0"
admin_list = []
rename = ['rename_1', 'rename_2', 'rename_3', 'rename_4', 'rename_5', 'rename_6', 'rename_7', 'rename_8', 'rename_9', 'rename_10', 'rename_11', 'rename_12', 'rename_13', 'rename_14', 'rename_15', 'rename_16', 'rename_17', 'rename_18', 'rename_19', 'rename_20', 'rename_21', 'rename_22']

# 0 - первая часть приветствия
# 1 - вторая часть приветствия
# 2 - с возвращением
# 3 - привел 1 друга в течение часа ч1
# 4 - привел 1 друга в течение часа ч2
# 5 - вы уже восп. реф. Ссылкой
# 6 - бонус 1
# 7 - бонус 2
# 8 - привел 2 друзей в течение часа ч1
# 9 - привел 2 друзей в течение часа ч2
# 10 - привел 3 друзей в течение часа ч1
# 11 - привел 3 друзей в течение часа ч2
# 12 - привел 4 друзей в течение часа ч1
# 13 - привел 4 друзей в течение часа ч2
# 14 - привел 5 друзей в срок
# 15 - привел 5 друзей не в срок
# 16 - кстати - нажмите на кнопку универсальная
# 17 - привел 6 друзей
# 18 - привел 7 друзей
# 19 - привел 8 друзей
# 20 - привел 9 друзей
# 21 - привел 10 друзей ч1
# 22 - привел 10 друзей ч2
inter = []
with open('messages.txt', encoding='utf-8') as file:
    text = file.read()

for i in range(len(text)-4):
    if text[i:i+2] == "**" and text[i+2] != '*':
        message = ''
        while text[i+2:i+5] != "***":
            message += text[i+2]
            i += 1
        inter.append(message)

static_messages = []
for elem in inter:
    if "**" not in elem:
        static_messages.append(elem)


def auto_messages(num_):
    inter_ = []
    with open('auto_message.txt', encoding='utf-8') as file_:
        text_ = file_.read()

    for i_ in range(len(text_) - 4):
        if text_[i_:i_ + 2] == "**" and text_[i_ + 2] != '*':
            message_ = ''
            while text_[i_ + 2:i_ + 5] != "***":
                message_ += text_[i_ + 2]
                i_ += 1
            inter_.append(message_)

    static_messages_ = []
    for elem_ in inter_:
        if "**" not in elem_:
            static_messages_.append(elem_)
    return static_messages_[num_]


