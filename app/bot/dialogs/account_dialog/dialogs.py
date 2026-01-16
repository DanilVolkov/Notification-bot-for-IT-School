from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const

from app.bot.consts.buttons_texts import CANCEL
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.account_dialog.getters import get_account
from app.bot.dialogs.states import AccountSG

account_dialog = Dialog(
    Window(
        Format('Личный кабинет\n\nℹ️ {user}\n🆔 {user_id}\n🔑 {user_role}'),
        StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
        Cancel(Const(CANCEL), id='btn_account_cancel'),
        getter=get_account,
        state=AccountSG.start
    )
)