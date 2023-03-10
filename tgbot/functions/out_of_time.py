


# class OutOfTime:
#     def __init__(self, message: Message):
#         self.bot = message.bot
#         self.message = message
#         self.send = self.bot.send_message
#
#     async def check(self):
#         inviter_id = int(self.message.text.split()[1])
#         referrals = int(Db().get_user(inviter_id).referrals)
#         bot_name = await self.bot.get_me()
#         link = f"https://t.me/{bot_name.username}?start={inviter_id}"
#         await self.message.answer(text="ты перешёл по ссылке")
#         await self.send(chat_id=inviter_id,
#                         text=Db().get_message("new_referral").Message.replace('[referrals]', referrals).replace('[link]', link),
#                         reply_markup=InlineKeyboard().reposts(link))
        # if referrals == 1:
        #     await self.send(chat_id=inviter_id,
        #                     text=Db().get_message("1_referral").Message,
        #                     reply_markup=InlineKeyboard().reposts(link, bot_name))
        # if referrals == 2:
        #     await self.send(chat_id=inviter_id,
        #                     text=Db().get_message("2_referral").Message,
        #                     reply_markup=InlineKeyboard().reposts(link, bot_name))
        # if referrals == 3:
        #     await self.send(chat_id=inviter_id,
        #                     text=Db().get_message("3_referral").Message,
        #                     reply_markup=InlineKeyboard().reposts(link, bot_name))
        # if referrals == 4:
        #     await self.send(chat_id=inviter_id,
        #                     text=Db().get_message("4_referral").Message,
        #                     reply_markup=InlineKeyboard().reposts(link, bot_name))
        # if referrals == 5:
        #     if (int(time.time()) - int(Db().get_user(inviter_id).registration_time)) <= 3600:
        #         print('Registration')
        #         text = Db().get_message("5_referral").Message
        #     else:
        #         print('Out of time')
        #         text = Db().get_message("5_referral_out_of_time").Message
        #     await self.send(chat_id=inviter_id,
        #                     text=text,
        #                     reply_markup=InlineKeyboard().reposts(link, bot_name))

