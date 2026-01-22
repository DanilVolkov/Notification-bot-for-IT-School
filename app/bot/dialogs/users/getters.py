from aiogram_dialog import DialogManager


async def get_users(dialog_manager: DialogManager, **kwargs):
    # TODO: сделать получение чатов и сортировку при запросе
    users = [
        ("Иванов Иван Иваныч", 1),
        ("Большков Сергей Дмитриевич", 2),
        ("Исаков Михаил Алексеевич", 3),
    ]
    return {"list_users": users}