import logging

from aiogram_dialog import DialogManager

from app.bot.consts import labels_texts
from app.bot.enums.message_statuses import MessageStatus

logger = logging.getLogger(__name__)


def get_sticker_from_status_message(status: MessageStatus):
    match status:
        case MessageStatus.SENT:
            return labels_texts.MESSAGE_STICKER_SENT
        case MessageStatus.PLANNED:
            return labels_texts.MESSAGE_STICKER_PLANNED
        case MessageStatus.DRAFT:
            return labels_texts.MESSAGE_STICKER_NONE
        case _:
            return ""


def get_text_from_status_message(status: MessageStatus):
    match status:
        case MessageStatus.SENT:
            return labels_texts.MESSAGE_TEXT_SENT
        case MessageStatus.PLANNED:
            return labels_texts.MESSAGE_TEXT_PLANNED
        case MessageStatus.DRAFT:
            return labels_texts.MESSAGE_TEXT_NONE
        case _:
            return ""


def parsing_message_status(status: str):
    status = status.strip()
    match status:
        case "Отправлено":
            return MessageStatus.SENT
        case "Запланировано":
            return MessageStatus.PLANNED
        case _:
            return MessageStatus.DRAFT


async def get_chat_messages(dialog_manager: DialogManager, **kwargs):
    # TODO: получение сообщений из чата их статуса и их парсинг по стикерам
    chat_id = dialog_manager.start_data.get("chat_id")
    chat_name = dialog_manager.start_data.get("chat_name")

    # TODO: получить статусы сообщений, названия, текста и времени из БД

    # TODO: добавить обработку для стикеров по статусу и формирование сообщения

    messages = [
        ("🕒 <дата> <время> <название>", 1),
        ("✅ 12.01.2026 17:30 Название сообщения", 2),
        ("Название сообщения", 3),
    ]
    return {"chat_name": chat_name, "list_messages": messages}


async def get_chat_name(dialog_manager: DialogManager, **kwargs):
    chat_name = dialog_manager.start_data.get("chat_name")
    return {"chat_name": chat_name}


async def get_chat_info(dialog_manager: DialogManager, **kwargs):
    chat_id = dialog_manager.start_data.get("chat_id")
    chat_name = dialog_manager.start_data.get("chat_name")
    return {"chat_id": chat_id, "chat_name": chat_name}


async def get_message_info(dialog_manager: DialogManager, **kwargs):
    # TODO: запрос данных из БД по id сообщения и id чата

    message_name = "Название сообщения"
    message_text = """Многострочный 
    Текст сообщения
Вот так вот"""
    message_datetime = "01.02.2026 17:30"  # TODO: парсинг даты из БД
    message_status_db = "Запланировано"

    message_status = parsing_message_status(message_status_db)

    # кешируем для изменения, чтобы запросы обрабатывались быстрее
    dialog_manager.dialog_data["message_name"] = message_name
    dialog_manager.dialog_data["message_text"] = message_text
    dialog_manager.dialog_data["message_datetime"] = message_datetime
    dialog_manager.dialog_data["message_status"] = message_status

    # message_name = dialog_manager.dialog_data.get("message_name", "")
    # message_text = dialog_manager.dialog_data.get("message_text", "")
    # message_date = dialog_manager.dialog_data.get("message_date", "")
    # message_time = dialog_manager.dialog_data.get("message_time", "")
    # message_status_db = dialog_manager.dialog_data.get("message_status", "")

    if message_status.SENT or message_status.PLANNED:
        message_status_sticker = get_sticker_from_status_message(message_status)
        message_status_text = get_text_from_status_message(message_status)

        message_date = message_datetime.split()[0]
        message_time = message_datetime.split()[1]

        message_info = (
            f"{message_name}\n\n"
            f"{message_text}\n\n"
            f"{message_status_sticker} {message_status_text} {message_date} в {message_time}"
        )
    else:
        message_info = f"{message_name}\n\n{message_text}"

    return {"message_info": message_info}


async def get_message_name(dialog_manager: DialogManager, **kwargs):
    message_name = dialog_manager.dialog_data.get("message_name")
    return {"message_name": message_name}


async def get_message_text(dialog_manager: DialogManager, **kwargs):
    message_text = dialog_manager.dialog_data.get("message_text")
    return {"message_text": message_text}


async def get_message_datetime(dialog_manager: DialogManager, **kwargs):
    message_datetime = dialog_manager.dialog_data.get("message_datetime")
    return {"message_datetime": message_datetime}


async def get_found_messages(dialog_manager: DialogManager, **kwargs):
    found_messages = dialog_manager.dialog_data.get("found_messages")
    found_messages = [(chat_name, index) for index, chat_name in enumerate(found_messages)]
    is_found_messages = True if found_messages else False
    return {
        "found_messages": found_messages,
        "is_found_messages": is_found_messages,
        "is_not_found_messages": not is_found_messages,
    }
