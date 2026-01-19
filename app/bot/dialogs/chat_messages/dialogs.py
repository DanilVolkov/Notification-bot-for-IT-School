from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select, SwitchTo, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.chat_messages.getters import get_chat_info, get_chat_messages, get_message_info, get_message_name, \
    get_message_text, get_message_datetime, get_chat_name, get_found_messages
from app.bot.dialogs.chat_messages import handlers
from app.bot.dialogs.states import MessagesSG
from app.bot.handlers.other_handlers import no_text

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('💬 {chat_name}'),
    SwitchTo(
        text=Const(buttons_texts.ADD_MESSAGE),
        id='btn_add_message',
        state=MessagesSG.add_message_name
    ),
    SwitchTo(
        text=Const(buttons_texts.FIND_MESSAGE),
        id='btn_find_message',
        state=MessagesSG.find_messages
    ),
    SwitchTo(
        text=Const(buttons_texts.CHANGE_CHAT_NAME),
        id='btn_change_chat_name',
        state=MessagesSG.change_chat_name
    ),
    SwitchTo(
        text=Const(buttons_texts.CHAT_MESSAGES),
        id='btn_list_messages_chat_name',
        state=MessagesSG.list_messages
    ),

    Cancel(Const(buttons_texts.CANCEL), id="btn_chat_info_cancel"),
    state=MessagesSG.start,
    getter=get_chat_info
)

list_messages_windows = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('💬 {chat_name}'),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="messages",
            item_id_getter=lambda x: x[1],
            items="list_messages",
            on_click=handlers.set_message_info
        ),
        id="messages_paginator",
        width=buttons_texts.COUNT_MESSAGES_WIDTH,
        height=buttons_texts.COUNT_MESSAGES_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_list_messages_cancel", state=MessagesSG.start),
    state=MessagesSG.list_messages,
    getter=get_chat_messages
)

add_message_name_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.NAME_MESSAGE),
    TextInput(id="name_message_input", type_factory=str, on_success=handlers.save_message_name),
    MessageInput(func=no_text),
    # TODO: здесь записываем только в dialog_data, в БД загрузка только после заполнения всех полей
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_name_cancel", state=MessagesSG.start),
    state=MessagesSG.add_message_name
)


add_message_text_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.TEXT_MESSAGE),
    TextInput(id="text_message_input", type_factory=str, on_success=handlers.save_message_text),
    MessageInput(func=no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_text_cancel", state=MessagesSG.add_message_name),
    state=MessagesSG.add_message_text
)


add_message_datetime_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.TIME_SEND_MESSAGE),
    TextInput(
        id="datetime_message_input",
        type_factory=handlers.datetime_check,
        on_success=handlers.save_message_datetime,
        on_error=handlers.error_datetime
    ),
    MessageInput(func=no_text),
    # TODO: добавить кнопку без времени
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_datetime_cancel", state=MessagesSG.add_message_text),
    state=MessagesSG.add_message_datetime
)  # TODO: после этого окна открывается окно с просмотром сообщения


message_info_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('{message_info}'),
    SwitchTo(Const(buttons_texts.CHANGE_MESSAGE_NAME), id="btn_change_message_name", state=MessagesSG.change_message_name),
    SwitchTo(Const(buttons_texts.CHANGE_MESSAGE_TEXT), id="btn_change_message_text", state=MessagesSG.change_message_text),
    SwitchTo(Const(buttons_texts.CHANGE_MESSAGE_DATETIME), id="btn_change_message_datetime", state=MessagesSG.change_message_datetime),
    SwitchTo(Const(buttons_texts.DEL_MESSAGE), id="btn_del_message", state=MessagesSG.del_message_confirm),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_message_info_cancel", state=MessagesSG.start),
    state=MessagesSG.message_info,
    getter=get_message_info
)

change_message_name_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущее название сообщения:\n<code>{message_name}</code>\n\nВведите новое название сообщения'),
    TextInput(id="new_message_name_input", type_factory=str, on_success=handlers.update_message_name),
    MessageInput(func=no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_message_name_cancel", state=MessagesSG.message_info),
    state=MessagesSG.change_message_name,
    getter=get_message_name

)

change_message_text_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущий текст сообщения:\n<code>{message_text}</code>\n\n' + f'{labels_texts.TEXT_MESSAGE}'),
    TextInput(id="new_message_text_input", type_factory=str, on_success=handlers.update_message_text),
    MessageInput(func=no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_message_text_cancel", state=MessagesSG.message_info),
    state=MessagesSG.change_message_text,
    getter=get_message_text
)

change_message_datetime_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущие дата и время отправки:\n<code>{message_datetime}</code>\n\n' + f'{labels_texts.TIME_SEND_MESSAGE}'),
    TextInput(
        id="new_message_datetime_input",
        type_factory = handlers.datetime_check,
        on_success = handlers.update_message_datetime,
        on_error = handlers.error_datetime
    ),
    MessageInput(func=no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_message_datetime_cancel", state=MessagesSG.message_info),
    state=MessagesSG.change_message_datetime,
    getter=get_message_datetime
)


confirm_del_message_window = Window(
    Format('⚠️ Вы точно хотите удалить сообщение "{message_name}"?'),  # TODO: изменить на название
    Row(
        Button(text=Const(buttons_texts.YES), id="btn_del_message_yes", on_click=handlers.del_message),
        SwitchTo(text=Const(buttons_texts.NO), id="btn_del_message_no", state=MessagesSG.message_info),
    ),
    state=MessagesSG.del_message_confirm,
    getter=get_message_name,
)

del_message_done_window = Window(
    Format('✅ Сообщение "{message_name}" успешно удалено!'),
    # TODO: изменить на название
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_copy_message_done_chat_cancel", state=MessagesSG.start),
    state=MessagesSG.del_message_done,
    getter=get_message_name,
)

change_chat_name = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущее название чата:\n<code>{chat_name}</code>\n\n' +
           f'{labels_texts.CHAT_NAME_INFO}\n\n'
           f'{labels_texts.CHAT_NAME}'),
    TextInput(id="new_chat_name_input", type_factory=str, on_success=handlers.update_chat_name),
    MessageInput(func=no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_chat_name_cancel", state=MessagesSG.start),
    state=MessagesSG.change_chat_name,
    getter=get_chat_name,
)


find_message_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.FIND_MESSAGE),
    TextInput(id="chat_input", type_factory=str, on_success=handlers.find_message),
    MessageInput(func=no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_find_messages_cancel", state=MessagesSG.start),
    state=MessagesSG.find_messages,
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
            on_click=handlers.set_message_info,  # TODO: добавить открытие информации о сообщении
        ),
        id="found_messages_paginator",
        width=buttons_texts.COUNT_MESSAGES_WIDTH,
        height=buttons_texts.COUNT_MESSAGES_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_found_messages_cancel", state=MessagesSG.start),
    state=MessagesSG.found_messages,
    getter=get_found_messages,
)



chats_messages_dialog = Dialog(
    main_window,
    list_messages_windows,
    add_message_name_window,
    add_message_text_window,
    add_message_datetime_window,
    message_info_window,
    confirm_del_message_window,
    del_message_done_window,
    change_message_name_window,
    change_message_text_window,
    change_message_datetime_window,
    change_chat_name,
    find_message_window,
    found_messages_window

)