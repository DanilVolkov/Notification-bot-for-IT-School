from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Row, SwitchTo, Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from app.bot.consts import buttons_texts
from app.bot.consts.buttons_texts import CANCEL
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.account_dialog import handlers
from app.bot.dialogs.account_dialog.getters import get_account
from app.bot.dialogs.states import AccountSG

account_dialog = Dialog(
    Window(
        StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
        Format('⬇️ Информация о пользователе\n\nℹ️ {user_fio}\n🆔 {user_id}\n🎭 {user_role}\n💫 {user_status}',
            when=F['is_admin']
        ),
        Format("Личный кабинет\n\nℹ️ {user_fio}\n🆔 {user_id}\n🔑 {user_role}",
            when=~F['is_admin']
        ),
        Row(
            Button(Const(buttons_texts.ACTIVATE_USER),
                 id='btn_status_user_block',
                 #on_click=handlers.,  # TODO: доделать бан
                 when=F['is_admin'] & ~F['is_find_user_creator'] & F["user_blocked"]
            ),
            Button(Const(buttons_texts.BLOCK_USER),
                 id='btn_status_user_active',
                 #on_click=handlers.,# TODO: доделать разблокировку
                 when=F['is_admin'] & ~F['is_find_user_creator'] & ~F["user_blocked"]
            ),
            Button(Const(buttons_texts.DEL_USER),
                   id='btn_del_user',
                   #on_click=, # TODO: доделать удаление
                   when=F['is_admin'] & ~F['is_find_user_creator'])
        ),  # TODO: доделать смену ФИО/роли
        Cancel(Const(CANCEL), id='btn_account_cancel'),
        getter=get_account,
        state=AccountSG.start,
    )
)

# TODO: сделать кнопку восстановления файлов для админов, создателей и прокураторов
