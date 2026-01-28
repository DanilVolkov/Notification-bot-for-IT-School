from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group, Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const
from magic_filter import F

from app.bot.consts import buttons_texts
from app.bot.consts.labels_texts import MAIN_MENU_TEXT
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.main_menu import getters, handlers
from app.bot.dialogs.states import ChatsSG, MenuSG, RecoverySG, UsersSG

main_menu_dialog = Dialog(
    Window(
        StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
        Const(MAIN_MENU_TEXT),
        Group(
            Start(
                text=Const(buttons_texts.MAIN_MENU_USERS),
                id='btn_main_menu_users',
                when='is_admin',
                state=UsersSG.start,
            ),
            Button(
                text=Const(buttons_texts.MAIN_MENU_ACCOUNTS),
                id='btn_main_menu_account',
                on_click=handlers.start_account_dialog,
            ),
            Start(text=Const(buttons_texts.MAIN_MENU_CHATS), id='btn_main_menu_chats', state=ChatsSG.start),
            Button(text=Const(buttons_texts.MAIN_MENU_FAQ), id='btn_main_menu_faq'),  # TODO: доделать меню FAQ
            Start(
                text=Const(buttons_texts.MAIN_MENU_RECOVERY),
                id='btn_main_menu_recovery',
                when=F['is_admin'] | F['is_procurator'],
                state=RecoverySG.start,
            ),  # TODO: сделать кнопку восстановления файлов для админов, создателей и прокураторов
            width=2,
        ),
        state=MenuSG.start,
        getter=getters.get_user,
    ),
)
