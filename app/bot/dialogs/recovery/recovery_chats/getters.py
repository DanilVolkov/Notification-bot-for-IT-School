from aiogram_dialog import DialogManager


async def get_del_chats(**kwargs):
    # TODO: сделать получение чатов и сортировку при запросе
    chats = [
        ('Базовый Python 2026 1 поток', 1),
        ('Docker 2026 1 поток', 2),
        ('Javascript junior', 3),
        ('Сетевое и системное администрирование: Linux', 4),
        ('DevOps', 5),
        ('1С-разработчик', 6),
        ('Javascript Fullstack', 7),
        ('Сетевое и системное администрирование: сети и телекоммуникации', 8),
        ('Основы Astra Linux', 9),
        ('Введение в контейнеризацию', 10),
        ('Введение в Kubernetes', 11),
    ]
    return {'list_chats': chats}


async def get_recovery_chat(dialog_manager: DialogManager, **kwargs):
    recovery_chat_name = dialog_manager.dialog_data.get('recovery_chat_name')
    recovery_mode = dialog_manager.dialog_data.get('recovery_mode')
    return {
        'recovery_chat_name': recovery_chat_name,
        'recovery_mode': recovery_mode
    }

