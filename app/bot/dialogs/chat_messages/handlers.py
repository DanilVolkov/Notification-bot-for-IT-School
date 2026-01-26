import logging
import os

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select

from app.bot.consts import labels_texts
from app.bot.dialogs.states import ChatMessagesSG, MessageInfoSG
from app.bot.handlers.other_handlers import check_correct_table

logger = logging.getLogger(__name__)


async def set_message_info(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    chat_id = dialog_manager.start_data.get('chat_id')

    logger.info(f'Получение сообщения {item_id} из чата {chat_id}')

    await dialog_manager.start(MessageInfoSG.start, data={'message_id': item_id, 'chat_id': chat_id})


async def save_message_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await dialog_manager.switch_to(ChatMessagesSG.add_message_text)


async def save_message_text(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await dialog_manager.switch_to(ChatMessagesSG.add_message_datetime)


async def save_message_datetime(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    chat_id = dialog_manager.start_data.get('chat_id')
    # TODO: создание в БД нового сообщения одной отдельной функцией
    # TODO: получение id сообщения
    await dialog_manager.switch_to(ChatMessagesSG.start)
    await dialog_manager.start(MessageInfoSG.start, data={'message_id': 5, 'chat_id': chat_id})


async def save_message_without_datetime(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    chat_id = dialog_manager.start_data.get('chat_id')
    # TODO: создание в БД нового сообщения одной отдельной функцией
    # TODO: получение id сообщения
    await dialog_manager.switch_to(ChatMessagesSG.start)
    await dialog_manager.start(MessageInfoSG.start, data={'message_id': 5, 'chat_id': chat_id})


async def update_chat_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    # TODO: изменение имени чата

    await dialog_manager.switch_to(state=ChatMessagesSG.start)


async def find_message(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    bot = dialog_manager.event.bot
    msg = await bot.send_message(chat_id=message.from_user.id, text=labels_texts.FIND_MESSAGE_PROCESS)
    # TODO: поиск сообщений в БД

    found_messages = [
        '✅ 12.01.2026 17:30 Название сообщения',
        '12.01.2026 17:35 Название сообщения',
    ]  # TODO: найденные чаты в БД
    # found_messages.clear()
    dialog_manager.dialog_data['found_messages'] = found_messages
    await msg.delete()
    await dialog_manager.switch_to(ChatMessagesSG.found_messages)


async def download_msgs_from_excel(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    bot = dialog_manager.event.bot

    document = message.document

    if document.file_name.split('.')[-1].endswith('xlsx'):
        msg = await bot.send_message(chat_id=message.from_user.id, text=labels_texts.DOWNLOAD_MSGS_FROM_EXCEL_PROCESS)
        file_on_server = await bot.get_file(document.file_id)
        file_path = f'./temp_excel_files/{document.file_unique_id}_{document.file_name}'
        await bot.download_file(file_on_server.file_path, file_path)
        is_valid, msg_error, df = check_correct_table(file_path)

        if not is_valid:
            await msg.delete()
            await message.answer(msg_error)
        else:
            pass
            # TODO: отправка файла в БД
            await msg.delete()
            await dialog_manager.switch_to(ChatMessagesSG.download_msgs_from_excel_done)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f'Файл удалён: {file_path}')
            else:
                logger.debug(f'Файл не найден: {file_path}')
        except PermissionError:
            logger.warning(f'Недостаточно прав для удаления файла: {file_path}')
        except OSError as ex:
            logger.warning(f'Ошибка при удалении файла {file_path}: {ex}')

    else:
        await message.answer(labels_texts.INCORRECT_EXTENSION)
