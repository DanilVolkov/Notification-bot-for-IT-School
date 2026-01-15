import logging
from typing import Callable

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Group, Button, Start, Cancel, ScrollingGroup, Select, NumberedPager, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts.label_texts import MAIN_MENU_TEXT
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.chats.getters import get_chats, get_copy_chats_name
from app.bot.dialogs.chats.handlers import chat_copy_from, chat_copy_in
from app.bot.dialogs.states import MenuSG, AccountSG, ChatsSG
from app.bot.consts import button_texts, label_texts
from app.bot.handlers.start_session import start_session_router


main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Group(
        SwitchTo(
            text=Const(button_texts.ADD_CHAT),
            id='btn_add_chat',
            state=ChatsSG.add_chat
        ),
        SwitchTo(
            text=Const(button_texts.DEL_CHAT),
            id='btn_del_chat',
            state=ChatsSG.del_chat
        ),
        width=2
    ),
    Button(
        text=Const(button_texts.FIND_CHAT),
        id='btn_search_chat',
        #state=ChatsSG.search_chat
    ),
    SwitchTo(
        text=Const(button_texts.COPY_MESSAGES),
        id='btn_copy_messages',
        state=ChatsSG.copy_messages_from_chat
    ),
    ScrollingGroup( # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats",
            item_id_getter=lambda x: x[1],  # TODO: доделать поиск чата по его id для подгрузки данных в него
            items="list_chats",
        ),
        id='chats_paginator',
        width=1,
        height=8,

    ),
    Cancel(Const(button_texts.CANCEL), id='btn_chats_cancel'),
    state=ChatsSG.start,
    getter=get_chats
)

add_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(label_texts.ADD_CHATS),
    SwitchTo(Const(button_texts.CANCEL), id='btn_add_chat_cancel', state=ChatsSG.start),
    state=ChatsSG.add_chat
)

del_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(label_texts.DEL_CHAT),
    ScrollingGroup( # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats_for_del",
            item_id_getter=lambda x: x[1],  # TODO: доделать удаление чата по его id
            items="list_chats",
        ),
        id='chats_paginator_for_del',
        width=1,
        height=8,
    ),
    SwitchTo(Const(button_texts.CANCEL), id='btn_del_chat_cancel', state=ChatsSG.start),
    state=ChatsSG.del_chat,
    getter=get_chats
)


copy_message_from_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(label_texts.COPY_CHAT_FROM),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats_for_copy_message_from",
            item_id_getter=lambda x: x[1],  # TODO: доделать копирование сообщений чата по его id
            items="list_chats",
            on_click=chat_copy_from
        ),
        id='chats_paginator_for_copy_message_from',
        width=1,
        height=8,
    ),
    SwitchTo(Const(button_texts.CANCEL), id='btn_copy_message_from_chat_cancel', state=ChatsSG.start),
    state=ChatsSG.copy_messages_from_chat,
    getter=get_chats
)

copy_message_in_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(label_texts.COPY_CHAT_IN),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats_for_copy_message_in",
            item_id_getter=lambda x: x[1],  # TODO: доделать копирование сообщений чата по его id
            items="list_chats",
            on_click=chat_copy_in
        ),
        id='chats_paginator_for_copy_message_in',
        width=1,
        height=8,
    ),
    SwitchTo(Const(button_texts.CANCEL), id='btn_copy_message_in_chat_cancel', state=ChatsSG.copy_messages_from_chat),
    state=ChatsSG.copy_messages_in_chat,
    getter=get_chats
)


copy_message_done_window = Window(
    Format('Сообщения успешно скопированы из чата {chat_from_id} в чат {chat_in_id}'),
    SwitchTo(Const(button_texts.CANCEL), id='btn_copy_message_done_chat_cancel', state=ChatsSG.start),
    state=ChatsSG.copy_messages_done,
    getter=get_copy_chats_name

)

chats_dialog = Dialog(
    main_window,
    add_chat_window,
    del_chat_window,
    copy_message_from_chat_window,
    copy_message_in_chat_window,
    copy_message_done_window

)

