from aiogram_dialog import DialogManager

from app.bot.enums.user_role import UserRole
from app.bot.enums.user_status import UserStatus


async def get_account(dialog_manager: DialogManager, **kwargs):
    find_user_id = dialog_manager.start_data.get('user_id')
    # TODO: получение данных из БД о пользователе по его id

    find_user_fio = 'Иванов Иван Иваныч'
    find_user_role = 'админ'
    find_user_status = 'Активен'
    # TODO: добавить логику, что если я ищу сам себя, то я могу менять о себе информацию

    is_find_user_creator = True if find_user_role.lower() == UserRole.CREATOR else False

    user_id = dialog_manager.event.from_user.id
    print(user_id)
    print(find_user_id)
    user_role = dialog_manager.middleware_data.get('user_role').lower()

    if find_user_id == user_id and is_find_user_creator:
        # если создатель открыл свой аккаунт, значит он может менять информацию о себе
        is_find_user_creator = False

    # Получаем информацию о текущем пользователе, который управляет сейчас ботом
    is_admin = (
        True if user_role in [UserRole.CREATOR, UserRole.ADMIN] else False
    )  # TODO: вынести как свойство в класс
    is_find_user_blocked = True if find_user_status.lower() == UserStatus.BLOCK else False
    dialog_manager.dialog_data["find_user_fio"] = find_user_fio
    dialog_manager.dialog_data["find_user_role"] = find_user_role


    info = {
        'find_user_fio': find_user_fio,
        'find_user_id': find_user_id,
        'find_user_role': find_user_role,
        'is_admin': is_admin,
        'is_find_user_creator': is_find_user_creator,
        'find_user_status': find_user_status,
        'is_find_user_blocked': is_find_user_blocked,
    }

    print(info)
    return info


async def get_del_user_info(dialog_manager: DialogManager, **kwargs):
    del_user_id = dialog_manager.dialog_data.get("del_user_id")
    del_user_fio = dialog_manager.dialog_data.get("del_user_fio")
    return {
        'del_user_id': del_user_id,
        'del_user_fio': del_user_fio
    }


async def get_user_roles(dialog_manager: DialogManager, **kwargs):
    # TODO: получение ролей из БД
    # TODO: Роль "Создатель" появляется только у того, кто сам создатель
    user_roles = [('Админ', 1), ('Прокуратор', 2), ('Куратор', 3)]
    dialog_manager.dialog_data['roles'] = user_roles
    current_user_role = dialog_manager.dialog_data.get("user_role")
    return {
        'user_roles': user_roles,
        'current_user_role': current_user_role
    }