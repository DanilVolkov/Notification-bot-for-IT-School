import hashlib
from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button

from app.bot.consts import labels_texts
from app.bot.dialogs.states import AddUserSG


def check_user_fio(user_fio: str) -> str:
    fio = user_fio.strip().split()
    if len(fio) == 3 and all(map(lambda s: s.isalpha(), fio)):
        return user_fio
    raise ValueError

async def save_fio_user(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data["user_fio"] = text
    await dialog_manager.switch_to(AddUserSG.add_role)

async def error_info_user(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    await message.answer(labels_texts.INCORRECT_INFO_USER)

async def save_user_info(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    roles = dialog_manager.dialog_data.get("roles")
    role_id = int(item_id)
    user_role = next(filter(lambda role: role[1] == role_id, roles))[0]
    dialog_manager.dialog_data["user_role_id"] = role_id  # TODO: id нужен для создания ссылки для поиска потом в БД роли
    dialog_manager.dialog_data["user_role"] = user_role

    await dialog_manager.switch_to(AddUserSG.user_info) # TODO: подумать, как удалять токен через день после создания в БД


async def create_user_link(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # TODO: заменить на redis

    # def create_registration_token(user_data: dict, ttl_seconds: int = 86400):
    #     token = uuid.uuid4().hex[:10]
    #
    #     redis_client.setex(
    #         token,
    #         ttl_seconds,
    #         json.dumps(user_data)
    #     )
    #     return token
    # user_info = {"role": "user", "fio": "Анна", "email": "anna@example.com"}
    # token = create_registration_token(user_info)
    # print(f"Ссылка для пользователя: t.me/bot?start={token}")

    # Ссылка создается в redis по ключу. Когда пользователь добавляется - в redis ищется токен в ссылке (по ключу)
    # Если найден - пользователь добавляется в БД

    user_fio = dialog_manager.dialog_data.get("user_fio")
    user_role_id = dialog_manager.dialog_data.get("user_role_id")
    user_role = dialog_manager.dialog_data.get("user_role_id")

    params = f"fio_{user_fio}_roleid_{user_role_id}_time_{str(datetime.now())}"
    # Создаём уникальный хеш
    token = hashlib.sha256(f"{params}".encode()).hexdigest()
    # Ссылка
    bot_info = await dialog_manager.event.bot.get_me()
    link = f"https://t.me/{bot_info.username}?start={token}"

    dialog_manager.dialog_data["user_link"] = link
    await dialog_manager.switch_to(AddUserSG.create_link)
