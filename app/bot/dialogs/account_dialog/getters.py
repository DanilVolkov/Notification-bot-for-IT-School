from aiogram_dialog import DialogManager


async def get_account(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data.get('user_id')
    # TODO: получение данных из БД о пользователе по его id
    user_fio = 'Иванов Иван Иваныч'
    user_role = 'Прокуратор'
    user_status = 'Активен'
    return {'user_fio': user_fio, 'user_id': user_id, 'user_role': user_role, 'user_status': user_status}
