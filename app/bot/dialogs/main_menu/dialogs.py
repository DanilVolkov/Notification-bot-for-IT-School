from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Const

from app.bot.dialogs.states import MainMenuSG

main_menu_dialog = Dialog(
    Window(
        Const('Привет!'),
        Group(
            Button(
                text=Const('Пользователи'),
                id='btn_users',
            ),
            Button(
                text=Const('Аккаунт'),
                id='btn_account',
            ),
            Button(
                text=Const('Чаты'),
                id='btn_chats',
            ),
            Button(
                text=Const('FAQ'),
                id='btn_faq',
            ),
            width=2,
        ),
        state=MainMenuSG.main_menu
    ),
)
