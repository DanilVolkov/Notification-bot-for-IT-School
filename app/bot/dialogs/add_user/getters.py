from aiogram_dialog import DialogManager


async def get_user_roles(dialog_manager: DialogManager, **kwargs):
    # TODO: получение ролей из БД
    # TODO: Роль "Создатель" появляется только у того, кто сам создатель
    user_roles = [('Админ', 1), ('Прокуратор', 2), ('Куратор', 3)]
    dialog_manager.dialog_data['roles'] = user_roles
    return {'user_roles': user_roles}


async def get_user_info(dialog_manager: DialogManager, **kwargs):
    user_fio = dialog_manager.dialog_data.get('user_fio')
    user_role_id = dialog_manager.dialog_data.get('user_role_id')
    user_role: str = dialog_manager.dialog_data.get('user_role')

    return {'user_fio': user_fio, 'user_role_id': user_role_id, 'user_role': user_role.capitalize()}


async def get_user_link(dialog_manager: DialogManager, **kwargs):
    user_link = dialog_manager.dialog_data.get('user_link')
    return {'user_link': user_link}
