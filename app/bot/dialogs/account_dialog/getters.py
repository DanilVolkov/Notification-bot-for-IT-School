from aiogram_dialog import DialogManager

from app.bot.enums.user_role import UserRole
from app.bot.enums.user_status import UserStatus


async def get_account(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data.get('user_id')
    # TODO: получение данных из БД о пользователе по его id
    user_fio = 'Иванов Иван Иваныч'
    user_role = 'Прокуратор'
    user_status = 'Активен'
    # создателя нельзя заблокировать/удалить и сменить о нём информацию
    is_find_user_creator = True if user_role.lower() == UserRole.CREATOR else False
    is_admin = True if dialog_manager.middleware_data.get('user_role') in [UserRole.CREATOR, UserRole.ADMIN] else False  # TODO: вынести в отдельный хендлер для всех
    user_blocked = True if user_status.lower() == UserStatus.BLOCK else False
    return {
        'user_fio': user_fio,
        'user_id': user_id,
        'user_role': user_role,
        'is_admin': is_admin,
        'is_find_user_creator': is_find_user_creator,
        'user_status': user_status,
        'user_blocked': user_blocked,
    }


