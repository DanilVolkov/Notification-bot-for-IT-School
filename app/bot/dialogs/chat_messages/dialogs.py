from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.chat_messages.getters import get_chat_info, get_chat_messages
from app.bot.dialogs.states import MessagesSG

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('💬 {chat_name}'),
    Button(
        text=Const(buttons_texts.ADD_MESSAGE),
        id='btn_add_message'
    ),
    Button(
        text=Const(buttons_texts.FIND_MESSAGE),
        id='btn_find_message'
    ),
    Button(
        text=Const(buttons_texts.CHANGE_CHAT_NAME),
        id='btn_change_chat_name'
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
    TextInput(id="chat_input", type_factory=str, on_success=),
    MessageInput(func=),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_name_cancel", state=MessagesSG.start),
    state=MessagesSG.add_message
)


add_message_text_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.NAME_MESSAGE),
    TextInput(id="chat_input", type_factory=str, on_success=),
    MessageInput(func=),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_text_cancel", state=MessagesSG.start),
    state=MessagesSG.add_message
)


add_message_date_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.NAME_MESSAGE),
    TextInput(id="chat_input", type_factory=str, on_success=),
    MessageInput(func=),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_message_date_cancel", state=MessagesSG.start),
    state=MessagesSG.add_message
)  # TODO: после этого окна открывается окно с просмотром сообщения

cancel_add_message_window = Window(

)

message_info_window = Window(

)





chats_messages_dialog = Dialog(
    main_window,
    list_messages_windows,
)