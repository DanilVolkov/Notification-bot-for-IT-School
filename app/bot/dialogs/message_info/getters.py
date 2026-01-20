from aiogram_dialog import DialogManager

from app.bot.consts import labels_texts
from app.bot.enums.message_statuses import MessageStatus


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


async def get_message_info(dialog_manager: DialogManager, **kwargs):
    # TODO: запрос данных из БД по id сообщения и id чата
    chat_id = dialog_manager.start_data.get("chat_id")
    message_id = dialog_manager.start_data.get("message_id")


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

    if (message_status.SENT or message_status.PLANNED) and message_datetime:
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
    is_datetime = False
    if message_datetime:
        is_datetime = True

    return {
        "message_datetime": message_datetime,
        "is_datetime": is_datetime,
        "not_is_datetime": not is_datetime
    }