from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from app.bot.consts import labels_texts, buttons_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.recovery import getters
from app.bot.dialogs.states import RecoverySG

# TODO: на каждое восстановление - своё окно. В сообщениях пишем сокращенно название чата и название сообщения.
# TODO: в сообщение можно зайти и посмотреть о нём доп. инфу
# TODO: сделать также поиск чатов и сообщений
main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.RECOVERY_INFO),
    # Start(
    #     text=Const(buttons_texts.RECOVERY_USERS),
    #     id='btn_recovery_users',
    #     when='is_admin',
    #     state=RecoverySG.recovery_users
    # ),
    state=RecoverySG.start,
    getter=getters.get_user
)


recovery_dialog = Dialog(
    main_window,
)