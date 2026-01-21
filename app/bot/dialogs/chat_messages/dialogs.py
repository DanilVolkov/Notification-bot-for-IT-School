from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.chat_messages import handlers
from app.bot.dialogs.chat_messages.getters import (
    get_chat_info,
    get_chat_messages,
    get_chat_name,
    get_found_messages,
)
from app.bot.dialogs.states import ChatMessagesSG
from app.bot.handlers import other_handlers

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format("💬 {chat_name}"),
    SwitchTo(text=Const(buttons_texts.ADD_MESSAGE), id="btn_add_message", state=ChatMessagesSG.add_message_name),
    SwitchTo(text=Const(buttons_texts.FIND_MESSAGE), id="btn_find_message", state=ChatMessagesSG.find_messages),
    SwitchTo(
        text=Const(buttons_texts.CHANGE_CHAT_NAME), id="btn_change_chat_name", state=ChatMessagesSG.change_chat_name
    ),
    SwitchTo(
        text=Const(buttons_texts.CHAT_MESSAGES), id="btn_list_messages_chat_name", state=ChatMessagesSG.list_messages
    ),
    SwitchTo(
        text=Const(text=buttons_texts.DOWNLOAD_MESSAGES_FROM_EXCEL),
        id="btn_download_messages_from_excel",
        state=ChatMessagesSG.download_msgs_from_excel
    ),
    Cancel(Const(buttons_texts.CANCEL), id="btn_chat_info_cancel"),
    state=ChatMessagesSG.start,
    getter=get_chat_info,
)

list_messages_windows = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format("💬 {chat_name}"),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="messages",
            item_id_getter=lambda x: x[1],
            items="list_messages",
            on_click=handlers.set_message_info,
        ),
        id="messages_paginator",
        width=buttons_texts.COUNT_MESSAGES_WIDTH,
        height=buttons_texts.COUNT_MESSAGES_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_list_messages_cancel", state=ChatMessagesSG.start),
    state=ChatMessagesSG.list_messages,
    getter=get_chat_messages,
)

add_message_name_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.NAME_MESSAGE),
    TextInput(id="name_message_input", type_factory=str, on_success=handlers.save_message_name),
    MessageInput(func=other_handlers.no_text),
    # TODO: здесь записываем только в dialog_data, в БД загрузка только после заполнения всех полей
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_name_cancel", state=ChatMessagesSG.start),
    state=ChatMessagesSG.add_message_name,
)


add_message_text_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.TEXT_MESSAGE),
    TextInput(id="text_message_input", type_factory=str, on_success=handlers.save_message_text),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_text_cancel", state=ChatMessagesSG.add_message_name),
    state=ChatMessagesSG.add_message_text,
)

add_message_datetime_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.TIME_SEND_MESSAGE),
    TextInput(
        id="datetime_message_input",
        type_factory=other_handlers.datetime_check,
        on_success=handlers.save_message_datetime,
        on_error=other_handlers.error_datetime,
    ),
    MessageInput(func=other_handlers.no_text),
    Row(
        Button(
            Const(buttons_texts.WITHOUT_DATETIME),
            id="btn_without_datetime",
            on_click=handlers.save_message_without_datetime,
        ),
        SwitchTo(
            Const(buttons_texts.CANCEL), id="btn_add_message_datetime_cancel", state=ChatMessagesSG.add_message_text
        ),
    ),
    state=ChatMessagesSG.add_message_datetime,
)


change_chat_name = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format(
        "Текущее название чата:\n<code>{chat_name}</code>\n\n" + f"{labels_texts.CHAT_NAME_INFO}\n\n"
        f"{labels_texts.CHAT_NAME}"
    ),
    TextInput(id="new_chat_name_input", type_factory=str, on_success=handlers.update_chat_name),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_chat_name_cancel", state=ChatMessagesSG.start),
    state=ChatMessagesSG.change_chat_name,
    getter=get_chat_name,
)


find_message_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.FIND_MESSAGE),
    TextInput(id="chat_input", type_factory=str, on_success=handlers.find_message),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_find_messages_cancel", state=ChatMessagesSG.start),
    state=ChatMessagesSG.find_messages,
)


found_messages_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format(text=labels_texts.FOUND_MESSAGES, when="is_found_messages"),
    Format(text=labels_texts.NOT_FOUND_MESSAGES, when="is_not_found_messages"),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="found_messages_id",
            item_id_getter=lambda x: x[1],  # TODO: доделать копирование сообщений чата по его id
            items="found_messages",
            on_click=handlers.set_message_info,
        ),
        id="found_messages_paginator",
        width=buttons_texts.COUNT_MESSAGES_WIDTH,
        height=buttons_texts.COUNT_MESSAGES_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_found_messages_cancel", state=ChatMessagesSG.start),
    state=ChatMessagesSG.found_messages,
    getter=get_found_messages,
)


download_msgs_from_excel_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.DOWNLOAD_MESSAGES_FROM_EXCEL),
    MessageInput(func=handlers.download_msgs_from_excel,
                 content_types=ContentType.DOCUMENT
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_download_msgs_from_excel_cancel", state=ChatMessagesSG.start),
    state=ChatMessagesSG.download_msgs_from_excel,
)


download_msgs_from_excel_done = Window(
    Format('✅ Сообщения загружены в чат "{chat_name}"'),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_download_msgs_from_excel_done_cancel", state=ChatMessagesSG.start),
    state=ChatMessagesSG.download_msgs_from_excel_done,
    getter=get_chat_name
)

chats_messages_dialog = Dialog(
    main_window,
    list_messages_windows,
    add_message_name_window,
    add_message_text_window,
    add_message_datetime_window,
    change_chat_name,
    find_message_window,
    found_messages_window,
    download_msgs_from_excel_window,
    download_msgs_from_excel_done
)
