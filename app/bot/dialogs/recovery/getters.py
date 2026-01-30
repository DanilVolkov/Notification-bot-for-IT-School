from aiogram_dialog import DialogManager

from app.bot.enums.user_role import UserRole


# TODO: вынести в отдельный хендлер, так как такая же функция есть у main_menu -> это будет реалзиовано middleware
async def get_user(dialog_manager: DialogManager, **kwargs):
    user_role = dialog_manager.middleware_data.get(
        'user_role'
    ).lower()  # TODO: заменить потом на получение объекта их класса
    is_admin = True if user_role in [UserRole.CREATOR, UserRole.ADMIN] else False  # TODO: вынести как свойство в класс
    is_procurator = True if user_role == UserRole.PROCURATOR else False

    return {'is_admin': is_admin, 'is_procurator': is_procurator}
