from aiogram_dialog import DialogManager


async def get_del_users(dialog_manager: DialogManager, **kwargs):
    # TODO: сделать получение чатов и сортировку при запросе
    users = [
        ('Иванов Иван Иваныч', 1),
        ('Большков Сергей Дмитриевич', 2),
        ('Исаков Михаил Алексеевич', 3),
    ]
    return {'list_users': users}


async def get_recovery_user(dialog_manager: DialogManager, **kwargs):
    recovery_username = dialog_manager.dialog_data.get('recovery_username')
    recovery_user_id = dialog_manager.dialog_data.get('recovery_user_id')
    recovery_user_role = dialog_manager.dialog_data.get('recovery_user_role')
    recovery_user_status = dialog_manager.dialog_data.get('recovery_user_status')
    return {
        'recovery_username': recovery_username,
        'recovery_user_id': recovery_user_id,
        'recovery_user_role': recovery_user_role,
        'recovery_user_status': recovery_user_status
    }
