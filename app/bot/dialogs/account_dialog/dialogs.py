from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts.buttons_texts import CANCEL
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.account_dialog.getters import get_account
from app.bot.dialogs.states import AccountSG

account_dialog = Dialog(
    Window(
        StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
        Format(
            '⬇️ Информация о пользователе\n\nℹ️ {user_fio}\n🆔 {user_id}\n🎭 {user_role}\n💫 {user_status}'
        ),  # TODO: показывать только для админа
        # Format("Личный кабинет\n\nℹ️ {user}\n🆔 {user_id}\n🔑 {user_role}"), # TODO: показывать для всех остальных
        Cancel(Const(CANCEL), id='btn_account_cancel'),
        getter=get_account,
        state=AccountSG.start,
    )
)
