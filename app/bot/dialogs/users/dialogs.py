from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select, Start, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.states import AddUserSG, UsersSG
from app.bot.dialogs.users import handlers
from app.bot.dialogs.users.getters import get_users

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Start(Const(buttons_texts.ADD_USER), id="btn_add_user", state=AddUserSG.start),
    SwitchTo(Const(buttons_texts.LIST_USERS), id="btn_list_users", state=UsersSG.list_users),
    Cancel(Const(buttons_texts.CANCEL), id="btn_users_cancel"),
    state=UsersSG.start,
)

list_users = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="users",
            item_id_getter=lambda x: x[1],
            items="list_users",
            on_click=handlers.start_account_dialog,
        ),
        id="users_paginator",
        width=buttons_texts.COUNT_USERS_WIDTH,
        height=buttons_texts.COUNT_USERS_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_users_cancel", state=UsersSG.start),
    state=UsersSG.list_users,
    getter=get_users,
)


users_dialog = Dialog(main_window, list_users)
