import logging
from typing import Callable

from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Group, Button, Start, Cancel
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts.label_texts import MAIN_MENU_TEXT
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.states import MenuSG, AccountSG
from app.bot.consts.button_texts import MAIN_MENU_USERS, MAIN_MENU_CHATS, MAIN_MENU_ACCOUNTS, MAIN_MENU_FAQ
from app.bot.handlers.start_session import start_session_router



main_menu_dialog = Dialog(
    Window(
        StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
        Group(
            Button(
                text=Const(MAIN_MENU_USERS),
                id='btn_main_menu_users',
            ),
            Start(
                text=Const(MAIN_MENU_ACCOUNTS),
                id='btn_main_menu_account',
                state=AccountSG.start
            ),
            Button(
                text=Const(MAIN_MENU_CHATS),
                id='btn_main_menu_chats',
            ),
            Button(
                text=Const(MAIN_MENU_FAQ),
                id='btn_main_menu_faq',
            ),
            width=2,
        ),
        state=MenuSG.main_menu
    ),
)


