import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.database.DB import Database


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin
        adm = Database().get_admins()
        self.admins = []
        for admin in adm:
            self.admins.append(admin[0])

    async def check(self, obj):
        if self.is_admin is None:
            return False
        return (obj.from_user.id in self.admins) == self.is_admin


class BlockedFilter(BoundFilter):
    key = 'is_blocked'

    def __init__(self, is_blocked: typing.Optional[bool] = None):
        self.is_blocked = is_blocked
        adm = Database().up_blocked()
        self.blocked = []
        for blocked in adm:
            self.blocked.append(blocked[0])

    async def check(self, obj):
        if self.is_blocked is None:
            return False
        return (obj.from_user.id in self.blocked) == self.is_blocked
