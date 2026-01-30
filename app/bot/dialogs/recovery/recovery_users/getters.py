from aiogram_dialog import DialogManager


async def get_users(dialog_manager: DialogManager, **kwargs):
    # TODO: сделать получение чатов и сортировку при запросе
    users = [
        ('Иванов Иван Иваныч', 1),
        ('Большков Сергей Дмитриевич', 2),
        ('Исаков Михаил Алексеевич', 3),
    ]
    return {'list_users': users}


async def get_recovery_user(dialog_manager: DialogManager, **kwargs):
    recovery_username = dialog_manager.dialog_data.get('recovery_username')
    return {'recovery_username': recovery_username}
