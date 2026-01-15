import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.bot.dialogs.states import ChatsSG

logger = logging.getLogger(__name__)

async def chat_copy_from(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    logger.debug(f'Выбран чат, откуда копировать, с id={item_id}')
    dialog_manager.dialog_data['chat_from_id'] = item_id
    await dialog_manager.switch_to(state=ChatsSG.copy_messages_in_chat)


async def chat_copy_in(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    logger.debug(f'Выбран чат, куда копировать, с id={item_id}')

    if dialog_manager.dialog_data.get('chat_from_id') == item_id:
        await callback.answer(text="Нельзя копировать сообщения в один и тот же чат!", show_alert=True)
        return

    logger.debug(f'Копирование сообщений из чата с id = {dialog_manager.dialog_data.get('chat_from_id')}'
                 f' в чат с id {item_id}')
    dialog_manager.dialog_data['chat_in_id'] = item_id
    # TODO: обмен данными с БД
    await dialog_manager.switch_to(state=ChatsSG.copy_messages_done)