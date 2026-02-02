from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.recovery.recovery_users import getters, handlers
from app.bot.dialogs.states import RecoverySG

recovery_users_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.RECOVERY_USERS),
    ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='users',
            item_id_getter=lambda x: x[1],
            items='list_users',
            on_click=handlers.set_user_for_recovery,
        ),
        id='users_paginator',
        hide_on_single_page=True,
        width=buttons_texts.COUNT_USERS_WIDTH,
        height=buttons_texts.COUNT_USERS_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id='btn_users_cancel', state=RecoverySG.start),
    state=RecoverySG.recovery_users,
    getter=getters.get_del_users,
)

confirm_recovery_user_window = Window(
    Format(
        '⬇️ Информация о пользователе\n\n'
        'ℹ️ {recovery_username}\n'
        '🆔 {recovery_user_id}\n'
        '🎭 {recovery_user_role}\n'
        '💫 {recovery_user_status}\n\n'
        '⚠️ Вы точно хотите восстановить пользователя?'
    ),
    Row(
        Button(text=Const(buttons_texts.YES), id='btn_recovery_user_yes', on_click=handlers.recovery_user),
        SwitchTo(text=Const(buttons_texts.NO), id='btn_recovery_user_no', state=RecoverySG.recovery_users),
    ),
    state=RecoverySG.confirm_recovery_user,
    getter=getters.get_recovery_user,
)

recovery_user_done_window = Window(
    Format('✅ Пользователь "{recovery_username}" успешно восстановлен!'),
    SwitchTo(Const(buttons_texts.CANCEL), id='btn_recovery_user_cancel', state=RecoverySG.recovery_users),
    state=RecoverySG.recovery_user_done,
    getter=getters.get_recovery_user,
)
