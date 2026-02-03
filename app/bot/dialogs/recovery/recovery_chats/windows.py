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

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.recovery.recovery_chats import getters, handlers
from app.bot.dialogs.states import RecoverySG

list_recovery_chats_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.RECOVERY_CHATS),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format('{item[0]}'),
            id='chats',
            item_id_getter=lambda x: x[
                1
            ],  # TODO: доделать поиск чата по его id для подгрузки данных в него
            items='list_chats',
            on_click=handlers.set_chat_for_recovery,
        ),
        id='chats_paginator',
        hide_on_single_page=True,
        width=buttons_texts.COUNT_CHATS_WIDTH,
        height=buttons_texts.COUNT_CHATS_HEIGHT,
    ),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_list_recovery_chats_cancel',
        state=RecoverySG.start,
    ),
    state=RecoverySG.recovery_chats,
    getter=getters.get_del_chats,
)

recovery_messages_for_chat_window = Window(
    Format(
        '💬 {recovery_chat_name}\n\n'
        '⬇️ Выберите, что сделать с сообщениями в чате:'
    ),
    Button(
        text=Const(buttons_texts.RECOVERY_MESSAGES_CHAT_WITH_DATES),
        id='btn_recovery_msg_with_dates',
        on_click=handlers.set_recovery_msg_mode,
    ),
    Button(
        text=Const(buttons_texts.RECOVERY_MESSAGES_CHAT_WITHOUT_DATES),
        id='btn_recovery_msg_without_dates',
        on_click=handlers.set_recovery_msg_mode,
    ),
    Button(
        text=Const(buttons_texts.RECOVERY_ONLY_CHAT),
        id='btn_recovery_only_chat',
        on_click=handlers.set_recovery_msg_mode,
    ),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_recovery_messages_for_chat_cancel',
        state=RecoverySG.recovery_chats,
    ),
    state=RecoverySG.recovery_messages_for_chat,
    getter=getters.get_recovery_chat,
)


confirm_recovery_chat_window = Window(
    Format(
        '💬 {recovery_chat_name}\n\n'
        'ℹ️ Режим восстановления: {recovery_mode}\n\n'
        '⚠️ Вы точно хотите восстановить чат с данным режимом?'
    ),
    Row(
        Button(
            text=Const(buttons_texts.YES),
            id='btn_recovery_chat_yes',
            on_click=handlers.recovery_chat,
        ),
        SwitchTo(
            text=Const(buttons_texts.NO),
            id='btn_recovery_chat_no',
            state=RecoverySG.recovery_chats,
        ),
    ),
    state=RecoverySG.confirm_recovery_chat,
    getter=getters.get_recovery_chat,
)

recovery_chat_done_window = Window(
    Format(
        '✅ Чат "{recovery_chat_name}" успешно восстановлен!\n\n'
        'ℹ️ Был применён режим восстановления: {recovery_mode}'
    ),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_recovery_chat_cancel',
        state=RecoverySG.recovery_chats,
    ),
    state=RecoverySG.recovery_chat_done,
    getter=getters.get_recovery_chat,
)
