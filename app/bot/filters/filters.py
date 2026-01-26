from aiogram.filters import BaseFilter


class HasRoleFilter(BaseFilter):
    def __init__(self, roles: list[str]):
        self.roles = roles

    async def __call__(self, data) -> bool:
        user_role = data.get('role')
        return user_role in self.roles


class IsAdminFilter(BaseFilter):
    async def __call__(self, data) -> bool:
        return data.get('role') == 'admin'
