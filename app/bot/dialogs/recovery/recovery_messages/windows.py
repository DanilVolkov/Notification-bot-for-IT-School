from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Row,
    ScrollingGroup,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.recovery.recovery_messages import getters, handlers
from app.bot.dialogs.states import RecoverySG

list_chats_recovery_messages_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.CHATS_WITH_DEL_MESSAGES),
    ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='chats',
            item_id_getter=lambda x: x[1],
            items='list_chats',
            on_click=handlers.set_chat_messages_for_recovery,
        ),
        id='chats_paginator',
        hide_on_single_page=True,
        width=buttons_texts.COUNT_MESSAGES_WIDTH,
        height=buttons_texts.COUNT_MESSAGES_HEIGHT,
    ),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_list_recovery_chats_msg_cancel',
        state=RecoverySG.start,
    ),
    state=RecoverySG.recovery_messages,
    getter=getters.get_chats_del_messages,
)


list_del_messages_in_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('💬 {chat_recovery_msgs_name}\n'),
    Const(
        labels_texts.RECOVERY_MESSAGES, when=~F['is_chat_recovery_msgs_del']
    ),
    Const(
        labels_texts.RECOVERY_MESSAGES_FOR_DEL_CHAT,
        when='is_chat_recovery_msgs_del',
    ),
    ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='messages',
            item_id_getter=lambda x: x[1],
            items='del_messages',
            on_click=handlers.set_del_message_info,
        ),
        id='messages_paginator',
        hide_on_single_page=True,
        width=buttons_texts.COUNT_MESSAGES_WIDTH,
        height=buttons_texts.COUNT_MESSAGES_HEIGHT,
    ),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_list_recovery_msgs_cancel',
        state=RecoverySG.recovery_messages,
    ),
    state=RecoverySG.list_del_messages_in_chat,
    getter=getters.get_chat_messages_for_recovery,
)


confirm_recovery_message_window = Window(
    Format('{recovery_message_info}\n'),
    Const(
        labels_texts.RECOVERY_MESSAGE_CONFIRM,
        when=~F['is_chat_recovery_msgs_del'],
    ),
    Row(
        Button(
            text=Const(buttons_texts.YES),
            id='btn_recovery_message_yes',
            on_click=handlers.recovery_message,
        ),
        SwitchTo(
            text=Const(buttons_texts.NO),
            id='btn_recovery_message_no',
            state=RecoverySG.list_del_messages_in_chat,
        ),
        when=~F['is_chat_recovery_msgs_del'],
    ),
    SwitchTo(
        text=Const(buttons_texts.CANCEL),
        id='btn_list_recovery_msg_cancel',
        when=F['is_chat_recovery_msgs_del'],
        state=RecoverySG.list_del_messages_in_chat,
    ),
    state=RecoverySG.confirm_recovery_messages,
    getter=getters.get_recovery_message_info,
)


recovery_messages_done_window = Window(
    Format('{recovery_message_info}\n'),
    Const(labels_texts.RECOVERY_MESSAGE_DONE),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_recovery_msg_cancel',
        state=RecoverySG.list_del_messages_in_chat,
    ),
    state=RecoverySG.recovery_message_done,
    getter=getters.get_recovery_message_info,
)
