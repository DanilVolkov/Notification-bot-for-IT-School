from aiogram.types import User


async def get_account(event_from_user: User, **kwargs):
    # получение данных из БД
    return {
        'user': f'{event_from_user.first_name} {event_from_user.last_name}',
        'user_id': event_from_user.id,
        'user_role': 'Админ'
    }